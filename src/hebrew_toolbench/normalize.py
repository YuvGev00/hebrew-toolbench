"""Deterministic value canonicalisation, driven by the parameter's JSON schema.

`canonical(value, schema)` maps a model-produced (or gold) value to a hashable
canonical form, or raises `TypeMismatch` when the value has the wrong JSON type
or an unparseable format. Two values are equivalent iff their canonical forms
are equal. There is no fuzzy matching and no LLM judge.
"""

from __future__ import annotations

import datetime as dt
import math
import re
import unicodedata
from typing import Any

JSON = Any
Canon = Any  # hashable: str | int | float | bool | tuple | frozenset

HEBREW_LETTER = re.compile(r"[א-ת]")
# Niqqud, cantillation and other Hebrew combining marks.
HEBREW_MARKS = re.compile(r"[\u0591-\u05c7]")
# LRM/RLM/ALM and the embedding/override/isolate controls: invisible in rendering.
BIDI_CONTROLS = re.compile(r"[\u200e\u200f\u061c\u202a-\u202e\u2066-\u2069]")
QUOTE_FOLD = str.maketrans({"״": '"', "”": '"', "“": '"', "׳": "'", "’": "'", "‘": "'"})
EDGE_PUNCT = " \t\n'\".,!?:;"
DATE_RE = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
TIME_RE = re.compile(r"^(\d{1,2}):(\d{2})(?::(00))?$")


class TypeMismatch(ValueError):
    """The value cannot be read as the schema's type/format."""


def has_hebrew(value: JSON) -> bool:
    if isinstance(value, str):
        return bool(HEBREW_LETTER.search(value))
    if isinstance(value, list):
        return any(has_hebrew(v) for v in value)
    if isinstance(value, dict):
        return any(has_hebrew(v) for v in value.values())
    return False


def normalize_string(s: str) -> str:
    """NFC, drop bidi controls and niqqud, fold geresh/gershayim, casefold, trim."""
    s = unicodedata.normalize("NFC", s)
    s = BIDI_CONTROLS.sub("", s)
    s = HEBREW_MARKS.sub("", s)
    s = s.translate(QUOTE_FOLD)
    s = " ".join(s.split()).casefold()
    return s.strip(EDGE_PUNCT)


def _date(s: str) -> dt.date:
    m = DATE_RE.match(s.strip())
    if not m:
        raise TypeMismatch(f"not an ISO date: {s!r}")
    try:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    except ValueError as e:
        raise TypeMismatch(str(e)) from e


def _time(s: str) -> tuple[int, int]:
    m = TIME_RE.match(s.strip())
    if not m or int(m[1]) > 23 or int(m[2]) > 59:
        raise TypeMismatch(f"not an HH:MM time: {s!r}")
    return int(m[1]), int(m[2])


def _datetime(s: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(s.strip())
    except ValueError as e:
        raise TypeMismatch(f"not an ISO datetime: {s!r}") from e
    # Wall-clock comparison: every item is in Israel time, offsets are noise.
    return parsed.replace(tzinfo=None, second=0, microsecond=0)


def _phone(s: str) -> str:
    digits = re.sub(r"\D", "", s)
    if digits.startswith("972"):
        digits = "0" + digits[3:]
    if not 9 <= len(digits) <= 10:
        raise TypeMismatch(f"not an Israeli phone number: {s!r}")
    return digits


def _number(value: JSON, *, integer: bool) -> int | float:
    # bool is an int subclass in Python but not a JSON number.
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeMismatch(f"expected number, got {type(value).__name__}")
    if not math.isfinite(value):
        raise TypeMismatch("non-finite number")
    if integer:
        if not float(value).is_integer():
            raise TypeMismatch(f"expected integer, got {value!r}")
        return int(value)
    # Round so 0.1 + 0.2 and 0.3 share a canonical form.
    return round(float(value), 6) + 0.0


def canonical(value: JSON, schema: dict[str, Any]) -> Canon:
    kind = schema.get("type", "string")
    if kind in ("integer", "number"):
        return _number(value, integer=kind == "integer")
    if kind == "boolean":
        if not isinstance(value, bool):
            raise TypeMismatch(f"expected boolean, got {type(value).__name__}")
        return value
    if kind == "array":
        if not isinstance(value, list):
            raise TypeMismatch(f"expected array, got {type(value).__name__}")
        items = schema.get("items", {})
        # Order-insensitive multiset: lists here are attendees, tickers, cities.
        return tuple(sorted((canonical(v, items) for v in value), key=repr))
    if kind == "object":
        if not isinstance(value, dict):
            raise TypeMismatch(f"expected object, got {type(value).__name__}")
        props = schema.get("properties", {})
        return frozenset((k, canonical(v, props.get(k, {}))) for k, v in value.items())
    if not isinstance(value, str):
        raise TypeMismatch(f"expected string, got {type(value).__name__}")
    fmt = schema.get("format") or schema.get("x-normalize")
    if fmt == "date":
        return _date(value).isoformat()
    if fmt == "time":
        hour, minute = _time(value)
        return f"{hour:02d}:{minute:02d}"
    if fmt == "date-time":
        return _datetime(value).isoformat()
    if fmt == "phone":
        return _phone(value)
    return normalize_string(value)
