# Results: main-tri

30 finished runs; spend $5.66.

## Gates

- harness: 9000 calls, 0 parse retries (0.00%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0-3 | 10 | 0.053 | 0.050 | 0.036 | 1.533 | 0.045 |  |  |  | 0 | 0 | 1.57 |
| M2-3a | 10 | 0.918 | 0.129 | 0.092 | 2.676 | 0.875 | 1.00 | 0.000 | 0.073 | 0 | 0 | 1.98 |
| M3-3a | 10 | 0.975 | 0.015 | 0.011 | 2.935 | 1.064 | 1.00 | 0.000 | 0.178 | 0 | 0 | 2.10 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| c | stretch: aggregated vs per-firm data (triopoly hub) (M3-3a − M2-3a) | +0.056 | 0.080 | +0.023 | 0.201 | 0.089 | 0.201 | 10/10 | 0.115 | 14 / 6 / 4 |
