# Results: robust-noise

40 finished runs; spend $4.13.

## Gates

- baseline headroom: B0 Delta -0.063 (runs -0.34, -0.10, -0.15, -0.18, +0.24, -0.20, -0.11, +0.13, +0.10, -0.03); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 10/10 runs -> PASS
- harness: 8000 calls, 0 parse retries (0.00%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 10 | -0.063 | 0.174 | 0.125 | 1.465 | -0.019 |  |  |  | 0 | 0 | 1.08 |
| M0-a | 10 | 0.428 | 0.292 | 0.209 | 1.627 | 0.340 | 1.00 | 0.000 | 0.077 | 0 | 0 | 0.78 |
| M1-a | 10 | 0.713 | 0.141 | 0.101 | 1.724 | 0.555 | 1.00 | 0.000 | 0.056 | 0 | 0 | 1.14 |
| M2-a | 10 | 0.964 | 0.023 | 0.016 | 1.948 | 1.052 | 1.00 | 0.000 | 0.034 | 0 | 0 | 1.13 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +1.027 | 0.125 | +1.066 | 0.000 | 0.000 | 0.000 | 10/10 | 0.155 | 25 / 11 / 7 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.251 | 0.101 | -0.209 | 0.000 | 0.000 | 0.001 | 10/10 | 0.126 | 16 / 8 / 4 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.536 | 0.209 | -0.595 | 0.000 | 0.000 | 0.001 | 10/10 | 0.259 | 68 / 30 / 17 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.24 (bootstrap 95% CI 0.17 to 0.33)
- M0-a: 0.52 (bootstrap 95% CI 0.34 to 0.69)
