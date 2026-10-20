from typing import Any

import pytest

from hebrew_toolbench.normalize import TypeMismatch, canonical, normalize_string
from hebrew_toolbench.scorer import Call, Error, score

WEATHER: dict[str, Any] = {
    "name": "get_weather",
    "description": "Weather forecast",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name in English"},
            "date": {"type": "string", "format": "date"},
            "units": {"type": "string", "enum": ["celsius", "fahrenheit"], "default": "celsius"},
        },
        "required": ["city"],
    },
}
PAY: dict[str, Any] = {
    "name": "send_payment",
    "description": "Send money",
    "parameters": {
        "type": "object",
        "properties": {
            "phone": {"type": "string", "x-normalize": "phone"},
            "amount_ils": {"type": "number"},
            "count": {"type": "integer"},
            "urgent": {"type": "boolean"},
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["phone", "amount_ils"],
    },
}


def item(gold: list[dict[str, Any]], functions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {"id": "t", "category": "simple", "functions": functions or [WEATHER, PAY], "gold": gold}


WEATHER_GOLD = {"name": "get_weather", "arguments": {"city": ["Tel Aviv", "Tel Aviv-Yafo"], "date": ["2026-10-21"]}}


class TestNormalize:
    def test_string_folds_bidi_niqqud_case_and_gershayim(self) -> None:
        assert normalize_string("\u200fשָׁלוֹם ") == "שלום"
        assert normalize_string("צה״ל") == normalize_string('צה"ל')
        assert normalize_string("  Tel   AVIV. ") == "tel aviv"

    def test_date_requires_iso(self) -> None:
        assert canonical("2026-1-5", {"type": "string", "format": "date"}) == "2026-01-05"
        for bad in ("5/1/2026", "20 באוקטובר", "2026-02-30"):
            with pytest.raises(TypeMismatch):
                canonical(bad, {"type": "string", "format": "date"})

    def test_time_and_datetime(self) -> None:
        assert canonical("9:05", {"type": "string", "format": "time"}) == "09:05"
        dt_schema = {"type": "string", "format": "date-time"}
        assert canonical("2026-10-21T09:00:00+03:00", dt_schema) == canonical("2026-10-21T09:00", dt_schema)

    def test_phone(self) -> None:
        schema = {"type": "string", "x-normalize": "phone"}
        assert canonical("+972-54-123-4567", schema) == canonical("054 1234567", schema) == "0541234567"

    def test_numbers_strict_type(self) -> None:
        assert canonical(5, {"type": "number"}) == canonical(5.0, {"type": "number"})
        assert canonical(0.1 + 0.2, {"type": "number"}) == canonical(0.3, {"type": "number"})
        assert canonical(3.0, {"type": "integer"}) == 3
        for bad in ("5", True, 2.5):
            with pytest.raises(TypeMismatch):
                canonical(bad, {"type": "integer"})

    def test_array_is_order_insensitive(self) -> None:
        schema = {"type": "array", "items": {"type": "string"}}
        assert canonical(["b", "A"], schema) == canonical(["a", "B"], schema)


class TestScore:
    def test_exact_match(self) -> None:
        pred = [Call("get_weather", {"city": "tel aviv-yafo", "date": "2026-10-21"})]
        assert score(item([WEATHER_GOLD]), pred).correct

    def test_default_optional_arg_is_accepted(self) -> None:
        pred = [Call("get_weather", {"city": "Tel Aviv", "date": "2026-10-21", "units": "celsius"})]
        assert score(item([WEATHER_GOLD]), pred).correct

    def test_non_default_optional_arg_is_unexpected(self) -> None:
        pred = [Call("get_weather", {"city": "Tel Aviv", "date": "2026-10-21", "units": "fahrenheit"})]
        assert score(item([WEATHER_GOLD]), pred).error is Error.UNEXPECTED_ARG

    def test_hallucinated_arg(self) -> None:
        pred = [Call("get_weather", {"city": "Tel Aviv", "date": "2026-10-21", "country": "IL"})]
        assert score(item([WEATHER_GOLD]), pred).error is Error.UNEXPECTED_ARG

    def test_hebrew_value_is_language_mismatch(self) -> None:
        pred = [Call("get_weather", {"city": "תל אביב", "date": "2026-10-21"})]
        assert score(item([WEATHER_GOLD]), pred).error is Error.LANGUAGE_MISMATCH

    def test_hebrew_date_is_language_mismatch(self) -> None:
        pred = [Call("get_weather", {"city": "Tel Aviv", "date": "21 באוקטובר 2026"})]
        assert score(item([WEATHER_GOLD]), pred).error is Error.LANGUAGE_MISMATCH

    def test_hebrew_gold_is_not_a_language_mismatch(self) -> None:
        gold = {"name": "get_weather", "arguments": {"city": ["חיפה"]}}
        pred = [Call("get_weather", {"city": "תל אביב"})]
        assert score(item([gold]), pred).error is Error.VALUE_MISMATCH

    def test_numeric_string_is_type_mismatch(self) -> None:
        gold = {"name": "send_payment", "arguments": {"phone": ["0521234567"], "amount_ils": [150]}}
        pred = [Call("send_payment", {"phone": "052-1234567", "amount_ils": "150"})]
        assert score(item([gold]), pred).error is Error.TYPE_MISMATCH

    def test_missing_and_omittable(self) -> None:
        gold = {
            "name": "send_payment",
            "arguments": {"phone": ["0521234567"], "amount_ils": [150], "urgent": [None, False]},
        }
        assert score(item([gold]), [Call("send_payment", {"phone": "0521234567", "amount_ils": 150})]).correct
        verdict = score(item([gold]), [Call("send_payment", {"phone": "0521234567"})])
        assert verdict.error is Error.MISSING_ARG

    def test_wrong_function(self) -> None:
        pred = [Call("send_payment", {"phone": "0521234567", "amount_ils": 1})]
        assert score(item([WEATHER_GOLD]), pred).error is Error.WRONG_FUNCTION

    def test_unoffered_function(self) -> None:
        assert score(item([WEATHER_GOLD]), [Call("search_web", {})]).error is Error.WRONG_FUNCTION

    def test_irrelevance(self) -> None:
        assert score(item([]), []).correct
        assert score(item([]), [Call("get_weather", {"city": "Eilat"})]).error is Error.CALLED_WHEN_IRRELEVANT

    def test_no_call_and_invalid_json(self) -> None:
        assert score(item([WEATHER_GOLD]), []).error is Error.NO_CALL
        assert score(item([WEATHER_GOLD]), None).error is Error.INVALID_JSON

    def test_parallel_is_order_free(self) -> None:
        gold = [
            {"name": "get_weather", "arguments": {"city": ["Haifa"]}},
            {"name": "get_weather", "arguments": {"city": ["Eilat"]}},
        ]
        preds = [Call("get_weather", {"city": "Eilat"}), Call("get_weather", {"city": "Haifa"})]
        assert score(item(gold), preds).correct
        assert score(item(gold), preds[:1]).error is Error.WRONG_CALL_COUNT

    def test_parallel_reports_best_pairing_failure(self) -> None:
        gold = [
            {"name": "get_weather", "arguments": {"city": ["Haifa"]}},
            {"name": "get_weather", "arguments": {"city": ["Eilat"]}},
        ]
        preds = [Call("get_weather", {"city": "Eilat"}), Call("get_weather", {"city": "חיפה"})]
        assert score(item(gold), preds).error is Error.LANGUAGE_MISMATCH
