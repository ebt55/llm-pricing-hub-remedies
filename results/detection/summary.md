# Detection: main, robust-nowtp

200 runs; positives (market-aligned hub) = 110; supra-competitive (Delta > 0.3) = 77.

| detector | AUROC hub vs not | TPR @ 5% FPR (hub) | AUROC: compliant hubs (M1-a, M0-a) vs non-hub | AUROC: supra-competitive outcome | flag rate in M0-a runs that stayed competitive (Delta <= 0.3) |
|---|---|---|---|---|---|
| price_screen | 0.904 | 0.72 | 0.945 | 1.000 | 0.18 (n=17) |
| variance_screen | 0.359 | 0.03 | 0.283 | 0.329 | 0.06 (n=17) |
| monitor_full | 0.994 | 0.96 | 0.989 | 0.833 | 0.88 (n=17) |
| monitor_visible | 0.993 | 0.96 | 0.988 | 0.880 | 0.88 (n=17) |

Per-arm mean scores:

| arm     |   price_screen |   variance_screen |   monitor_full |   monitor_visible |   delta |
|:--------|---------------:|------------------:|---------------:|------------------:|--------:|
| B0      |          0.048 |            -0.02  |         18.467 |            11.467 |   0.065 |
| B0-cold |          0.071 |            -0.017 |         11.2   |             8.8   |   0.109 |
| M0-a    |          0.241 |            -0.022 |         84.533 |            84.633 |   0.33  |
| M1-a    |          0.643 |            -0.042 |         89.133 |            90     |   0.756 |
| M2-a    |          0.995 |            -0.016 |         90.167 |            91.6   |   0.991 |
| M2-d    |          0.074 |            -0.019 |         91     |            89.4   |   0.107 |
| R0-d    |          0.04  |            -0.014 |         13.8   |             8.6   |   0.061 |
| R2-a    |         -0.007 |            -0.002 |         66.45  |            60.55  |  -0.011 |
| R2-d    |          0.067 |            -0.022 |         57.1   |            54.45  |   0.072 |
| S-mono  |          0.062 |            -0.048 |          8     |             8.4   |   0.066 |
| S-nash  |          0.052 |            -0.042 |         10.4   |            13.2   |   0.049 |
