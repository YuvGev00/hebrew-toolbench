"""pack_home: v1 items (see scripts/packs/AUTHORING.md).

Domain: home, health, food and shopping. Israeli brand drug names must become generic English names,
Hebrew restaurant names must become Latin names, dunams, Hebrew weekdays (the week starts on Sunday)
and time words. Dishes and products in order_food / order_groceries stay in Hebrew, verbatim.
"""

from build_seed import CITY, FRI, MON, SAT, SUN, THU, TODAY, TOMORROW, call, irrelevant, multiple, parallel, simple

# --- brand (or Hebrew-spelled generic) -> generic English name -------------------------------------
DRUG = {
    "paracetamol": ["paracetamol", "acetaminophen"],
    "metamizole": ["metamizole", "metamizol", "dipyrone", "metamizole sodium", "noramidopyrine"],
    "metformin": ["metformin", "metformin hydrochloride", "metformin HCl"],
    "levothyroxine": ["levothyroxine", "levothyroxine sodium", "L-thyroxine", "thyroxine", "levothyroxin"],
    "atorvastatin": ["atorvastatin", "atorvastatin calcium"],
    "amlodipine": ["amlodipine", "amlodipine besylate", "amlodipine besilate"],
    "aspirin": ["aspirin", "acetylsalicylic acid", "ASA"],
    "escitalopram": ["escitalopram", "escitalopram oxalate"],
    "omeprazole": ["omeprazole"],
    "salbutamol": ["salbutamol", "albuterol", "salbutamol sulfate", "albuterol sulfate"],
    "cetirizine": ["cetirizine", "cetirizine hydrochloride", "cetirizine HCl", "cetirizine dihydrochloride"],
    "bisoprolol": ["bisoprolol", "bisoprolol fumarate", "bisoprolol hemifumarate"],
    "esomeprazole": ["esomeprazole", "esomeprazole magnesium"],
    "warfarin": ["warfarin", "warfarin sodium"],
    "furosemide": ["furosemide", "frusemide"],
    "methylphenidate": ["methylphenidate", "methylphenidate hydrochloride", "methylphenidate HCl"],
    "ibuprofen": ["ibuprofen"],
    "diclofenac": ["diclofenac", "diclofenac sodium", "diclofenac potassium"],
    "simvastatin": ["simvastatin"],
}

# --- Hebrew restaurant name -> Latin name as listed --------------------------------------------------
REST = {
    "benedict": ["Benedict", "Benedict Tel Aviv"],
    "japanika": ["Japanika", "Japanica"],
    "miznon": ["Miznon", "HaMiznon", "Ha Miznon", "Ha-Miznon"],
    "dominos": ["Domino's", "Dominos", "Domino's Pizza", "Dominos Pizza"],
    "kosem": ["HaKosem", "Ha Kosem", "Ha-Kosem", "Hakossem", "HaKossem"],
    "abu_hassan": ["Abu Hassan", "Abu Hasan", "Abu Hassan (Ali Karavan)", "Ali Karavan"],
    "mcdonalds": ["McDonald's", "McDonalds", "McDonald's Israel"],
    "taizu": ["Taizu", "Taizo"],
    "machneyuda": ["Machneyuda", "Machne Yuda", "Mahneyuda", "Mahane Yehuda", "Machane Yehuda", "Machneyehuda"],
    "shila": ["Shila", "Shila Sharon Cohen's Kitchen & Bar"],
    "azura": ["Azura"],
    "manta_ray": ["Manta Ray", "Mantaray", "Manta-Ray"],
    "uri_buri": ["Uri Buri", "Uri Bouri", "Uri-Buri", "UriBuri"],
    "landwer": ["Landwer", "Cafe Landwer", "Landwer Cafe", "Café Landwer", "Landwer Café"],
    "hasalon": ["HaSalon", "Ha Salon", "Ha-Salon", "Hasalon"],
    "burgeranch": ["Burgeranch", "Burger Ranch", "BurgeRanch"],
    "pizza_hut": ["Pizza Hut"],
    "port_said": ["Port Said", "Port-Said", "Port Sa'id"],
    "orna_ella": ["Orna and Ella", "Orna & Ella", "Orna ve Ella", "Orna VeElla", "Orna Ve'Ella", "Orna veElla"],
    "nanuchka": ["Nanuchka", "Nanouchka", "Nanuchka Tel Aviv"],
    "raphael": ["Raphael", "Rafael"],
    "habasta": ["HaBasta", "Ha Basta", "Ha-Basta", "Habasta"],
    "greg": ["Cafe Greg", "Greg", "Greg Cafe", "Café Greg", "Greg Café"],
    "agadir": ["Agadir", "Agadir Burger Bar"],
}

NETANYA = ["Netanya", "Netania"]
WORKWEEK = [["sunday", "monday", "tuesday", "wednesday", "thursday"]]
B1 = [None, 1]  # boxes: default 1

# =====================================================================================================
# simple: one tool offered, one call expected (47)
# =====================================================================================================
RX = "renew_prescription"

# renew_prescription (12)
simple(["canonical_value"], "תחדש לי את המרשם של האקמול",
       call(RX, medication=DRUG["paracetamol"], boxes=B1))
simple(["canonical_value", "number_words"], "צריך לחדש מרשם לאופטלגין, שתי קופסאות, אני אוסף בבאר שבע",
       call(RX, medication=DRUG["metamizole"], boxes=2, pickup_city=CITY["BS"]))
simple(["canonical_value", "gender_addressee"], "תחדשי לי את הגלוקומין, 3 קופסאות",
       call(RX, medication=DRUG["metformin"], boxes=3))
simple(["canonical_value"], "נגמר לי האלטרוקסין, תחדש מרשם עם איסוף בחיפה",
       call(RX, medication=DRUG["levothyroxine"], boxes=B1, pickup_city=CITY["HFA"]))
simple(["canonical_value"], "חידוש מרשם לליפיטור בבקשה",
       call(RX, medication=DRUG["atorvastatin"], boxes=B1))
simple(["canonical_value", "number_words"], "תזמין לי חידוש של הנורבסק, ארבע קופסאות לאיסוף בפתח תקווה",
       call(RX, medication=DRUG["amlodipine"], boxes=4, pickup_city=CITY["PT"]))
simple(["canonical_value"], "אני צריכה עוד קרטיה, תחדש לי",
       call(RX, medication=DRUG["aspirin"], boxes=B1))
simple(["canonical_value"], "תחדש את המרשם של הציפרלקס",
       call(RX, medication=DRUG["escitalopram"], boxes=B1))
simple(["canonical_value", "number_words"], "המרשם לאומפרדקס נגמר, תחדש לי שתי קופסאות",
       call(RX, medication=DRUG["omeprazole"], boxes=2))
simple(["transliteration"], "תחדש לי מרשם למטפורמין",
       call(RX, medication=DRUG["metformin"], boxes=B1))
simple(["canonical_value"], "חידוש ונטולין, קופסה אחת, איסוף בכפר סבא",
       call(RX, medication=DRUG["salbutamol"], boxes=B1, pickup_city=CITY["KFS"]))
simple(["canonical_value"], "תחדש לי את הזירטק, עונת האלרגיות מתחילה",
       call(RX, medication=DRUG["cetirizine"], boxes=B1))

# order_food (7)
FOOD = "order_food"
simple(["transliteration", "free_text_hebrew"], "תזמין לי מבנדיקט שקשוקה ומיץ תפוזים סחוט",
       call(FOOD, restaurant=REST["benedict"], items=[["שקשוקה", "מיץ תפוזים סחוט"], ["שקשוקה", "ומיץ תפוזים סחוט"]]))
simple(["transliteration", "free_text_hebrew", "currency_ils"], "בא לי ג׳פניקה. תזמין 'ספייסי סלמון רול' ו'אדממה', טיפ 10 ש״ח",
       call(FOOD, restaurant=REST["japanika"], items=[["ספייסי סלמון רול", "אדממה"]], tip_ils=10))
simple(["transliteration", "free_text_hebrew"], "תעשה הזמנה בוולט ממסעדת 'מזנון': 'כרובית שלמה' ו'פיתה סטייק'",
       call(FOOD, restaurant=REST["miznon"], items=[["כרובית שלמה", "פיתה סטייק"]]))
simple(["transliteration", "free_text_hebrew", "currency_ils", "number_words"],
       "דומינוס, פיצה משפחתית עם זיתים, ותוסיף חמישה עשר שקל טיפ",
       call(FOOD, restaurant=REST["dominos"], items=[["פיצה משפחתית עם זיתים"]], tip_ils=15))
simple(["transliteration", "free_text_hebrew"], "תזמין מהקוסם 'מנה פלאפל' ו'סביח'",
       call(FOOD, restaurant=REST["kosem"], items=[["מנה פלאפל", "סביח"]]))
simple(["transliteration", "free_text_hebrew"], "תזמין לי חומוס מאבו חסן",
       call(FOOD, restaurant=REST["abu_hassan"], items=[["חומוס"], ["וחומוס"]]))
simple(["transliteration", "free_text_hebrew", "currency_ils"], "מקדונלדס, תזמין ביג מק וצ׳יפס גדול, טיפ 5 שקל",
       call(FOOD, restaurant=REST["mcdonalds"], items=[["ביג מק", "צ׳יפס גדול"], ["ביג מק", "וצ׳יפס גדול"]], tip_ils=5))

# order_groceries (5)
GRO = "order_groceries"
simple(["free_text_hebrew", "date_relative", "canonical_value"], "תזמין מהסופר לחם, חלב, ביצים וקוטג׳ למחר בבוקר",
       call(GRO, items=[["לחם", "חלב", "ביצים", "קוטג׳"], ["לחם", "חלב", "ביצים", "וקוטג׳"]], delivery_date=TOMORROW, window="morning"))
simple(["free_text_hebrew", "date_relative", "canonical_value"], "משלוח לשישי בצהריים: חלות, יין לקידוש, נרות שבת",
       call(GRO, items=[["חלות", "יין לקידוש", "נרות שבת"]], delivery_date=FRI, window="noon"))
simple(["free_text_hebrew", "date_ddmm", "canonical_value"], "תזמין קניות ל-29/10 בערב: 'במבה', 'ביסלי גריל', 'שוקו'",
       call(GRO, items=[["במבה", "ביסלי גריל", "שוקו"]], delivery_date="2026-10-29", window="evening"))
simple(["free_text_hebrew", "date_relative"], "צריכה משלוח מהסופר ליום ראשון: אורז, עדשים, שמן זית. לא משנה באיזו שעה",
       call(GRO, items=[["אורז", "עדשים", "שמן זית"]], delivery_date=SUN, window=[None]))
simple(["free_text_hebrew", "date_relative", "canonical_value"], "תזמין לי מהסופר מחרתיים בערב טחינה, פיתות וחומוס",
       call(GRO, items=[["טחינה", "פיתות", "חומוס"]], delivery_date=THU, window="evening"))

# book_table (6)
TB = "book_table"
simple(["transliteration", "date_relative", "time_words"], "תשריין לנו שולחן בטאיזו ביום חמישי בתשע בערב, אנחנו ארבעה",
       call(TB, restaurant=REST["taizu"], date=THU, time="21:00", party_size=4))
simple(["transliteration", "date_relative"], "שולחן לשניים במחניודה מחר ב-20:30",
       call(TB, restaurant=REST["machneyuda"], date=TOMORROW, time="20:30", party_size=2))
simple(["transliteration", "date_ddmm", "time_words"], "תזמין מקום בשילה ל-6 אנשים ב-31/10 ברבע לשמונה בערב",
       call(TB, restaurant=REST["shila"], date="2026-10-31", time="19:45", party_size=6))
simple(["transliteration", "date_relative", "number_words"], "אני רוצה להזמין שולחן בעזורה ביום שני ב-13:00, שלושה סועדים",
       call(TB, restaurant=REST["azura"], date=MON, time="13:00", party_size=3))
simple(["transliteration", "date_relative", "time_words"], "שולחן במנטה ריי לחמישה, בשבת הקרובה באחת וחצי בצהריים",
       call(TB, restaurant=REST["manta_ray"], date=SAT, time="13:30", party_size=5))
simple(["transliteration", "date_ddmm", "time_words"], "תזמין לנו באורי בורי בעכו, 8 אנשים, ב-7/11 בשמונה בערב",
       call(TB, restaurant=REST["uri_buri"], date="2026-11-07", time="20:00", party_size=8))

# set_alarm (7)
AL = "set_alarm"
simple(["time_words"], "תעיר אותי מחר ברבע לשבע",
       call(AL, time="06:45", days=[None]))
simple(["canonical_value"], "שעון מעורר ל-5:30 בימים א׳ עד ה׳",
       call(AL, time="05:30", days=WORKWEEK))
simple(["canonical_value", "time_words", "free_text_hebrew"], "תכוון לי שעון לשבע וחצי בבוקר בכל שישי ושבת עם התווית 'סוף שבוע'",
       call(AL, time="07:30", days=[["friday", "saturday"]], label="סוף שבוע"))
simple(["canonical_value", "time_words", "free_text_hebrew"], "תכוון שעון מעורר לעשרים לשמונה בערב בימי שני ורביעי, תקרא לו 'חדר כושר'",
       call(AL, time="19:40", days=[["monday", "wednesday"]], label="חדר כושר"))
simple(["gender_addressee", "time_words", "free_text_hebrew"], "תכווני שעון מעורר לעשר וחצי בלילה עם הכיתוב 'כדור'",
       call(AL, time="22:30", days=[None], label="כדור"))
simple(["canonical_value", "inference"], "תכוון שעון לשש בבוקר כל יום חוץ משבת",
       call(AL, time="06:00", days=[["sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]]))
simple(["canonical_value", "time_words"], "שעון מעורר לרבע אחרי חמש בבוקר, בכל יום ראשון",
       call(AL, time="05:15", days=[["sunday"]]))

# convert_units (7)
CU = "convert_units"
simple(["unit_local", "canonical_value"], "כמה מטר רבוע זה 5 דונם?",
       call(CU, value=5, from_unit="dunam", to_unit="square_meter"))
simple(["unit_local", "number_words"], "יש לסבא שלי חלקה של שלושה וחצי דונם במושב, כמה זה באקרים?",
       call(CU, value=3.5, from_unit="dunam", to_unit="acre"))
simple(["canonical_value"], "כמה קילו זה 180 פאונד?",
       call(CU, value=180, from_unit="pound", to_unit="kilogram"))
simple(["canonical_value"], "תמיר 42 קילומטר למיילים",
       call(CU, value=42, from_unit="kilometer", to_unit="mile"))
simple(["canonical_value"], "המתכון אומר 350 מעלות פרנהייט, כמה זה בצלזיוס?",
       call(CU, value=350, from_unit="fahrenheit", to_unit="celsius"))
simple(["canonical_value", "inference"], "כמה ליטרים יש בגלון אחד?",
       call(CU, value=1, from_unit="gallon", to_unit="liter"))
simple(["unit_local", "canonical_value"], "2 הקטאר זה כמה דונם?",
       call(CU, value=2, from_unit="hectare", to_unit="dunam"))

# existing tools (3)
simple(["canonical_value", "date_relative", "time_words"], "תור לאורתופד בטבריה ביום חמישי ברבע לעשר בבוקר",
       call("book_doctor", specialty="orthopedics", date=THU, time="09:45", city=CITY["TIB"]))
simple(["canonical_value", "date_ddmm", "time_words"], "צריך רופא אף אוזן גרון בחיפה ב-2/11 בארבע אחה״צ",
       call("book_doctor", specialty="ent", date="2026-11-02", time="16:00", city=CITY["HFA"]))
simple(["date_relative", "free_text_hebrew"], "תזכיר לי ביום ראשון בשמונה בבוקר 'לאסוף תרופות מבית המרקחת'",
       call("set_reminder", text="לאסוף תרופות מבית המרקחת", datetime=f"{SUN}T08:00"))

# =====================================================================================================
# multiple: 3 tools offered, pick the right one (33)
# =====================================================================================================
MED = ["renew_prescription", "book_doctor", "set_reminder"]
FOODG = ["order_food", "order_groceries", "book_table"]
DINE = ["book_table", "search_restaurants", "order_food"]
WAKE = ["set_alarm", "set_reminder", "create_event"]
UNITS = ["convert_units", "convert_currency", "get_weather"]
CLIMATE = ["set_ac", "get_weather", "set_alarm"]

multiple(["canonical_value"], "נגמרו לי הכדורים של הקונקור, תחדש לי", MED,
         call(RX, medication=DRUG["bisoprolol"], boxes=B1))
multiple(["canonical_value", "number_words"], "תחדש מרשם לנקסיום, שתי קופסאות, איסוף בירושלים", MED,
         call(RX, medication=DRUG["esomeprazole"], boxes=2, pickup_city=CITY["JLM"]))
multiple(["canonical_value"], "אני צריך לחדש את הקומדין של אבא שלי", MED,
         call(RX, medication=DRUG["warfarin"], boxes=B1))
multiple(["canonical_value", "date_relative", "time_words"], "תקבע לי תור לרופאת משפחה בדימונה מחר בשמונה ועשרה בבוקר", MED,
         call("book_doctor", specialty="family", date=TOMORROW, time="08:10", city=CITY["DIM"]))
multiple(["canonical_value", "date_ddmm", "gender_addressee"], "תקבעי תור לרופא עיניים בהרצליה ב-12/11 ב-17:00", MED,
         call("book_doctor", specialty="ophthalmology", date="2026-11-12", time="17:00", city=CITY["HRZ"]))
multiple(["date_relative", "time_words", "free_text_hebrew"], "תזכיר לי מחר בתשע בערב 'לקחת אנטיביוטיקה'", MED,
         call("set_reminder", text="לקחת אנטיביוטיקה", datetime=f"{TOMORROW}T21:00"))
multiple(["canonical_value", "date_relative", "time_words"], "הבן שלי צריך רופא ילדים, תקבע לו בנהריה ביום ראשון בעשר וחצי בבוקר", MED,
         call("book_doctor", specialty="pediatrics", date=SUN, time="10:30", city=CITY["NAH"]))
multiple(["canonical_value", "number_words"], "תחדש לי את הפוסיד, שלוש קופסאות", MED,
         call(RX, medication=DRUG["furosemide"], boxes=3))
multiple(["canonical_value"], "המרשם של הריטלין של הבת שלי צריך חידוש, איסוף בראש העין", MED,
         call(RX, medication=DRUG["methylphenidate"], boxes=B1, pickup_city=CITY["RHA"]))
multiple(["transliteration", "free_text_hebrew"], "תזמין מקפה לנדוור 'שניצל בבגט' ו'הפוך גדול'", FOODG,
         call(FOOD, restaurant=REST["landwer"], items=[["שניצל בבגט", "הפוך גדול"]]))
multiple(["free_text_hebrew", "date_relative", "canonical_value"], "תזמין קניות למחר בצהריים: עגבניות, מלפפונים, בצל", FOODG,
         call(GRO, items=[["עגבניות", "מלפפונים", "בצל"]], delivery_date=TOMORROW, window="noon"))
multiple(["transliteration", "date_relative"], "שולחן לשבעה בהסלון ביום שישי ב-22:00", FOODG,
         call(TB, restaurant=REST["hasalon"], date=FRI, time="22:00", party_size=7))
multiple(["transliteration", "free_text_hebrew"], "בא לי בורגראנץ׳, תזמין דאבל צ׳יזבורגר וטבעות בצל", FOODG,
         call(FOOD, restaurant=REST["burgeranch"], items=[["דאבל צ׳יזבורגר", "טבעות בצל"], ["דאבל צ׳יזבורגר", "וטבעות בצל"]]))
multiple(["free_text_hebrew", "date_relative", "canonical_value"],
         "תשלח לי מהסופר ביום חמישי בערב חיתולים, מגבונים ומטרנה", FOODG,
         call(GRO, items=[["חיתולים", "מגבונים", "מטרנה"], ["חיתולים", "מגבונים", "ומטרנה"]], delivery_date=THU, window="evening"))
multiple(["transliteration", "free_text_hebrew", "currency_ils"], "תזמין מפיצה האט 'פיצה פפרוני' ו'לחם שום', טיפ 12 ש״ח", FOODG,
         call(FOOD, restaurant=REST["pizza_hut"], items=[["פיצה פפרוני", "לחם שום"]], tip_ils=12))
multiple(["canonical_value"], "תמצא מסעדה גאורגית בבאר שבע", DINE,
         call("search_restaurants", city=CITY["BS"], cuisine="georgian"))
multiple(["canonical_value", "currency_ils"], "איפה יש אוכל אתיופי בתל אביב עד 80 שקל לאדם?", DINE,
         call("search_restaurants", city=CITY["TA"], cuisine="ethiopian", max_price_per_person_ils=80))
multiple(["transliteration", "date_relative", "number_words", "time_words"], "תזמין שולחן בפורט סעיד הערב בתשע, אנחנו שישה", DINE,
         call(TB, restaurant=REST["port_said"], date=TODAY, time="21:00", party_size=6))
multiple(["canonical_value"], "יש מסעדת דגים כשרה בעכו?", DINE,
         call("search_restaurants", city=CITY["ACRE"], cuisine="fish", kosher=True))
multiple(["transliteration", "free_text_hebrew"], "תזמין משלוח מאורנה ואלה: 'לביבות בטטה' ו'סלט ירוק'", DINE,
         call(FOOD, restaurant=REST["orna_ella"], items=[["לביבות בטטה", "סלט ירוק"]]))
multiple(["transliteration", "date_relative", "inference", "time_words"], "שולחן בננוצ׳קה לזוג ביום ראשון בשמונה וחצי בערב", DINE,
         call(TB, restaurant=REST["nanuchka"], date=SUN, time="20:30", party_size=2))
multiple(["canonical_value", "time_words"], "שעון לשש ועשרים בבוקר, בימים ב׳ ו-ד׳", WAKE,
         call(AL, time="06:20", days=[["monday", "wednesday"]]))
multiple(["time_words"], "תעיר אותי מחר בחמש לפנות בוקר", WAKE,
         call(AL, time="05:00", days=[None]))
multiple(["date_relative", "free_text_hebrew"], "תזכיר לי ביום שישי בעשר בבוקר 'להזמין עוף לשבת'", WAKE,
         call("set_reminder", text="להזמין עוף לשבת", datetime=f"{FRI}T10:00"))
multiple(["canonical_value", "time_words", "free_text_hebrew"], "כל שבת בשמונה וחצי בבוקר, שעון מעורר בשם 'בית כנסת'", WAKE,
         call(AL, time="08:30", days=[["saturday"]], label="בית כנסת"))
multiple(["canonical_value"], "כמה מעלות צלזיוס זה 98.6 פרנהייט?", UNITS,
         call(CU, value=98.6, from_unit="fahrenheit", to_unit="celsius"))
multiple(["unit_local", "number_format"], "כמה דונם זה 10,000 מטר רבוע?", UNITS,
         call(CU, value=10000, from_unit="square_meter", to_unit="dunam"))
multiple(["canonical_value"], "התינוקת נולדה 7.5 פאונד, כמה זה בקילו?", UNITS,
         call(CU, value=7.5, from_unit="pound", to_unit="kilogram"))
multiple(["canonical_value"], "כמה גלונים זה 50 ליטר?", UNITS,
         call(CU, value=50, from_unit="liter", to_unit="gallon"))
multiple(["canonical_value", "number_words"], "קר בחדר של הילדים, תדליק חימום על עשרים וארבע", CLIMATE,
         call("set_ac", room="kids_room", temperature_c=24, mode="heat"))
multiple(["canonical_value"], "תפעיל במשרד את המזגן על ייבוש, 26 מעלות", CLIMATE,
         call("set_ac", room="office", temperature_c=26, mode="dry"))
multiple(["canonical_value"], "תשים מאוורר בחדר השינה על 27", CLIMATE,
         call("set_ac", room="bedroom", temperature_c=27, mode="fan"))
multiple(["transliteration", "date_ddmm"], "תזמין שולחן לעשרה ברפאל ב-15/11 ב-19:00", FOODG,
         call(TB, restaurant=REST["raphael"], date="2026-11-15", time="19:00", party_size=10))

# =====================================================================================================
# parallel: several calls in one turn (25)
# =====================================================================================================
parallel(["canonical_value"], "תחדש לי מרשם לאקמול ולנורופן", [RX],
         call(RX, medication=DRUG["paracetamol"], boxes=B1), call(RX, medication=DRUG["ibuprofen"], boxes=B1))
parallel(["canonical_value"], "אבא צריך חידוש לליפיטור, לנורבסק ולגלוקופאג׳, הכול לאיסוף בעכו", [RX],
         *(call(RX, medication=DRUG[m], boxes=B1, pickup_city=CITY["ACRE"]) for m in ("atorvastatin", "amlodipine", "metformin")))
parallel(["date_relative", "time_words"], "שני שעונים מעוררים למחר: אחד לשש בבוקר ואחד לשש ורבע", [AL],
         call(AL, time="06:00", days=[None]), call(AL, time="06:15", days=[None]))
parallel(["canonical_value"], "תכוון שעון לשבע בבוקר בימים א׳-ה׳ ולתשע בבוקר בשישי ושבת", [AL],
         call(AL, time="07:00", days=WORKWEEK), call(AL, time="09:00", days=[["friday", "saturday"]]))
parallel(["unit_local", "canonical_value"], "כמה מטר רבוע זה 4 דונם, וכמה זה באקרים?", [CU],
         call(CU, value=4, from_unit="dunam", to_unit="square_meter"), call(CU, value=4, from_unit="dunam", to_unit="acre"))
parallel(["canonical_value"], "תמיר 10 ק״מ, 21.1 ק״מ ו-42.2 ק״מ למיילים", [CU],
         *(call(CU, value=v, from_unit="kilometer", to_unit="mile") for v in (10, 21.1, 42.2)))
parallel(["transliteration", "date_relative"], "תזמין שולחן לשניים בטאיזו מחר ב-20:00 ושולחן לארבעה בשילה ביום חמישי ב-21:00", [TB],
         call(TB, restaurant=REST["taizu"], date=TOMORROW, time="20:00", party_size=2),
         call(TB, restaurant=REST["shila"], date=THU, time="21:00", party_size=4))
parallel(["transliteration", "free_text_hebrew"], "תזמין 'פיצה מרגריטה' מדומינוס ו'בורגר קלאסי' מבורגראנץ׳", [FOOD],
         call(FOOD, restaurant=REST["dominos"], items=[["פיצה מרגריטה"]]),
         call(FOOD, restaurant=REST["burgeranch"], items=[["בורגר קלאסי"]]))
parallel(["canonical_value"], "תכוון 22 בקירור בסלון, בחדר השינה ובחדר של הילדים", ["set_ac"],
         *(call("set_ac", room=r, temperature_c=22, mode="cool") for r in ("living_room", "bedroom", "kids_room")))
parallel(["canonical_value", "date_relative"], "תור לרופא עור ב-9:00 ולרופא עיניים ב-11:00, שניהם ביום ראשון בחיפה", ["book_doctor"],
         call("book_doctor", specialty="dermatology", date=SUN, time="09:00", city=CITY["HFA"]),
         call("book_doctor", specialty="ophthalmology", date=SUN, time="11:00", city=CITY["HFA"]))
parallel(["date_relative", "free_text_hebrew"], "תזכיר לי היום ב-14:00 'לקחת כדור' ושוב ב-22:00 'לקחת כדור'", ["set_reminder"],
         call("set_reminder", text="לקחת כדור", datetime=f"{TODAY}T14:00"),
         call("set_reminder", text="לקחת כדור", datetime=f"{TODAY}T22:00"))
parallel(["canonical_value"], "חפש מסעדות תימניות בראש העין ובפתח תקווה", ["search_restaurants"],
         call("search_restaurants", city=CITY["RHA"], cuisine="yemenite"),
         call("search_restaurants", city=CITY["PT"], cuisine="yemenite"))
parallel(["parallel_multiple", "canonical_value", "date_relative"],
         "תחדש לי את הוולטרן ותקבע תור לאורתופד בכפר סבא ביום שני ב-16:30", [RX, "book_doctor"],
         call(RX, medication=DRUG["diclofenac"], boxes=B1),
         call("book_doctor", specialty="orthopedics", date=MON, time="16:30", city=CITY["KFS"]))
parallel(["parallel_multiple", "free_text_hebrew", "date_relative", "time_words", "canonical_value"],
         "תזמין מהסופר למחר בבוקר 'חלב סויה' ו'גרנולה', ותזכיר לי היום בשש בערב 'לפנות מקום במקרר'",
         [GRO, "set_reminder"],
         call(GRO, items=[["חלב סויה", "גרנולה"]], delivery_date=TOMORROW, window="morning"),
         call("set_reminder", text="לפנות מקום במקרר", datetime=f"{TODAY}T18:00"))
parallel(["parallel_multiple", "transliteration", "date_relative", "free_text_hebrew"],
         "שולחן לחמישה בהבסטה ביום ראשון ב-20:00, ותזכיר לי באותו יום ב-18:00 'לסגור בייביסיטר'", [TB, "set_reminder"],
         call(TB, restaurant=REST["habasta"], date=SUN, time="20:00", party_size=5),
         call("set_reminder", text="לסגור בייביסיטר", datetime=f"{SUN}T18:00"))
parallel(["parallel_multiple", "canonical_value", "time_words"],
         "תכוון שעון מעורר לרבע לשש בבוקר בימי ראשון עד חמישי ותדליק חימום בחדר השינה על 23", [AL, "set_ac"],
         call(AL, time="05:45", days=WORKWEEK),
         call("set_ac", room="bedroom", temperature_c=23, mode="heat"))
parallel(["parallel_multiple", "canonical_value", "currency_ils"], "כמה קילו זה 5 פאונד, וכמה זה 20 דולר בשקלים?",
         [CU, "convert_currency"],
         call(CU, value=5, from_unit="pound", to_unit="kilogram"),
         call("convert_currency", amount=20, from_currency="USD", to_currency="ILS"))
parallel(["parallel_multiple", "transliteration", "free_text_hebrew", "date_relative"],
         "תזמין מגרג 'סלט חלומי' ותזכיר לי בעוד שעה 'לפתוח לשליח את השער'", [FOOD, "set_reminder"],
         call(FOOD, restaurant=REST["greg"], items=[["סלט חלומי"]]),
         call("set_reminder", text="לפתוח לשליח את השער", datetime=f"{TODAY}T10:00"))
parallel(["free_text_hebrew", "date_relative", "canonical_value"],
         "שני משלוחים מהסופר: 'תפוחי אדמה' ו'גזר' למחר בבוקר, ו'עוף שלם' לשישי בצהריים", [GRO],
         call(GRO, items=[["תפוחי אדמה", "גזר"]], delivery_date=TOMORROW, window="morning"),
         call(GRO, items=[["עוף שלם"]], delivery_date=FRI, window="noon"))
parallel(["parallel_multiple", "canonical_value", "date_relative", "inference"],
         "תחדש לי שתי קופסאות סימבקור עם איסוף בדימונה, ותקבע לי תור לרופא משפחה שם ביום חמישי ב-8:00",
         [RX, "book_doctor"],
         call(RX, medication=DRUG["simvastatin"], boxes=2, pickup_city=CITY["DIM"]),
         call("book_doctor", specialty="family", date=THU, time="08:00", city=CITY["DIM"]))
parallel(["canonical_value"], "כמה זה 20 ו-30 מעלות צלזיוס בפרנהייט?", [CU],
         call(CU, value=20, from_unit="celsius", to_unit="fahrenheit"),
         call(CU, value=30, from_unit="celsius", to_unit="fahrenheit"))
parallel(["parallel_multiple", "transliteration", "free_text_hebrew", "date_relative", "number_words"],
         "תזמין לי עכשיו מאגדיר 'המבורגר 300 גרם', ותשריין שם שולחן לשלושה בשבת ב-13:00", [FOOD, TB],
         call(FOOD, restaurant=REST["agadir"], items=[["המבורגר 300 גרם"]]),
         call(TB, restaurant=REST["agadir"], date=SAT, time="13:00", party_size=3))
parallel(["canonical_value"], "בסלון תשים קירור על 24 ובמשרד ייבוש על 25", ["set_ac"],
         call("set_ac", room="living_room", temperature_c=24, mode="cool"),
         call("set_ac", room="office", temperature_c=25, mode="dry"))
parallel(["transliteration"], "תחדש לי מרשם לאומפרזול ולאמלודיפין", [RX],
         call(RX, medication=DRUG["omeprazole"], boxes=B1), call(RX, medication=DRUG["amlodipine"], boxes=B1))
parallel(["date_relative", "free_text_hebrew", "time_words"],
         "תזכיר לי ביום חמישי בשבע וחצי בבוקר 'בדיקת דם בצום' וביום שישי בצהריים ב-12:00 'לאסוף תוצאות'", ["set_reminder"],
         call("set_reminder", text="בדיקת דם בצום", datetime=f"{THU}T07:30"),
         call("set_reminder", text="לאסוף תוצאות", datetime=f"{FRI}T12:00"))

# =====================================================================================================
# irrelevance: no offered tool fits (24)
# =====================================================================================================
irrelevant(["near_miss"], "תקבע לי תור לפסיכולוג ביום ראשון בחיפה", ["book_doctor"])
irrelevant(["near_miss"], "תבדוק אם יש אופטלגין במלאי בבית המרקחת ליד הבית", [RX])
irrelevant(["near_miss"], "תבטל את ההזמנה מוולט, זה מתעכב יותר מדי", [FOOD])
irrelevant(["near_miss"], "תבטל את השעון המעורר של שש בבוקר", [AL])
irrelevant(["near_miss"], "כמה כפות זה 100 גרם סוכר?", [CU])
irrelevant(["near_miss"], "תדליק את הדוד, אני רוצה להתקלח בעוד שעה", ["set_ac"])
irrelevant(["near_miss"], "תחדש לי את המנוי לחדר כושר", [RX])
irrelevant(["near_miss"], "תזמין מאיקאה מגבות וסדינים", [GRO])
irrelevant(["near_miss"], "תקבע לי תור לרופא שיניים ביום ראשון בעשר בבאר שבע", ["book_doctor"])
irrelevant(["near_miss"], "כמה גרם זה 3 כוסות קמח?", [CU, "convert_currency"])
irrelevant(["near_miss"], "תשריין לי תור במספרה ביום חמישי בחמש", [TB])
irrelevant(["near_miss"], "תדליק את המזגן באמבטיה על 25", ["set_ac"])
irrelevant(["near_miss"], "תוריד את התריסים בסלון", ["set_ac", AL])
irrelevant(["near_miss"], "תזמין לי מונית מהמסעדה הביתה", [TB, FOOD])
irrelevant(["missing_info"], "תזמין לנו שולחן לארבעה מחר בערב", [TB])
irrelevant(["missing_info"], "תזכיר לי לקחת את הכדור", ["set_reminder"])
irrelevant(["missing_info"], "תחדש לי את המרשם", [RX])
irrelevant(["knowledge"], "כמה קלוריות יש במנה פלאפל בפיתה?", [FOOD])
irrelevant(["knowledge"], "איך מכינים שקשוקה?", [FOOD, GRO])
irrelevant(["missing_info", "unit_local"], "כמה דונם יש לסבא שלי במושב, תמיר לי לאקרים", [CU])
irrelevant(["knowledge"], "מה המינון המקסימלי של אקמול ביום למבוגר?", [RX])
irrelevant(["advice"], "כדאי לי לעבור מכללית למכבי?", ["book_doctor"])
irrelevant(["chitchat", "gender_morphology"], "אני מרגישה קצת חולה היום, סתם רציתי לפרוק", ["book_doctor", "set_reminder"])
irrelevant(["chitchat"], "בוקר טוב! איזה יום יפה היום", [FOOD, "set_alarm"])

