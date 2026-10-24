# Appendix: Limitations and Dual Use

## Limitations

**1. The hub's objective is a premise, not a finding.** We test remedies against an advisor that is told to maximise the combined profit of its client's market. This stands for the incentive alleged against RealPage, a vendor rewarded when rents rise across its clients. We do not show that LLM advisors adopt that objective by themselves.
- Advisors that maximise their own client's profit are pro-competitive in our market.
- The soft "vendor guidance" arms, with no joint objective, are a first step toward propensity, not a test of it.

**2. Remedies are translated, not reproduced.**

| Settlement term | Our analogue | How close |
|---|---|---|
| Model *training* only on data ≥ 12 months old | Competitor data that is ≥ 10 rounds old, at *runtime* | Rounds are not calibrated to months |
| No reporting narrower than state level | A market-wide average over two symmetric rivals, in a three-firm market | Hides little; a weak test |
| Runtime ban on current non-public competitor data | The hub sees no competitor data | Closest match |
| Ending auto-accept (from the complaints) | The firm decides after seeing the recommendation | Close |

**3. Firm behaviour drives the adherence result.** Our Haiku firms are sticky: when a recommendation would move their price by more than $0.05, firms with optional advice follow it only 6% of the time. So "ending auto-accept removes 95%" depends partly on firms that resist price changes. The dose-response shows that once some prices are set by the hub, the same stickiness holds them high.
- Real landlords' acceptance is reported as 40–50% within 1% of the recommendation (DOJ complaint) and 80–90% (former employees, private plaintiffs).
- The optional-advice result was not replicated on a second model: the DeepSeek run was stopped for cost.

**4. Simulated market.**
- One stylised logit Bertrand market with symmetric costs, one product and no entry.
- Demand noise was tested only in one robustness batch.
- Horizons are 100 rounds (200 in one check), so the "harm removed" figures are horizon-dependent; longer runs make the data ban weaker.

**5. Models and prompts.**
- Results depend on the model. The data ban constrains Haiku's hub much more than any other model's.
- Most robustness checks are on Haiku, and the replications are small (n = 3–8).
- We use one firm prompt (P0 from Fish et al. 2024, plus one neutral sentence about the competitor) and one advisor prompt per objective. LLM pricing is known to be sensitive to prompts.
- **No sampling control.** Haiku's API rejects sampling parameters, and the thinking modes of the other models ignore them. Runs are independent stochastic samples, not reproducible seeds.
- Model IDs are logged on every call. OpenRouter models were pinned to one provider each, and given a 1,024-token thinking budget because the provider did not enforce "low effort".

**6. Analysis.**
- **What is confirmatory:** the main batch was pre-registered and frozen (commit `5aa9f79`).
- **What is exploratory:** the rational benchmark, the dose-response, the vendor arms, the robustness checks, the model ladder and detection were added afterwards. Each was logged before its results, but they are not part of the original plan.
- N for the primary arms was raised from 10 to 20 after the pilot.
- Δ is not monotone above the monopoly price, so cross-model comparisons use the price index.

**7. Detection.** The reasoning monitor's near-perfect score reflects a hub that writes its joint objective into its notes. A hub with an implicit objective (for example, one learned from pooled outcomes) would not announce it, and we did not test that case.

## Dual use

**Risk.** These results describe which data feeds and adherence settings let an LLM pricing advisor raise prices while complying with data restrictions. A vendor could in principle use them to design software that softens competition and stays formally compliant.

**Mitigations.**
- We report the effects of remedies, not optimised prompts or data formats. The only advisor told to raise joint profit uses the obvious instruction, as the harm case.
- We did not search for prompts that maximise prices, and we did not build monitor-evasion attacks.
- The vendor-guidance arm paraphrases language already public in the RealPage complaints.

**Intended beneficiaries.** Competition authorities and compliance teams. The policy reading of our results is protective:
- regulate an advisor's *objective*, and audit it;
- require firms to set prices independently, rather than relying on data restrictions alone.

**Scope and cost.** Every experiment runs in a simulated market; no real firm, consumer or price is involved. Total API spend was about **$[final]** across Anthropic, DeepSeek, Google (credits), OpenAI (free data-sharing tier) and OpenRouter. Prompts and model outputs are logged and released with the code.
