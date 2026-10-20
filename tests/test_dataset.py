"""Integrity checks on the seed set: every gold answer must be well-formed and self-consistent."""

from collections import Counter
from typing import Any

import pytest
from pyluach import dates, hebrewcal

from hebrew_toolbench.dataset import CATEGORIES, load_items
from hebrew_toolbench.normalize import canonical
from hebrew_toolbench.scorer import Call, score

ITEMS = load_items()
IDS = [i["id"] for i in ITEMS]
# pyluach numbers months from Nisan; Adar I/II only exist in leap years.
MONTH_NUMBER = {
    "Nisan": 1,
    "Iyar": 2,
    "Sivan": 3,
    "Tammuz": 4,
    "Av": 5,
    "Elul": 6,
    "Tishrei": 7,
    "Cheshvan": 8,
    "Kislev": 9,
    "Tevet": 10,
    "Shevat": 11,
    "Adar": 12,
    "Adar I": 12,
    "Adar II": 13,
}


def test_ids_unique_and_categories_valid() -> None:
    assert len(set(IDS)) == len(IDS)
    assert {i["category"] for i in ITEMS} == set(CATEGORIES)
    assert len(ITEMS) >= 150


@pytest.mark.parametrize("item", ITEMS, ids=IDS)
def test_gold_is_well_formed(item: dict[str, Any]) -> None:
    functions = {f["name"]: f for f in item["functions"]}
    assert (item["category"] == "irrelevance") == (not item["gold"])
    if item["category"] in ("simple", "multiple"):
        assert len(item["gold"]) == 1
    for gold in item["gold"]:
        params = functions[gold["name"]]["parameters"]
        for arg in params["required"]:
            assert None not in gold["arguments"].get(arg, [None]), f"required {arg} must be pinned"
        for arg, acceptable in gold["arguments"].items():
            schema = params["properties"][arg]
            for value in acceptable:
                if value is None:
                    continue
                canonical(value, schema)  # raises on a malformed gold value
                if "enum" in schema:
                    assert value in schema["enum"]


@pytest.mark.parametrize("item", ITEMS, ids=IDS)
def test_gold_scores_itself_correct(item: dict[str, Any]) -> None:
    preds = [
        Call(
            g["name"],
            {
                k: next(v for v in vals if v is not None)
                for k, vals in g["arguments"].items()
                if any(v is not None for v in vals)
            },
        )
        for g in item["gold"]
    ]
    assert score(item, preds).correct


def _hebrew_calls(name: str) -> list[dict[str, Any]]:
    return [g for i in ITEMS for g in i["gold"] if g["name"] == name]


@pytest.mark.parametrize("gold", _hebrew_calls("convert_hebrew_date"))
def test_hebrew_dates_exist(gold: dict[str, Any]) -> None:
    (year,), (month,), (day,) = gold["arguments"]["year"], gold["arguments"]["month"], gold["arguments"]["day"]
    leap = hebrewcal.Year(year).leap
    invalid = ("Adar",) if leap else ("Adar I", "Adar II")
    assert month not in invalid, f"{month} does not exist in {year}"
    assert day <= len(list(hebrewcal.Month(year, MONTH_NUMBER[month]).iterdates()))


def test_calendar_compute_items_match_pyluach() -> None:
    # "א׳ בכסלו תשפ״ז" must resolve to the Gregorian date pyluach computes.
    item = next(i for i in ITEMS if "calendar_compute" in i["tags"])
    expected = dates.HebrewDate(5787, MONTH_NUMBER["Kislev"], 1).to_greg().to_pydate().isoformat()
    assert item["gold"][0]["arguments"]["date"] == [expected]


def test_tag_coverage() -> None:
    tags = Counter(t for i in ITEMS for t in i["tags"])
    for required in (
        "hebrew_calendar",
        "currency_ils",
        "gender_morphology",
        "transliteration",
        "mixed_direction",
        "canonical_value",
    ):
        assert tags[required] >= 5, required
