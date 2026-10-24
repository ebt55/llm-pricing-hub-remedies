# Stale Data Isn't Enough: Only Ending Auto-Accept Stops an LLM Pricing Hub

*Testing the RealPage settlement's remedies on LLM pricing advisors*

*Draft v2, Sun 25 Oct ~02:30 IST, rewritten after the methods red-team and the judge simulation. Section markers say which results are **confirmatory** (pre-registered before the main batch, freeze commit `5aa9f79`) and which are **exploratory** (added later, each logged in SPRINT_LOG before its results). The model-ladder and OpenAI numbers are filled in when those runs finish. Target: ≤ 8 pages on the Apart template.*

## Abstract

Shared pricing software can align competitors' prices without any agreement between them. That is the theory of the US case against RealPage. Its settlement bars the software from using competitors' current non-public data at runtime, limits model training to data at least a year old, and restricts reporting to coarse aggregates; the complaints also targeted auto-accepting the software's recommendations. We test whether these remedies still work when the advisor is a large language model whose objective is aligned with the whole market, which is the incentive alleged against RealPage.

In a repeated logit Bertrand duopoly that starts from competitive prices, a market-aligned LLM hub (Claude Haiku 5.5) drives prices to joint monopoly (profit gain Δ = 0.99, n = 20). Giving it only competitor data that is ten rounds old removes just 21% of this harm, and a market-wide average removes none. Removing competitor data entirely removes 69% for Haiku but only 10% for DeepSeek V4.1 Flash. A scripted rational hub with no data still reaches Δ = 0.82, so data bans bind only hubs that under-optimise their own objective. Ending auto-accept removes 95% of the harm. Partial adherence does not: at 50%, 80% and 90% acceptance, 73%, 90% and 94% of the harm remains.

Without any instruction to coordinate, realistic "avoid a race to the bottom" guidance also raises prices (Δ 0.45 vs 0.06), and ending auto-accept again removes the rise. The results hold under demand noise, without the prompt's price ceiling, and at higher reasoning effort. We conclude that remedies for LLM pricing software should target its objective and firms' adherence, not only its data.

*(~250 words. Add the ladder sentence once Gemini lands; trim to fit.)*

## 1. Introduction

**The premise, stated plainly.** We study a pricing advisor whose objective is aligned with the whole market rather than with its own client. This is the incentive alleged against RealPage: one vendor serving competing landlords, rewarded when rents rise across its clients. We do not claim that LLM advisors adopt this objective on their own. We ask a policy question conditional on it: if such a hub exists, do the remedies regulators actually imposed stop it?

**The remedies.** In the RealPage settlement, the software may not use competitors' current non-public data at runtime, models may be trained only on data at least 12 months old, and reporting must not be narrower than state level. The complaints also targeted auto-accept, which applies recommendations without review. About $360M in MDL settlements were approved in October 2026 [cite].

**Contributions.**
1. **A remedy testbed.** It maps each remedy onto a controlled arm, against an explicit harm case, with mechanical and behavioural positive controls.
2. **A finding about data remedies.** Data remedies leave most of the hub's harm in place. A scripted rational benchmark shows why: a joint-profit objective makes raising prices optimal even without rival data. Only hubs that under-optimise their objective are constrained, and that varies by model.
3. **A finding about adherence.** Only *ending* auto-accept removes the harm. Even the acceptance rate the DOJ alleged leaves most of it.
4. **A propensity probe.** Realistic revenue-management guidance, with no coordination instruction, also raises prices.
5. **A detection test.** Classic cartel screens and a reasoning monitor, scored against ground truth.

**Concurrent work.** zerocommcartel (2026) studies what firms are told about rivals' advisors in a one-shot Cournot game. We vary the advisor's data access and firms' adherence (the settlement's remedies) in a repeated Bertrand market.

## 2. Related work

*(Write as prose; ~½ page.)*

- **Algorithmic collusion:** Calvano et al. (2020); Assad et al. (2024) on German gasoline.
- **LLM pricing agents:** Fish et al. (2024); Riemer et al. (2026, whose llm-cartel code we build on); Keppo et al. (2026).
- **Shared algorithms and monoculture:** Cao & Hu (2026); hub-and-spoke doctrine.
- **Remedies and cases:** the RealPage complaint and settlement; the hotel cases (Gibson; Cornish-Adebiyi).
- **Deviation audits:** Tran & Yu (2026).
- **Focal caps:** Dhanda (2026).
- **Cartel screens:** Abrantes-Metz et al. (2006); Harrington.
- **Reasoning monitors:** Baker et al. (2025); Korbak et al. (2025).
- **Concurrent:** zerocommcartel.

## 3. Setup

**Market.**
- Logit Bertrand duopoly with Calvano et al.'s parameters (a = 2, μ = 0.25, c = 1): Nash price 1.4729, joint-monopoly price 1.9250.
- **Profit gain** Δ = (π − π_N)/(π_M − π_N), averaged over the last 20 of 100 rounds. The **unit of analysis is the run.**
- Every run starts with 10 rounds of competitive pre-adoption history (Nash ± 0.05).
- **Why that start:** in diagnostics, firms given no history and not told a rival exists priced at the midpoint of cost and the stated price ceiling, which happens to be ≈ p_M.

**Firms.**
- llm-cartel's P0 prompt, plus one neutral sentence: the firm competes with one other firm whose prices and sales it does not observe.
- Firms see only their own price, quantity and profit, and, in advisor arms, the software's recommendation for this round and its past recommendations.

**Advisors.**
- One call per firm per round.
- The *client* objective maximises the client's long-run profit.
- The *market-aligned hub* objective maximises "the combined profit of all firms in your client's market". The prompt is otherwise identical, and never says the hub advises the rival.

**Arms (Table 1).**

| Arm | Advisor and data | Adherence | Maps to |
|---|---|---|---|
| B0 | none | — | baseline |
| R2-a | client objective; rival's price and quantity through t−1 | auto | advisor without a market objective |
| **M2-a** | **hub; rival data through t−1** | **auto** | **the alleged harm** |
| M1-a | hub; rival data ≥ 10 rounds old | auto | the 12-month rule (a runtime analogue of a *training*-data rule) |
| M0-a | hub; no rival data | auto | the runtime data ban |
| M2-d | hub; rival data through t−1 | the firm decides | ending auto-accept |
| M2-q50/80/90 | hub; rival data through t−1 | auto with probability q | partial adherence *(exploratory)* |
| M3-3a vs M2-3a | triopoly hub; market average vs per-firm data | auto | aggregation *(stretch)* |
| V2-a, V0-a, V2-d | vendor guidance; current / no rival data | auto / decides | propensity probe *(exploratory)* |
| J2-a, J1-a, J0-a | scripted rational joint-profit hub | auto | benchmark *(exploratory, $0)* |
| S-mono-a, D-BR-a | static monopoly price; best-response rule | auto | mechanical controls |

**Models.**
- Claude Haiku 5.5, with adaptive thinking at low effort; the API allows no sampling control.
- Replications on DeepSeek V4.1 Flash, GPT-5.4 mini, and Gemini 3.5 Flash-Lite, 3.8 Flash and 4 Argon.
- The model ID the API returns is logged on every call.

**Statistics.**
- Welch t intervals and tests, plus Mann-Whitney, with Holm correction within stage.
- Harm removed = (M2-a − X)/(M2-a − B0), with a bootstrap 95% CI.
- The minimum detectable effect is reported for every contrast.
- N was raised after the pilot, from the planned 10 to 20 for primary arms.

## 4. Results

### 4.1 Controls *(confirmatory)*

- **Mechanical controls:** S-mono-a gives Δ = 1.00 and D-BR-a gives 0.01.
- **Baseline:** B0 gives 0.06 (n = 20).
- **Harness:** 41,000 calls with 0 parse failures and 0 refusals.
- **Behavioural positive control:** M2-a exceeds B0 by at least 0.3 in 20/20 runs.

### 4.2 Advisors without a market objective are pro-competitive *(confirmatory)*

The client advisor with the rival's current data (R2-a) gives Δ = −0.01, against 0.06 for B0 (p < .001). Pooled data alone does not cause harm; the advisor best-responds.

### 4.3 The hub, and the data remedies *(confirmatory; Figure 1)*

The market-aligned hub reaches joint monopoly: M2-a Δ = 0.99 (SD 0.01). Against it:

| Remedy | Δ | Harm removed |
|---|---|---|
| Stale data (M1-a) | 0.79 | **21%** (CI 14–29%) |
| No competitor data (M0-a) | 0.35, bimodal | **69%** (CI 55–82%) |
| Ending auto-accept (M2-d) | 0.11 | **95%** (CI 88–102%) |

- Contrasts H2–H4 have Holm-adjusted p < .001.
- **Aggregation (stretch, triopoly, n = 10):** the hub given only the market average (M3-3a, Δ 0.98) is no less harmful than with per-firm data (M2-3a, 0.92). With two symmetric rivals, the average hides little, so this is a weak test of state-level aggregation.

### 4.4 Why the data remedies fail *(exploratory)*

**A rational benchmark.** A scripted hub that maximises joint profit, given the rival price it can see, gives:

| Scripted hub | Δ |
|---|---|
| Current data | 1.00 |
| Stale data | 1.00 |
| No data (assumes the rival stays at Nash) | 0.82 |

So under a joint objective, raising the price is optimal even without rival information, and data restrictions only delay a rational hub.

**The models differ.**
- Haiku's no-data hub hesitates ("deviating upward risks losing volume to a competitor") and reaches 0.35.
- It stays there at high reasoning effort (0.29, n = 10), so the restraint is a trait of the model, not an effort artefact.
- DeepSeek's no-data hub reaches **0.91** (n = 8; it removes 10% of the harm, CI 1–21%), close to the rational benchmark.
- Stale data removes 2% for DeepSeek. *[Model ladder: Gemini Flash-Lite, 3.8 Flash, 4 Argon, and GPT-5.4 mini. Figure 4.]*

**Mechanism, from the reasoning traces.**
- With data, the hub raises prices from its estimate of the monopoly price, then holds once data confirms the rival is high.
- Data that is ten rounds old confirms a stable rival as well as current data does.
- Over 200 rounds, 2 of 5 no-data Haiku hubs inferred the rival's behaviour from their own quantities and climbed.

### 4.5 Adherence: only *ending* auto-accept works *(dose-response exploratory; Figure 3)*

| Probability the firm's price is the recommendation | Harm retained |
|---|---|
| 0 | 5% |
| 0.5 | 73% |
| 0.8 | 90% |
| 0.9 | 94% |
| 1 | 100% |

- **For calibration:** the DOJ complaint alleges that final prices were within 1% of RealPage's recommendation for 40–50% of new leases. Former employees and private plaintiffs put acceptance at 80–90%.
- **Caveat: firm stickiness.**
  - When the recommendation would move the price by more than $0.05, Haiku firms with optional advice follow it 6% of the time.
  - So "ending auto-accept" works partly because the firms stay where they are.
  - Once some rounds are set by the hub, the same stickiness holds the high price.
  - *[DeepSeek M2-d replication.]*

### 4.6 Without any coordination instruction: vendor guidance *(exploratory)*

The advisor maximises its client's profit and follows "avoid a race to the bottom" guidance: don't chase volume with price cuts, don't match discounts. This paraphrases the RealPage complaints.

| Arm | Δ | vs B0 |
|---|---|---|
| V0-a (no rival data) | **0.45** | +0.39 ± 0.23, p = .004 |
| V2-a (current rival data) | 0.21 | +0.15, p = .11 |
| V2-d (optional advice) | 0.09 | n.s. |

- Realistic guidance raises prices without any joint objective.
- With no rival data the guidance ratchets prices up unchecked, so here **a data ban may backfire** (V0-a − V2-a = +0.24, p = .09).
- Ending auto-accept again removes the rise.

### 4.7 Robustness *(exploratory)*

**Demand noise** (log-normal shocks, sd 0.1, so own quantities no longer reveal the rival's price): the ordering survives.

| Arm | Δ | Harm removed |
|---|---|---|
| B0 | −0.06 | — |
| M2-a | 0.96 | — |
| M1-a | 0.71 | 24% |
| M0-a | 0.43 | 52% |

**No price-ceiling cue** ("No customer would pay more than $2.89" removed): M2-a 0.99; stale data removes 34% and the ban 77%. The cue modestly helps hubs coordinate, but doesn't create the effect.

**Horizon (200 rounds):** M1-a reaches 0.87 and M0-a reaches 0.44, so the 100-round "harm removed" figures are upper bounds.

**Asymmetric adoption** (only one firm uses the hub):
- The hub prices its client at 1.88; the plain rival best-responds at 1.64.
- The hub's client loses (gain −0.09) and the rival gains (+1.46).
- So the harm needs both firms on the hub, which is the hub-and-spoke structure.

### 4.8 Detection *(exploratory; 200 LLM runs)*

**Screens catch outcomes.**
- The price-level screen: AUROC 0.90; it detects 72% of hubs at a 5% false-positive rate. It misses hubs that a remedy held back.
- The variance screen (Abrantes-Metz et al. 2006) is **inverted**: AUROC 0.36.

**Monitors catch stated intent.**
- A reasoning monitor (Haiku judge) reaches AUROC 0.99, even from the one-line stated reasons alone. It flags hubs whose prices stayed competitive: M2-d scores 91 while its Δ is 0.11.
- This is the easy case: the hub's objective is written in its notes.
- The monitor also flags honest client advisors that watch the rival: they score 55–66, against 10–18 for baselines.

## 5. Discussion

**Data-compliant coordination.** A hub that obeys every data restriction can still move prices most of the way to joint monopoly, because its objective drives the prices and data mostly confirms that the rival has followed.

**Two implications for remedies on LLM pricing software:**
1. **Constrain the objective.** Require auditable alignment to the individual client. Data remedies bind only hubs that under-optimise, and stronger models undo them.
2. **End auto-accept fully.** Partial overrides leave most of the harm, including at the acceptance rate the DOJ alleged.

**Detection.** Outcome screens and intent monitors are complements. Neither handles a hub whose objective is implicit.

## 6. Limitations

See `appendix-limitations-dual-use.md`. Key items:
- **The market-aligned objective is an assumption,** stated as the premise.
- **Our firms are cautious and sticky.**
- **Remedy mappings are analogues:** rounds for months, a runtime lag for a training-data rule, a market average for state-level reporting.
- **Most robustness checks are on Haiku**, and the replications are small.
- **Results are for one market model** and 100–200 rounds.

## Appendix

- Prompts (verbatim).
- Per-arm tables.
- Costs (to tally).
- SPRINT_LOG excerpt: provenance, independence, and what was pre-registered when.
- Limitations and dual use.
