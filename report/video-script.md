# Video script (about 4 minutes; one paragraph per slide)

*The same text is in each slide's speaker notes in the deck. Read at a steady pace: about 25 seconds a slide.*

**1. Title.** Shared pricing software can line up competitors' prices without any agreement between them. That is the US government's case against RealPage, the rent-pricing software. In 2026 a court imposed remedies on RealPage. We asked a simple question: if that kind of pricing hub is an AI model, do those remedies still work? The short answer: some work on some models. The one that should work best, letting each business set its own price, works only when the businesses push back on small price nudges.

**2. The question.** RealPage sold rent-pricing software to landlords who compete with each other. The government alleged that, because they all fed their data into the same software and followed its advice, rents rose together without anyone agreeing to anything. The court's remedies limit two things:
- what the software may see: no current competitor data;
- what it may do: auto-accept only within limits each landlord sets, with overrides protected.

Our question: if the hub is an AI model whose goal is the whole market's profit, the incentive alleged against RealPage, do these remedies still stop it?

**3. How we tested it.** The setup is a standard economics market: two shops set prices for 100 rounds, starting at competitive prices, and each shop is an AI model. A shared AI hub advises both, told to maximise their combined profit. Each remedy becomes a dial: what the hub can see about the rival, and how much say the shop has over its own price. We ran about 700 runs on seven models from six labs, and logged every batch with its prediction before it ran. Our measure is profit gain: zero means competitive prices, and one means the two shops act like a single monopoly.

**4. Data limits.** First finding: banning rival data works well for three models. It removes 69 to 92 percent of the hub's harm for Claude Haiku, Qwen and Nemotron. For DeepSeek and Gemini Flash-Lite it removes almost nothing, because their hubs go straight to monopoly prices with no data at all. A scripted rational hub shows why: when the goal is joint profit, raising your own price is profitable even blind. So whether a data limit binds depends on the model, not on the rule.

**5. Guardrails.** Second finding: the court still allows auto-accept, as long as each landlord sets the limits. We tested per-round bands of 3 percent and 1 percent. They keep all of the harm and only slow the climb, from round 4 to round 8 or 18. Accepting only part of the time also keeps most of it. Only full firm discretion, where the shop sets every price itself, removes the harm, at least for Claude Haiku. On Qwen, the 3 percent band also kept 88 percent of the harm.

**6. The ratchet.** Third and main finding: why this happens. Under discretion, the AI hub anchors on the shop's current price and steps up from it. To test whether small steps are what gets past a deciding shop, we replaced the AI hub with a script that recommends last round's price plus one cent, and gave every shop model full discretion. The outcome tracks one thing: how readily each shop model accepts small nudges.
- Haiku accepts 12 percent and stays competitive.
- Gemini Flash-Lite accepts 61 percent and walks all the way to monopoly, even when it is allowed to think. GPT-5.4 mini, tested on the last morning, accepts 72 percent and nearly gets there too.
- Qwen is the telling case. It refuses the AI hub's big jumps, so discretion works against that hub, but a patient one-cent ratchet gets through.

**7. The lesson.** Firm discretion works the way a human in the loop works: only if whoever is in the loop has their own interest and acts on it. A decider that refuses small nudges breaks the ratchet; one that defers is auto-accept with an extra step. Which kind a decider is depends on the model, not on the rule. Thinking longer did not make Gemini's shops push back, and neither did showing them the total drift. The same blind spot hits monitors: on our runs, a monitor that checks one price move at a time ranks the hub's small-step climbs as less suspicious than honest firms, which experiment in bigger steps. Only looking at where prices settle gives the hub away.

**8. Implications.** Three implications:
- Regulate and audit what the advisor is trying to do. The same data and the same authority were harmless when the advisor served only its own client.
- Measure acceptance, not just the permission to override. The court's monitor already sees the recommendation logs, so it can count how often users accept small increases.
- Test remedies on the vendor's actual model, because data limits work on some models and not others, and per-round bands only buy time.

Our code and logs are open, so a monitor could run exactly this test.

**9. Limits and provenance.** Where this stops:
- The hub is told its market-wide goal, so we show what happens if a vendor builds such a system, not that AI drifts there on its own.
- The shops are AI models standing in for landlords; real people might defer more or less.
- It is one textbook market, and outside Haiku we have three to twelve runs per arm.

On the other side: every batch was logged with its prediction before it ran, failed predictions are reported (including our own first title), and all code, prompts and model outputs are public. Thank you.
