# Authoring v1 pack items

Each pack is one Python module in `scripts/packs/` that registers items with the helpers from
`scripts/build_seed.py`. Read `build_seed.py` first: it holds the 150 v0 items, and they are the style reference.

```python
from build_seed import CITY, THIS_WEEK, TODAY, TOMORROW, call, d, irrelevant, multiple, parallel, simple
```

Validate the pack on its own (it builds v0 plus your pack, runs every dataset test, and checks the counts):

```bash
cd scripts && uv run python check_pack.py pack_gov
```

## Hard rules

1. **Native Hebrew.** Write how Israelis actually type to an assistant: short, colloquial, sometimes with no
   punctuation, slang (תביא לי, תזמין, איזה, כמה עולה), abbreviations (ת״א, ב״ש, נתב״ג, ש״ח, מע״מ, בי״ס),
   and both masculine and feminine speakers. Never translate an English sentence. Never reuse a v0 question;
   every question in v1 must be unique.
2. **Exactly one correct answer.** A careful human annotator must agree with the gold without hesitating.
   - Relative dates resolve against the fixed reference: **Tuesday 20 Oct 2026, 09:00, ט׳ בחשוון תשפ״ז**.
     Use `d(n)`, `TODAY`, `TOMORROW`, `THU`, `FRI`, `SAT`, `SUN`, `MON` and `THIS_WEEK`. Don't use "next
     Tuesday" style phrases that people read in two ways.
   - Israeli dates are **DD/MM** (3/11 = 3 November).
   - Each gold argument is a **list of acceptable values**. List every spelling a reasonable API would
     accept (transliterations, "Tel Aviv"/"Tel Aviv-Yafo"). Use the `CITY` dict in `build_seed.py` for cities,
     and add a local dict in your pack for others. `None` in the list means the argument may be omitted; use
     it for optional arguments the user didn't specify, and for defaults (e.g. `passengers=[None, 1]`).
   - Free-text fields described as "exactly as the user wrote it" or "in the user's language" must appear
     verbatim in the question, ideally in quotes. Don't make a free-text gold that has to match a paraphrase.
   - Any computed value (a Hebrew date converted to Gregorian, days between dates, a sum) is computed **in
     code** in the pack (`pyluach` is available; `import datetime`), never typed by hand.
   - Enum values must be from the schema. Integers are integers (`zone=4`, not `"4"`).
3. **Tools.** Use the tool schemas in `scripts/tools.py` (52 tools). Don't edit `tools.py`; if a tool is
   missing, build the item differently.
   - `simple`: exactly 1 tool offered, 1 gold call.
   - `multiple`: exactly 3 tools offered, 1 gold call. The 2 distractors must be plausible (same domain).
   - `parallel`: 1–2 tools offered, 2–4 gold calls in one turn. Tag `parallel_multiple` when 2 different
     functions are called.
   - `irrelevance`: 1–2 tools offered, no call is correct. Mix the subtypes, tagged: `near_miss` (a tool
     that *almost* fits; at least half of your irrelevance items), `missing_info` (a required argument is
     impossible to infer, so the model must ask), `chitchat`, `knowledge`, `advice`.
4. **Tags.** Use only this vocabulary (tests enforce it):
   `canonical_value` (a Hebrew mention must become an English/ISO/enum value: the MLCL case),
   `transliteration` (Hebrew name → Latin), `free_text_hebrew` (the value must *stay* Hebrew),
   `hebrew_calendar`, `gematria`, `leap_year`, `calendar_compute`, `date_relative`, `date_ddmm`,
   `time_words` (רבע לשמונה, חצי שעה), `currency_ils`, `number_words` (מאתיים וחמישים), `number_format`
   (3,540 / 2.5K), `half_rooms` (3.5 חדרים / שלושה וחצי), `unit_local` (דונם), `gender_morphology`
   (gender inferred from inflection), `gender_addressee` (feminine imperative to the assistant), `mixed_direction`
   (LTR tokens inside RTL text), `bidi_controls`, `inference`, `parallel_multiple`, `near_miss`,
   `missing_info`, `chitchat`, `knowledge`, `advice`.
   Aim for **at least 40% of your items to carry `canonical_value` or `transliteration`**, because that
   is the benchmark's main hypothesis, and cover the Israeli phenomena that fit your domain.
5. **Safety and realism.** Fictional people, phone numbers in 050/052/053/054/058 format, plausible IDs.
   No real private individuals, and no war or security-alert scenarios.

## Your counts

| Pack | simple | multiple | parallel | irrelevance |
|---|---|---|---|---|
| pack_gov | 47 | 34 | 25 | 24 |
| pack_transport | 47 | 34 | 25 | 24 |
| pack_money | 47 | 34 | 25 | 24 |
| pack_home | 47 | 33 | 25 | 24 |
| pack_culture | 48 | 33 | 26 | 24 |

`check_pack.py` must pass (all tests green and counts exact) before you are done.
