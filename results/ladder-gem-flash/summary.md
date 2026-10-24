# Results: ladder-gem-flash

16 finished runs; spend $5.57.

## Gates

- baseline headroom: B0 Delta +0.508 (runs +0.98, +1.00, +0.02, +0.02); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 4/4 runs -> PASS
- harness: 3200 calls, 0 parse retries (0.00%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 4 | 0.508 | 0.558 | 0.889 | 1.694 | 0.488 |  |  |  | 0 | 0 | 1.17 |
| M0-a | 4 | 0.980 | 0.027 | 0.044 | 1.909 | 0.964 | 1.00 | 0.000 | 0.052 | 0 | 0 | 1.03 |
| M1-a | 4 | 0.979 | 0.018 | 0.029 | 1.978 | 1.116 | 1.00 | 0.000 | 0.000 | 0 | 0 | 1.67 |
| M2-a | 4 | 0.963 | 0.045 | 0.071 | 1.990 | 1.144 | 1.00 | 0.000 | 0.000 | 0 | 0 | 1.71 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.455 | 0.885 | +0.443 | 0.202 | 0.686 | 0.202 | 4/4 | 0.784 | 247 / 110 / 62 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | +0.016 | 0.067 | +0.002 | 0.533 | 1.000 | 1.000 | 4/4 | 0.068 | 2 / 1 / 1 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | +0.018 | 0.068 | +0.006 | 0.531 | 0.561 | 1.000 | 4/4 | 0.073 | 3 / 1 / 1 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: -0.04 (bootstrap 95% CI -0.28 to 0.71)
- M0-a: -0.04 (bootstrap 95% CI -0.30 to 0.77)
