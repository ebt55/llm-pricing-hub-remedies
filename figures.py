"""Paper figures (static, light mode) -> report/figures/*.png and *.pdf

    uv run python figures.py

Palette: validated categorical slots (dataviz reference palette, light mode): model families use slots 1-3
(blue Haiku, orange DeepSeek, aqua OpenAI; all-pairs CVD-safe); price-path series use slots 1-5 in fixed order.
Slots 3-5 sit below 3:1 contrast on the surface, so every series is also direct-labelled.
"""

from __future__ import annotations

import glob
import gzip  # noqa: F401  (kept for parity with detect.py readers)
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "report", "figures")
SLOT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
MODELS = [("main", "Claude Haiku 5.5", SLOT[0]), ("replicate-dsflash", "DeepSeek V4.1 Flash", SLOT[1]),
          ("replicate-openai", "GPT-5.4 mini", SLOT[2])]
ARM_COLOR = {"B0": SLOT[0], "M2-a": SLOT[1], "M1-a": SLOT[2], "M0-a": SLOT[3], "M2-d": SLOT[4]}  # entity, not rank
LADDER = [("B0", "No advisor"), ("R2-a", "Client-only\nadvisor,\ncurrent data"), ("M2-a", "Hub,\ncurrent data"),
          ("M1-a", "Hub,\nstale data"), ("M0-a", "Hub,\nno rival data"), ("M2-d", "Hub,\nadvice optional")]

plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb"})


def finished(tag):
    """{arm: [(summary, play_rounds), ...]} for finished runs of a results tag."""
    out = {}
    for path in sorted(glob.glob(os.path.join(HERE, "results", tag, "*", "s*.jsonl"))):
        if ".thoughts." in path:
            continue
        with open(path, encoding="utf-8") as f:
            lines = [json.loads(x) for x in f if x.strip()]
        if lines and lines[-1].get("type") == "summary":
            play = [r for r in lines if r.get("type") == "round" and r["kind"] == "play"]
            out.setdefault(lines[-1]["arm"], []).append((lines[-1], play))
    return out


def ci(x):
    x = np.asarray(x, float)
    if len(x) < 2:
        return x.mean(), 0.0
    return x.mean(), stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_ladder():
    data = {tag: finished(tag) for tag, _, _ in MODELS}
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    offsets = {"main": 0.0, "replicate-dsflash": 0.22, "replicate-openai": 0.34}
    rng = np.random.default_rng(0)
    for i, (arm, _) in enumerate(LADDER):
        runs = [s["delta_lastk"] for s, _ in data["main"].get(arm, [])]
        if runs:  # individual Haiku runs, recessive
            ax.scatter(i - 0.12 + rng.uniform(-0.05, 0.05, len(runs)), runs, s=9, color=MUTED, alpha=0.55,
                       linewidths=0, zorder=2)
    for tag, label, color in MODELS:
        xs, ms, hs = [], [], []
        for i, (arm, _) in enumerate(LADDER):
            vals = [s["delta_lastk"] for s, _ in data[tag].get(arm, [])]
            if len(vals) >= 2:
                m, h = ci(vals)
                xs.append(i + offsets[tag]), ms.append(m), hs.append(h)
        if xs:
            ns = sorted({len(data[tag][a]) for a, _ in LADDER if a in data[tag]})
            n = f"{ns[0]}" if len(ns) == 1 else f"{ns[0]}–{ns[-1]}"
            ax.errorbar(xs, ms, yerr=hs, fmt="o", ms=6, color=color, ecolor=color, elinewidth=1.5, capsize=3,
                        mec="#fcfcfb", mew=1.2, zorder=3, label=f"{label} (n = {n} runs per arm)")
    ax.axhline(0, color=MUTED, lw=0.8, ls=":", zorder=1)
    ax.axhline(1, color=MUTED, lw=0.8, ls=":", zorder=1)
    ax.text(len(LADDER) - 0.45, 1.0, "cartel\n(joint monopoly)", color=INK2, fontsize=7.5, va="center")
    ax.text(len(LADDER) - 0.45, 0.0, "competitive\n(Nash)", color=INK2, fontsize=7.5, va="center")
    ax.set_xticks(range(len(LADDER)), [l for _, l in LADDER], fontsize=8)
    ax.set_xlim(-0.5, len(LADDER) + 0.3)
    ax.set_ylim(-0.15, 1.3)
    ax.set_ylabel("Profit gain Δ (last 20 of 100 rounds)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left", bbox_to_anchor=(0.0, 1.16), ncol=3)
    save(fig, "fig1_remedy_ladder")


def fig_paths(tag="main", arms=(("B0", "No advisor"), ("M2-a", "Hub, current data"), ("M1-a", "Hub, stale data"),
                                ("M0-a", "Hub, no rival data"), ("M2-d", "Hub, advice optional")),
              name="fig2_price_paths", title=None):
    data = finished(tag)
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ends = []
    for k, (arm, label) in enumerate(arms):
        series = [np.array([r["prices"] for r in play]).mean(axis=1) for _, play in data.get(arm, [])]
        if not series:
            continue
        L = min(len(s) for s in series)
        m = np.mean([s[:L] for s in series], axis=0)
        color = ARM_COLOR.get(arm, SLOT[k % len(SLOT)])
        ax.plot(np.arange(1, L + 1), m, color=color, lw=2, label=f"{label} (n={len(series)})", zorder=3)
        ends.append([m[-1], label, color, L])
    ends.sort(key=lambda e: e[0])  # direct labels at the line ends, nudged apart
    for j in range(1, len(ends)):
        ends[j][0] = max(ends[j][0], ends[j - 1][0] + 0.035)
    for y, label, color, L in ends:
        ax.text(L + 2, y, label, color=INK2, fontsize=7.5, va="center")
        ax.plot([L, L + 1.5], [y, y], color=color, lw=2)
    for y, lab, dy in ((1.4729, "Nash 1.47", -0.022), (1.9250, "monopoly 1.93", 0.012)):
        ax.axhline(y, color=MUTED, lw=0.8, ls=":", zorder=1)
        ax.text(1, y + dy, lab, color=INK2, fontsize=7)
    lo, hi = ax.get_ylim()
    ax.set_ylim(min(lo, 1.44), max(hi, 1.95))
    ax.set_xlabel("round of play (after 10 rounds of competitive history)")
    ax.set_ylabel("mean market price")
    ax.set_xlim(0, (ends[0][3] if ends else 100) * 1.28)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left", bbox_to_anchor=(0.0, 1.2), ncol=3)
    if title:
        ax.set_title(title, fontsize=9, color=INK, loc="left")
    save(fig, name)


if __name__ == "__main__":
    fig_ladder()
    fig_paths()
    fig_paths("robust-long", (("B0", "No advisor"), ("M1-a", "Hub, stale data"), ("M0-a", "Hub, no rival data")),
              "figA_long_horizon")
    print("wrote", sorted(os.listdir(OUT)))


def fig_dose():
    """Adherence dose-response: Delta vs probability that a firm's price is the hub's recommendation."""
    main, fu = finished("main"), finished("followup")
    pts = [(0.0, main.get("M2-d", [])), (0.5, fu.get("M2-q50", [])), (0.8, fu.get("M2-q80", [])),
           (0.9, fu.get("M2-q90", [])), (1.0, main.get("M2-a", []))]
    b0 = [s["delta_lastk"] for s, _ in main.get("B0", [])]
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    rng = np.random.default_rng(1)
    xs, ms, hs = [], [], []
    for q, runs in pts:
        vals = [s["delta_lastk"] for s, _ in runs]
        if len(vals) < 2:
            continue
        ax.scatter(q + rng.uniform(-0.012, 0.012, len(vals)), vals, s=9, color=MUTED, alpha=0.55, linewidths=0, zorder=2)
        m, h = ci(vals)
        xs.append(q), ms.append(m), hs.append(h)
    ax.errorbar(xs, ms, yerr=hs, fmt="-o", ms=6, color=SLOT[0], ecolor=SLOT[0], lw=2, capsize=3, mec="#fcfcfb",
                mew=1.2, zorder=3)
    if b0:
        ax.axhline(np.mean(b0), color=MUTED, lw=0.8, ls=":")
        ax.text(1.02, np.mean(b0), "no advisor", color=INK2, fontsize=7.5, va="center")
    ax.axhline(1, color=MUTED, lw=0.8, ls=":")
    ax.text(1.02, 1.0, "cartel", color=INK2, fontsize=7.5, va="center")
    # Sourced acceptance figures (SPRINT_LOG 02:10): DOJ complaint para 71, final price within 1% of the
    # recommendation in 40-50% of new leases; former employees (ProPublica 2022) and MDL plaintiffs: 80-90%.
    ax.axvspan(0.4, 0.5, color=GRID, alpha=0.7, zorder=0, lw=0)
    ax.text(0.45, 0.28, "DOJ:\n40–50%\nwithin 1%", color=INK2, fontsize=6.5, ha="center")
    ax.axvspan(0.8, 0.9, color=GRID, alpha=0.7, zorder=0, lw=0)
    ax.text(0.85, 0.28, "ex-employees,\nplaintiffs:\n80–90%", color=INK2, fontsize=6.5, ha="center")
    ax.set_xticks([0, 0.5, 0.8, 0.9, 1.0], ["0\n(advice optional)", "0.5", "0.8", "0.9", "1\n(auto-accept)"], fontsize=8)
    ax.set_xlim(-0.08, 1.18)
    ax.set_ylim(-0.15, 1.12)
    ax.set_xlabel("probability that a firm's price is the hub's recommendation")
    ax.set_ylabel("Profit gain \u0394 (last 20 rounds)")
    ax.set_title("Market-aligned hub with current data, Claude Haiku 5.5 (n = 10\u201320 per point)", fontsize=8.5,
                 color=INK, loc="left")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    save(fig, "fig3_adherence_dose")


if __name__ == "__main__":
    fig_dose()


CROSS_MODELS = [("main", "Claude\nHaiku 5.5"), ("replicate-openai", "GPT-5.4\nmini"), ("ladder-or-qwen", "Qwen3.8\nFlash"),
                ("ladder-or-nemotron", "Nemotron 3.5\nLightning"), ("ladder-gem-lite", "Gemini 3.5\nFlash-Lite"),
                ("replicate-dsflash", "DeepSeek\nV4.1 Flash"), ("ladder-gem-flash", "Gemini 3.8\nFlash")]


def fig_cross_model():
    """Price index (0 = Nash, 1 = joint monopoly, > 1 = above monopoly) for the hub under each data rule, per model.
    The price index is used instead of Delta because Delta falls on both sides of the monopoly price and would
    hide overshooting hubs. Error bars (t 95% CI) only where n >= 8; dots are individual runs."""
    arms = [("B0", "no advisor"), ("M2-a", "hub, current data"), ("M1-a", "hub, stale data"), ("M0-a", "hub, no rival data")]
    p_n, p_m = 1.4729, 1.9250

    def idx(play):
        return (np.mean([np.mean(r["prices"]) for r in play[-20:]]) - p_n) / (p_m - p_n)

    data = [(label, finished(tag)) for tag, label in CROSS_MODELS]
    data = [(label, d) for label, d in data if sum(len(d.get(a, [])) >= 2 for a, _ in arms) == len(arms)]
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    off = {"B0": -0.27, "M2-a": -0.09, "M1-a": 0.09, "M0-a": 0.27}
    rng = np.random.default_rng(2)
    for arm, label in arms:
        xs, ms = [], []
        for i, (_, d) in enumerate(data):
            vals = [idx(play) for _, play in d.get(arm, [])]
            x = i + off[arm]
            ax.scatter(x + rng.uniform(-0.025, 0.025, len(vals)), vals, s=7, color=ARM_COLOR[arm], alpha=0.4,
                       linewidths=0, zorder=2)
            m, h = ci(vals)
            if len(vals) >= 8:
                ax.errorbar([x], [m], yerr=[h], fmt="none", ecolor=ARM_COLOR[arm], elinewidth=1.2, capsize=2, zorder=3)
            xs.append(x), ms.append(m)
        ax.scatter(xs, ms, s=34, color=ARM_COLOR[arm], edgecolors="#fcfcfb", linewidths=1.0, zorder=4, label=label)
    j0 = (1.7464 - p_n) / (p_m - p_n)  # scripted rational hub, no rival data: both firms at the joint BR to Nash
    ax.axhline(j0, color=INK2, lw=1, ls="--", zorder=1)
    ax.text(len(data) - 0.45, j0 + 0.06, "rational hub,\nno rival data", color=INK2, fontsize=7, va="bottom")
    for y, lab in ((0, "competitive (Nash)"), (1, "joint monopoly")):
        ax.axhline(y, color=MUTED, lw=0.8, ls=":")
        ax.text(len(data) - 0.45, y, lab, color=INK2, fontsize=7, va="center")
    ax.set_xticks(range(len(data)), [l for l, _ in data], fontsize=7.5)
    ax.set_xlim(-0.6, len(data) + 0.5)
    ax.set_ylim(-0.3, 1.65)
    ax.set_ylabel("price index (last 20 of 100 rounds)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left", bbox_to_anchor=(0.0, 1.16), ncol=4)
    save(fig, "fig4_cross_model")


if __name__ == "__main__":
    fig_cross_model()
