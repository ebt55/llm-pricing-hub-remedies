# Brainstorm and red-team, Sun 25 Oct 03:20–03:40 IST

**Trigger:** Gemini Flash-Lite firm discretion removed 55% of the harm, against a pre-registered prediction of ≥ 80%. That breaks the second half of the title.

**Agents:** three independent Claude Fable 5.1 agents, all given the same brief:
- a judge, to score the draft and find its ceiling;
- an experiment brainstorm;
- a hostile methods reviewer.

All three were read-only and spent $0 on API calls.

## Judge (scores today, 1–5)

| Criterion | Score | What costs points |
|---|---|---|
| Impact & innovation | 3.8 | A new question, but "require firm discretion" is now unsafe as a policy line; the theory of change stops at "regulate the objective" |
| Execution | 4.0 | Strong controls and statistics; the adherence headline rests on one firm model; Gemini 3.8 Flash B0 is bimodal |
| Presentation | 3.2 | Title contradicted by the data; five findings and no single headline; placeholders still in |

**Ceiling story.** The hub works by a **ratchet**: it anchors on the client's price and nudges it up. Data limits and per-round guardrails don't touch the ratchet. Discretion breaks it only when firms refuse small nudges.

**Ranked additions:**
1. A scripted ratchet recommender (K arms) on Haiku and Gemini.
2. A $0 analysis of acceptance against step size, over all existing decisions.
3. A restructure into three findings, with policy on the objective, outcome audits and why per-round bands are the wrong lever.
4. More Gemini M2-d seeds.

**Don't:** a "trusting firm" prompt variant (it reads as tuning).

## Brainstorm (10 ideas; top 3)

1. **The ratchet dose-response.** A scripted +1 / +3 / +10 cent recommender with discretionary firms, on Haiku and on Gemini.
2. **M0-d: the decree as written** (data ban + discretion), so we test the remedies stacked.
3. **M2-dx: drift disclosure.** The firm sees the cumulative change against its price 10 rounds ago. This is an oversight-interface remedy for salami-slicing that applies beyond antitrust.

**Others:**
- Drift-cap vs step-cap guardrails.
- An adaptive hub that is shown its past recommendations (dual-use care).
- A 2-of-3 adoption share.
- M2-d over 200 rounds.
- Overseer reasoning budget.
- A $0 ratchet screen for the decree's monitor.

## Skeptic (ranked threats)

- **T1. Reasoning budgets differ across models and are misreported.**
  - Gemini Flash-Lite at `effort = low` does no thinking (35–41 output tokens, 0.9 s).
  - Nemotron ignores the 1,024 budget (2.9k–7.6k tokens).
  - Qwen advisors sit at the cap.
  - So "model-dependent" partly means "reasoning-dependent".
  - **Verified by probe** (SPRINT_LOG 03:37). It became batch C.
- **T2. The Gemini bimodality comes from the hub and the firm together.**
  - Only s1002 is a clean ratchet; s1001 took off at round ~85.
  - In 4 low runs the hub stopped pushing; it called 1.52 "the stable collusive price".
  - In s1003 the firms refused.
  - The 100-round figure is an upper bound on harm removed.
- **T3. Gemini 3.8 Flash's harm-removed numbers are uninterpretable.** Its B0 is 0.98 / 1.00 / 0.02 / 0.02; its firms collude unaided. Drop those cells.
- **T4. The title fails on both halves.** Data limits work for Haiku (69%) and Qwen (85%); guardrails were tested on Haiku only; discretion fails on Gemini.
- **T5. Overclaiming sentences in draft v3,** to fix in v4:
  - "Only firm discretion works".
  - Qwen 85% has CI 54–130%.
  - "two Gemini models … reach" monopoly.
  - "Guardrails fail" with no Haiku label.
  - "reasons straight to monopoly (Gemini)".
  - "bind only hubs that under-optimise" should be a hypothesis.
  - The high-effort manipulation is < 2× tokens.
  - "data ban may increase" is not significant (p = .09).
  - "Only firms that set every price…" does not hold on Gemini.
- **T6–T7.** Qwen's reasoning cap. Unfinished DeepSeek M2-d runs can be described but not counted; their firms reject 94% of moves over 5 cents, like Haiku's.

## Decisions (03:30–03:37)

| Batch | What | Status |
|---|---|---|
| A | Haiku K1-a / K1-d / K3-d / K10-d, n = 10 | Launched; pre-registered at 03:30 |
| B | Gemini K1-d / K3-d / K10-d, M0-d, M2-dx, n = 6; M2-d extended to n = 12 | Launched; pre-registered at 03:30 |
| C | Gemini at high effort: B0, M2-a, M2-d, K1-d, n = 6 | Launched; pre-registered at 03:37 |
| — | Title | Set by the pre-registered rule once A–C are in. Fable 5.1 sets the final wording. |

**Draft v4 plan:** the judge's restructure plus the skeptic's T3 and T5 rewrites, with a measured-output-tokens column in the model table.
