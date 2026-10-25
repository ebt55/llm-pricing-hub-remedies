# Results: ladder-gem-lite-hi

18 finished runs; spend $9.49.

## Gates

- baseline headroom: B0 Delta +0.051 (runs +0.03, +0.14, -0.01); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 3/3 runs -> PASS
- harness: 4800 calls, 0 parse retries (0.00%), 0 refusals
- manipulation check M2-d: follow rate 0.83 (last rounds); follow rate when the recommendation moves the price by > $0.05: 0.21 (n = 34 decisions)

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 3 | 0.051 | 0.078 | 0.195 | 1.488 | 0.032 |  |  |  | 0 | 0 | 0.96 |
| K1-d | 6 | 1.000 | 0.000 | 0.000 | 1.918 | 0.986 | 0.85 | 0.002 | 0.000 | 0 | 0 | 1.74 |
| M2-a | 3 | 0.983 | 0.023 | 0.058 | 1.967 | 1.092 | 1.00 | 0.000 | 0.007 | 0 | 0 | 1.78 |
| M2-d | 6 | 0.998 | 0.002 | 0.002 | 1.931 | 1.013 | 0.83 | 0.004 | 0.010 | 0 | 0 | 5.02 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.933 | 0.177 | +0.969 | 0.001 | 0.100 | 0.001 | 3/3 | 0.132 | 6 / 3 / 2 |
| 2 | H4 adherence remedy: discretionary vs auto-accept (hub) (M2-d − M2-a) | +0.015 | 0.058 | +0.003 | 0.383 | 0.095 | 0.383 | 6/3 | 0.038 | 1 / 1 / 1 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M2-d: -0.02 (bootstrap 95% CI -0.05 to -0.00)
