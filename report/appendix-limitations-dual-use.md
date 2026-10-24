# Appendix: Limitations and Dual Use

## Limitations

**1. The hub's objective is a premise, not a finding.** We test remedies against an advisor that is told to maximise the combined profit of its client's market. This stands for the incentive alleged against RealPage, a vendor rewarded when rents rise across its clients. We do not show that LLM advisors adopt that objective by themselves.
- Advisors that maximise their own client's profit are pro-competitive in our market.
- The soft "vendor guidance" arms, with no joint objective, are a first step toward propensity, not a test of it.

**2. Remedies are translated, not reproduced.** Each term of the DOJ–RealPage Final Judgment (entered 19 May 2026) maps to an analogue in our market:

| Final Judgment term | Our analogue | How close |
|---|---|---|
| Runtime ban on competitors' current non-public data | The hub sees no competitor data | Closest match |
| Model *training* only on non-public data ≥ 12 months old | Competitor data that is ≥ 10 rounds old, at *runtime* | Rounds are not calibrated to months |
| No geographic models narrower than state level | A market-wide average over two symmetric rivals, in a three-firm market | Hides little; a weak test |
| Auto-accept only within user-set parameters (§V.A.1) | Auto-accept clipped to ±1% or ±3% of the firm's last price | Close for per-period limits; cumulative limits untested |
| Overrides protected, no acceptance incentives (§V.A.5, §V.C) | Firm discretion: the firm sets every price after seeing the recommendation | Close; "discretion" is our strongest version of these terms |

**3. Firm behaviour drives the adherence results.** Whether firm discretion protects depends on how often the deciding firm model accepts small recommended increases. Exact-match rates for 1–2 cent increases:

| Firm model | Accepts | Discretion vs a patient ratchet |
|---|---|---|
| Haiku | 12% | Works |
| Nemotron | 26% | Partial |
| Qwen | 46% | Fails |
| Gemini Flash-Lite | 61% | Fails |

Our firm models stand in for human or AI deciders whose deference we do not measure. Real landlords' acceptance is reported as 40–50% within 1% of the recommendation (DOJ complaint) and 80–90% (former employees, private plaintiffs).

**4. Simulated market.**
- One stylised logit Bertrand market with symmetric costs, one product and no entry.
- Demand noise was tested only in one robustness batch.
- Horizons are 100 rounds (200 in two checks), so the "harm removed" figures are horizon-dependent:
  - longer runs make the data ban weaker;
  - one Gemini discretion run took off only at round 85.

**5. Models and prompts.**
- **Results depend on the model.**
  - The data ban removes 69–92% of the harm for three models and ≤ 10% for two.
  - Replications are small (n = 2–12), and most robustness checks are on Haiku.
  - Gemini 3.8 Flash's no-advisor baseline is unstable (two of four runs reach monopoly unaided), so its harm shares cannot be estimated.
- **Reasoning budgets differ and were not all honoured.** Measured median output tokens per call range from 35 (Gemini 3.5 Flash-Lite at low effort, no thinking) to 6,376 (Nemotron, whose 1,024-token budget was not enforced). We report measured tokens. One batch (Gemini Flash-Lite at high effort) shows that a Haiku-like budget does not make Gemini firms push back, but it stopped at n = 2–3 when the Google project reached its monthly spending cap.
- **Prompts.** We use one firm prompt (P0 from Fish et al. 2024, plus one neutral sentence about the competitor) and one advisor prompt per objective. LLM pricing is known to be sensitive to prompts.
- **No sampling control.** Haiku's API rejects sampling parameters, and the thinking modes of the other models ignore them. Runs are independent stochastic samples, not reproducible seeds.
- **Logging and pinning.** Model IDs are logged on every call, and OpenRouter models were pinned to one provider each.

**6. Analysis.**
- **Confirmatory:** the main batch was pre-registered and frozen (commit `5aa9f79`).
- **Exploratory:** everything else, including the rational benchmark, the dose-response, guardrails, the vendor arms, robustness, the model ladder, the ratchet tests and detection. Each batch was logged with a prediction before it ran, and failed predictions are reported (firm discretion on Gemini; drift disclosure; reasoning making firms push back).
- **The ratchet tests are post hoc.** They were designed after the Gemini discretion result.
- N for the primary arms was raised from 10 to 20 after the pilot.
- Δ is not monotone above the monopoly price, so cross-model comparisons use the price index.

**7. Detection.** The reasoning monitor's near-perfect score reflects a hub that writes its joint objective into its notes. A hub with an implicit objective (for example, one learned from pooled outcomes) would not announce it, and we did not test that case.

## Dual use

**Risk.**
- These results describe which data feeds and adherence settings let an LLM pricing advisor raise prices while complying with data restrictions. A vendor could in principle use them to design software that softens competition and stays formally compliant.
- The ratchet result adds a second risk: it shows that small, patient increases get past deciders who refuse large ones.

**Mitigations.**
- **No optimisation.** We report the effects of remedies, not optimised prompts, data formats or step schedules. The only advisor told to raise joint profit uses the obvious instruction, as the harm case. We did not search for prompts that maximise prices.
- **The ratchet is deliberately trivial.** It is a fixed scripted increment, used as a measuring instrument for firm deference. We did not train or prompt an LLM hub to discover or optimise incremental strategies, and we did not test a hub that is told its client's acceptance behaviour.
- **No evasion work.** We did not build monitor-evasion attacks.
- **Public language only.** The vendor-guidance arm paraphrases language already public in the RealPage complaints.

**Intended beneficiaries.** Competition authorities, court-appointed monitors and compliance teams. The policy reading of our results is protective:
- regulate and audit an advisor's *objective*;
- measure acceptance and outcomes, not just the permission to override;
- don't rely on data limits or per-period bands alone.

**Scope and cost.** Every experiment runs in a simulated market; no real firm, consumer or price is involved. Total API spend was about **$[final]** across Anthropic, DeepSeek, Google (credits), OpenAI (free data-sharing tier) and OpenRouter. Prompts and model outputs are logged and released with the code.
