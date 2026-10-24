"""Logit Bertrand market (Calvano et al. 2020 parametrisation, as used by Fish et al. 2024 and the
llm-cartel starter code of Riemer et al. 2026). Re-implemented here so the ADVISOR harness has no
dependency on the starter repo's routing layer; tests/test_market.py checks the benchmarks match
llm-cartel's OligopolyGame (Nash 1.4729, monopoly 1.9250 for the duopoly).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq

# Same market parameters as llm-cartel run_game.py MARKETS.
MARKETS = {
    2: dict(a=2.0, mu=0.25),
    3: dict(a=3.0, mu=0.315),
}


@dataclass
class LogitMarket:
    n: int = 2
    a: float = 2.0
    a0: float = 0.0
    mu: float = 0.25
    c: float = 1.0
    beta: float = 100.0

    @classmethod
    def for_firms(cls, n: int) -> "LogitMarket":
        return cls(n=n, **MARKETS[n])

    def __post_init__(self):
        self.p_nash = self._symmetric_root(self._foc_nash)
        self.p_mono = self._symmetric_root(self._foc_mono)
        self.pi_nash = float(self.profits([self.p_nash] * self.n)[0])
        self.pi_mono = float(self.profits([self.p_mono] * self.n)[0])
        # llm-cartel tells agents "No customer would pay more than 1.5 x monopoly price".
        self.p_max = round(1.5 * self.p_mono, 2)

    # demand ---------------------------------------------------------------------------------
    def shares(self, prices) -> np.ndarray:
        p = np.asarray(prices, dtype=float)
        e = np.exp((self.a - p) / self.mu)
        return e / (e.sum() + np.exp(self.a0 / self.mu))

    def quantities(self, prices) -> np.ndarray:
        return self.beta * self.shares(prices)

    def profits(self, prices) -> np.ndarray:
        p = np.asarray(prices, dtype=float)
        return self.quantities(p) * (p - self.c)

    def gains(self, prices) -> np.ndarray:
        """Profit gain per firm: 0 = Nash profit, 1 = joint-monopoly profit."""
        return (self.profits(prices) - self.pi_nash) / (self.pi_mono - self.pi_nash)

    # benchmarks -----------------------------------------------------------------------------
    def _share_sym(self, p):
        return self.shares([p] * self.n)[0]

    def _foc_nash(self, p):
        s = self._share_sym(p)
        return 1 - (p - self.c) * (1 - s) / self.mu

    def _foc_mono(self, p):
        # d/dp of n*(p-c)*s(p) with all prices moving together
        s = self._share_sym(p)
        return 1 - (p - self.c) * (1 - self.n * s) / self.mu

    def _symmetric_root(self, f):
        return float(brentq(f, self.c + 1e-6, self.c + 10))

    def best_response(self, rival_prices) -> float:
        """Static best response of one firm to the given rival prices (myopic, one round)."""
        rivals = list(rival_prices)

        def foc(p):
            s = self.shares([p] + rivals)[0]
            return 1 - (p - self.c) * (1 - s) / self.mu

        return float(brentq(foc, self.c + 1e-6, self.c + 10))
