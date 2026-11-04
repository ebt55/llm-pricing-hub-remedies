"""Recompute the numbers behind the 4 Nov 2026 corrections ($0, existing logs; Appendix G of report/draft.md).

    uv run python tools/corrections_check.py

1. Acceptance of 1-2 cent recommended increases on the +1 cent ratchet (K1-d) only, per firm model. A decision is
   accepted if the firm's price equals the recommendation to the cent (as in tools/ratchet_curve.py, which pools
   every ratchet step size and so mixes in Gemini Flash-Lite's +3 and +10 cent runs).
2. Share of harm removed by the data ban (M0-a) and stale data (M1-a), on profit gain and on the price index
   (p - p_N) / (p_M - p_N), which does not fall again above p_M. Bootstrap 95% CI: 4,000 draws, seed 0.
3. Rounds for a per-round clip band to lift a price from warm-up levels to 0.95 * p_M, with cent rounding.
"""

from __future__ import annotations

import glob
import json
import os
import random
import statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def runs(tag: str, arm: str):
    for f in sorted(glob.glob(os.path.join(ROOT, "results", tag, arm, "s*.jsonl"))):
        if ".thoughts." in f:
            continue
        rows = [json.loads(line) for line in open(f, encoding="utf-8")]
        if any(r.get("type") == "summary" for r in rows):
            yield rows


def acceptance(tag: str, arm: str = "K1-d"):
    k = n = 0
    for rows in runs(tag, arm):
        rounds = [r for r in rows if r.get("type") == "round"]
        for a, b in zip(rounds, rounds[1:]):
            if b.get("kind") != "play" or not b.get("recs"):
                continue
            deciders = {c["who"] for c in b.get("calls", []) if c.get("who", "").startswith("firm")}
            for i, rec in enumerate(b["recs"]):
                if rec is None or f"firm{i}" not in deciders:
                    continue
                if 0.005 <= rec - a["prices"][i] < 0.025:
                    n += 1
                    k += abs(b["prices"][i] - rec) < 0.005
    return k, n


def outcomes(tag: str, arm: str):
    out = []
    for rows in runs(tag, arm):
        m = rows[0]["market"]
        s = next(r for r in rows if r.get("type") == "summary")
        out.append(((s["price_lastk"] - m["p_nash"]) / (m["p_mono"] - m["p_nash"]), s["delta_lastk"]))
    return out


def share(hub, rem, base, idx):
    h, r, b = (st.mean(x[idx] for x in arr) for arr in (hub, rem, base))
    return (h - r) / (h - b)


def boot_ci(hub, rem, base, idx, draws=4000):
    rng = random.Random(0)
    vals = []
    for _ in range(draws):
        sample = [[rng.choice(arr) for _ in arr] for arr in (hub, rem, base)]
        try:
            vals.append(share(*sample, idx))
        except ZeroDivisionError:
            pass
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]


def main():
    print("## 1. Acceptance of 1-2 cent increases, +1 cent ratchet with firm discretion (K1-d)\n")
    for label, tag in [("Claude Haiku 5.5", "ratchet"), ("Nemotron 3.5 Lightning", "ladder-or-nemotron"),
                       ("Qwen3.8 Flash", "ladder-or-qwen"), ("GPT-5.4 mini", "replicate-openai"),
                       ("Gemini 3.5 Flash-Lite", "ladder-gem-lite"),
                       ("Gemini 3.5 Flash-Lite, thinking on", "ladder-gem-lite-hi")]:
        k, n = acceptance(tag)
        print(f"- {label}: {k}/{n} = {k / n:.0%}")
    k3, n3 = acceptance("ladder-gem-lite", "K3-d")
    k10, n10 = acceptance("ladder-gem-lite", "K10-d")
    print(f"- (Gemini Flash-Lite 1-2 cent steps inside the +3 / +10 cent runs: {k3}/{n3}, {k10}/{n10})")

    print("\n## 2. Share of harm removed, profit gain vs price index (bootstrap 95% CI)\n")
    for label, tag in [("Claude Haiku 5.5", "main"), ("Nemotron 3.5 Lightning", "ladder-or-nemotron"),
                       ("Qwen3.8 Flash", "ladder-or-qwen"), ("DeepSeek V4.1 Flash", "replicate-dsflash"),
                       ("Gemini 3.5 Flash-Lite", "ladder-gem-lite"), ("GPT-5.4 mini", "replicate-openai")]:
        base, hub = outcomes(tag, "B0"), outcomes(tag, "M2-a")
        print(f"- {label}: price index B0 {st.mean(x[0] for x in base):.2f}, hub {st.mean(x[0] for x in hub):.2f}")
        for rem_label, arm in [("data ban", "M0-a"), ("stale data", "M1-a")]:
            rem = outcomes(tag, arm)
            cells = []
            for idx, name in [(1, "profit gain"), (0, "price index")]:
                lo, hi = boot_ci(hub, rem, base, idx)
                cells.append(f"{name} {share(hub, rem, base, idx):.0%} ({lo:.0%} to {hi:.0%})")
            print(f"  - {rem_label} (price index {st.mean(x[0] for x in rem):.2f}): " + "; ".join(cells))

    print("\n## 3. Rounds for a clip band to reach 0.95 * p_M from warm-up prices (cent rounding)\n")
    p_mono = 1.9249809190177618
    for band in (0.03, 0.01):
        counts = []
        for p0 in (1.43, 1.47, 1.48, 1.50, 1.53):
            p, rounds = p0, 0
            while p < 0.95 * p_mono:
                p, rounds = round(p * (1 + band), 2), rounds + 1
            counts.append(rounds)
        print(f"- +/-{band:.0%}: {min(counts)}-{max(counts)} rounds (start prices 1.43-1.53)")

    print("\n## 4. Gemini 3.5 Flash-Lite hub runs that touch the $2.89 willingness-to-pay line\n")
    for arm in ("M2-a", "M0-a", "M1-a"):
        touched, total, pinned = 0, 0, []
        for rows in runs("ladder-gem-lite", arm):
            total += 1
            play = [r for r in rows if r.get("type") == "round" and r.get("kind") == "play"]
            if any(abs(p - 2.89) < 0.005 for r in play for p in r["prices"]):
                touched += 1
            last = play[-20:]
            for i in range(len(last[0]["prices"])):
                if all(abs(r["prices"][i] - 2.89) < 0.005 for r in last):
                    pinned.append(f"seed {rows[0]['seed']} firm {i}")
        note = f"; at $2.89 in all of the last 20 rounds: {', '.join(pinned)}" if pinned else ""
        print(f"- {arm}: {touched} of {total} runs have a firm price of $2.89 in some round{note}")


if __name__ == "__main__":
    main()
