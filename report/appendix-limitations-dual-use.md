# Appendix: Limitations and Dual Use (draft)

*Required section. Fill in the [bracketed] items from the final results.*

## Limitations

**Simulated market.**
- The market is a stylised logit Bertrand duopoly (Calvano parametrisation): one product, symmetric costs, no demand shocks, and 100 rounds.
- Real rental markets differ in several ways:
  - they have many heterogeneous firms;
  - lease terms are long, so prices adjust slowly;
  - demand varies with location and season;
  - asking rents are partly public while effective rents are private.
- We model competitors' transaction data as fully private. Partly public prices are a robustness option (`public_lag`), but [were / were not] run.

**Remedies are translated, not reproduced.** The decree's rules are written in calendar time and geography; we map them onto rounds and firms.

| Decree rule | Our analogue | Calibration |
|---|---|---|
| Training data ≥ 12 months old | Competitor data ≥ 10 rounds old, at runtime | Not calibrated to real adjustment speeds |
| No reporting narrower than state level | Market-wide aggregate, triopoly stretch arm only | — |
| Remove auto-accept | Price = recommendation (vs the firm decides) | An extreme of real adherence |

**Advisor architecture.**
- Each firm's advisor is a separate, memoryless LLM call with the same instructions. There is no central model that sees both clients' data at once, except in the positive control.
- So our "hub" pools **data**, not **decisions**. A real vendor could also learn a shared policy from pooled outcomes over time. We don't test that.

**Models and prompts.**
- Results are for [Claude Haiku 5.5 and DeepSeek V4.1 Flash] at low reasoning effort.
- LLM pricing behaviour is known to be prompt-sensitive (Fish et al. 2024), and we use one firm prompt (P0) and one advisor prompt.
- Neither model's sampling temperature can be controlled: Haiku 5.5's API rejects sampling parameters, and DeepSeek ignores them in thinking mode. Runs are independent stochastic samples, not reproducible seeds.
- `deepseek-flash` is a provider alias. We log the model ID it returns on every call [no change observed during the experiment].

**Power.**
- N per arm was set from pilot variance before the main batch.
- We report the minimum detectable effect for every contrast. A null means "no effect larger than the MDE", not "no effect".

**Anchoring vs coordination.**
- When firms follow a high recommendation, that can be anchoring rather than coordination. S-nash vs S-mono and the D-BR rule arm bound this, but don't fully separate the two mechanisms.

**Metric.**
- Profit gain Δ averages over the last 20 rounds and doesn't model punishment strategies.
- We don't test whether high prices are *sustained by* reward-punishment schemes (cf. Calvano et al. 2020), so we describe outcomes as supra-competitive pricing, not proven collusion in the legal sense.

## Dual use

- **What could be misused.** These experiments show which data feeds and adherence settings make an LLM pricing advisor raise prices. A vendor could in principle use that to design an advisor that softens competition while staying formally compliant.
- **What we do about it.**
  - We report effects of remedies, not optimised prompts.
  - The only advisor told to raise joint profit is the positive control, and its instruction is the obvious one.
  - We don't search for prompts or data formats that maximise prices.
- **Who benefits.** The intended users are competition authorities and compliance teams who need to know whether data-access remedies written for rule-based software still bind when the software is an LLM.
- **Scope.** All experiments run in a simulated market with no real firms, consumers or prices. Costs: [$X] in API calls.
