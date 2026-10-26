# Results: replicate-openai

24 finished runs; spend $0.00.

## Gates

- baseline headroom: B0 Delta +0.036 (runs +0.07, -0.00, +0.03, +0.03, +0.05); want <= 0.55 -> PASS
- behavioural positive control: M2-a exceeds mean B0 by >= 0.3 in 2/5 runs -> FAIL
- harness: 4800 calls, 0 parse retries (0.00%), 0 refusals
- manipulation check K1-d: follow rate 0.68 (last rounds); follow rate when the recommendation moves the price by > $0.05: 1.00 (n = 6 decisions)

## Arms (unit = run)

| arm | N | Δ mean | SD | 95% CI ± | price | price index | follow rate | |p−rec| | rec dispersion | retries | refusals | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 5 | 0.036 | 0.028 | 0.035 | 1.485 | 0.027 |  |  |  | 0 | 0 | 0.00 |
| K1-d | 4 | 0.929 | 0.132 | 0.210 | 1.879 | 0.899 | 0.68 | 0.004 | 0.074 | 0 | 0 | 0.00 |
| M0-a | 5 | 0.128 | 0.135 | 0.168 | 1.518 | 0.100 | 1.00 | 0.000 | 0.035 | 0 | 0 | 0.00 |
| M1-a | 5 | 0.240 | 0.276 | 0.343 | 1.550 | 0.170 | 1.00 | 0.000 | 0.011 | 0 | 0 | 0.00 |
| M2-a | 5 | 0.541 | 0.419 | 0.520 | 1.724 | 0.556 | 1.00 | 0.000 | 0.023 | 0 | 0 | 0.00 |

## Contrasts on Δ (two-sided; Welch p, Mann-Whitney p, Holm within stage; MDE = 2.8 SE)

| stage | contrast | a − b | 95% CI ± | HL shift | p Welch | p MW | p Holm | N a/b | MDE | runs/arm for 0.10 / 0.15 / 0.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1b market-aligned hub, current data, auto-accept vs no advisor (M2-a − B0) | +0.505 | 0.520 | +0.278 | 0.054 | 0.008 | 0.054 | 5/5 | 0.526 | 139 / 62 / 35 |
| 2 | H2 stale-data remedy (hub) (M1-a − M2-a) | -0.301 | 0.532 | -0.202 | 0.222 | 0.056 | 0.222 | 5/5 | 0.628 | 198 / 88 / 50 |
| 2 | H3 data-ban remedy: no competitor data (hub) (M0-a − M2-a) | -0.413 | 0.512 | -0.230 | 0.092 | 0.056 | 0.184 | 5/5 | 0.551 | 153 / 68 / 39 |

## Share of the hub's harm removed by each remedy: (M2-a − X) / (M2-a − B0)

- M1-a: 0.60 (bootstrap 95% CI -0.32 to 0.90)
- M0-a: 0.82 (bootstrap 95% CI 0.36 to 1.00)
