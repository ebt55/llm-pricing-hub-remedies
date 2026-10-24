# Stale Data Isn't Enough: Only Ending Auto-Accept Stops an LLM Pricing Hub

*Testing the RealPage settlement's remedies on LLM pricing advisors. Apart Research AI Collusion Research Sprint, October 2026.*

**Question.** The DOJ's settlement with RealPage limits what a shared pricing advisor may use: no competitors' current non-public data at runtime, training data at least 12 months old, and no reporting narrower than state level. The complaints also targeted auto-accept. Do these remedies stop an LLM pricing advisor whose objective is aligned with the whole market, the incentive alleged against RealPage?

**Main findings** (Claude Haiku 5.5, n = 20 per arm unless noted; details in [report/draft.md](report/draft.md)):

1. **The hub causes the harm.** A market-aligned hub drives a competitive market to joint monopoly (profit gain Δ 0.06 → 0.99). An advisor that serves only its own client is pro-competitive (Δ −0.01).
2. **Data remedies leave most of the harm.**
   - Stale competitor data removes 21% of it.
   - A market average removes none (triopoly).
   - A full data ban removes 69% for Haiku but ~0–10% for DeepSeek and the Gemini models.
   - A scripted rational hub with no data still raises prices, so the ban binds only hubs that under-optimise.
3. **Only *ending* auto-accept works.** It removes 95% of the harm. At 50%, 80% and 90% acceptance, 73%, 90% and 94% of the harm remains.
4. **Coordination needs no instruction.** Advice to "avoid a race to the bottom", with no joint objective, also raises prices (Δ 0.45 without rival data).
5. **Robustness.** The results hold under demand noise, without the prompt's price-ceiling cue, at higher reasoning effort, and over 200 rounds. With one-sided adoption, the hub only hurts its own client.
6. **Detection.** The price-level screen catches outcomes. The classic variance screen fails (AUROC 0.36). A reasoning monitor catches the hub's *stated* intent, but also flags honest advisors that watch rivals.

## Repository

| Path | What |
|---|---|
| `advisor/` | Market (`market.py`), model providers with spend caps (`providers.py`), prompts (`prompts.py`), arm definitions (`arms.py`), game loop (`game.py`) |
| `run.py` | Runs arms × seeds in parallel from a TOML config; resumable; prints a cost estimate |
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
