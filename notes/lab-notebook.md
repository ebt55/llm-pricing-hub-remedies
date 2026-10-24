# Lab notebook

*Working notes, newest at the bottom, times in IST. SPRINT_LOG.md is the formal record (provenance and pre-registration). This file holds observations and hunches as they come. Confounds are tracked in [confounds.md](confounds.md).*

## Sat 24 Oct

**22:50 Harness built**
- Mock dry runs pass.
- Two bugs found in the llm-cartel starter code:
  - the triopoly monopoly price;
  - the α ≠ 1 benchmarks.

**23:15 Smoke tests**
- Haiku is clean.
- DeepSeek thinking runs long, and returns empty answers at a 4096-token cap.
- Haiku firms jump to ~1.95 at once.

**23:20 Diagnostics**
- The jump is the midpoint of cost and willingness to pay: firms price as monopolists because they don't know a rival exists.
- Ten rounds of competitive history keep B0 near Nash.
- Fable 5.1's review recommended a market-aligned hub as the harm case, which became design v2.

**23:27–23:50 pilot2**

| | |
|---|---|
| Runs | 39 |
| Cost | $4.23 |
| Failures | 0 |
| B0 | 0.08 |
| M2-a | 0.99 |
| M1-a (stale) | 0.84 (removes 17%) |
| M0-a (data ban) | 0.23 (removes 84%, noisy) |
| M2-d (optional advice) | 0.07 (removes ~100%) |
| R2-a (client advisor) | −0.01 (pro-competitive) |

- With the competitor sentence, a cold start no longer jumps (B0-cold ≈ B0).

## Sun 25 Oct

**~00:00 Design freeze (commit `5aa9f79`)**
- The main batch launched with n = 20 primary arms and n = 5 controls, plus the triopoly stretch at n = 10.
- Replications launched in parallel: OpenAI gpt-5.4-mini (n = 5) and DeepSeek flash (n = 3).

**~00:05 Read the hub's reasoning in pilot2**

How the hub thinks:
- It fits a linear demand curve using **$2.89 as the choke price**, so its monopoly estimate (~1.94) comes partly from the prompt's willingness-to-pay line (confound C1).
- With current or stale competitor data, it raises prices early from theory, then holds them once the data confirms the rival is high. Data is used to **confirm**, not to discover (C4).
- Without competitor data (M0-a), it stays cautious for most of the run: "deviating upward risks losing volume to a competitor". One run creeps up late, inferring "tacit" joint raises from its own quantities (C3).
- It calls its own target "combined collusive profit", which makes text-based detection trivial in M arms (C7).

**Next:** after the main batch, run the C1 robustness (no willingness-to-pay line) and the C3 long horizon.

**~00:25 Main batch nearly done** (167/170 runs; n = 20 primary arms; 39,800 calls; 0 retries; 0 refusals; $21)

All controls pass:
- S-mono-a: Δ 1.00;
- D-BR-a: Δ 0.01;
- B0: Δ 0.06;
- M2-a beats B0 by ≥ 0.3 in 20/20 runs.

| Arm | Δ | Harm removed | Reading |
|---|---|---|---|
| R2-a (client advisor, current data) | −0.01 | — | **Pro-competitive** (below B0, p < .001) |
| M2-a (hub, current data) | 0.99 | — | Harm: **+0.93 vs B0** |
| M1-a (hub, stale data) | 0.79 | **21% (CI 14–29%)** | Compliant collusion holds |
| M0-a (hub, no competitor data) | 0.35 (SD 0.29) | **69% (CI 55–82%)** | Lower than the pilot's 84%; the data ban leaves about a third of the harm |
| M2-d (hub, optional advice) | 0.11 | **95% (CI 87–103%)** | |
| S-mono vs S-nash | — | — | Firms ignore a static cartel-level number (follow rate 0.02) |

**Triopoly stretch** (n = 10): **aggregated data (M3-3a) removes nothing.** Δ is 0.98 vs 0.92 for per-firm data, and B0-3 is 0.05. A market-wide average is enough for the hub to coordinate. That cuts against the "no reporting narrower than state level" remedy (caveat: our aggregate is market-level, not state-level).

**Confound C1 (no willingness-to-pay line, n = 10): the effects survive.**
- M2-a: 0.99.
- M1-a: 0.68, so stale data removes 34% (CI 20–50%).
- M0-a: 0.29, so the ban removes 77% (CI 60–92%).
- The anchor slightly helps the stale-data hub coordinate, but it isn't the cause.

**"Too good" check.** The hub's effect is near-total by construction: it is told to maximise joint profit, and auto-accept passes its price straight through (C2). That is the *harm case*, not a finding.

The findings are the remedy contrasts, and those are mixed, not too clean:
- stale data fails;
- the data ban is partial;
- aggregation fails;
- only removing auto-accept works.

The suspiciously clean one is M2-d (C6: our firms are cautious). Still to check:
- C3, long horizon (running);
- cross-family replications (DeepSeek running; OpenAI at 05:30).

**~00:30 Confound C3: long horizon (200 rounds, n = 5; last 20 rounds)**

| Arm | Δ at 200 rounds | Δ at 100 rounds (main batch) |
|---|---|---|
| B0 | 0.05 | 0.06 |
| M1-a (stale data) | 0.87 | 0.79 |
| M0-a (data ban) | 0.44 (SD 0.46) | 0.35 |

- **M0-a is bimodal.** Some runs reach cartel prices and others stay near Nash.
- **Reading:** the data ban **delays** coordination rather than preventing it. Over a longer horizon, more no-data hubs infer that the rival is following (from their own quantities) and climb.
- Stale data gets slightly *more* harmful with time.
- **For the paper:** report "harm removed" as horizon-dependent. The 100-round figures (21% and 69%) are upper bounds on what these remedies achieve.

**~00:45 Main batch complete** (170/170 runs, 41,000 calls, 0 retries, 0 refusals, $21.74). Final numbers match the ~00:25 entry.
- M2-d final: Δ 0.11, removes 95% (CI 88–102%).
- Figures: `results/main/fig_delta_by_arm.png`, `results/main/fig_price_paths.png`.

**~00:45 DeepSeek replication** (n = 3, $2.95, 0.5% parse retries, 0 refusals). The model ID stayed `deepseek-flash` on every call.

| Arm | Δ by run | Harm removed |
|---|---|---|
| B0 | 0.27, 0.13, 0.17 | — |
| M2-a | 1.00, 1.00, 1.00 | — |
| M1-a (stale data) | 1.00, 1.00, 0.88 | 5% |
| M0-a (data ban) | 0.97, 0.94, 0.66 | **18%** |

**The striking part: DeepSeek's no-data hub reaches cartel prices anyway.** A stronger reasoner with a joint objective computes the joint-monopoly price, assumes a symmetric rival, and posts it, so no data is needed. Haiku's no-data hub is more cautious (69% removed at 100 rounds, decaying by 200).

- **Implication:** the data ban's effect depends on the model. Data remedies don't touch the actual driver, which is the hub's *objective* together with auto-accept.
- **Robust remedy so far:** only removing auto-accept, i.e. letting firms decide.

**Follow-up:** DeepSeek extended to n = 8 for B0, M0-a and M1-a (seeds 303–307, about $3.4, lifetime spend kept under $9.50).

**Housekeeping:** reasoning sidecars of finished runs are gzipped (`tools/pack_thoughts.py`); results are now about 50 MB.

**~01:00 Detection add-on** (`detect.py`, `results/detection/`)
- 200 runs (main batch plus the no-willingness-to-pay batch). The mechanical controls are excluded because no AI acts in them.
- Labels: positive = market-aligned hub (110 runs).

| Detector | AUROC (hub vs not) | TPR at 5% FPR | AUROC (compliant hubs only) | Note |
|---|---|---|---|---|
| Price screen (price index) | 0.90 | 0.72 | 0.95 | Catches the *outcome*; misses hubs a remedy held back (M2-d, most of M0-a) |
| Variance screen (Abrantes-Metz et al. 2006) | 0.36 | 0.03 | — | **Fails.** LLM-cartel prices are not less variable than competitive ones here |
| Reasoning monitor, full notes (Haiku judge) | 0.99 | 0.96 | — | Catches *intent*, even in hubs that stayed competitive (88% flagged) |
| Reasoning monitor, stated reason only | 0.99 | 0.96 | — | Same |

**Two caveats that belong in the paper:**
- **C7, the easy case.** The hub's objective is explicit, and it says "joint profit", so a text monitor's job is trivial. A hub whose objective is implicit (for example, learned from pooled outcomes) would not announce it. We did not build that case: it would be detection-evasion work, a dual-use concern.
- **False alarms on rival-aware honest advisors.** Client-only advisors that see the rival's current data score 55–66 out of 100, against ~10–18 for B0 and the static arms, although their prices are competitive (Δ ≈ 0). Monitors confuse "uses competitor data" with "coordinates".

**Independence.** We deliberately avoided a best-response-gap detector, because zerocommcartel's issue #33 lists "best-response consistency" audits. We use classic economic screens plus a generic CoT/reasoning monitor, and evaluate them against ground-truth labels in a repeated market.
