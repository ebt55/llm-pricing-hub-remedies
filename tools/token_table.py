"""Measured reasoning budget per model ($0): median output tokens (thinking included) and latency per call.

    uv run python tools/token_table.py

Gemini's OpenAI-compatible endpoint omits thinking tokens from completion_tokens, so providers.py logs
total - prompt tokens for Gemini; every other provider reports thinking inside its output count.
"""

from __future__ import annotations

import glob
import json
import statistics as st
from collections import defaultdict

TAGS = {"main": "low", "robust-effort": "high", "replicate-dsflash": "low", "replicate-openai": "low",
        "ladder-gem-lite": "low", "ladder-gem-lite-hi": "high", "ladder-gem-flash": "low", "ladder-or-qwen": "1,024 budget",
        "ladder-or-nemotron": "1,024 budget"}


def main():
    cells = defaultdict(lambda: {"out": [], "lat": [], "retry": 0, "n": 0})
    for tag, effort in TAGS.items():
        for f in glob.glob(f"results/{tag}/*/s*.jsonl"):
            if ".thoughts." in f:
                continue
            for line in open(f, encoding="utf-8"):
                r = json.loads(line)
                for c in r.get("calls", []) if r.get("type") == "round" else []:
                    role = "hub" if c["who"].startswith("advisor") else "firm"
                    cell = cells[(c.get("api_model", "?"), effort, role)]
                    cell["out"].append(c["usage"]["tokens_out"])
                    cell["lat"].append(c["usage"].get("latency_s") or 0)
                    cell["retry"] += c.get("attempts", 1) > 1
                    cell["n"] += 1
    print("| Model (API id) | Setting | Role | Calls | Median output tokens | P90 | Median latency (s) | Retry rate |")
    print("|---|---|---|---|---|---|---|---|")
    for (model, effort, role), c in sorted(cells.items()):
        out = sorted(c["out"])
        print(f"| {model} | {effort} | {role} | {c['n']} | {st.median(out):.0f} | {out[int(0.9 * (len(out) - 1))]} | "
              f"{st.median(c['lat']):.1f} | {c['retry'] / c['n']:.3f} |")


if __name__ == "__main__":
    main()
