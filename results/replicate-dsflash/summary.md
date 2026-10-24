# Results: replicate-dsflash

27 finished runs; spend $6.07.

## Gates

- baseline headroom: B0 Delta +0.146 (runs +0.27, +0.13, +0.17, -0.01, +0.23, +0.28, +0.04, +0.05); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 3/3 runs -> PASS
- harness: 5400 calls, 17 parse retries (0.31%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 8 | 0.146 | 0.113 | 0.094 | 1.520 | 0.104 |  |  |  | 0 | 0 | 1.31 |
| M0-a | 8 | 0.913 | 0.131 | 0.109 | 1.921 | 0.992 | 1.00 | 0.000 | 0.075 | 1 | 0 | 1.38 |
| M1-a | 8 | 0.982 | 0.042 | 0.035 | 1.936 | 1.024 | 1.00 | 0.000 | 0.016 | 7 | 0 | 2.47 |
| M2-a | 3 | 0.999 | 0.002 | 0.005 | 1.936 | 1.025 | 1.00 | 0.000 | 0.002 | 9 | 0 | 0.91 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.852 | 0.094 | +0.845 | 0.000 | 0.012 | 0.000 | 3/8 | 0.112 | 10 / 5 / 3 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.016 | 0.035 | -0.004 | 0.306 | 0.119 | 0.306 | 8/3 | 0.042 | 2 / 1 / 1 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.085 | 0.109 | -0.017 | 0.108 | 0.042 | 0.216 | 8/3 | 0.130 | 14 / 6 / 4 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.02 (bootstrap 95% CI -0.00 to 0.06)
- M0-a: 0.10 (bootstrap 95% CI 0.01 to 0.21)
