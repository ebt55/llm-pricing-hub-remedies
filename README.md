# An LLM Pricing Hub Survives Data Limits on Some Models; Firm Discretion Works Only When Firms Refuse Small Nudges

*Pre-registered tests of the RealPage Final Judgment's remedies (data bans, stale data, parameterised auto-accept, firm discretion) on LLM pricing advisors from six labs. Apart Research AI Collusion Research Sprint, October 2026.*

**Question.** The DOJ's settlement with RealPage limits what a shared pricing advisor may use: no competitors' current non-public data at runtime, training data at least 12 months old, and no reporting narrower than state level. The complaints also targeted auto-accept. Do these remedies stop an LLM pricing advisor whose objective is aligned with the whole market, the incentive alleged against RealPage?

**Main findings** (details in [report/draft.md](report/draft.md); Claude Haiku 5.5 with n = 20 per arm unless noted; more than 700 runs on seven models):

1. **The hub causes the harm.** A market-aligned hub drives a competitive market to joint monopoly (profit gain Δ 0.06 → 0.99). An advisor that serves only its own client is pro-competitive (Δ −0.01).
2. **Data limits help unevenly.** A competitor-data ban removes:
   - 85% of the harm for Qwen3.8 Flash (n = 4);
   - 69% for Haiku;
   - ≤ 10% for DeepSeek V4.1 Flash and Gemini 3.5 Flash-Lite.

   Stale data removes 21% for Haiku, and a market average removes none. A scripted rational hub with no data still raises prices.
3. **Guardrails and partial adherence keep the harm.** Auto-accept within ±1–3% per round, the Final Judgment's "user-set parameters", retains all of it on Haiku and 88% on Qwen, and only delays monopoly (Haiku: round 4 → 8–19). At 50–90% acceptance, 73–94% remains.
4. **Firm discretion works only when firms refuse small nudges.** We swap in a scripted recommender that adds 1 cent per round:
   - Haiku firms stay competitive (Δ 0.05).
   - Gemini Flash-Lite firms follow it to monopoly (Δ 1.00), with or without thinking.

   With an LLM hub, discretion removes 95% of the harm for Haiku and 57% for Gemini Flash-Lite. Stacking the data ban on top, or showing firms the cumulative drift, doesn't fix the Gemini case.
5. **Coordination needs no joint instruction.** Advice to "avoid a race to the bottom" also raises prices (Δ 0.45 without rival data, n = 10).
6. **Detection.** The price-level screen catches outcomes (AUROC 0.90). Two classic instruments point the wrong way: the variance screen (0.36), and a monitor of single price moves, which ranks the hub's guardrailed and ratcheting climbs as *less* suspicious than honest play (0.05–0.22). A reasoning monitor catches the hub's *stated* intent, but also flags honest advisors that watch rivals.

## Repository

| Path | What |
|---|---|
| `advisor/` | Market (`market.py`), model providers with spend caps (`providers.py`), prompts (`prompts.py`), arm definitions (`arms.py`), game loop (`game.py`) |
| `run.py` | Runs arms × seeds in parallel from a TOML config; resumable; prints a cost estimate |
| `tools/` | `ratchet_curve.py` (acceptance by recommended step), `token_table.py` (measured reasoning budget per model), `pack_thoughts.py` |
| `analyze.py` | Per-arm tables, pre-registered contrasts (Welch t, Mann-Whitney, Holm), MDE, share of harm removed, gate checks |
| `detect.py` | Detection add-on: cartel screens and the reasoning monitor, scored against ground truth |
| `figures.py` | Paper figures, written to `report/figures/` |
| `configs/` | One TOML per batch (pilot, main, robustness, follow-up, ladder, replications) |
| `results/<batch>/<arm>/s<seed>.jsonl` | One run per file: config line, one line per round, summary. Model reasoning is in `*.thoughts.jsonl.gz` |
| `report/` | Draft, appendices (prompts; limitations and dual use), figures |
| `SPRINT_LOG.md` | **Provenance and pre-registration:** idea origin, independence from concurrent work, every design decision and batch logged before its results |
| `notes/` | Lab notebook and the confound watch |
| `docs/` | Plain-language summary and FAQ |

## Reproduce

```bash
uv sync
cp .env.example .env                    # add the keys for the providers you want
uv run python tests/test_market.py      # benchmarks vs the llm-cartel starter code
uv run python run.py --config configs/smoke.toml --dry       # $0 dry run with mock models
uv run python run.py --config configs/main.toml              # main batch (~$22 on Claude Haiku 5.5)
uv run python analyze.py main
uv run python figures.py
```

Every run prints a cost estimate and asks before spending (`-y` skips the prompt). Per-provider spend caps are set in `advisor/providers.py`.

## Attribution and provenance

- **Built on:** the market parametrisation (Calvano et al. 2020), the P0 firm prompt (Fish et al. 2024) and the history-table format, all via the sprint's `llm-cartel` starter code (Riemer et al. 2026). The market is re-implemented and tested against it. `SPRINT_LOG.md` lists exactly what was reused, and the two benchmark bugs we found in the starter code.
- **Concurrent sprint work:** zerocommcartel (2026) studies a different variable (what firms are told about rivals' advisors) in a one-shot Cournot game. We used none of its code or prompts; see `SPRINT_LOG.md`.
- **Tooling:** written with Claude Code (Claude Opus 5.5). Reviews by independent Claude Fable 5.1 subagents are logged in `SPRINT_LOG.md`.
