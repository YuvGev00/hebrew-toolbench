"""Tool (function) schemas shared by the seed items. One source of truth.

Descriptions are in English, as real APIs are. Parameters that expect a
canonical value (English city names, ISO codes, enums, ISO dates) say so,
which is what makes the MLCL language-mismatch failure measurable.
"""

from __future__ import annotations

from typing import Any

STATIONS = [
    "Tel Aviv Savidor Center",
    "Tel Aviv HaShalom",
    "Jerusalem Yitzhak Navon",
    "Haifa Hof HaCarmel",
    "Ben Gurion Airport",
    "Beer Sheva Center",
    "Nahariya",
    "Modiin Center",
    "Ashdod Ad Halom",
    "Netanya",
]
HEBREW_MONTHS = [
    "Tishrei", "Cheshvan", "Kislev", "Tevet", "Shevat", "Adar", "Adar I", "Adar II",
    "Nisan", "Iyar", "Sivan", "Tammuz", "Av", "Elul",
]
HOLIDAYS = [
    "rosh_hashana", "yom_kippur", "sukkot", "simchat_torah", "hanukkah", "tu_bishvat", "purim",
    "passover", "yom_hashoah", "yom_hazikaron", "yom_haatzmaut", "lag_baomer", "shavuot", "tisha_bav",
]
CURRENCIES = ["ILS", "USD", "EUR", "GBP", "JPY", "CHF"]

DATE = {"type": "string", "format": "date", "description": "Date in YYYY-MM-DD format"}
TIME = {"type": "string", "format": "time", "description": "24-hour time, HH:MM"}
CITY = {"type": "string", "description": "City name in English, e.g. 'Tel Aviv'"}
PHONE = {"type": "string", "x-normalize": "phone", "description": "Israeli phone number, digits only, e.g. 0541234567"}


def fn(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "parameters": {"type": "object", "properties": properties, "required": required},
    }


TOOLS: dict[str, dict[str, Any]] = {
    t["name"]: t
    for t in [
        fn("get_weather", "Get the weather forecast for a city.",
           {"city": CITY, "date": {**DATE, "description": "Forecast date, YYYY-MM-DD. Defaults to today."},
            "units": {"type": "string", "enum": ["celsius", "fahrenheit"], "default": "celsius"}},
           ["city"]),
        fn("convert_currency", "Convert an amount between currencies at today's rate.",
           {"amount": {"type": "number", "description": "Amount to convert"},
            "from_currency": {"type": "string", "enum": CURRENCIES, "description": "ISO 4217 code"},
            "to_currency": {"type": "string", "enum": CURRENCIES, "description": "ISO 4217 code"}},
           ["amount", "from_currency", "to_currency"]),
        fn("book_train", "Book Israel Railways tickets.",
           {"origin": {"type": "string", "enum": STATIONS}, "destination": {"type": "string", "enum": STATIONS},
            "date": DATE, "time": {**TIME, "description": "Departure time, 24-hour HH:MM"},
            "passengers": {"type": "integer", "default": 1}},
           ["origin", "destination", "date", "time"]),
        fn("convert_hebrew_date", "Convert a Hebrew (Jewish calendar) date to a Gregorian date.",
           {"year": {"type": "integer", "description": "Hebrew year as a number, e.g. 5787"},
            "month": {"type": "string", "enum": HEBREW_MONTHS},
            "day": {"type": "integer", "description": "Day of the month, 1-30"}},
           ["year", "month", "day"]),
        fn("get_holiday_date", "Get the Gregorian date of a Jewish or Israeli holiday in a given year.",
           {"holiday": {"type": "string", "enum": HOLIDAYS},
            "gregorian_year": {"type": "integer", "description": "Gregorian year, e.g. 2027"}},
           ["holiday", "gregorian_year"]),
        fn("get_shabbat_times", "Get candle-lighting and havdalah times for the Shabbat of a given week.",
           {"city": CITY, "date": {**DATE, "description": "Any date in the target week, YYYY-MM-DD. Defaults to this week."}},
           ["city"]),
        fn("create_event", "Create a calendar event.",
           {"title": {"type": "string", "description": "Event title, in the user's language"},
            "date": DATE, "start_time": TIME,
            "duration_minutes": {"type": "integer", "default": 60},
            "attendees": {"type": "array", "items": {"type": "string"}, "description": "Attendee email addresses"}},
           ["title", "date", "start_time"]),
        fn("set_reminder", "Set a reminder.",
           {"text": {"type": "string", "description": "Reminder text, in the user's language"},
            "datetime": {"type": "string", "format": "date-time", "description": "ISO 8601 local time, YYYY-MM-DDTHH:MM"}},
           ["text", "datetime"]),
        fn("send_bit", "Send money with the Bit payment app.",
           {"phone": PHONE, "amount_ils": {"type": "number", "description": "Amount in shekels"},
            "note": {"type": "string", "description": "Optional note shown to the recipient"}},
           ["phone", "amount_ils"]),
        fn("send_sms", "Send a text message.",
           {"phone": PHONE, "text": {"type": "string", "description": "Message text, verbatim"}},
           ["phone", "text"]),
        fn("calculate_vat", "Compute Israeli VAT (18%) for an amount.",
           {"amount_ils": {"type": "number"},
            "includes_vat": {"type": "boolean", "description": "true if the amount already includes VAT"}},
           ["amount_ils", "includes_vat"]),
        fn("search_restaurants", "Search restaurants.",
           {"city": CITY,
            "cuisine": {"type": "string", "enum": ["italian", "japanese", "israeli", "mediterranean", "yemenite",
                                                     "ethiopian", "georgian", "burgers", "vegan", "asian", "meat", "fish"]},
            "kosher": {"type": "boolean"},
            "max_price_per_person_ils": {"type": "number"}},
           ["city"]),
        fn("translate_text", "Translate text into a target language.",
           {"text": {"type": "string", "description": "Text to translate, verbatim"},
            "target_language": {"type": "string", "enum": ["he", "en", "ar", "ru", "fr", "es", "am"],
                                "description": "ISO 639-1 code"}},
           ["text", "target_language"]),
        fn("find_contact", "Look up a contact in the phone book.",
           {"name": {"type": "string", "description": "Contact name in Latin script as stored, e.g. 'Yossi Levi'"}},
           ["name"]),
        fn("get_stock_quote", "Get the latest price of a stock.",
           {"ticker": {"type": "string", "description": "Ticker symbol in Latin letters, e.g. 'TEVA'"}},
           ["ticker"]),
        fn("check_flight_status", "Check the status of a flight.",
           {"flight_number": {"type": "string", "description": "IATA flight number, e.g. 'LY001'"},
            "date": {**DATE, "description": "Flight date, YYYY-MM-DD. Defaults to today."}},
           ["flight_number"]),
        fn("loan_payment", "Compute the monthly payment of a fixed-rate loan or mortgage.",
           {"principal_ils": {"type": "number"},
            "annual_rate_percent": {"type": "number", "description": "Annual interest rate, e.g. 4.5 for 4.5%"},
            "years": {"type": "integer"}},
           ["principal_ils", "annual_rate_percent", "years"]),
        fn("set_ac", "Control a smart air conditioner.",
           {"room": {"type": "string", "enum": ["living_room", "bedroom", "kids_room", "office"]},
            "temperature_c": {"type": "integer"},
            "mode": {"type": "string", "enum": ["cool", "heat", "fan", "dry"]}},
           ["room", "temperature_c", "mode"]),
        fn("book_doctor", "Book a clinic appointment with the health fund (kupat holim).",
           {"specialty": {"type": "string", "enum": ["family", "pediatrics", "dermatology", "orthopedics",
                                                       "gynecology", "ent", "ophthalmology"]},
            "date": DATE, "time": TIME, "city": CITY},
           ["specialty", "date", "time", "city"]),
        fn("pay_bill", "Pay a household bill.",
           {"provider": {"type": "string", "enum": ["electric_company", "water", "arnona", "bezeq", "internet", "gas"]},
            "account_number": {"type": "string", "description": "Account number exactly as on the bill"},
            "amount_ils": {"type": "number"}},
           ["provider", "account_number", "amount_ils"]),
        fn("track_package", "Track an Israel Post package.",
           {"tracking_number": {"type": "string", "description": "Tracking number, e.g. 'RR123456789IL'"}},
           ["tracking_number"]),
        fn("get_bus_arrivals", "Get real-time bus arrivals at a stop.",
           {"stop_code": {"type": "integer", "description": "Station code"},
            "line": {"type": "string", "description": "Line number, e.g. '480'"}},
           ["stop_code"]),
        fn("register_class", "Register for a class at the community center.",
           {"full_name": {"type": "string", "description": "Full name exactly as the user wrote it"},
            "gender": {"type": "string", "enum": ["male", "female"], "description": "Used to assign changing rooms"},
            "class_name": {"type": "string", "enum": ["yoga", "pilates", "spinning", "swimming", "krav_maga"]}},
           ["full_name", "gender", "class_name"]),
        fn("send_greeting", "Send a greeting card. The text is generated with correct Hebrew grammatical gender.",
           {"recipient_name": {"type": "string", "description": "Recipient name exactly as the user wrote it"},
            "recipient_gender": {"type": "string", "enum": ["male", "female"]},
            "occasion": {"type": "string", "enum": ["birthday", "wedding", "new_baby", "holiday", "get_well", "graduation"]}},
           ["recipient_name", "recipient_gender", "occasion"]),
    ]
}
