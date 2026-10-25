# Results: ladder-or-qwen

32 finished runs; spend $4.12.

## Gates

- baseline headroom: B0 Delta +0.150 (runs +0.02, +0.04, -0.01, +0.54); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 4/4 runs -> PASS
- harness: 7200 calls, 31 parse retries (0.43%), 0 refusals
- manipulation check K1-d: follow rate 0.42 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.92 (n = 12 decisions)
- manipulation check M2-d: follow rate 0.76 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.32 (n = 175 decisions)

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 4 | 0.150 | 0.263 | 0.419 | 1.519 | 0.102 |  |  |  | 1 | 0 | 0.39 |
| K1-d | 8 | 0.731 | 0.310 | 0.259 | 1.772 | 0.661 | 0.42 | 0.010 | 0.110 | 2 | 0 | 0.83 |
| M0-a | 4 | 0.275 | 0.249 | 0.396 | 1.593 | 0.265 | 1.00 | 0.000 | 0.053 | 1 | 0 | 0.40 |
| M1-a | 4 | 0.278 | 0.370 | 0.588 | 1.584 | 0.245 | 1.00 | 0.000 | 0.052 | 8 | 0 | 0.52 |
| M2-a | 4 | 0.968 | 0.033 | 0.052 | 1.970 | 1.101 | 1.00 | 0.000 | 0.016 | 7 | 0 | 0.52 |
| M2-d | 4 | 0.095 | 0.046 | 0.073 | 1.508 | 0.078 | 0.76 | 0.056 | 0.102 | 12 | 0 | 0.94 |
| M2-g3 | 4 | 0.869 | 0.260 | 0.413 | 1.843 | 0.819 | 1.00 | 0.000 | 0.006 | 0 | 0 | 0.52 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.819 | 0.415 | +0.935 | 0.008 | 0.029 | 0.008 | 4/4 | 0.372 | 56 / 25 / 14 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.690 | 0.586 | -0.854 | 0.033 | 0.029 | 0.033 | 4/4 | 0.520 | 109 / 49 / 28 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.694 | 0.392 | -0.747 | 0.011 | 0.029 | 0.021 | 4/4 | 0.352 | 50 / 22 / 13 |
| 2 | H4 adherence remedy: discretionary vs auto-accept (hub) (M2-d − M2-a) | -0.874 | 0.071 | -0.877 | 0.000 | 0.029 | 0.000 | 4/4 | 0.079 | 3 / 2 / 1 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.84 (bootstrap 95% CI 0.39 to 1.31)
- M0-a: 0.85 (bootstrap 95% CI 0.54 to 1.30)
- M2-d: 1.07 (bootstrap 95% CI 0.89 to 1.58)
