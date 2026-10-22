"""Validate one pack on its own: build v0 + that pack, run the dataset tests on it, check its counts.

Run: uv run python scripts/check_pack.py pack_gov
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from build_v1 import build, write

TARGETS = {
    "pack_gov": {"simple": 47, "multiple": 34, "parallel": 25, "irrelevance": 24},
    "pack_transport": {"simple": 47, "multiple": 34, "parallel": 25, "irrelevance": 24},
    "pack_money": {"simple": 47, "multiple": 34, "parallel": 25, "irrelevance": 24},
    "pack_home": {"simple": 47, "multiple": 33, "parallel": 25, "irrelevance": 24},
    "pack_culture": {"simple": 48, "multiple": 33, "parallel": 26, "irrelevance": 24},
}

if __name__ == "__main__":
    pack = sys.argv[1]
    items = build([pack])
    mine = [i for i in items if i["source"] == pack]
    counts = Counter(i["category"] for i in mine)
    print(f"{pack}: {len(mine)} items {dict(counts)} (target {TARGETS[pack]})")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "data.jsonl"
        write(items, path)
        root = Path(__file__).resolve().parent.parent
        rc = subprocess.call(
            ["pytest", "-q", "-x", "tests/test_dataset.py"], cwd=root, env={**os.environ, "HTB_DATA": str(path)}
        )
    if dict(counts) != TARGETS[pack]:
        print("COUNTS DO NOT MATCH TARGET")
        rc = rc or 1
    sys.exit(rc)
