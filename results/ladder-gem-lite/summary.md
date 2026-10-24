# Results: ladder-gem-lite

62 finished runs; spend $9.56.

## Gates

- baseline headroom: B0 Delta +0.033 (runs +0.03, +0.13, -0.02, -0.09, +0.12); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 5/5 runs -> PASS
- harness: 17200 calls, 3 parse retries (0.02%), 0 refusals
- manipulation check K10-d: follow rate 0.43 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.05 (n = 439 decisions) -> 'no adherence'
- manipulation check M0-d: follow rate 0.88 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.14 (n = 139 decisions) -> 'no adherence'
- manipulation check M2-d: follow rate 0.91 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.28 (n = 158 decisions)
- manipulation check M2-dx: follow rate 0.98 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.05 (n = 20 decisions) -> 'no adherence'

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 5 | 0.033 | 0.092 | 0.114 | 1.484 | 0.025 |  |  |  | 1 | 0 | 0.43 |
| K1-d | 6 | 0.999 | 0.001 | 0.001 | 1.918 | 0.984 | 0.85 | 0.002 | 0.002 | 0 | 0 | 0.62 |
| K10-d | 6 | 0.933 | 0.103 | 0.108 | 1.866 | 0.869 | 0.43 | 0.038 | 0.033 | 0 | 0 | 0.61 |
| K3-d | 6 | 0.995 | 0.007 | 0.007 | 1.908 | 0.963 | 0.60 | 0.009 | 0.006 | 0 | 0 | 0.61 |
| M0-a | 5 | 0.833 | 0.261 | 0.324 | 2.067 | 1.315 | 1.00 | 0.000 | 0.222 | 1 | 0 | 0.48 |
| M0-d | 6 | 0.383 | 0.472 | 0.496 | 1.635 | 0.359 | 0.88 | 0.044 | 0.102 | 0 | 0 | 1.19 |
| M1-a | 5 | 0.571 | 0.893 | 1.109 | 2.137 | 1.470 | 1.00 | 0.000 | 0.053 | 0 | 0 | 0.68 |
| M2-a | 5 | 0.907 | 0.183 | 0.228 | 1.870 | 0.878 | 1.00 | 0.000 | 0.000 | 0 | 0 | 0.67 |
| M2-d | 12 | 0.409 | 0.420 | 0.267 | 1.640 | 0.369 | 0.91 | 0.004 | 0.013 | 1 | 0 | 2.85 |
| M2-dx | 6 | 0.572 | 0.469 | 0.492 | 1.720 | 0.546 | 0.98 | 0.000 | 0.004 | 0 | 0 | 1.42 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.873 | 0.225 | +0.881 | 0.000 | 0.011 | 0.000 | 5/5 | 0.257 | 33 / 15 / 9 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.335 | 1.098 | +0.000 | 0.453 | 0.656 | 0.907 | 5/5 | 1.141 | 652 / 290 / 163 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.074 | 0.336 | -0.047 | 0.621 | 0.746 | 0.907 | 5/5 | 0.399 | 80 / 36 / 20 |
| 2 | H4 adherence remedy: discretionary vs auto-accept (hub) (M2-d − M2-a) | -0.498 | 0.312 | -0.759 | 0.004 | 0.111 | 0.012 | 12/5 | 0.410 | 165 / 74 / 42 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.38 (bootstrap 95% CI -0.22 to 1.32)
- M0-a: 0.08 (bootstrap 95% CI -0.21 to 0.37)
- M2-d: 0.57 (bootstrap 95% CI 0.27 to 0.84)
- M0-d: 0.60 (bootstrap 95% CI 0.16 to 0.98)
- M2-dx: 0.38 (bootstrap 95% CI -0.04 to 0.76)
