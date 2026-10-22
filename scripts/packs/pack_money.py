"""pack_money: v1 items (see scripts/packs/AUTHORING.md).

Domain: money, work and housing. Net salary with credit points, Yad2 apartment search (half rooms),
job search (Hebrew titles -> English), fuel prices, currency, VAT, loans, stock quotes (Hebrew company
names -> tickers), Bit transfers and household bills.
"""

from build_seed import CITY, TODAY, call, irrelevant, multiple, parallel, simple

MONTH_NOW = [None, TODAY[:7]]  # "2026-10": get_fuel_price defaults to the current month
LAST_MONTH, NEXT_MONTH = "2026-09", "2026-11"

C = {
    **CITY,
    "RG": ["Ramat Gan"],
    "RLZ": ["Rishon LeZion", "Rishon Lezion", "Rishon Le Zion", "Rishon LeTsiyon", "Rishon LeZiyyon", "Rishon Letzion"],
    "HOL": ["Holon"],
    "NET": ["Netanya", "Natanya"],
    "ASD": ["Ashdod"],
    "MOD": ["Modiin", "Modi'in", "Modiin-Maccabim-Reut", "Modi'in-Maccabim-Re'ut", "Modiin Maccabim Reut"],
    "RAN": ["Raanana", "Ra'anana"],
    "GIV": ["Givatayim", "Giv'atayim"],
    "REH": ["Rehovot"],
    "KAR": ["Karmiel", "Carmiel"],
    "HAD": ["Hadera"],
    "KG": ["Kiryat Gat", "Qiryat Gat"],
    "AFU": ["Afula"],
    "HOD": ["Hod HaSharon", "Hod Hasharon", "Hod Ha-Sharon"],
}

# Hebrew job titles -> every reasonable English title an API would accept.
J = {
    "backend": ["Backend Developer", "Backend Engineer", "Back-end Developer", "Back End Developer",
                "Back-End Developer", "Back-end Engineer", "Back End Engineer", "Backend Software Engineer"],
    "frontend": ["Frontend Developer", "Frontend Engineer", "Front-end Developer", "Front End Developer",
                 "Front-End Developer", "Front-end Engineer", "Front End Engineer"],
    "fullstack": ["Full Stack Developer", "Fullstack Developer", "Full-Stack Developer", "Full Stack Engineer",
                  "Fullstack Engineer", "Full-Stack Engineer", "Full Stack", "Fullstack", "Full-Stack"],
    "data_scientist": ["Data Scientist"],
    "pm": ["Product Manager"],
    "devops": ["DevOps Engineer", "DevOps", "DevOps Developer"],
    "qa": ["QA Engineer", "QA Tester", "QA Analyst", "QA", "Software Tester", "Quality Assurance Engineer",
           "Software QA Engineer", "QA Automation Engineer"],
    "nurse": ["Nurse", "Registered Nurse"],
    "accountant": ["Accountant", "CPA", "Certified Public Accountant"],
    "math_teacher": ["Math Teacher", "Mathematics Teacher", "Maths Teacher"],
    "truck": ["Truck Driver"],
    "electrician": ["Electrician"],
    "sales": ["Salesperson", "Sales Representative", "Sales Rep", "Sales Associate", "Sales Agent", "Sales Person"],
    "physio": ["Physiotherapist", "Physical Therapist"],
    "civil": ["Civil Engineer"],
    "med_secretary": ["Medical Secretary", "Medical Receptionist", "Medical Office Secretary"],
    "android": ["Android Developer", "Android Engineer"],
    "kg_teacher": ["Kindergarten Teacher", "Preschool Teacher"],
    "hw": ["Hardware Engineer"],
}

# Hebrew company names -> tickers (with the TASE suffix for dual-listed names).
T = {
    "TEVA": ["TEVA", "TEVA.TA"],
    "LUMI": ["LUMI", "LUMI.TA"],
    "POLI": ["POLI", "POLI.TA"],
    "DSCT": ["DSCT", "DSCT.TA"],
    "MZTF": ["MZTF", "MZTF.TA"],
    "BEZQ": ["BEZQ", "BEZQ.TA"],
    "TSEM": ["TSEM", "TSEM.TA"],
    "NVMI": ["NVMI", "NVMI.TA"],
    "ORA": ["ORA", "ORA.TA"],
    "ICL": ["ICL", "ICL.TA"],
    "ELAL": ["ELAL", "ELAL.TA"],
    "DOX": ["DOX"],
    "WIX": ["WIX"],
    "MNDY": ["MNDY"],
    "NVDA": ["NVDA"],
    "AAPL": ["AAPL"],
    "MSFT": ["MSFT"],
}

NET, APT, JOBS, FUEL, FX, VAT, LOAN, STOCK, BIT, BILL = (
    "calculate_net_salary", "search_apartments", "search_jobs", "get_fuel_price", "convert_currency",
    "calculate_vat", "loan_payment", "get_stock_quote", "send_bit", "pay_bill",
)

# --- simple (47) ------------------------------------------------------------------------------
# net salary
simple(["number_format"], "כמה נטו יוצא מ-18,000 ברוטו? יש לי 2.25 נקודות זיכוי",
       call(NET, gross_ils=18000, credit_points=2.25))
simple(["currency_ils", "number_words"],
       "אני מרוויחה שתים עשרה אלף וחמש מאות שקל ברוטו, עם 2.75 נקודות זיכוי. כמה נשאר לי ביד?",
       call(NET, gross_ils=12500, credit_points=2.75))
simple(["number_format", "number_words"], "תחשב לי נטו: ברוטו 22.5K, שלוש נקודות זיכוי, הפרשה לפנסיה 6%",
       call(NET, gross_ils=22500, credit_points=3, pension_percent=6))
simple(["currency_ils", "number_format", "number_words"],
       "משכורת של 9,800 ₪ ברוטו, ארבע וחצי נקודות זיכוי ו-7 אחוז פנסיה – כמה נטו?",
       call(NET, gross_ils=9800, credit_points=4.5, pension_percent=7))
simple(["inference", "number_words"], "יש לי 2.25 נקודות בסיס ועוד נקודה וחצי על הילדה. מה הנטו מ-15 אלף ברוטו?",
       call(NET, gross_ils=15000, credit_points=2.25 + 1.5))
simple(["number_words"], "הציעו לי שלושים אלף ברוטו לחודש. עם 2.25 נקודות זיכוי כמה זה בנטו?",
       call(NET, gross_ils=30000, credit_points=2.25))
simple(["gender_addressee", "currency_ils", "number_format"], "ברוטו 7,400 ש״ח, נקודות זיכוי 2.75, פנסיה 6 – תחשבי נטו",
       call(NET, gross_ils=7400, credit_points=2.75, pension_percent=6))
simple(["number_words"], "כמה ייכנס לי לבנק מ-11 אלף ברוטו אם יש לי שתיים ורבע נקודות זיכוי?",
       call(NET, gross_ils=11000, credit_points=2.25))
# apartments
simple(["canonical_value", "half_rooms", "currency_ils", "number_format"],
       "תחפש לי דירה להשכרה בתל אביב, 3.5 חדרים, עד 7,500 ש״ח לחודש",
       call(APT, city=C["TA"], deal="rent", min_rooms=3.5, max_price_ils=7500))
simple(["canonical_value", "half_rooms", "number_words", "number_format"],
       "מחפשת לקנות דירת ארבעה וחצי חדרים במודיעין, תקציב עד 2.6 מיליון",
       call(APT, city=C["MOD"], deal="buy", min_rooms=4.5, max_price_ils=2600000))
simple(["canonical_value", "free_text_hebrew"], "דירות להשכרה בשכונת 'פלורנטין' בתל אביב, לפחות 2 חדרים",
       call(APT, city=C["TA"], deal="rent", min_rooms=2, neighborhood="פלורנטין"))
simple(["canonical_value", "number_words"], "יש משהו למכירה בבאר שבע עד מיליון ומאתיים אלף?",
       call(APT, city=C["BS"], deal="buy", max_price_ils=1200000))
simple(["canonical_value", "free_text_hebrew", "currency_ils", "number_format"],
       "תמצא לי שכירות בחיפה בשכונת 'הדר', עד 4,000 שקל",
       call(APT, city=C["HFA"], deal="rent", max_price_ils=4000, neighborhood="הדר"))
simple(["canonical_value", "half_rooms", "number_words"], "דירת שלושה חדרים וחצי למכירה ברמת גן",
       call(APT, city=C["RG"], deal="buy", min_rooms=3.5))
simple(["canonical_value", "free_text_hebrew", "number_words"],
       "אני רוצה לשכור בירושלים בשכונת קטמון, חמישה חדרים, עד 9 אלף",
       call(APT, city=C["JLM"], deal="rent", min_rooms=5, max_price_ils=9000, neighborhood="קטמון"))
simple(["canonical_value", "half_rooms"], "דירה לקנייה בראשון לציון, לפחות 5.5 חדרים",
       call(APT, city=C["RLZ"], deal="buy", min_rooms=5.5))
simple(["canonical_value", "half_rooms", "currency_ils", "number_format"],
       "דירת חדר וחצי להשכרה באשדוד עד 2,800 ₪",
       call(APT, city=C["ASD"], deal="rent", min_rooms=1.5, max_price_ils=2800))
# jobs
simple(["canonical_value"], "תמצא לי משרות של מפתח בקאנד בתל אביב",
       call(JOBS, title=J["backend"], city=C["TA"]))
simple(["canonical_value", "gender_morphology"], "מחפשת עבודה כדאטה סיינטיסטית מהבית",
       call(JOBS, title=J["data_scientist"], remote=True))
simple(["canonical_value"], "יש משרות לאחות בחיפה?",
       call(JOBS, title=J["nurse"], city=C["HFA"]))
simple(["canonical_value"], "עבודה כרואה חשבון בירושלים עם לפחות 3 שנות ניסיון",
       call(JOBS, title=J["accountant"], city=C["JLM"], min_experience_years=3))
simple(["canonical_value"], "משרות לנהג משאית באשדוד",
       call(JOBS, title=J["truck"], city=C["ASD"]))
simple(["canonical_value", "number_words"], "חפש משרה של מנהל מוצר בהרצליה, לפחות חמש שנות ניסיון",
       call(JOBS, title=J["pm"], city=C["HRZ"], min_experience_years=5))
simple(["canonical_value"], "אני חשמלאי מוסמך, יש עבודה בכרמיאל?",
       call(JOBS, title=J["electrician"], city=C["KAR"]))
simple(["canonical_value"], "משרות פולסטאק מרחוק",
       call(JOBS, title=J["fullstack"], remote=True))
simple(["canonical_value"], "מורה למתמטיקה בפתח תקווה, יש משרות פנויות?",
       call(JOBS, title=J["math_teacher"], city=C["PT"]))
# fuel
simple(["canonical_value", "date_relative"], "כמה עולה ליטר בנזין 95 החודש?",
       call(FUEL, fuel="gasoline_95", month=MONTH_NOW))
simple(["canonical_value", "date_relative"], "מה המחיר של סולר בחודש הבא?",
       call(FUEL, fuel="diesel", month=NEXT_MONTH))
simple(["canonical_value", "inference"], "כמה היה הבנזין באוגוסט?",
       call(FUEL, fuel="gasoline_95", month="2026-08"))
simple(["canonical_value"], "מחיר דיזל לינואר 2027",
       call(FUEL, fuel="diesel", month="2027-01"))
# currency
simple(["canonical_value", "currency_ils", "number_format"], "כמה זה 4,300 שקל בדולרים?",
       call(FX, amount=4300, from_currency="ILS", to_currency="USD"))
simple(["canonical_value", "currency_ils", "number_format"], "קיבלתי משכורת של 2,800 פאונד, תמיר לי לשקלים",
       call(FX, amount=2800, from_currency="GBP", to_currency="ILS"))
simple(["canonical_value", "number_words"], "תמיר שמונה מאות פרנק שוויצרי לאירו",
       call(FX, amount=800, from_currency="CHF", to_currency="EUR"))
simple(["canonical_value", "currency_ils", "number_words"], "כמה ין יפני מקבלים על 150 אלף שקל?",
       call(FX, amount=150000, from_currency="ILS", to_currency="JPY"))
# VAT
simple(["currency_ils", "number_format"], "הקבלן ביקש 42,000 ש״ח לפני מע״מ על השיפוץ. כמה זה עם מע״מ?",
       call(VAT, amount_ils=42000, includes_vat=False))
simple(["currency_ils", "number_format"], "החשבונית יצאה 9,440 ₪ כולל מע״מ, כמה המחיר בלי?",
       call(VAT, amount_ils=9440, includes_vat=True))
# loans
simple(["number_words"], "משכנתא של 950 אלף ל-20 שנה בריבית 4.9%, מה ההחזר?",
       call(LOAN, principal_ils=950000, annual_rate_percent=4.9, years=20))
simple(["currency_ils", "number_format", "number_words"],
       "לקחתי הלוואה לרכב, 120,000 ₪ לשש שנים בריבית של 7 אחוזים. כמה בחודש?",
       call(LOAN, principal_ils=120000, annual_rate_percent=7, years=6))
simple(["currency_ils", "number_words"],
       "כמה אשלם בחודש על משכנתא של מיליון שש מאות אלף שקל לשלושים שנה בריבית ארבעה אחוז?",
       call(LOAN, principal_ils=1600000, annual_rate_percent=4, years=30))
# stocks
simple(["transliteration", "canonical_value"], "מה המחיר של מניית הפועלים?",
       call(STOCK, ticker=T["POLI"]))
simple(["transliteration", "canonical_value"], "כמה עולה היום מניה של בזק?",
       call(STOCK, ticker=T["BEZQ"]))
simple(["transliteration", "canonical_value", "gender_addressee"], "תבדקי לי את מאנדיי בבורסה",
       call(STOCK, ticker=T["MNDY"]))
simple(["transliteration", "canonical_value"], "מה השער של טאואר?",
       call(STOCK, ticker=T["TSEM"]))
# Bit and bills
simple(["currency_ils", "mixed_direction", "free_text_hebrew"],
       "תעביר בביט 320 שקל לשירה, 052-8834410, ותכתוב 'שכר דירה חלק שלי'",
       call(BIT, phone="0528834410", amount_ils=320, note="שכר דירה חלק שלי"))
simple(["gender_addressee", "number_words", "mixed_direction", "currency_ils"],
       "שלחי בביט אלף ומאתיים ש״ח ל-054-6620913",
       call(BIT, phone="0546620913", amount_ils=1200))
simple(["canonical_value", "mixed_direction", "currency_ils", "number_format"],
       "תשלם את חשבון המים, מספר צרכן 20-118734, סכום 286.40 שקל",
       call(BILL, provider="water", account_number="20-118734", amount_ils=286.4))

simple(["canonical_value", "currency_ils"], "תשלם את חשבון האינטרנט, מספר מנוי 88120456, 109 ₪",
       call(BILL, provider=["internet", "bezeq"], account_number="88120456", amount_ils=109))

# --- multiple (34) ----------------------------------------------------------------------------
JOB3 = [JOBS, APT, NET]
APT3 = [APT, LOAN, JOBS]
SAL3 = [NET, "request_tax_refund", "check_bituach_leumi_payment"]
FUEL3 = [FUEL, "pay_parking", FX]
PAY3 = [BILL, BIT, VAT]
MKT3 = [STOCK, FX, "get_news"]
FX3 = [FX, VAT, LOAN]
LOAN3 = [LOAN, APT, NET]

multiple(["canonical_value", "gender_morphology"], "תחפש משרות של מפתחת פרונטאנד ברעננה", JOB3,
         call(JOBS, title=J["frontend"], city=C["RAN"]))
multiple(["number_format"], "מה הנטו שלי אם הברוטו 16,200 ויש לי 2.75 נקודות זיכוי?", SAL3,
         call(NET, gross_ils=16200, credit_points=2.75))
multiple(["canonical_value", "half_rooms", "number_format"], "דירת 3.5 חדרים להשכרה בגבעתיים עד 6,800", APT3,
         call(APT, city=C["GIV"], deal="rent", min_rooms=3.5, max_price_ils=6800))
multiple(["canonical_value", "date_relative"], "מה המחיר המקסימלי של סולר באוקטובר?", FUEL3,
         call(FUEL, fuel="diesel", month=MONTH_NOW))
multiple(["canonical_value", "currency_ils", "mixed_direction"], "תשלם לבזק 89.90 ש״ח, מספר לקוח 7731205", PAY3,
         call(BILL, provider="bezeq", account_number="7731205", amount_ils=89.9))
multiple(["transliteration", "canonical_value"], "מה עושה מניית אמדוקס היום?", MKT3,
         call(STOCK, ticker=T["DOX"]))
multiple(["canonical_value", "currency_ils", "number_words"], "כמה שווים 12 אלף יורו בשקלים?", FX3,
         call(FX, amount=12000, from_currency="EUR", to_currency="ILS"))
multiple(["number_words"], "משכנתא של שני מיליון לעשרים וחמש שנה בריבית 5.1 אחוז, כמה ההחזר?", LOAN3,
         call(LOAN, principal_ils=2000000, annual_rate_percent=5.1, years=25))
multiple(["canonical_value"], "מחפש עבודה כאיש מכירות בנתניה", JOB3,
         call(JOBS, title=J["sales"], city=C["NET"]))
multiple(["canonical_value", "gender_morphology"], "יש עבודה לפיזיותרפיסטית ברחובות?", JOB3,
         call(JOBS, title=J["physio"], city=C["REH"]))
multiple(["canonical_value", "number_words"], "תמצא לי דירה לקנות בחולון עם ארבעה חדרים לפחות", APT3,
         call(APT, city=C["HOL"], deal="buy", min_rooms=4))
multiple(["number_words"], "כמה נטו נשאר ממשכורת של 26 אלף? 2.25 נקודות, 6.5% לפנסיה", SAL3,
         call(NET, gross_ils=26000, credit_points=2.25, pension_percent=6.5))
multiple(["currency_ils", "mixed_direction", "free_text_hebrew"],
         "תעביר ביט של 75 ש״ח ל-058-3301122, הערה: 'מתנה למורה'", PAY3,
         call(BIT, phone="0583301122", amount_ils=75, note="מתנה למורה"))
multiple(["canonical_value", "currency_ils", "number_format", "mixed_direction"],
         "שלם ארנונה לחשבון 100-552-13, 1,612 שקל", PAY3,
         call(BILL, provider="arnona", account_number="100-552-13", amount_ils=1612))
multiple(["transliteration", "canonical_value"], "מה המחיר של מזרחי טפחות?", MKT3,
         call(STOCK, ticker=T["MZTF"]))
multiple(["transliteration", "canonical_value"], "תבדוק כמה עולה אל על בבורסה", MKT3,
         call(STOCK, ticker=T["ELAL"]))
multiple(["currency_ils", "number_format"], "מה המע״מ על 3,300 ש״ח לפני מע״מ?", FX3,
         call(VAT, amount_ils=3300, includes_vat=False))
multiple(["currency_ils", "number_words"], "הלוואה של 45 אלף שקל ל-3 שנים בריבית 8.5%, מה התשלום החודשי?", FX3,
         call(LOAN, principal_ils=45000, annual_rate_percent=8.5, years=3))
multiple(["canonical_value", "mixed_direction", "number_words"], "משרות DevOps בבאר שבע עם לפחות שנתיים ניסיון", JOB3,
         call(JOBS, title=J["devops"], city=C["BS"], min_experience_years=2))
multiple(["canonical_value"], "אני מחפש עבודה כמהנדס אזרחי בירושלים", JOB3,
         call(JOBS, title=J["civil"], city=C["JLM"]))
multiple(["canonical_value", "free_text_hebrew", "gender_addressee"], "תחפשי דירה להשכרה בשכונת 'נווה שאנן' בחיפה", APT3,
         call(APT, city=C["HFA"], deal="rent", neighborhood="נווה שאנן"))
multiple(["canonical_value", "date_relative"], "מה מחיר הבנזין 95 שייקבע לנובמבר?", FUEL3,
         call(FUEL, fuel="gasoline_95", month=NEXT_MONTH))
multiple(["canonical_value", "currency_ils"], "תמיר 600 דולר לשקל", MKT3,
         call(FX, amount=600, from_currency="USD", to_currency="ILS"))
multiple(["canonical_value", "currency_ils", "mixed_direction"], "תשלם את חשבון הגז: מספר לקוח G-40912, 157 ₪", PAY3,
         call(BILL, provider="gas", account_number="G-40912", amount_ils=157))
multiple(["transliteration", "canonical_value"], "תבדוק את השער של אורמת", MKT3,
         call(STOCK, ticker=T["ORA"]))
multiple(["canonical_value"], "מחפשת משרה של מזכירה רפואית בעפולה", JOB3,
         call(JOBS, title=J["med_secretary"], city=C["AFU"]))
multiple(["canonical_value", "currency_ils", "number_format"], "יש דירות למכירה בקריית גת עד 1.3 מיליון ש״ח?", APT3,
         call(APT, city=C["KG"], deal="buy", max_price_ils=1300000))
multiple(["number_words", "number_format"], "ברוטו 13,750, נקודות זיכוי שתיים ושלושה רבעים – תחשב נטו", SAL3,
         call(NET, gross_ils=13750, credit_points=2.75))
multiple(["canonical_value"], "חפש משרות של מפתח אנדרואיד מהבית", JOB3,
         call(JOBS, title=J["android"], remote=True))
multiple(["canonical_value", "currency_ils", "number_format"], "כמה זה 2,000 ש״ח בפרנקים שוויצריים?", FX3,
         call(FX, amount=2000, from_currency="ILS", to_currency="CHF"))
multiple(["transliteration", "canonical_value"], "מה קורה עם כי״ל היום בבורסה?", MKT3,
         call(STOCK, ticker=T["ICL"]))
multiple(["currency_ils", "mixed_direction", "gender_addressee"], "תעבירי 140 שקל בביט לעומר, 053-9087766", PAY3,
         call(BIT, phone="0539087766", amount_ils=140))
multiple(["canonical_value", "date_relative"], "בכמה נמכר דיזל בחודש שעבר?", FUEL3,
         call(FUEL, fuel="diesel", month=LAST_MONTH))
multiple(["canonical_value"], "תמצא משרות לגננת בהוד השרון", JOB3,
         call(JOBS, title=J["kg_teacher"], city=C["HOD"]))

# --- parallel (25) ----------------------------------------------------------------------------
parallel(["transliteration", "canonical_value"], "מה המחיר של לאומי, הפועלים ודיסקונט?", [STOCK],
         call(STOCK, ticker=T["LUMI"]), call(STOCK, ticker=T["POLI"]), call(STOCK, ticker=T["DSCT"]))
parallel(["number_format"], "תחשב נטו ל-14,000 ול-17,000 ברוטו, בשניהם 2.25 נקודות זיכוי", [NET],
         call(NET, gross_ils=14000, credit_points=2.25), call(NET, gross_ils=17000, credit_points=2.25))
parallel(["canonical_value", "currency_ils", "number_format"],
         "דירות להשכרה בתל אביב וברמת גן, 3 חדרים לפחות, עד 7,000 ₪", [APT],
         call(APT, city=C["TA"], deal="rent", min_rooms=3, max_price_ils=7000),
         call(APT, city=C["RG"], deal="rent", min_rooms=3, max_price_ils=7000))
parallel(["canonical_value", "date_relative"], "מה מחיר הבנזין 95 והסולר החודש?", [FUEL],
         call(FUEL, fuel="gasoline_95", month=MONTH_NOW), call(FUEL, fuel="diesel", month=MONTH_NOW))
parallel(["canonical_value", "mixed_direction"], "משרות QA בתל אביב ובהרצליה", [JOBS],
         call(JOBS, title=J["qa"], city=C["TA"]), call(JOBS, title=J["qa"], city=C["HRZ"]))
parallel(["canonical_value", "currency_ils", "number_format"], "כמה זה 1,000 שקל בדולר, ביורו ובפאונד?", [FX],
         call(FX, amount=1000, from_currency="ILS", to_currency="USD"),
         call(FX, amount=1000, from_currency="ILS", to_currency="EUR"),
         call(FX, amount=1000, from_currency="ILS", to_currency="GBP"))
parallel(["canonical_value", "currency_ils", "mixed_direction"],
         "תשלם את חשבון המים, 312 ₪ (חשבון 55-60912), ואת חשבון הגז, 140 ₪ (חשבון 8812-4)", [BILL],
         call(BILL, provider="water", account_number="55-60912", amount_ils=312),
         call(BILL, provider="gas", account_number="8812-4", amount_ils=140))
parallel(["currency_ils", "mixed_direction"], "תעביר בביט 90 ש״ח לנועה 054-3328811 ו-110 ש״ח ליונתן 052-7718200", [BIT],
         call(BIT, phone="0543328811", amount_ils=90), call(BIT, phone="0527718200", amount_ils=110))
parallel(["parallel_multiple", "canonical_value", "number_format"],
         "תחפש לי דירה להשכרה בחיפה עד 4,500, ותבדוק משרות של מהנדס חומרה בחיפה", [APT, JOBS],
         call(APT, city=C["HFA"], deal="rent", max_price_ils=4500),
         call(JOBS, title=J["hw"], city=C["HFA"]))
parallel(["parallel_multiple", "number_words"],
         "כמה נטו מ-20 אלף ברוטו עם 2.75 נקודות, ומה ההחזר על משכנתא של מיליון ל-25 שנה ב-4.6%?", [NET, LOAN],
         call(NET, gross_ils=20000, credit_points=2.75),
         call(LOAN, principal_ils=1000000, annual_rate_percent=4.6, years=25))
parallel(["number_words"], "תשווה לי החזר חודשי על 700 אלף ל-15 שנה ול-25 שנה, ריבית 5% בשניהם", [LOAN],
         call(LOAN, principal_ils=700000, annual_rate_percent=5, years=15),
         call(LOAN, principal_ils=700000, annual_rate_percent=5, years=25))
parallel(["transliteration", "canonical_value"], "מה המחיר של אנבידיה, אפל ומיקרוסופט?", [STOCK],
         call(STOCK, ticker=T["NVDA"]), call(STOCK, ticker=T["AAPL"]), call(STOCK, ticker=T["MSFT"]))
parallel(["parallel_multiple", "transliteration", "canonical_value", "currency_ils", "number_format"],
         "מה שער המניה של וויקס, וכמה זה 3,000 דולר בשקלים?", [STOCK, FX],
         call(STOCK, ticker=T["WIX"]), call(FX, amount=3000, from_currency="USD", to_currency="ILS"))
parallel(["currency_ils", "number_format"], "מע״מ על 1,500 ש״ח ועל 2,750 ש״ח, שניהם לפני מע״מ", [VAT],
         call(VAT, amount_ils=1500, includes_vat=False), call(VAT, amount_ils=2750, includes_vat=False))
parallel(["canonical_value"], "כמה עלה סולר בספטמבר ובאוקטובר?", [FUEL],
         call(FUEL, fuel="diesel", month=LAST_MONTH), call(FUEL, fuel="diesel", month=MONTH_NOW))
parallel(["canonical_value"], "תמצא משרות של מפתח בקאנד ושל מפתח פרונטאנד בירושלים", [JOBS],
         call(JOBS, title=J["backend"], city=C["JLM"]), call(JOBS, title=J["frontend"], city=C["JLM"]))
parallel(["canonical_value", "half_rooms", "number_format"], "דירה למכירה בנתניה ובחדרה, 4.5 חדרים, עד 2.2 מיליון", [APT],
         call(APT, city=C["NET"], deal="buy", min_rooms=4.5, max_price_ils=2200000),
         call(APT, city=C["HAD"], deal="buy", min_rooms=4.5, max_price_ils=2200000))
parallel(["parallel_multiple", "currency_ils", "mixed_direction", "number_format"],
         "תשלם ארנונה, חשבון 3390-17, 1,045 ₪, ותעביר בביט 500 ש״ח לבעל הבית ל-050-4471239", [BILL, BIT],
         call(BILL, provider="arnona", account_number="3390-17", amount_ils=1045),
         call(BIT, phone="0504471239", amount_ils=500))
parallel(["number_format"], "תחשב נטו לי ולבעלי: אני 19,500 ברוטו עם 2.75 נקודות זיכוי, הוא 23,000 עם 2.25", [NET],
         call(NET, gross_ils=19500, credit_points=2.75), call(NET, gross_ils=23000, credit_points=2.25))
parallel(["parallel_multiple", "canonical_value", "date_relative", "currency_ils"],
         "מה המחיר של בנזין 95 החודש, וכמה זה 70 יורו בשקלים?", [FUEL, FX],
         call(FUEL, fuel="gasoline_95", month=MONTH_NOW), call(FX, amount=70, from_currency="EUR", to_currency="ILS"))
parallel(["transliteration", "canonical_value"], "מה עושות היום טבע ונובה?", [STOCK],
         call(STOCK, ticker=T["TEVA"]), call(STOCK, ticker=T["NVMI"]))
parallel(["gender_addressee", "currency_ils", "mixed_direction"],
         "תעבירי בביט 45 ש״ח לכל אחת מהן: 053-1102030 ו-058-6607080", [BIT],
         call(BIT, phone="0531102030", amount_ils=45), call(BIT, phone="0586607080", amount_ils=45))
parallel(["parallel_multiple", "canonical_value", "number_format"],
         "תחפש משרות לאחות בבאר שבע ותחשב לי נטו על 12,800 ברוטו עם 2.75 נקודות זיכוי", [JOBS, NET],
         call(JOBS, title=J["nurse"], city=C["BS"]), call(NET, gross_ils=12800, credit_points=2.75))
parallel(["canonical_value", "number_words"], "כמה זה 250 אלף ין ביורו ובדולר?", [FX],
         call(FX, amount=250000, from_currency="JPY", to_currency="EUR"),
         call(FX, amount=250000, from_currency="JPY", to_currency="USD"))
parallel(["parallel_multiple", "canonical_value", "number_words"],
         "תחפש דירה לקנות בכרמיאל עד מיליון וחצי, ותחשב החזר על משכנתא של מיליון ומאה אלף ל-20 שנה בריבית 4.75%",
         [APT, LOAN],
         call(APT, city=C["KAR"], deal="buy", max_price_ils=1500000),
         call(LOAN, principal_ils=1100000, annual_rate_percent=4.75, years=20))

# --- irrelevance (24) -------------------------------------------------------------------------
irrelevant(["near_miss"], "כמה עולה ליטר בנזין 98?", [FUEL])
irrelevant(["near_miss", "currency_ils"], "כמה זה 500 שקל ברובלים?", [FX])
irrelevant(["near_miss", "currency_ils"], "תמיר 300 דולר קנדי לשקלים", [FX])
irrelevant(["near_miss"], "תחפש לי משרד להשכרה בפתח תקווה, 80 מטר", [APT])
irrelevant(["knowledge"], "מה מדרגות מס ההכנסה בישראל השנה?", [NET])
irrelevant(["near_miss", "currency_ils"], "תעביר 2,000 ש״ח מהעו״ש שלי בלאומי לחשבון החיסכון", [BIT])
irrelevant(["near_miss", "currency_ils"], "תשלם את הוועד בית, 180 ש״ח לחודש", [BILL])
irrelevant(["near_miss"], "תחשב כמה מס רכישה אשלם על דירה ב-2.4 מיליון", [VAT])
irrelevant(["near_miss"], "מה הריבית שאני משלם היום על המשכנתא שלי?", [LOAN])
irrelevant(["near_miss"], "תגיש בשמי מועמדות למשרת המפתח בוויקס", [JOBS])
irrelevant(["near_miss"], "כמה עולה קוט״ש חשמל?", [FUEL, BILL])
irrelevant(["near_miss"], "תקנה לי 10 מניות של טבע", [STOCK])
irrelevant(["near_miss"], "תמצא לי שותף לדירה בגבעתיים", [APT])
irrelevant(["near_miss", "knowledge"], "מה שכר המינימום בישראל?", [NET])
irrelevant(["near_miss"], "תפרסם את הדירה שלי להשכרה ביד2: 3 חדרים בחולון, 5,200 לחודש", [APT])
irrelevant(["missing_info"], "תחשב לי כמה נטו נשאר לי מהמשכורת החודש", [NET])
irrelevant(["missing_info", "currency_ils"], "תעביר לדני 200 שקל בביט", [BIT])
irrelevant(["missing_info"], "כמה אני משלם כל חודש על המשכנתא שלקחנו?", [LOAN])
irrelevant(["missing_info"], "תשלם את חשבון החשמל", [BILL])
irrelevant(["missing_info"], "תחפש לי דירה 4 חדרים עד 6,000 לחודש", [APT])
irrelevant(["advice"], "כדאי לי לקנות דירה עם משכנתא או להמשיך לשכור ולהשקיע את ההון העצמי?", [APT, LOAN])
irrelevant(["advice"], "עדיף להשקיע במניות בודדות או בקרן סל על מדד ת״א 125?", [STOCK])
irrelevant(["chitchat"], "יאללה סוף סוף התקבלתי לעבודה!! אני כל כך מאושרת", [JOBS])
irrelevant(["knowledge"], "מה זה בכלל נקודות זיכוי ומי מקבל אותן?", [NET])
