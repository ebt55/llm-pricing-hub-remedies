# Better Call SAUL? Shared Advisors Under Legal Remedies

*Subtitle: Do the RealPage antitrust remedies stop a shared LLM pricing advisor from running a hub-and-spoke cartel?*

*Draft. Paste into the official Apart template at the end. ≤ 8 pages; abstract 150–250 words.*

## Abstract (fill last; 150–250 words, with the headline number)

[Problem: shared algorithmic pricing advisors; the RealPage settlement restricts competitor-data access, and the complaints targeted auto-accept.]

[Method: a repeated logit Bertrand duopoly with LLM firms and per-firm LLM advisors. We vary what competitor data the advisor sees (none / stale / current / aggregated) and whether firms must follow advice, with static, rule-based and instructed-cartel controls. Models: Claude Haiku 5.5, plus DeepSeek V4.1 Flash for robustness.]

[Results: Δ for R2 vs R0; stale vs current; auto vs discretionary; follow rate for a cartel-level number; the positive control.]

[Implication for remedy design.]

## 1. Introduction

- Algorithmic pricing vendors and the RealPage case: the ~$360M MDL settlements, approved 16 Oct 2026, and the DOJ decree terms.
- The open question: the decree's remedies were written for rule-based software that pools competitor data. Do they bind when the advisor is an LLM that reasons from whatever data it gets?
- Contributions:
  1. A testbed that maps the decree's remedies onto controlled arms.
  2. Results for the data and adherence remedies, with a positive control and the minimum detectable effect (MDE) for every contrast.
  3. A separation of anchoring from coordination, using static and rule-based recommenders.
- **One sentence that separates this from concurrent work:** zerocommcartel (2026) studies what firms are told about rivals' advisors in a one-shot Cournot game. We vary the advisor's data access and firms' adherence in a repeated Bertrand market.

## 2. Related work

- Algorithmic collusion: Calvano et al. 2020.
- LLM pricing agents: Fish et al. 2024; Riemer et al. 2026 (llm-cartel); Keppo 2026.
- Hub-and-spoke and shared advisors: Cao & Hu 2026 (AI monoculture); Hillenbrand.
- Remedies and enforcement: the RealPage complaint and decree; hotel cases (Gibson, Cornish-Adebiyi).
- Audits and deviations: Tran & Yu 2026.
- Caps as focal points: Dhanda 2026.
- Concurrent sprint work: zerocommcartel (cite precisely; verify numbers on the day).

## 3. Setup

- **Market.** Calvano parameters; Nash and monopoly benchmarks; profit gain Δ.
- **Agents.**
  - The firm uses the P0 prompt from Fish et al. via llm-cartel.
  - The advisor's prompt is identical across arms.
  - Information design: competitor data is non-public.
- **Arms.** A table with each arm's mapping to a decree clause.
- **Models and settings.** Low-effort reasoning; no sampling control; model IDs are logged per call.
- **Pre-registration.** Gates, the model-selection rule, the frozen config (commit hash), N from pilot variance, and the contrasts H1–H5.

## 4. Results

- **4.1 The positive control and harness checks.** PC Δ; parse and refusal rates.
- **4.2 Do firms follow advice?** S-mono vs S-nash; follow rates; auto vs discretionary.
- **4.3 The data remedies.** The R0 / R1 / R2 ladder (Figure 1: Δ by arm with CIs).
- **4.4 Does the LLM add anything beyond the data?** R2 vs D-BR.
- **4.5 Robustness.** The second model family; [triopoly aggregation].
- **4.6 What advisors say.** Reasoning summaries and reason lines: how often they mention the competitor's price, matching, or price wars. Descriptive only.

## 5. Discussion

- What this implies for remedy design: which levers bind for LLM advisors and which don't.
- [If H1 is null] Data pooling isn't the binding channel at this capability level; adherence is. [If H1 is positive] Data restrictions matter, and the stale-data rule [does / doesn't] restore baseline prices.

## 6. Limitations

See `appendix-limitations-dual-use.md`.

## Appendix

- Prompts (verbatim).
- Per-arm tables.
- Costs.
- SPRINT_LOG excerpt: provenance and independence.
- Limitations and dual use.
