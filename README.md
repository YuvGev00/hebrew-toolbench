# Hebrew ToolBench

A Hebrew tool-calling benchmark, modelled on [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html):
**800 single-turn items in Hebrew, 52 Israeli-domain tools, and a deterministic AST scorer** (no LLM judge).
It tests what generic benchmarks miss: Hebrew mentions that an API needs in English or as an enum
("באר שבע" → `Beer Sheva`), the Jewish calendar, gematria, ₪ amounts in words, DD/MM dates, spoken
times, gendered inflection, and right-to-left text with embedded IDs.

## Results (v1, 800 items, 2026-10-22)

Accuracy in %, with a 95% Wilson interval on the overall score. Single turn, `tool_choice: auto`.

| Model | Overall | 95% CI | simple (300) | multiple (200) | parallel (150) | irrelevance (150) |
|---|---|---|---|---|---|---|
| `claude-sonnet-5-5` † | **95.8** | 94.1–96.9 | 96.3 | 98.5 | 95.3 | 91.3 |
| `gemini-3.5-flash` | **93.4** | 91.4–94.9 | 96.7 | 97.5 | 95.3 | 79.3 |
| `claude-haiku-5-5` † | 92.5 | 90.5–94.1 | 93.7 | 95.0 | 90.0 | 89.3 |
| `gemma-4-31b-it` | 90.6 | 88.4–92.5 | 89.3 | 91.5 | 91.3 | 91.3 |
| `deepseek-v4.1-flash` | 90.1 | 87.9–92.0 | 92.7 | 91.0 | 90.7 | 83.3 |
| `glm-5.3` | 90.1 | 87.9–92.0 | 91.0 | 89.0 | 90.0 | 90.0 |
| `qwen3.8-27b` | 85.9 | 83.3–88.1 | 84.3 | 85.5 | 85.3 | 90.0 |
| `gemini-3.5-flash-lite` | 81.8 | 78.9–84.3 | 85.0 | 90.0 | 82.0 | 64.0 |
| `minimax-m3.1-flash:free` | 59.9 | 56.4–63.2 | 61.3 | 65.5 | 70.7 | 38.7 |

† The v1 items were drafted by Claude (see [How the items were made](#how-the-items-were-made)), so the two
Claude models may have a home advantage. Their rank should be read with that in mind.

Error and per-tag tables for every model are in [`results/summary.md`](results/summary.md). Raw model
outputs are committed in `results/raw/`, and `uv run hebrew-toolbench report` re-scores them offline.

### What the results show

- **The Hebrew calendar is the hardest part for every model.** On `calendar_compute` items, where a
  Hebrew date such as י״ט בכסלו must become a Gregorian date with no tool to help, accuracy falls far
  below each model's plain `simple` items: Gemma 55.6 vs 90.5, Qwen 38.9 vs 88.1, Gemini Flash-Lite
  50.0 vs 82.7. Only Claude Sonnet (94.4) holds up.
- **Near-miss requests cause spurious calls; small talk doesn't.** Every model scores about 100% on
  chit-chat, but 59–89% on `near_miss` items (Minimax: 28%), where an offered tool *almost* fits (98 octane with a tool
  that knows only 95; Tu B'Av with a holiday list that has only Tisha B'Av). Gemini 3.5 Flash is the
  clearest case: 97.5% on `multiple`, but 70.1% on near-misses.
- **The MLCL failure exists in Hebrew, but only in the smaller model.** MLCL ([Luo et al., 2026](https://arxiv.org/abs/2601.05366))
  found that models write parameter values in the user's language where the API expects a canonical
  English value. Here that is **19 of Gemini Flash-Lite's 71 errors** on canonical-value items
  (`city="ראש העין"`). Every other model makes 0–2 such errors, so the effect is real but confined to the
  small end of this lineup.
- **Format strictness separates providers, not just models.** JSON Schema's `format: time` means
  `08:00:00Z`, and three models served through OpenRouter follow it. The scorer accepts that form (see
  [DECISIONS D15](DECISIONS.md)); before that fix it would have cost GLM 8 points.

## What's in v1

| | |
|---|---|
| Items | 800: 300 simple, 200 multiple (pick 1 of 3 tools), 150 parallel (2–4 calls), 150 irrelevance (no call is right) |
| Tools | 52 Israeli-domain tools, e.g. Gov.il appointments, Bituach Leumi, Rav-Kav, Waze, Pango, Yad2, net salary, Wolt, Ontopo, zmanim, Mifal HaPais |
| Tags | 490 items test the Hebrew→canonical mapping (`canonical_value` / `transliteration`); 86 `hebrew_calendar`, 80 `currency_ils`, 67 `date_ddmm`, 56 `time_words`, 51 `mixed_direction`, … |
| Gold | Each argument lists every acceptable value (spellings, defaults); every calendar gold is computed with `pyluach` |
| Reference date | Every item is anchored to Tuesday 20 Oct 2026, 09:00 (ט׳ בחשוון תשפ״ז), so relative dates have one answer |

`data/v1.jsonl` is the benchmark. `data/seed_v0.jsonl` (the first 150 items, unchanged inside v1) is kept for
reproducibility. [DESIGN.md](DESIGN.md) covers the categories, the scoring rules and the hypotheses;
[DECISIONS.md](DECISIONS.md) logs every decision.

## How the items were made

Honesty about provenance matters for a benchmark, so here it is in full:

1. **Drafting.** The 650 new items were drafted by an LLM (Claude), split into five domain packs, under
   written rules ([`scripts/packs/AUTHORING.md`](scripts/packs/AUTHORING.md)): native colloquial Hebrew,
   exactly one correct answer, computed golds, and a fixed tag vocabulary. They are not translations.
2. **Automatic checks** (2,454 tests, in CI): every gold is valid against its schema and scores itself
   correct, every Hebrew date exists, questions are unique, and the category counts are exact.
3. **Adjudication.** Every item that both strong models (Claude Sonnet 5.5 and Gemini 3.5 Flash)
   failed was reviewed by hand: 19 items. 8 were fixed, because the models' behaviour was reasonable;
   11 were kept, because the gold is right and the item is hard ([`results/adjudication.md`](results/adjudication.md)).
4. **Native review: pending.** No independent native speaker has signed off yet; every item says
   `"review": "pending"`. Treat v1 as a preview until that pass is done.

## Usage

```bash
uv sync
uv run pytest -q
```

Run a model on any OpenAI-compatible endpoint (resumes from cache):

```bash
uv run hebrew-toolbench run --model <model-id> --env-file path/to/.env --rpm 30
```

The env file sets `TAINTWALL_BASE_URL` and `TAINTWALL_API_KEY`. For Claude 5.5 models, add
`--no-temperature`, because they reject the parameter. To score every cached model:

```bash
uv run hebrew-toolbench report
```

## Limitations

- **Single turn.** There are no multi-turn, executable or state-based checks, which BFCL v3/v4 have.
- **LLM-drafted items**, with a native review still pending (above), and a possible home advantage for Claude.
- **Serving stack included.** Each score measures a model *and* the provider's tool-call parsing.
- **DictaLM 3.0 is missing.** No API provider we found serves it.

## License

Code: [MIT](LICENSE). Data (`data/*.jsonl`): [CC BY 4.0](LICENSE-DATA).
