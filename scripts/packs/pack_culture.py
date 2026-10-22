"""pack_culture: v1 items (see scripts/packs/AUTHORING.md).

Domain: calendar, Jewish time, culture and media. Every Gregorian date derived from a Hebrew date is computed
with pyluach below, never typed by hand.
"""

from __future__ import annotations

import datetime as dt

from build_seed import CITY, FRI, MON, SAT, SUN, THIS_WEEK, THU, TODAY, TOMORROW, call, d, irrelevant, multiple, parallel, simple
from pyluach import dates, parshios

# pyluach numbers months from Nisan.
MONTH = {"Nisan": 1, "Iyar": 2, "Sivan": 3, "Tammuz": 4, "Av": 5, "Elul": 6, "Tishrei": 7, "Cheshvan": 8,
         "Kislev": 9, "Tevet": 10, "Shevat": 11, "Adar": 12, "Adar I": 12, "Adar II": 13}


def heb(year: int, month: str, day: int) -> str:
    """Gregorian ISO date of a Hebrew date."""
    return dates.HebrewDate(year, MONTH[month], day).to_greg().to_pydate().isoformat()


def heb_year(year: int, month: str, day: int) -> int:
    return dates.HebrewDate(year, MONTH[month], day).to_greg().year


def week_of(iso: str) -> list[str]:
    """Sunday..Saturday of the week containing `iso` (any of them identifies that Shabbat)."""
    day = dt.date.fromisoformat(iso)
    sunday = day - dt.timedelta(days=(day.weekday() + 1) % 7)
    return [(sunday + dt.timedelta(days=n)).isoformat() for n in range(7)]


def shabbat_of_parsha(name: str) -> str:
    """The first Shabbat from the reference date on whose Torah reading (Israel) is `name`."""
    day = dates.GregorianDate(2026, 10, 20)
    for _ in range(400):
        if day.weekday() == 7 and parshios.getparsha_string(day, israel=True) == name:
            return day.to_pydate().isoformat()
        day = day + 1
    raise ValueError(name)


C = {
    **CITY,
    "BB": ["Bnei Brak", "Bene Beraq", "Bnei Braq", "Bene Brak"],
    "BSH": ["Beit Shemesh", "Bet Shemesh", "Beth Shemesh"],
    "ASD": ["Ashdod"],
    "HOL": ["Holon"],
    "MOD": ["Modiin", "Modi'in", "Modiin-Maccabim-Re'ut", "Modi'in-Maccabim-Re'ut", "Modiin Maccabim Reut"],
    "RLZ": ["Rishon LeZion", "Rishon Lezion", "Rishon LeTsiyon", "Rishon Le Zion", "Rishon LeZiyyon"],
    "RAN": ["Ra'anana", "Raanana", "Ra'annana"],
}
TEAM = {
    "MTA": ["Maccabi Tel Aviv", "Maccabi Tel-Aviv"],
    "HTA": ["Hapoel Tel Aviv", "Hapoel Tel-Aviv"],
    "MHFA": ["Maccabi Haifa"],
    "BEITAR": ["Beitar Jerusalem", "Betar Jerusalem", "Beitar Yerushalayim"],
    "HBS": ["Hapoel Beer Sheva", "Hapoel Be'er Sheva", "Hapoel Beersheba", "Hapoel Beer-Sheva", "Hapoel Be'er-Sheva"],
    "HJLM": ["Hapoel Jerusalem"],
    "SAKH": ["Bnei Sakhnin", "Bnei Sachnin", "Bnei Sakhnin FC"],
    "HHOL": ["Hapoel Holon"],
    "IKS": ["Ironi Kiryat Shmona", "Hapoel Ironi Kiryat Shmona", "Ironi Kiryat Shemona"],
}
MOVIE = {
    "lion": ["The Lion King", "Lion King"],
    "godfather": ["The Godfather", "Godfather"],
    "toy": ["Toy Story"],
    "bttf": ["Back to the Future"],
    "shawshank": ["The Shawshank Redemption", "Shawshank Redemption"],
    "jurassic": ["Jurassic Park"],
    "schindler": ["Schindler's List", "Schindlers List"],
    "nemo": ["Finding Nemo"],
    "interstellar": ["Interstellar"],
    "titanic": ["Titanic"],
    "avatar": ["Avatar"],
    "jaws": ["Jaws"],
    "beauty": ["Beauty and the Beast"],
}
Z, M, S = "get_zmanim", "book_movie", "get_sports_score"

# --- simple ---------------------------------------------------------------------------------
# zmanim
simple(["canonical_value", "date_relative"], "מתי הנץ מחר בירושלים?",
       call(Z, city=C["JLM"], date=TOMORROW, zman="sunrise"))
simple(["canonical_value"], "עד מתי סוף זמן קריאת שמע היום בבני ברק?",
       call(Z, city=C["BB"], date=[None, TODAY], zman="sof_zman_shma"))
simple(["canonical_value", "date_relative"], "תגיד לי מתי עלות השחר ביום שישי בצפת",
       call(Z, city=C["SFD"], date=FRI, zman="alot_hashachar"))
simple(["canonical_value", "date_ddmm"], "מתי חצות היום בתל אביב ב-5/11?",
       call(Z, city=C["TA"], date="2026-11-05", zman="chatzot"))
simple(["canonical_value"], "מאיזו שעה אפשר להתפלל מנחה גדולה היום בחיפה?",
       call(Z, city=C["HFA"], date=[None, TODAY], zman="mincha_gedola"))
simple(["canonical_value", "hebrew_calendar", "gematria", "calendar_compute"], "באיזו שעה השקיעה בי״ז בחשוון בבאר שבע?",
       call(Z, city=C["BS"], date=heb(5787, "Cheshvan", 17), zman="sunset"))
simple(["canonical_value", "date_relative"], "צאת הכוכבים ביום ראשון בבית שמש, מתי זה?",
       call(Z, city=C["BSH"], date=SUN, zman="tzeit_hakochavim"))
simple(["canonical_value", "hebrew_calendar", "gematria", "calendar_compute"], "מה שעת הזריחה בטבריה בא׳ בכסלו?",
       call(Z, city=C["TIB"], date=heb(5787, "Kislev", 1), zman="sunrise"))
simple(["canonical_value", "date_relative", "gender_morphology"], "אני צריכה לדעת מתי צאת הכוכבים מחרתיים במודיעין",
       call(Z, city=C["MOD"], date=THU, zman="tzeit_hakochavim"))
simple(["canonical_value", "date_ddmm"], "מתי נץ החמה באילת ב-12.11?",
       call(Z, city=C["ETH"], date="2026-11-12", zman="sunrise"))
# holidays
simple(["canonical_value", "hebrew_calendar"], "מתי ל״ג בעומר 2027?",
       call("get_holiday_date", holiday="lag_baomer", gregorian_year=2027))
simple(["canonical_value", "hebrew_calendar"], "באיזה תאריך שבועות יוצא ב-2028?",
       call("get_holiday_date", holiday="shavuot", gregorian_year=2028))
simple(["canonical_value", "hebrew_calendar", "gematria", "inference"], "מתי חנוכה תשפ״ח?",
       call("get_holiday_date", holiday="hanukkah", gregorian_year=heb_year(5788, "Kislev", 25)))
simple(["canonical_value", "hebrew_calendar"], "מתי צמים תשעה באב ב-2027?",
       call("get_holiday_date", holiday="tisha_bav", gregorian_year=2027))
simple(["canonical_value", "hebrew_calendar", "gematria", "inference"], "מתי ראש השנה תשפ״ט?",
       call("get_holiday_date", holiday="rosh_hashana", gregorian_year=heb_year(5789, "Tishrei", 1)))
simple(["canonical_value", "hebrew_calendar"], "תבדוק לי מתי יוצא יום השואה ב-2029",
       call("get_holiday_date", holiday="yom_hashoah", gregorian_year=2029))
simple(["canonical_value", "hebrew_calendar"], "באיזה יום יוצא ט״ו בשבט של 2028?",
       call("get_holiday_date", holiday="tu_bishvat", gregorian_year=2028))
simple(["canonical_value", "hebrew_calendar"], "מתי שמחת תורה בשנת 2027?",
       call("get_holiday_date", holiday="simchat_torah", gregorian_year=2027))
# Hebrew -> Gregorian
simple(["hebrew_calendar", "gematria"], "אני נולדתי בכ״ג בשבט תשמ״ה, מה התאריך הלועזי?",
       call("convert_hebrew_date", year=5745, month="Shevat", day=23))
simple(["hebrew_calendar", "gematria"], "מה התאריך הלועזי של ל׳ בחשוון תשפ״ז?",
       call("convert_hebrew_date", year=5787, month="Cheshvan", day=30))
simple(["hebrew_calendar", "gematria", "leap_year"], "פורים קטן תשפ״ז, י״ד באדר א׳, באיזה תאריך לועזי זה יוצא?",
       call("convert_hebrew_date", year=5787, month="Adar I", day=14))
simple(["hebrew_calendar", "gematria", "leap_year"], "היארצייט של סבתא בג׳ באדר תשפ״ח, מה התאריך הלועזי?",
       call("convert_hebrew_date", year=5788, month="Adar", day=3))
simple(["hebrew_calendar", "gematria", "leap_year"], "הבת שלי נולדה בכ״ט באדר ב׳ תשע״ו. תמיר לי ללועזי",
       call("convert_hebrew_date", year=5776, month="Adar II", day=29))
simple(["hebrew_calendar", "gematria", "gender_addressee"], "תמירי לי את ה׳ בטבת ה׳תשפ״ז לתאריך לועזי",
       call("convert_hebrew_date", year=5787, month="Tevet", day=5))
simple(["hebrew_calendar", "gematria"], "כ״ז בניסן תשפ״ח, איזה תאריך לועזי?",
       call("convert_hebrew_date", year=5788, month="Nisan", day=27))
simple(["hebrew_calendar", "gematria"], "ההורים שלי התחתנו בי״ח בסיון תש״ן, באיזה תאריך לועזי זה היה?",
       call("convert_hebrew_date", year=5750, month="Sivan", day=18))
# calendar events on Hebrew dates
simple(["hebrew_calendar", "gematria", "calendar_compute", "time_words", "free_text_hebrew"],
       "תוסיף ליומן 'הדלקת נרות אצל סבתא' בכ״ה בכסלו תשפ״ז בחמש וחצי אחה״צ",
       call("create_event", title="הדלקת נרות אצל סבתא", date=[heb(5787, "Kislev", 24), heb(5787, "Kislev", 25)], start_time="17:30",
            duration_minutes=[None, 60]))
simple(["hebrew_calendar", "gematria", "calendar_compute", "free_text_hebrew"],
       "תקבע לי ביומן 'אזכרה לסבא משה' בי״ב בטבת תשפ״ז ב-16:00 לשעתיים",
       call("create_event", title="אזכרה לסבא משה", date=heb(5787, "Tevet", 12), start_time="16:00", duration_minutes=120))
simple(["hebrew_calendar", "gematria", "calendar_compute", "leap_year", "free_text_hebrew"],
       "תכניס 'סעודת פורים' בי״ד באדר ב׳ הקרוב ב-13:00",
       call("create_event", title="סעודת פורים", date=heb(5787, "Adar II", 14), start_time="13:00", duration_minutes=[None, 60]))
simple(["hebrew_calendar", "gematria", "calendar_compute", "gender_addressee", "free_text_hebrew"],
       "שימי ביומן 'מסיבה בגן של יעלי' בט״ו בשבט הקרוב ב-10:00",
       call("create_event", title="מסיבה בגן של יעלי", date=heb(5787, "Shevat", 15), start_time="10:00",
            duration_minutes=[None, 60]))
# Shabbat times
simple(["canonical_value", "hebrew_calendar", "inference"], "מתי הדלקת נרות בשבת פרשת וירא בפתח תקווה?",
       call("get_shabbat_times", city=C["PT"], date=week_of(shabbat_of_parsha("Vayeira"))))
simple(["canonical_value", "hebrew_calendar", "date_relative"], "מתי נכנסת שבת בעוד שבועיים בראשון לציון?",
       call("get_shabbat_times", city=C["RLZ"], date=week_of(d(14))))
simple(["canonical_value", "hebrew_calendar", "date_ddmm"], "זמני כניסה ויציאה לשבת של ה-14/11 ברעננה",
       call("get_shabbat_times", city=C["RAN"], date=week_of("2026-11-14")))
# sports
simple(["canonical_value", "transliteration"], "מה התוצאה של מכבי חיפה בכדורגל?",
       call(S, team=TEAM["MHFA"], sport="football"))
simple(["canonical_value", "transliteration"], "איך נגמר המשחק של בית״ר ירושלים בכדורגל?",
       call(S, team=TEAM["BEITAR"], sport="football"))
simple(["canonical_value", "transliteration"], "הפועל ירושלים בכדורסל, מה היה הסקור?",
       call(S, team=TEAM["HJLM"], sport="basketball"))
simple(["canonical_value", "transliteration", "inference"], "תבדוק לי איך יצא המשחק האחרון של מכבי ת״א ביורוליג",
       call(S, team=TEAM["MTA"], sport="basketball"))
simple(["canonical_value", "transliteration"], "בני סכנין ניצחו בליגת העל בכדורגל?",
       call(S, team=TEAM["SAKH"], sport="football"))
simple(["canonical_value", "transliteration"], "מה עשתה הפועל באר שבע במשחק האחרון שלה בכדורגל?",
       call(S, team=TEAM["HBS"], sport="football"))
# movies
simple(["canonical_value", "date_relative"], "תזמין לי שני כרטיסים ל'מלך האריות' ביס פלאנט ראשון מחר ב-18:00",
       call(M, movie=MOVIE["lion"], cinema="Yes Planet Rishon LeZion", date=TOMORROW, time="18:00", tickets=2))
simple(["canonical_value", "date_relative", "time_words"], "כרטיס ל'הסנדק' בלב דיזנגוף ביום חמישי בתשע וחצי בערב",
       call(M, movie=MOVIE["godfather"], cinema="Lev Dizengoff", date=THU, time="21:30", tickets=[None, 1]))
simple(["canonical_value", "date_relative"], "4 כרטיסים ל'צעצוע של סיפור' בסינמה סיטי גלילות בשבת ב-11 בבוקר",
       call(M, movie=MOVIE["toy"], cinema="Cinema City Glilot", date=SAT, time="11:00", tickets=4))
simple(["canonical_value", "date_ddmm", "gender_addressee"], "תקני לי 3 כרטיסים ל'בחזרה לעתיד' ברב חן גבעתיים ב-31/10 ב-20:15",
       call(M, movie=MOVIE["bttf"], cinema="Rav-Hen Givatayim", date="2026-10-31", time="20:15", tickets=3))
simple(["canonical_value", "date_relative", "number_words"], "שני כרטיסים ל'חומות של תקווה' ביס פלאנט חיפה ביום ראשון ב-19:45",
       call(M, movie=MOVIE["shawshank"], cinema="Yes Planet Haifa", date=SUN, time="19:45", tickets=2))
# lottery and news
simple(["canonical_value"], "מה המספרים שיצאו בלוטו האחרון?",
       call("get_lottery_results", game="lotto", draw_date=[None]))
simple(["canonical_value", "date_ddmm"], "תבדוק את תוצאות הצ׳אנס מ-18/10",
       call("get_lottery_results", game="chance", draw_date="2026-10-18"))
simple(["canonical_value"], "תביא לי כותרות כלכלה באנגלית",
       call("get_news", topic="economy", language="en"))
simple(["canonical_value"], "מה החדשות בתרבות?",
       call("get_news", topic="culture", language=[None, "he"]))

# --- multiple -------------------------------------------------------------------------------
ZM = ["get_zmanim", "get_shabbat_times", "get_weather"]
HOL = ["get_holiday_date", "convert_hebrew_date", "create_event"]
FUN = ["get_sports_score", "get_news", "get_lottery_results"]
MOV = ["book_movie", "book_table", "create_event"]
GREET = ["send_greeting", "send_sms", "translate_text"]

multiple(["canonical_value", "hebrew_calendar"], "מתי צאת שבת השבוע בבני ברק?",
         ["get_shabbat_times", "get_zmanim", "get_holiday_date"],
         call("get_shabbat_times", city=C["BB"], date=THIS_WEEK))
multiple(["canonical_value", "date_relative"], "עד איזה שעה אפשר לקרוא שמע מחר בירושלים?", ZM,
         call(Z, city=C["JLM"], date=TOMORROW, zman="sof_zman_shma"))
multiple(["canonical_value", "date_relative"], "מתי שקיעה ביום חמישי באשדוד?", ZM,
         call(Z, city=C["ASD"], date=THU, zman="sunset"))
multiple(["canonical_value", "hebrew_calendar", "gematria", "calendar_compute"], "מתי חצות היום בכ׳ בחשוון בירושלים?", ZM,
         call(Z, city=C["JLM"], date=heb(5787, "Cheshvan", 20), zman="chatzot"))
multiple(["canonical_value", "date_ddmm"], "מתי עלות השחר ב-1/11 בחולון?", ZM,
         call(Z, city=C["HOL"], date="2026-11-01", zman="alot_hashachar"))
multiple(["canonical_value", "hebrew_calendar", "gematria", "inference"], "מתי פסח תשפ״ח?", HOL,
         call("get_holiday_date", holiday="passover", gregorian_year=heb_year(5788, "Nisan", 15)))
multiple(["hebrew_calendar", "gematria", "leap_year"], "מה התאריך הלועזי של כ״ד באדר א׳ תשפ״ז?", HOL,
         call("convert_hebrew_date", year=5787, month="Adar I", day=24))
multiple(["canonical_value", "hebrew_calendar"], "באיזה תאריך חוגגים את יום העצמאות ב-2027?", HOL,
         call("get_holiday_date", holiday="yom_haatzmaut", gregorian_year=2027))
multiple(["hebrew_calendar", "gematria", "calendar_compute", "free_text_hebrew"], "תכניס ליומן 'ערב שירה' בי״ט בכסלו ב-20:00", HOL,
         call("create_event", title="ערב שירה", date=heb(5787, "Kislev", 19), start_time="20:00", duration_minutes=[None, 60]))
multiple(["canonical_value", "hebrew_calendar"], "סוכות 2027 מתחיל מתי?", HOL,
         call("get_holiday_date", holiday="sukkot", gregorian_year=2027))
multiple(["canonical_value", "transliteration"], "מה עשתה מכבי תל אביב בכדורסל?", FUN,
         call(S, team=TEAM["MTA"], sport="basketball"))
multiple(["canonical_value", "transliteration"], "הפועל תל אביב בכדורגל, מה התוצאה?", FUN,
         call(S, team=TEAM["HTA"], sport="football"))
multiple(["canonical_value"], "מה יצא בהגרלת 777 האחרונה?", FUN,
         call("get_lottery_results", game="777", draw_date=[None]))
multiple(["canonical_value", "date_ddmm"], "מה יצא בלוטו של ה-17/10?", FUN,
         call("get_lottery_results", game="lotto", draw_date="2026-10-17"))
multiple(["canonical_value"], "תביא לי חדשות ספורט ברוסית", FUN,
         call("get_news", topic="sports", language="ru"))
multiple(["canonical_value"], "מה הכותרות בעולם ההייטק והטכנולוגיה?", FUN,
         call("get_news", topic="technology", language=[None, "he"]))
multiple(["canonical_value", "date_relative"], "מה המספרים של ה-123 בהגרלה של היום?", FUN,
         call("get_lottery_results", game="123", draw_date=[None, TODAY]))
multiple(["canonical_value", "date_relative"], "תזמין 2 כרטיסים ל'פארק היורה' בסינמה סיטי ירושלים ביום שישי ב-14:30", MOV,
         call(M, movie=MOVIE["jurassic"], cinema="Cinema City Jerusalem", date=FRI, time="14:30", tickets=2))
multiple(["canonical_value", "date_ddmm", "time_words"], "כרטיס אחד ל'רשימת שינדלר' ביס פלאנט באר שבע ב-2/11 בשמונה בערב", MOV,
         call(M, movie=MOVIE["schindler"], cinema="Yes Planet Beer Sheva", date="2026-11-02", time="20:00", tickets=[None, 1]))
multiple(["canonical_value", "date_relative", "number_words"], "אנחנו חמישה, תזמין ל'מוצאים את נמו' בסינמה סיטי גלילות מחר ב-16:00", MOV,
         call(M, movie=MOVIE["nemo"], cinema="Cinema City Glilot", date=TOMORROW, time="16:00", tickets=5))
multiple(["transliteration", "date_relative"], "שלושה כרטיסים ל'אינטרסטלר' בלב דיזנגוף בשבת ב-21:00", MOV,
         call(M, movie=MOVIE["interstellar"], cinema="Lev Dizengoff", date=SAT, time="21:00", tickets=3))
multiple(["gender_morphology", "canonical_value"], "תשלח ברכת חג שמח לאסתר", GREET,
         call("send_greeting", recipient_name="אסתר", recipient_gender="female", occasion="holiday"))
multiple(["gender_morphology", "gender_addressee", "canonical_value"], "תשלחי ברכת חנוכה לאבי שמעוני", GREET,
         call("send_greeting", recipient_name="אבי שמעוני", recipient_gender="male", occasion="holiday"))
multiple(["canonical_value", "free_text_hebrew"], "תתרגם לאמהרית 'חג סיגד שמח'", GREET,
         call("translate_text", text="חג סיגד שמח", target_language="am"))
multiple(["mixed_direction", "free_text_hebrew"], "שלח לנתנאל ב-052-3344556: 'נתראה בבית הכנסת בשש'", GREET,
         call("send_sms", phone="0523344556", text="נתראה בבית הכנסת בשש"))
multiple(["gender_morphology", "free_text_hebrew", "canonical_value"], "תרשום אותי ליוגה, אני רינה גולן",
         ["register_class", "send_greeting", "create_event"],
         call("register_class", full_name="רינה גולן", gender="female", class_name="yoga"))
multiple(["transliteration"], "תמצא את המספר של אליהו בן דוד", ["find_contact", "send_sms", "send_greeting"],
         call("find_contact", name=["Eliyahu Ben David", "Eliyahu Ben-David", "Eliahu Ben David", "Eliahu Ben-David"]))
multiple(["canonical_value", "hebrew_calendar"], "מתי נכנס יום כיפור ב-2028?", ["get_holiday_date", "get_shabbat_times", "get_zmanim"],
         call("get_holiday_date", holiday="yom_kippur", gregorian_year=2028))
multiple(["hebrew_calendar", "gematria", "inference"], "ט״ו בכסלו הקרוב, מה זה בתאריך לועזי?", HOL,
         call("convert_hebrew_date", year=5787, month="Kislev", day=15))
multiple(["canonical_value", "hebrew_calendar", "inference"], "מתי מבדילים במוצ״ש הזה בראשון לציון?", ZM,
         call("get_shabbat_times", city=C["RLZ"], date=THIS_WEEK))
multiple(["canonical_value", "transliteration"], "מה המצב של הפועל חולון בכדורסל?", FUN,
         call(S, team=TEAM["HHOL"], sport="basketball"))
multiple(["canonical_value"], "תביא חדשות בריאות בערבית", FUN,
         call("get_news", topic="health", language="ar"))
multiple(["hebrew_calendar", "gematria", "leap_year"], "מה התאריך הלועזי של ז׳ באדר תשפ״ט?", HOL,
         call("convert_hebrew_date", year=5789, month="Adar", day=7))

# --- parallel -------------------------------------------------------------------------------
parallel(["canonical_value", "date_relative"], "מתי הנץ ומתי השקיעה מחר בירושלים?", [Z],
         call(Z, city=C["JLM"], date=TOMORROW, zman="sunrise"), call(Z, city=C["JLM"], date=TOMORROW, zman="sunset"))
parallel(["canonical_value"], "מתי סוף זמן ק״ש היום בבני ברק ובירושלים?", [Z],
         call(Z, city=C["BB"], date=[None, TODAY], zman="sof_zman_shma"),
         call(Z, city=C["JLM"], date=[None, TODAY], zman="sof_zman_shma"))
parallel(["canonical_value", "hebrew_calendar", "gematria", "calendar_compute", "inference"],
         "מתי עלות השחר ומתי צאת הכוכבים ביום כיפור תשפ״ח בתל אביב?", [Z],
         call(Z, city=C["TA"], date=heb(5788, "Tishrei", 10), zman="alot_hashachar"),
         call(Z, city=C["TA"], date=heb(5788, "Tishrei", 10), zman="tzeit_hakochavim"))
parallel(["canonical_value", "hebrew_calendar"], "מתי ל״ג בעומר ומתי שבועות ב-2027?", ["get_holiday_date"],
         call("get_holiday_date", holiday="lag_baomer", gregorian_year=2027),
         call("get_holiday_date", holiday="shavuot", gregorian_year=2027))
parallel(["hebrew_calendar", "gematria", "leap_year"], "תמיר לי ללועזי את י״ד באדר א׳ ואת י״ד באדר ב׳ תשפ״ז", ["convert_hebrew_date"],
         call("convert_hebrew_date", year=5787, month="Adar I", day=14),
         call("convert_hebrew_date", year=5787, month="Adar II", day=14))
parallel(["canonical_value", "transliteration"], "מה התוצאות של מכבי חיפה ושל הפועל באר שבע בכדורגל?", [S],
         call(S, team=TEAM["MHFA"], sport="football"), call(S, team=TEAM["HBS"], sport="football"))
parallel(["canonical_value", "transliteration"], "מכבי ת״א והפועל ת״א, שתיהן בכדורסל, איך יצאו?", [S],
         call(S, team=TEAM["MTA"], sport="basketball"), call(S, team=TEAM["HTA"], sport="basketball"))
parallel(["canonical_value"], "תביא לי את תוצאות הלוטו והצ׳אנס האחרונות", ["get_lottery_results"],
         call("get_lottery_results", game="lotto", draw_date=[None]),
         call("get_lottery_results", game="chance", draw_date=[None]))
parallel(["canonical_value"], "כותרות ספורט וכלכלה, באנגלית בבקשה", ["get_news"],
         call("get_news", topic="sports", language="en"), call("get_news", topic="economy", language="en"))
parallel(["transliteration", "date_relative"],
         "תזמין 2 כרטיסים ל'טיטאניק' ו-2 ל'אווטאר' בסינמה סיטי גלילות מחר, טיטאניק ב-17:00 ואווטאר ב-20:30", [M],
         call(M, movie=MOVIE["titanic"], cinema="Cinema City Glilot", date=TOMORROW, time="17:00", tickets=2),
         call(M, movie=MOVIE["avatar"], cinema="Cinema City Glilot", date=TOMORROW, time="20:30", tickets=2))
parallel(["parallel_multiple", "canonical_value", "mixed_direction", "free_text_hebrew", "date_relative"],
         "תזמין 2 כרטיסים ל'מלתעות' בלב דיזנגוף ביום חמישי ב-22:00, ותשלח לליאור ב-054-7778899 'הזמנתי לנו כרטיסים לחמישי'",
         [M, "send_sms"],
         call(M, movie=MOVIE["jaws"], cinema="Lev Dizengoff", date=THU, time="22:00", tickets=2),
         call("send_sms", phone="0547778899", text="הזמנתי לנו כרטיסים לחמישי"))
parallel(["parallel_multiple", "canonical_value", "hebrew_calendar", "gematria", "calendar_compute", "free_text_hebrew"],
         "מתי פורים 2027? וגם תכניס ליומן 'מסיבת חנוכה בעבודה' בכ״ז בכסלו תשפ״ז ב-18:00",
         ["get_holiday_date", "create_event"],
         call("get_holiday_date", holiday="purim", gregorian_year=2027),
         call("create_event", title="מסיבת חנוכה בעבודה", date=heb(5787, "Kislev", 27), start_time="18:00",
              duration_minutes=[None, 60]))
parallel(["gender_morphology", "canonical_value"], "תשלח ברכת חג לדוד ולשרה", ["send_greeting"],
         call("send_greeting", recipient_name="דוד", recipient_gender="male", occasion="holiday"),
         call("send_greeting", recipient_name="שרה", recipient_gender="female", occasion="holiday"))
parallel(["gender_morphology", "canonical_value"], "תשלח ברכת יום הולדת לעומר, הוא בן 40 היום, וברכה ללידה לאחותו נועה",
         ["send_greeting"],
         call("send_greeting", recipient_name="עומר", recipient_gender="male", occasion="birthday"),
         call("send_greeting", recipient_name="נועה", recipient_gender="female", occasion="new_baby"))
parallel(["canonical_value", "free_text_hebrew"], "תתרגם 'שבת שלום ומבורך' לאנגלית ולרוסית", ["translate_text"],
         call("translate_text", text="שבת שלום ומבורך", target_language="en"),
         call("translate_text", text="שבת שלום ומבורך", target_language="ru"))
parallel(["canonical_value", "hebrew_calendar"], "זמני שבת השבוע בצפת, בטבריה ובאילת", ["get_shabbat_times"],
         *(call("get_shabbat_times", city=C[c], date=THIS_WEEK) for c in ("SFD", "TIB", "ETH")))
parallel(["parallel_multiple", "canonical_value", "hebrew_calendar", "date_relative"],
         "מתי כניסת שבת השבוע בחיפה, ומתי הנץ שם ביום שבת?", ["get_shabbat_times", Z],
         call("get_shabbat_times", city=C["HFA"], date=THIS_WEEK), call(Z, city=C["HFA"], date=SAT, zman="sunrise"))
parallel(["hebrew_calendar", "gematria"], "מה התאריך הלועזי של כ״ה באלול תשפ״ז ושל א׳ בתשרי תשפ״ח?", ["convert_hebrew_date"],
         call("convert_hebrew_date", year=5787, month="Elul", day=25),
         call("convert_hebrew_date", year=5788, month="Tishrei", day=1))
parallel(["canonical_value", "date_ddmm"], "מתי חצות היום בירושלים, בתל אביב ובבאר שבע ב-3/11?", [Z],
         *(call(Z, city=C[c], date="2026-11-03", zman="chatzot") for c in ("JLM", "TA", "BS")))
parallel(["gender_morphology", "gender_addressee", "free_text_hebrew", "canonical_value"],
         "תרשמי אותי ואת בעלי לפילאטיס, אני נגה ברק והוא אסף ברק", ["register_class"],
         call("register_class", full_name="נגה ברק", gender="female", class_name="pilates"),
         call("register_class", full_name="אסף ברק", gender="male", class_name="pilates"))
parallel(["parallel_multiple", "canonical_value", "transliteration"],
         "איך יצא המשחק של בית״ר ירושלים בכדורגל? ותביא לי גם כותרות ספורט", [S, "get_news"],
         call(S, team=TEAM["BEITAR"], sport="football"), call("get_news", topic="sports", language=[None, "he"]))
parallel(["parallel_multiple", "canonical_value", "mixed_direction", "free_text_hebrew"],
         "תבדוק מה יצא בלוטו האחרון ותשלח לאבא ב-050-6667788 'בדקתי את הלוטו, אעדכן בערב'",
         ["get_lottery_results", "send_sms"],
         call("get_lottery_results", game="lotto", draw_date=[None]),
         call("send_sms", phone="0506667788", text="בדקתי את הלוטו, אעדכן בערב"))
parallel(["canonical_value", "hebrew_calendar"], "מתי פורים, פסח ושבועות ב-2028?", ["get_holiday_date"],
         *(call("get_holiday_date", holiday=h, gregorian_year=2028) for h in ("purim", "passover", "shavuot")))
parallel(["hebrew_calendar", "gematria", "calendar_compute", "leap_year", "free_text_hebrew"],
         "תוסיף ליומן 'סדר ט״ו בשבט' בט״ו בשבט ב-19:00 ו'מסיבת פורים' בי״ד באדר ב׳ ב-20:00, שניהם בשנה הזאת", ["create_event"],
         call("create_event", title="סדר ט״ו בשבט", date=heb(5787, "Shevat", 15), start_time="19:00", duration_minutes=[None, 60]),
         call("create_event", title="מסיבת פורים", date=heb(5787, "Adar II", 14), start_time="20:00", duration_minutes=[None, 60]))
parallel(["transliteration"], "תמצא לי את שלמה אזולאי ואת רחל אברג׳יל", ["find_contact"],
         call("find_contact", name=["Shlomo Azoulay", "Shlomo Azulay", "Shlomo Azoulai", "Shlomo Azulai"]),
         call("find_contact", name=["Rachel Abergel", "Rahel Abergel", "Rachel Abergil", "Rahel Abergil", "Rachel Aberjil"]))
parallel(["canonical_value", "transliteration"], "מה התוצאות של מכבי תל אביב גם בכדורגל וגם בכדורסל?", [S],
         call(S, team=TEAM["MTA"], sport="football"), call(S, team=TEAM["MTA"], sport="basketball"))

# --- irrelevance ----------------------------------------------------------------------------
irrelevant(["near_miss", "hebrew_calendar"], "מתי המולד של חודש כסלו?", [Z])
irrelevant(["near_miss", "hebrew_calendar"], "מתי חג הסיגד ב-2027?", ["get_holiday_date"])
irrelevant(["near_miss", "hebrew_calendar"], "מתי ט״ו באב ב-2027?", ["get_holiday_date"])
irrelevant(["near_miss"], "מתי פלג המנחה מחר בירושלים?", [Z])
irrelevant(["near_miss"], "תזמין לי שני כרטיסים להצגה 'הקמצן' בהבימה ביום חמישי", [M])
irrelevant(["near_miss"], "מה התוצאה של מכבי תל אביב בכדורעף?", [S])
irrelevant(["near_miss"], "איך יצא המשחק של ריאל מדריד אתמול?", [S])
irrelevant(["near_miss"], "תמלא לי טופס לוטו עם המספרים 3, 8, 15, 22, 31, 36", ["get_lottery_results"])
irrelevant(["near_miss", "hebrew_calendar", "date_ddmm"], "מה התאריך העברי של 25/12/2026?", ["convert_hebrew_date"])
irrelevant(["near_miss"], "אילו סרטים מוקרנים הערב ביס פלאנט חיפה?", [M])
irrelevant(["near_miss"], "באיזה מקום הפועל באר שבע בטבלה?", [S])
irrelevant(["near_miss", "hebrew_calendar"], "מתי ראש חודש טבת?", ["get_holiday_date"])
irrelevant(["near_miss"], "תבטל לי את הכרטיסים לסרט שהזמנתי למחר", [M])
irrelevant(["near_miss", "hebrew_calendar"], "איזו פרשה קוראים השבת?", ["get_shabbat_times"])
irrelevant(["missing_info"], "תזמין לי שני כרטיסים ל'אופנהיימר' מחר בערב", [M])
irrelevant(["missing_info"], "מתי השקיעה היום?", [Z])
irrelevant(["missing_info"], "מה הייתה התוצאה של המשחק אתמול?", [S])
irrelevant(["missing_info"], "תשלח ברכת חג שמח", ["send_greeting"])
irrelevant(["chitchat"], "שבוע טוב! איך עבר עליך הסופ״ש?", ["get_shabbat_times"])
irrelevant(["advice"], "תמליץ לי על סרט טוב לראות הערב עם הילדים", [M])
irrelevant(["knowledge", "hebrew_calendar", "leap_year"], "למה יש שנים עם שני חודשי אדר?", ["convert_hebrew_date"])
irrelevant(["knowledge", "gematria"], "כמה שווה המילה 'חי' בגימטריה?", ["convert_hebrew_date", "get_holiday_date"])
irrelevant(["knowledge"], "מי ביים את 'הסנדק'?", [M])
irrelevant(["advice"], "כדאי לי למלא לוטו או צ׳אנס?", ["get_lottery_results"])
