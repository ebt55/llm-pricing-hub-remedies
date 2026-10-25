# Appendix F: Supplementary tables and figures

## Table F1. Measured reasoning budget per model

Median output tokens per call, with thinking included (`tools/token_table.py`). Gemini's OpenAI-compatible endpoint omits thinking tokens from `completion_tokens`, so for Gemini we log total minus prompt tokens.

| Model | Setting | Median output tokens, firm / hub |
|---|---|---|
| Claude Haiku 5.5 (primary) | Adaptive thinking, low effort | 557 / 778 |
| Claude Haiku 5.5 (robustness) | High effort | — / 1,319 |
| DeepSeek V4.1 Flash | Thinking, low effort | 692 / 928 |
| Qwen3.8 Flash | 1,024-token reasoning budget | 613 / 872 |
| Nemotron 3.5 Lightning (open weights) | 1,024-token budget (not enforced) | 2,916 / 6,376 |
| GPT-5.4 mini | Low effort | 196 / 169 |
| Gemini 3.8 Flash | Low effort | 142 / 122 |
| Gemini 3.5 Flash-Lite | Low effort | **35 / 39 (no thinking)** |
| Gemini 3.5 Flash-Lite | High effort (thinking-on batch) | 408 / 816 |

## Table F2. Acceptance of the LLM hub's recommended increases, under firm discretion

The share of recommended increases (recommendation minus the firm's last price) that the firm matched exactly, pooled over all finished discretionary runs with the market-aligned hub (`tools/ratchet_curve.py`).

| Firm model | +1–2 cents | +3–5 cents | +6–9 cents | ≥ +10 cents |
|---|---|---|---|---|
| Claude Haiku 5.5 | 16% (n = 529) | 8% (981) | 4% (599) | 4% (1,383) |
| Qwen3.8 Flash | 40% (15) | 23% (93) | 50% (12) | 18% (114) |
| Gemini 3.5 Flash-Lite, no thinking | 67% (531) | 46% (304) | 18% (45) | 8% (147) |
| Gemini 3.5 Flash-Lite, thinking on | 52% (235) | 71% (157) | 14% (21) | 17% (6) |

Cell sizes differ by model because the hubs recommend different steps. Haiku's hub, when ignored, keeps recommending large increases, while Gemini's mostly recommends holding.

## Table F3. Robustness (Claude Haiku 5.5)

| Δ by check (n) | No advisor | Hub, current data | Hub, stale data | Hub, no rival data |
|---|---|---|---|---|
| Main batch (20) | 0.06 | 0.99 | 0.79 | 0.35 |
| Demand noise, log-normal sd 0.1 (10) | −0.06 | 0.96 | 0.71 | 0.43 |
| No price-ceiling cue in the prompt (10) | 0.07 | 0.99 | 0.68 | 0.29 |
| Higher reasoning effort (10) | — | — | 0.91 | 0.29 |
| 200 rounds (5) | 0.05 | — | 0.87 | 0.44 |
| 200 rounds, firm discretion (5) | — | 0.03 | — | — |
| 200 rounds, +1 cent ratchet with discretion (5) | — | 0.03 (scripted) | — | — |

## Table F4. Detection (200 runs; mechanical arms excluded)

| Detector | AUROC | Note |
|---|---|---|
| Price-level screen | 0.90 | 72% caught at a 5% false-alarm rate; misses hubs that a remedy holds back |
| Variance screen (Abrantes-Metz et al., 2006) | **0.36** | Inverted: it points the wrong way |
| Reasoning monitor (Claude Haiku 5.5 judge) | 0.99 | Reads stated reasons |

**The monitor case is the easy one.** The hub states its objective in its notes. The monitor also flags honest advisors that watch rivals (scores 55–66, against 10–18 for baselines).

## Table F5. Two candidate fixes for firm discretion (Gemini 3.5 Flash-Lite, no thinking; n = 6; exploratory)

| Remedy | Δ | Harm removed (95% CI) | Pre-registered prediction |
|---|---|---|---|
| Firm discretion alone (n = 12) | 0.41 | 57% (27–84) | — |
| Data ban + discretion (the decree's remedies stacked) | 0.38 | 60% (16–98) | < 80% removed: held |
| Discretion + drift disclosure ("+7.5% compared with your price 10 rounds ago") | 0.57 | 38% (−4 to 76) | more than discretion alone: failed |

Neither fix helps. The drift sentence (Appendix A) did not make Gemini firms refuse nudges.

## Figure A1. Partial adherence and guardrails (Claude Haiku 5.5)

![Figure A1](figures/figA1_adherence_dose.png)

**(a) Partial adherence.** Δ by the probability that a firm's price is the hub's recommendation (n = 10–20 per point). The shaded bands mark the acceptance rates reported in the RealPage case.

**(b) Guardrails.** Mean market price over the first 40 rounds, under auto-accept, ±3% and ±1% per-round bands, and firm discretion.
