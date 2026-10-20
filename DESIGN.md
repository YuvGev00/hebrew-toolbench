# Design: Hebrew ToolBench

A Hebrew analogue of the [Berkeley Function Calling Leaderboard (BFCL)](https://gorilla.cs.berkeley.edu/leaderboard.html):
single-turn tool-calling items written natively in Hebrew, scored deterministically by comparing
the predicted call's AST with gold calls.

## Why

- No public Hebrew tool-calling or agent eval set was found on Hugging Face (as of 2026-10).
- The Hebrew LLM leaderboard (MAFAT/DICTA) has no tool-use track, while DictaLM 3.0
  ([arXiv 2602.02104](https://arxiv.org/abs/2602.02104)) advertises tool calling.
- MLCL ([Luo et al., ACL 2026, arXiv 2601.05366](https://arxiv.org/abs/2601.05366)) shows that
  in Chinese, Hindi and Igbo, a dominant failure is **parameter-value language mismatch**: the model
  picks the right tool but writes the value in the user's language ("תל אביב") where the API expects
  a canonical value ("Tel Aviv"). Hebrew wasn't tested; it adds a non-Latin script, RTL text and
  a separate calendar.

## Hypotheses

- **H1 (MLCL transfer):** on items tagged `canonical_value`, a meaningful share of errors will be
  `value_language_mismatch`, more so for smaller models.
- **H2 (Israeli specifics):** accuracy on `hebrew_calendar`/`gematria`, `number_words`,
  `date_ddmm` and `gender_morphology` items will be lower than on plain `simple` items.
- **H3 (irrelevance):** Hebrew near-miss requests (a tool that *almost* fits) will cause more
  spurious calls than chit-chat does.

## Categories (as in BFCL)

| Category | Tools offered | Gold | v0 count |
|---|---|---|---|
| `simple` | 1 | exactly 1 call | 64 |
| `multiple` | 3 | 1 call to the right tool | 32 |
| `parallel` | 1–2 | 2–4 calls in one turn, any order (includes BFCL's *parallel-multiple*, tag `parallel_multiple`) | 24 |
| `irrelevance` | 1–2 | no call | 30 |

## Israeli-specific phenomena (item tags)

| Tag | Example | What it tests |
|---|---|---|
| `canonical_value` | "מזג האוויר בבאר שבע" → `city="Beer Sheva"` | MLCL language mismatch |
| `hebrew_calendar`, `gematria`, `leap_year` | "י״ד באדר ב׳ תשפ״ז" → `(5787, "Adar II", 14)` | Jewish calendar, Hebrew numerals |
| `calendar_compute` | "א׳ בכסלו תשפ״ז" → `date="2026-11-11"` | Converting the date without a tool (gold checked with `pyluach`) |
| `date_relative`, `date_ddmm` | "ב-3/11" → `2026-11-03` (DD/MM, not MM/DD) | Israeli date order, relative dates |
| `time_words` | "רבע לעשר בבוקר" → `09:45` | Spoken times |
| `currency_ils`, `number_words`, `number_format` | "שלושת אלפים וחמש מאות שקל" → `3500` | ₪/ש״ח amounts, gendered number words |
| `gender_morphology` | "אני מתעניינת…" → `gender="female"` | Inferring gender from verb/adjective inflection, using unisex names (טל, שחר, עדי) |
| `gender_addressee` | "קבעי לי…" | Feminine imperative addressed *to* the assistant must not leak into arguments |
| `transliteration` | "צחי בן חמו" → `"Tzachi Ben Hamo"` | Hebrew→Latin entity names (gold lists accepted spellings) |
| `mixed_direction`, `bidi_controls` | "מספר: LX998877665IL", RLM-wrapped IDs | Extracting LTR tokens from RTL text |
| `free_text_hebrew` | `title="סקירה רבעונית"` | The reverse of MLCL: free-text fields must stay in Hebrew |
| `near_miss`, `missing_info` | °C→°F with a currency tool | Irrelevance subtypes |

Every item carries a fixed system prompt that gives the reference date (Tuesday, 20 Oct 2026 /
ט׳ בחשוון תשפ״ז), so relative dates have exactly one answer.

## Item format (JSONL)

```json
{"id": "simple_001", "category": "simple", "tags": ["canonical_value", "date_relative"],
 "system": "התאריך היום: …", "question": "מה מזג האוויר מחר בתל אביב?",
 "functions": [{"name": "get_weather", "parameters": {…JSON Schema…}}],
 "gold": [{"name": "get_weather", "arguments": {"city": ["Tel Aviv", "Tel Aviv-Yafo"], "date": ["2026-10-21"]}}],
 "review": "pending"}
```

Each gold argument is a list of acceptable values, as in BFCL's `possible_answer`. `null` means
the argument may be omitted. Items are generated from `scripts/build_seed.py`, so each tool schema
is defined once, in `scripts/tools.py`.

## Scoring (deterministic, no LLM judge)

An item is correct iff the predicted calls match the gold calls exactly (for `parallel`, under
some one-to-one pairing). Per call:

1. **Function name** must match. A name that isn't among the offered tools → `wrong_function`.
2. **Argument names**: an argument not in the schema, or not in the gold (unless it equals the
   schema `default`), → `unexpected_arg`. A gold argument without `null` that is missing → `missing_arg`.
3. **Values** are compared via `canonical(value, schema)`:
   - `integer`/`number`: must be JSON numbers (`"150"` → `type_mismatch`); `5 == 5.0`; rounded to 6 dp.
   - `format: date` → strict ISO `YYYY-MM-DD`; `time` → `HH:MM`; `date-time` → ISO, wall clock.
   - `x-normalize: phone` → digits only, `+972` → `0`. (`x-*` keys are stripped before sending.)
   - strings: NFC, bidi controls and niqqud removed, ״/׳ folded to `"`/`'`, case-folded,
     whitespace collapsed, edge punctuation trimmed.
   - arrays: order-insensitive multiset; objects: recursive.
4. **Error taxonomy.** Each failure gets exactly one label. If the predicted value contains Hebrew
   letters and no acceptable value does, it's `value_language_mismatch` (the MLCL failure); if not,
   it's `type_mismatch` or `value_mismatch`. Other labels: `no_call`, `called_when_irrelevant`,
   `wrong_call_count` and `invalid_json`.

Raw model outputs are cached in `results/raw/*.jsonl` before scoring, so a scorer change can be
applied again without spending API quota.

## Known limitations of v0

- **Single author.** The items have not yet had an independent native-speaker review
  (`review: pending`). A transliteration gold that lists too few spellings causes false negatives;
  those items are tagged so they can be reported apart.
- **150 items:** about ±8 pp 95% CI on overall accuracy, and wider for each tag.
- **Single-turn only.** There are no multi-turn, executable or state-based checks (BFCL v3/v4 have them).
- **Free-tier models only.** Provider-side tool-call parsing differs, and the benchmark measures
  model and serving stack together.

## Plan to reach about 800 items (v1)

1. **Native review of v0** by the author: fix gold, set `review: native_verified`, and log every
   change in DECISIONS.md.
2. **Add tools:** grow from 24 to about 60 Israeli-domain tools (Gov.il services, Rav-Kav, Waze,
   Wolt, banks, HMOs, IDF reserve forms, municipal services).
3. **Grow each category toward BFCL's mix:** simple 300, multiple 200, parallel 150 and
   irrelevance 150, all native Hebrew. Use templated *variation* (city, amount, date) only for
   canonical-value items, capped at 30% of the set. Every item gets a human pass.
4. **Second annotator:** a second native speaker labels a 100-item sample. Report agreement
   on the gold.
5. **Contrast set:** an English twin of each `canonical_value` item, to measure the Hebrew vs
   English gap directly (MLCL's main comparison).
6. **Models:** DictaLM 3.0 through a free HF Inference endpoint or locally. Also add a
   prompt-level mitigation baseline ("use canonical English values"), as MLCL does.
