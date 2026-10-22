from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

CATEGORIES = ("simple", "multiple", "parallel", "irrelevance")
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
# v1 (800 items) is the default; HTB_DATA points tests and tools at another file (scripts/check_pack.py).
DEFAULT_DATASET = Path(os.environ.get("HTB_DATA", DATA_DIR / "v1.jsonl"))
SEED_V0 = DATA_DIR / "seed_v0.jsonl"


def load_items(path: Path = DEFAULT_DATASET) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
