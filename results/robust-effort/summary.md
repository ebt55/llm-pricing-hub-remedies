# Results: robust-effort

20 finished runs; spend $3.64.

## Gates

- harness: 4000 calls, 37 parse retries (0.92%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M0-a | 10 | 0.290 | 0.295 | 0.211 | 1.573 | 0.222 | 1.00 | 0.000 | 0.052 | 1 | 0 | 1.40 |
| M1-a | 10 | 0.910 | 0.102 | 0.073 | 1.888 | 0.919 | 1.00 | 0.000 | 0.070 | 36 | 0 | 2.24 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
