# Results: followup

60 finished runs; spend $8.27.

## Gates

- harness: 15656 calls, 0 parse retries (0.00%), 0 refusals
- manipulation check M2-q50: follow rate 0.60 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.10 (n = 490 decisions) -> 'no adherence'
- manipulation check M2-q80: follow rate 0.83 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.15 (n = 127 decisions) -> 'no adherence'
- manipulation check M2-q90: follow rate 0.92 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.20 (n = 46 decisions) -> 'no adherence'
- manipulation check V2-d: follow rate 0.78 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.43 (n = 118 decisions)

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M2-q50 | 10 | 0.741 | 0.176 | 0.126 | 1.776 | 0.670 | 0.60 | 0.077 | 0.030 | 0 | 0 | 1.73 |
| M2-q80 | 10 | 0.901 | 0.047 | 0.033 | 1.863 | 0.862 | 0.83 | 0.037 | 0.019 | 0 | 0 | 1.41 |
| M2-q90 | 10 | 0.936 | 0.055 | 0.040 | 1.898 | 0.940 | 0.92 | 0.021 | 0.020 | 0 | 0 | 1.27 |
| V0-a | 10 | 0.453 | 0.325 | 0.233 | 1.633 | 0.355 | 1.00 | 0.000 | 0.056 | 0 | 0 | 0.87 |
| V2-a | 10 | 0.214 | 0.267 | 0.191 | 1.541 | 0.152 | 1.00 | 0.000 | 0.008 | 0 | 0 | 1.05 |
| V2-d | 10 | 0.085 | 0.103 | 0.074 | 1.502 | 0.064 | 0.78 | 0.014 | 0.024 | 0 | 0 | 1.94 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
