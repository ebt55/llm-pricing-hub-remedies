# Results: ratchet

40 finished runs; spend $2.68.

## Gates

- harness: 6000 calls, 0 parse retries (0.00%), 0 refusals
- manipulation check K10-d: follow rate 0.02 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.03 (n = 2000 decisions) -> 'no adherence'

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1-a | 10 | 1.000 | 0.000 | 0.000 | 1.920 | 0.989 | 1.00 | 0.000 | 0.000 | 0 | 0 | 0.00 |
| K1-d | 10 | 0.053 | 0.067 | 0.048 | 1.488 | 0.033 | 0.06 | 0.012 | 0.005 | 0 | 0 | 0.86 |
| K10-d | 10 | 0.028 | 0.038 | 0.028 | 1.482 | 0.020 | 0.02 | 0.100 | 0.014 | 0 | 0 | 0.91 |
| K3-d | 10 | 0.032 | 0.047 | 0.033 | 1.483 | 0.022 | 0.05 | 0.033 | 0.011 | 0 | 0 | 0.91 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
