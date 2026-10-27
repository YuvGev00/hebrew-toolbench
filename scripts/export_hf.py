"""Export data/v1.jsonl in the layout the Hugging Face Hub expects.

`functions` and `gold` differ in shape from item to item (each tool has its own
parameters), which Arrow cannot store as one column type, so they are written as
JSON strings, as BFCL does. Everything else is copied unchanged.

    python scripts/export_hf.py        # writes hf/data/test.jsonl next to hf/README.md
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "v1.jsonl"
OUT = ROOT / "hf" / "data" / "test.jsonl"
JSON_FIELDS = ("functions", "gold")


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with SRC.open(encoding="utf-8") as src, OUT.open("w", encoding="utf-8") as out:
        for line in src:
            item = json.loads(line)
            for field in JSON_FIELDS:
                item[field] = json.dumps(item[field], ensure_ascii=False)
            out.write(json.dumps(item, ensure_ascii=False) + "\n")
            n += 1
    print(f"wrote {n} items to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
