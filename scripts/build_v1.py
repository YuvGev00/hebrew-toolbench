"""Build data/v1.jsonl: the 150 v0 seed items, then the five v1 domain packs.

v0 items keep their ids and content; pack items continue each category's numbering.
Every item records its `source` (v0 or the pack that wrote it).

Run: uv run python scripts/build_v1.py
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

from build_seed import ITEMS, SYSTEM
from tools import TOOLS

PACKS = ["pack_gov", "pack_transport", "pack_money", "pack_home", "pack_culture"]
OUT = Path(__file__).resolve().parent.parent / "data" / "v1.jsonl"


def build(packs: list[str] = PACKS) -> list[dict[str, Any]]:
    source = ["v0"] * len(ITEMS)
    for name in packs:
        before = len(ITEMS)
        importlib.import_module(f"packs.{name}")
        source += [name] * (len(ITEMS) - before)
    counters: dict[str, int] = {}
    out = []
    for (category, tags, question, tools, gold), src in zip(ITEMS, source, strict=True):
        counters[category] = counters.get(category, 0) + 1
        out.append(
            {
                "id": f"{category}_{counters[category]:03d}",
                "category": category,
                "tags": tags,
                "system": SYSTEM,
                "question": question,
                "functions": [TOOLS[t] for t in tools],
                "gold": gold,
                "source": src,
                "review": "pending",
            }
        )
    return out


def write(items: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    items = build()
    write(items, OUT)
    print(f"wrote {len(items)} items to {OUT.relative_to(Path.cwd())}")
