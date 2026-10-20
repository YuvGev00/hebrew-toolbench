# Hebrew ToolBench

A Hebrew tool-calling benchmark, modelled on [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html).
The items are written natively in Hebrew and scored by a deterministic AST scorer, with no LLM judge.

## Results: seed set v0 (150 items, 2026-10-20)

Accuracy in %. All models run on $0 free tiers, at temperature 0.

| Model | Overall | simple (64) | multiple (32) | parallel (24) | irrelevance (30) | canonical-value slice (44) | value-language-mismatch errors |
|---|---|---|---|---|---|---|---|
| `gemini-3.5-flash-lite` | **90.7** | 92.2 | 96.9 | 91.7 | 80.0 | 95.5 | 3 |
| `gemma-4-31b-it` | **90.7** | 89.1 | 93.8 | 87.5 | 93.3 | 90.9 | 2 |
| `minimax-m3.1-flash:free` | **72.0** | 73.4 | 78.1 | 87.5 | 50.0 | 77.3 | 0 |

With n=150 the 95% CI is about ±5 pp at 90% accuracy and ±7 pp at 72%, so the two leaders are tied.
Full error and tag breakdowns are in [`results/summary.md`](results/summary.md).

What v0 shows so far:

- **MLCL's failure mode shows up in Hebrew, but rarely.** 5 of the 12 value-level errors made
  by the two leading models are Hebrew values sent where the API expects Latin script:
  `name='צחי בן חמו'`, `city='ראש העין'`. Most are on *person names*, not cities.
- **Hebrew-calendar reasoning is the weak spot.** Errors include ה׳ באייר read as Nisan, the wrong
  year for "ט״ו באב הקרוב", and א׳ בכסלו תשפ״ז converted one day off.
- **Irrelevance separates the models.** Near-miss requests (Bitcoin with a currency tool,
  Japanese with an enum that has no `ja`, sunset time with a Shabbat-times tool) lead to spurious
  calls. Minimax calls a tool on half the irrelevance items, and often calls the same tool twice.
- `gemma-4-31b-it` on the Gemini API sometimes answers translation requests itself, with
  `<thought>` text, instead of calling the tool. This is scored as `no_call` (see DECISIONS D14).

## What's in v0

- `data/seed_v0.jsonl`: 150 items (64 simple, 32 multiple, 24 parallel, 30 irrelevance) using
  24 Israeli-domain tools. Tags cover the Jewish calendar and gematria, ₪ amounts and Hebrew number
  words, DD/MM dates, gendered morphology, Hebrew↔Latin names, mixed-direction/RTL strings, and
  canonical-value parameters. Items are generated from [`scripts/build_seed.py`](scripts/build_seed.py).
- `src/hebrew_toolbench/scorer.py`: an AST scorer that checks the function name and the argument
  names, and compares values after schema-driven normalisation (ISO dates and times, numbers,
  Israeli phone numbers, Hebrew string folding). Each failure gets one label, including
  `value_language_mismatch`.
- `src/hebrew_toolbench/runner.py`: a runner for any OpenAI-compatible endpoint. It caches raw
  outputs, so re-scoring costs nothing.
- [DESIGN.md](DESIGN.md) covers the categories, scoring rules, hypotheses and the plan to reach
  about 800 items. [DECISIONS.md](DECISIONS.md) logs the decisions and why each was made.

## Usage

```bash
uv sync
uv run pytest -q
```

To query a model, set `TAINTWALL_BASE_URL` and `TAINTWALL_API_KEY`, or pass a file that defines them:

```bash
uv run hebrew-toolbench run --model models/gemini-3.5-flash-lite --env-file path/to/.env.gemini --rpm 12
```

The run resumes from cache. To score every cached model:

```bash
uv run hebrew-toolbench report
```

## Status

The items were written by a single author and haven't had an independent native-speaker review
yet (`"review": "pending"` on every item). Treat the numbers as preliminary.
