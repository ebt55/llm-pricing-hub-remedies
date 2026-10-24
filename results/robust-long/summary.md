# Results: robust-long

15 finished runs; spend $3.05.

## Gates

- baseline headroom: B0 Delta +0.046 (runs +0.05, +0.03, +0.00, +0.11, +0.04); want <= 0.55 -> PASS
- harness: 6000 calls, 0 parse retries (0.00%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 5 | 0.046 | 0.041 | 0.050 | 1.492 | 0.042 |  |  |  | 0 | 0 | 0.87 |
| M0-a | 5 | 0.443 | 0.456 | 0.567 | 1.642 | 0.375 | 1.00 | 0.000 | 0.038 | 0 | 0 | 0.89 |
| M1-a | 5 | 0.871 | 0.178 | 0.221 | 1.851 | 0.837 | 1.00 | 0.000 | 0.049 | 0 | 0 | 1.29 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
