---
license: cc-by-4.0
language:
  - he
pretty_name: Hebrew ToolBench
size_categories:
  - n<1K
task_categories:
  - text-generation
tags:
  - function-calling
  - tool-use
  - benchmark
  - hebrew
  - israel
  - evaluation
configs:
  - config_name: default
    data_files:
      - split: test
        path: data/test.jsonl
---

# Hebrew ToolBench

A Hebrew tool-calling benchmark, modelled on [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html):
**800 single-turn items in Hebrew, 52 Israeli-domain tools, and a deterministic AST scorer** (no LLM judge).

It tests what generic benchmarks miss:
- Hebrew mentions that an API needs in English or as an enum ("באר שבע" → `Beer Sheva`);
- the Jewish calendar and gematria;
- ₪ amounts written in words;
- DD/MM dates and spoken times;
- gendered inflection;
- right-to-left text with embedded IDs.

Code, scorer and raw model outputs: **[github.com/YuvGev00/hebrew-toolbench](https://github.com/YuvGev00/hebrew-toolbench)**

## Quick start

```python
import json
from datasets import load_dataset

ds = load_dataset("YuvGev/hebrew-toolbench", split="test")
item = ds[0]
functions = json.loads(item["functions"])  # tool schemas to offer the model
gold = json.loads(item["gold"])            # expected call(s), with every acceptable value
print(item["question"])
```

To score a model, use the AST scorer in the GitHub repo (`uv run hebrew-toolbench run` and `report`). It
handles the acceptable-value lists, defaults and order-free parallel calls.

## Fields

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Item id, e.g. `simple_001` |
| `category` | string | `simple` (300), `multiple` (200, pick 1 of 3 tools), `parallel` (150, 2–4 calls), `irrelevance` (150, no call is right) |
| `tags` | list of strings | What the item tests, e.g. `canonical_value`, `hebrew_calendar`, `currency_ils`, `date_ddmm`, `time_words`, `mixed_direction` |
| `system` | string | System prompt. Every item is anchored to Tuesday 20 Oct 2026, 09:00 (ט׳ בחשוון תשפ״ז), so relative dates have one answer |
| `question` | string | The user's request, in Hebrew |
| `functions` | JSON string | Tool schemas (OpenAI function format) |
| `gold` | JSON string | Expected calls. Each argument lists every acceptable value; `[]` means no call is correct |
| `source` | string | `v0` (the first 150 items) or the domain pack the item came from |
| `review` | string | Native-speaker review status (currently `pending` for every item) |

## Results (v1, 2026-10-22)

Accuracy in %, with a 95% Wilson interval. Single turn, `tool_choice: auto`.

| Model | Overall | 95% CI | simple | multiple | parallel | irrelevance |
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

† The items were drafted by Claude (see below), so the two Claude models may have a home advantage.

**Main findings:**
- **The Hebrew calendar is the hardest part for every model.** Converting a Hebrew date such as
  י״ט בכסלו to a Gregorian date drops most models far below their plain `simple` score.
- **Near-miss requests cause spurious calls.** An offered tool that *almost* fits (98 octane with a tool
  that only knows 95) brings models down to 59–89%.
- **Writing values in Hebrew where the API expects English** appears mainly in the smallest model:
  19 of Gemini Flash-Lite's 71 errors on canonical-value items.

## How the items were made, and limitations

- **Drafting:** 650 of the 800 items were drafted by an LLM (Claude) under written authoring rules: native
  colloquial Hebrew, exactly one correct answer, computed golds. They are not translations.
- **Automatic checks:** 2,454 tests in CI. Every gold is valid against its schema, every Hebrew date exists
  (computed with `pyluach`), and questions are unique.
- **Adjudication:** every item that both strong models failed (19) was reviewed by hand; 8 were fixed.
- **Native review is pending:** no independent native speaker has signed off yet. Treat v1 as a preview.
- **Single turn only:** there are no multi-turn or executable checks.

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code (in the GitHub repo): MIT.

## Citation

```bibtex
@misc{geva2026hebrewtoolbench,
  title  = {Hebrew ToolBench: a Hebrew tool-calling benchmark},
  author = {Geva, Yuval},
  year   = {2026},
  url    = {https://github.com/YuvGev00/hebrew-toolbench}
}
```
