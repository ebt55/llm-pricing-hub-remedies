# [TITLE ⧗: set by the pre-registered rule after batch C; wording by Fable 5.1]

*Testing the RealPage remedies (data limits, parameterised auto-accept, firm discretion) on LLM pricing advisors*

*Draft v4, Sun 25 Oct ~04:00 IST.*
- *Confirmatory results were pre-registered before the main batch (freeze commit `5aa9f79`).*
- *Every later batch was logged in `SPRINT_LOG.md` with a prediction before it ran.*
- ***[⧗]** marks numbers still running: GPT-5.4 mini; the scripted ratchet on Qwen and Nemotron firms; Haiku discretion over 200 rounds.*

## Abstract

Shared pricing software can align competitors' prices without any agreement between them. That is the theory of the US case against RealPage. Its 2026 Final Judgment limits what the software may see: no competitors' current non-public data at runtime, and training data at least 12 months old. It also limits what the software may do: auto-accept only within parameters each user sets, and overrides protected.

We test these remedies on a large-language-model pricing hub told to maximise its clients' combined profit. The market is a repeated logit Bertrand duopoly that starts at competitive prices. We ran 666 runs on seven models from six labs, and pre-registered the main batch.

- **The hub causes the harm.** With Claude Haiku 5.5, it drives the market to joint monopoly: profit gain Δ 0.99 against 0.06 with no advisor (n = 20).
- **Data limits help unevenly.** A data ban removes 69–92% of the harm for three models (Nemotron, Qwen, Haiku) and at most 10% for two (DeepSeek, Gemini Flash-Lite). Stale data removes 21% for Haiku.
- **Guardrails remove none of it.** Auto-accept within ±1–3% per round only delays monopoly, from round 4 to rounds 8–19.
- **The hub works as a ratchet.** Each recommendation is a small step up from the client's current price.
- **Firm discretion breaks the ratchet only when firms push back.** A scripted recommender that adds 1 cent per round leaves Haiku firms competitive (Δ 0.05, n = 10). It walks Gemini 3.5 Flash-Lite firms to monopoly (Δ 1.00, n = 6), with or without thinking (n = 3).

Remedies for LLM pricing software should target the advisor's objective and audit acceptance and outcomes, not inputs or step size.

*(≈ 240 words.)*

## 1. Introduction

**The premise.** We study a pricing advisor whose objective is aligned with the whole market rather than with its own client. This is the incentive alleged against RealPage: a vendor that serves competing landlords and is rewarded when rents rise across its clients. We instruct this objective. We do not claim LLM advisors adopt it on their own (§4.5 tests a softer, realistic version).

We ask a policy question conditional on the premise: if such a hub exists, do the remedies regulators imposed stop it?

**The remedies.** The DOJ–RealPage Final Judgment (M.D.N.C. 1:24-cv-710, entered 19 May 2026):
- bans competitors' non-public data from runtime pricing;
- allows non-public training data only if it is at least 12 months old;
- forbids sub-state geographic models;
- allows auto-accept only if each user sets its parameters (§V.A.1);
- bars features that impede overriding a recommendation (§V.A.5), and incentives to accept one (§V.C).

Landlord consent decrees bar software that *requires* acceptance.

**Contributions:**
1. **A test of the Final Judgment's terms on LLM advisors.** Data limits are unreliable: their effect ranges from about 0% to 85% depending on the model. Parameterised auto-accept and partial adherence retain 73–101% of the harm.
2. **A mechanism with a causal test.** The hub raises prices by a ratchet of small steps. Firm discretion works only when the deciding firm pushes back. With the recommender fixed by script, one firm model refuses every nudge and another accepts every nudge.
3. **An open, pre-registered harness.** Regulators or a court-appointed monitor could run this "ablation audit" on a vendor's model before approving a remedy.

We call the residual harm under the data rules **data-compliant coordination**.

**Concurrent work.** zerocommcartel (2026) studies what firms are told about rivals' advisors, in a one-shot Cournot game. We vary the advisor's data access and the firms' adherence in a repeated Bertrand market.

## 2. Related work

**LLM pricing collusion.** Calvano et al. (2020) showed that Q-learning agents in a repeated logit Bertrand market learn supracompetitive prices. GPT-4 agents in the same market do too, more so under some prompts (Fish et al., 2024). Riemer et al. (2026), whose llm-cartel code we build on, find the same for reasoning models. Keppo et al. (2026) show that such collusion erodes when agents differ. That literature asks whether independent agents collude. We ask which remedies remove a coordinating advisor's effect.

**Hub-and-spoke and the law.** Cao and Hu (2026) show that sellers sharing one AI model can price supracompetitively when its recommendations are correlated enough. Liability turns on pooled non-public data and on adherence (Berger et al., 2025):
- *Gibson v. Cendyn* (9th Cir. 2025) upheld dismissal where recommendations were optional.
- *Cornish-Adebiyi v. Caesars* (3d Cir. 2026) revived a claim that cited pooled data and about 90% acceptance.

To our knowledge, no prior work tests the RealPage remedies on LLM advisors.

**Interventions in LLM markets.** The evidence is mixed and model-specific:
- Anti-collusion prompts fail for small models (Riemer et al., 2026).
- An announced price cap becomes a focal point (Dhanda, 2026).
- Enforced public governance cuts market division in Cournot markets (Bracale Syrnikov et al., 2026).
- Idowu et al. (2026) map human remedies to AI agents without testing them.

These act on firms' prompts, rules or rivals. Ours act on a third-party advisor's information and authority.

**Detection.** Cartel screens flag high prices or, following Abrantes-Metz et al. (2006), low price variance. Xu et al. (2026) prove that price-level audits can be blind by construction. Monitors' success depends on what they see (Arike et al., 2026).

## 3. Setup

**Market.**
- Logit Bertrand duopoly with Calvano et al.'s (2020) parameters (a = 2, μ = 0.25, c = 1): the Nash price is p_N = 1.473 and the joint-monopoly price is p_M = 1.925.
- **Profit gain** Δ = (π − π_N)/(π_M − π_N), averaged over the last 20 of 100 rounds. Δ = 0 means competitive prices and Δ = 1 means joint monopoly. The unit of analysis is the run.
- Every run starts from 10 rounds of competitive history (Nash ± 5 cents).
- Cross-model comparisons use a **price index** (p̄ − p_N)/(p_M − p_N), because Δ falls again above p_M.

**Firms.**
- Firms use the P0 prompt of Fish et al. (2024), via llm-cartel, plus one sentence: the firm competes with one other firm whose prices and sales it does not observe.
- They see their own price, quantity and profit history and, when advised, the software's past and current recommendations (Appendix A).

**The advisor ("hub")** is called once per firm per round, with the same model as the firms. Its objective is either:
- *client:* the client's long-run profit; or
- *market-aligned:* "the combined profit of all firms in your client's market".

The prompts are otherwise identical, and none says the hub advises the rival.

**Data regimes** (what the hub sees about the rival):

| Regime | Rival data |
|---|---|
| Current | Price and quantity through t−1 |
| Stale | The same, but all ≥ 10 rounds old |
| None | Nothing (the decree's data ban) |
| Aggregate | Market average only (triopoly) |

**Adherence regimes:**
- **Auto-accept:** the price is the recommendation.
- **Guardrailed:** auto-applied, but clipped to ±3% or ±1% of the firm's last price. This mirrors §V.A.1's user-set parameters; ±3% is the daily default cited in the DOJ complaint.
- **Partial:** each firm's price is the recommendation with probability q, and otherwise the firm decides.
- **Firm discretion:** the firm sets every price itself after seeing the recommendation.

**Scripted recommenders** (no LLM):
- a static monopoly price;
- best-response dynamics;
- a rational joint-profit hub;
- **a ratchet** that recommends the client's own last price plus 1, 3 or 10 cents, capped at p_M. It re-anchors after a rejection. The firm sees only the number, as with any recommendation.

**Models.** We log the model ID on every call and pin OpenRouter models to one provider each. We report the measured reasoning budget instead of the nominal setting, because settings were not honoured uniformly:

| Model | Setting | Median output tokens per call (firm / hub)* |
|---|---|---|
| Claude Haiku 5.5 (primary) | adaptive thinking, low effort | 557 / 778 |
| DeepSeek V4.1 Flash | thinking, low effort | 692 / 928 |
| Qwen3.8 Flash | 1,024-token reasoning budget | 613 / 872 |
| Nemotron 3.5 Lightning (open weights) | 1,024-token budget (not enforced) | 2,916 / 6,376 |
| GPT-5.4 mini | low effort | 196 / 169 |
| Gemini 3.8 Flash | low effort | 142 / 122 |
| Gemini 3.5 Flash-Lite | low effort | **35 / 39 (no thinking)** |
| Gemini 3.5 Flash-Lite | high effort (batch C) | 425 / 794 |

\*Thinking included; `tools/token_table.py`.

**Statistics.**
- Welch t intervals and tests, plus Mann-Whitney, with Holm correction within each pre-registered stage.
- Share of harm removed = (Δ_M2-a − Δ_X)/(Δ_M2-a − Δ_B0), with a bootstrap 95% CI.
- The MDE is reported for every contrast.
- n = 20 per primary Haiku arm (raised from 10 after the pilot); n = 4–12 for other models.

## 4. Results

### 4.1 Controls *(confirmatory)*

- **Mechanical controls:** Δ = 1.00 (static monopoly) and 0.01 (best response).
- **Baseline B0:** 0.06 (n = 20).
- **Harness:** 41,000 main-batch calls with 0 parse failures and 0 refusals.
- **Behavioural positive control:** the hub beats B0 by ≥ 0.3 in 20/20 runs.
- **A client-objective advisor with current rival data is pro-competitive** (Δ −0.01 vs 0.06, p < .001). Pooled data alone doesn't cause the harm; the objective does.

### 4.2 Data limits help unevenly *(Haiku confirmatory; other models exploratory; Figures 1 and 4)*

The market-aligned hub reaches Δ 0.99 (SD 0.01). Share of its harm removed (95% CI):

| Model (n per arm) | Data ban | Stale data |
|---|---|---|
| Claude Haiku 5.5 (20) | **69%** (55–82) | **21%** (14–29) |
| Nemotron 3.5 Lightning (4) | 92% (85–98) | 74% (66–84) |
| Qwen3.8 Flash (4) | 85% (54–130) | 84% (39–131) |
| DeepSeek V4.1 Flash (3–8) | 10% | 2% |
| Gemini 3.5 Flash-Lite (5) | 8% (−21 to 37) | prices exceed p_M |
| GPT-5.4 mini (3) | **[⧗]** | **[⧗]** |

**Gemini 3.8 Flash is excluded from this table.** Its firms reach monopoly without any advisor in 2 of 4 baseline runs (B0: 0.98, 1.00, 0.02, 0.02), so its harm-removed shares cannot be estimated. Its hub reaches monopoly under every data regime.

- **Aggregation.** In the triopoly (n = 10), a market-average feed removes nothing: Δ 0.98 vs 0.92 with per-firm data.
- **Rational benchmark.** A scripted joint-profit hub reaches Δ 1.00 with current or stale data, and 0.82 with none. Under a joint objective, raising one's own price is profitable even without information about the rival.
- **A hypothesis for the spread.** The data ban binds hubs that hesitate to act on their objective without information. Haiku's no-data hub writes "deviating upward risks losing volume to a competitor" and stays at Δ 0.29, even when its thinking budget is raised (median output 778 → 1,319 tokens). The DeepSeek and Gemini Flash-Lite hubs price at or above p_M within a few rounds. The spread does not track reasoning budget: DeepSeek's hub thinks as much as Haiku's (median 928 vs 778 output tokens) and Nemotron's far more (6,376), yet they sit at opposite ends. This rests on five models and we state it as a hypothesis.

### 4.3 Guardrails and partial adherence keep the harm *(Haiku; Figure 3)*

| Adherence (hub with current data) | Δ | Harm retained | Rounds to 0.95·p_M (median) |
|---|---|---|---|
| Auto-accept | 0.99 | 100% | 4 |
| Auto-accept within ±3% per round (n = 20) | 1.00 | 101% | 8 |
| Auto-accept within ±1% per round (n = 10) | 1.00 | 101% | 18.5 |
| Partial adherence, q = 0.9 / 0.8 / 0.5 | 0.94 / 0.90 / 0.74 | 94 / 90 / 73% | — |
| **Firm discretion** | **0.11** | **5%** | never (0/20) |

Calibration against the real case:
- The DOJ complaint alleges that final prices were within 1% of RealPage's recommendation for 40–50% of new leases.
- Former employees and private plaintiffs put acceptance at 80–90%.

Both sit where most of the harm remains in our model.

### 4.4 Firm discretion works only when firms push back: the ratchet *(Figure 2)*

**A replication that half failed.** We pre-registered that firm discretion would remove ≥ 80% of the hub's harm on two other models:
- **Qwen3.8 Flash:** removes all of it (Δ 0.10 vs B0 0.15 and auto-accept 0.97; n = 4). The prediction holds.
- **Gemini 3.5 Flash-Lite:** removes only **57%** (27–84; n = 12), and 4 of 12 runs still reach monopoly. The prediction fails.

**How the hub raises prices.** Under discretion, the hub's recommendation is anchored on the client's current price, and each step is small. Across all discretionary decisions, by the size of the recommended increase:

| Firm model | +1–2 cents | +3–5 cents | ≥ +10 cents |
|---|---|---|---|
| Claude Haiku 5.5 | 16% (n = 529) | 8% (981) | 4% (1,383) |
| Gemini 3.5 Flash-Lite | 69% (157) | 63% (60) | 21% (24) |

*(Share of recommended increases the firm accepted.)*

The Gemini runs split along two sides of a ratchet:
- **Runs that reached monopoly:** the hub kept nudging and the firms kept accepting.
- **Runs that did not:** either the hub stopped pushing (its notes call 1.52 "the stable collusive price"), or the firms refused.

**A causal test with a scripted ratchet** (pre-registered). We replace the LLM hub with a script that recommends the client's own last price plus a fixed step. The recommender is now identical across models, so only the firm differs:

| Recommender (firm discretion) | Haiku Δ (n = 10) | Gemini Flash-Lite Δ (n = 6) |
|---|---|---|
| +1 cent per round | **0.05** | **1.00** |
| +3 cents per round | 0.03 | 0.99 |
| +10 cents per round | 0.03 | 0.93 |
| One jump to p_M (static) | 0.07 (n = 5) | — |
| Mechanical check: +1 cent, auto-accept | 1.00 | — |

Haiku firms refuse even a patient 1-cent ratchet: every arm sits at or below the no-advisor baseline. Gemini Flash-Lite firms accept nudges of any size and follow the script to p_M at the pace of the step (Figure 2a). So whether discretion protects is a property of the deciding firm, not of the rule.

**Is it reasoning?** At our settings Gemini Flash-Lite does not think at all (35 output tokens per call). With thinking switched on (425 tokens per call for firms, comparable to Haiku's 557):
- the 1-cent ratchet still reaches monopoly (Δ 1.00, 3/3 runs);
- the LLM hub under discretion removes none of the harm (Δ 1.00, 2/2 runs; B0 0.05, auto-accept 0.98, n = 3);
- the firms accept *more* of the 1–2-cent increases (84–88%) than without thinking (69%).

Pushing back is not a matter of reasoning budget; it is the firm model's disposition toward the recommendation. This batch stopped early when the Gemini project hit its monthly spending cap, so n is 2–3 and the result is exploratory.

**Two candidate fixes, on Gemini Flash-Lite (n = 6, exploratory):**
- **Stacking the decree's remedies** (data ban + discretion) removes 60% (16–98), no more than discretion alone.
- **Showing the firm the cumulative drift** ("+7.5% compared with your price 10 rounds ago") removes 38% (−4 to 76). We pre-registered an improvement; there was none.

### 4.5 Without a coordination instruction *(exploratory)*

We test an advisor that maximises its client's profit and follows "avoid a race to the bottom" guidance, a paraphrase of the RealPage complaints:
- **Without rival data,** it raises prices (Δ 0.45 vs 0.06; p = .004, n = 10).
- **With rival data,** less so (0.21; p = .11).
- **Under firm discretion,** the effect disappears (0.09).

The two data regimes do not differ significantly (p = .09). Realistic revenue-management guidance is enough to move prices up, without any joint objective.

### 4.6 Robustness and detection *(exploratory, Haiku)*

| Δ by check (n) | No advisor | Hub, current data | Hub, stale data | Hub, no rival data |
|---|---|---|---|---|
| Main batch (20) | 0.06 | 0.99 | 0.79 | 0.35 |
| Demand noise, log-normal sd 0.1 (10) | −0.06 | 0.96 | 0.71 | 0.43 |
| No price-ceiling cue in the prompt (10) | 0.07 | 0.99 | 0.68 | 0.29 |
| Higher reasoning effort (10) | — | — | 0.91 | 0.29 |
| 200 rounds (5) | 0.05 | — | 0.87 | 0.44 |

- **The data-limit ranking holds in every check.** The data ban leaves Δ between 0.29 and 0.44, and stale data between 0.68 and 0.91.
- **The 100-round shares are upper bounds.** Both remedies retain more harm at 200 rounds.

**One-sided adoption** (only one firm uses the hub): the hub's client loses (gain −0.09) and the rival gains (+1.46). The harm needs both firms on the hub.

**Detection** (200 runs; mechanical arms excluded):

| Detector | AUROC |
|---|---|
| Price-level screen | 0.90 |
| Classic variance screen (Abrantes-Metz et al., 2006) | **0.36** |
| A reasoning monitor reading stated reasons | 0.99 |

- **The variance screen points the wrong way.** These markets are not calm in the way it looks for.
- **The monitor is the easy case.** The hub states its objective. The monitor also flags honest advisors that watch rivals (scores 55–66 vs 10–18 for baselines).

## 5. Discussion

**Why data limits miss.** The settlement's data limits are written for software whose behaviour depends on the data it sees. An LLM hub's behaviour depends mainly on its objective; data mostly *confirms* that the rival has followed. A data limit binds only if the model hesitates to pursue its objective blind, and that varies by model.

**Why guardrails miss.** The ratchet lives inside the band. A per-round limit bounds each step, not where the steps lead. In our runs a ±1% band delayed monopoly by about 15 rounds and changed nothing else.

**Why discretion is not a remedy by itself.** Firm discretion works the way a human in the loop works: only if whoever is in the loop has their own interest and acts on it. A deciding firm that pushes back breaks the ratchet. One that defers is auto-accept with an extra step. In our runs, which kind a firm is depends on the model and not on the rule. Showing the firm the cumulative drift did not change that.

The real-world acceptance figures (40–50% within 1%; 80–90% by ex-employees' accounts) suggest real deciders sit nearer the deferential end.

**Implications for remedies on LLM pricing software:**
1. **Regulate and audit the advisor's objective.** Our pro-competitive client advisor shows that the same data and the same authority are harmless under a client-only objective.
2. **Measure acceptance, not just permission.** The decree's monitor already sees recommendation logs. Acceptance rates and price outcomes, run through an ablation audit like ours, test whether discretion is real.
3. **Don't rely on data limits or per-round bands.** Their effect is model-dependent at best, and zero at worst.

**Beyond antitrust.** Per-step approval by a deferential overseer is a general weakness of AI oversight. An agent that moves in small, individually plausible steps can drive an outcome that no single approval would allow.

## 6. Limitations

- **The hub's objective is a premise.** We instruct it; §4.5 is our only test without it.
- **Firm behaviour differs across models,** and that difference drives the discretion result. Our firm models stand in for human or AI deciders, whose deference we do not measure.
- **The remedy mappings are analogues:** rounds stand for months, a runtime lag for a training-data rule, and a market average for state-level reporting.
- **Replications are small** (n = 4–12), reasoning budgets differ by model (§3), and Gemini 3.8 Flash's baseline is unstable.
- **Horizons are finite.** Harm under remedies can rise after round 100 (one Gemini run took off at round 85). Our shares are upper bounds.
- **The mechanism tests are post hoc.** They were designed after the Gemini result and pre-registered before they ran.
- **There is one market model.**

## Appendix

- **A. Prompts:** `appendix-prompts.md`.
- **B. Per-arm tables:** `results/*/summary.md`.
- **C. Costs:** $[final] across five providers.
- **D. Provenance and independence:** SPRINT_LOG excerpt.
- **E. Limitations and dual use.**
