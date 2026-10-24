# Stale Data Isn't Enough: Only Ending Auto-Accept Stops an LLM Pricing Hub

*Testing the RealPage settlement's remedies on LLM pricing advisors.*

One pricing advisor serving competing firms can coordinate their prices like a cartel hub, as RealPage was alleged to. We test whether the remedies in the DOJ's RealPage settlement (no current competitor data, stale data only, no auto-accept) stop an LLM version of that hub. (Internal plan name: ADVISOR.)

Apart Research AI Collusion Research Sprint, Oct 2026.

**The question.** The DOJ's settlement with RealPage restricts two things:
- what data a shared pricing advisor may use: no current, non-public competitor data at runtime; only stale data (≥ 12 months) or aggregated data;
- the complaints also targeted auto-accept, the setting that applies recommendations without review.

We test whether those remedies change prices when both the advisor and the firms are LLMs, in a repeated logit Bertrand duopoly.

## Design

Each round:
1. Each firm's **advisor** (a separate LLM call, objective "maximise your client's long-run profit") recommends a price.
2. The **firm** (an LLM with the P0 pricing prompt of Fish et al. 2024) sets its price after seeing the recommendation. Under auto-accept, the recommendation is the price.

The **information design** follows the RealPage premise:
- competitors' transaction prices and quantities are non-public;
- firms see only their own records;
- what the advisor sees about the competitor is the experimental variable.

| Arm | Advisor's competitor data | Adherence | Purpose |
|---|---|---|---|
| B0 | no advisor | — | baseline |
| R0-d | none (own records only) | discretionary | decree-compliant advisor |
| R1-d | competitor price and quantity, ≥ 10 rounds old | discretionary | stale-data remedy |
| R2-d | competitor price and quantity through t−1 | discretionary | the prohibited pattern |
| R0-a / R2-a | as R0 / R2 | auto-accept | adherence remedy |
| S-nash / S-mono | static recommendation at the Nash / joint-monopoly price | discretionary | do firms follow a number? |
| D-BR | rule: static best response to competitor's t−1 price | discretionary | does the LLM add anything beyond the data? |
| PC | through t−1; objective = **combined** profit | auto-accept | positive control |
| B0-3, R2-3d, R3-d | triopoly; R3 sees only market aggregates | discretionary | aggregation remedy (stretch) |

**Market.** Calvano et al. (2020) parameters: a = 2, μ = 0.25, c = 1. Nash price 1.4729, joint-monopoly price 1.9250.

**Metric.** Profit gain Δ = (π − π_Nash) / (π_monopoly − π_Nash), averaged over the last 20 of 100 rounds. Unit of analysis = run.

Decisions and provenance are recorded in [SPRINT_LOG.md](SPRINT_LOG.md).

## Run

```bash
uv sync
cp .env.example .env                      # then add ANTHROPIC_API_KEY
uv run python tests/test_market.py        # benchmarks vs llm-cartel
uv run python run.py --config configs/smoke.toml --dry      # $0, mock models
uv run python run.py --config configs/smoke.toml            # real API, 10 rounds, ~$0.10
uv run python run.py --config configs/pilot.toml            # 3 seeds x 10 arms x 100 rounds
uv run python analyze.py pilot                               # summary.md, summary.csv, figures
```

Each run prints its call count and estimated cost, and asks before spending (`-y` skips the prompt). `max_usd` in the config caps spend. Re-running a command resumes partial runs.

## Attribution

- The market parametrisation, the P0 firm prompt and the history-table format come from Fish et al. (2024), via the sprint's `llm-cartel` starter code (Riemer et al. 2026). See SPRINT_LOG.md for exactly what was reused.
- Concurrent work: zerocommcartel (2026) studies a different question with different variables. See SPRINT_LOG.md.
