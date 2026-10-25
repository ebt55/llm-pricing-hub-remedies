## Related Work

**LLM pricing collusion.** Calvano et al. (2020) showed that Q-learning agents in a repeated logit Bertrand market learn supracompetitive prices backed by reward–punishment strategies. GPT-4 agents in the same market also price supracompetitively, more so under some prompt wordings (Fish et al., 2024). Riemer et al. (2026), whose llm-cartel code we build on, find the same for a reasoning model, and Keppo et al. (2026) show such collusion erodes under agent heterogeneity. This work asks whether collusion emerges among independent agents; we ask which remedies remove a coordinating advisor's effect.

**Shared algorithms and hub-and-spoke.** Cao and Hu (2026) show theoretically that sellers sharing one AI model can reach supracompetitive prices without communication when its recommendations are correlated enough, which they liken to hub-and-spoke collusion. Liability turns on nonpublic data pooling and adherence (Berger et al., 2025): *Gibson v. Cendyn* (9th Cir. 2025) upheld dismissal where recommendations were optional and no pooling of confidential data was alleged, whereas *Cornish-Adebiyi v. Caesars* (3d Cir. 2026) revived a claim citing pooled nonpublic data and about 90% acceptance. The DOJ's RealPage settlement, as reported, bars runtime use of competitors' nonpublic data, requires nonpublic training data at least 12 months old and forbids reporting below state level; the complaints also cited auto-accept settings and a "race to the bottom" pitch. To our knowledge, no prior work tests these remedies on LLM advisors.

**Interventions in LLM markets.** Evidence is mixed and model-specific. Anti-collusion prompts, monitoring notices and fines fail for Riemer et al.'s (2026) 7B model, the prompts even raising prices, while GPT-5.4 obeys them. An announced price cap becomes a focal point for small models (Dhanda, 2026). Enforced public governance, unlike a written constitution, cuts severe Cournot market division from 50% to 5.6% of runs (Bracale Syrnikov et al., 2026). Collina et al. (2025) prove a no-regret defector can break collusion in large markets, and Idowu et al. (2026) propose untested AI analogues of human remedies, such as aggregated information. These act on firms' prompts, rules or rivals; ours act on a third-party advisor's information and authority.

**Detection and concurrent work.** Cartel screens flag elevated prices or, following Abrantes-Metz et al. (2006), low price variance; Xu et al. (2026) prove price-level audits are blind when collusion acts only through dependence. LLM judges reading chain-of-thought missed steering-induced collusion (Riemer et al., 2026), and monitors' sabotage detection depends on what they see (Arike et al., 2026). We test both screens and a reasoning monitor. Concurrent work, zerocommcartel (2026), varies whether a firm's prompt says rivals use the same AI model in a one-shot Cournot game and tests a provider-side system-prompt remedy; we vary the advisor's data access and firms' adherence in a repeated price-setting market.

### Reference list

- Abrantes-Metz, R. M., Froeb, L. M., Geweke, J., & Taylor, C. T. (2006). A variance screen for collusion. *International Journal of Industrial Organization*, 24(3), 467–486.
- Arike, R., Mehta Moreno, R., Subramani, R., Biswas, S., & Ward, F. R. (2026). How does information access affect LLM monitors' ability to detect sabotage? arXiv:2601.21112 (v2). https://arxiv.org/abs/2601.21112
- Berger, L. F., Weiner, M. L., & Jiang, W. (2025). Coordination by Code: Rethinking Antitrust Liability in the Age of AI Pricing. *Antitrust* (ABA Section of Antitrust Law), 40(1), Fall 2025. https://www.americanbar.org/groups/antitrust_law/resources/magazine/2025-fall/coordination-code-rethinking-antitrust-liability-age-ai-pricing/
- Bracale Syrnikov, M., Pierucci, F., Galisai, M., Prandi, M., Bisconti, P., Giarrusso, F., Sorokoletova, O., Suriani, V., & Nardi, D. (2026). Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs. arXiv:2601.11369 (v2). https://arxiv.org/abs/2601.11369
- Calvano, E., Calzolari, G., Denicolò, V., & Pastorello, S. (2020). Artificial Intelligence, Algorithmic Pricing, and Collusion. *American Economic Review*, 110(10), 3267–3297. https://doi.org/10.1257/aer.20190623
- Cao, S., & Hu, M. (2026). Supracompetitive Pricing Under AI Monoculture. arXiv:2601.01279 (v3). https://arxiv.org/abs/2601.01279
- Collina, N., Arunachaleswaran, E. R., & Jagadeesan, M. (2025). Breaking Algorithmic Collusion in Human-AI Ecosystems. arXiv:2511.21935. https://arxiv.org/abs/2511.21935
- Dhanda, K. (2026). A Price Cap Can Act as a Focal Point for LLM Pricing Agents: Evidence from a Repeated Bertrand Duopoly (Revised). Research Square preprint (not peer reviewed). https://doi.org/10.21203/rs.3.rs-10183486/v1
- Fish, S., Gonczarowski, Y. A., & Shorrer, R. (2024). Algorithmic Collusion by Large Language Models. arXiv:2404.00806 (first version Jan 2024; v6 Aug 2026). https://arxiv.org/abs/2404.00806
- Idowu, J., Almasoud, A., & Alfahid, A. (2026). Mapping Human Anti-collusion Mechanisms to Multi-agent AI Systems. arXiv:2601.00360 (v3). https://arxiv.org/abs/2601.00360
- Keppo, J., Li, Y., Tsoukalas, G., & Yuan, N. (2026). On the Fragility of AI Agent Collusion. arXiv:2603.20281. https://arxiv.org/abs/2603.20281
- Riemer, M., Tosato, T., Memarian, A., Puelma Touzel, M., Berseth, G., Rish, I., & Dumas, G. (2026). Position: Collusion Risks Among AI Reasoning Agents Justify Certification Requirements for Making Market Decisions. ICML 2026 (position track). arXiv:2608.18078; OpenReview Vhi9tHbKTa. Code (llm-cartel): https://github.com/mattriemer/LLMCartel
- Xu, X., Wu, C., Lu, J., Tan, K., Tao, S., & Hong, H. (2026). Collusion with Competitive Marginals: Price-Level Audits Are Blind by Construction. arXiv:2607.26385. https://arxiv.org/abs/2607.26385
- zerocommcartel (2026). Concurrent Apart Research collusion-sprint project. https://github.com/carver/apart-research-collusion-sprint-2026 (only the README and issues #31–#34 were read, on 24 Oct 2026).
- *United States et al. v. RealPage, Inc. et al.*, No. 1:24-cv-00710 (M.D.N.C.); proposed final judgment and competitive impact statement, Federal Register, 21 Jan 2026. https://www.justice.gov/atr/case/us-et-al-v-realpage-inc-et-al
- *Gibson v. Cendyn Group*, 148 F.4th 1069 (9th Cir. 2025), cert. denied (20 Apr 2026).
- *Cornish-Adebiyi v. Caesars Entertainment*, No. 24-3006 (3d Cir. 29 Jul 2026).

**Verification (25 Oct, ~05:50 IST).** A verification agent checked every reference against primary or public sources: Crossref, arXiv, the court opinions and CourtListener. All exist. Corrections were applied in `draft.md`:
- the RealPage URL now points to the entered Final Judgment;
- the full captions for *Gibson* (cert. denied, Apr 2026) and *Cornish-Adebiyi* (reversed and remanded, precedential);
- the Abrantes-Metz DOI, Fish et al. (EC 2026) and Idowu et al. (*Knowledge-Based Systems*).

Still unverified: the page range of Berger et al. (the ABA page returned 403). This file's own reference list predates those corrections; `draft.md` is the canonical list.
