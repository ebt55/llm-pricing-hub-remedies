"""Benchmarks must match llm-cartel's OligopolyGame (Calvano parametrisation)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from advisor.market import LogitMarket  # noqa: E402


def test_duopoly_benchmarks():
    m = LogitMarket.for_firms(2)
    assert abs(m.p_nash - 1.4729) < 1e-3
    assert abs(m.p_mono - 1.9250) < 1e-3
    assert abs(m.pi_nash - 22.29) < 0.01
    assert abs(m.pi_mono - 33.75) < 0.01
    assert abs(m.gains([m.p_nash] * 2)[0]) < 1e-9 and abs(m.gains([m.p_mono] * 2)[0] - 1) < 1e-9
    assert abs(m.best_response([m.p_nash]) - m.p_nash) < 1e-6  # Nash is a fixed point of BR
    assert abs(m.best_response([1.80]) - 1.614) < 2e-3  # matches vetting/scripts/br_benchmark.py


def test_triopoly_runs():
    m = LogitMarket.for_firms(3)
    assert m.p_nash < m.p_mono


if __name__ == "__main__":
    test_duopoly_benchmarks()
    test_triopoly_runs()
    m = LogitMarket.for_firms(2)
    print("ok", round(m.p_nash, 4), round(m.p_mono, 4), round(m.pi_nash, 2), round(m.pi_mono, 2), m.p_max)
    m3 = LogitMarket.for_firms(3)
    print("triopoly", round(m3.p_nash, 4), round(m3.p_mono, 4))
