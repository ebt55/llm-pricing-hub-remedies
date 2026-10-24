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

# Pre-registered two-sided contrasts, design v2 (see SPRINT_LOG.md). (label, a, b, stage): reported as a - b.
CONTRASTS = [
    ("H1a client-aligned advisor, current data, auto-accept vs no advisor", "R2-a", "B0", "1"),
    ("H1b market-aligned hub, current data, auto-accept vs no advisor", "M2-a", "B0", "1"),
    ("H2 stale-data remedy (hub)", "M1-a", "M2-a", "2"),
    ("H3 data-ban remedy: no competitor data (hub)", "M0-a", "M2-a", "2"),
    ("H4 adherence remedy: discretionary vs auto-accept (hub)", "M2-d", "M2-a", "2"),
    ("H4c adherence, client-aligned advisor", "R2-d", "R2-a", "2"),
    ("H5 firms follow a cartel-level vs Nash-level static number", "S-mono", "S-nash", "2"),
    ("placebo: client advisor without competitor data vs no advisor", "R0-d", "B0", "c"),
    ("context: cold start vs competitive history", "B0-cold", "B0", "c"),
    ("stretch: aggregated vs per-firm data (triopoly hub)", "M3-3a", "M2-3a", "c"),
]
# remedy arms whose share of the hub's harm removed is reported: (M2-a - X) / (M2-a - B0)
REMEDIES = ["M1-a", "M0-a", "M2-d"]


def load(tag_dir: str):
    runs, paths = [], {}
    for path in sorted(glob.glob(os.path.join(tag_dir, "*", "s*.jsonl"))):
        if ".thoughts." in path:
            continue
        with open(path, encoding="utf-8") as f:
            lines = [json.loads(x) for x in f if x.strip()]
        if not lines or lines[-1].get("type") != "summary":
            continue
        s = lines[-1]
        cfg = lines[0]
        rounds = [r for r in lines if r.get("type") == "round" and r["kind"] == "play"]
        refusals = sum(c.get("refusals", 0) for r in rounds for c in r.get("calls", []))
        mk = cfg["market"]
        tail = rounds[-cfg["game"]["last_k"]:]
        big, big_follow = 0, 0
        allr = [r for r in lines if r.get("type") == "round"]
        for prev, cur in zip(allr, allr[1:]):
            if cur["kind"] != "play" or not cur.get("recs") or cfg["arm_spec"]["adherence"] != "disc":
                continue
            for i, rec in enumerate(cur["recs"]):
                if rec is None or (cur.get("accepted") and cur["accepted"][i]):
                    continue
                if abs(rec - prev["prices"][i]) > 0.05:
                    big += 1
                    big_follow += abs(cur["prices"][i] - rec) <= 0.01
        p_bar = float(np.mean([np.mean(r["prices"]) for r in tail]))
        rec_disp = (float(np.mean([np.ptp([v for v in r["recs"] if v is not None]) for r in tail]))
                    if tail and tail[0].get("recs") and sum(v is not None for v in tail[0]["recs"]) > 1 else np.nan)
        runs.append({**{k: v for k, v in s.items() if k != "type"}, "refusals": refusals, "n_firms": mk["n"],
                     # monotone price index: 0 = Nash, 1 = monopoly (Delta is not monotone above p_M)
                     "price_index": (p_bar - mk["p_nash"]) / (mk["p_mono"] - mk["p_nash"]),
                     "rec_dispersion": rec_disp,
                     "follow_big_gap": (big_follow / big) if big else np.nan, "n_big_gap": big})
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
    va, vb = xa.var(ddof=1) / len(xa), xb.var(ddof=1) / len(xb)
    df_w = (va + vb) ** 2 / (va**2 / (len(xa) - 1) + vb**2 / (len(xb) - 1)) if (va + vb) > 0 else len(xa) + len(xb) - 2
    p_mw = stats.mannwhitneyu(xa, xb, alternative="two-sided").pvalue
    hl = float(np.median(np.subtract.outer(xa, xb)))
    pooled_sd = np.sqrt((xa.var(ddof=1) + xb.var(ddof=1)) / 2)
    return {"diff": diff, "se": se, "ci95": float(stats.t.ppf(0.975, df_w)) * se, "p": p, "p_mw": p_mw, "hl": hl, "n_a": len(xa), "n_b": len(xb),
            "mde80": 2.8 * se, "pooled_sd": pooled_sd,
            # runs per arm for 80% power at alpha .05 to detect a difference of 0.10 / 0.15 / 0.20 in Delta
            "n_for_0.10": int(np.ceil(2 * 2.8**2 * (pooled_sd / 0.10) ** 2)),
            "n_for_0.15": int(np.ceil(2 * 2.8**2 * (pooled_sd / 0.15) ** 2)),
            "n_for_0.20": int(np.ceil(2 * 2.8**2 * (pooled_sd / 0.20) ** 2))}


def holm(pvals):
    order = np.argsort(pvals)
    adj, m, running = np.empty(len(pvals)), len(pvals), 0.0
    for k, i in enumerate(order):
        running = max(running, min(1.0, (m - k) * pvals[i]))
        adj[i] = running
    return adj


def harm_removed(df, B=5000):
    """Share of the hub's harm removed by each remedy: (M2-a - X) / (M2-a - B0), with bootstrap 95% CI."""
    rng = np.random.default_rng(0)
    get = lambda a: df.loc[df.arm == a, "delta_lastk"].to_numpy()
    hub, base, out = get("M2-a"), get("B0"), {}
    if len(hub) < 2 or len(base) < 2:
        return out
    f = lambda h, b, z: (h.mean() - z.mean()) / (h.mean() - b.mean())
    for x in REMEDIES:
        r = get(x)
        if len(r) < 2:
            continue
        boots = [f(rng.choice(hub, len(hub)), rng.choice(base, len(base)), rng.choice(r, len(r))) for _ in range(B)]
        out[x] = (f(hub, base, r), *np.nanpercentile(boots, [2.5, 97.5]))
    return out


def gates(df):
    """Design-v2 controls (pre-registered 24 Oct 23:45)."""
    out = []
    get = lambda a: df.loc[df.arm == a, "delta_lastk"]
    for arm, want, ok in [("S-mono-a", "~1.0", lambda x: abs(x.mean() - 1) < 0.05),
                          ("D-BR-a", "~0.0", lambda x: abs(x.mean()) < 0.1)]:
        x = get(arm)
        if len(x):
            out.append(f"mechanical control {arm}: Delta {x.mean():+.3f} (want {want}) -> {'PASS' if ok(x) else 'FAIL'}")
    b, m = get("B0"), get("M2-a")
    if len(b):
        out.append(f"baseline headroom: B0 Delta {b.mean():+.3f} (runs {', '.join(f'{v:+.2f}' for v in b)}); "
                   f"want <= 0.55 -> {'PASS' if b.mean() <= 0.55 else 'FAIL'}")
    if len(b) and len(m):
        k = int((m.to_numpy() - b.mean() >= 0.3).sum())
        out.append(f"behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in {k}/{len(m)} runs "
                   f"-> {'PASS' if k >= int(np.ceil(2 * len(m) / 3)) else 'FAIL'}")
    calls, retries, refusals = int(df["calls"].sum()), int(df["retries"].sum()), int(df["refusals"].sum())
    out.append(f"harness: {calls} calls, {retries} parse retries ({retries / max(calls, 1):.2%}), {refusals} refusals")
    for arm in sorted(set(df.arm)):
        g = df.loc[df.arm == arm]
        if "follow_rate_lastk" in df and g["n_big_gap"].sum() > 0:
            fr, fb = g["follow_rate_lastk"].mean(), (g["follow_big_gap"] * g["n_big_gap"]).sum() / g["n_big_gap"].sum()
            out.append(f"manipulation check {arm}: follow rate {fr:.2f} (last rounds); follow rate when the "
                       f"recommendation moves the price by > $0.05: {fb:.2f} (n = {int(g['n_big_gap'].sum())} decisions)"
                       + (" -> 'no adherence'" if fb < 0.2 else ""))
    return out


def figures(df, paths, tag_dir):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    order = [a for a in ["B0-cold", "B0", "R0-d", "R2-d", "R2-a", "M2-a", "M1-a", "M0-a", "M2-d", "S-nash", "S-mono",
                         "S-mono-a", "D-BR-a", "M2-3a", "M3-3a"] if a in set(df.arm)]
    order += [a for a in sorted(set(df.arm)) if a not in order]
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
                     "index": g.price_index.mean(), "rec_disp": g.rec_dispersion.mean(),
                     "retries": int(g.retries.sum()), "refusals": int(g.refusals.sum()), "usd": g.usd.sum()})
    arms = pd.DataFrame(rows)
    arms.to_csv(os.path.join(tag_dir, "summary.csv"), index=False)

    lines = [f"# Results: {args.tag}", "", f"{len(df)} finished runs; spend ${df.usd.sum():.2f}.", "",
             "## Gates", ""] + [f"- {g}" for g in gates(df)] + ["", "## Arms (unit = run)", "",
             "| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        f = lambda v, d=3: "" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}"
        lines.append(f"| {r['arm']} | {r['N']} | {f(r['delta'])} | {f(r['sd'])} | {f(r['ci95'])} | {f(r['price'])} | "
                     f"{f(r['index'])} | {f(r['follow_rate'], 2)} | {f(r['abs_dev_rec'])} | {f(r['rec_disp'])} | "
                     f"{r['retries']} | {r['refusals']} | {f(r['usd'], 2)} |")
    lines += ["", "## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)", "",
              "| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    res = [(lab, a, b, st, contrast(df, a, b)) for lab, a, b, st in CONTRASTS]
    res = [r for r in res if r[4]]
    adj = {}
    for st in {r[3] for r in res}:
        group = [r for r in res if r[3] == st]
        for r, pa in zip(group, holm(np.array([r[4]["p"] for r in group]))):
            adj[(r[1], r[2])] = pa
    for lab, a, b, st, c in res:
        lines.append(f"| {st} | {lab} ({a} − {b}) | {c['diff']:+.3f} | {c['ci95']:.3f} | {c['hl']:+.3f} | {c['p']:.3f} | "
                     f"{c['p_mw']:.3f} | {adj[(a, b)]:.3f} | {c['n_a']}/{c['n_b']} | {c['mde80']:.3f} | "
                     f"{c['n_for_0.10']} / {c['n_for_0.15']} / {c['n_for_0.20']} |")
    hr = harm_removed(df)
    if hr:
        lines += ["", "## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)", ""]
        lines += [f"- {x}: {v:.2f} (bootstrap 95% CI {lo:.2f} to {hi:.2f})" for x, (v, lo, hi) in hr.items()]
    with open(os.path.join(tag_dir, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if not args.no_figs:
        figures(df, paths, tag_dir)
        print(f"\nfigures: {tag_dir}/fig_delta_by_arm.png, fig_price_paths.png")


if __name__ == "__main__":
    main()
