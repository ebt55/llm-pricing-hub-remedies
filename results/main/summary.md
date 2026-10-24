# Results: main

170 finished runs; spend $21.74.

## Gates

- mechanical control S-mono-a: Delta +1.000 (want ~1.0) -> PASS
- mechanical control D-BR-a: Delta +0.007 (want ~0.0) -> PASS
- baseline headroom: B0 Delta +0.062 (runs +0.09, +0.02, +0.04, +0.03, +0.07, -0.02, +0.06, +0.03, +0.06, +0.02, +0.03, +0.04, +0.25, +0.08, +0.03, +0.03, +0.15, -0.04, +0.25, +0.03); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 20/20 runs -> PASS
- harness: 41000 calls, 0 parse retries (0.00%), 0 refusals
- manipulation check R0-d: follow rate 0.84
- manipulation check R2-d: follow rate 0.78
- manipulation check M2-d: follow rate 0.37
- manipulation check S-nash: follow rate 0.70
- manipulation check S-mono: follow rate 0.02 (< 0.2: 'no adherence')

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0-cold | 5 | 0.109 | 0.066 | 0.083 | 1.505 | 0.071 |  |  |  | 0 | 0 | 0.44 |
| B0 | 20 | 0.062 | 0.076 | 0.036 | 1.494 | 0.047 |  |  |  | 0 | 0 | 1.78 |
| D-BR-a | 5 | 0.007 | 0.018 | 0.023 | 1.475 | 0.005 | 1.00 | 0.000 | 0.002 | 0 | 0 | 0.00 |
| M0-a | 20 | 0.352 | 0.286 | 0.134 | 1.593 | 0.265 | 1.00 | 0.000 | 0.048 | 0 | 0 | 1.74 |
| M1-a | 20 | 0.793 | 0.164 | 0.077 | 1.787 | 0.695 | 1.00 | 0.000 | 0.079 | 0 | 0 | 2.61 |
| M2-a | 20 | 0.989 | 0.013 | 0.006 | 1.922 | 0.992 | 1.00 | 0.000 | 0.020 | 0 | 0 | 2.40 |
| M2-d | 20 | 0.107 | 0.138 | 0.065 | 1.506 | 0.074 | 0.37 | 0.094 | 0.126 | 0 | 0 | 4.62 |
| R0-d | 5 | 0.061 | 0.071 | 0.089 | 1.491 | 0.040 | 0.84 | 0.005 | 0.013 | 0 | 0 | 0.88 |
| R2-a | 20 | -0.011 | 0.024 | 0.011 | 1.470 | -0.007 | 1.00 | 0.000 | 0.001 | 0 | 0 | 2.20 |
| R2-d | 20 | 0.072 | 0.137 | 0.064 | 1.503 | 0.067 | 0.78 | 0.011 | 0.011 | 0 | 0 | 4.14 |
| S-mono-a | 5 | 1.000 | 0.000 | 0.000 | 1.920 | 0.989 | 1.00 | 0.000 | 0.000 | 0 | 0 | 0.00 |
| S-mono | 5 | 0.066 | 0.052 | 0.065 | 1.501 | 0.062 | 0.02 | 0.419 | 0.000 | 0 | 0 | 0.48 |
| S-nash | 5 | 0.049 | 0.148 | 0.184 | 1.496 | 0.052 | 0.70 | 0.034 | 0.000 | 0 | 0 | 0.45 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1a client-aligned advisor, current data, auto-accept vs no advisor (R2-a − B0) | -0.074 | 0.035 | -0.051 | 0.000 | 0.000 | 0.000 | 20/20 | 0.050 | 6 / 3 / 2 |
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.927 | 0.034 | +0.954 | 0.000 | 0.000 | 0.000 | 20/20 | 0.048 | 5 / 3 / 2 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.196 | 0.072 | -0.159 | 0.000 | 0.000 | 0.000 | 20/20 | 0.103 | 22 / 10 / 6 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.637 | 0.125 | -0.688 | 0.000 | 0.000 | 0.000 | 20/20 | 0.179 | 65 / 29 / 17 |
| 2 | H4 adherence remedy: discretionary vs auto-accept (hub) (M2-d − M2-a) | -0.882 | 0.061 | -0.949 | 0.000 | 0.000 | 0.000 | 20/20 | 0.087 | 16 / 7 / 4 |
| 2 | H4c adherence, client-aligned advisor (R2-d − R2-a) | +0.083 | 0.061 | +0.046 | 0.015 | 0.000 | 0.029 | 20/20 | 0.087 | 16 / 7 / 4 |
| 2 | H5 firms follow a cartel-level vs Nash-level static number (S-mono − S-nash) | +0.017 | 0.138 | +0.047 | 0.821 | 0.151 | 0.821 | 5/5 | 0.197 | 20 / 9 / 5 |
| c | placebo: client advisor without competitor data vs no advisor (R0-d − B0) | -0.001 | 0.071 | +0.002 | 0.978 | 0.921 | 0.978 | 5/20 | 0.101 | 9 / 4 / 3 |
| c | context: cold start vs competitive history (B0-cold − B0) | +0.046 | 0.067 | +0.070 | 0.218 | 0.129 | 0.436 | 5/20 | 0.096 | 9 / 4 / 3 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.21 (bootstrap 95% CI 0.14 to 0.29)
- M0-a: 0.69 (bootstrap 95% CI 0.55 to 0.82)
- M2-d: 0.95 (bootstrap 95% CI 0.88 to 1.02)
