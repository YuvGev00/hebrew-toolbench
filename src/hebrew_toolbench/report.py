"""Score cached raw outputs and render Markdown tables."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from hebrew_toolbench.dataset import CATEGORIES
from hebrew_toolbench.scorer import Call, Error, Verdict, score


@dataclass
class ModelResult:
    model: str
    verdicts: dict[str, Verdict] = field(default_factory=dict)

    def accuracy(self, ids: list[str]) -> float | None:
        scored = [self.verdicts[i].correct for i in ids if i in self.verdicts]
        return sum(scored) / len(scored) if scored else None


def score_raw(items: list[dict[str, Any]], raw: Path) -> ModelResult:
    by_id = {i["id"]: i for i in items}
    records = [json.loads(line) for line in raw.open(encoding="utf-8")]
    result = ModelResult(records[0]["model"] if records else raw.stem)
    for rec in records:
        if rec["id"] not in by_id:
            continue
        calls = None if rec["calls"] is None else [Call(c["name"], c["arguments"]) for c in rec["calls"]]
        result.verdicts[rec["id"]] = score(by_id[rec["id"]], calls)
    return result


def _pct(x: float | None) -> str:
    return "–" if x is None else f"{100 * x:.1f}"


def results_table(items: list[dict[str, Any]], results: list[ModelResult]) -> str:
    groups = {c: [i["id"] for i in items if i["category"] == c] for c in CATEGORIES}
    # MLCL-style slice: items whose gold expects a canonical (non-Hebrew) value.
    groups["canonical_value"] = [i["id"] for i in items if "canonical_value" in i["tags"]]
    all_ids = [i["id"] for i in items]
    head = ["Model", "N", "Overall", *(f"{k} ({len(v)})" for k, v in groups.items()), "lang-mismatch errors"]
    rows = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in sorted(results, key=lambda r: -(r.accuracy(all_ids) or 0)):
        lang = sum(v.error is Error.LANGUAGE_MISMATCH for v in r.verdicts.values())
        cells = [
            f"`{r.model.removeprefix('models/')}`",
            str(len(r.verdicts)),
            _pct(r.accuracy(all_ids)),
            *(_pct(r.accuracy(ids)) for ids in groups.values()),
            str(lang),
        ]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def error_table(results: list[ModelResult]) -> str:
    counts = {r.model: Counter(v.error for v in r.verdicts.values() if v.error) for r in results}
    errors = [e for e in Error if any(c[e] for c in counts.values())]
    head = ["Error type", *(f"`{m.removeprefix('models/')}`" for m in counts)]
    rows = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    rows += ["| " + " | ".join([e.value, *(str(c[e]) for c in counts.values())]) + " |" for e in errors]
    return "\n".join(rows)


def tag_table(items: list[dict[str, Any]], results: list[ModelResult], min_items: int = 5) -> str:
    tags = Counter(t for i in items for t in i["tags"])
    head = ["Tag", "N", *(f"`{r.model.removeprefix('models/')}`" for r in results)]
    rows = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for tag, n in tags.most_common():
        if n < min_items:
            continue
        ids = [i["id"] for i in items if tag in i["tags"]]
        rows.append("| " + " | ".join([tag, str(n), *(_pct(r.accuracy(ids)) for r in results)]) + " |")
    return "\n".join(rows)
