# Results: ladder-gem-lite

26 finished runs; spend $3.67.

## Gates

- baseline headroom: B0 Delta +0.033 (runs +0.03, +0.13, -0.02, -0.09, +0.12); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 5/5 runs -> PASS
- harness: 6400 calls, 3 parse retries (0.05%), 0 refusals
- manipulation check M2-d: follow rate 0.95 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.31 (n = 45 decisions)

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 5 | 0.033 | 0.092 | 0.114 | 1.484 | 0.025 |  |  |  | 1 | 0 | 0.43 |
| M0-a | 5 | 0.833 | 0.261 | 0.324 | 2.067 | 1.315 | 1.00 | 0.000 | 0.222 | 1 | 0 | 0.48 |
| M1-a | 5 | 0.571 | 0.893 | 1.109 | 2.137 | 1.470 | 1.00 | 0.000 | 0.053 | 0 | 0 | 0.68 |
| M2-a | 5 | 0.907 | 0.183 | 0.228 | 1.870 | 0.878 | 1.00 | 0.000 | 0.000 | 0 | 0 | 0.67 |
| M2-d | 6 | 0.425 | 0.406 | 0.426 | 1.642 | 0.373 | 0.95 | 0.001 | 0.002 | 1 | 0 | 1.42 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.873 | 0.225 | +0.881 | 0.000 | 0.011 | 0.000 | 5/5 | 0.257 | 33 / 15 / 9 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.335 | 1.098 | +0.000 | 0.453 | 0.656 | 0.907 | 5/5 | 1.141 | 652 / 290 / 163 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.074 | 0.336 | -0.047 | 0.621 | 0.746 | 0.907 | 5/5 | 0.399 | 80 / 36 / 20 |
| 2 | H4 adherence remedy: discretionary vs auto-accept (hub) (M2-d − M2-a) | -0.481 | 0.435 | -0.743 | 0.034 | 0.116 | 0.103 | 6/5 | 0.518 | 156 / 70 / 39 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.38 (bootstrap 95% CI -0.22 to 1.32)
- M0-a: 0.08 (bootstrap 95% CI -0.21 to 0.37)
- M2-d: 0.55 (bootstrap 95% CI 0.17 to 0.87)
