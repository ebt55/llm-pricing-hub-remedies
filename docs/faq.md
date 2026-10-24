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

**Data Limits and Guardrails Don't Stop an LLM Pricing Hub; Only Firm Discretion Does** states the three main findings directly:
- **Data limits**, the RealPage settlement's data rules (stale data only, no current competitor data, aggregation), leave most of an AI hub's harm in place.
- **Guardrails** don't help either. The settlement still allows auto-accept within limits each landlord sets, such as a 3% daily cap. Under that rule the hub reached near-monopoly prices by round 8 instead of round 4.
- **Only firm discretion works.** When firms set every price themselves, with the hub's advice optional, almost all the harm goes away.

We call the residual harm **data-compliant coordination**: the hub obeys every data restriction, but prices still move toward joint monopoly, because the hub's *objective* drives them.

Earlier titles were changed during the sprint. "S'all Good, Man?" was dropped after a simulated judge review found it unclear. "…Only Ending Auto-Accept Stops…" was dropped because the settlement restricts auto-accept rather than ending it.
