"""Ratchet analysis ($0, existing data): how often a firm accepts a recommendation, by the step it implies.

A decision is a round in which firm i priced after seeing a recommendation (a `firm{i}` call is logged). Its step is
the recommendation minus the firm's own price in the previous round; it is accepted if the firm's price equals the
recommendation (to the cent). Also reports the LLM hub's step distribution under auto-accept vs discretion.

    uv run python tools/ratchet_curve.py                  # all batches
    uv run python tools/ratchet_curve.py main ladder-gem-lite
"""

from __future__ import annotations

import glob
import json
import math
import os
import sys
from collections import defaultdict

BINS = [(-9, -0.095, "cut > 9c"), (-0.095, -0.005, "cut 1-9c"), (-0.005, 0.005, "hold"), (0.005, 0.025, "up 1-2c"),
        (0.025, 0.055, "up 3-5c"), (0.055, 0.095, "up 6-9c"), (0.095, 9, "up >= 10c")]


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def runs(tags):
    for tag in tags:
        for f in sorted(glob.glob(f"results/{tag}/*/s*.jsonl")):
            if ".thoughts." in f:
                continue
            rows = [json.loads(line) for line in open(f, encoding="utf-8")]
            cfg = rows[0]
            if not any(r.get("type") == "summary" for r in rows):
                continue  # unfinished
            model = (cfg.get("firm_model") or cfg.get("advisor_model") or "scripted").split(":")[-1]
            yield tag, cfg["arm"], cfg["arm_spec"], model, [r for r in rows if r.get("type") == "round"]


def main(tags):
    acc = defaultdict(lambda: [0, 0])  # (model, group, bin) -> [accepted, n]
    hub_steps = defaultdict(list)  # (model, arm) -> steps of LLM hub recommendations
    for tag, arm, spec, model, rounds in runs(tags):
        group = {"llm": "LLM hub" if spec["objective"] == "joint" else "LLM client advisor",
                 "static": "static", "ratchet": "scripted ratchet", "br": "scripted BR"}.get(spec["advisor"])
        if group is None:
            continue
        for a, b in zip(rounds, rounds[1:]):
            if b.get("kind") != "play" or not b.get("recs"):
                continue
            deciders = {c["who"] for c in b.get("calls", []) if c.get("who", "").startswith("firm")}
            for i, rec in enumerate(b["recs"]):
                if rec is None:
                    continue
                step = rec - a["prices"][i]
                if spec["advisor"] == "llm" and spec["objective"] == "joint" and len(b["recs"]) == 2:
                    hub_steps[(model, arm)].append(step)
                if f"firm{i}" not in deciders:
                    continue
                k = next(lab for lo, hi, lab in BINS if lo <= step < hi)
                cell = acc[(model, group, k)]
                cell[0] += abs(b["prices"][i] - rec) < 0.005
                cell[1] += 1

    print("## Acceptance by recommended step (firm decisions after seeing a recommendation)\n")
    print("| Firm model | Recommender | " + " | ".join(lab for _, _, lab in BINS) + " |")
    print("|---|---|" + "---|" * len(BINS))
    for model, group in sorted({(m, g) for m, g, _ in acc}):
        cells = []
        for _, _, lab in BINS:
            k, n = acc[(model, group, lab)]
            cells.append(f"{k / n:.2f} ({n})" if n else "—")
        print(f"| {model} | {group} | " + " | ".join(cells) + " |")

    print("\n## LLM hub's recommended step vs the client's last price (duopoly, joint objective)\n")
    print("| Model | Arm | n | median | share up 1-5c | share >= 10c up | share hold |")
    print("|---|---|---|---|---|---|---|")
    for (model, arm), xs in sorted(hub_steps.items()):
        xs = sorted(xs)
        n = len(xs)
        small = sum(0.005 <= x < 0.055 for x in xs) / n
        big = sum(x >= 0.095 for x in xs) / n
        hold = sum(abs(x) < 0.005 for x in xs) / n
        print(f"| {model} | {arm} | {n} | {xs[n // 2]:+.3f} | {small:.2f} | {big:.2f} | {hold:.2f} |")


if __name__ == "__main__":
    tags = sys.argv[1:] or sorted(d for d in os.listdir("results") if os.path.isdir(f"results/{d}") and d != "dry")
    main(tags)
