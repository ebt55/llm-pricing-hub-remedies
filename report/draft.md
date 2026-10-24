# Data Limits and Guardrails Don't Stop an LLM Pricing Hub; Only Firm Discretion Does

*Testing the RealPage remedies (stale data, data bans, parameterised auto-accept) on LLM pricing advisors*

*Draft v3, Sun 25 Oct ~03:30 IST. Confirmatory results were pre-registered before the main batch (freeze commit `5aa9f79`). Exploratory results were each logged in SPRINT_LOG before their runs. **[⧗]** marks numbers still running: Nemotron, GPT-5.4 mini, and the firm-discretion replications on Gemini Flash-Lite and Qwen. Target: ≤ 8 pages on the Apart template.*

## Abstract

Shared pricing software can align competitors' prices without any agreement between them. That is the theory of the US case against RealPage. The DOJ's 2026 Final Judgment bars runtime use of competitors' current non-public data, ages training data by at least 12 months, and coarsens reporting to state level. It allows auto-accept only within parameters each landlord sets, and bars impeding overrides or rewarding acceptance.

We test these remedies against a large-language-model pricing hub whose objective is aligned with the whole market, the incentive alleged against RealPage. The market is a repeated logit Bertrand duopoly that starts from competitive prices.

**Data limits are unreliable.** The hub drives prices to joint monopoly (profit gain Δ 0.99 vs 0.06 without an advisor; Claude Haiku 5.5, n = 20). Banning competitor data removes 85% of that harm for Qwen3.8 Flash and 69% for Haiku, but at most 10% for DeepSeek V4.1 Flash and two Gemini models, whose hubs reach monopoly with no rival data at all. A scripted rational hub with no data reaches Δ 0.82. Stale data removes 21% for Haiku, and a market average removes none.

**Guardrails fail.** Auto-accept within a ±3% per-round band retains all of the harm and only delays monopoly by four rounds. Even 50% acceptance retains 73%.

**Only firm discretion works.** When firms set each price themselves and see the recommendation, 95% of the harm disappears **[⧗ replications]**.

Realistic "avoid a race to the bottom" guidance also raises prices without any joint objective. Classic variance screens miss these markets.

*(≈ 245 words.)*

## 1. Introduction

**The premise.** We study a pricing advisor whose objective is aligned with the whole market rather than with its own client. This is the incentive alleged against RealPage: a vendor serving competing landlords, rewarded when rents rise across its clients. We do not claim LLM advisors adopt this objective on their own. We ask a policy question conditional on it: if such a hub exists, do the remedies regulators imposed stop it?

**The remedies.** The DOJ–RealPage Final Judgment (M.D.N.C., entered 19 May 2026):
- bans competitors' non-public data from runtime pricing;
- allows non-public training data only if it is at least 12 months old;
- forbids sub-state geographic models;
- permits an auto-accept feature only if it requires each user to set its parameters (§V.A.1);
- bars features that impede rejecting or overriding a recommendation (§V.A.5), and incentives to accept one (§V.C).

Landlord consent decrees bar software that requires acceptance. About $360M in class settlements were approved in October 2026.

**What we find.**
1. **Data limits are model-dependent.** They bind a hub that hesitates to act on its objective without data (Haiku, Qwen), but not one that reasons straight to the joint-monopoly price (DeepSeek, Gemini). A scripted rational hub shows that a joint objective makes higher prices optimal even with no rival data.
2. **Parameterised auto-accept only slows the hub.** So does probabilistic partial adherence.
3. **Firm discretion removes nearly all the harm.**
4. **Realistic revenue-management guidance raises prices too,** with no joint objective.
5. **Classic variance screens fail,** and reasoning monitors catch only stated intent.

We call the residual harm under data rules **data-compliant coordination**.

**Concurrent work.** zerocommcartel (2026) studies what firms are told about rivals' advisors in a one-shot Cournot game. We vary the advisor's data access and firms' adherence in a repeated Bertrand market.

## 2. Related work

*(Use `related-work.md`, ~450 words; trim to ~300 for the page limit.)*

## 3. Setup

**Market.**
- Logit Bertrand duopoly with Calvano et al.'s (2020) parameters (a = 2, μ = 0.25, c = 1): Nash price p_N = 1.4729, joint-monopoly price p_M = 1.9250.
- **Profit gain** Δ = (π − π_N)/(π_M − π_N), averaged over the last 20 of 100 rounds. Unit of analysis: the run.
- **Price index** (p̄ − p_N)/(p_M − p_N), used for cross-model comparisons because Δ is not monotone above p_M.
- Every run starts from 10 rounds of competitive history (Nash ± 0.05).

**Agents.**
- **Firms** use the P0 prompt of Fish et al. (2024) via llm-cartel, plus one sentence: the firm competes with one other firm whose prices and sales it doesn't observe.
- **Advisors** are called once per firm per round.
  - The *client* objective maximises the client's long-run profit.
  - The *market-aligned hub* objective maximises "the combined profit of all firms in your client's market". The prompt is otherwise identical, and never says the hub advises the rival.
- **Data regimes:**

| Regime | What the advisor sees about the rival |
|---|---|
| Current | Price and quantity through t−1 |
| Stale | The same, but all ≥ 10 rounds old |
| None | Nothing |
| Aggregate | Market average only (triopoly) |

**Adherence regimes:**
- **auto-accept:** the price is the recommendation;
- **firm discretion:** the firm sets the price after seeing the recommendation;
- **partial:** the recommendation is used with probability q;
- **guardrailed:** the recommendation is auto-applied but clipped to ±3% or ±1% of the firm's last price, a §V.A.1-style parameter.

**Controls.**
- Mechanical: a static monopoly price; best-response dynamics.
- A scripted rational joint-profit hub.
- A client-objective advisor.
- A one-sided-adoption arm.

**Models.** Claude Haiku 5.5 is the primary model, with adaptive thinking at low effort. Replications:
- DeepSeek V4.1 Flash;
- Gemini 3.5 Flash-Lite and 3.8 Flash;
- Qwen3.8 Flash;
- Nemotron 3.5 Lightning, open-weight;
- GPT-5.4 mini.

Reasoning is low effort, or a 1,024-token thinking budget where the provider didn't enforce effort. The model ID is logged on every call, and OpenRouter models are pinned to one provider each.

**Statistics.**
- Welch t intervals and tests, plus Mann-Whitney, with Holm correction within stage.
- Share of harm removed = (M2-a − X)/(M2-a − B0), with a bootstrap 95% CI.
- MDE reported for every contrast. N per primary arm was raised from 10 to 20 after the pilot.

## 4. Results

### 4.1 Controls *(confirmatory)*

- **Mechanical controls:** Δ = 1.00 and 0.01.
- **Baseline (B0):** 0.06 (n = 20).
- **Harness:** 41,000 main-batch calls with 0 parse failures and 0 refusals.
- **Behavioural positive control:** the hub beats B0 by at least 0.3 in 20/20 runs.
- **A client-objective advisor with current rival data is pro-competitive:** Δ −0.01 vs 0.06, p < .001. Pooled data alone doesn't cause harm.

### 4.2 The hub, and the data limits *(confirmatory, Haiku; Figure 1)*

The market-aligned hub reaches Δ 0.99 (SD 0.01). Against it:

| Data limit | Harm removed |
|---|---|
| Stale data | **21%** (14–29%) |
| No rival data | **69%** (55–82%) |

Holm-adjusted p < .001 for both. In the triopoly stretch arm (n = 10), a market-average feed removes nothing: Δ 0.98 vs 0.92 with per-firm data.

### 4.3 Data limits are model-dependent *(exploratory; Figure 4)*

| Model | Data ban removes | Stale data removes |
|---|---|---|
| Qwen3.8 Flash | 85% | 84% |
| Haiku | 69% | 21% |
| DeepSeek | 10% | 2% |
| Gemini Flash-Lite | 8% | — (overshoots p_M) |
| Gemini 3.8 Flash | ~0% | ~0% |
| Nemotron 3.5 Lightning | **[⧗]** | **[⧗]** |
| GPT-5.4 mini | **[⧗]** | **[⧗]** |

**Rational benchmark.** A scripted joint-profit hub reaches Δ 1.00 with current or stale data and 0.82 with none, because under a joint objective raising one's own price is optimal even without information.

**Haiku's no-data hub hesitates.** It stays at 0.29 even at high reasoning effort, and its notes say "deviating upward risks losing volume to a competitor". DeepSeek's and Gemini's hubs post the joint-monopoly price directly.

**Data limits bind only hubs that under-optimise their objective.**

### 4.4 Adherence: guardrails and partial adherence fail; firm discretion works *(Figure 3)*

| Adherence regime (hub, current data) | Δ | Harm retained |
|---|---|---|
| Auto-accept | 0.99 | 100% |
| Auto-accept within ±1% per round | 1.00 | 101% |
| Auto-accept within ±3% per round | 1.00 | 101% |
| Partial, q = 0.9 | 0.94 | 94% |
| Partial, q = 0.8 | 0.90 | 90% |
| Partial, q = 0.5 | 0.74 | 73% |
| **Firm discretion** | **0.11** | **5%** |

- **Guardrails only delay.** The median round at which prices first reach 95% of p_M is round 4 with no band, round 8 with ±3%, and round 18.5 with ±1% (Figure 3b).
- **Acceptance rates for calibration.** The DOJ complaint alleges that final prices were within 1% of RealPage's recommendation 40–50% of the time. Former employees and private plaintiffs put acceptance at 80–90%. Both sit where most of the harm remains.
- **Caveat.** Haiku firms are sticky: they follow a recommended move of more than $0.05 only 6% of the time. That stickiness helps firm discretion hold prices down, and helps partial adherence hold them up.
- Firm discretion on Gemini Flash-Lite and Qwen: **[⧗]**.

### 4.5 Without a coordination instruction: vendor guidance *(exploratory)*

The advisor maximises its client's profit and follows "avoid a race to the bottom" guidance, a paraphrase of the RealPage complaints.

| Arm | Δ | vs B0 |
|---|---|---|
| No rival data | 0.45 | +0.39 ± 0.23, p = .004 |
| Current rival data | 0.21 | +0.15, p = .11 |
| Firm discretion | 0.09 | n.s. |

So realistic guidance alone raises prices, a data ban may *increase* the effect, and firm discretion removes it.

### 4.6 Robustness *(exploratory)*

- **Demand noise** (log-normal, sd 0.1): stale data removes 24% and the ban 52%.
- **No price-ceiling cue:** stale data removes 34% and the ban 77%.
- **High reasoning effort:** the ban leaves Δ at 0.29.
- **200 rounds:** the ban leaves 0.44 and stale data 0.87, so the 100-round figures are upper bounds.
- **One-sided adoption:** the hub prices its own client at 1.88 and the plain rival best-responds at 1.64. The client loses (gain −0.09) and the rival gains (+1.46). Harm needs both firms on the hub.

### 4.7 Detection *(exploratory; 200 runs)*

| Detector | AUROC | Note |
|---|---|---|
| Price-level screen | 0.90 | 72% caught at a 5% false-alarm rate; misses hubs a remedy holds back |
| Variance screen (Abrantes-Metz et al. 2006) | **0.36** | Inverted: points the wrong way |
| Reasoning monitor | 0.99 | Even from one-line stated reasons |

The monitor's score is the easy case, because the hub states its objective. It also flags honest rival-watching advisors, which score 55–66 against 10–18 for the baselines.

## 5. Discussion

**Data-compliant coordination.** The settlement's data limits are written for software whose behaviour depends on the data it sees. An LLM hub's behaviour depends mainly on its objective: data mostly *confirms* that the rival has followed. Whether a data limit binds then depends on how hard the model pursues that objective, which varies across models and will likely rise with capability.

**Adherence.** Parameterised auto-accept and partial acceptance leave the hub in control of enough prices to sustain the outcome. Only firms that set every price themselves broke it in our tests.

**Implications for remedies on LLM pricing software:**
1. Regulate and audit the advisor's **objective**.
2. Require **firm discretion**, not just guardrails.
3. Don't rely on data limits alone.

**Detection.** Outcome screens and intent monitors complement each other. Variance screens built for human cartels point the wrong way here.

## 6. Limitations

See `appendix-limitations-dual-use.md`. In brief:
- the hub's objective is a premise;
- firms are sticky;
- remedy mappings are analogues (rounds for months; a runtime lag for a training-data rule; a market average for state-level reporting);
- most robustness checks are on Haiku;
- replications are small (n = 3–8);
- there is one market model.

## Appendix

- **A. Prompts:** `appendix-prompts.md`.
- **B. Per-arm tables:** `results/*/summary.md`.
- **C. Costs:** $[final] across five providers.
- **D. Provenance and independence:** SPRINT_LOG excerpt.
- **E. Limitations and dual use.**
