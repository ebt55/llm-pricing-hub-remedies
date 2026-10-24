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
