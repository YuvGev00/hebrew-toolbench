"""Build data/seed_v0.jsonl from the hand-written items below.

All items are written natively in Hebrew for this benchmark (no translation of
BFCL or any other dataset). Relative dates resolve against REFERENCE_DATE,
which every item states in its system prompt.

Run: uv run python scripts/build_seed.py
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from tools import TOOLS

REFERENCE_DATE = dt.date(2026, 10, 20)  # Tuesday, 9 Cheshvan 5787
SYSTEM = "התאריך היום: יום שלישי, 20 באוקטובר 2026 (ט׳ בחשוון תשפ״ז). השעה 09:00. המשתמש נמצא בישראל."
OUT = Path(__file__).resolve().parent.parent / "data" / "seed_v0.jsonl"


def d(days: int) -> str:
    return (REFERENCE_DATE + dt.timedelta(days=days)).isoformat()


TODAY, TOMORROW = d(0), d(1)
THU, FRI, SAT, SUN, MON = d(2), d(3), d(4), d(5), d(6)
THIS_WEEK: list[str | None] = [None, *(d(n) for n in range(-2, 5))]  # Sun 18/10 - Sat 24/10

CITY = {
    "TA": ["Tel Aviv", "Tel Aviv-Yafo", "Tel Aviv-Jaffa", "Tel Aviv Yafo"],
    "JLM": ["Jerusalem"],
    "HFA": ["Haifa"],
    "BS": ["Beer Sheva", "Be'er Sheva", "Beersheba", "Beer-Sheva", "Be'er-Sheva"],
    "ETH": ["Eilat"],
    "SFD": ["Safed", "Tzfat", "Zefat", "Tsfat", "Zfat", "Tzefat"],
    "KS": ["Kiryat Shmona", "Qiryat Shemona", "Kiryat Shemona"],
    "PT": ["Petah Tikva", "Petah Tikvah", "Petach Tikva", "Petach Tikvah"],
    "KFS": ["Kfar Saba", "Kefar Sava", "Kfar Sava"],
    "HRZ": ["Herzliya", "Herzliyya", "Herzlia"],
    "ACRE": ["Acre", "Akko", "Acco"],
    "RHA": ["Rosh HaAyin", "Rosh Ha'Ayin", "Rosh Haayin", "Rosh Ha-Ayin"],
    "TIB": ["Tiberias", "Tverya"],
    "NAH": ["Nahariya", "Nahariyya"],
    "DIM": ["Dimona"],
}

Gold = dict[str, Any]


def call(name: str, /, **args: Any) -> Gold:
    """A gold call. Each argument is a list of acceptable values; None = may be omitted."""
    assert name in TOOLS, name
    return {"name": name, "arguments": {k: v if isinstance(v, list) else [v] for k, v in args.items()}}


ITEMS: list[tuple[str, list[str], str, list[str], list[Gold]]] = []


def add(category: str, tags: list[str], question: str, tools: list[str], *gold: Gold) -> None:
    ITEMS.append((category, tags, question, tools, list(gold)))


def simple(tags: list[str], question: str, gold: Gold) -> None:
    add("simple", tags, question, [gold["name"]], gold)


# --- simple: one tool offered, one call expected -------------------------------------------
simple(["canonical_value", "date_relative"], "מה מזג האוויר מחר בתל אביב?",
       call("get_weather", city=CITY["TA"], date=TOMORROW))
simple(["canonical_value", "date_relative"], "יהיה גשם בירושלים ביום חמישי?",
       call("get_weather", city=CITY["JLM"], date=THU))
simple(["canonical_value"], "כמה מעלות יהיו היום באילת? תן לי בפרנהייט",
       call("get_weather", city=CITY["ETH"], date=[None, TODAY], units="fahrenheit"))
simple(["canonical_value", "date_ddmm"], "תבדוק לי את התחזית לבאר שבע ב-3/11",
       call("get_weather", city=CITY["BS"], date="2026-11-03"))
simple(["canonical_value", "date_relative"], "מה התחזית לצפת לשבת הקרובה?",
       call("get_weather", city=CITY["SFD"], date=SAT))
simple(["canonical_value"], "קר היום בקריית שמונה?",
       call("get_weather", city=CITY["KS"], date=[None, TODAY]))
simple(["currency_ils", "canonical_value"], "כמה זה 200 דולר בשקלים?",
       call("convert_currency", amount=200, from_currency="USD", to_currency="ILS"))
simple(["currency_ils", "number_format"], "תמיר לי 1,250 ₪ ליורו",
       call("convert_currency", amount=1250, from_currency="ILS", to_currency="EUR"))
simple(["currency_ils", "number_words"], "כמה ין יפני אני מקבל על שלושת אלפים וחמש מאות שקל?",
       call("convert_currency", amount=3500, from_currency="ILS", to_currency="JPY"))
simple(["currency_ils", "number_words"], "תמיר חצי מיליון שקל לפרנק שוויצרי",
       call("convert_currency", amount=500000, from_currency="ILS", to_currency="CHF"))
simple(["currency_ils", "canonical_value"], "כמה שווים 75 פאונד בש״ח?",
       call("convert_currency", amount=75, from_currency="GBP", to_currency="ILS"))
simple(["canonical_value", "number_words", "date_relative", "time_words"],
       "תזמין לי שני כרטיסים לרכבת מתל אביב סבידור לירושלים יצחק נבון מחר בשמונה בבוקר",
       call("book_train", origin="Tel Aviv Savidor Center", destination="Jerusalem Yitzhak Navon",
            date=TOMORROW, time="08:00", passengers=2))
simple(["canonical_value", "date_relative"], "רכבת מחיפה חוף הכרמל לנתב״ג ביום ראשון ב-5:40 לפנות בוקר",
       call("book_train", origin="Haifa Hof HaCarmel", destination="Ben Gurion Airport",
            date=SUN, time="05:40", passengers=[None, 1]))
simple(["canonical_value", "date_ddmm", "time_words"], "כרטיס אחד מבאר שבע מרכז לתל אביב השלום ב-12/11 בשמונה וחצי בערב",
       call("book_train", origin="Beer Sheva Center", destination="Tel Aviv HaShalom",
            date="2026-11-12", time="20:30", passengers=[None, 1]))
simple(["canonical_value", "number_words", "time_words"], "אנחנו שלושה, תזמין רכבת ממודיעין מרכז לנהריה מחרתיים ברבע לעשר בבוקר",
       call("book_train", origin="Modiin Center", destination="Nahariya", date=THU, time="09:45", passengers=3))
simple(["hebrew_calendar", "gematria"], "איזה תאריך לועזי יוצא ט״ו בשבט תשפ״ז?",
       call("convert_hebrew_date", year=5787, month="Shevat", day=15))
simple(["hebrew_calendar", "gematria"], "נולדתי בי״ז בתמוז תשנ״ה. איזה תאריך לועזי זה?",
       call("convert_hebrew_date", year=5755, month="Tammuz", day=17))
simple(["hebrew_calendar", "gematria"], "ה׳ באייר תש״ח – מה התאריך הלועזי?",
       call("convert_hebrew_date", year=5708, month="Iyar", day=5))
simple(["hebrew_calendar", "gematria"], "בר המצווה של הבן שלי בח׳ באלול תשפ״ז. מה התאריך בלוח הלועזי?",
       call("convert_hebrew_date", year=5787, month="Elul", day=8))
simple(["hebrew_calendar", "gematria", "leap_year"], "מה התאריך הלועזי של י״ד באדר ב׳ תשפ״ז?",
       call("convert_hebrew_date", year=5787, month="Adar II", day=14))
simple(["hebrew_calendar", "gematria", "inference"], "החתונה שלנו בל״ג בעומר תשפ״ח, איזה תאריך לועזי זה יוצא?",
       call("convert_hebrew_date", year=5788, month="Iyar", day=18))
simple(["hebrew_calendar", "gematria"], "האזכרה של סבא בכ״ט באב תשפ״ז, תמיר לי לתאריך לועזי",
       call("convert_hebrew_date", year=5787, month="Av", day=29))
simple(["hebrew_calendar", "inference"], "מתי יוצא ט״ו באב הקרוב בתאריך לועזי?",
       call("convert_hebrew_date", year=5787, month="Av", day=15))
simple(["hebrew_calendar", "canonical_value"], "באיזה תאריך יוצא יום כיפור ב-2027?",
       call("get_holiday_date", holiday="yom_kippur", gregorian_year=2027))
simple(["hebrew_calendar", "canonical_value"], "מתי מדליקים נר ראשון של חנוכה בשנת 2026?",
       call("get_holiday_date", holiday="hanukkah", gregorian_year=2026))
simple(["hebrew_calendar", "canonical_value"], "מתי יום העצמאות 2028?",
       call("get_holiday_date", holiday="yom_haatzmaut", gregorian_year=2028))
simple(["hebrew_calendar", "canonical_value"], "מתי ליל הסדר ב-2027?",
       call("get_holiday_date", holiday="passover", gregorian_year=2027))
simple(["hebrew_calendar", "canonical_value"], "מתי כניסת שבת השבוע בחיפה?",
       call("get_shabbat_times", city=CITY["HFA"], date=THIS_WEEK))
simple(["hebrew_calendar", "date_ddmm"], "מה שעת הדלקת נרות בירושלים לשבת של ה-6/11?",
       call("get_shabbat_times", city=CITY["JLM"], date=[f"2026-11-0{n}" for n in range(1, 8)]))
simple(["mixed_direction", "date_relative", "free_text_hebrew"],
       "תקבע פגישה בשם 'סקירה רבעונית' ביום חמישי בעשר בבוקר, לשעה וחצי, עם dana.cohen@acme.co.il",
       call("create_event", title="סקירה רבעונית", date=THU, start_time="10:00", duration_minutes=90,
            attendees=[["dana.cohen@acme.co.il"]]))
simple(["date_relative", "free_text_hebrew"], "תכניס ליומן 'ארוחת ערב משפחתית' ביום שישי ב-19:30",
       call("create_event", title="ארוחת ערב משפחתית", date=FRI, start_time="19:30", duration_minutes=[None, 60]))
simple(["mixed_direction", "gender_addressee", "date_ddmm", "time_words"],
       "קבעי לי 'שיחת עבודה עם Microsoft' ב-4.11 בשלוש אחר הצהריים, לחצי שעה",
       call("create_event", title="שיחת עבודה עם Microsoft", date="2026-11-04", start_time="15:00", duration_minutes=30))
simple(["hebrew_calendar", "calendar_compute"], "תוסיף ליומן 'יום הולדת לנועה' בא׳ בכסלו תשפ״ז בשמונה בערב",
       call("create_event", title="יום הולדת לנועה", date="2026-11-11", start_time="20:00", duration_minutes=[None, 60]))
simple(["date_relative", "free_text_hebrew"], "תזכיר לי מחר בשבע בבוקר: 'לקחת את התרופה'",
       call("set_reminder", text="לקחת את התרופה", datetime=f"{TOMORROW}T07:00"))
simple(["date_relative", "gender_addressee"], "תזכירי לי בעוד שבועיים ב-9:00 'לחדש את הדרכון'",
       call("set_reminder", text="לחדש את הדרכון", datetime=f"{d(14)}T09:00"))
simple(["date_relative", "time_words"], "תזכורת ליום ראשון הבא ברבע לשמונה בערב: 'להוציא את הזבל'",
       call("set_reminder", text="להוציא את הזבל", datetime=f"{SUN}T19:45"))
simple(["currency_ils", "mixed_direction"], "תעביר 150 ש״ח בביט ל-054-1234567 עם ההערה 'פיצה'",
       call("send_bit", phone="0541234567", amount_ils=150, note="פיצה"))
simple(["mixed_direction", "free_text_hebrew"], "שלח לאמא, 052-7654321, הודעה: 'אני בדרך הביתה'",
       call("send_sms", phone="0527654321", text="אני בדרך הביתה"))
simple(["currency_ils", "number_words", "mixed_direction"], "תשלם בביט מאתיים וחמישים שקל ל-+972-50-111-2233",
       call("send_bit", phone="0501112233", amount_ils=250))
simple(["mixed_direction", "gender_addressee"], "שלחי SMS ל-058-9990000: 'הפגישה נדחתה ל-14:00'",
       call("send_sms", phone="0589990000", text="הפגישה נדחתה ל-14:00"))
simple(["currency_ils", "number_format"], "כמה מע״מ יש בחשבונית של 1,180 ש״ח כולל מע״מ?",
       call("calculate_vat", amount_ils=1180, includes_vat=True))
simple(["currency_ils", "number_format"], "מחיר לפני מע״מ הוא 2,500 ₪. כמה זה יוצא כולל?",
       call("calculate_vat", amount_ils=2500, includes_vat=False))
simple(["canonical_value", "currency_ils"], "תמצא לי מסעדה איטלקית כשרה בירושלים עד 120 ש״ח לסועד",
       call("search_restaurants", city=CITY["JLM"], cuisine="italian", kosher=True, max_price_per_person_ils=120))
simple(["canonical_value"], "איפה אפשר לאכול אוכל תימני בראש העין?",
       call("search_restaurants", city=CITY["RHA"], cuisine="yemenite"))
simple(["canonical_value"], "חפש מסעדה טבעונית בחיפה",
       call("search_restaurants", city=CITY["HFA"], cuisine="vegan"))
simple(["canonical_value", "free_text_hebrew"], "תתרגם לאנגלית: 'בוקר טוב לכולם'",
       call("translate_text", text="בוקר טוב לכולם", target_language="en"))
simple(["canonical_value", "free_text_hebrew"], "איך אומרים 'תודה רבה על העזרה' בערבית?",
       call("translate_text", text="תודה רבה על העזרה", target_language="ar"))
simple(["canonical_value", "free_text_hebrew"], "תרגם לרוסית את המשפט 'הרכבת מאחרת בעשר דקות'",
       call("translate_text", text="הרכבת מאחרת בעשר דקות", target_language="ru"))
simple(["transliteration"], "תמצא לי את המספר של יוסי לוי",
       call("find_contact", name=["Yossi Levi", "Yosi Levi", "Yossi Levy", "Yosi Levy"]))
simple(["transliteration"], "חפש באנשי הקשר את חיים כהן",
       call("find_contact", name=["Haim Cohen", "Chaim Cohen", "Hayim Cohen", "Khaim Cohen", "Haim Kohen", "Chaim Kohen"]))
simple(["transliteration"], "מה הטלפון של צחי בן חמו?",
       call("find_contact", name=["Tzachi Ben Hamo", "Tsachi Ben Hamo", "Tzahi Ben Hamo", "Tsahi Ben Hamo",
                                  "Tzachi Ben-Hamo", "Tzahi Ben-Hamo", "Tzachi Ben Chamo", "Tzahi Ben Chamo"]))
simple(["transliteration", "canonical_value"], "מה מחיר המניה של טבע?",
       call("get_stock_quote", ticker="TEVA"))
simple(["transliteration", "canonical_value"], "כמה עולה מניה של אלביט מערכות?",
       call("get_stock_quote", ticker=["ESLT", "ESLT.TA"]))
simple(["transliteration", "canonical_value"], "תבדוק את השער של צ׳ק פוינט",
       call("get_stock_quote", ticker="CHKP"))
simple(["canonical_value", "transliteration"], "מה הסטטוס של טיסת אל על 001 היום?",
       call("check_flight_status", flight_number=["LY001", "LY1", "LY 001", "LY 1"], date=[None, TODAY]))
simple(["mixed_direction", "date_relative"], "הטיסה של ישראייר 6H863 ממריאה בזמן מחר?",
       call("check_flight_status", flight_number=["6H863", "6H 863"], date=TOMORROW))
simple(["currency_ils", "number_words"],
       "כמה יהיה ההחזר החודשי על משכנתא של מיליון ומאתיים אלף שקל ל-25 שנה בריבית של 4.5%?",
       call("loan_payment", principal_ils=1200000, annual_rate_percent=4.5, years=25))
simple(["canonical_value"], "תדליק את המזגן בסלון על 24 מעלות בקירור",
       call("set_ac", room="living_room", temperature_c=24, mode="cool"))
simple(["canonical_value", "date_relative"], "תקבע לי תור לרופא עור ביום ראשון ב-16:15 בפתח תקווה",
       call("book_doctor", specialty="dermatology", date=SUN, time="16:15", city=CITY["PT"]))
simple(["mixed_direction", "currency_ils", "number_format"], "תשלם את הארנונה: מספר חשבון 4471-22-A, סכום 1,340.50 ₪",
       call("pay_bill", provider="arnona", account_number="4471-22-A", amount_ils=1340.5))
simple(["bidi_controls", "mixed_direction"], "מה מצב החבילה \u200fRR123456789IL\u200f?",
       call("track_package", tracking_number="RR123456789IL"))
simple(["mixed_direction"], "מתי מגיע קו 480 לתחנה 21345?",
       call("get_bus_arrivals", stop_code=21345, line="480"))
simple(["gender_morphology", "free_text_hebrew"], "קוראים לי טל כהן ואני מתעניינת בשיעור פילאטיס, תרשום אותי",
       call("register_class", full_name="טל כהן", gender="female", class_name="pilates"))
simple(["gender_morphology"], "תשלח ברכת יום הולדת לחן, היא חוגגת 30 היום",
       call("send_greeting", recipient_name="חן", recipient_gender="female", occasion="birthday"))


def multiple(tags: list[str], question: str, tools: list[str], gold: Gold) -> None:
    assert gold["name"] in tools
    add("multiple", tags, question, tools, gold)


# --- multiple: 3 tools offered, pick the right one -------------------------------------------
CAL = ["get_weather", "get_shabbat_times", "get_holiday_date"]
DATES = ["convert_hebrew_date", "get_holiday_date", "create_event"]
MONEY = ["convert_currency", "calculate_vat", "loan_payment"]
TRAVEL = ["book_train", "check_flight_status", "get_bus_arrivals"]
COMMS = ["send_sms", "send_bit", "find_contact"]
HOME = ["set_ac", "get_weather", "set_reminder"]
HEALTH = ["book_doctor", "create_event", "set_reminder"]
SOCIAL = ["register_class", "send_greeting", "create_event"]
MARKETS = ["get_stock_quote", "convert_currency", "calculate_vat"]

multiple(["hebrew_calendar"], "מתי יוצאת השבת השבוע בתל אביב?", CAL,
         call("get_shabbat_times", city=CITY["TA"], date=THIS_WEEK))
multiple(["currency_ils", "number_format"], "חשבונית של 3,540 ₪ כולל מע״מ – כמה מתוכה זה מע״מ?", MONEY,
         call("calculate_vat", amount_ils=3540, includes_vat=True))
multiple(["canonical_value", "date_ddmm", "time_words"], "תזמין רכבת מנתניה לאשדוד עד הלום ב-8/11 בשבע ועשרים בבוקר", TRAVEL,
         call("book_train", origin="Netanya", destination="Ashdod Ad Halom", date="2026-11-08", time="07:20",
              passengers=[None, 1]))
multiple(["hebrew_calendar", "canonical_value"], "מתי פורים 2027?", DATES,
         call("get_holiday_date", holiday="purim", gregorian_year=2027))
multiple(["hebrew_calendar", "gematria"], "מה התאריך הלועזי של א׳ בניסן תשפ״ז?", DATES,
         call("convert_hebrew_date", year=5787, month="Nisan", day=1))
multiple(["currency_ils", "number_words", "mixed_direction"], "תעביר שמונים ושבעה שקל לרוני ב-053-4445566", COMMS,
         call("send_bit", phone="0534445566", amount_ils=87))
multiple(["mixed_direction", "free_text_hebrew"], "תשלח הודעה ל-050-2223344: 'נפגשים בקפה ב-10'", ["send_sms", "send_bit", "set_reminder"],
         call("send_sms", phone="0502223344", text="נפגשים בקפה ב-10"))
multiple(["canonical_value", "free_text_hebrew"], "תתרגם לצרפתית 'איפה התחנה המרכזית?'", ["translate_text", "find_contact", "send_sms"],
         call("translate_text", text="איפה התחנה המרכזית?", target_language="fr"))
multiple(["transliteration"], "מה המחיר של מניית נייס?", MARKETS,
         call("get_stock_quote", ticker=["NICE", "NICE.TA"]))
multiple(["mixed_direction", "date_relative"], "תבדוק אם טיסה LY 315 מחר יוצאת בזמן", ["check_flight_status", "book_train", "get_weather"],
         call("check_flight_status", flight_number=["LY315", "LY 315"], date=TOMORROW))
multiple(["canonical_value"], "חם לי בחדר השינה, תוריד ל-22 בקירור", HOME,
         call("set_ac", room="bedroom", temperature_c=22, mode="cool"))
multiple(["canonical_value", "number_words"], "תחמם את חדר הילדים לעשרים ושתיים מעלות", HOME,
         call("set_ac", room="kids_room", temperature_c=22, mode="heat"))
multiple(["canonical_value", "date_relative"], "תקבע לבת שלי תור לרופא ילדים בכפר סבא ביום שני ב-8:30", HEALTH,
         call("book_doctor", specialty="pediatrics", date=MON, time="08:30", city=CITY["KFS"]))
multiple(["canonical_value", "date_ddmm", "gender_morphology"], "אני צריכה תור לרופאת נשים בהרצליה, ב-10.11 בשתיים בצהריים", HEALTH,
         call("book_doctor", specialty="gynecology", date="2026-11-10", time="14:00", city=CITY["HRZ"]))
multiple(["mixed_direction", "currency_ils"], "תשלם חשבון חשמל, חוזה מספר 346-5512-9, סכום 612 שקל", ["pay_bill", "send_bit", "calculate_vat"],
         call("pay_bill", provider="electric_company", account_number="346-5512-9", amount_ils=612))
multiple(["mixed_direction"], "המשלוח שלי (מספר: LX998877665IL) עוד לא הגיע, תבדוק איפה הוא", ["track_package", "check_flight_status", "pay_bill"],
         call("track_package", tracking_number="LX998877665IL"))
multiple([], "עוד כמה זמן מגיע אוטובוס לתחנה 32891?", TRAVEL,
         call("get_bus_arrivals", stop_code=32891, line=[None]))
multiple(["gender_morphology", "free_text_hebrew"], "אני רוצה להירשם לספינינג, אני חדש פה. השם שלי עדי מזרחי", SOCIAL,
         call("register_class", full_name="עדי מזרחי", gender="male", class_name="spinning"))
multiple(["gender_morphology"], "תכתוב ברכה ליובל שסיים את התואר", ["send_greeting", "send_sms", "create_event"],
         call("send_greeting", recipient_name="יובל", recipient_gender="male", occasion="graduation"))
multiple(["gender_morphology", "gender_addressee"], "תשלחי ברכה לגל שילדה בן", ["send_greeting", "send_sms", "create_event"],
         call("send_greeting", recipient_name="גל", recipient_gender="female", occasion="new_baby"))
multiple(["gender_morphology", "free_text_hebrew"], "שמי שחר אברהם, אני רוצה להירשם לקרב מגע, אני מתחילה מאפס", SOCIAL,
         call("register_class", full_name="שחר אברהם", gender="female", class_name="krav_maga"))
multiple(["canonical_value", "inference"], "תמצא מקום לאכול סושי בהרצליה", ["search_restaurants", "get_weather", "book_train"],
         call("search_restaurants", city=CITY["HRZ"], cuisine="japanese"))
multiple(["canonical_value", "currency_ils"], "בא לי בשרים, משהו לא כשר באילת עד 200 שקל לבנאדם", ["search_restaurants", "get_weather", "book_train"],
         call("search_restaurants", city=CITY["ETH"], cuisine="meat", kosher=False, max_price_per_person_ils=200))
multiple(["transliteration"], "מה המספר של אביטל שושני?", COMMS,
         call("find_contact", name=["Avital Shoshani", "Avital Shushani"]))
multiple(["transliteration"], "תחפש את שרון אוחיון בטלפון", COMMS,
         call("find_contact", name=["Sharon Ohayon", "Sharon Ohayun", "Sharon Ohion", "Sharon Ochayon"]))
multiple(["currency_ils", "number_words"], "הלוואה של 80 אלף שקל לחמש שנים בריבית 6.2 אחוז – כמה אשלם בחודש?", MONEY,
         call("loan_payment", principal_ils=80000, annual_rate_percent=6.2, years=5))
multiple(["canonical_value", "date_relative"], "תביא לי תחזית לעכו לעוד שבוע", ["get_weather", "get_shabbat_times", "check_flight_status"],
         call("get_weather", city=CITY["ACRE"], date=d(7)))
multiple(["date_ddmm", "time_words", "free_text_hebrew"], "תכניס ליומן 'אסיפת הורים' ב-17/11 בשש וחצי בערב", HEALTH,
         call("create_event", title="אסיפת הורים", date="2026-11-17", start_time="18:30", duration_minutes=[None, 60]))
multiple(["date_relative", "time_words", "free_text_hebrew"], "תזכיר לי מחרתיים ב-12 בצהריים 'לשלם ביטוח לאומי'",
         ["set_reminder", "create_event", "send_sms"],
         call("set_reminder", text="לשלם ביטוח לאומי", datetime=f"{THU}T12:00"))
multiple(["canonical_value", "number_format"], "יש לי 2,000 יורו, כמה זה בדולרים?", MARKETS,
         call("convert_currency", amount=2000, from_currency="EUR", to_currency="USD"))
multiple(["transliteration"], "מה המצב של בנק לאומי בבורסה?", MARKETS,
         call("get_stock_quote", ticker=["LUMI", "LUMI.TA"]))
multiple(["hebrew_calendar", "gematria"], "באיזה תאריך לועזי יוצא י׳ בטבת תשפ״ז?", DATES,
         call("convert_hebrew_date", year=5787, month="Tevet", day=10))


def parallel(tags: list[str], question: str, tools: list[str], *gold: Gold) -> None:
    assert len(gold) > 1
    add("parallel", tags, question, tools, *gold)


# --- parallel: several calls in one turn (same or different functions) ------------------------
W = "get_weather"
parallel(["canonical_value", "date_relative"], "מה מזג האוויר מחר בתל אביב, בחיפה ובאילת?", [W],
         call(W, city=CITY["TA"], date=TOMORROW), call(W, city=CITY["HFA"], date=TOMORROW), call(W, city=CITY["ETH"], date=TOMORROW))
parallel(["currency_ils"], "כמה זה 100 דולר ו-100 יורו בשקלים?", ["convert_currency"],
         call("convert_currency", amount=100, from_currency="USD", to_currency="ILS"),
         call("convert_currency", amount=100, from_currency="EUR", to_currency="ILS"))
parallel(["transliteration"], "מה המחיר של טבע ושל אלביט?", ["get_stock_quote"],
         call("get_stock_quote", ticker="TEVA"), call("get_stock_quote", ticker=["ESLT", "ESLT.TA"]))
parallel(["gender_morphology"], "תשלח ברכת חתונה לשחר ולאור – שחר הוא חבר שלי מהצבא, ואור היא בת הזוג שלו",
         ["send_greeting"],
         call("send_greeting", recipient_name="שחר", recipient_gender="male", occasion="wedding"),
         call("send_greeting", recipient_name="אור", recipient_gender="female", occasion="wedding"))
parallel(["canonical_value"], "תכוון את המזגן בסלון ל-23 ובחדר השינה ל-25, שניהם בקירור", ["set_ac"],
         call("set_ac", room="living_room", temperature_c=23, mode="cool"),
         call("set_ac", room="bedroom", temperature_c=25, mode="cool"))
parallel(["hebrew_calendar", "gematria"], "מה התאריכים הלועזיים של ט״ו בשבט ושל ט״ו באב בשנת תשפ״ז?", ["convert_hebrew_date"],
         call("convert_hebrew_date", year=5787, month="Shevat", day=15),
         call("convert_hebrew_date", year=5787, month="Av", day=15))
parallel(["hebrew_calendar"], "מתי חנוכה ומתי פורים בשנת 2027?", ["get_holiday_date"],
         call("get_holiday_date", holiday="hanukkah", gregorian_year=2027),
         call("get_holiday_date", holiday="purim", gregorian_year=2027))
parallel(["transliteration"], "תמצא לי את יוסי לוי ואת דנה כהן באנשי הקשר", ["find_contact"],
         call("find_contact", name=["Yossi Levi", "Yosi Levi", "Yossi Levy", "Yosi Levy"]),
         call("find_contact", name=["Dana Cohen", "Dana Kohen"]))
parallel(["transliteration"], "מה המצב של טיסות אל על 001 ו-002 היום?", ["check_flight_status"],
         call("check_flight_status", flight_number=["LY001", "LY1", "LY 001", "LY 1"], date=[None, TODAY]),
         call("check_flight_status", flight_number=["LY002", "LY2", "LY 002", "LY 2"], date=[None, TODAY]))
parallel(["mixed_direction"], "תבדוק את שתי החבילות שלי: RR111222333IL ו-CP444555666IL", ["track_package"],
         call("track_package", tracking_number="RR111222333IL"), call("track_package", tracking_number="CP444555666IL"))
parallel(["hebrew_calendar"], "מתי נכנסת שבת השבוע בירושלים ובתל אביב?", ["get_shabbat_times"],
         call("get_shabbat_times", city=CITY["JLM"], date=THIS_WEEK),
         call("get_shabbat_times", city=CITY["TA"], date=THIS_WEEK))
parallel(["canonical_value"], "מה מזג האוויר היום בחיפה, טבריה, נהריה ודימונה?", [W],
         *(call(W, city=CITY[c], date=[None, TODAY]) for c in ("HFA", "TIB", "NAH", "DIM")))
parallel(["mixed_direction", "free_text_hebrew"], "תשלח ל-050-1112233 ול-052-4445566 את ההודעה: 'הישיבה בוטלה'", ["send_sms"],
         call("send_sms", phone="0501112233", text="הישיבה בוטלה"), call("send_sms", phone="0524445566", text="הישיבה בוטלה"))
parallel([], "מתי מגיעים קווים 480 ו-947 לתחנה 21345?", ["get_bus_arrivals"],
         call("get_bus_arrivals", stop_code=21345, line="480"), call("get_bus_arrivals", stop_code=21345, line="947"))
parallel(["currency_ils", "mixed_direction"], "תעביר בביט 60 שקל לכל אחד מהם: 054-1110000, 054-2220000, 054-3330000", ["send_bit"],
         *(call("send_bit", phone=p, amount_ils=60) for p in ("0541110000", "0542220000", "0543330000")))
parallel(["canonical_value", "free_text_hebrew"], "תתרגם 'ברוכים הבאים לישראל' לאנגלית ולערבית", ["translate_text"],
         call("translate_text", text="ברוכים הבאים לישראל", target_language="en"),
         call("translate_text", text="ברוכים הבאים לישראל", target_language="ar"))
parallel(["parallel_multiple", "currency_ils"], "מה מזג האוויר באילת מחר, וכמה זה 300 דולר בשקלים?", [W, "convert_currency"],
         call(W, city=CITY["ETH"], date=TOMORROW), call("convert_currency", amount=300, from_currency="USD", to_currency="ILS"))
parallel(["parallel_multiple", "date_relative"],
         "תזמין רכבת מתל אביב סבידור לחיפה חוף הכרמל מחר ב-7:00, ותזכיר לי היום ב-22:00 'להטעין את הרב-קו'",
         ["book_train", "set_reminder"],
         call("book_train", origin="Tel Aviv Savidor Center", destination="Haifa Hof HaCarmel", date=TOMORROW, time="07:00",
              passengers=[None, 1]),
         call("set_reminder", text="להטעין את הרב-קו", datetime=f"{TODAY}T22:00"))
parallel(["parallel_multiple", "mixed_direction", "free_text_hebrew"],
         "תכניס ליומן 'פגישה עם רו״ח' ביום שני ב-11:00, ותשלח לרואה החשבון ב-03-5551234: 'אישרתי את הפגישה ביום שני'",
         ["create_event", "send_sms"],
         call("create_event", title="פגישה עם רו״ח", date=MON, start_time="11:00", duration_minutes=[None, 60]),
         call("send_sms", phone="035551234", text="אישרתי את הפגישה ביום שני"))
parallel(["parallel_multiple", "currency_ils", "number_format"], "מה המחיר של NICE, ותמיר 5,000 ש״ח לדולר",
         ["get_stock_quote", "convert_currency"],
         call("get_stock_quote", ticker=["NICE", "NICE.TA"]),
         call("convert_currency", amount=5000, from_currency="ILS", to_currency="USD"))
parallel(["parallel_multiple", "currency_ils"], "תחשב מע״מ על 850 ש״ח לפני מע״מ, ותעביר בביט 850 ש״ח ל-052-1212121",
         ["calculate_vat", "send_bit"],
         call("calculate_vat", amount_ils=850, includes_vat=False), call("send_bit", phone="0521212121", amount_ils=850))
parallel(["parallel_multiple", "hebrew_calendar", "gematria"], "מתי ראש השנה ב-2027, ומה התאריך הלועזי של ה׳ בתשרי תשפ״ח?",
         ["get_holiday_date", "convert_hebrew_date"],
         call("get_holiday_date", holiday="rosh_hashana", gregorian_year=2027),
         call("convert_hebrew_date", year=5788, month="Tishrei", day=5))
parallel(["gender_morphology", "free_text_hebrew"], "תרשום אותי ואת אשתי לשחייה. אני דן אלון והיא מיכל אלון", ["register_class"],
         call("register_class", full_name="דן אלון", gender="male", class_name="swimming"),
         call("register_class", full_name="מיכל אלון", gender="female", class_name="swimming"))
parallel(["parallel_multiple"], "תבדוק מה מזג האוויר בירושלים היום ותדליק חימום בסלון על 21", [W, "set_ac"],
         call(W, city=CITY["JLM"], date=[None, TODAY]), call("set_ac", room="living_room", temperature_c=21, mode="heat"))


def irrelevant(tags: list[str], question: str, tools: list[str]) -> None:
    add("irrelevance", tags, question, tools)


# --- irrelevance: no offered tool fits; the model must not call any ---------------------------
irrelevant([], "מה מזג האוויר מחר בצפת?", ["convert_currency", "calculate_vat"])
irrelevant(["chitchat"], "ספר לי בדיחה על מתכנתים", ["get_stock_quote"])
irrelevant(["knowledge"], "מי היה ראש הממשלה הראשון של ישראל?", ["get_holiday_date", "convert_hebrew_date"])
irrelevant(["near_miss"], "כמה זה 30 מעלות צלזיוס בפרנהייט?", ["convert_currency"])
irrelevant(["near_miss"], "תעביר 100 דולר לחשבון בנק בגרמניה, IBAN DE89370400440532013000", ["send_bit"])
irrelevant(["near_miss"], "תתרגם 'שלום' ליפנית", ["translate_text"])
irrelevant(["near_miss"], "תדליק את האור בסלון", ["set_ac"])
irrelevant(["near_miss"], "תקבע תור לווטרינר לכלב שלי ביום ראשון", ["book_doctor"])
irrelevant(["near_miss"], "מה השער של ביטקוין בשקלים?", ["convert_currency"])
irrelevant(["near_miss"], "תשלם את הדו״ח חניה שקיבלתי, 250 ש״ח", ["pay_bill"])
irrelevant(["chitchat"], "היי, מה שלומך היום?", ["get_weather", "find_contact"])
irrelevant(["chitchat"], "תכתוב לי שיר קצר על ירושלים", ["get_weather"])
irrelevant(["near_miss"], "כמה עולה נסיעה באוטובוס בירושלים?", ["get_bus_arrivals"])
irrelevant(["missing_info"], "מה מצב החבילה שלי?", ["track_package"])
irrelevant(["missing_info", "gender_morphology"], "תשלח הודעה לאמא שאני מאחרת", ["send_sms"])
irrelevant(["missing_info"], "תזמין לי רכבת לירושלים", ["book_train"])
irrelevant(["near_miss"], "תזמין לי מונית לנתב״ג", ["book_train", "get_weather"])
irrelevant(["knowledge"], "מתי יום ההולדת של אמא שלי?", ["set_reminder", "create_event"])
irrelevant(["near_miss"], "מה שעת השקיעה היום בתל אביב?", ["get_shabbat_times"])
irrelevant(["advice"], "כדאי לי לקחת משכנתא בריבית קבועה או משתנה?", ["loan_payment"])
irrelevant(["near_miss"], "תזמין לי שולחן לארבעה במסעדה 'מחניודה' הערב", ["search_restaurants"])
irrelevant(["knowledge"], "מה ההבדל בין מניה לאג״ח?", ["get_stock_quote", "convert_currency"])
irrelevant(["near_miss", "knowledge"], "מה אחוז המע״מ באילת?", ["calculate_vat"])
irrelevant(["near_miss"], "כמה זמן לוקחת טיסה מתל אביב לניו יורק?", ["check_flight_status"])
irrelevant(["near_miss", "hebrew_calendar"], "איזה תאריך עברי היום?", ["convert_hebrew_date"])
irrelevant(["knowledge", "transliteration"], "איך מאייתים את השם 'צחי' באנגלית?", ["find_contact"])
irrelevant(["near_miss"], "תכתוב לי ברכה ליום הולדת, אני אשלח אותה בעצמי בוואטסאפ", ["send_greeting"])
irrelevant(["near_miss"], "אילו חוגים יש במתנ״ס?", ["register_class"])
irrelevant(["knowledge"], "ממה מכינים פלאפל?", ["get_weather", "get_holiday_date"])
irrelevant(["near_miss"], "תסכם לי את הידיעה: 'הכנסת אישרה הלילה בקריאה ראשונה את חוק התקציב לשנת 2027'", ["translate_text"])


def build() -> list[dict[str, Any]]:
    counters: dict[str, int] = {}
    out = []
    for category, tags, question, tools, gold in ITEMS:
        counters[category] = counters.get(category, 0) + 1
        out.append({
            "id": f"{category}_{counters[category]:03d}",
            "category": category,
            "tags": tags,
            "system": SYSTEM,
            "question": question,
            "functions": [TOOLS[t] for t in tools],
            "gold": gold,
            "review": "pending",  # set to "native_verified" after a native-speaker pass
        })
    return out


if __name__ == "__main__":
    items = build()
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"wrote {len(items)} items to {OUT.relative_to(Path.cwd())}")
