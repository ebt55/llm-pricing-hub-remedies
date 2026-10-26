# Submission checklist (for Mon 26 Oct; target 15:30 IST, hard deadline 17:29 IST)

## Needs you

1. **Review the decisions Fable 5.1 made overnight** (SPRINT_LOG, entries from 03:22 to 05:04):
   - the ratchet tests;
   - the final title;
   - the draft-v5 edits.
2. **Your name and affiliation.** Line 5 of `report/draft.md` currently says "Ebin [full name and affiliation: author to confirm]".
3. **Copy the draft into the official template** and place the figures so they fill each page. The renderer leaves gaps because figures jump to the next page. Without the gaps, the main text is about 7.8 pages.
   - Template: https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing
   - **Paste-ready:** run `python tools/render_pdf.py` (it writes `report/draft.html` and `report/draft.pdf`). Open `draft.html` in Chrome, select from the title to the end of References, copy, and paste into the template. Headings, bold, lists and tables survive the paste. Insert the three figures by hand at their captions. `draft.pdf` is a preview: the whole draft, references included, comes to 8 pages.
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
5. **Submit the form** (summary text below). Pick every track that fits; Track 1 is the main one.
   - **Slides:** https://claude.ai/artifact/K6U988h9poQFMKiNaQPbCU (9 slides; speaker notes on each). The deck is private until you share it from its Share menu. You can also download it as PowerPoint or PDF from Share › Export.
   - **Title image:** `report/figures/fig3_ratchet.png`.
   - **Video (optional):** read `report/video-script.md` (about 4 minutes) over the slides.

## Monday morning (Claude, after the 05:30 GPT-5.4 mini runs): done 05:48 IST, see SPRINT_LOG

1. `uv run python tools/gpt_ratchet_patch.py` prints the GPT ratchet row and the P14 check.
2. Insert the row into `report/draft.md` §4.4, re-render Fig 3, and add a GPT chip on the deck's ratchet slide (re-upload `fig3_ratchet.png`).
3. If seeds 203–204 finished, update GPT-5.4 mini's data-limits row.
4. Log the results in SPRINT_LOG, then commit and push. Numbers freeze at 12:00 IST.

## Done (check if you like)

- [x] Abstract: 238 words, with numbers, n and CIs.
- [x] Variance, seeds and baselines reported; positive and mechanical controls in §4.1.
- [x] Pre-registration: freeze commit `5aa9f79` for the main batch; every later batch is logged with a prediction before its run.
- [x] Appendix "Limitations and Dual Use" (E).
- [x] Pre-existing code statement (Appendix D). No code predates the sprint, and no starter-repo file is included or modified.
- [x] References section with URLs.
- [x] Every number traces to `results/` via `analyze.py`, `tools/ratchet_curve.py` and `tools/token_table.py`.

## Still open at the time of writing

- **Total cost:** filled in (about $115; $112.50 logged per call). The GPT-5.4 mini calls are $0 (free tier).
- **References:** verified against primary or public sources (Crossref, arXiv, the court opinions, CourtListener) at ~05:50 Sun. Corrections are applied. Only the page range of Berger et al. (2025) is unverified, because the ABA page returned 403. A quick look in your browser would settle it.
- **GPT-5.4 mini:** n = 5 and its ratchet test (n = 4) are in the draft (P14 held: 72% acceptance, Δ 0.93).

## Form summary (short)

> We test whether the remedies in the DOJ's 2026 RealPage Final Judgment stop an LLM pricing hub that is told to maximise its clients' combined profit, in a repeated Bertrand duopoly (more than 700 runs, seven models from six labs, pre-registered main batch).
>
> - **Data bans** remove 69–92% of the hub's harm on three models and ≤ 10% on two.
> - **Auto-accept within ±1–3% per round** keeps 88–101% of it (Haiku, Qwen).
> - **Firm discretion** works only when firms refuse small nudges.
>
> A scripted 1-cent-per-round ratchet leaves Haiku firms competitive but walks Qwen, GPT-5.4 mini and Gemini firms most or all of the way to monopoly. Remedies should target the advisor's objective and audit acceptance and outcomes. Code, logs and every pre-registration: https://github.com/ebt55/llm-pricing-hub-remedies
