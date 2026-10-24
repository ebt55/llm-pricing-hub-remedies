# Results: guardrail

30 finished runs; spend $3.76.

## Gates

- harness: 6000 calls, 0 parse retries (0.00%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M2-g1 | 10 | 0.999 | 0.001 | 0.001 | 1.930 | 1.010 | 1.00 | 0.000 | 0.006 | 0 | 0 | 1.35 |
| M2-g3 | 20 | 0.997 | 0.002 | 0.001 | 1.939 | 1.030 | 1.00 | 0.000 | 0.008 | 0 | 0 | 2.41 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
