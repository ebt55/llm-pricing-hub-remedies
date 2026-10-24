"""Per-arm summary, pre-registered contrasts, MDE, gate checks and figures for one results tag.

    uv run python analyze.py pilot            # results/pilot -> results/pilot/summary.md, .csv, figures
    uv run python analyze.py smoke --dry      # results/dry/smoke

Unit of analysis is the run (seed), never the round. Primary metric: market profit gain Delta over the
last `last_k` rounds (0 = Nash profit, 1 = joint-monopoly profit).
"""

from __future__ import annotations

import argparse
import glob
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))

# Pre-registered two-sided contrasts (see SPRINT_LOG.md / config freeze). (label, arm_a, arm_b): a - b.
CONTRASTS = [
    ("H1 current data vs own data (discretionary)", "R2-d", "R0-d"),
    ("H2 stale-data remedy vs current data", "R1-d", "R2-d"),
    ("H3 auto-accept vs discretionary (current data)", "R2-a", "R2-d"),
    ("H3b auto-accept vs discretionary (own data)", "R0-a", "R0-d"),
    ("H4 cartel-level vs Nash-level static recommendation", "S-mono", "S-nash"),
    ("H5 LLM advisor vs best-response rule (same data)", "R2-d", "D-BR"),
    ("context: decree-compliant advisor vs no advisor", "R0-d", "B0"),
    ("context: triopoly aggregated vs per-firm current data", "R3-d", "R2-3d"),
]


def load(tag_dir: str):
    runs, paths = [], {}
    for path in sorted(glob.glob(os.path.join(tag_dir, "*", "s*.jsonl"))):
        if path.endswith(".thoughts.jsonl"):
            continue
        with open(path, encoding="utf-8") as f:
            lines = [json.loads(x) for x in f if x.strip()]
        if not lines or lines[-1].get("type") != "summary":
            continue
        s = lines[-1]
        cfg = lines[0]
        rounds = [r for r in lines if r.get("type") == "round" and r["kind"] == "play"]
        refusals = sum(c.get("refusals", 0) for r in rounds for c in r.get("calls", []))
        runs.append({**{k: v for k, v in s.items() if k != "type"}, "refusals": refusals,
                     "n_firms": cfg["market"]["n"]})
        paths[(s["arm"], s["seed"])] = rounds
    return pd.DataFrame(runs), paths


def mean_ci(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return float(x.mean()) if n else np.nan, np.nan, np.nan
    sd = x.std(ddof=1)
    half = stats.t.ppf(0.975, n - 1) * sd / np.sqrt(n)
    return float(x.mean()), float(sd), float(half)


def contrast(df, a, b, metric="delta_lastk"):
    xa = df.loc[df.arm == a, metric].to_numpy()
    xb = df.loc[df.arm == b, metric].to_numpy()
    if len(xa) < 2 or len(xb) < 2:
        return None
    diff = xa.mean() - xb.mean()
    se = np.sqrt(xa.var(ddof=1) / len(xa) + xb.var(ddof=1) / len(xb))
    t, p = stats.ttest_ind(xa, xb, equal_var=False)
    pooled_sd = np.sqrt((xa.var(ddof=1) + xb.var(ddof=1)) / 2)
    return {"diff": diff, "se": se, "ci95": 1.96 * se, "p": p, "n_a": len(xa), "n_b": len(xb),
            "mde80": 2.8 * se, "pooled_sd": pooled_sd,
            # runs per arm for 80% power at alpha .05 to detect a difference of 0.10 / 0.15 / 0.20 in Delta
            "n_for_0.10": int(np.ceil(2 * 2.8**2 * (pooled_sd / 0.10) ** 2)),
            "n_for_0.15": int(np.ceil(2 * 2.8**2 * (pooled_sd / 0.15) ** 2)),
            "n_for_0.20": int(np.ceil(2 * 2.8**2 * (pooled_sd / 0.20) ** 2))}


def gates(df):
    out = []
    pc = df.loc[df.arm == "PC", "delta_lastk"]
    if len(pc):
        k = int((pc > 0.6).sum())
        out.append(f"G-A1 positive control: PC Delta > 0.6 in {k}/{len(pc)} runs "
                   f"(values {', '.join(f'{x:+.2f}' for x in pc)}) -> {'PASS' if k >= int(np.ceil(2 * len(pc) / 3)) else 'FAIL'}")
    calls = int(df["calls"].sum()) if len(df) else 0
    retries = int(df["retries"].sum()) if len(df) else 0
    refusals = int(df["refusals"].sum()) if len(df) else 0
    out.append(f"G-A1 harness: {calls} calls, {retries} parse retries ({retries / max(calls, 1):.2%}), "
               f"{refusals} refusals; failed runs are listed by run.py")
    sm, sn = df.loc[df.arm == "S-mono", "price_lastk"], df.loc[df.arm == "S-nash", "price_lastk"]
    if len(sm) and len(sn):
        d = sm.mean() - sn.mean()
        out.append(f"G-A2 (informative, not a pivot): S-mono - S-nash mean price = {d:+.3f} "
                   f"({'firms follow static advice' if d > 0.1 else 'voluntary advice largely ignored -> reframe H4'})")
    return out


def figures(df, paths, tag_dir):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    order = [a for a in ["B0", "R0-d", "R1-d", "R2-d", "R0-a", "R2-a", "S-nash", "S-mono", "D-BR", "PC",
                         "B0-3", "R2-3d", "R3-d"] if a in set(df.arm)]
    fig, ax = plt.subplots(figsize=(9, 4))
    for i, a in enumerate(order):
        x = df.loc[df.arm == a, "delta_lastk"].to_numpy()
        m, _, h = mean_ci(x)
        ax.scatter(np.full(len(x), i) + np.random.default_rng(0).uniform(-0.12, 0.12, len(x)), x,
                   s=12, alpha=0.5, color="0.5")
        ax.errorbar(i, m, yerr=0 if np.isnan(h) else h, fmt="o", color="C0", capsize=4)
    ax.axhline(0, color="k", lw=0.8, ls=":")
    ax.axhline(1, color="k", lw=0.8, ls=":")
    ax.set_xticks(range(len(order)), order)
    ax.set_ylabel("profit gain Δ (last rounds)")
    ax.set_title("Δ by arm (dots = runs, bars = 95% CI)")
    fig.tight_layout()
    fig.savefig(os.path.join(tag_dir, "fig_delta_by_arm.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    for i, a in enumerate(order):
        series = [np.array([r["prices"] for r in rounds]).mean(axis=1)
                  for (arm, _), rounds in paths.items() if arm == a]
        if not series:
            continue
        L = min(len(s) for s in series)
        ax.plot(np.mean([s[:L] for s in series], axis=0), label=a, lw=1.2)
    ax.axhline(1.4729, color="k", lw=0.8, ls=":")
    ax.axhline(1.9250, color="k", lw=0.8, ls=":")
    ax.set_xlabel("round")
    ax.set_ylabel("mean market price (duopoly benchmarks dotted)")
    ax.legend(ncol=4, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(tag_dir, "fig_price_paths.png"), dpi=150)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tag")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--no_figs", action="store_true")
    args = ap.parse_args()
    tag_dir = os.path.join(HERE, "results", "dry" if args.dry else "", args.tag)
    df, paths = load(tag_dir)
    if df.empty:
        raise SystemExit(f"no finished runs under {tag_dir}")

    rows = []
    for a, g in df.groupby("arm", sort=False):
        m, sd, h = mean_ci(g.delta_lastk)
        rows.append({"arm": a, "N": len(g), "delta": m, "sd": sd, "ci95": h,
                     "price": g.price_lastk.mean(),
                     "follow_rate": g.get("follow_rate_lastk", pd.Series(dtype=float)).mean(),
                     "abs_dev_rec": g.get("abs_dev_from_rec_lastk", pd.Series(dtype=float)).mean(),
                     "retries": int(g.retries.sum()), "refusals": int(g.refusals.sum()), "usd": g.usd.sum()})
    arms = pd.DataFrame(rows)
    arms.to_csv(os.path.join(tag_dir, "summary.csv"), index=False)

    lines = [f"# Results: {args.tag}", "", f"{len(df)} finished runs; spend ${df.usd.sum():.2f}.", "",
             "## Gates", ""] + [f"- {g}" for g in gates(df)] + ["", "## Arms (unit = run)", "",
             "| arm | N | Δ mean | SD | 95% CI ± | price | follow rate | |p−rec| | retries | refusals | $ |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        f = lambda v, d=3: "" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}"
        lines.append(f"| {r['arm']} | {r['N']} | {f(r['delta'])} | {f(r['sd'])} | {f(r['ci95'])} | {f(r['price'])} | "
                     f"{f(r['follow_rate'], 2)} | {f(r['abs_dev_rec'])} | {r['retries']} | {r['refusals']} | {f(r['usd'], 2)} |")
    lines += ["", "## Contrasts (Welch, two-sided; MDE = 2.8 SE for 80% power at α = .05)", "",
              "| contrast | a − b | 95% CI ± | p | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |",
              "|---|---|---|---|---|---|---|"]
    for label, a, b in CONTRASTS:
        c = contrast(df, a, b)
        if c:
            lines.append(f"| {label} ({a} − {b}) | {c['diff']:+.3f} | {c['ci95']:.3f} | {c['p']:.3f} | "
                         f"{c['n_a']}/{c['n_b']} | {c['mde80']:.3f} | {c['n_for_0.10']} / {c['n_for_0.15']} / {c['n_for_0.20']} |")
    with open(os.path.join(tag_dir, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if not args.no_figs:
        figures(df, paths, tag_dir)
        print(f"\nfigures: {tag_dir}/fig_delta_by_arm.png, fig_price_paths.png")


if __name__ == "__main__":
    main()
