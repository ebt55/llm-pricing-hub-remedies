# FAQ (plain language)

*Answers to questions asked during the sprint, Sat 24 – Sun 25 Oct 2026. See also [initial-direction.md](initial-direction.md).*

## What are our antitrust remedies?

**Antitrust remedies** are the rules a court or settlement imposes to stop anticompetitive behaviour. Ours come from the US government's settlement with RealPage, as reported in our incident notes. We turn each rule into a setting in the simulation and test it on the AI hub:

| Remedy (real world) | What it means | How we test it | Arm |
|---|---|---|---|
| **1. Data ban** | The software can't use competitors' *current private* data when making recommendations | The hub sees only its own shop's data, nothing about the rival | M0-a |
| **2. Old data only** | Competitors' private data can be used only if it's at least 12 months old | The hub sees the rival's data only from 10+ rounds ago | M1-a |
| **3. No auto-accept** | Landlords shouldn't let the software set rents automatically; a person decides | The shop's AI sees the hub's advice but is free to ignore it | M2-d |
| **4. Aggregated data only** | No reporting narrower than state level: no competitor-by-competitor detail | The hub sees only a market-wide average (needs 3 shops, so this is the stretch arm) | M3-3a |

The **harmful starting point** we compare against is the hub that sees the rival's current data and whose advice is auto-accepted (M2-a). That's the pattern the lawsuit targeted.

Two honest caveats for the paper:
- **Rule 2 is translated, not copied.** The real 12-month rule is about the data used to *train* the software. We test the closest live equivalent: old data at the moment of each decision.
- **Rule 3 came from the lawsuit's complaints** about landlords auto-accepting recommendations. It isn't one of the settlement's main data rules, and we say so.

## How does this help identify collusion between AI models?

Honestly, the project's main contribution is **prevention** (do the legal rules stop AI collusion?), not detection. But it helps with identifying collusion in four ways, and a cheap fifth step makes detection a real part of the paper.

**1. It shows where the collusion lives, so investigators know where to look.**
Our two shop AIs never talk to each other. The coordination runs through the shared hub: the same goal, applied by the same kind of AI, to pooled data. Reading messages between firms would find nothing; you have to look at the advisor's objective and its data feed. The lesson for regulators: AI collusion can be silent.

**2. It gives a causal test a regulator could actually run.**
"Cut off the competitor data and see whether prices fall" is an audit, not a correlation. If prices drop when data access is removed, the data was enabling the coordination. Our remedy arms are this test, run under controlled conditions.

**3. It separates collusion from innocent high prices.**
The same data with a different goal gives a different outcome. An advisor serving only its own shop undercuts, so prices stay low; a market-wide hub raises them. That gives a measurable signature: **recommendations above the best response to the data the advisor saw.** An advisor that knows the rival's price but still recommends well above the profit-maximising reply is acting for the market, not its client.

**4. It records the warning signs regulators look for.**
We log signals that match the legal "plus factors" in our prep notes:
- prices moving in lockstep;
- both firms getting near-identical recommendations;
- how often firms follow the advice;
- the advisor's own reasoning text for every decision.

**5. The add-on: test detectors against known answers.**
Our runs come with built-in labels: we *know* which advisors work for the whole market and which don't. So we can score detectors on how many collusive hubs they catch and how many false alarms they raise:
- **a price-based detector**, using the "above best response" gap;
- **an AI monitor** that reads the advisor's reasoning and flags coordination talk like "match the rival" or "avoid a price war".

The key test is the **"technically legal" cases** (the hub with old data, or with no data): does a detector still catch the hub when it follows the rules?

That connects the paper to the sprint's detection track as well as the markets track. It reuses data we already collect and adds an estimated ~$1–3 in monitor calls. Planned as a stretch section after the main batch.

## Why this title?

**An LLM Pricing Hub Survives Data Limits on Some Models; Firm Discretion Works Only When Firms Refuse Small Nudges** states the two findings that held up across models:
- **Data limits on some models.** A ban on rival data removes most of the hub's harm for three models (Nemotron 92%, Qwen 85%, Haiku 69%), but almost none for two (DeepSeek 10%, Gemini Flash-Lite 8%). So the rule's effect depends on the model, not the rule.
- **Firm discretion only when firms refuse small nudges.** The hub raises prices in small steps (a "ratchet"). Discretion stops it only if the shop's AI says no to small nudges. Haiku's shops do. Qwen's refuse big jumps but let a patient 1-cent ratchet through. Gemini Flash-Lite's accept nudges of any size, even with thinking switched on, and so do GPT-5.4 mini's.

**Guardrails** (auto-accept within ±1–3% per round) are not in the title, because we tested them on two models only. On Haiku they removed none of the harm, and on Qwen 12%. In both they only delayed monopoly.

**How it was chosen.** The wording follows rules logged before the results (SPRINT_LOG 03:05 and 03:30), with the final wording set by an independent Fable 5.1 review (SPRINT_LOG 05:04).

**Earlier titles:**
- "S'all Good, Man?" was dropped as unclear.
- "…Only Ending Auto-Accept Stops…" was dropped because the settlement restricts auto-accept rather than ending it.
- "Data Limits and Guardrails Don't Stop an LLM Pricing Hub; Only Firm Discretion Does" was dropped when data limits turned out to work on three models and firm discretion failed on Gemini.

We call the harm that survives the data rules **data-compliant coordination**.

## What is firm discretion, and how does it hold the AIs off collusion?

**What it is.** Each round, a shared pricing hub (an AI told to maximise the two shops' *combined* profit, the incentive alleged against RealPage) recommends a price to each shop's AI.
- **Auto-accept:** the recommendation simply becomes the price. The shop's AI isn't even asked.
- **Firm discretion:** the shop's AI sees the recommendation next to its own sales history and picks its own price. It can follow the recommendation, ignore it, or land in between.

The real-world version is a leasing manager who can override RealPage. The DOJ settlement protects overrides (§V.A.5) and bans rewards for accepting (§V.C).

**Why it holds collusion off.** The collusion lives in the hub: both shops get the same "everyone raise prices" plan. That plan is good for the pair, but each shop, looking only at its own data, sees that raising its price loses customers to a cheaper rival. A shop that thinks for itself keeps drifting back down. This is the classic cartel problem: every member is tempted to cheat.

**Auto-accept is what removes that temptation.** The hub sets both prices, so nobody can cheat. Discretion puts the temptation back. The shop isn't *trying* to fight collusion; its own self-interest is what breaks the cartel. A real Claude Haiku shop, in round 18, recommended $1.60:

> "Average observed profit is highest near $1.43 … and $1.60 lies outside the tested range, so I'll stay near the best-performing tested price."

**When it fails.** Discretion only protects if the one deciding actually pushes back. We tested this with a scripted hub that nudges the price up by +1, +3 or +10 cents a round. Profit gain Δ is 0 at competitive prices and 1 at the monopoly price:

| Shop AI | Δ | Outcome |
|---|---|---|
| Claude Haiku (reasons before answering) | 0.03–0.05 | Competitive, the same as having no hub |
| Gemini Flash-Lite (no thinking at our settings) | 0.93–1.00 | Followed the nudges all the way to monopoly |

A typical Gemini reason:

> "…the software's upward nudge, a slight increase to 1.52 will test higher profit margins…"

Two fixes didn't help the Gemini shops:
- showing them the total drift ("+7.5% vs 10 rounds ago");
- adding the data ban on top.

**The AI-safety translation.** Firm discretion is a "human (or AI) in the loop". It works only if whoever is in the loop has their own interest and uses their own judgment. A rubber stamp in the loop is the same as auto-accept. Former RealPage employees put landlords' acceptance at 80–90%, which is closer to our Gemini shops than to our Haiku ones.

## Is RealPage real, or part of the simulation?

**RealPage is real.** It's a real company and a real antitrust case. The "incident" label just comes from the sprint prep folder (`02_incidents/`), where it's one of the real-world cases we collected. Nothing about RealPage itself is inside our experiment.

**What's real (outside our study):**
- RealPage sells rent-pricing software to US landlords. Landlords feed it their private rent and occupancy data, and it recommends rents.
- The US Department of Justice and several states sued in 2024. They alleged that competing landlords coordinated rents through the software: a "hub-and-spoke" cartel, with RealPage as the hub.
- The case ended in settlements. The Final Judgment we cite (entered 19 May 2026) sets the rules we test: no competitors' current private data, training data at least 12 months old, protected overrides, and more.
- The numbers on how often landlords accepted the recommendations come from the DOJ complaint and from reporting based on former employees.

**What's simulated (our study):**
- A toy market with two shops selling one product. It's a standard economics model (Calvano et al.), not rental housing.
- The shops and the hub are LLMs: Claude Haiku, Gemini, Qwen and others.
- The hub plays a RealPage-*like* role. It advises both shops and is told to care about their combined profit.
- Each settlement rule becomes a setting, for example "the hub can't see the rival's data". We then check whether prices still rise to the monopoly level.

**The honest caveat** (it's in the paper): RealPage's real software is its own pricing algorithm, not an LLM. We don't claim RealPage behaves like our hub. The question is forward-looking: if pricing hubs like this are built on LLMs, would the remedies written for RealPage still work? So far the answer is "mostly not, and it depends on the model."
