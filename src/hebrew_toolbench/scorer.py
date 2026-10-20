"""AST scorer: compares predicted tool calls with gold calls, BFCL-style.

Gold format (per item): a list of calls, each
    {"name": str, "arguments": {param: [acceptable values...]}}
`null` in an acceptable list means the parameter may be omitted. An empty gold
list means the model must not call any tool (irrelevance).

Every failure is labelled with exactly one error type, so results can be broken
down by failure mode, not just pass/fail.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from hebrew_toolbench.normalize import TypeMismatch, canonical, has_hebrew


class Error(StrEnum):
    INVALID_JSON = "invalid_json"
    CALLED_WHEN_IRRELEVANT = "called_when_irrelevant"
    NO_CALL = "no_call"
    WRONG_CALL_COUNT = "wrong_call_count"
    WRONG_FUNCTION = "wrong_function"
    MISSING_ARG = "missing_arg"
    UNEXPECTED_ARG = "unexpected_arg"
    TYPE_MISMATCH = "type_mismatch"
    # MLCL's failure mode: a Hebrew value where the API expects a canonical one.
    LANGUAGE_MISMATCH = "value_language_mismatch"
    VALUE_MISMATCH = "value_mismatch"


@dataclass(frozen=True)
class Call:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class Verdict:
    correct: bool
    error: Error | None = None
    detail: str = ""


OK = Verdict(True)
MAX_PERMUTATION_CALLS = 7  # 7! = 5040 orderings; items stay well below this.


def _fail(error: Error, detail: str) -> Verdict:
    return Verdict(False, error, detail)


def _match_value(pred: Any, acceptable: list[Any], schema: dict[str, Any], arg: str) -> Verdict:
    try:
        got = canonical(pred, schema)
    except TypeMismatch as e:
        if has_hebrew(pred) and not any(has_hebrew(a) for a in acceptable):
            return _fail(Error.LANGUAGE_MISMATCH, f"{arg}={pred!r}")
        return _fail(Error.TYPE_MISMATCH, f"{arg}: {e}")
    if any(got == canonical(a, schema) for a in acceptable if a is not None):
        return OK
    if has_hebrew(pred) and not any(has_hebrew(a) for a in acceptable):
        return _fail(Error.LANGUAGE_MISMATCH, f"{arg}={pred!r}")
    return _fail(Error.VALUE_MISMATCH, f"{arg}={pred!r}, expected one of {acceptable!r}")


def score_call(gold: dict[str, Any], pred: Call, function: dict[str, Any]) -> Verdict:
    if pred.name != gold["name"]:
        return _fail(Error.WRONG_FUNCTION, f"{pred.name} != {gold['name']}")
    props: dict[str, Any] = function["parameters"].get("properties", {})
    expected: dict[str, list[Any]] = gold["arguments"]
    for arg, value in pred.arguments.items():
        if arg not in props:
            return _fail(Error.UNEXPECTED_ARG, f"{arg} not in schema")
        if arg not in expected:
            # An optional arg the gold does not constrain is fine at its default.
            if "default" in props[arg] and _match_value(value, [props[arg]["default"]], props[arg], arg).correct:
                continue
            return _fail(Error.UNEXPECTED_ARG, f"{arg}={value!r} not expected")
        verdict = _match_value(value, expected[arg], props[arg], arg)
        if not verdict.correct:
            return verdict
    for arg, acceptable in expected.items():
        if arg not in pred.arguments and None not in acceptable:
            return _fail(Error.MISSING_ARG, arg)
    return OK


def score(item: dict[str, Any], preds: list[Call] | None) -> Verdict:
    """Score one item. `preds is None` means the model output was unparseable."""
    if preds is None:
        return _fail(Error.INVALID_JSON, "tool call arguments were not valid JSON")
    gold: list[dict[str, Any]] = item["gold"]
    if not gold:
        return OK if not preds else _fail(Error.CALLED_WHEN_IRRELEVANT, preds[0].name)
    if not preds:
        return _fail(Error.NO_CALL, "")
    if len(preds) != len(gold):
        return _fail(Error.WRONG_CALL_COUNT, f"{len(preds)} calls, expected {len(gold)}")
    if len(gold) > MAX_PERMUTATION_CALLS:
        raise ValueError(f"{item['id']}: too many gold calls for exhaustive matching")
    functions = {f["name"]: f for f in item["functions"]}
    unknown = next((p.name for p in preds if p.name not in functions), None)
    if unknown is not None:
        return _fail(Error.WRONG_FUNCTION, f"{unknown} is not an offered function")
    # Parallel calls are order-free: accept if any pairing matches. Otherwise
    # report the first failure of the pairing that matched the most calls.
    best: tuple[int, Verdict] = (-1, OK)
    for order in itertools.permutations(preds):
        verdicts = [score_call(g, p, functions[p.name]) for g, p in zip(gold, order, strict=True)]
        failures = [v for v in verdicts if not v.correct]
        if not failures:
            return OK
        hits = len(verdicts) - len(failures)
        if hits > best[0]:
            best = (hits, failures[0])
    return best[1]
