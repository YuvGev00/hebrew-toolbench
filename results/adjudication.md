# Adjudication: items failed by all of claude-sonnet-5-5, models/gemini-3.5-flash

11 of 800 items.

## irrelevance_019 (v0, near_miss)

- question: מה שעת השקיעה היום בתל אביב?
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "get_shabbat_times", "arguments": {"city": "Tel Aviv", "date": "2026-10-20"}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "get_shabbat_times", "arguments": {"date": "2026-10-20", "city": "Tel Aviv"}}]`

## irrelevance_039 (pack_gov, near_miss)

- question: תדווח לחברת החשמל שעמוד חשמל נפל ברחוב התאנה בבית שמש
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "check_power_outage", "arguments": {"city": "Beit Shemesh", "street": "התאנה"}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "check_power_outage", "arguments": {"city": "Beit Shemesh", "street": "התאנה"}}]`

## irrelevance_065 (pack_transport, near_miss, mixed_direction)

- question: תשלח לי את כרטיס העלייה למטוס של LY 315
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "check_flight_status", "arguments": {"flight_number": "LY315", "date": "2026-10-20"}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "check_flight_status", "arguments": {"flight_number": "LY315"}}]`

## irrelevance_079 (pack_money, near_miss)

- question: כמה עולה ליטר בנזין 98?
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "get_fuel_price", "arguments": {"fuel": "gasoline_95"}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "get_fuel_price", "arguments": {"month": "2026-10", "fuel": "gasoline_95"}}]`

## irrelevance_090 (pack_money, near_miss)

- question: תקנה לי 10 מניות של טבע
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "get_stock_quote", "arguments": {"ticker": "TEVA"}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "get_stock_quote", "arguments": {"ticker": "TEVA"}}]`

## irrelevance_128 (pack_culture, near_miss, hebrew_calendar)

- question: מתי חג הסיגד ב-2027?
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "get_holiday_date", "arguments": {"holiday": "yom_kippur", "gregorian_year": 2027}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "get_holiday_date", "arguments": {"gregorian_year": 2027, "holiday": "yom_kippur"}}]`

## irrelevance_129 (pack_culture, near_miss, hebrew_calendar)

- question: מתי ט״ו באב ב-2027?
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "get_holiday_date", "arguments": {"holiday": "tisha_bav", "gregorian_year": 2027}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "get_holiday_date", "arguments": {"gregorian_year": 2027, "holiday": "tisha_bav"}}]`

## irrelevance_135 (pack_culture, near_miss, hebrew_calendar, date_ddmm)

- question: מה התאריך העברי של 25/12/2026?
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "convert_hebrew_date", "arguments": {"year": 5787, "month": "Tevet", "day": 15}}, {"name": "convert_hebrew_date", "arguments": {"year": 5787, "month": "Tevet", "day": 16}}, {"name": "convert_hebrew_date", "arguments": {"year": 5787, "month": "Tevet", "day": 17}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "convert_hebrew_date", "arguments": {"year": 5787, "month": "Tevet", "day": 15}}]`

## irrelevance_137 (pack_culture, near_miss)

- question: באיזה מקום הפועל באר שבע בטבלה?
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "get_sports_score", "arguments": {"team": "Hapoel Beer Sheva", "sport": "football"}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "get_sports_score", "arguments": {"sport": "football", "team": "Hapoel Beer Sheva"}}]`

## irrelevance_138 (pack_culture, near_miss, hebrew_calendar)

- question: מתי ראש חודש טבת?
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "get_holiday_date", "arguments": {"holiday": "hanukkah", "gregorian_year": 2026}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "get_holiday_date", "arguments": {"gregorian_year": 2026, "holiday": "hanukkah"}}]`

## irrelevance_142 (pack_culture, missing_info)

- question: מתי השקיעה היום?
- gold: `[]`
- claude-sonnet-5-5 (called_when_irrelevant): `[{"name": "get_zmanim", "arguments": {"city": "Jerusalem", "zman": "sunset", "date": "2026-10-20"}}]`
- models/gemini-3.5-flash (called_when_irrelevant): `[{"name": "get_zmanim", "arguments": {"city": "Jerusalem", "date": "2026-10-20", "zman": "sunset"}}, {"name": "get_zmanim", "arguments": {"zman": "sunset", "date": "2026-10-20", "city": "Tel Aviv"}}]`

