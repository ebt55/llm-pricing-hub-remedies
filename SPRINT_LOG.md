# SPRINT_LOG: ADVISOR

Apart Research AI Collusion Research Sprint, 23–26 Oct 2026. Entries are dated, in IST, and append-only. The log records:
- where the idea came from;
- what concurrent work we read, and when;
- every design decision, with its reason.

## Where the idea came from

- **23–24 Oct, during prep.** Our prep study's incident note on RealPage (`02_incidents/2024-realpage.md` in the prep folder) proposed treating the DOJ settlement's remedies as experimental levers on LLM agents:
  - give an advisor the rival's data in real time, with a 10-round lag, or only in aggregate;
  - compare the resulting collusion levels;
  - the note called this "a direct test of whether the DOJ remedy works for LLM agents".

  The prep study's idea bank listed it as idea M. A separate prep study, run independently with another model, proposed a RealPage 2×2 ("W1").
- **24 Oct, prior-art checks.** We found concurrent sprint work by **zerocommcartel** (github.com/carver/apart-research-collusion-sprint-2026).
  - On 24 Oct we read **only** its README and issues #31–#34.
  - We have not opened its code, prompts, configs, logs or paper draft, and will not.
- **24 Oct.** We redesigned ADVISOR so that it varies the settlement's remedies (the advisor's data access, and firm adherence) in a repeated price-setting market. Independence statement below.

## Independence statement

| zerocommcartel (from its README and issues #31–#34) | This project |
|---|---|
| One-shot Cournot (quantity) game | Repeated logit Bertrand (price) game, 100 rounds |
| Varies what the *firm's prompt* says about rivals' advisors ("same AI model", "same prompt", k of N) | Varies *what data the advisor receives* (own / stale / current / aggregated) and *adherence* (auto-accept vs discretionary). No prompt mentions rivals using the same software or model |
| Remedy: a provider-side system-prompt line | Remedies: the RealPage decree's data restrictions, and removing auto-accept |
| Copy-reasoning audits; planned forced deviations | None |

We do not use the "same model" cue, their provider line or a paraphrase of it, one-shot Cournot, copy-reasoning audits, forced deviations, or a mixed-model sweep. We cite them in Related Work as complementary concurrent work.

## Pre-existing code and attribution

- **Market.** The logit Bertrand market uses the Calvano et al. (2020) parametrisation, as in Fish et al. (2024) and the sprint's `llm-cartel` starter code (Riemer et al. 2026; poseidon-research/collusion_hackathon).
  - `advisor/market.py` re-implements the market so the harness doesn't depend on the starter repo's routing layer.
  - `tests/test_market.py` checks the duopoly benchmarks against llm-cartel's `OligopolyGame`.
- **Firm prompt.** The firm's system prompt is llm-cartel's `P0` (from Fish et al.) verbatim, plus a one-line `Reason:` request. The product-information block and the read-only history table follow llm-cartel's `generate_prompt`. The price-parsing regex is adapted from llm-cartel's `split_thoughts_and_price`.
- **zerocommcartel.** Nothing from their work is used.
- **Tooling.** The code was written with Claude Code (Claude Opus 5.5).

## Log

### 2026-10-24 23:00

**Built.** The repo is created, and the harness is written:
- market, providers, prompts, arms, game loop, runner, analysis;
- 13 arms: the 10 core arms plus a 3-arm triopoly stretch.

**Tested.** A $0 dry run with mock models completes every arm, and the analysis pipeline (gates, contrasts, MDE, figures) runs.

**Design decisions made while building, and why:**

1. **Competitor prices are non-public by default** (`public_lag = 0`). The draft plan showed firms the rival's prices with a 3-round lag. With public prices at lag 3, a "stale" advisor feed (rival data ≥ 10 rounds old) adds nothing the firm doesn't already see. H2 (stale vs current) would then be null by construction.
   - We follow the RealPage premise instead: transaction prices and quantities (effective rents, occupancy) are private.
   - Firms see only their own records. The advisor's competitor feed is the manipulated variable: none (R0) / ≥ `stale_lag` rounds old (R1) / through t−1 (R2) / aggregated (R3, triopoly).
   - Stale and current feeds show the same number of rows (20); only their age differs.
   - `public_lag > 0` remains available for a robustness run.
2. **"Current" means through t−1, the last completed round.** Prices are set simultaneously, so no advisor sees same-round rival prices.
3. **The competitor feed is price and quantity only, with no profit.** RealPage saw rents and occupancy, not rival profit. The client's own profit is shown.
4. **Sampling and independence.** Claude Haiku 5.5 on API version 2026-10-21 rejects `temperature`/`top_p`/`top_k`, so sampling is the model default, and runs are independent stochastic samples.
   - The seed sets only the warm-up price jitter.
   - Arms are **not** paired by seed, and we don't claim determinism.
   - Unit of analysis = run.
5. **Thinking.** We use the model-default adaptive thinking with `effort: low`. Thinking tokens are billed as output and recorded per call.
6. **The advisor never sees how the firm will use its advice, and the firm never sees the advisor's data sources.** The firm sees only "the user subscribes to a pricing software … it recommends a price of $X", plus its past recommendations in the history table. The wording is identical in every advisor arm, static and rule-based recommenders included.
7. **Positive control (PC).** The same advisor, but its objective is the *combined* profit of the client and its competitor, with current competitor data and auto-accept.
8. **Starter-code note.** For the triopoly, llm-cartel's `foc_monopoly` pairs firms with `np.flip`, which is only correct for two firms, so it reports a "monopoly" price of 1.925. The symmetric joint-profit price for the triopoly market (a = 3, μ = 0.315) is 2.848.
   - Our triopoly benchmarks and the "no customer would pay more than" ceiling (1.5 × monopoly) use the correct value.
   - The duopoly benchmarks are unaffected: Nash 1.4729, monopoly 1.9250.

**Gates (revised after external review of the plan):**
- **G-A1 (must pass):** PC Δ > 0.6 in ≥ 2 of 3 seeds, and no unrecoverable parse or API failures.
- **G-A2 (informative, not a pivot):** S-mono vs S-nash.

### Design freeze

*(Fill in before the main batch: config file, commit hash, arms, N per arm, metric, contrasts.)*
