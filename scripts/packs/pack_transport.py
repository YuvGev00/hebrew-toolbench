"""pack_transport: v1 items (see scripts/packs/AUTHORING.md).

Transport and travel: navigation, Rav-Kav, taxis, flights, hotels, trains, buses, parking.
The core of the pack is Hebrew place names that must become English cities, IATA codes and
station enums.
"""

from __future__ import annotations

import datetime as dt

from pyluach import dates

from build_seed import CITY, FRI, MON, SAT, SUN, THU, TODAY, TOMORROW, call, d, irrelevant, multiple, parallel, simple

C = {
    **CITY,
    "RG": ["Ramat Gan"],
    "HOL": ["Holon"],
    "RLZ": ["Rishon LeZion", "Rishon Lezion", "Rishon LeTsiyon", "Rishon Le Zion", "Rishon Letzion", "Rishon LeTzion"],
    "NTN": ["Netanya", "Natanya"],
    "ASK": ["Ashkelon", "Ashqelon"],
    "ZY": ["Zichron Yaakov", "Zikhron Ya'akov", "Zichron Ya'akov", "Zikhron Yaakov", "Zichron Yaacov"],
    "MR": ["Mitzpe Ramon", "Mitspe Ramon", "Mizpe Ramon", "Mitzpeh Ramon"],
    "KAR": ["Karmiel", "Carmiel"],
    "KTZ": ["Katzrin", "Qatsrin", "Katsrin", "Qazrin"],
    "ROME": ["Rome", "Roma"],
    "ATH": ["Athens"],
    "PAR": ["Paris"],
    "LON": ["London"],
    "BER": ["Berlin"],
    "BUD": ["Budapest"],
    "VIE": ["Vienna", "Wien"],
}

NOW = [None, f"{TODAY}T09:00"]  # "now": the argument may be omitted, or set to the reference time
ONE = [None, 1]
TWO = [None, 2]
NATIONAL = [None, "national"]


def fl(code: str, num: int) -> list[str]:
    """Acceptable spellings of an IATA flight number, e.g. LY81 / LY 81 / LY081."""
    out: list[str] = []
    for n in (str(num), str(num).zfill(3)):
        for sep in ("", " "):
            if f"{code}{sep}{n}" not in out:
                out.append(f"{code}{sep}{n}")
    return out


def st(name: str) -> list[str]:
    """A street exactly as written, with or without the word רחוב."""
    return [name, f"רחוב {name}"]


def heb(year: int, month: int, day: int) -> str:
    """Hebrew date (pyluach month numbering, Nisan = 1) to an ISO Gregorian date."""
    return dates.HebrewDate(year, month, day).to_greg().to_pydate().isoformat()


def plus(iso: str, days: int) -> str:
    return (dt.date.fromisoformat(iso) + dt.timedelta(days=days)).isoformat()


KISLEV = 9

# --- simple ---------------------------------------------------------------------------------
# navigate
simple(["canonical_value", "free_text_hebrew"], "תנווט אותי לדיזנגוף 50 בת״א",
       call("navigate", destination_city=C["TA"], street=st("דיזנגוף"), house_number=50, depart_at=NOW))
simple(["canonical_value"], "תנווט לאילת, בלי כבישי אגרה",
       call("navigate", destination_city=C["ETH"], avoid_tolls=True, depart_at=NOW))
simple(["canonical_value", "date_relative", "free_text_hebrew"], "נווט לרחוב הרצל 12 בראשון לציון, אני יוצא מחר ב-7:15",
       call("navigate", destination_city=C["RLZ"], street=st("הרצל"), house_number=12, depart_at=f"{TOMORROW}T07:15"))
simple(["canonical_value", "gender_addressee", "free_text_hebrew"], "תנווטי לי לז׳בוטינסקי 7 ברמת גן",
       call("navigate", destination_city=C["RG"], street=st("ז׳בוטינסקי"), house_number=7, depart_at=NOW))
simple(["canonical_value", "inference", "free_text_hebrew"], "תנווט לב״ש, לשדרות רגר 1, ותמנע מכביש 6",
       call("navigate", destination_city=C["BS"], street=["שדרות רגר", "רגר"], house_number=1, avoid_tolls=True,
            depart_at=NOW))
simple(["canonical_value", "date_relative", "time_words"], "תכין ניווט לצפת, יוצאים ביום שישי בשש וחצי בבוקר",
       call("navigate", destination_city=C["SFD"], depart_at=f"{FRI}T06:30"))
simple(["canonical_value", "free_text_hebrew"], "נווט לרחוב ויצמן 3 בכפר סבא",
       call("navigate", destination_city=C["KFS"], street=st("ויצמן"), house_number=3, depart_at=NOW))
simple(["transliteration", "canonical_value"], "נווט אותי למצפה רמון",
       call("navigate", destination_city=C["MR"], depart_at=NOW))
simple(["canonical_value", "date_relative", "time_words", "free_text_hebrew"],
       "אני יוצא מחר ברבע לשמונה בבוקר לרחוב הנשיא 100 בחיפה, תכין לי ניווט",
       call("navigate", destination_city=C["HFA"], street=st("הנשיא"), house_number=100, depart_at=f"{TOMORROW}T07:45"))
simple(["transliteration", "inference"], "ניווט לזכרון בבקשה",
       call("navigate", destination_city=C["ZY"], depart_at=NOW))

# load_rav_kav
simple(["canonical_value"], "תטעין חופשי חודשי גוש דן על הרב קו שלי, מספר 30512874",
       call("load_rav_kav", card_number="30512874", product="monthly", area="gush_dan"))
simple(["gender_addressee", "currency_ils", "canonical_value"], "תטעיני 100 ש״ח ערך צבור לכרטיס 41178902",
       call("load_rav_kav", card_number="41178902", product="stored_value", amount_ils=100, area=NATIONAL))
simple(["canonical_value"], "חופשי יומי ירושלים לרב-קו 55203318",
       call("load_rav_kav", card_number="55203318", product="daily", area="jerusalem"))
simple(["canonical_value"], "שבועי ארצי לרב קו 6620-1145",
       call("load_rav_kav", card_number="66201145", product="weekly", area="national"))
simple(["number_words", "currency_ils", "canonical_value"], "תעלה מאה וחמישים שקל ערך צבור לרב קו 70033251",
       call("load_rav_kav", card_number="70033251", product="stored_value", amount_ils=150, area=NATIONAL))
simple(["canonical_value"], "חודשי באר שבע לרב-קו 11229384 בבקשה",
       call("load_rav_kav", card_number="11229384", product="monthly", area="beer_sheva"))

# book_taxi
simple(["free_text_hebrew"], "תזמין מונית מ'הרצל 15, רמת גן' ל'נתב״ג טרמינל 3'",
       call("book_taxi", pickup="הרצל 15, רמת גן", destination="נתב״ג טרמינל 3", pickup_time=NOW))
simple(["free_text_hebrew"], "מונית לעכשיו: איסוף מ'בלפור 7 בת ים', יעד 'קניון איילון'",
       call("book_taxi", pickup="בלפור 7 בת ים", destination="קניון איילון", pickup_time=NOW))
simple(["gender_addressee", "date_relative", "free_text_hebrew"],
       "תזמיני לי מונית מחר ב-5 לפנות בוקר מ'ההגנה 4 חולון' ל'רכבת השלום'",
       call("book_taxi", pickup="ההגנה 4 חולון", destination="רכבת השלום", pickup_time=f"{TOMORROW}T05:00"))
simple(["canonical_value", "date_relative", "free_text_hebrew"],
       "צריך מונית ואן לשמונה אנשים מ'מלון דן אילת' ל'נמל התעופה רמון', ביום שבת ב-11:30",
       call("book_taxi", pickup="מלון דן אילת", destination="נמל התעופה רמון", pickup_time=f"{SAT}T11:30", vehicle="van"))
simple(["canonical_value", "free_text_hebrew"],
       "מונית נגישה לכיסא גלגלים מ'בית חולים שיבא' ל'סוקולוב 40 הרצליה' היום ב-14:00",
       call("book_taxi", pickup="בית חולים שיבא", destination="סוקולוב 40 הרצליה", pickup_time=f"{TODAY}T14:00",
            vehicle="accessible"))
simple(["canonical_value", "time_words", "free_text_hebrew"],
       "תזמין מונית פרימיום מ'מגדלי עזריאלי' ל'מלון המלך דוד ירושלים' הערב בשמונה וחצי",
       call("book_taxi", pickup="מגדלי עזריאלי", destination="מלון המלך דוד ירושלים", pickup_time=f"{TODAY}T20:30",
            vehicle="premium"))
simple(["date_relative", "time_words", "free_text_hebrew"],
       "מונית מ'אחד העם 9 כפר סבא' ל'תחנת רכבת כפר סבא נורדאו' ביום חמישי ברבע לשבע בבוקר",
       call("book_taxi", pickup="אחד העם 9 כפר סבא", destination="תחנת רכבת כפר סבא נורדאו", pickup_time=f"{THU}T06:45"))

# book_flight
simple(["canonical_value", "date_ddmm"], "תזמין טיסה מנתב״ג ללרנקה ב-12/11, חזור ב-15/11",
       call("book_flight", origin="TLV", destination="LCA", depart_date="2026-11-12", return_date="2026-11-15",
            passengers=ONE))
simple(["canonical_value", "date_relative"], "טיסה בכיוון אחד מתל אביב לאילת ביום ראשון, שני נוסעים",
       call("book_flight", origin="TLV", destination="ETM", depart_date=SUN, return_date=[None], passengers=2))
simple(["canonical_value", "date_ddmm"], "טיסה מנתב״ג לרומא ב-3/12 וחזרה ב-10/12, לארבעה, במחלקת עסקים",
       call("book_flight", origin="TLV", destination="FCO", depart_date="2026-12-03", return_date="2026-12-10",
            passengers=4, cabin="business"))
simple(["canonical_value", "date_ddmm"], "אני צריכה טיסה מלונדון לתל אביב ב-28/10, כיוון אחד",
       call("book_flight", origin="LHR", destination="TLV", depart_date="2026-10-28", return_date=[None], passengers=ONE))
simple(["canonical_value", "date_ddmm", "inference"],
       "תזמין לנו טיסה לבנגקוק מנתב״ג, יוצאים ב-1/12 וחוזרים ב-20/12, אני ואשתי והשניים הקטנים",
       call("book_flight", origin="TLV", destination="BKK", depart_date="2026-12-01", return_date="2026-12-20",
            passengers=4))
simple(["canonical_value", "date_ddmm"], "פרימיום אקונומי לניו יורק, יוצא מתל אביב ב-15.11 חוזר ב-29.11",
       call("book_flight", origin="TLV", destination="JFK", depart_date="2026-11-15", return_date="2026-11-29",
            passengers=ONE, cabin="premium_economy"))
simple(["canonical_value", "date_ddmm"], "טיסה מבודפשט לווינה ב-7/11",
       call("book_flight", origin="BUD", destination="VIE", depart_date="2026-11-07", return_date=[None], passengers=ONE))
simple(["canonical_value", "date_relative"], "תמצא לי טיסה מת״א לדובאי למחרתיים, רק הלוך",
       call("book_flight", origin="TLV", destination="DXB", depart_date=THU, return_date=[None], passengers=ONE))

# book_hotel
simple(["canonical_value", "date_relative"], "תזמין מלון באילת מיום חמישי עד יום ראשון",
       call("book_hotel", city=C["ETH"], check_in=THU, check_out=SUN, guests=TWO, rooms=ONE))
simple(["canonical_value", "date_ddmm", "inference"], "חדר בטבריה לשלושה לילות מ-5/11, אנחנו זוג",
       call("book_hotel", city=C["TIB"], check_in="2026-11-05", check_out=plus("2026-11-05", 3), guests=TWO, rooms=ONE))
simple(["canonical_value", "date_relative"],
       "מלון בירושלים, צ׳ק אין ביום שישי וצ׳ק אאוט ביום ראשון, 2 חדרים ל-4 אנשים",
       call("book_hotel", city=C["JLM"], check_in=FRI, check_out=SUN, guests=4, rooms=2))
simple(["canonical_value", "transliteration", "date_ddmm"], "מלון ברומא מ-10/11 עד 14/11 לשלושה אנשים",
       call("book_hotel", city=C["ROME"], check_in="2026-11-10", check_out="2026-11-14", guests=3, rooms=ONE))
simple(["transliteration", "gender_addressee", "date_relative"], "תזמיני לי לילה אחד במצפה רמון, מחר",
       call("book_hotel", city=C["MR"], check_in=TOMORROW, check_out=plus(TOMORROW, 1), guests=[None, 1, 2], rooms=ONE))
simple(["canonical_value", "hebrew_calendar", "gematria", "calendar_compute"], "מלון בחיפה מכ״ה בכסלו עד כ״ח בכסלו תשפ״ז",
       call("book_hotel", city=C["HFA"], check_in=heb(5787, KISLEV, 25), check_out=heb(5787, KISLEV, 28),
            guests=TWO, rooms=ONE))

# book_train
simple(["canonical_value"], "רכבת מסבידור לנתב״ג היום ב-17:20",
       call("book_train", origin="Tel Aviv Savidor Center", destination="Ben Gurion Airport", date=TODAY, time="17:20",
            passengers=ONE))
simple(["canonical_value", "inference", "date_relative", "time_words"], "כרטיס לרכבת מב״ש לחיפה ביום שני בעשר ורבע בבוקר",
       call("book_train", origin="Beer Sheva Center", destination="Haifa Hof HaCarmel", date=MON, time="10:15",
            passengers=ONE))
simple(["canonical_value", "inference", "gender_addressee", "date_ddmm", "number_words"],
       "תזמיני לנו רכבת מאשדוד לנתניה לחמישה אנשים, ב-5/11 ב-16:00",
       call("book_train", origin="Ashdod Ad Halom", destination="Netanya", date="2026-11-05", time="16:00", passengers=5))

# check_flight_status
simple(["transliteration", "canonical_value", "date_relative"], "מה המצב של טיסת ארקיע 211 מחר?",
       call("check_flight_status", flight_number=fl("IZ", 211), date=TOMORROW))
simple(["mixed_direction", "gender_addressee"], "תבדקי לי את ויז אייר W6 2318 היום",
       call("check_flight_status", flight_number=fl("W6", 2318), date=[None, TODAY]))

# get_bus_arrivals
simple(["number_words"], "מתי מגיע קו שש לתחנה 20841?",
       call("get_bus_arrivals", stop_code=20841, line="6"))
simple([], "מתי האוטובוס הבא בתחנה 13562",
       call("get_bus_arrivals", stop_code=13562, line=[None]))

# get_weather
simple(["canonical_value", "transliteration", "date_ddmm"], "מה יהיה מזג האוויר באתונה ב-5/11? אני טס לשם",
       call("get_weather", city=C["ATH"], date="2026-11-05"))

# pay_parking
simple(["canonical_value"], "תפעיל חניה בפנגו בת״א אזור 4, רכב 12-345-67, לשעתיים",
       call("pay_parking", city=C["TA"], zone=4, license_plate="1234567", duration_minutes=120))
simple(["canonical_value", "time_words"], "חניה בחיפה לחצי שעה, רכב 8812345",
       call("pay_parking", city=C["HFA"], zone=[None], license_plate="8812345", duration_minutes=30))

# --- multiple -------------------------------------------------------------------------------
FLY = ["book_flight", "check_flight_status", "book_hotel"]
TRIP = ["book_hotel", "book_flight", "get_weather"]
DRIVE = ["navigate", "pay_parking", "get_fuel_price"]
RIDE = ["book_taxi", "navigate", "book_train"]
PUBLIC = ["get_bus_arrivals", "load_rav_kav", "book_train"]
TRAIN = ["book_train", "book_taxi", "get_bus_arrivals"]

multiple(["canonical_value", "date_ddmm"], "טיסה לאמסטרדם מנתב״ג ב-19/11 וחזור ב-23/11", FLY,
         call("book_flight", origin="TLV", destination="AMS", depart_date="2026-11-19", return_date="2026-11-23",
              passengers=ONE))
multiple(["transliteration", "canonical_value"], "נחתה כבר הטיסה של אל על 316 מפריז?", FLY,
         call("check_flight_status", flight_number=fl("LY", 316), date=[None, TODAY]))
multiple(["transliteration", "canonical_value", "date_ddmm"], "מלון בברלין מ-19/11 עד 22/11, אני לבד", FLY,
         call("book_hotel", city=C["BER"], check_in="2026-11-19", check_out="2026-11-22", guests=1, rooms=ONE))
multiple(["canonical_value", "transliteration", "date_relative"], "מה מזג האוויר בבודפשט מחר?", TRIP,
         call("get_weather", city=C["BUD"], date=TOMORROW))
multiple(["canonical_value", "transliteration", "date_ddmm"], "תזמין לי מלון בווינה מ-1/12 ל-4/12, שני חדרים לארבעה אנשים", TRIP,
         call("book_hotel", city=C["VIE"], check_in="2026-12-01", check_out="2026-12-04", guests=4, rooms=2))
multiple(["canonical_value", "date_ddmm"], "תזמין טיסה מאתונה לת״א ב-30/10", TRIP,
         call("book_flight", origin="ATH", destination="TLV", depart_date="2026-10-30", return_date=[None], passengers=ONE))
multiple(["canonical_value", "free_text_hebrew"], "תנווט לשדרות רוטשילד 1 בת״א בלי אגרות", DRIVE,
         call("navigate", destination_city=C["TA"], street=["שדרות רוטשילד", "רוטשילד"], house_number=1,
              avoid_tolls=True, depart_at=NOW))
multiple(["canonical_value", "time_words"], "תפעיל חניה לשעה וחצי בכפר סבא, אזור 2, מספר רכב 4455667", DRIVE,
         call("pay_parking", city=C["KFS"], zone=2, license_plate="4455667", duration_minutes=90))
multiple(["canonical_value"], "כמה עולה ליטר סולר החודש?", DRIVE,
         call("get_fuel_price", fuel="diesel", month=[None, "2026-10"]))
multiple(["canonical_value", "inference"], "מה היה מחיר בנזין 95 בספטמבר?", DRIVE,
         call("get_fuel_price", fuel="gasoline_95", month="2026-09"))
multiple(["free_text_hebrew"], "תזמין מונית מ'דרך מנחם בגין 132' ל'שוק הכרמל', עכשיו", RIDE,
         call("book_taxi", pickup="דרך מנחם בגין 132", destination="שוק הכרמל", pickup_time=NOW))
multiple(["canonical_value", "inference", "date_relative"], "רכבת מירושלים לתל אביב השלום מחר ב-7:30", RIDE,
         call("book_train", origin="Jerusalem Yitzhak Navon", destination="Tel Aviv HaShalom", date=TOMORROW, time="07:30",
              passengers=ONE))
multiple(["transliteration", "canonical_value"], "תנווט לקצרין", RIDE,
         call("navigate", destination_city=C["KTZ"], depart_at=NOW))
multiple(["canonical_value"], "תטעין חופשי שבועי חיפה לכרטיס 90817263", PUBLIC,
         call("load_rav_kav", card_number="90817263", product="weekly", area="haifa"))
multiple([], "מתי מגיע קו 18 לתחנה 26492?", PUBLIC,
         call("get_bus_arrivals", stop_code=26492, line="18"))
multiple(["currency_ils", "canonical_value"], "תטעין 200 ₪ לרב קו 33445566", PUBLIC,
         call("load_rav_kav", card_number="33445566", product="stored_value", amount_ils=200, area=NATIONAL))
multiple(["canonical_value", "number_words", "date_relative"], "שלושה כרטיסים מנהריה למודיעין מרכז ביום ראשון ב-6:50", TRAIN,
         call("book_train", origin="Nahariya", destination="Modiin Center", date=SUN, time="06:50", passengers=3))
multiple(["gender_addressee", "free_text_hebrew"], "תזמיני מונית מ'תחנת רכבת יצחק נבון' ל'הכותל המערבי', עכשיו", TRAIN,
         call("book_taxi", pickup="תחנת רכבת יצחק נבון", destination="הכותל המערבי", pickup_time=NOW))
multiple(["mixed_direction", "date_relative"], "יש עיכוב ב-LY 81 של מחר?", FLY,
         call("check_flight_status", flight_number=fl("LY", 81), date=TOMORROW))
multiple(["canonical_value"], "תטעין לבת שלי חופשי חודשי צפון לרב קו 22113344",
         ["load_rav_kav", "get_bus_arrivals", "pay_parking"],
         call("load_rav_kav", card_number="22113344", product="monthly", area="north"))
multiple(["canonical_value", "number_words"], "פנגו בירושלים, אזור 7, רכב 5566778, לשלוש שעות",
         ["pay_parking", "navigate", "book_taxi"],
         call("pay_parking", city=C["JLM"], zone=7, license_plate="5566778", duration_minutes=180))
multiple(["transliteration", "inference", "date_relative"], "מלון בזכרון מחמישי לשבת", ["book_hotel", "book_taxi", "get_weather"],
         call("book_hotel", city=C["ZY"], check_in=THU, check_out=SAT, guests=TWO, rooms=ONE))
multiple(["canonical_value", "transliteration", "date_relative"], "יהיה גשם בכרמיאל מחר?", ["get_weather", "navigate", "pay_parking"],
         call("get_weather", city=C["KAR"], date=TOMORROW))
multiple(["canonical_value", "date_ddmm"], "טיסה ללונדון מת״א ב-2/12, חזור 9/12, שני אנשים",
         ["book_flight", "get_weather", "convert_currency"],
         call("book_flight", origin="TLV", destination="LHR", depart_date="2026-12-02", return_date="2026-12-09",
              passengers=2))
multiple(["transliteration", "canonical_value", "date_relative"], "ישראייר 552 ביום חמישי, יש עדכון?",
         ["check_flight_status", "book_flight", "get_weather"],
         call("check_flight_status", flight_number=fl("6H", 552), date=THU))
multiple(["canonical_value", "gender_addressee", "free_text_hebrew"], "תפעילי ניווט לסמילנסקי 5 בנתניה",
         ["navigate", "book_taxi", "get_bus_arrivals"],
         call("navigate", destination_city=C["NTN"], street=st("סמילנסקי"), house_number=5, depart_at=NOW))
multiple(["canonical_value", "date_relative", "time_words", "free_text_hebrew"],
         "מונית ואן מ'העצמאות 30 אשדוד' ל'נתב״ג' מחרתיים בארבע לפנות בוקר",
         ["book_taxi", "book_train", "book_flight"],
         call("book_taxi", pickup="העצמאות 30 אשדוד", destination="נתב״ג", pickup_time=f"{THU}T04:00", vehicle="van"))
multiple(["canonical_value", "date_ddmm", "time_words"], "רכבת מנתניה לנתב״ג ב-9/11 בשש ורבע בבוקר",
         ["book_train", "book_flight", "book_hotel"],
         call("book_train", origin="Netanya", destination="Ben Gurion Airport", date="2026-11-09", time="06:15",
              passengers=ONE))
multiple(["canonical_value", "date_relative"], "מלון באילת מהיום לשלושה לילות, אני והחבר שלי", TRIP,
         call("book_hotel", city=C["ETH"], check_in=TODAY, check_out=d(3), guests=TWO, rooms=ONE))
multiple(["number_words"], "הקו מאה עשרים וחמש מגיע עוד מעט לתחנה 4521?", ["get_bus_arrivals", "book_taxi", "load_rav_kav"],
         call("get_bus_arrivals", stop_code=4521, line="125"))
multiple(["canonical_value", "transliteration", "date_relative"], "תכין מסלול לאשקלון ליציאה מחר בחמש אחר הצהריים",
         ["navigate", "get_fuel_price", "pay_parking"],
         call("navigate", destination_city=C["ASK"], depart_at=f"{TOMORROW}T17:00"))
multiple(["canonical_value", "date_relative"], "טיסה מאילת לתל אביב ביום ראשון לשלושה", FLY,
         call("book_flight", origin="ETM", destination="TLV", depart_date=SUN, return_date=[None], passengers=3))
multiple(["canonical_value"], "חופשי יומי בב״ש לכרטיס 44556677", ["load_rav_kav", "book_train", "get_bus_arrivals"],
         call("load_rav_kav", card_number="44556677", product="daily", area="beer_sheva"))
multiple(["canonical_value", "inference", "date_relative"], "רכבת ממודיעין לחיפה ביום שישי ב-8:10, שני כרטיסים",
         ["book_train", "navigate", "book_taxi"],
         call("book_train", origin="Modiin Center", destination="Haifa Hof HaCarmel", date=FRI, time="08:10", passengers=2))

# --- parallel -------------------------------------------------------------------------------
W = "get_weather"
parallel(["canonical_value", "date_relative"], "מה מזג האוויר בשבת באילת ובטבריה?", [W],
         call(W, city=C["ETH"], date=SAT), call(W, city=C["TIB"], date=SAT))
parallel(["transliteration", "canonical_value"], "מה המצב של אל על 3 ושל ארקיע 352 היום?", ["check_flight_status"],
         call("check_flight_status", flight_number=fl("LY", 3), date=[None, TODAY]),
         call("check_flight_status", flight_number=fl("IZ", 352), date=[None, TODAY]))
parallel(["parallel_multiple", "canonical_value", "transliteration", "date_ddmm"],
         "טיסה לאתונה מת״א ב-5/11 וחזרה ב-9/11 לשניים, ומלון באתונה לאותם תאריכים", ["book_flight", "book_hotel"],
         call("book_flight", origin="TLV", destination="ATH", depart_date="2026-11-05", return_date="2026-11-09",
              passengers=2),
         call("book_hotel", city=C["ATH"], check_in="2026-11-05", check_out="2026-11-09", guests=TWO, rooms=ONE))
parallel(["free_text_hebrew"],
         "תזמין שתי מוניות לעכשיו: אחת מ'ביאליק 10 רמת גן' ל'עזריאלי', והשנייה מ'הירקון 50 בני ברק' ל'עזריאלי'",
         ["book_taxi"],
         call("book_taxi", pickup="ביאליק 10 רמת גן", destination="עזריאלי", pickup_time=NOW),
         call("book_taxi", pickup="הירקון 50 בני ברק", destination="עזריאלי", pickup_time=NOW))
parallel(["canonical_value"], "תטעין חופשי חודשי גוש דן לשני הילדים, רב קו 12121212 ו-34343434", ["load_rav_kav"],
         call("load_rav_kav", card_number="12121212", product="monthly", area="gush_dan"),
         call("load_rav_kav", card_number="34343434", product="monthly", area="gush_dan"))
parallel(["canonical_value", "inference", "date_relative"],
         "רכבת מנתניה לב״ש ביום חמישי ב-8:00, וחזרה ביום שישי ב-13:00", ["book_train"],
         call("book_train", origin="Netanya", destination="Beer Sheva Center", date=THU, time="08:00", passengers=ONE),
         call("book_train", origin="Beer Sheva Center", destination="Netanya", date=FRI, time="13:00", passengers=ONE))
parallel([], "מה מגיע עכשיו לתחנות 10234 ו-10235?", ["get_bus_arrivals"],
         call("get_bus_arrivals", stop_code=10234, line=[None]), call("get_bus_arrivals", stop_code=10235, line=[None]))
parallel(["parallel_multiple", "transliteration", "mixed_direction", "date_relative"],
         "מה מזג האוויר בלונדון מחר, ומה המצב של BA 164 מחר?", [W, "check_flight_status"],
         call(W, city=C["LON"], date=TOMORROW), call("check_flight_status", flight_number=fl("BA", 164), date=TOMORROW))
parallel(["canonical_value", "date_ddmm"], "תזמין: ת״א–רומא ב-10/11, רומא–פריז ב-14/11, ופריז–ת״א ב-18/11", ["book_flight"],
         call("book_flight", origin="TLV", destination="FCO", depart_date="2026-11-10", return_date=[None], passengers=ONE),
         call("book_flight", origin="FCO", destination="CDG", depart_date="2026-11-14", return_date=[None], passengers=ONE),
         call("book_flight", origin="CDG", destination="TLV", depart_date="2026-11-18", return_date=[None], passengers=ONE))
parallel(["canonical_value", "transliteration", "date_relative"], "מה התחזית למחר ברומא, בפריז ובלונדון?", [W],
         *(call(W, city=C[c], date=TOMORROW) for c in ("ROME", "PAR", "LON")))
parallel(["parallel_multiple", "currency_ils", "canonical_value"],
         "תטעין 50 ש״ח לרב-קו 98765432 ותבדוק מתי מגיע קו 1 לתחנה 2786", ["load_rav_kav", "get_bus_arrivals"],
         call("load_rav_kav", card_number="98765432", product="stored_value", amount_ils=50, area=NATIONAL),
         call("get_bus_arrivals", stop_code=2786, line="1"))
parallel(["canonical_value", "date_ddmm"], "מלון בטבריה מ-25/10 עד 27/10, ואחר כך בחיפה מ-27/10 עד 29/10", ["book_hotel"],
         call("book_hotel", city=C["TIB"], check_in="2026-10-25", check_out="2026-10-27", guests=TWO, rooms=ONE),
         call("book_hotel", city=C["HFA"], check_in="2026-10-27", check_out="2026-10-29", guests=TWO, rooms=ONE))
parallel(["canonical_value"], "תפעיל חניה בהרצליה אזור 3 לשני הרכבים שלנו, 1112233 ו-4445566, שעה לכל אחד", ["pay_parking"],
         call("pay_parking", city=C["HRZ"], zone=3, license_plate="1112233", duration_minutes=60),
         call("pay_parking", city=C["HRZ"], zone=3, license_plate="4445566", duration_minutes=60))
parallel(["mixed_direction", "gender_addressee", "date_relative"], "תבדקי לי שלוש טיסות של מחר: LY 1, 6H 101 ו-IZ 621",
         ["check_flight_status"],
         call("check_flight_status", flight_number=fl("LY", 1), date=TOMORROW),
         call("check_flight_status", flight_number=fl("6H", 101), date=TOMORROW),
         call("check_flight_status", flight_number=fl("IZ", 621), date=TOMORROW))
parallel(["parallel_multiple", "canonical_value", "inference", "date_relative", "free_text_hebrew"],
         "תזמין רכבת מחיפה לנתב״ג מחר ב-5:10, ומונית מ'מוריה 40 חיפה' ל'תחנת רכבת חוף הכרמל' מחר ב-4:40",
         ["book_train", "book_taxi"],
         call("book_train", origin="Haifa Hof HaCarmel", destination="Ben Gurion Airport", date=TOMORROW, time="05:10",
              passengers=ONE),
         call("book_taxi", pickup="מוריה 40 חיפה", destination="תחנת רכבת חוף הכרמל", pickup_time=f"{TOMORROW}T04:40"))
parallel(["parallel_multiple", "transliteration", "canonical_value"], "מה מזג האוויר במצפה רמון היום? ותפעיל ניווט לשם",
         [W, "navigate"],
         call(W, city=C["MR"], date=[None, TODAY]), call("navigate", destination_city=C["MR"], depart_at=NOW))
parallel(["canonical_value"], "מה המחיר של בנזין 95 ושל סולר החודש?", ["get_fuel_price"],
         call("get_fuel_price", fuel="gasoline_95", month=[None, "2026-10"]),
         call("get_fuel_price", fuel="diesel", month=[None, "2026-10"]))
parallel(["date_relative", "free_text_hebrew"],
         "מונית ביום חמישי ב-19:00 מ'הגפן 3 רעננה' ל'היכל התרבות', וחזרה מ'היכל התרבות' ל'הגפן 3 רעננה' ב-23:00",
         ["book_taxi"],
         call("book_taxi", pickup="הגפן 3 רעננה", destination="היכל התרבות", pickup_time=f"{THU}T19:00"),
         call("book_taxi", pickup="היכל התרבות", destination="הגפן 3 רעננה", pickup_time=f"{THU}T23:00"))
parallel(["parallel_multiple", "canonical_value", "date_ddmm"], "מלון בעכו מ-12/11 עד 14/11, ומה מזג האוויר שם ב-12/11?",
         ["book_hotel", W],
         call("book_hotel", city=C["ACRE"], check_in="2026-11-12", check_out="2026-11-14", guests=TWO, rooms=ONE),
         call(W, city=C["ACRE"], date="2026-11-12"))
parallel(["parallel_multiple", "canonical_value", "transliteration", "hebrew_calendar", "gematria", "calendar_compute", "inference"],
         "טיסה מנתב״ג לברלין בא׳ בכסלו וחזרה בה׳ בכסלו, ומלון בברלין לאותם תאריכים", ["book_flight", "book_hotel"],
         call("book_flight", origin="TLV", destination="BER", depart_date=heb(5787, KISLEV, 1),
              return_date=heb(5787, KISLEV, 5), passengers=ONE),
         call("book_hotel", city=C["BER"], check_in=heb(5787, KISLEV, 1), check_out=heb(5787, KISLEV, 5),
              guests=[None, 1, 2], rooms=ONE))
parallel(["number_words"], "מתי מגיעים קו ארבע וקו שבעים ושתיים לתחנה 30511?", ["get_bus_arrivals"],
         call("get_bus_arrivals", stop_code=30511, line="4"), call("get_bus_arrivals", stop_code=30511, line="72"))
parallel(["canonical_value", "date_relative"], "מה התחזית ליום שישי בפ״ת ובראשל״צ?", [W],
         call(W, city=C["PT"], date=FRI), call(W, city=C["RLZ"], date=FRI))
parallel(["parallel_multiple", "gender_addressee", "currency_ils", "canonical_value", "inference"],
         "תטעיני 30 שקל לרב קו 77889900 ותזמיני רכבת מנהריה לחוף הכרמל היום ב-12:00", ["load_rav_kav", "book_train"],
         call("load_rav_kav", card_number="77889900", product="stored_value", amount_ils=30, area=NATIONAL),
         call("book_train", origin="Nahariya", destination="Haifa Hof HaCarmel", date=TODAY, time="12:00", passengers=ONE))
parallel(["parallel_multiple", "mixed_direction", "free_text_hebrew"],
         "LY 8 נוחתת היום בזמן? ותזמין מונית מ'נתב״ג טרמינל 3' ל'יפו 97 ירושלים' להיום ב-16:00",
         ["check_flight_status", "book_taxi"],
         call("check_flight_status", flight_number=fl("LY", 8), date=[None, TODAY]),
         call("book_taxi", pickup="נתב״ג טרמינל 3", destination="יפו 97 ירושלים", pickup_time=f"{TODAY}T16:00"))
parallel(["canonical_value", "date_ddmm"], "תזמין טיסה בכיוון אחד מנתב״ג לבודפשט בשבילי ב-3/11, ולאחותי מנתב״ג לווינה ב-4/11",
         ["book_flight"],
         call("book_flight", origin="TLV", destination="BUD", depart_date="2026-11-03", return_date=[None], passengers=ONE),
         call("book_flight", origin="TLV", destination="VIE", depart_date="2026-11-04", return_date=[None], passengers=ONE))

# --- irrelevance ----------------------------------------------------------------------------
irrelevant(["near_miss"], "תזמין לי רכבת מתל אביב סבידור לאילת מחר ב-8:00", ["book_train"])
irrelevant(["near_miss"], "תזמין טיסה מנתב״ג לפאפוס ב-5/11", ["book_flight"])
irrelevant(["near_miss"], "תבטל לי את המונית שהזמנתי לשש", ["book_taxi"])
irrelevant(["near_miss"], "כמה כסף נשאר לי ברב-קו 30512874?", ["load_rav_kav"])
irrelevant(["near_miss"], "תבטל את ההזמנה שלי במלון בטבריה", ["book_hotel"])
irrelevant(["near_miss"], "תשכיר לי רכב באילת מחמישי עד ראשון", ["book_taxi", "navigate"])
irrelevant(["near_miss"], "תעצור את החניה בפנגו, אני כבר נוסע", ["pay_parking"])
irrelevant(["near_miss"], "מתי הרכבת הבאה מנתניה לתל אביב?", ["book_train"])
irrelevant(["near_miss"], "תקנה לי כרטיס לאוטובוס 405 לירושלים", ["get_bus_arrivals"])
irrelevant(["near_miss"], "תזמין לי מעבורת מחיפה ללימסול", ["book_flight"])
irrelevant(["near_miss", "mixed_direction"], "תשלח לי את כרטיס העלייה למטוס של LY 315", ["check_flight_status"])
irrelevant(["near_miss"], "תשלם את החשבונית של כביש 6", ["pay_parking"])
irrelevant(["near_miss"], "מאיזה רציף יוצאת הרכבת לחיפה בסבידור?", ["book_train"])
irrelevant(["near_miss"], "תזמין לי קורקינט שיתופי ליד הבית", ["book_taxi"])
irrelevant(["missing_info"], "תבדוק את מצב הטיסה שלי לאתונה מחר", ["check_flight_status"])
irrelevant(["missing_info"], "תזמין לנו מלון בחיפה", ["book_hotel"])
irrelevant(["missing_info"], "תנווט אותי הביתה", ["navigate"])
irrelevant(["missing_info"], "תטעין לי חופשי חודשי גוש דן ברב-קו", ["load_rav_kav"])
irrelevant(["missing_info"], "מתי מגיע קו 5 לתחנה ליד הבית?", ["get_bus_arrivals"])
irrelevant(["missing_info", "gender_addressee"], "תזמיני מונית לרכבת סבידור, עוד רבע שעה", ["book_taxi"])
irrelevant(["chitchat"], "תודה, הנהג היה ממש נחמד 🙂", ["book_taxi"])
irrelevant(["knowledge"], "מה הקוד של שדה התעופה באילת?", ["book_flight"])
irrelevant(["advice"], "מה עדיף, חופשי חודשי או ערך צבור, אם אני נוסע לעבודה שלוש פעמים בשבוע?", ["load_rav_kav"])
irrelevant(["knowledge"], "צריך דרכון כדי לטוס לאילת?", ["book_flight", "check_flight_status"])
