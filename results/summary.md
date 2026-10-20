| Model | N | Overall | simple (64) | multiple (32) | parallel (24) | irrelevance (30) | canonical_value (44) | lang-mismatch errors |
|---|---|---|---|---|---|---|---|---|
| `gemini-3.5-flash-lite` | 150 | 90.7 | 92.2 | 96.9 | 91.7 | 80.0 | 95.5 | 3 |
| `gemma-4-31b-it` | 150 | 90.7 | 89.1 | 93.8 | 87.5 | 93.3 | 90.9 | 2 |
| `minimax/minimax-m3.1-flash:free` | 150 | 72.0 | 73.4 | 78.1 | 87.5 | 50.0 | 77.3 | 0 | 

| Error type | `gemini-3.5-flash-lite` | `gemma-4-31b-it` | `minimax/minimax-m3.1-flash:free` |
|---|---|---|---|
| invalid_json | 0 | 0 | 1 |
| called_when_irrelevant | 6 | 2 | 15 |
| no_call | 0 | 5 | 0 |
| wrong_call_count | 2 | 1 | 13 |
| wrong_function | 0 | 0 | 1 |
| value_language_mismatch | 3 | 2 | 0 |
| value_mismatch | 3 | 4 | 12 | 

| Tag | N | `gemini-3.5-flash-lite` | `gemma-4-31b-it` | `minimax/minimax-m3.1-flash:free` |
|---|---|---|---|---|
| canonical_value | 44 | 95.5 | 90.9 | 77.3 |
| hebrew_calendar | 24 | 91.7 | 87.5 | 62.5 |
| currency_ils | 22 | 100.0 | 100.0 | 86.4 |
| mixed_direction | 19 | 100.0 | 100.0 | 78.9 |
| date_relative | 18 | 100.0 | 100.0 | 55.6 |
| free_text_hebrew | 18 | 94.4 | 72.2 | 77.8 |
| near_miss | 17 | 76.5 | 94.1 | 52.9 |
| transliteration | 15 | 86.7 | 80.0 | 66.7 |
| gematria | 11 | 90.9 | 90.9 | 63.6 |
| gender_morphology | 10 | 70.0 | 80.0 | 100.0 |
| number_words | 9 | 100.0 | 100.0 | 77.8 |
| time_words | 8 | 100.0 | 100.0 | 62.5 |
| date_ddmm | 7 | 100.0 | 100.0 | 100.0 |
| number_format | 7 | 100.0 | 100.0 | 100.0 |
| parallel_multiple | 7 | 100.0 | 100.0 | 71.4 |
| knowledge | 6 | 100.0 | 83.3 | 33.3 |
