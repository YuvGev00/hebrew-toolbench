"""List items that every adjudicator model got wrong, for a manual gold review.

When strong models independently fail the same item, the item is either genuinely hard or its gold is
wrong. Each flagged item is printed with its question, gold and every adjudicator's calls, so a human can
decide. Decisions go into DECISIONS.md; gold fixes go into the pack that wrote the item.

Run: uv run python scripts/adjudicate.py claude-sonnet-5-5 gemini-3.5-flash > results/adjudication.md
"""

from __future__ import annotations

import json
import sys

from hebrew_toolbench.dataset import load_items
from hebrew_toolbench.report import score_raw
from hebrew_toolbench.runner import raw_path


def main(models: list[str]) -> None:
    items = load_items()
    results = [score_raw(items, raw_path(m)) for m in models]
    raw = {m: {r["id"]: r for r in map(json.loads, raw_path(m).open(encoding="utf-8"))} for m in models}
    flagged = [i for i in items if all(i["id"] in r.verdicts and not r.verdicts[i["id"]].correct for r in results)]
    print(f"# Adjudication: items failed by all of {', '.join(models)}\n")
    print(f"{len(flagged)} of {len(items)} items.\n")
    for item in flagged:
        print(f"## {item['id']} ({item['source']}, {', '.join(item['tags']) or 'no tags'})\n")
        print(f"- question: {item['question']}")
        print(f"- gold: `{json.dumps(item['gold'], ensure_ascii=False)}`")
        for m, r in zip(models, results, strict=True):
            calls = raw[m][item["id"]]["calls"]
            print(f"- {m} ({r.verdicts[item['id']].error}): `{json.dumps(calls, ensure_ascii=False)}`")
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
