# Results: ladder-or-qwen

16 finished runs; spend $1.83.

## Gates

- baseline headroom: B0 Delta +0.150 (runs +0.02, +0.04, -0.01, +0.54); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 4/4 runs -> PASS
- harness: 3200 calls, 17 parse retries (0.53%), 0 refusals

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 4 | 0.150 | 0.263 | 0.419 | 1.519 | 0.102 |  |  |  | 1 | 0 | 0.39 |
| M0-a | 4 | 0.275 | 0.249 | 0.396 | 1.593 | 0.265 | 1.00 | 0.000 | 0.053 | 1 | 0 | 0.40 |
| M1-a | 4 | 0.278 | 0.370 | 0.588 | 1.584 | 0.245 | 1.00 | 0.000 | 0.052 | 8 | 0 | 0.52 |
| M2-a | 4 | 0.968 | 0.033 | 0.052 | 1.970 | 1.101 | 1.00 | 0.000 | 0.016 | 7 | 0 | 0.52 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.819 | 0.415 | +0.935 | 0.008 | 0.029 | 0.008 | 4/4 | 0.372 | 56 / 25 / 14 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.690 | 0.586 | -0.854 | 0.033 | 0.029 | 0.033 | 4/4 | 0.520 | 109 / 49 / 28 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.694 | 0.392 | -0.747 | 0.011 | 0.029 | 0.021 | 4/4 | 0.352 | 50 / 22 / 13 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.84 (bootstrap 95% CI 0.39 to 1.31)
- M0-a: 0.85 (bootstrap 95% CI 0.54 to 1.30)
