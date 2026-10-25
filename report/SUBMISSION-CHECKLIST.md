# Submission checklist (for Mon 26 Oct; target 15:30 IST, hard deadline 17:29 IST)

## Needs you

1. **Review the decisions Fable 5.1 made overnight** (SPRINT_LOG, entries from 03:22 to 05:04):
   - the ratchet tests;
   - the final title;
   - the draft-v5 edits.
2. **Your name and affiliation.** Line 5 of `report/draft.md` currently says "Ebin [full name and affiliation: author to confirm]".
3. **Copy the draft into the official template** and place the figures so they fill each page. The renderer leaves gaps because figures jump to the next page. Without the gaps, the main text is about 7.8 pages.
   - Template: https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing
   - Main text: title to Limitations in `report/draft.md`.
   - Figures: `report/figures/fig1_remedy_ladder.png`, `fig2_cross_model.png`, `fig3_ratchet.png`.
   - Appendices:
     - A: `appendix-prompts.md`;
     - E: `appendix-limitations-dual-use.md`;
     - F: `appendix-tables.md`, with `figA1_adherence_dose.png`.
4. **Make the repo public, then check the link in a private window:**
   ```bash
   gh repo edit ebt55/llm-pricing-hub-remedies --visibility public --accept-visibility-change-consequences
   ```
5. **Submit the form** (summary text below). Pick every track that fits; Track 1 is the main one. Slides and a video are optional.

## Done (check if you like)

- [x] Abstract: 238 words, with numbers, n and CIs.
- [x] Variance, seeds and baselines reported; positive and mechanical controls in §4.1.
- [x] Pre-registration: freeze commit `5aa9f79` for the main batch; every later batch is logged with a prediction before its run.
- [x] Appendix "Limitations and Dual Use" (E).
- [x] Pre-existing code statement (Appendix D). No code predates the sprint, and no starter-repo file is included or modified.
- [x] References section with URLs.
- [x] Every number traces to `results/` via `analyze.py`, `tools/ratchet_curve.py` and `tools/token_table.py`.

## Still open at the time of writing

- **GPT-5.4 mini row (§4.2).** It runs on the free daily allowance from 05:30 IST. If it is not complete by Mon 14:00 IST, delete the row and say "not completed" in Appendix D.
- **Total cost:** filled in (about $110; $107.65 logged per call). Add the GPT-5.4 mini calls once they finish ($0, free tier).
- **References to double-check** (from `report/related-work.md`):
  - Abrantes-Metz et al. (2006): the volume and pages are from memory.
  - The *Gibson* and *Cornish-Adebiyi* holdings come from law-firm summaries; the opinions were not fetched.
  - Berger et al. (2025): it's unclear whether the full text or only the abstract was read.
  - Riemer et al. (2026): the arXiv-to-OpenReview match rests on identical title and authors.

## Form summary (short)

> We test whether the remedies in the DOJ's 2026 RealPage Final Judgment stop an LLM pricing hub that is told to maximise its clients' combined profit, in a repeated Bertrand duopoly (666 runs, seven models from six labs, pre-registered main batch).
>
> - **Data bans** remove 69–92% of the hub's harm on three models and ≤ 10% on two.
> - **Auto-accept within ±1–3% per round** keeps all of it (Haiku).
> - **Firm discretion** works only when firms refuse small nudges.
>
> A scripted 1-cent-per-round ratchet leaves Haiku firms competitive but walks Qwen and Gemini firms most or all of the way to monopoly. Remedies should target the advisor's objective and audit acceptance and outcomes. Code, logs and every pre-registration: https://github.com/ebt55/llm-pricing-hub-remedies
