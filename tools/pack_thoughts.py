"""Gzip the reasoning sidecars (*.thoughts.jsonl) of FINISHED runs, to keep the repository small.

    uv run python tools/pack_thoughts.py results/main results/main-tri ...

A run is finished when its main .jsonl ends with a summary line; unfinished runs are left alone because
the game loop appends to their sidecar on resume. Read packed files with gzip.open(path, "rt").
"""
import gzip
import json
import os
import shutil
import sys

for root in sys.argv[1:]:
    packed = 0
    for dirpath, _, files in os.walk(root):
        for name in files:
            if not name.endswith(".thoughts.jsonl"):
                continue
            side = os.path.join(dirpath, name)
            main = side.replace(".thoughts.jsonl", ".jsonl")
            with open(main, encoding="utf-8") as f:
                lines = [x for x in f if x.strip()]
            if not lines or json.loads(lines[-1]).get("type") != "summary":
                continue
            with open(side, "rb") as src, gzip.open(side + ".gz", "wb") as dst:
                shutil.copyfileobj(src, dst)
            os.remove(side)
            packed += 1
    print(f"{root}: packed {packed} sidecars")
