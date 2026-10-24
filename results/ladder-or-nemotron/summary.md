# Results: ladder-or-nemotron

16 finished runs; spend $3.61.

## Gates

- baseline headroom: B0 Delta +0.033 (runs +0.04, +0.04, -0.01, +0.06); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 4/4 runs -> PASS
- harness: 3200 calls, 45 parse retries (1.41%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 4 | 0.033 | 0.031 | 0.049 | 1.492 | 0.043 |  |  |  | 11 | 0 | 0.51 |
| M0-a | 4 | 0.110 | 0.073 | 0.116 | 1.522 | 0.109 | 1.00 | 0.000 | 0.050 | 4 | 0 | 0.78 |
| M1-a | 4 | 0.280 | 0.102 | 0.163 | 1.592 | 0.263 | 1.00 | 0.000 | 0.136 | 14 | 0 | 1.22 |
| M2-a | 4 | 0.990 | 0.011 | 0.017 | 1.932 | 1.016 | 1.00 | 0.000 | 0.027 | 16 | 0 | 1.10 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.956 | 0.046 | +0.950 | 0.000 | 0.029 | 0.000 | 4/4 | 0.046 | 1 / 1 / 1 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.710 | 0.162 | -0.688 | 0.001 | 0.029 | 0.001 | 4/4 | 0.144 | 9 / 4 / 3 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.879 | 0.114 | -0.897 | 0.000 | 0.029 | 0.000 | 4/4 | 0.103 | 5 / 2 / 2 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.74 (bootstrap 95% CI 0.66 to 0.84)
- M0-a: 0.92 (bootstrap 95% CI 0.85 to 0.98)
