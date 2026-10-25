"""Monday-morning helper: print the GPT-5.4 mini ratchet result (K1-d) and check it against P14 (SPRINT_LOG).

    uv run python tools/gpt_ratchet_patch.py

Prints the table row for report/draft.md §4.4 and the slide-chip text. Figure 3 picks the series up by itself
(`uv run python -c "import figures; figures.fig_ratchet()"`).
"""

from __future__ import annotations

import glob
import json
import statistics as st

TAG = "results/replicate-openai/K1-d"


def main():
    deltas, acc, n_dec = [], 0, 0
    for f in sorted(glob.glob(f"{TAG}/s*.jsonl")):
        if ".thoughts." in f:
            continue
        rows = [json.loads(line) for line in open(f, encoding="utf-8")]
        if rows[-1].get("type") != "summary":
            print(f"unfinished: {f}")
            continue
        deltas.append(rows[-1]["delta_lastk"])
        rounds = [r for r in rows if r.get("type") == "round"]
        for a, b in zip(rounds, rounds[1:]):
            if b.get("kind") != "play" or not b.get("recs"):
                continue
            for i, rec in enumerate(b["recs"]):
                if rec is None or not 0.005 <= rec - a["prices"][i] < 0.025:
                    continue
                n_dec += 1
                acc += abs(b["prices"][i] - rec) < 0.005
    if not deltas:
        print("no finished GPT-5.4 mini K1-d runs yet")
        return
    share = acc / n_dec if n_dec else float("nan")
    mean = st.mean(deltas)
    band = "< 0.2" if share < 0.20 else ("> 0.5" if share > 0.40 else "0.2–0.5")
    ok = (mean < 0.2) if share < 0.20 else ((mean > 0.5) if share > 0.40 else (0.2 <= mean <= 0.5))
    print(f"runs: {len(deltas)}  per run: {', '.join(f'{d:.2f}' for d in deltas)}")
    print(f"accepts 1–2 cent nudges: {share:.0%} (n = {n_dec})   mean Δ: {mean:.2f}")
    print(f"P14: acceptance implies Δ {band}; observed {mean:.2f} -> {'HOLDS' if ok else 'FAILS'}")
    print("\ndraft.md §4.4 row (insert after the Qwen row):")
    print(f"| GPT-5.4 mini | {share:.0%} | **{mean:.2f}** (n = {len(deltas)}) | — | — | — |")
    print(f"\nslide chip: GPT-5.4 mini {share:.0%} → {mean:.2f}")


if __name__ == "__main__":
    main()
