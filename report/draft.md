# S'all Good, Man? Do Antitrust Remedies Stop an AI Pricing Cartel?

*Testing the RealPage settlement on LLM pricing advisors*

*Draft v1, Sun 25 Oct ~01:15 IST. Haiku numbers are final (main batch, frozen design). Items marked [pending] wait on the DeepSeek extension and the OpenAI replication. Paste into the official Apart template at the end: ≤ 8 pages, abstract 150–250 words.*

## Abstract (draft; ~230 words)

Shared pricing software can coordinate competitors' prices without any agreement between them. That is the theory behind the US case against RealPage, whose settlement:
- bans the use of competitors' current non-public data at runtime;
- allows such data only once it is old or aggregated;
- follows complaints that targeted auto-accepting the software's recommendations.

We ask whether these remedies still work when the advisor is a large language model. In a repeated logit Bertrand duopoly, LLM firms set prices, and each firm's LLM advisor recommends a price. We vary the advisor's competitor data and whether firms must follow it. Every run starts from competitive pre-adoption history.

An advisor that maximises only its own client's profit is pro-competitive (profit gain Δ = −0.01 vs 0.06 with no advisor). A market-aligned hub, the RealPage concern, drives prices to joint monopoly (Δ = 0.99, n = 20, Claude Haiku 5.5). Against this hub:
- stale competitor data removes only **21%** of the harm (95% CI 14–29%);
- a full ban on competitor data removes **69%** (55–82%), but the ban delays rather than prevents: at 200 rounds, some hubs reach cartel prices from their own sales data;
- market-wide aggregated data removes **none** (three-firm market);
- making the advice optional removes **95%** (88–102%).

A second model family (DeepSeek V4.1 Flash) is even less constrained: its hub reaches cartel prices without any competitor data [n pending].

We call the residual harm **compliant collusion**: data remedies leave it largely intact because the hub's objective, not its data, drives coordination. Classic variance screens miss these cartels. Reasoning monitors catch the hub's intent, but also flag honest advisors that merely watch rivals.

## 1. Introduction

**Hook.** Saul Goodman's trademark is staying technically legal while doing shady things. Our question has the same shape: can an AI pricing hub that follows the RealPage remedies to the letter still coordinate prices? We find that largely it can. We call this *compliant collusion*.

**The case.**
- RealPage sold revenue-management software that pooled landlords' non-public rent and occupancy data.
- The DOJ and states alleged this let competitors coordinate rents.
- The settlement restricts runtime use of competitors' current non-public data, allows only data at least 12 months old for model training, and bars reporting narrower than state level.
- Complaints also targeted auto-accept.
- About $360M in MDL settlements were approved on 16 Oct 2026.

**The gap.** These remedies were written for rule-based software. LLM advisors reason from whatever they are given, and may infer what they are denied.

**Contributions.**
1. **A testbed.** It maps each remedy onto a controlled arm, against an explicit harm case, with mechanical and behavioural positive controls.
2. **Remedy effects with uncertainty**, reported as the share of harm removed, across horizons and model families.
3. **A mechanism.** Hub coordination is driven by the objective. Data mostly *confirms* that the rival has followed.
4. **A detection test.** Classic cartel screens and reasoning monitors, scored against ground-truth labels.

**Concurrent work.** zerocommcartel (2026) studies what firms are told about rivals' advisors in a one-shot Cournot game. We instead vary the advisor's data access and firms' adherence (the decree's remedies) in a repeated Bertrand market.

## 2. Related work

- **Algorithmic collusion:** Calvano et al. (2020).
- **LLM pricing agents:** Fish et al. (2024); Riemer et al. (2026, llm-cartel); Keppo et al. (2026).
- **Shared advisors and monoculture:** Cao & Hu (2026); Hillenbrand.
- **Remedies:** the RealPage complaint and decree; the hotel cases (Gibson; Cornish-Adebiyi).
- **Audits and deviations:** Tran & Yu (2026).
- **Focal caps:** Dhanda (2026).
- **Cartel screens:** Abrantes-Metz et al. (2006); Harrington.
- **CoT monitoring:** Baker et al. (2025); Korbak et al. (2025).
- **Concurrent:** zerocommcartel (verify numbers on the day).

## 3. Setup

**Market.**
- Logit Bertrand duopoly with Calvano parameters (a = 2, μ = 0.25, c = 1): Nash price 1.4729, joint-monopoly price 1.9250.
- Profit gain Δ = (π − π_N) / (π_M − π_N), averaged over the last 20 of 100 rounds.
- Each run starts with **10 rounds of competitive pre-adoption history** (Nash ± 0.05).

**Firms.**
- The P0 pricing prompt (Fish et al. via llm-cartel), plus one neutral sentence: the firm competes with one other firm whose prices and sales it doesn't observe.
- Firms see only their own records, plus the software's recommendation in advisor arms.

**Advisors.**
- One call per firm per round.
- The *client* objective maximises the client's long-run profit.
- The *market-aligned hub* objective maximises "the combined profit of all firms in your client's market". This is otherwise the same prompt. The hub is never told that it advises the rival.

**Arms (Table 1).**

| Arm | Setting | Maps to |
|---|---|---|
| B0 | No advisor | Baseline |
| R2-a | Client advisor, current competitor data (through t−1), auto-accept | Advisor without a market objective |
| M2-a | Hub, current data, auto-accept | **The alleged harm** |
| M1-a | Hub, competitor data ≥ 10 rounds old | Stale-data remedy |
| M0-a | Hub, no competitor data | Runtime data ban |
| M2-d | Hub, current data; the firm decides | No auto-accept |
| M3-3a vs M2-3a | Triopoly hub, market average vs per-firm data | Aggregation |
| S-mono-a, D-BR-a | Static monopoly price; best-response rule, both auto-accepted | Mechanical controls |
| S-nash, S-mono, R0-d, B0-cold | Static numbers, discretionary; client advisor without data; 1-round warm-up | Further controls |

**Models.**
- Claude Haiku 5.5: adaptive thinking at effort low; the API allows no sampling control.
- Replications on DeepSeek V4.1 Flash (thinking, low effort) and GPT-5.4 mini (reasoning low).
- The model ID the API returns is logged on every call.

**Pre-registration.** The gates, the model-selection rule, the hypotheses and the frozen configs are committed with timestamps before each batch (design freeze commit `5aa9f79`). N was set from pilot variance: n = 20 for primary arms, 5 for controls.

## 4. Results

### 4.1 Controls and harness

- **Mechanical controls:** S-mono-a Δ = 1.00 and D-BR-a Δ = 0.01.
- **Baseline:** B0 Δ = 0.06 (n = 20).
- **Behavioural positive control:** M2-a exceeds B0 by ≥ 0.3 in 20/20 runs.
- **Harness:** 41,000 Haiku calls with 0 parse failures and 0 refusals; $21.7 for the main batch.

### 4.2 Advisors without a market objective are pro-competitive

R2-a: Δ = −0.01 vs B0's 0.06 (difference −0.07, p < .001). A client advisor that sees the rival's current prices best-responds, so pooled data alone doesn't produce harm.

### 4.3 The market-aligned hub, and the remedies (Figure 1, Figure 2)

The hub drives prices to joint monopoly: M2-a Δ = 0.99 (SD 0.01).

**Share of harm removed, (M2-a − X)/(M2-a − B0), with bootstrap 95% CIs:**

| Remedy | Arm | Δ | Harm removed |
|---|---|---|---|
| Stale data | M1-a | 0.79 | **21%** (14–29%) |
| Data ban | M0-a | 0.35, bimodal | **69%** (55–82%) |
| No auto-accept | M2-d | 0.11 | **95%** (88–102%) |
| Aggregation (triopoly, n = 10) | M3-3a | 0.98 vs per-firm 0.92 | **none** |

All stage-2 contrasts have Holm-adjusted p < .001.

### 4.4 Mechanism: data confirms, the objective drives

From the hub's reasoning:
- With competitor data, current or stale, the hub raises prices early, reasoning from its estimate of the joint-monopoly price. It then holds them once the data confirms the rival is high.
- Data that is ten rounds old confirms a stable rival just as well as current data. That is why the stale-data rule fails once prices have settled.
- Without data, the hub hesitates ("deviating upward risks losing volume to a competitor"). Over longer horizons some hubs infer the rival's behaviour from their own quantities and climb.
  - **Horizon check** (200 rounds, n = 5): M0-a reaches 0.44 (bimodal: 0.97 and 0.91 in two runs) and M1-a reaches 0.87.

### 4.5 Do firms follow advice?

- Firms follow recommendations close to their own recent prices: follow rate 0.84 for R0-d and 0.70 for S-nash.
- They reject high ones: 0.02 for S-mono and 0.37 for M2-d.
- So a static cartel-level number has no effect when firms are free to choose (S-mono vs S-nash: +0.02, n.s.). The harm runs through auto-accept.

### 4.6 Robustness

- **Willingness-to-pay cue removed** (n = 10). The hub reads the prompt's "no customer would pay more than $2.89" as a demand choke price. Without it:
  - M2-a stays at 0.99;
  - stale data removes 34% (20–50%);
  - the ban removes 77% (60–92%).
  - The cue helps the stale-data hub coordinate a little, but doesn't cause the effect.
- **Second model family: DeepSeek V4.1 Flash** [n = 3, extension to 8 pending].
  - B0 0.19, M2-a 1.00, M1-a 0.96, M0-a 0.85.
  - Stale data removes 5%, the ban 18%.
  - The no-data hub computes the joint-monopoly price and posts it.
- **Third model family: GPT-5.4 mini** [pending].

### 4.7 Can screens or monitors detect it? (exploratory)

200 LLM runs, scored against ground-truth labels:

| Detector | AUROC | TPR at 5% FPR | Notes |
|---|---|---|---|
| Price screen | 0.90 | 0.72 | Catches outcomes; misses hubs that a remedy held back |
| Variance screen (Abrantes-Metz et al. 2006) | **0.36** | — | **Fails** |
| Reasoning monitor (Haiku judge) | 0.99 | 0.96 | Same result from the one-line stated reasons alone |

Two caveats about the reasoning monitor:
- The hub *states* its joint-profit objective, so this is the easy case.
- The monitor flags honest client advisors that watch the rival, which score 55–66 out of 100 against about 10–18 for the baselines.

## 5. Discussion

**Compliant collusion.**
- When the advisor's objective is market-aligned, the data remedies leave most of the harm in place:
  - stale and aggregated data barely help;
  - a data ban helps for one model and delays coordination for another.
- The remedy that works across our settings is the one that breaks the transmission: firms that are free not to follow high recommendations.

**Policy implication.** Remedies for LLM pricing software should:
- target the **objective** the software optimises, with auditable alignment to the individual client;
- target **adherence**, with no auto-accept and with logged overrides;
- not rely on **data access** alone.

**Detection.**
- Outcome screens catch only cartels that succeed.
- Text monitors catch intent, but only when it is stated, and they confuse watching the rival with coordinating.

## 6. Limitations

See `appendix-limitations-dual-use.md`. Additions from the results:
- **The hub's objective is a modelling assumption.** We test remedies conditional on a market-aligned hub.
- **Our firms are cautious.** That likely overstates the effect of removing auto-accept, since real landlords reportedly followed RealPage most of the time.
- **The stale lag is in rounds, not months.**
- **Aggregation is market-level** in a three-firm market.
- **DeepSeek and OpenAI replications are small.**

## Appendix

- Prompts (verbatim).
- Per-arm tables (`results/*/summary.md`).
- Costs (about $45 in total).
- SPRINT_LOG excerpt: provenance and independence.
- Limitations and dual use.
