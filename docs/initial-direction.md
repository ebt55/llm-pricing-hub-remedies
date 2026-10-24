# Initial direction (plain-language summary)

*Written Sat 24 Oct 2026, ~23:50 IST, while the first pilot of design v2 was finishing. The early numbers below come from single pilot runs and are **not final results**.*

## The real-world story

RealPage sold pricing software to competing landlords. It used every landlord's private rent data to recommend rents, and rents went up. The US government sued, and the settlement set rules:

1. The software can't use competitors' current private data.
2. It can only use old data.
3. Landlords shouldn't just auto-accept its recommendations.

## Our question

Do those rules still work if the pricing software is an AI, like ChatGPT or Claude?

## How we test it

We run a simulated market:
- Two shops sell the same product, and each sets a price every round for 100 rounds.
- Each shop is run by an AI, and each shop's pricing software is also an AI.
- Each run starts with 10 rounds of normal, competitive prices: the "before the software arrived" period.
- We measure whether prices drift up toward the price a cartel would charge.

## The key twist (from the redesign)

Software that tries to help **only its own shop** keeps prices low: it just undercuts the rival.

The harmful case is software that acts for **the whole market**, a hub that wants all its customers to profit. That's the RealPage worry.

So we build that harmful hub, then apply each legal rule one at a time and check whether prices come back down:

| Setup | What we learn |
|---|---|
| No software | The normal price level |
| Hub with competitors' **current** data | The harm: does it act like a cartel? |
| Hub with only **old** data | Does rule 2 fix it? |
| Hub with **no** competitor data | Does rule 1 fix it? |
| Hub's advice is **optional**, not auto-accepted | Does rule 3 fix it? |

Plus controls to check that the measurements work.

## What the early runs showed (one run each, not final)

| Setup | Prices |
|---|---|
| No software | Stay normal (~1.45) |
| Hub with current data | Climb to cartel level (~1.90) |
| Hub with no competitor data | Stay normal: the data ban seems to work |
| Hub with old data | Still rise partway (~1.8) |

The old-data result suggests the allowed data may still leave room for a "technically legal" cartel. That's the Saul Goodman angle behind the title: Saul's trademark is staying technically legal while doing shady things. In the paper we call this **compliant collusion**.

## Next steps

1. Check the pilot numbers.
2. Run the full experiment with more repeats, so the results are solid.
3. Repeat the key comparison on OpenAI's model (free), and possibly DeepSeek, to show the result isn't specific to Claude.
4. Write it up as **S'all Good, Man? Do Antitrust Remedies Stop an AI Pricing Cartel?**

For the detail behind each decision, see [SPRINT_LOG.md](../SPRINT_LOG.md).
