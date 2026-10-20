from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CATEGORIES = ("simple", "multiple", "parallel", "irrelevance")
DEFAULT_DATASET = Path(__file__).resolve().parents[2] / "data" / "seed_v0.jsonl"


def load_items(path: Path = DEFAULT_DATASET) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
