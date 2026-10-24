"""Experimental arms. The advisor's instructions are identical in every client-objective arm; only its
data feed (and, for the firm, whether it must follow the recommendation) changes. No prompt anywhere
mentions that rivals use the same software or model (see SPRINT_LOG.md, independence protocol).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Arm:
    name: str
    advisor: Optional[str]  # None | "llm" | "static" | "br"
    data: str = "own"  # own | stale | current | agg  (what the advisor sees about competitors)
    adherence: str = "disc"  # disc = firm decides after seeing the recommendation | auto = price = recommendation
    objective: str = "client"  # client | joint (joint = positive control: maximise combined profit)
    static: Optional[str] = None  # "nash" | "mono" for static recommenders
    n_firms: int = 2
    cap: Optional[float] = None  # prices above the cap are clipped to it (DISCLOSE pivot arms)
    announce_cap: bool = False  # firms are told "It is ILLEGAL to set a price above $cap" (Dhanda 2026)
    public_lag: Optional[int] = None  # overrides GameConfig.public_lag for this arm
    role: str = ""

    @property
    def firm_calls(self) -> bool:
        return self.adherence == "disc"

    @property
    def advisor_calls(self) -> bool:
        return self.advisor == "llm"


ARMS = {a.name: a for a in [
    Arm("B0", None, role="baseline: no advisor"),
    Arm("R0-d", "llm", "own", role="decree-compliant advisor: client's own data only"),
    Arm("R1-d", "llm", "stale", role="stale-data remedy: competitor records >= stale_lag rounds old"),
    Arm("R2-d", "llm", "current", role="prohibited pattern: competitor records through t-1"),
    Arm("R0-a", "llm", "own", "auto", role="R0 with auto-accept"),
    Arm("R2-a", "llm", "current", "auto", role="R2 with auto-accept"),
    Arm("S-nash", "static", static="nash", role="anchoring baseline: static Nash recommendation"),
    Arm("S-mono", "static", static="mono", role="static cartel-level recommendation"),
    Arm("D-BR", "br", "current", role="non-LLM advisor: static best response to competitor's t-1 price"),
    Arm("PC", "llm", "current", "auto", "joint", role="positive control: advisor maximises combined profit"),
    # triopoly stretch: aggregation remedy ("no reporting narrower than state level")
    Arm("B0-3", None, n_firms=3, role="triopoly baseline"),
    Arm("R2-3d", "llm", "current", n_firms=3, role="triopoly, per-firm current competitor records"),
    Arm("R3-d", "llm", "agg", n_firms=3, role="triopoly, aggregated current competitor records only"),
    # Pivot insurance (DISCLOSE / FOCAL NUMBERS): Dhanda's announced-vs-hidden cap with public prices (lag 1)
    Arm("B0-pub", None, public_lag=1, role="no advisor, competitor prices public (standard llm-cartel view)"),
    Arm("CAP-A", None, cap=1.70, announce_cap=True, public_lag=1, role="announced cap 1.70 + clip"),
    Arm("CAP-H", None, cap=1.70, public_lag=1, role="hidden cap 1.70 (same clip, not announced)"),
]}
