"""One episode: warm-up round near Nash, then `rounds` rounds of (advisor ->) firm pricing.

Run files are JSONL: a config line, one line per round, and a summary line when complete. A partial
file is resumed: the market is deterministic given prices, so the history is rebuilt from the file.
A call that cannot be parsed after all retries aborts the run (no substituted price is ever recorded).
"""

from __future__ import annotations

import json
import math
import os
import random
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from typing import List, Optional

import numpy as np

from .arms import Arm
from .market import LogitMarket
from .prompts import ADVISOR_SYSTEM, FIRM_SYSTEM, advisor_prompt, firm_prompt
from .providers import FatalProviderError, Refusal, parse_answer


@dataclass
class GameConfig:
    rounds: int = 100
    window: int = 20
    stale_lag: int = 10
    public_lag: int = 0  # 0 = competitor prices are non-public; L > 0 shows them with an L-round lag
    prior_steps: int = 1
    max_retries: int = 3
    last_k: int = 20  # rounds in the primary metric
    price_scale: float = 1.0  # alpha (Fish et al.): all prices and costs scaled
    demand_noise: float = 0.0  # sd of i.i.d. log-normal quantity shocks per firm-round (0 = noiseless)
    show_wtp: bool = True  # "No customer would pay more than $X" line (confound check C1: False removes it)


class AgentCallError(RuntimeError):
    pass


def ask(provider, system: str, user: str, role: str, max_retries: int) -> dict:
    """One decision with parse retries. Returns price, reason, attempts, summed usage, and the raw answer
    plus the model's reasoning text (written to the run's .thoughts.jsonl sidecar, not the main file)."""
    usage_total = {"tokens_in": 0, "tokens_out": 0, "cache_hit": 0, "usd": 0.0, "latency_s": 0.0}
    failures, refusals, api_model = [], 0, None
    for attempt in range(1, max_retries + 2):
        try:
            text, usage = provider.complete(system, user)
        except Refusal as e:
            refusals += 1
            failures.append(f"refusal: {e}")
            continue
        for k in usage_total:
            usage_total[k] += usage.get(k, 0) or 0
        api_model = usage.get("api_model")
        if usage.get("utc_day"):
            usage_total["utc_day"] = usage["utc_day"]
        price, reason = parse_answer(text, role)
        if price is not None and 0 < price < 10:
            return {"price": price, "reason": reason, "attempts": attempt, "refusals": refusals,
                    "usage": usage_total, "stop_reason": usage.get("stop_reason"), "api_model": api_model,
                    "text": text, "reasoning": usage.get("reasoning", ""), "failed": failures}
        failures.append(text[-400:])
    raise AgentCallError(f"{getattr(provider, 'spec', provider)} {role}: no valid price after "
                         f"{max_retries + 1} attempts; last: {failures[-1]!r}")


def _read(path: str) -> List[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _append(path: str, rec: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def summarize_rounds(rounds: List[dict], market: LogitMarket, last_k: int) -> dict:
    llm = [r for r in rounds if r["kind"] == "play"]
    tail = llm[-last_k:]
    prices = np.array([r["prices"] for r in tail])
    gains = np.array([r["gains"] for r in tail])
    out = {
        "rounds_played": len(llm),
        "delta_lastk": float(gains.mean()),  # market profit gain over the last k rounds
        "price_lastk": float(prices.mean()),
        "price_lastk_by_firm": prices.mean(axis=0).round(4).tolist(),
    }
    recs = [r for r in tail if r.get("recs") is not None]
    if recs:
        idx = [i for i, v in enumerate(recs[0]["recs"]) if v is not None]
        p = np.array([[r["prices"][i] for i in idx] for r in recs])
        rc = np.array([[r["recs"][i] for i in idx] for r in recs])
        out["rec_lastk"] = float(rc.mean())
        out["abs_dev_from_rec_lastk"] = float(np.abs(p - rc).mean())
        out["follow_rate_lastk"] = float((np.abs(p - rc) <= 0.01).mean())
    calls = [c for r in llm for c in r.get("calls", [])]
    out["calls"] = len(calls)
    out["retries"] = sum(c["attempts"] - 1 for c in calls)
    out["usd"] = round(sum(c["usage"]["usd"] for c in calls), 5)
    out["tokens_in"] = sum(c["usage"]["tokens_in"] for c in calls)
    out["tokens_out"] = sum(c["usage"]["tokens_out"] for c in calls)
    return out


def run_episode(arm: Arm, seed: int, cfg: GameConfig, path: str, firm_provider, advisor_provider,
                meta: Optional[dict] = None) -> dict:
    market = LogitMarket.for_firms(arm.n_firms, cfg.price_scale)
    prior_steps = arm.prior_steps if arm.prior_steps is not None else cfg.prior_steps

    def shocks(t):  # deterministic per (seed, round), so resumed runs see the same demand draws
        if cfg.demand_noise <= 0:
            return None
        g = random.Random(seed * 7919 + t * 31 + 17)
        return [math.exp(g.gauss(0.0, cfg.demand_noise)) for _ in range(arm.n_firms)]
    n = market.n
    records = _read(path)
    if records and records[0].get("arm") != arm.name:
        raise RuntimeError(f"{path} belongs to arm {records[0].get('arm')}, not {arm.name}")
    def _cfg_matches(old: dict) -> bool:  # fields added after a run started must still be at their defaults
        new = asdict(cfg)
        return all(new.get(k) == v for k, v in old.items()) and all(
            k in old or new[k] == GameConfig.__dataclass_fields__[k].default for k in new)

    if records and (not _cfg_matches(records[0].get("game", {})) or records[0].get("arm_spec") != asdict(arm)):
        raise RuntimeError(f"{path} was started with a different config; use a new --tag or delete the file")
    if records and records[-1].get("type") == "summary":
        return records[-1]
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not records:
        header = {"type": "config", "arm": arm.name, "arm_spec": asdict(arm), "seed": seed,
                  "game": asdict(cfg), "market": {"n": n, "a": market.a, "mu": market.mu, "c": market.unit_cost, "alpha": market.alpha,
                                                  "p_nash": market.p_nash, "p_mono": market.p_mono,
                                                  "pi_nash": market.pi_nash, "pi_mono": market.pi_mono},
                  "firm_model": firm_provider.spec if arm.firm_calls else None,
                  "advisor_model": advisor_provider.spec if arm.advisor_calls else None,
                  **(meta or {})}
        _append(path, header)
        rng = random.Random(seed)
        for r in range(1, prior_steps + 1):  # llm-cartel warm-up: Nash +/- 0.05
            prices = [round(market.p_nash + market.alpha * (rng.randint(0, 11) - 5) / 100, 2) for _ in range(n)]
            rec = _round_record(r, "warmup", prices, market, None, [], [], [], shocks(r))
            _append(path, rec)
        records = _read(path)

    history = [r for r in records if r.get("type") == "round"]
    static_price = None
    if arm.advisor == "static":
        static_price = round(market.p_nash if arm.static == "nash" else market.p_mono, 2)

    thoughts_path = path.replace(".jsonl", ".thoughts.jsonl")
    public_lag = arm.public_lag if arm.public_lag is not None else cfg.public_lag
    announced = arm.cap if arm.announce_cap else None
    pool = ThreadPoolExecutor(max_workers=n)
    try:
        total = prior_steps + cfg.rounds
        for t in range(len(history) + 1, total + 1):
            calls = []
            # 1) recommendations
            recs, rec_reasons = None, None
            if arm.advisor == "static":
                recs = [static_price] * n
            elif arm.advisor == "br":
                last = history[-1]["prices"]
                recs = [round(market.best_response([p for j, p in enumerate(last) if j != i]), 2)
                        for i in range(n)]
            elif arm.advisor == "jbr":
                recs = []
                for i in range(n):
                    if arm.data == "current":
                        seen = history[-1]["prices"]
                    elif arm.data == "stale":
                        old = [h for h in history if h["round"] <= t - cfg.stale_lag]
                        seen = old[-1]["prices"] if old else [market.p_nash] * n
                    else:
                        seen = [market.p_nash] * n
                    recs.append(round(market.joint_best_response([p for j, p in enumerate(seen) if j != i]), 2))
            elif arm.advisor == "llm":
                system = ADVISOR_SYSTEM[arm.objective]
                adv_ids = [i for i in range(n) if arm.advised is None or arm.advised[i]]
                prompts = [advisor_prompt(i, t, history, market.unit_cost, market.p_max if cfg.show_wtp else None,
                                          cfg.window, arm.data, cfg.stale_lag, public_lag) for i in adv_ids]
                outs = list(pool.map(lambda u: ask(advisor_provider, system, u, "advisor", cfg.max_retries),
                                     prompts))
                recs, rec_reasons = [None] * n, [None] * n
                for i, o in zip(adv_ids, outs):
                    recs[i], rec_reasons[i] = o["price"], o["reason"]
                calls += [{"who": f"advisor{i}", **o} for i, o in zip(adv_ids, outs)]

            # 2) prices
            firm_reasons = None
            accepted = None
            if arm.accept_prob is not None:
                draw = random.Random(seed * 100003 + t)
                accepted = [draw.random() < arm.accept_prob for _ in range(n)]
            if arm.advised is not None:  # advised firms follow arm.adherence; others always decide alone
                deciders = [i for i in range(n) if not (arm.advised[i] and arm.adherence == "auto")]
                prompts = [firm_prompt(i, t, history, market.unit_cost, market.p_max if cfg.show_wtp else None,
                                       cfg.window, recs[i] if recs else None, public_lag, announced)
                           for i in deciders]
                outs = list(pool.map(lambda u: ask(firm_provider, FIRM_SYSTEM, u, "firm", cfg.max_retries), prompts))
                prices = [recs[i] if recs else None for i in range(n)]
                firm_reasons = [None] * n
                for i, o in zip(deciders, outs):
                    prices[i], firm_reasons[i] = o["price"], o["reason"]
                calls += [{"who": f"firm{i}", **o} for i, o in zip(deciders, outs)]
            elif arm.adherence == "auto":
                prices = list(recs)
            elif accepted is not None:
                deciders = [i for i in range(n) if not accepted[i]]
                prompts = [firm_prompt(i, t, history, market.unit_cost, market.p_max if cfg.show_wtp else None,
                                       cfg.window, recs[i], public_lag, announced) for i in deciders]
                outs = list(pool.map(lambda u: ask(firm_provider, FIRM_SYSTEM, u, "firm", cfg.max_retries), prompts))
                prices = list(recs)
                firm_reasons = [None] * n
                for i, o in zip(deciders, outs):
                    prices[i] = o["price"]
                    firm_reasons[i] = o["reason"]
                calls += [{"who": f"firm{i}", **o} for i, o in zip(deciders, outs)]
            else:
                prompts = [firm_prompt(i, t, history, market.unit_cost, market.p_max if cfg.show_wtp else None, cfg.window,
                                       recs[i] if recs else None, public_lag, announced) for i in range(n)]
                outs = list(pool.map(lambda u: ask(firm_provider, FIRM_SYSTEM, u, "firm", cfg.max_retries),
                                     prompts))
                prices = [o["price"] for o in outs]
                firm_reasons = [o["reason"] for o in outs]
                calls += [{"who": f"firm{i}", **o} for i, o in enumerate(outs)]

            chosen = list(prices)
            if arm.cap is not None:
                prices = [min(p, arm.cap) for p in prices]
            rec = _round_record(t, "play", prices, market, recs, rec_reasons, firm_reasons, calls, shocks(t))
            if arm.cap is not None:
                rec["chosen"] = chosen
            if accepted is not None:
                rec["accepted"] = accepted
            if calls:
                _append(thoughts_path, {"round": t, "calls": [
                    {"who": c["who"], "text": c["text"], "reasoning": c["reasoning"], "failed": c["failed"]}
                    for c in calls]})
            _append(path, rec)
            history.append(rec)
    finally:
        pool.shutdown(wait=False)

    summary = {"type": "summary", "arm": arm.name, "seed": seed,
               **summarize_rounds(history, market, cfg.last_k)}
    _append(path, summary)
    return summary


def _round_record(t, kind, prices, market, recs, rec_reasons, firm_reasons, calls, shock=None) -> dict:
    """Quantities and profits shown to agents include demand shocks; gains (the metric) are the expected,
    noise-free profit gains at these prices."""
    q = market.quantities(prices)
    if shock is not None:
        q = q * np.array(shock)
    pi = q * (np.asarray(prices, dtype=float) - market.unit_cost)
    g = market.gains(prices)
    return {"type": "round", "round": t, "kind": kind, "prices": [float(p) for p in prices],
            "quantities": [round(float(x), 4) for x in q], "profits": [round(float(x), 4) for x in pi],
            "gains": [round(float(x), 4) for x in g], "recs": recs, "rec_reasons": rec_reasons,
            "firm_reasons": firm_reasons, "shocks": shock,
            "calls": [{k: v for k, v in c.items() if k not in ("reason", "text", "reasoning", "failed")} for c in calls]}


__all__ = ["GameConfig", "run_episode", "AgentCallError", "FatalProviderError", "summarize_rounds"]
