# Decisions log

Newest last. Each entry: the decision, the alternatives, and why.

### D1 — Write items natively in Hebrew; don't translate BFCL (2026-10-20)
BFCL's code and data are Apache-2.0 (checked on the `gorilla-llm/Berkeley-Function-Calling-Leaderboard`
dataset card and the gorilla repo's LICENSE), so translation would be legal with attribution.
I rejected it anyway: translated items carry US-centric entities (cities, currencies, dates in
MM/DD) and translationese, which hides exactly the Israeli phenomena this benchmark targets.
Only BFCL's *design* (categories, the AST scorer, the acceptable-values gold format) is reused.
No BFCL text is copied.

### D2 — Deterministic AST scorer, no LLM judge
It is reproducible, free, and holds up in an interview. The cost is that free-text arguments need
the exact text, so items quote free text verbatim ("עם הכותרת 'סקירה רבעונית'"). Paraphrase-tolerant
judging is out of scope.

### D3 — Strict JSON types (`"150"` is not `150`)
BFCL type-checks too. A string number is a real integration bug: many APIs reject it. Strict
types keep `type_mismatch` separate from `value_mismatch`.

### D4 — A separate `value_language_mismatch` label
This makes the MLCL hypothesis directly measurable. The rule is deterministic: the predicted value
contains Hebrew letters and no acceptable value does. It's applied only on failure, so a Hebrew
`free_text_hebrew` value never counts against the model.

### D5 — Strict ISO dates
`format: date` accepts only `YYYY-MM-DD`, not `20/10/2026`. Real APIs that state the format reject
the other forms, and accepting DD/MM would hide the DD/MM vs MM/DD confusion the `date_ddmm` items test.

### D6 — Arrays compare order-insensitively
Every array in v0 is a set (attendees). If an ordered array is needed later, add an `x-ordered`
schema flag.

### D7 — A fixed reference date in the system prompt
Relative dates ("מחר", "ביום חמישי") need a "today". A fixed date (Tue 2026-10-20) keeps the gold
stable forever. The Hebrew date given (ט׳ בחשוון תשפ״ז) was checked with `pyluach`.

### D8 — Generate the seed set from a Python builder
Tool schemas are defined once (`scripts/tools.py`), relative dates are computed instead of typed
by hand, and CI fails if `data/seed_v0.jsonl` drifts from the builder. The JSONL stays
self-contained (each item embeds its schemas), as BFCL's does.

### D9 — Commit raw outputs; scoring is offline
Free-tier quota is scarce, so `results/raw/*.jsonl` holds what each model returned, and the
scorer can be re-run against it. This makes the results table auditable.

### D10 — Use stdlib `urllib` instead of the `openai` SDK
One endpoint (`/chat/completions`) doesn't justify a dependency. Configuration comes from
`TAINTWALL_BASE_URL` and `TAINTWALL_API_KEY` (shared with the taintwall project), optionally
loaded with `--env-file`. Keys are never printed.

### D11 — Models: $0 only
Two models via the Gemini API free tier (`gemini-3.5-flash-lite`, `gemma-4-31b-it`) and one via
OpenRouter `:free` (`minimax-m3.1-flash`). `nvidia/nemotron-3-super-120b-a12b:free` returned a
provider 404 for every request, so it was dropped. Temperature is 0 and `tool_choice` is `auto`,
with no extra system instructions beyond the date.

### D12 — `pyluach` (MIT) as a dev dependency only
It's used in tests to check that every Hebrew-calendar gold exists (Adar I/II only in leap years,
day within month length) and that `calendar_compute` golds are correct. It isn't a runtime dependency.

### D13 — Gold audit after the first run (2026-10-20)
A gold value may be widened after seeing model outputs only when the model's value is correct
by an external standard, never because a model produced it. One change so far: `Kfar Saba` now
also accepts `Kefar Sava` (the official CBS and road-sign spelling) and `Kfar Sava`. Rejected:
`asian` for "סושי". `japanese` is the most specific enum value, so that answer stays wrong.

### D14 — Gemma's `<thought>` output and answering instead of calling a tool count as failures
On the Gemini API, `gemma-4-31b-it` sometimes returns its reasoning as `<thought>…</thought>` in
`content` and answers translation requests itself, without calling `translate_text`.
BFCL also scores a missing call as wrong. This is kept as `no_call`, not special-cased.

### D15 — Accept an RFC 3339 full-time where the schema says `format: time` (2026-10-22)
JSON Schema's `format: time` means an RFC 3339 *full-time* (`08:00:00Z`), not `HH:MM`. GLM, Qwen and
DeepSeek (through OpenRouter) followed the standard and sent seconds plus an offset. They were scored
`type_mismatch` until the gap showed up as 74 GLM errors concentrated on `time_words`. The scorer
now accepts a full-time on the minute and compares the wall clock, as D5's date-time rule already did.
Non-zero seconds or fractions (GLM sometimes emitted `09:45:00.0123…-09:45`) stay a type mismatch.
Effect on overall accuracy: GLM 82.4 → 90.1, DeepSeek 87.4 → 90.1, Qwen 82.4 → 85.9; no other model changed.

### D16 — v1 items were drafted by an LLM, then checked three ways (2026-10-22)
The 650 v1 items were drafted by Claude (five agents, one per domain pack) under the written rules in
`scripts/packs/AUTHORING.md`. They were not written by a human. Checks:
1. **Automatic** (`tests/test_dataset.py`): gold well-formed against each schema; gold scores itself
   correct; Hebrew dates exist (pyluach); Hebrew questions; unique questions; fixed tag vocabulary;
   exact category counts; v0 kept byte-identical inside v1.
2. **Manual** review of a random 30-item sample and of every item an agent flagged as uncertain. Fixes:
   list items keep an optional leading ו; a candle-lighting event on כ״ה בכסלו accepts both Gregorian
   dates; an internet bill accepts `bezeq`.
3. **Adjudication** (`scripts/adjudicate.py`): any item that both strong models (Claude Sonnet 5.5 and
   Gemini 3.5 Flash) failed was reviewed by hand. Of 19, 8 were fixed because the models' behaviour
   was reasonable: two calendar items offered a lookup tool that makes a valid first step, and six
   no-call items had a defensible call (default credit points, a derivable zman, a computable area,
   quotes before advice). The other 11 were kept: the gold is right and the items are hard.
Every item still has `review: pending`; a native-speaker pass by the maintainer is the next step.
Known bias: the drafting model is the same family as two evaluated models (Claude Sonnet and Haiku).

### D17 — Models for v1: paid tiers allowed, a few dollars in total (2026-10-22)
The user approved paid runs, so D11's $0 rule no longer limits the model list. Nine models were run:
Claude Sonnet 5.5 and Haiku 5.5 (Anthropic's OpenAI-compatible endpoint, no temperature, because these
models reject it), Gemini 3.5 Flash and Flash-Lite, Gemma 4 31B (Gemini API), Qwen 3.8 27B,
DeepSeek V4.1 Flash and GLM 5.3 (OpenRouter, paid), and Minimax M3.1 Flash (OpenRouter `:free`).
Estimated total cost is about $5-7. `nvidia/nemotron-3-ultra-550b-a55b:free` was dropped after 44 items
(about 2 requests a minute, and it would have used up the free daily quota); its partial outputs are
kept in `results/excluded/`. DictaLM 3.0 is not offered by any API provider we found, so it is not
evaluated.

### Open
- Licence: decided 2026-10-22. MIT for code (matching the author's other repos), CC BY 4.0 for data.
- Public repo and HF dataset: being prepared (2026-10-22).
