"""Animated replay of two logged runs under the same scripted 1-cent ratchet, for the README ($0, no model calls).

    uv run python tools/replay_gif.py      # writes report/figures/ratchet_replay.gif

Left: Claude Haiku 5.5 firms (seed 100, a typical run). Right: Gemini 3.5 Flash-Lite firms (seed 1000; all six
Gemini runs end at monopoly). Each frame is one round: both firms' prices, the hub's recommendations and the running
profit gain over the last 20 rounds, which ends at the run's logged value.
"""

from __future__ import annotations

import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from figures import GRID, INK, INK2, MUTED, SLOT  # noqa: E402

RUNS = [("results/ratchet/K1-d/s100.jsonl", "Claude Haiku 5.5 firms", SLOT[0]),
        ("results/ladder-gem-lite/K1-d/s1000.jsonl", "Gemini 3.5 Flash-Lite firms", SLOT[1])]
P_N, P_M = 1.4729, 1.9250
HOLD = 30  # frames to hold the last round


def load(path: str) -> dict:
    rows = [json.loads(line) for line in open(os.path.join(HERE, path), encoding="utf-8")]
    rounds = [r for r in rows if r.get("type") == "round"]
    return {"prices": np.array([r["prices"] for r in rounds], float),
            "recs": [r["recs"] for r in rounds],
            "gains": np.array([r["gains"] for r in rounds], float),
            "warm": np.array([r.get("kind") == "warmup" for r in rounds]),
            "delta": rows[-1]["delta_lastk"]}


def main(out=os.path.join(HERE, "report", "figures", "ratchet_replay.gif")):
    runs = [(load(p), label, color) for p, label, color in RUNS]
    n = len(runs[0][0]["prices"])
    n_warm = int(runs[0][0]["warm"].sum())
    x = np.arange(1, n + 1) - n_warm  # warm-up rounds are <= 0

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.4), dpi=100, sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.78, bottom=0.2, wspace=0.08)
    fig.text(0.5, 0.95, "Same scripted ratchet, two firm models", ha="center", fontsize=13, color=INK, weight="bold")
    fig.text(0.5, 0.885, "Each round the hub recommends each firm its own last price + 1¢; the firm's AI decides its price.",
             ha="center", fontsize=9, color=INK2)
    fig.text(0.5, 0.025, "Replay of logged runs (seeds 100 and 1000), github.com/ebt55/llm-pricing-hub-remedies",
             ha="center", fontsize=7.5, color=MUTED)
    artists = []
    for ax, (run, label, color) in zip(axes, runs):
        ax.axvspan(x[0] - 0.5, 0.5, color=GRID, alpha=0.6, lw=0)
        ax.text(x[0] + 0.5, 1.985, "warm-up", fontsize=7, color=INK2, va="top")
        for y, lab, dy, va in ((P_N, "competitive (Nash)", -0.01, "top"), (P_M, "joint monopoly", 0.008, "bottom")):
            ax.axhline(y, color=MUTED, lw=0.8, ls=":")
            ax.text(x[-1], y + dy, lab, fontsize=7, color=INK2, ha="right", va=va)
        ax.set_xlim(x[0] - 0.5, x[-1] + 1)
        ax.set_ylim(1.40, 2.0)
        ax.set_title(label, fontsize=10, color=INK, loc="left")
        ax.set_xlabel("round", fontsize=8, color=INK2)
        ax.tick_params(labelsize=7.5, colors=INK2)
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        rec, = ax.plot([], [], ls="none", marker="o", ms=2.6, mfc="none", mec=INK2, mew=0.6, alpha=0.7)
        a, = ax.plot([], [], color=color, lw=2)
        b, = ax.plot([], [], color=color, lw=1.4, alpha=0.5)
        dot, = ax.plot([], [], ls="none", marker="o", ms=5, color=color, mec="white", mew=1)
        txt = ax.text(0.98, 0.62, "", transform=ax.transAxes, ha="right", fontsize=9, color=INK,
                      bbox={"boxstyle": "round,pad=0.35", "fc": "white", "ec": GRID})
        artists.append((run, rec, a, b, dot, txt))
    axes[0].set_ylabel("price", fontsize=8, color=INK2)
    handles = [plt.Line2D([], [], color=INK2, lw=2), plt.Line2D([], [], color=INK2, lw=1.4, alpha=0.5),
               plt.Line2D([], [], ls="none", marker="o", ms=4, mfc="none", mec=INK2)]
    fig.legend(handles, ["firm A price", "firm B price", "hub's recommendation"], loc="lower center",
               bbox_to_anchor=(0.5, 0.06), ncol=3, frameon=False, fontsize=8)

    def frame(i):
        t = min(i, n - 1)
        out = []
        for run, rec, a, b, dot, txt in artists:
            p = run["prices"]
            a.set_data(x[:t + 1], p[:t + 1, 0])
            b.set_data(x[:t + 1], p[:t + 1, 1])
            rx, ry = [], []
            for k in range(t + 1):
                if run["recs"][k]:
                    rx += [x[k]] * len(run["recs"][k])
                    ry += list(run["recs"][k])
            rec.set_data(rx, ry)
            dot.set_data([x[t], x[t]], p[t])
            if x[t] <= 0:
                txt.set_text("warm-up: competitive history")
            else:
                play = np.where(~run["warm"][:t + 1])[0][-20:]
                g = run["gains"][play].mean()
                txt.set_text(f"round {x[t]} of {x[-1]}\nprofit gain (last 20): {g:.2f}")
            out += [rec, a, b, dot, txt]
        return out

    frames = list(range(0, n_warm, 2)) + list(range(n_warm, n)) + [n - 1] * HOLD
    anim = FuncAnimation(fig, frame, frames=frames, blit=False)
    anim.save(out, writer=PillowWriter(fps=12))
    for run, label, _ in runs:
        print(f"{label}: logged profit gain {run['delta']:.3f}")
    print(f"wrote {out} ({os.path.getsize(out) / 1e6:.2f} MB, {len(frames)} frames)")


if __name__ == "__main__":
    main()
