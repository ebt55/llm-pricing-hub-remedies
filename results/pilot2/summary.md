# Results: pilot2

39 finished runs; spend $4.23.

## Gates

- mechanical control S-mono-a: Delta +1.000 (want ~1.0) -> PASS
- mechanical control D-BR-a: Delta +0.020 (want ~0.0) -> PASS
- baseline headroom: B0 Delta +0.081 (runs +0.05, +0.15, +0.05); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 3/3 runs -> PASS
- harness: 8400 calls, 0 parse retries (0.00%), 0 refusals
- manipulation check R0-d: follow rate 0.90
- manipulation check R2-d: follow rate 0.86
- manipulation check M2-d: follow rate 0.36
- manipulation check S-nash: follow rate 0.90
- manipulation check S-mono: follow rate 0.01 (< 0.2: 'no adherence')

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0-cold | 3 | 0.072 | 0.082 | 0.204 | 1.494 | 0.046 |  |  |  | 0 | 0 | 0.26 |
| B0 | 3 | 0.081 | 0.059 | 0.147 | 1.500 | 0.061 |  |  |  | 0 | 0 | 0.27 |
| D-BR-a | 3 | 0.020 | 0.011 | 0.027 | 1.478 | 0.012 | 1.00 | 0.000 | 0.003 | 0 | 0 | 0.00 |
| M0-a | 3 | 0.226 | 0.220 | 0.546 | 1.548 | 0.167 | 1.00 | 0.000 | 0.035 | 0 | 0 | 0.26 |
| M1-a | 3 | 0.839 | 0.095 | 0.237 | 1.817 | 0.762 | 1.00 | 0.000 | 0.100 | 0 | 0 | 0.40 |
| M2-a | 3 | 0.989 | 0.006 | 0.015 | 1.942 | 1.039 | 1.00 | 0.000 | 0.016 | 0 | 0 | 0.34 |
| M2-d | 3 | 0.071 | 0.083 | 0.207 | 1.497 | 0.053 | 0.36 | 0.128 | 0.189 | 0 | 0 | 0.69 |
| R0-d | 3 | 0.015 | 0.017 | 0.042 | 1.482 | 0.020 | 0.90 | 0.008 | 0.009 | 0 | 0 | 0.51 |
| R2-a | 3 | -0.013 | 0.003 | 0.007 | 1.469 | -0.008 | 1.00 | 0.000 | 0.001 | 0 | 0 | 0.31 |
| R2-d | 3 | 0.036 | 0.032 | 0.080 | 1.484 | 0.025 | 0.86 | 0.005 | 0.005 | 0 | 0 | 0.62 |
| S-mono-a | 3 | 1.000 | 0.000 | 0.000 | 1.920 | 0.989 | 1.00 | 0.000 | 0.000 | 0 | 0 | 0.00 |
| S-mono | 3 | 0.023 | 0.076 | 0.190 | 1.487 | 0.032 | 0.01 | 0.433 | 0.000 | 0 | 0 | 0.29 |
| S-nash | 3 | 0.004 | 0.003 | 0.008 | 1.487 | 0.031 | 0.90 | 0.018 | 0.000 | 0 | 0 | 0.27 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1a client-aligned advisor, current data, auto-accept vs no advisor (R2-a − B0) | -0.094 | 0.067 | -0.062 | 0.110 | 0.100 | 0.110 | 3/3 | 0.095 | 3 / 2 / 1 |
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.909 | 0.067 | +0.937 | 0.001 | 0.100 | 0.003 | 3/3 | 0.096 | 3 / 2 / 1 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.150 | 0.108 | -0.147 | 0.112 | 0.100 | 0.335 | 3/3 | 0.154 | 8 / 4 / 2 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.763 | 0.249 | -0.876 | 0.026 | 0.100 | 0.106 | 3/3 | 0.355 | 38 / 17 / 10 |
| 2 | H4 adherence remedy: discretionary vs auto-accept (hub) (M2-d − M2-a) | -0.918 | 0.095 | -0.963 | 0.003 | 0.100 | 0.013 | 3/3 | 0.135 | 6 / 3 / 2 |
| 2 | H4c adherence, client-aligned advisor (R2-d − R2-a) | +0.049 | 0.037 | +0.044 | 0.118 | 0.100 | 0.335 | 3/3 | 0.052 | 1 / 1 / 1 |
| 2 | H5 firms follow a cartel-level vs Nash-level static number (S-mono − S-nash) | +0.019 | 0.086 | -0.019 | 0.706 | 0.700 | 0.706 | 3/3 | 0.123 | 5 / 3 / 2 |
| c | placebo: client advisor without competitor data vs no advisor (R0-d − B0) | -0.065 | 0.069 | -0.042 | 0.188 | 0.100 | 0.376 | 3/3 | 0.099 | 3 / 2 / 1 |
| c | context: cold start vs competitive history (B0-cold − B0) | -0.009 | 0.115 | +0.006 | 0.889 | 1.000 | 0.889 | 3/3 | 0.164 | 9 / 4 / 3 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.17 (bootstrap 95% CI 0.06 to 0.27)
- M0-a: 0.84 (bootstrap 95% CI 0.56 to 1.02)
- M2-d: 1.01 (bootstrap 95% CI 0.90 to 1.11)
