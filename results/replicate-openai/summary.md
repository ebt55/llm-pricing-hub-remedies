# Results: replicate-openai

12 finished runs; spend $0.00.

## Gates

- baseline headroom: B0 Delta +0.033 (runs +0.07, -0.00, +0.03); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 1/3 runs -> FAIL
- harness: 2400 calls, 0 parse retries (0.00%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 3 | 0.033 | 0.039 | 0.096 | 1.485 | 0.027 |  |  |  | 0 | 0 | 0.00 |
| M0-a | 3 | 0.095 | 0.050 | 0.123 | 1.507 | 0.075 | 1.00 | 0.000 | 0.033 | 0 | 0 | 0.00 |
| M1-a | 3 | 0.315 | 0.361 | 0.897 | 1.577 | 0.231 | 1.00 | 0.000 | 0.014 | 0 | 0 | 0.00 |
| M2-a | 3 | 0.512 | 0.423 | 1.052 | 1.705 | 0.513 | 1.00 | 0.000 | 0.015 | 0 | 0 | 0.00 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.479 | 1.040 | +0.282 | 0.188 | 0.100 | 0.188 | 3/3 | 0.687 | 142 / 63 / 36 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.197 | 0.901 | -0.202 | 0.574 | 0.400 | 0.574 | 3/3 | 0.900 | 243 / 108 / 61 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.417 | 1.032 | -0.230 | 0.229 | 0.100 | 0.458 | 3/3 | 0.689 | 143 / 64 / 36 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.41 (bootstrap 95% CI -1.30 to 0.92)
- M0-a: 0.87 (bootstrap 95% CI 0.56 to 0.99)
