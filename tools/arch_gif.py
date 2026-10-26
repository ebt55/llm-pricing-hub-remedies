"""Animated architecture of the game for the README: one LLM hub advising two LLM firms, with the RealPage
remedies as switches and each setting's measured outcome ($0; numbers from results/main and results/guardrail).

    uv run python tools/arch_gif.py      # writes report/figures/arch_playground.gif

Each scenario plays one round (hub reads data, recommends, the price is set, customers buy), then holds on its
outcome: the mean profit gain for Claude Haiku 5.5 over the last 20 of 100 rounds (n = 20 per setting). It opens with
the no-hub baseline (B0), where each firm's LLM prices alone. Every LLM agent wears an "LLM" badge, black when that
model is called each round and grey when idle: as in advisor/game.py, under auto-accept and the clip band the hub's
(clipped) price is applied without calling the firm's model; under discretion the firm's model sees it and decides.
Icons are drawn with matplotlib patches on a light background in the figures.py palette.
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.backends.backend_agg import RendererAgg  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle, Wedge  # noqa: E402
from PIL import Image  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 840, 470  # the axes are in pixels: 1 data unit = 1 px
BG, CARD, WHITE = "#fcfcfb", "#f4f3ef", "#ffffff"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"  # as in figures.py
BLUE, ORANGE = "#2a78d6", "#eb6834"  # SLOT[0]: firms and active switches; SLOT[1]: the flow and highlights
BLUE_LT, LINE = "#d4e4f7", "#c3c2bd"  # light tint of BLUE; idle arrows
DONE = "#aac8ee"  # a mid tint of BLUE: scenes already shown in the progress bar
LW = 1.3  # one stroke width (pt) for every icon outline
NO_ADVISOR = 0.06
# (name, hub goal, rival data, adherence, Haiku profit gain, note); see report/draft.md §4 (Haiku, n = 20 per arm).
# The first is the B0 baseline: no hub (goal and data None), each firm's LLM prices alone.
SCENARIOS = [
    ("No pricing hub (baseline)", None, None, "alone", NO_ADVISOR, "LLM firms pricing alone stay competitive"),
    ("No remedy", "both", "current", "auto", 0.99, "joint monopoly"),
    ("Stale rival data", "both", "stale", "auto", 0.79, "21% of the harm removed"),
    ("Data ban", "both", "none", "auto", 0.35, "69% of the harm removed"),
    ("±3% per-round band", "both", "current", "band", 1.00, "none removed; monopoly only delayed"),
    ("Firm discretion", "both", "current", "disc", 0.11, "95% removed: Haiku firms refuse nudges"),
    ("Hub serves each client only", "own", "current", "auto", -0.01, "pro-competitive"),
]
BASE = ("both", "current", "auto")  # the no-remedy setting; a switch that differs from it is the remedy
GOAL = {"both": ("goal: combined profit", "of both firms"), "own": ("goal: each client's", "own profit")}
DATA = {"current": "current", "stale": "10 rounds old", "none": "banned"}
ADH = {"auto": ("hub's price applied;", "its LLM is idle"), "band": ("hub's price, capped", "at ±3% a round"),
       "disc": ("own LLM decides,", "seeing hub's price"), "alone": ("own LLM decides", "alone")}
DECIDES = {"auto": False, "band": False, "disc": True, "alone": True}  # is the firm's LLM called each round?
BUBBLE = {"disc": "my call", "alone": "my price"}  # what a deciding firm's LLM says
STAMP = {"auto": "auto", "band": "±3% cap"}  # how the hub's price is applied when the firm's LLM is idle
STEP3 = {"auto": "Hub's price applied", "band": "Hub's price applied (capped ±3%)", "disc": "Each firm's LLM decides",
         "alone": "Each firm's LLM decides"}
STEPS = ["Hub reads data", "Recommends a price", None, "Customers buy"]  # step 3 depends on the adherence
# Pacing (ms; GIF delays are whole centiseconds). The first TEACH scenes (baseline, no remedy) play each step slowly
# (~0.8 s) to teach the flow; later scenes play steps at ~0.45 s but hold the outcome ~3 s so the note can be read.
# Each scene opens on a still frame (SCENE_PAUSE_MS) so the viewer sees which switch flipped.
TEACH = 2
STEP_FRAMES = 6  # token frames per step; the last one lingers
STEP_MS, STEP_PAUSE_MS, HOLD_MS = {True: 80, False: 50}, {True: 320, False: 150}, {True: 2800, False: 3000}
GROW_FRAMES, GROW_MS, SCENE_PAUSE_MS = 5, 40, 300  # the outcome bar grows, then holds
HOLD_SPLIT = 4  # the hold is cut into this many frames so the scene-progress bar keeps moving (tiny delta frames)

# the game, laid out as a hub-and-spoke diamond in the left column (x 24-512)
HUB, FIRM_A, FIRM_B, CROWD = (268, 308), (96, 204), (440, 204), (268, 90)
HUB_W, HUB_H = 92, 62
PATHS = {"data": ((268, 120), (268, 271)), "recA": ((238, 271), (128, 236)), "recB": ((298, 271), (408, 236)),
         "priceA": ((136, 184), (230, 104)), "priceB": ((400, 184), (306, 104))}
TOKEN_END = {"data": 0.92, "recA": 0.8, "recB": 0.8, "priceA": 0.84, "priceB": 0.84}  # tokens stop short of the icon
# the remedies panel in the right column
PX0, PX1 = 552, 800  # content edges


def halo(ax, xy, w, h):
    x, y = xy
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=12", fc=ORANGE,
                                ec="none", alpha=0.13, zorder=1))


def badge(ax, xy, on=True):
    """The mark of an LLM agent: black when its model is called each round, grey outline when idle."""
    x, y = xy
    ax.add_patch(FancyBboxPatch((x - 15, y - 8), 30, 16, boxstyle="round,pad=0,rounding_size=8",
                                fc=INK if on else WHITE, ec=BG if on else MUTED, lw=1.6 if on else 1.0, zorder=8))
    ax.text(x, y - 0.5, "LLM", ha="center", va="center", fontsize=7, weight="bold", color=WHITE if on else MUTED,
            zorder=9)


def hub_icon(ax, active, off=False):
    """Pricing software: an app window with a price chart, run by an LLM; faded with a dashed outline when off."""
    x, y = HUB
    if active:
        halo(ax, HUB, HUB_W + 22, HUB_H + 22)
    ink = LINE if off else INK
    x0, y0, x1, y1 = x - HUB_W / 2, y - HUB_H / 2, x + HUB_W / 2, y + HUB_H / 2
    ax.add_patch(FancyBboxPatch((x0, y0), HUB_W, HUB_H, boxstyle="round,pad=0,rounding_size=7", fc=WHITE, ec=ink,
                                lw=LW, ls=(0, (4, 3)) if off else "-", zorder=3))
    ax.plot([x0, x1], [y1 - 13, y1 - 13], color=ink, lw=LW * 0.8, zorder=4)
    for i in range(3):
        ax.add_patch(Circle((x0 + 9 + 7 * i, y1 - 6.5), 2.1, fc=GRID if off else MUTED, ec="none", zorder=4))
    ax.plot([x0 + 10, x1 - 10], [y0 + 9, y0 + 9], color=GRID, lw=1, zorder=4)
    xs = np.linspace(x0 + 12, x1 - 14, 6)
    ys = y0 + 12 + np.array([3, 10, 7, 17, 21, 28])
    ax.plot(xs, ys, color=GRID if off else INK2, lw=1.5, zorder=5, solid_capstyle="round", solid_joinstyle="round")
    if not off:
        ax.add_patch(Circle((xs[-1], ys[-1]), 3.4, fc=ORANGE, ec=WHITE, lw=1, zorder=6))
    badge(ax, (x1 - 8, y1), on=not off)


def stamp(ax, xy, text):
    """The hub's price applied mechanically: a rubber stamp on the storefront, no thinking involved."""
    ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=7.5, weight="bold", color=ORANGE, rotation=8,
            zorder=12, bbox=dict(boxstyle="round,pad=0.3,rounding_size=0.4", fc=WHITE, ec=ORANGE, lw=1.3))


def shop(ax, xy, active, side, deciding=True):
    """A firm: a storefront priced by its LLM (badge on the outer corner, black when that LLM is called)."""
    x, y = xy
    if active:
        halo(ax, (x, y + 3), 86, 74)  # clear of the firm's name below
    ax.add_patch(Rectangle((x - 27, y - 28), 54, 34, fc=WHITE, ec=BLUE, lw=LW, zorder=3))
    ax.add_patch(Rectangle((x - 20, y - 17), 19, 13, fc=BLUE_LT, ec=BLUE, lw=LW * 0.8, zorder=4))
    ax.add_patch(Rectangle((x + 6, y - 28), 14, 22, fc=BLUE_LT, ec=BLUE, lw=LW * 0.8, zorder=4))
    for i in range(4):  # striped awning with a scalloped edge
        c, sx = (BLUE if i % 2 == 0 else BLUE_LT), x - 32 + 16 * i
        ax.add_patch(Rectangle((sx, y + 6), 16, 13, fc=c, ec="none", zorder=5))
        ax.add_patch(Wedge((sx + 8, y + 6), 8, 180, 360, fc=c, ec="none", zorder=5))
    ax.add_patch(FancyBboxPatch((x - 32, y + 19), 64, 8, boxstyle="round,pad=0,rounding_size=2", fc=BLUE, ec="none",
                                zorder=5))
    badge(ax, (x + side * 27, y + 27), on=deciding)


def crowd(ax, active):
    x, y = CROWD
    if active:
        halo(ax, (x, y), 92, 56)
    for dx, k, c in ((-21, 0.95, MUTED), (21, 0.95, MUTED), (0, 1.15, INK2)):  # the middle customer in front
        cx = x + dx
        ax.add_patch(Wedge((cx, y - 15 * k), 14 * k, 0, 180, fc=c, ec=BG, lw=1.6, zorder=4 + k))
        ax.add_patch(Circle((cx, y + 5 * k), 7.5 * k, fc=c, ec=BG, lw=1.6, zorder=4 + k))


def tag(ax, xy):
    """A price (recommended or set) travelling along an arrow."""
    x, y = xy
    ax.add_patch(Polygon([(x - 12, y - 7.5), (x + 6, y - 7.5), (x + 13, y), (x + 6, y + 7.5), (x - 12, y + 7.5)],
                         fc=ORANGE, ec=WHITE, lw=1.2, joinstyle="round", zorder=10))
    ax.add_patch(Circle((x + 6.5, y), 1.7, fc=WHITE, ec="none", zorder=11))
    ax.text(x - 3, y - 0.5, "$", ha="center", va="center", fontsize=8, weight="bold", color=WHITE, zorder=11)


def packet(ax, xy):
    """Market data (prices and sales) travelling to the hub."""
    x, y = xy
    ax.add_patch(FancyBboxPatch((x - 10, y - 10), 20, 20, boxstyle="round,pad=0,rounding_size=4", fc=ORANGE,
                                ec=WHITE, lw=1.2, zorder=10))
    for i, h in enumerate((6, 11, 8)):
        ax.add_patch(Rectangle((x - 6 + 4.6 * i, y - 6), 3, h, fc=WHITE, ec="none", zorder=11))


def arrow(ax, key, active):
    (x0, y0), (x1, y1) = PATHS[key]
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>,head_length=0.55,head_width=0.3",
                                 mutation_scale=14, shrinkA=0, shrinkB=0, lw=2.0 if active else 1.2,
                                 color=ORANGE if active else LINE, zorder=2))


def along(key, u):
    (x0, y0), (x1, y1) = PATHS[key]
    u = (0.5 - 0.5 * np.cos(np.pi * u)) * TOKEN_END[key]  # ease in and out
    return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u


def text_w(s, size, weight="normal", _r=RendererAgg(10, 10, 100)):
    """Width in px of a string as Agg draws it at 100 dpi."""
    return _r.get_text_width_height_descent(s, FontProperties(size=size, weight=weight), ismath=False)[0]


def bubble(ax, xy, text):
    """What a firm's LLM says about the recommendation; the tail points down at its badge."""
    x, y = xy
    w = max(text_w(text, 7.5, "bold"), 14) + 20
    ax.add_patch(FancyBboxPatch((x - w / 2, y - 10), w, 20, boxstyle="round,pad=0,rounding_size=10", fc=WHITE,
                                ec=INK2, lw=1.0, zorder=12))
    ax.add_patch(Polygon([(x - 5, y - 9.4), (x + 5, y - 9.4), (x, y - 17)], fc=WHITE, ec="none", zorder=13))
    ax.plot([x - 5, x, x + 5], [y - 10, y - 17, y - 10], color=INK2, lw=1.0, zorder=13)
    ax.text(x, y - 0.5, text, ha="center", va="center", fontsize=7.5, weight="bold", color=INK, zorder=14)


def ban(ax, xy, r=7):
    x, y = xy
    ax.add_patch(Circle((x, y), r, fc=WHITE, ec=ORANGE, lw=1.8, zorder=6))
    d = r * 0.7
    ax.plot([x - d, x + d], [y + d, y - d], color=ORANGE, lw=1.8, zorder=7, solid_capstyle="butt")


def stepper(ax, step, adh, skipped=(), y=404):
    """The four steps of a round, spread from the left margin to the panel's right edge. Each slot is as wide as its
    widest label in any scene, so the steps stay put; skipped steps (no hub) are drawn faint with a dashed ring."""
    slots = [26 + max(text_w(v, 8.5, "bold") for v in ([lab] if lab else STEP3.values())) for lab in STEPS]
    gap = (816 - 24 - sum(slots)) / 3
    x = 24
    for k, (label, w) in enumerate(zip(STEPS, slots)):
        on, off, label = k == step, k in skipped, label or STEP3[adh]
        ax.add_patch(Circle((x + 9, y), 9, fc=ORANGE if on else WHITE, ec=ORANGE if on else (GRID if off else LINE),
                            lw=LW, ls=(0, (2, 2)) if off else "-", zorder=3))
        ax.text(x + 9, y - 0.5, str(k + 1), ha="center", va="center", fontsize=7.5, weight="bold",
                color=WHITE if on else (LINE if off else MUTED), zorder=4)
        ax.text(x + 26, y, label, va="center", fontsize=8.5, color=INK if on else (LINE if off else MUTED),
                weight="bold" if on else "normal")
        if k < 3:  # connector to the next step, from the end of this label
            ax.plot([x + 26 + text_w(label, 8.5, "bold" if on else "normal") + 12, x + w + gap - 12], [y, y],
                    color=GRID, lw=1.2, zorder=2)
        x += w + gap


def switch(ax, y, label, options, active, changed, dim=False):
    """A segmented control; dimmed (no option on) when there is no hub for the remedy to act on."""
    ax.text(PX0, y + 21, label, fontsize=8, va="center", color=ORANGE if changed else (LINE if dim else INK2),
            weight="bold" if changed else "normal")
    ax.add_patch(FancyBboxPatch((PX0, y - 11), PX1 - PX0, 22, boxstyle="round,pad=0,rounding_size=11",
                                fc=CARD if dim else WHITE, ec=GRID, lw=1, zorder=3))
    w = (PX1 - PX0) / len(options)
    for i, (key, text) in enumerate(options):
        x, on = PX0 + i * w, key == active
        if on:
            ax.add_patch(FancyBboxPatch((x + 2.5, y - 8.5), w - 5, 17, boxstyle="round,pad=0,rounding_size=8.5",
                                        fc=BLUE, ec="none", zorder=4))
        ax.text(x + w / 2, y - 0.5, text, ha="center", va="center", fontsize=7.5, zorder=5,
                color=WHITE if on else (LINE if dim else INK2), weight="bold" if on else "normal")


def scene_progress(ax, s, prog, y=441):
    """Top right, level with the title: "Scene k of n" and one segment per scene; the current one fills in orange
    over the scene's duration, earlier ones are a blue tint, later ones grey. Right-aligned to the panel's edge."""
    n, seg, gap = len(SCENARIOS), 16, 3
    x0 = 816 - n * seg - (n - 1) * gap
    ax.text(x0 - 10, y, f"Scene {s + 1} of {n}", fontsize=7.5, color=INK2, va="center", ha="right")
    for i in range(n):
        x = x0 + i * (seg + gap)
        ax.add_patch(FancyBboxPatch((x, y - 2.5), seg, 5, boxstyle="round,pad=0,rounding_size=2.5",
                                    fc=DONE if i < s else GRID, ec="none", zorder=3))
        if i == s and prog > 0:
            ax.add_patch(FancyBboxPatch((x, y - 2.5), max(seg * min(prog, 1), 5), 5,
                                        boxstyle="round,pad=0,rounding_size=2.5", fc=ORANGE, ec="none", zorder=4))


def draw(ax, s, step, u, prog=0.0):
    name, goal, data, adh, gain, note = SCENARIOS[s]
    hub = goal is not None  # the baseline has no hub
    changed = [a != b for a, b in zip((goal, data, adh), BASE)] if hub else [False] * 3
    decides = DECIDES[adh]
    ax.clear()
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, fc=BG, ec="none", zorder=0))
    ax.text(24, 441, "The game: one LLM pricing hub advises both firms", fontsize=13.5, weight="bold", color=INK,
            va="center")
    scene_progress(ax, s, prog)
    stepper(ax, step, adh, skipped=() if hub else (0, 1))
    for i, (on, text) in enumerate(((True, "deciding"), (False, "idle"))):  # legend for the LLM badges
        x = 24 + 96 * i
        badge(ax, (x + 15, 350), on=on)
        ax.text(x + 36, 350, text, fontsize=7.5, color=INK2, va="center")

    # the game
    for k, on in (("data", step == 0), ("recA", step == 1), ("recB", step == 1)):
        if hub:
            arrow(ax, k, on)
        else:  # nothing flows to or from an absent hub
            (x0, y0), (x1, y1) = PATHS[k]
            ax.plot([x0, x1], [y0, y1], color=GRID, lw=1.2, ls=(0, (3, 3)), zorder=2)
    for k in ("priceA", "priceB"):
        arrow(ax, k, step == 3)
    hub_icon(ax, hub and (step == 0 and u > 0.8 or step == 1), off=not hub)
    hx, hy = HUB[0] + HUB_W / 2 + 16, HUB[1]  # the hub's label, right of the window
    ax.text(hx, hy + 10, "Pricing hub", fontsize=9.5, weight="bold", color=INK if hub else MUTED, va="center")
    hl = changed[0] or not hub
    for i, line in enumerate(GOAL[goal] if hub else ("switched off",)):
        ax.text(hx, hy - 8 - 12 * i, line, fontsize=7.5, va="center", color=ORANGE if hl else INK2,
                weight="bold" if hl else "normal")
    for xy, label, side in ((FIRM_A, "Firm A", -1), (FIRM_B, "Firm B", 1)):
        shop(ax, xy, step == 2 and decides, side, deciding=decides)
        ax.text(xy[0], xy[1] - 44, label, ha="center", fontsize=9, weight="bold", color=INK, va="center")
        for i, line in enumerate(ADH[adh]):
            ax.text(xy[0], xy[1] - 59 - 11.5 * i, line, ha="center", fontsize=7.5, va="center",
                    color=ORANGE if changed[2] else INK2, weight="bold" if changed[2] else "normal")
        if step == 2 and decides:
            bubble(ax, (xy[0] + side * 27, xy[1] + 56), "\u00b7" * (int(u * 5) + 1) if u < 0.5 else BUBBLE[adh])
        elif step == 2 and u >= 0.4:
            stamp(ax, (xy[0], xy[1] + 52), STAMP[adh])  # over the storefront, where a bubble would be
    crowd(ax, step == 3 and u > 0.8)
    ax.text(CROWD[0], CROWD[1] - 36, "Customers", ha="center", fontsize=9, weight="bold", color=INK, va="center")
    ax.text(CROWD[0], CROWD[1] - 50, "buy by price (logit demand)", ha="center", fontsize=7.5, color=INK2,
            va="center")
    if hub:
        dx, dy = PATHS["data"][0][0] + 17, (PATHS["data"][0][1] + PATHS["data"][1][1]) / 2  # the rival-data label
        if data == "none":  # the ban mark sits beside its label
            ban(ax, (dx + 8, dy))
            dx += 22
        ax.text(dx, dy + 6, "rival data:", fontsize=7.5, color=INK2, va="center")
        ax.text(dx, dy - 6, DATA[data], fontsize=7.5, va="center", color=ORANGE if changed[1] else INK2,
                weight="bold" if changed[1] else "normal")
    if step == 0:
        packet(ax, along("data", u))
    elif step == 1:
        tag(ax, along("recA", u)), tag(ax, along("recB", u))
    elif step == 2 and hub and decides:  # the recommendation waits at each firm while its LLM decides
        tag(ax, along("recA", 1)), tag(ax, along("recB", 1))
    elif step == 2 and hub:  # the hub's price passes straight through the shop: no model is called
        e = 0.5 - 0.5 * np.cos(np.pi * u)
        for a, b in (("recA", "priceA"), ("recB", "priceB")):
            (x0, y0), (x1, y1) = along(a, 1), PATHS[b][0]
            tag(ax, (x0 + (x1 - x0) * e, y0 + (y1 - y0) * e))
    elif step == 3:
        tag(ax, along("priceA", u)), tag(ax, along("priceB", u))

    # the remedies as switches, and the outcome
    ax.add_patch(FancyBboxPatch((536, 36), 280, 336, boxstyle="round,pad=0,rounding_size=12", fc=CARD, ec="none",
                                zorder=1))
    ax.text(PX0, 350, "RealPage remedies as switches", fontsize=9.5, weight="bold", color=INK, va="center")
    switch(ax, 306, "Hub's goal", [("both", "both firms"), ("own", "each client")], goal, changed[0], not hub)
    switch(ax, 260, "Rival data", [("current", "current"), ("stale", "stale"), ("none", "none (ban)")], data,
           changed[1], not hub)
    switch(ax, 214, "Firm adherence", [("auto", "auto-accept"), ("band", "±3% band"), ("disc", "discretion")],
           adh, changed[2], not hub)
    ax.plot([PX0, PX1], [188, 188], color=GRID, lw=1, zorder=2)
    ax.text(PX0, 170, name, fontsize=10.5, weight="bold", color=INK, va="center")
    ax.text(PX0, 153, "profit gain, Claude Haiku 5.5 (n = 20)", fontsize=7.5, color=INK2, va="center")
    yb = 104  # the outcome bar: 0 = competitive at PX0, 1 = joint monopoly at PX1
    ax.add_patch(FancyBboxPatch((PX0, yb - 5), PX1 - PX0, 10, boxstyle="round,pad=0,rounding_size=5", fc=GRID,
                                ec="none", zorder=3))
    if step == 4:
        w = max(gain, 0) * (PX1 - PX0) * u
        if w > 0:
            ax.add_patch(FancyBboxPatch((PX0, yb - 5), max(w, 10), 10, boxstyle="round,pad=0,rounding_size=5",
                                        fc=ORANGE, ec="none", zorder=4))
        ax.text(PX1, yb + 24, f"{gain:.2f}".replace("-", "−"), fontsize=15, weight="bold", color=INK,
                va="center", ha="right")
        ax.text(PX0, 60, note, fontsize=8, color=INK, va="center")
    xn = PX0 + NO_ADVISOR * (PX1 - PX0)
    ax.plot([xn, xn], [yb - 8, yb + 15], color=INK, lw=1.1, zorder=5)
    ax.text(xn + 4, yb + 16, "no advisor", fontsize=7, color=INK2, va="center")
    ax.text(PX0, yb - 17, "0 = competitive", fontsize=7, color=INK2, va="center")
    ax.text(PX1, yb - 17, "1 = joint monopoly", fontsize=7, color=INK2, va="center", ha="right")
    ax.text(24, 13, "100 rounds per run; outcomes are means over the last 20. Seven models tested; results differ "
            "by model.", fontsize=7, color=MUTED, va="center")


def plan():
    """(scenario, step, progress 0-1, duration in ms) for every frame; step 4 is the outcome."""
    out = []
    for s in range(len(SCENARIOS)):
        slow, first = s < TEACH, len(out)
        for step in range(4) if SCENARIOS[s][1] else (2, 3):  # without a hub, steps 1-2 do not happen
            out += [(s, step, k / (STEP_FRAMES - 1),
                     STEP_MS[slow] + (STEP_PAUSE_MS[slow] if k == STEP_FRAMES - 1 else 0)) for k in range(STEP_FRAMES)]
        out[first] = out[first][:3] + (out[first][3] + SCENE_PAUSE_MS,)  # a still beat as the scene opens
        out += [(s, 4, k / GROW_FRAMES, GROW_MS) for k in range(1, GROW_FRAMES)]
        out += [(s, 4, 1.0, HOLD_MS[slow] // HOLD_SPLIT)] * HOLD_SPLIT
    return out


def progress(frames):
    """For each frame, the share of its scene's duration elapsed by the frame's end (the progress-bar fill)."""
    total, done, out = {}, {}, []
    for s, *_, d in frames:
        total[s] = total.get(s, 0) + d
    for s, *_, d in frames:
        done[s] = done.get(s, 0) + d
        out.append(done[s] / total[s])
    return out


def main(out=os.path.join(HERE, "report", "figures", "arch_playground.gif")):
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])

    def render(s, step, u, prog=0.5):
        draw(ax, s, step, u, prog)
        fig.canvas.draw()
        return Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[..., :3].copy())

    frames = plan()
    # one shared palette, built from a sample of frames, so colours do not shimmer from frame to frame
    sample = [render(s, step, 0.5) for s in range(len(SCENARIOS)) for step in (1, 2)] + [render(5, 4, 1.0)]
    sheet = Image.new("RGB", (W, H * len(sample)))
    for i, im in enumerate(sample):
        sheet.paste(im, (0, H * i))
    palette = sheet.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    images = [render(s, step, u, prog).quantize(palette=palette, dither=Image.Dither.NONE)
              for (s, step, u, _), prog in zip(frames, progress(frames))]
    images[0].save(out, save_all=True, append_images=images[1:], duration=[d for *_, d in frames], loop=0)
    plt.close(fig)
    total = sum(d for *_, d in frames) / 1000
    print(f"wrote {out} ({os.path.getsize(out) / 1e6:.2f} MB, {len(frames)} frames, {total:.1f} s loop)")


if __name__ == "__main__":
    main()
