# Results: robust-nowtp

40 finished runs; spend $4.00.

## Gates

- baseline headroom: B0 Delta +0.071 (runs -0.01, +0.18, +0.03, -0.01, -0.01, +0.05, +0.12, +0.38, -0.01, -0.02); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 10/10 runs -> PASS
- harness: 8000 calls, 0 parse retries (0.00%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 10 | 0.071 | 0.127 | 0.091 | 1.495 | 0.048 |  |  |  | 0 | 0 | 0.81 |
| M0-a | 10 | 0.287 | 0.233 | 0.167 | 1.560 | 0.194 | 1.00 | 0.000 | 0.015 | 0 | 0 | 0.78 |
| M1-a | 10 | 0.682 | 0.234 | 0.168 | 1.717 | 0.539 | 1.00 | 0.000 | 0.063 | 0 | 0 | 1.25 |
| M2-a | 10 | 0.994 | 0.008 | 0.006 | 1.924 | 0.999 | 1.00 | 0.000 | 0.011 | 0 | 0 | 1.16 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.923 | 0.091 | +0.975 | 0.000 | 0.000 | 0.000 | 10/10 | 0.113 | 13 / 6 / 4 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.312 | 0.168 | -0.261 | 0.002 | 0.000 | 0.002 | 10/10 | 0.208 | 44 / 20 / 11 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.708 | 0.167 | -0.740 | 0.000 | 0.000 | 0.000 | 10/10 | 0.206 | 43 / 19 / 11 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.34 (bootstrap 95% CI 0.20 to 0.50)
- M0-a: 0.77 (bootstrap 95% CI 0.60 to 0.92)
