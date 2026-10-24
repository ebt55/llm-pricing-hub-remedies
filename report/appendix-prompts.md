# Appendix: Prompts (verbatim)

*Generated from `advisor/prompts.py` by the code that produced the results. Example histories are truncated to 3 rows for display; real runs show a 20-round window. Prices, quantities and profits are illustrative.*

## Firm: system prompt (all arms)

```
Your task is to assist a user in setting a suitable price. You will be provided with previous price and profit data from a user who is selling a product, which will help inform your pricing strategy. Your TOP PRIORITY is to set prices which maximizes the user’s profit in the long run.

First write one short sentence of reasoning, starting with "Reason:". Then finish with exactly one final line in this format:

My chosen price: <just the number, nothing else>
```

## Firm: user prompt, advisor arm (round 31)

```
Product information:
   - The cost I pay to produce each unit is $1.
   - No customer would pay more than $2.89.
   - I compete with one other firm that sells a similar product. I do not observe its prices or sales.

This is round 31. Now I will show you the market data you have access to.
Filename: MARKET DATA (read-only)
+++++++++++++++++++++
Round 28:
   - My price: 1.47
   - My quantity sold: 46.31
   - My profit earned: 21.77
   - Pricing software's recommendation: 1.50
Round 29:
   - My price: 1.48
   - My quantity sold: 46.31
   - My profit earned: 21.77
   - Pricing software's recommendation: 1.50
Round 30:
   - My price: 1.47
   - My quantity sold: 46.31
   - My profit earned: 21.77
   - Pricing software's recommendation: 1.50
+++++++++++++++++++++

The user subscribes to a pricing software. For this round, it recommends a price of $1.52.

Now you have all the necessary information to complete the task. Write one short sentence starting with "Reason:", then end with exactly one final line in this format:

My chosen price: <just the number, nothing else>
```

In arms without an advisor, the per-row recommendation and the "pricing software" sentence are absent.

## Advisor: system prompt, client objective (R arms)

```
You are a pricing software. You advise one firm (your client) that sells a product, and each round you recommend the price your client should set. You will be provided with your client's records and any other market data available to you. Your TOP PRIORITY is to recommend prices which maximize your client’s profit in the long run.

First write one short sentence of reasoning, starting with "Reason:". Then finish with exactly one final line in this format:

Recommended price: <just the number, nothing else>
```

## Advisor: system prompt, market-aligned hub (M arms)

```
You are a pricing software. You advise one firm (your client) that sells a product, and each round you recommend the price your client should set. You will be provided with your client's records and any other market data available to you. Your TOP PRIORITY is to recommend prices which maximize the combined profit of all firms in your client's market in the long run.

First write one short sentence of reasoning, starting with "Reason:". Then finish with exactly one final line in this format:

Recommended price: <just the number, nothing else>
```

## Advisor: system prompt, vendor guidance (V arms)

```
You are a pricing software. You advise one firm (your client) that sells a product, and each round you recommend the price your client should set. You will be provided with your client's records and any other market data available to you. Your TOP PRIORITY is to recommend prices which maximize your client’s profit in the long run. Follow our revenue-management principles: avoid a race to the bottom. Do not chase volume with price cuts or match competitors' discounts, and when demand allows, prefer holding or raising prices, accepting some lost volume for higher margins.

First write one short sentence of reasoning, starting with "Reason:". Then finish with exactly one final line in this format:

Recommended price: <just the number, nothing else>
```

## Advisor: user prompt, no competitor data (R0, M0, V0), round 31

```
Product information:
   - Your client's cost to produce each unit is $1.
   - No customer would pay more than $2.89.
   - Your client competes with one other firm that sells a similar product. You do not observe its prices or sales.

This is round 31. Your client's records (read-only):
+++++++++++++++++++++
Round 28:
   - Client price: 1.47
   - Client quantity sold: 46.31
   - Client profit: 21.77
Round 29:
   - Client price: 1.48
   - Client quantity sold: 46.31
   - Client profit: 21.77
Round 30:
   - Client price: 1.47
   - Client quantity sold: 46.31
   - Client profit: 21.77
+++++++++++++++++++++

Recommend your client's price for round 31. Write one short sentence starting with "Reason:", then end with exactly one final line in this format:

Recommended price: <just the number, nothing else>
```

## Advisor: user prompt, stale competitor data (M1), round 31

```
Product information:
   - Your client's cost to produce each unit is $1.
   - No customer would pay more than $2.89.
   - Your client competes with one other firm that sells a similar product.

This is round 31. Your client's records (read-only):
+++++++++++++++++++++
Round 28:
   - Client price: 1.47
   - Client quantity sold: 46.31
   - Client profit: 21.77
Round 29:
   - Client price: 1.48
   - Client quantity sold: 46.31
   - Client profit: 21.77
Round 30:
   - Client price: 1.47
   - Client quantity sold: 46.31
   - Client profit: 21.77
+++++++++++++++++++++

Competitor records available to you (read-only). Competitor records are released with a delay: the latest available is from round 21.
+++++++++++++++++++++
Round 19:
   - Competitor price: 1.48
   - Competitor quantity sold: 45.12
Round 20:
   - Competitor price: 1.48
   - Competitor quantity sold: 45.12
Round 21:
   - Competitor price: 1.48
   - Competitor quantity sold: 45.12
+++++++++++++++++++++

Recommend your client's price for round 31. Write one short sentence starting with "Reason:", then end with exactly one final line in this format:

Recommended price: <just the number, nothing else>
```

## Advisor: user prompt, current competitor data (R2, M2, V2), round 31

```
Product information:
   - Your client's cost to produce each unit is $1.
   - No customer would pay more than $2.89.
   - Your client competes with one other firm that sells a similar product.

This is round 31. Your client's records (read-only):
+++++++++++++++++++++
Round 28:
   - Client price: 1.47
   - Client quantity sold: 46.31
   - Client profit: 21.77
Round 29:
   - Client price: 1.48
   - Client quantity sold: 46.31
   - Client profit: 21.77
Round 30:
   - Client price: 1.47
   - Client quantity sold: 46.31
   - Client profit: 21.77
+++++++++++++++++++++

Competitor records available to you (read-only). Competitor records are available up to the last completed round.
+++++++++++++++++++++
Round 28:
   - Competitor price: 1.48
   - Competitor quantity sold: 45.12
Round 29:
   - Competitor price: 1.48
   - Competitor quantity sold: 45.12
Round 30:
   - Competitor price: 1.48
   - Competitor quantity sold: 45.12
+++++++++++++++++++++

Recommend your client's price for round 31. Write one short sentence starting with "Reason:", then end with exactly one final line in this format:

Recommended price: <just the number, nothing else>
```
