"""pack_gov: v1 items (see scripts/packs/AUTHORING.md).

Domain: government and civic life in Israel (Population Authority, Bituach Leumi, tax refunds,
reserve-duty compensation, municipal hotline 106, street parking, kindergarten registration,
power outages).
"""

from __future__ import annotations

import datetime as dt

from pyluach import dates

from build_seed import CITY, MON, SUN, THU, TODAY, TOMORROW, call, d, irrelevant, multiple, parallel, simple

C = {
    **CITY,
    "RLZ": ["Rishon LeZion", "Rishon Lezion", "Rishon Le Zion", "Rishon LeTsiyon", "Rishon LeTzion", "Rishon Letzion"],
    "RG": ["Ramat Gan"],
    "HOL": ["Holon"],
    "BY": ["Bat Yam"],
    "NTN": ["Netanya", "Natanya"],
    "ASD": ["Ashdod"],
    "ASK": ["Ashkelon"],
    "REH": ["Rehovot", "Rechovot"],
    "MOD": ["Modiin", "Modi'in", "Modiin-Maccabim-Reut", "Modi'in-Maccabim-Re'ut", "Modiin Maccabim Reut"],
    "RAN": ["Raanana", "Ra'anana"],
    "HOD": ["Hod HaSharon", "Hod Hasharon"],
    "GIV": ["Givatayim", "Giv'atayim"],
    "KG": ["Kiryat Gat", "Qiryat Gat"],
    "AFU": ["Afula"],
    "KAR": ["Karmiel", "Carmiel"],
    "SDE": ["Sderot"],
    "NZ": ["Ness Ziona", "Nes Ziona", "Ness Tziona", "Nes Tziona"],
    "HAD": ["Hadera"],
    "YAV": ["Yavne", "Yavneh"],
    "KA": ["Kiryat Ata", "Qiryat Ata"],
    "NAZ": ["Nazareth"],
    "RAM": ["Ramla", "Ramle"],
    "LOD": ["Lod"],
    "BSH": ["Beit Shemesh", "Bet Shemesh"],
    "OFK": ["Ofakim"],
    "NTV": ["Netivot"],
    "RH": ["Ramat HaSharon", "Ramat Hasharon"],
}

# pyluach numbers months from Nisan.
TISHREI, CHESHVAN, ADAR = 7, 8, 12


def heb(year: int, month: int, day: int) -> str:
    """A Hebrew date as an ISO Gregorian date, computed (never typed by hand)."""
    return str(dates.HebrewDate(year, month, day).to_greg().to_pydate().isoformat())


def plus_days(iso: str, n: int) -> str:
    return (dt.date.fromisoformat(iso) + dt.timedelta(days=n)).isoformat()


def st(name: str, *extra: str) -> list[str]:
    """A street the user named: the bare name, or with the word 'רחוב' that the user wrote before it."""
    return [name, f"רחוב {name}", *extra]


THIS_MONTH, LAST_MONTH = "2026-10", "2026-09"
NEXT_SCHOOL_YEAR = "2027-2028"  # school year תשפ״ח; today (Oct 2026) we are in 2026-2027
SELF_EMPLOYED_DEFAULT = [None, False]

B, BL, TAX, RES = "book_gov_appointment", "check_bituach_leumi_payment", "request_tax_refund", "claim_reserve_compensation"
MUN, PARK, KG, PWR = "report_municipal_issue", "pay_parking", "register_kindergarten", "check_power_outage"

# --- simple ----------------------------------------------------------------------------------
# book_gov_appointment
simple(["canonical_value", "date_relative"], "תקבע לי תור לחידוש דרכון ברשות האוכלוסין בחולון, מחר ב-8:30",
       call(B, service="passport_renewal", city=C["HOL"], date=TOMORROW, time="08:30"))
simple(["canonical_value", "date_relative", "time_words"], "צריכה תור לדרכון לבן שלי, הוא בן 6, בראשל״צ ביום ראשון ברבע לעשר",
       call(B, service="child_passport", city=C["RLZ"], date=SUN, time="09:45"))
simple(["canonical_value", "date_ddmm"], "תזמין תור להנפקת תעודה ביומטרית במשרד הפנים בב״ש ב-2/11 ב-11:15",
       call(B, service="biometric_id", city=C["BS"], date="2026-11-02", time="11:15"))
simple(["canonical_value", "date_relative", "inference"],
       "עברנו לכרמיאל, תקבע לי תור לעדכון כתובת בלשכה שם ביום שני בשמונה בבוקר",
       call(B, service="address_change", city=C["KAR"], date=MON, time="08:00"))
simple(["canonical_value", "date_ddmm"], "נולדה לנו בת! תקבע תור לרישום לידה במשרד הפנים בנתניה ב-28.10 בעשר",
       call(B, service="birth_registration", city=C["NTN"], date="2026-10-28", time="10:00"))
simple(["canonical_value", "hebrew_calendar", "gematria", "calendar_compute", "time_words"],
       "תקבע לי תור לתעודת זהות ביומטרית בירושלים בט״ו בחשוון בתשע וחצי",
       call(B, service="biometric_id", city=C["JLM"], date=heb(5787, CHESHVAN, 15), time="09:30"))
simple(["canonical_value", "date_relative", "gender_addressee"], "תקבעי לי תור לחידוש ת״ז בפ״ת מחרתיים ב-12:00",
       call(B, service=["id_card", "biometric_id"], city=C["PT"], date=THU, time="12:00"))
simple(["canonical_value", "date_ddmm", "time_words"], "דרכון לילד – תור באשדוד ב-3/11 בשתיים וחצי",
       call(B, service="child_passport", city=C["ASD"], date="2026-11-03", time="14:30"))
simple(["canonical_value", "date_relative"], "חייב לחדש דרכון לפני הטיסה, תקבע לי ברמת גן בעוד שבוע ב-07:45",
       call(B, service="passport_renewal", city=C["RG"], date=d(7), time="07:45"))

# check_bituach_leumi_payment
simple(["canonical_value", "date_relative"], "נכנסה כבר קצבת הילדים של החודש?",
       call(BL, benefit="child_allowance", month=THIS_MONTH))
simple(["canonical_value"], "תבדוק לי את דמי האבטלה של ספטמבר",
       call(BL, benefit="unemployment", month="2026-09"))
simple(["canonical_value"], "אמא שלי רוצה לדעת אם קצבת הזקנה של אוגוסט עברה",
       call(BL, benefit="old_age", month="2026-08"))
simple(["canonical_value", "mixed_direction"], "הבטחת הכנסה – מה הסטטוס של התשלום ל-06/2026?",
       call(BL, benefit="income_support", month="2026-06"))

# request_tax_refund
simple(["canonical_value"], "החלפתי עבודה באמצע 2025, תגיש לי בקשה להחזר מס",
       call(TAX, tax_year=2025, reason="job_change"))
simple(["canonical_value", "date_relative"], "תרמתי לעמותות כל השנה שעברה, אני רוצה לקבל החזר מס על זה",
       call(TAX, tax_year=2025, reason="donations"))
simple(["canonical_value"], "סיימתי תואר ראשון ב-2024, תגיש בקשת החזר מס על שנת 2025 בגלל התואר",
       call(TAX, tax_year=2025, reason="academic_degree"))
simple(["canonical_value", "inference"], "גרתי בשדרות כל 2023 ולא קיבלתי את ההטבה במשכורת, תגיש טופס 135",
       call(TAX, tax_year=2023, reason="periphery_resident"))
simple(["canonical_value", "inference"],
       "השתחררתי מהצבא באוגוסט 2024 ועבדתי רק כמה חודשים, תגיש החזר מס על אותה שנה",
       call(TAX, tax_year=2024, reason="partial_year"))
simple(["canonical_value"], "שילמתי ביטוח חיים פרטי ב-2022, תגיש בשבילי החזר",
       call(TAX, tax_year=2022, reason="life_insurance"))
simple(["canonical_value", "date_relative"], "עשיתי המון מילואים בשנה שעברה, תגיש לי החזר מס על זה",
       call(TAX, tax_year=2025, reason="reserve_duty"))

# claim_reserve_compensation
simple(["date_ddmm"], "תגיש תביעה על המילואים שלי מ-1/9 עד 24/9",
       call(RES, start_date="2026-09-01", end_date="2026-09-24", self_employed=SELF_EMPLOYED_DEFAULT))
simple(["date_ddmm", "gender_addressee"], "אני עצמאית, הייתי במילואים מ-14.7 עד 2.8, תגישי תביעת פיצוי",
       call(RES, start_date="2026-07-14", end_date="2026-08-02", self_employed=True))
simple(["hebrew_calendar", "gematria", "calendar_compute"], "שירתתי במילואים מי״ז בתשרי עד כ״ט בתשרי, תגיש תביעה",
       call(RES, start_date=heb(5787, TISHREI, 17), end_date=heb(5787, TISHREI, 29), self_employed=SELF_EMPLOYED_DEFAULT))
simple(["date_ddmm", "calendar_compute"], "היו לי 10 ימי מילואים שהתחילו ב-5/10, אני שכיר. תגיש פיצוי",
       call(RES, start_date="2026-10-05", end_date=plus_days("2026-10-05", 9), self_employed=SELF_EMPLOYED_DEFAULT))
simple(["inference"], "יש לי עסק עצמאי, עשיתי מילואים מה-1 עד ה-20 באוגוסט. תגיש פיצוי",
       call(RES, start_date="2026-08-01", end_date="2026-08-20", self_employed=True))
simple(["date_relative"], "סבב מילואים: התחלתי לפני שבועיים בדיוק וסיימתי אתמול. תגיש לי תביעה",
       call(RES, start_date=d(-14), end_date=d(-1), self_employed=SELF_EMPLOYED_DEFAULT))

# report_municipal_issue
simple(["canonical_value", "free_text_hebrew"], "יש בור ענק בכביש ברחוב ז׳בוטינסקי 40 ברמת גן, תדווח לעירייה",
       call(MUN, city=C["RG"], issue_type="pothole", street=st("ז׳בוטינסקי"), house_number=40))
simple(["canonical_value", "free_text_hebrew"], "פנס רחוב לא עובד ברחוב הנביאים בחיפה",
       call(MUN, city=C["HFA"], issue_type="streetlight", street=st("הנביאים")))
simple(["canonical_value", "free_text_hebrew", "inference"], "הזבל לא נאסף כבר שבוע בשדרות רוטשילד 12 ת״א",
       call(MUN, city=C["TA"], issue_type="garbage", street=["שדרות רוטשילד", "רוטשילד"], house_number=12))
simple(["canonical_value", "free_text_hebrew", "gender_addressee"],
       "תפתחי פנייה ל-106: כלב משוטט בלי בעלים ברחוב הגפן 7 בכפר סבא",
       call(MUN, city=C["KFS"], issue_type="stray_animal", street=st("הגפן"), house_number=7))
simple(["canonical_value", "free_text_hebrew"], "התפוצץ צינור ויש מים שזורמים ברחוב העצמאות באשקלון",
       call(MUN, city=C["ASK"], issue_type="water_leak", street=st("העצמאות")))
simple(["canonical_value", "free_text_hebrew"], "עץ נפל על המדרכה ברח׳ הרצל 55 ברחובות",
       call(MUN, city=C["REH"], issue_type="fallen_tree", street=st("הרצל", "רח׳ הרצל"), house_number=55))
simple(["canonical_value", "free_text_hebrew"], "רכב חונה לי על המדרכה וחוסם את הכניסה, רחוב סוקולוב 18 בחולון",
       call(MUN, city=C["HOL"], issue_type="parking_violation", street=st("סוקולוב"), house_number=18))

# pay_parking
simple(["canonical_value", "time_words"], "תפעיל חניה בפנגו לשעתיים בתל אביב, אזור 3, רכב 1234567",
       call(PARK, city=C["TA"], zone=3, license_plate="1234567", duration_minutes=120))
simple(["canonical_value", "time_words", "mixed_direction"], "תחנה לי ברעננה לשעה וחצי, מספר רכב 45-678-90",
       call(PARK, city=C["RAN"], license_plate="4567890", duration_minutes=90))
simple(["canonical_value"], "פנגו: ירושלים אזור 7, 3 שעות, רכב 123-45-678",
       call(PARK, city=C["JLM"], zone=7, license_plate="12345678", duration_minutes=180))
simple(["canonical_value", "time_words", "gender_addressee"], "שימי לי חניה לרבע שעה בהרצליה, הרכב 98-765-43",
       call(PARK, city=C["HRZ"], license_plate="9876543", duration_minutes=15))
simple(["canonical_value", "number_words"], "תשלם חניה בחיפה לארבעים וחמש דקות, אזור 2, מספר הרכב 5551234",
       call(PARK, city=C["HFA"], zone=2, license_plate="5551234", duration_minutes=45))

# register_kindergarten
simple(["free_text_hebrew", "canonical_value", "hebrew_calendar", "gematria", "date_ddmm"],
       "תרשום את נועה לגן עירייה בהוד השרון לשנה״ל תשפ״ח. היא נולדה ב-14/3/2023",
       call(KG, child_name="נועה", birth_date="2023-03-14", city=C["HOD"], school_year=NEXT_SCHOOL_YEAR))
simple(["free_text_hebrew", "canonical_value", "date_ddmm", "inference"],
       "רישום לגן: הבן שלי איתי, נולד ב-2.9.2022, בראש העין, לשנת הלימודים הבאה",
       call(KG, child_name="איתי", birth_date="2022-09-02", city=C["RHA"], school_year=NEXT_SCHOOL_YEAR))
simple(["free_text_hebrew", "canonical_value", "date_ddmm", "gender_addressee"],
       "תרשמי את אורי לגן במודיעין לשנת הלימודים 2027-2028, תאריך לידה 30.12.2022",
       call(KG, child_name="אורי", birth_date="2022-12-30", city=C["MOD"], school_year="2027-2028"))
simple(["free_text_hebrew", "canonical_value", "hebrew_calendar", "gematria", "calendar_compute"],
       "הבת שלי שירה נולדה בכ״ח באדר תשפ״ג, תרשום אותה לגן בגבעתיים לשנת תשפ״ח",
       call(KG, child_name="שירה", birth_date=heb(5783, ADAR, 28), city=C["GIV"], school_year=NEXT_SCHOOL_YEAR))

# check_power_outage
simple(["canonical_value", "free_text_hebrew"], "אין לנו חשמל בבית, יש הפסקה באזור? אני בנהריה ברחוב הגעתון",
       call(PWR, city=C["NAH"], street=st("הגעתון")))
simple(["canonical_value", "free_text_hebrew"], "קפץ החשמל בכל הבניין, תבדוק אם יש תקלה של חברת חשמל ברחוב ויצמן בכפ״ס",
       call(PWR, city=C["KFS"], street=st("ויצמן")))

# existing tools in a civic context
simple(["mixed_direction", "currency_ils", "number_format", "canonical_value"],
       "תשלם ארנונה לעיריית חולון, חשבון 2209-114, סכום 1,875 ש״ח",
       call("pay_bill", provider="arnona", account_number="2209-114", amount_ils=1875))
simple(["mixed_direction"], "תעקוב אחרי המכתב הרשום שמס הכנסה שלחו לי: RE556677889IL",
       call("track_package", tracking_number="RE556677889IL"))
simple(["date_ddmm", "free_text_hebrew"], "תזכיר לי ב-1/11 בשמונה בבוקר 'להגיש טופס 135'",
       call("set_reminder", text="להגיש טופס 135", datetime="2026-11-01T08:00"))

# --- multiple ---------------------------------------------------------------------------------
GOV3 = [B, BL, TAX]
BL3 = [BL, RES, TAX]
MUNI = [MUN, PARK, "pay_bill"]
POWER = [PWR, MUN, "pay_bill"]
KIDS = [KG, B, "create_event"]
PARKING = [PARK, "navigate", MUN]
REM = ["set_reminder", "create_event", B]
MAIL = ["track_package", "pay_bill", BL]

multiple(["canonical_value", "date_relative"], "תור לחידוש דרכון בכפר סבא ביום שני ב-9:15", GOV3,
         call(B, service="passport_renewal", city=C["KFS"], date=MON, time="09:15"))
multiple(["canonical_value", "date_relative", "time_words"],
         "תקבע לי תור בלשכה בעפולה להוציא דרכון לבת שלי, היא בת 4. מחר בעשר וחצי", KIDS,
         call(B, service="child_passport", city=C["AFU"], date=TOMORROW, time="10:30"))
multiple(["canonical_value", "date_ddmm", "time_words"], "תשריין לי תור לתעודה ביומטרית בבת ים ב-5/11 בשמונה ורבע", GOV3,
         call(B, service="biometric_id", city=C["BY"], date="2026-11-05", time="08:15"))
multiple(["canonical_value", "date_relative"], "צריך לעדכן כתובת בת״ז, תקבע תור בלוד ביום ראשון ב-13:00", REM,
         call(B, service="address_change", city=C["LOD"], date=SUN, time="13:00"))
multiple(["canonical_value", "date_relative", "time_words"], "תקבע תור לרישום לידה של התאומים במשרד הפנים בחדרה, ביום שני בתשע",
         GOV3, call(B, service="birth_registration", city=C["HAD"], date=MON, time="09:00"))
multiple(["canonical_value", "hebrew_calendar", "gematria", "calendar_compute", "time_words"],
         "תור לחידוש דרכון בנצרת בכ״ב בחשוון בשתים עשרה בצהריים", GOV3,
         call(B, service="passport_renewal", city=C["NAZ"], date=heb(5787, CHESHVAN, 22), time="12:00"))
multiple(["canonical_value"], "כמה ביטוח לאומי העביר לי על המילואים באוגוסט?", BL3,
         call(BL, benefit="reserve_duty", month="2026-08"))
multiple(["canonical_value"], "נכנסו כבר דמי האבטלה של אוקטובר?", GOV3,
         call(BL, benefit="unemployment", month="2026-10"))
multiple(["canonical_value"], "תבדוק אם קצבת הילדים של ספטמבר נכנסה לחשבון", MAIL,
         call(BL, benefit="child_allowance", month="2026-09"))
multiple(["canonical_value", "inference", "date_relative"],
         "סבתא שלי שואלת אם הקצבה של אזרחים ותיקים לחודש שעבר הגיעה", BL3,
         call(BL, benefit="old_age", month=LAST_MONTH))
multiple(["canonical_value", "date_relative", "gender_addressee"], "תבדקי מה עם הבטחת ההכנסה שלי לחודש הזה", GOV3,
         call(BL, benefit="income_support", month=THIS_MONTH))
multiple(["canonical_value"], "מה עם דמי הלידה שלי ליולי? עוד לא ראיתי כלום בבנק", BL3,
         call(BL, benefit="maternity", month="2026-07"))
multiple(["canonical_value", "number_words"], "תגיש החזר מס על 2024, עברתי שלוש עבודות באותה שנה", GOV3,
         call(TAX, tax_year=2024, reason="job_change"))
multiple(["canonical_value", "inference"], "אני גר בקריית שמונה, תגיש בשבילי בקשה להחזר מס לשנת 2025", BL3,
         call(TAX, tax_year=2025, reason="periphery_resident"))
multiple(["canonical_value"], "יש לי קבלות על תרומות מ-2022, תגיש החזר מס", [TAX, "calculate_vat", "calculate_net_salary"],
         call(TAX, tax_year=2022, reason="donations"))
multiple(["canonical_value"], "שילמתי פרמיה על ביטוח חיים ב-2024, תגיש בקשה להחזר מס על זה", BL3,
         call(TAX, tax_year=2024, reason="life_insurance"))
multiple(["canonical_value"], "סיימתי תואר שני ב-2023, תגיש לי החזר מס לשנת 2024 בזכות התואר",
         [TAX, "calculate_net_salary", BL],
         call(TAX, tax_year=2024, reason="academic_degree"))
multiple(["date_ddmm"], "מילואים: התחלתי ב-3/8 וסיימתי ב-29/8, אני עצמאי. תגיש תביעה", BL3,
         call(RES, start_date="2026-08-03", end_date="2026-08-29", self_employed=True))
multiple(["date_ddmm"], "תגיש לי פיצוי על המילואים מה-21.9 עד ה-30.9", [RES, TAX, "create_event"],
         call(RES, start_date="2026-09-21", end_date="2026-09-30", self_employed=SELF_EMPLOYED_DEFAULT))
multiple(["canonical_value", "free_text_hebrew"], "כל לילה יש רעש מהבר ברחוב דיזנגוף 150 בת״א, תדווח לעירייה", MUNI,
         call(MUN, city=C["TA"], issue_type="noise", street=st("דיזנגוף"), house_number=150))
multiple(["canonical_value", "free_text_hebrew"], "יש נזילת מים מתחת למדרכה ברחוב ביאליק 22 ברמת השרון", POWER,
         call(MUN, city=C["RH"], issue_type="water_leak", street=st("ביאליק"), house_number=22))
multiple(["canonical_value", "free_text_hebrew"], "עמוד תאורה כבוי כבר שבוע ברחוב הדקל בעכו", MUNI,
         call(MUN, city=C["ACRE"], issue_type="streetlight", street=st("הדקל")))
multiple(["canonical_value", "free_text_hebrew"], "חתול פצוע מסתובב ברחוב השקד בנס ציונה, תפתח קריאה במוקד",
         [MUN, PWR, "navigate"],
         call(MUN, city=C["NZ"], issue_type="stray_animal", street=st("השקד")))
multiple(["canonical_value"], "פנגו לשעה בבאר שבע אזור 1, רכב 7654321", PARKING,
         call(PARK, city=C["BS"], zone=1, license_plate="7654321", duration_minutes=60))
multiple(["canonical_value", "time_words", "mixed_direction"], "תשלם חניה ברחובות לשעתיים וחצי, רכב 20-202-20", MUNI,
         call(PARK, city=C["REH"], license_plate="2020220", duration_minutes=150))
multiple(["canonical_value", "time_words"], "תפעיל לי חניה ביבנה לשלושת רבעי שעה, רכב 8642097", PARKING,
         call(PARK, city=C["YAV"], license_plate="8642097", duration_minutes=45))
multiple(["canonical_value", "free_text_hebrew"], "יש הפסקת חשמל ברחוב הרצל באשקלון?", POWER,
         call(PWR, city=C["ASK"], street=st("הרצל")))
multiple(["canonical_value", "inference"], "החשמל נפל אצלנו בכל השכונה, אנחנו גרים בקריית גת", [PWR, MUN, "set_ac"],
         call(PWR, city=C["KG"]))
multiple(["canonical_value", "mixed_direction", "currency_ils"], "תשלם את חשבון המים: חשבון 88-1203, 236.40 ש״ח", MUNI,
         call("pay_bill", provider="water", account_number="88-1203", amount_ils=236.4))
multiple(["free_text_hebrew", "canonical_value", "hebrew_calendar", "gematria", "date_ddmm"],
         "תרשום את יונתן לגן חובה בנתיבות לשנת הלימודים תשפ״ח, הוא נולד ב-11.06.2022", KIDS,
         call(KG, child_name="יונתן", birth_date="2022-06-11", city=C["NTV"], school_year=NEXT_SCHOOL_YEAR))
multiple(["free_text_hebrew", "canonical_value", "date_ddmm"], "רישום לגן ברמלה: מאיה, נולדה 5/5/2023, שנת לימודים 2027-2028", KIDS,
         call(KG, child_name="מאיה", birth_date="2023-05-05", city=C["RAM"], school_year="2027-2028"))
multiple(["date_relative", "free_text_hebrew"], "תזכיר לי מחר בעשר 'לבדוק אם נכנסה קצבת הילדים'", REM,
         call("set_reminder", text="לבדוק אם נכנסה קצבת הילדים", datetime=f"{TOMORROW}T10:00"))
multiple(["date_ddmm", "free_text_hebrew"], "תכניס ליומן 'תור לדרכון בחולון' ב-4/11 ב-8:40", REM,
         call("create_event", title="תור לדרכון בחולון", date="2026-11-04", start_time="08:40", duration_minutes=[None, 60]))
multiple(["mixed_direction"], "הדרכון החדש נשלח אליי בדואר, מספר מעקב RR987654321IL. איפה הוא?", MAIL,
         call("track_package", tracking_number="RR987654321IL"))

# --- parallel ---------------------------------------------------------------------------------
parallel(["canonical_value"], "תבדוק את קצבת הילדים של אוגוסט ושל ספטמבר", [BL],
         call(BL, benefit="child_allowance", month="2026-08"), call(BL, benefit="child_allowance", month="2026-09"))
parallel(["canonical_value", "date_relative"],
         "תקבע לי ולאשתי תורים לחידוש דרכון בהרצליה ביום ראשון, לי ב-9:00 ולה ב-9:20", [B],
         call(B, service="passport_renewal", city=C["HRZ"], date=SUN, time="09:00"),
         call(B, service="passport_renewal", city=C["HRZ"], date=SUN, time="09:20"))
parallel(["canonical_value"], "תגיש החזרי מס על 2023 ועל 2024, בשתי השנים החלפתי עבודה", [TAX],
         call(TAX, tax_year=2023, reason="job_change"), call(TAX, tax_year=2024, reason="job_change"))
parallel(["canonical_value", "free_text_hebrew"], "תדווח לעירייה בבת ים: יש בור ברחוב בלפור 10 ופנס שבור ברחוב בלפור 30", [MUN],
         call(MUN, city=C["BY"], issue_type="pothole", street=st("בלפור"), house_number=10),
         call(MUN, city=C["BY"], issue_type="streetlight", street=st("בלפור"), house_number=30))
parallel(["canonical_value"], "יש הפסקת חשמל בחיפה ובקריית אתא?", [PWR],
         call(PWR, city=C["HFA"]), call(PWR, city=C["KA"]))
parallel(["free_text_hebrew", "canonical_value", "hebrew_calendar", "gematria", "date_ddmm"],
         "תרשום את התאומים עומר ואלה לגן בראשון לציון לתשפ״ח, שניהם נולדו ב-7/7/2023", [KG],
         call(KG, child_name="עומר", birth_date="2023-07-07", city=C["RLZ"], school_year=NEXT_SCHOOL_YEAR),
         call(KG, child_name="אלה", birth_date="2023-07-07", city=C["RLZ"], school_year=NEXT_SCHOOL_YEAR))
parallel(["parallel_multiple", "canonical_value", "date_ddmm"],
         "תגיש תביעה על המילואים מ-6/9 עד 27/9 ותבדוק אם ביטוח לאומי כבר שילם על המילואים של ספטמבר", [RES, BL],
         call(RES, start_date="2026-09-06", end_date="2026-09-27", self_employed=SELF_EMPLOYED_DEFAULT),
         call(BL, benefit="reserve_duty", month="2026-09"))
parallel(["parallel_multiple", "canonical_value", "free_text_hebrew"],
         "תדווח על עץ שנפל ברחוב האלון 3 בכרמיאל ותבדוק אם יש הפסקת חשמל ברחוב האלון", [MUN, PWR],
         call(MUN, city=C["KAR"], issue_type="fallen_tree", street=st("האלון"), house_number=3),
         call(PWR, city=C["KAR"], street=st("האלון")))
parallel(["parallel_multiple", "canonical_value", "number_words", "date_relative", "free_text_hebrew"],
         "תפעיל חניה בת״א לשעה, רכב 6655443, ותזכיר לי בעוד חמישים דקות 'להאריך את החניה'", [PARK, "set_reminder"],
         call(PARK, city=C["TA"], license_plate="6655443", duration_minutes=60),
         call("set_reminder", text="להאריך את החניה", datetime=f"{TODAY}T09:50"))
parallel(["parallel_multiple", "canonical_value", "date_ddmm", "free_text_hebrew"],
         "תקבע תור לתעודה ביומטרית בפ״ת ב-9/11 ב-10:00 ותכניס את זה ליומן בשם 'משרד הפנים'", [B, "create_event"],
         call(B, service="biometric_id", city=C["PT"], date="2026-11-09", time="10:00"),
         call("create_event", title="משרד הפנים", date="2026-11-09", start_time="10:00", duration_minutes=[None, 60]))
parallel(["canonical_value", "time_words"], "תפעיל חניה לשני הרכבים שלנו בגבעתיים לשעתיים: 1112223 ו-4445556", [PARK],
         call(PARK, city=C["GIV"], license_plate="1112223", duration_minutes=120),
         call(PARK, city=C["GIV"], license_plate="4445556", duration_minutes=120))
parallel(["canonical_value", "date_relative"], "מה עם הקצבאות של אבא שלי לחודש שעבר – קצבת זקנה וקצבת נכות?", [BL],
         call(BL, benefit="old_age", month=LAST_MONTH), call(BL, benefit="disability", month=LAST_MONTH))
parallel(["canonical_value", "currency_ils", "number_format", "mixed_direction"],
         "תשלם ארנונה 1,450 ש״ח לחשבון 5531-07, וגם את המים, 310 ש״ח לחשבון 7781", ["pay_bill"],
         call("pay_bill", provider="arnona", account_number="5531-07", amount_ils=1450),
         call("pay_bill", provider="water", account_number="7781", amount_ils=310))
parallel(["canonical_value"], "תגיש החזר מס לשנת 2025: גם על תרומות וגם על ביטוח חיים", [TAX],
         call(TAX, tax_year=2025, reason="donations"), call(TAX, tax_year=2025, reason="life_insurance"))
parallel(["canonical_value"], "יש תקלות חשמל בשדרות, באופקים ובנתיבות?", [PWR],
         call(PWR, city=C["SDE"]), call(PWR, city=C["OFK"]), call(PWR, city=C["NTV"]))
parallel(["parallel_multiple", "canonical_value", "mixed_direction", "free_text_hebrew"],
         "תעקוב אחרי החבילה RR246813579IL ותבדוק אם יש הפסקת חשמל ברחוב שלי, הנרקיס בהוד השרון", ["track_package", PWR],
         call("track_package", tracking_number="RR246813579IL"),
         call(PWR, city=C["HOD"], street=["הנרקיס", "רחוב הנרקיס"]))
parallel(["date_ddmm"], "תגיש פיצוי על שני סבבי המילואים שלי: 2/8–13/8 ו-20/9–4/10", [RES],
         call(RES, start_date="2026-08-02", end_date="2026-08-13", self_employed=SELF_EMPLOYED_DEFAULT),
         call(RES, start_date="2026-09-20", end_date="2026-10-04", self_employed=SELF_EMPLOYED_DEFAULT))
parallel(["parallel_multiple", "canonical_value", "date_ddmm", "free_text_hebrew"],
         "תקבע תור לדרכון לבן שלי, בן 3, בטבריה ב-10/11 ב-8:00, ותזכיר לי ב-9/11 בשמונה בערב 'להביא תמונות פספורט'",
         [B, "set_reminder"],
         call(B, service="child_passport", city=C["TIB"], date="2026-11-10", time="08:00"),
         call("set_reminder", text="להביא תמונות פספורט", datetime="2026-11-09T20:00"))
parallel(["canonical_value", "free_text_hebrew"],
         "דיווח ל-106 בהרצליה: גרפיטי ברחוב סוקולוב 5 וזבל שלא נאסף ברחוב סוקולוב 9", [MUN],
         call(MUN, city=C["HRZ"], issue_type="graffiti", street=st("סוקולוב"), house_number=5),
         call(MUN, city=C["HRZ"], issue_type="garbage", street=st("סוקולוב"), house_number=9))
parallel(["parallel_multiple", "canonical_value"],
         "תבדוק את דמי הלידה שלי של יולי, ותגיש החזר מס על 2025 כי עבדתי רק חצי שנה", [BL, TAX],
         call(BL, benefit="maternity", month="2026-07"), call(TAX, tax_year=2025, reason="partial_year"))
parallel(["canonical_value", "date_relative"],
         "תקבע לשלושתנו תורים לתעודות ביומטריות בירושלים מחר: 8:00, 8:15 ו-8:30", [B],
         *(call(B, service="biometric_id", city=C["JLM"], date=TOMORROW, time=t) for t in ("08:00", "08:15", "08:30")))
parallel(["parallel_multiple", "canonical_value", "free_text_hebrew"],
         "יש בור בכביש ברחוב יפו 97 בירושלים, תדווח, ותפעיל לי חניה בירושלים לשעה, רכב 3456789", [MUN, PARK],
         call(MUN, city=C["JLM"], issue_type="pothole", street=st("יפו"), house_number=97),
         call(PARK, city=C["JLM"], license_plate="3456789", duration_minutes=60))
parallel(["canonical_value"], "תבדוק אם נכנסו דמי האבטלה של יולי, אוגוסט וספטמבר", [BL],
         *(call(BL, benefit="unemployment", month=m) for m in ("2026-07", "2026-08", "2026-09")))
parallel(["parallel_multiple", "free_text_hebrew", "canonical_value", "hebrew_calendar", "gematria", "date_ddmm"],
         "תרשום את רוני לגן בעפולה לתשפ״ח (נולדה 1.1.2023) ותזכיר לי ב-1/2/2027 בתשע בבוקר 'לבדוק שיבוץ גנים'",
         [KG, "set_reminder"],
         call(KG, child_name="רוני", birth_date="2023-01-01", city=C["AFU"], school_year=NEXT_SCHOOL_YEAR),
         call("set_reminder", text="לבדוק שיבוץ גנים", datetime="2027-02-01T09:00"))
parallel(["canonical_value", "free_text_hebrew"], "תבדוק הפסקות חשמל ברחוב הרצל וברחוב ויצמן בנס ציונה", [PWR],
         call(PWR, city=C["NZ"], street=st("הרצל")), call(PWR, city=C["NZ"], street=st("ויצמן")))

# --- irrelevance ------------------------------------------------------------------------------
irrelevant(["near_miss"], "תקבע לי תור לחידוש רישיון נהיגה במשרד הרישוי בחולון מחר ב-9", [B])
irrelevant(["near_miss", "currency_ils"], "תשלם לי את הקנס שקיבלתי על חניה באדום-לבן, 250 ש״ח", [PARK])
irrelevant(["near_miss"], "יש הפסקת מים מתוכננת ברעננה היום?", [PWR])
irrelevant(["near_miss"], "פוטרתי אתמול, תגיש לי בקשה לדמי אבטלה", [BL])
irrelevant(["near_miss"], "תדווח לעירייה שהשכן סוגר מרפסת בלי היתר, רחוב הזית 4 בכפר סבא", [MUN])
irrelevant(["near_miss"], "תרשום את הבן שלי לכיתה א׳ בבית ספר בהרצליה", [KG])
irrelevant(["near_miss"], "תגיש לי בקשה למענק עבודה (מס הכנסה שלילי) על 2025", [TAX])
irrelevant(["near_miss"], "תבטל את התור שלי לחידוש דרכון ביום ראשון", [B])
irrelevant(["near_miss"], "תדווח לחברת החשמל שעמוד חשמל נפל ברחוב התאנה בבית שמש", [PWR])
irrelevant(["near_miss", "currency_ils", "number_format"], "תשלם את האגרה השנתית של רישיון הרכב, 1,280 ש״ח", ["pay_bill", PARK])
irrelevant(["near_miss"], "כמה ימי מילואים צברתי מתחילת השנה?", [RES])
irrelevant(["near_miss"], "תקבע לי תור ברבנות לפתיחת תיק נישואין בירושלים ביום ראשון ב-10:00", [B])
irrelevant(["near_miss"], "מה הסטטוס של הבקשה להחזר מס שהגשתי על 2024?", [TAX])
irrelevant(["near_miss"], "תחדש לי את תו החניה לתושבים בתל אביב", [PARK])
irrelevant(["missing_info"], "יש בור בכביש ליד הבית, תדווח", [MUN])
irrelevant(["missing_info"], "תפעיל לי חניה לשעה בפנגו", [PARK])
irrelevant(["missing_info"], "תגיש תביעת פיצוי על המילואים האחרונים שלי", [RES])
irrelevant(["missing_info"], "תקבע לי תור לחידוש דרכון בנתניה", [B])
irrelevant(["missing_info"], "תבדוק אם נכנסה הקצבה שלי החודש", [BL])
irrelevant(["knowledge"], "עד כמה שנים אחורה אפשר לבקש החזר מס?", [TAX])
irrelevant(["knowledge"], "מה המספר של המוקד העירוני?", [MUN, PWR])
irrelevant(["advice"], "כדאי לי לפתוח תיק עוסק פטור או עוסק מורשה?", [TAX])
irrelevant(["chitchat"], "תודה רבה, סוף סוף הצלחתי להסתדר עם משרד הפנים", [B])
irrelevant(["chitchat"], "איזה באסה, שוב הלכתי לסניף של ביטוח לאומי וחיכיתי שעתיים בתור", [BL])
