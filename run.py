"""Run ADVISOR arms x seeds in parallel.

    uv run python run.py --config configs/smoke.toml --dry          # $0: mock models, whole pipeline
    uv run python run.py --config configs/smoke.toml                # ~$0.10: real API smoke test
    uv run python run.py --config configs/pilot.toml --max_usd 8    # pilot, 3 seeds x all arms
    uv run python run.py --config configs/pilot.toml --arms PC,S-mono --seeds 0 1 2

Results: results/<tag>/<arm>/s<seed>.jsonl (config line, one line per round, summary line).
Re-running the same command resumes partial runs and skips finished ones.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import tomllib
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv

from advisor.arms import ARMS
from advisor.game import GameConfig, run_episode
from advisor.market import LogitMarket
from advisor.prompts import ADVISOR_SYSTEM, FIRM_SYSTEM, advisor_prompt, firm_prompt
from advisor.providers import SPEND, FatalProviderError, make_provider, usd_cost

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def estimate(arms, seeds, cfg: GameConfig, firm_spec, advisor_spec, out_tokens=(60, 700), arm_n=None):
    """Calls and a cost range per arm. Input tokens from rendered full-window prompts (chars/3,
    Haiku 5.5's tokenizer counts ~30% more than chars/4); output tokens are a low/high guess
    (reason line only vs. reason line + low-effort thinking). Replace with measured cost after the smoke run."""
    rows, tot_calls, lo, hi = [], 0, 0.0, 0.0
    for name in arms:
        arm = ARMS[name]
        m = LogitMarket.for_firms(arm.n_firms, cfg.price_scale)
        fake = [{"round": r, "kind": "play", "prices": [1.61] * m.n, "quantities": [38.17] * m.n,
                 "profits": [23.28] * m.n, "recs": [1.6] * m.n} for r in range(1, 41)]
        n_adv = m.n if arm.advisor_calls else 0
        n_firm = m.n if arm.firm_calls else 0
        n_runs = (arm_n or {}).get(name, len(seeds))
        calls = cfg.rounds * (n_adv + n_firm) * n_runs
        tin = 0
        if n_adv:
            tin += n_adv * (len(ADVISOR_SYSTEM[arm.objective]) + len(
                advisor_prompt(0, 41, fake, m.unit_cost, m.p_max, cfg.window, arm.data, cfg.stale_lag, cfg.public_lag))) / 3
        if n_firm:
            rec = 1.6 if arm.advisor else None
            tin += n_firm * (len(FIRM_SYSTEM) + len(
                firm_prompt(0, 41, fake, m.unit_cost, m.p_max, cfg.window, rec, cfg.public_lag))) / 3
        per_round_in = tin
        calls_per_round = n_adv + n_firm
        cost = []
        for spec_mix in out_tokens:
            usd = 0.0
            for spec, k in ((advisor_spec, n_adv), (firm_spec, n_firm)):
                if not k:
                    continue
                share_in = per_round_in * k / max(calls_per_round, 1)
                usd += usd_cost(spec, int(share_in), k * spec_mix)
            cost.append(usd * cfg.rounds * n_runs)
        rows.append((name, calls, cost[0], cost[1]))
        tot_calls += calls
        lo += cost[0]
        hi += cost[1]
    return rows, tot_calls, lo, hi


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--arms", default=None, help="comma-separated subset of the config's arms")
    ap.add_argument("--seeds", type=int, nargs="+", default=None)
    ap.add_argument("--workers", type=int, default=None, help="runs in parallel (default from config)")
    ap.add_argument("--max_usd", type=float, default=None, help="stop launching new runs past this spend")
    ap.add_argument("--model", default=None, help="override firm_model and advisor_model, e.g. deepseek:deepseek-flash")
    ap.add_argument("--tag", default=None, help="override the config's results tag")
    ap.add_argument("--set", nargs="*", default=[], metavar="KEY=VALUE",
                    help="override config values, e.g. --set rounds=40 prior_steps=10 price_scale=3.2")
    ap.add_argument("--dry", action="store_true", help="mock models, $0, writes to results/dry/")
    ap.add_argument("-y", "--yes", action="store_true", help="skip the cost confirmation")
    args = ap.parse_args()

    load_dotenv(os.path.join(HERE, ".env"), override=True)
    c = load_config(args.config)
    for kv in args.set:
        k, _, v = kv.partition("=")
        c[k] = type(c[k])(v) if k in c else (float(v) if "." in v else int(v))
    tag = args.tag or c["tag"]
    arms = args.arms.split(",") if args.arms else c["arms"]
    seeds = args.seeds if args.seeds is not None else c["seeds"]
    workers = args.workers or c.get("workers", 8)
    max_usd = args.max_usd if args.max_usd is not None else c.get("max_usd", 5.0)
    unknown = [a for a in arms if a not in ARMS]
    if unknown:
        sys.exit(f"unknown arms {unknown}; known: {list(ARMS)}")
    cfg = GameConfig(**{k: c[k] for k in GameConfig.__dataclass_fields__ if k in c})
    firm_spec = "mock" if args.dry else (args.model or c["firm_model"])
    advisor_spec = "mock" if args.dry else (args.model or c["advisor_model"])
    out_root = os.path.join(HERE, "results", "dry" if args.dry else "", tag)

    rows, calls, lo, hi = estimate(arms, seeds, cfg, firm_spec, advisor_spec,
                                   arm_n={a: len(c.get("arm_seeds", {}).get(a, seeds)) for a in arms})
    print(f"{tag}: {len(arms)} arms x {len(seeds)} seeds x {cfg.rounds} rounds | firm={firm_spec} advisor={advisor_spec}")
    for name, n, a, b in rows:
        print(f"   {name:7s} {n:6d} calls   est ${a:6.2f} - ${b:6.2f}")
    print(f"   total  {calls:6d} calls   est ${lo:6.2f} - ${hi:6.2f}   (budget cap ${max_usd:.2f})")
    if not args.dry and not args.yes:
        if input("Proceed? [y/N] ").strip().lower() != "y":
            sys.exit("aborted")

    try:
        firm = make_provider(firm_spec, effort=c.get("effort", "low"), max_tokens=c.get("max_tokens", 4096))
        adv = make_provider(advisor_spec, effort=c.get("effort", "low"), max_tokens=c.get("max_tokens", 4096))
    except FatalProviderError as e:
        sys.exit(f"provider error: {e}")

    # seed per-provider lifetime spend from every run file already on disk, so caps hold across invocations
    import glob, json
    for path in glob.glob(os.path.join(HERE, "results", "**", "s*.jsonl"), recursive=True):
        if ".thoughts." in path or os.sep + "dry" + os.sep in path:
            continue
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                r = json.loads(line)
                if r.get("type") != "round":
                    continue
                for call in r.get("calls", []):
                    am = str(call.get("api_model") or "")
                    kind = "deepseek" if am.startswith("deepseek") else "openai" if am.startswith(("gpt", "o3", "o4")) else None
                    if kind:
                        u = call["usage"]
                        SPEND.by_provider[kind] = SPEND.by_provider.get(kind, 0.0) + u["usd"]
                        if u.get("utc_day"):
                            key = (kind, u["utc_day"])
                            SPEND.day_tokens[key] = SPEND.day_tokens.get(key, 0) + u["tokens_in"] + u["tokens_out"]
    if SPEND.by_provider:
        print("   lifetime spend already recorded:", {k: round(v, 2) for k, v in SPEND.by_provider.items()},
              "| tokens by UTC day:", SPEND.day_tokens)

    # seed-major so partial batches cover all arms; arm_seeds (optional) gives an arm its own seed list
    arm_seeds = {a: c.get("arm_seeds", {}).get(a, seeds) for a in arms} if args.seeds is None else {a: seeds for a in arms}
    all_seeds = sorted({s for v in arm_seeds.values() for s in v})
    jobs = [(a, s) for s in all_seeds for a in arms if s in arm_seeds[a]]
    t0 = time.time()
    done, failed, skipped = 0, [], []
    meta = {"tag": tag, "config_file": os.path.relpath(args.config, HERE), "effort": c.get("effort", "low")}

    def job(arm_name, seed):
        if SPEND.usd >= max_usd:
            return arm_name, seed, None, "budget"
        path = os.path.join(out_root, arm_name, f"s{seed}.jsonl")
        try:
            s = run_episode(ARMS[arm_name], seed, cfg, path, firm, adv, meta)
            return arm_name, seed, s, None
        except Exception as e:  # noqa: BLE001  (logged and reported; the run file stays resumable)
            return arm_name, seed, None, f"{type(e).__name__}: {e}"

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(job, a, s) for a, s in jobs]
        for f in as_completed(futs):
            a, s, summ, err = f.result()
            if err == "budget":
                skipped.append((a, s))
                continue
            if err:
                failed.append((a, s, err))
                print(f"   FAIL {a} s{s}: {err[:300]}")
                continue
            done += 1
            extra = ""
            if "follow_rate_lastk" in summ:
                extra = f" follow {summ['follow_rate_lastk']:.2f} rec {summ['rec_lastk']:.3f}"
            print(f"   done {a:7s} s{s}: delta {summ['delta_lastk']:+.3f} price {summ['price_lastk']:.3f}"
                  f"{extra} retries {summ['retries']} ${summ['usd']:.3f}   [total ${SPEND.usd:.2f}, "
                  f"{done}/{len(jobs)}, {time.time() - t0:.0f}s]")

    print(f"\nfinished {done}/{len(jobs)} runs in {time.time() - t0:.0f}s; spend ${SPEND.usd:.3f} "
          f"({SPEND.calls} calls, {SPEND.tokens_in} in / {SPEND.tokens_out} out tokens)")
    if SPEND.calls:
        print(f"   per call: {SPEND.tokens_in / SPEND.calls:.0f} in, {SPEND.tokens_out / SPEND.calls:.0f} out, "
              f"${SPEND.usd / SPEND.calls:.5f}")
    if skipped:
        print(f"   skipped (budget cap): {len(skipped)} runs; re-run with a higher --max_usd to continue")
    if failed:
        print(f"   FAILED: {len(failed)} runs (files are resumable):")
        for a, s, e in failed:
            print(f"      {a} s{s}: {e[:200]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
