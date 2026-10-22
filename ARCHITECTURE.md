# Architecture

## 1. What I inherited

### 1.1 History
Starting point tagged `inherited-baseline` (`672c7f6`). There are 8 commits, and each feature (country filter, year filter, classification) was added straight into one function.

### 1.2 What it does
`uv run raconteur` asks for an optional country and year, then reads `data.json` (375 EVAs, USA and Russia), skips incomplete records (330 remain), and:
- prints short (< 4h) / standard (4–7h) / long (≥ 7h) counts and percentages
- prints total hours and number of EVAs
- plots cumulative hours to `cumulative_duration.png`

All of it lives in one 75-line function, `main()` in `src/raconteur/__init__.py`.

### 1.3 Responsibilities in `main()`
| Lines | Does | Tag |
|---|---|---|
| 6–7 | asks for country and year | Coordinate |
| 9–10 | opens and loads `data.json` | Read |
| 14–26 | skips incomplete records, parses date and duration | Validate |
| 28–44 | filters, sorts, classifies, counts | Analyse |
| 51–58 | totals and cumulative hours | Analyse |
| 46–49, 60–72 | prints and plots | Present |

### 1.4 Mixed responsibilities
- `main()` does all five jobs.
- `classify()` is defined inside the loop (line 35), so it can't be called on its own.
- The cumulative loop (55–58) builds both a printed total and the plot data.

### 1.5 Coupling example
**`main()` in `src/raconteur/__init__.py`, positional tuple indices.** Records are `(date, hours, country)` (line 26). The filters use `record[2]` and `record[0]` (29, 31), classification appends a 4th element (39), and the counts read `r[3]` (41–43). Changing the tuple's shape breaks the filters, counts and plot at once.

### 1.6 Hard to test
- Nothing returns a value. Results are only printed or plotted.
- Input comes from `input()`. The data path `"data.json"` is hardcoded and relative.
- `plt.show()` blocks without `MPLBACKEND=Agg`.

### 1.7 Known defects (kept as-is)
- No matching records → `ZeroDivisionError` (line 47).
- A non-numeric year → `ValueError`.

### 1.8 Baseline outputs
Saved in `baseline/` (`.txt` and `.png` per run), recorded with `printf "<country>\n<year>\n" | MPLBACKEND=Agg uv run -q raconteur`.

| Run | EVAs | S / Std / L | Hours |
|---|---|---|---|
| all | 330 | 71 / 187 / 72 | 1785.03 |
| USA | 217 | 36 / 111 / 70 | 1257.13 |
| Russia | 113 | 35 / 76 / 2 | 527.90 |
| 2000 | 10 | 0 / 8 / 2 | 65.12 |
| USA 1965 | 1 | 1 / 0 / 0 | 0.6 |
| Narnia | crash | – | – |

## 2. Proposed architecture

### 2.1 Structure
```
                 __init__.py : main()
                 Coordinate (input, wiring)
                /           |            \
               v            v             v
          data.py       analysis.py     display.py
       Read + Validate    Analyse         Present
       (json, datetime)  (no imports)   (print, matplotlib)
```
Dependencies only go down from `main()`. The three modules never import each other.

### 2.2 Modules
| Module | Job | Depends on | Interface |
|---|---|---|---|
| `data.py` | Load `data.json`, skip incomplete records, parse fields | `json`, `datetime` | `Record(date, hours, country)`<br>`load_records(path) -> list[Record]` |
| `analysis.py` | All calculations, pure functions | nothing | `filter_records(records, country=None, start_year=None, end_year=None) -> list[Record]` (sorted by date)<br>`classify(hours) -> str`<br>`count_by_class(records) -> dict[str, int]`<br>`total_hours(records) -> float`<br>`cumulative_hours(records) -> (dates, hours)`<br>`compare_countries(records, a, b, start_year, end_year) -> dict` |
| `display.py` | Print and plot, no calculations | `matplotlib` | `print_summary(counts, total_hours, country, year)`<br>`plot_cumulative(dates, hours)`<br>`print_comparison(result)` |
| `__init__.py` | Ask for input, call the others in order | the three above | `main()` |

### 2.3 Why these boundaries (AR2)
Each module changes for one reason only:
- a new file format → `data.py`
- a new calculation or rule → `analysis.py`
- a new output style → `display.py`
- a new command or prompt → `main()`

### 2.4 Why each module hangs together (AR4)
- `data.py`: everything that knows the JSON field names and string formats.
- `analysis.py`: functions that take records and return values. No I/O, so each can be tested alone.
- `display.py`: everything that writes to the screen or an image.

### 2.5 How the coupling is fixed (AR3)
| Before (1.5) | After |
|---|---|
| Fields read by position: `record[2]`, `r[3]` | `Record` named tuple: `r.country`, `r.hours` |
| Classification appended as a 4th element | `classify(hours)` called when it's needed. The record shape never changes. |
| JSON field names read in the function that prints | JSON field names only appear in `data.py` |

### 2.6 Where the country comparison goes
- `analysis.compare_countries` reuses `filter_records` (with a year range) and `total_hours`. It raises `ValueError` for an unknown country or a start year after the end year.
- `display.print_comparison` formats the result.
- `main()` runs it on `uv run raconteur compare`, so the existing prompts and baseline outputs stay unchanged.

## 3. ADR-001: Split by responsibility into modules

**Context:** All logic is in one `main()` (1.3). Nothing can be tested without stdin, `data.json` and printing (1.6), and the comparison feature would mean adding a fourth job into that same function.

**Alternatives**
| Option | Rejected / chosen because |
|---|---|
| A. Keep one file, split it into functions | Rejected. It would be testable, but reading, analysis and display still share a file and its imports. |
| B. Four modules by responsibility | **Chosen** |
| C. Layered packages with classes or interfaces | Rejected. Too much structure for a 75-line program. |

**Decision:** Option B, the structure in 2.1 and 2.2.

**Rationale**
- Separates the five responsibilities from 1.3.
- The analysis functions are pure, so tests can call them directly.
- The comparison only touches `analysis`, `display` and `main()`.

**Consequences**
- ➕ Calculations can be tested and reused. The record shape is named.
- ➖ Four files instead of one.
- ➖ `python src/raconteur/__init__.py` stops working because of the package imports. The README must switch to `python -m raconteur`.

## 4. Adding the comparison

### 4.1 Modules changed
| Module | Change |
|---|---|
| `analysis.py` | added `compare_countries()` |
| `display.py` | added `print_comparison()` |
| `__init__.py` | added `compare()` and the `compare` command |
| `data.py` | **unchanged** |

That's 3 of 4 modules, and every change is an addition. No existing function was edited.

### 4.2 Code reused
- `filter_records(records, country, start_year, end_year)`, the same function the year filter uses
- `total_hours(records)`
- `load_records(path)`

### 4.3 Edge cases
| Case | Handled in | Result |
|---|---|---|
| Inclusive years | `filter_records` uses `>=` / `<=` | 2000–2000 gives 9 USA + 1 Russia, matching the 10 in the 2000 baseline |
| Country with no EVAs | `compare_countries` | count 0, total 0.00, average "unavailable" (`None`) |
| Equal totals | `compare_countries` | `leader` is `None`, printed as "Tie" |
| Start year after end year | `compare_countries` raises `ValueError` | message, no crash |
| Unknown country | `compare_countries` raises `ValueError` | message listing the known countries |
| Non-numeric year | `compare()` | message, no crash |

### 4.4 Old features
The six baseline runs still give identical output and plots.

## 5. Testing

### 5.1 Tests (`tests/test_analysis.py`)
Hand-made `Record` lists, calling `analysis` functions directly with no file reading or printing.

| Test | Checks |
|---|---|
| `test_known_answers` | A: 2 EVAs, 3.0h, avg 1.5; B: 1 EVA, 2.0h; leader A. Records one year outside the range on each side are excluded. |
| `test_no_evas_is_unavailable_and_tie` | No EVAs in range: count 0, total 0, average `None`, leader `None` (tie) |
| `test_invalid_input_raises` | Start year after end year, and an unknown country, both raise `ValueError` |
| `test_boundaries` | `classify`: 3.99 short, 4 standard, 6.99 standard, 7 long |

### 5.2 Output
```
$ uv run python -m unittest discover -s tests -v
test_boundaries (test_analysis.TestClassify.test_boundaries) ... ok
test_invalid_input_raises (test_analysis.TestCompareCountries.test_invalid_input_raises) ... ok
test_known_answers (test_analysis.TestCompareCountries.test_known_answers) ... ok
test_no_evas_is_unavailable_and_tie (test_analysis.TestCompareCountries.test_no_evas_is_unavailable_and_tie) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```
Sanity check: changing the year filter's `>=` to `>` makes `test_known_answers` fail.

### 5.3 Old features
After the restructure and again after adding the comparison, the six runs in 1.8 were re-run and diffed against `baseline/`. The printed output and the plots were identical both times.

## 6. Before vs after

| Criterion | Before (`inherited-baseline`) | After |
|---|---|---|
| Modules touched for the comparison | Would mean editing the one `main()`, mixed in with input, printing and plotting | 3 of 4 (`analysis`, `display`, `__init__`), additions only. `data.py` untouched. |
| Dependencies | `json`, `datetime` and `matplotlib` all in one function | `data`: `json`, `datetime`. `analysis`: stdlib only. `display`: `matplotlib`. They never import each other. |
| Calculations testable alone | No. Needs stdin, `data.json`, and returns nothing. | Yes. All `analysis` functions are pure, and 4 tests run with no files or printing. |
| Clarity | 75-line `main()`, fields read by position (`r[3]`) | Largest function is `compare_countries` (22 lines). Fields are named (`r.hours`). |
| Duplication | EVA count computed twice. Total hours built inside the plot loop. | Count computed once. Comparison reuses `filter_records` and `total_hours`. |
| Added complexity | 1 file, 75 lines | 4 files, 161 lines (including the new feature). Comparison results are plain dicts with no type. Direct script run (`python src/raconteur/__init__.py`) no longer works. |

## 7. ADR-002: Run the comparison as a `compare` command

**Context:** The comparison needs its own entry point. The existing summary's prompts (`country:`, `year:`) are what the baseline runs feed in, so they must not change (AR5).

**Alternatives**
| Option | Rejected / chosen because |
|---|---|
| A. Menu prompt before everything ("1 summary / 2 compare") | Rejected. It adds a prompt to the existing feature and breaks every baseline run. |
| B. Second script in `pyproject.toml` (`raconteur-compare`) | Rejected. A second entry point to install and document for one feature. |
| C. `argparse` with arguments (`compare USA Russia 1990 2000`) | Rejected. Inconsistent with the existing prompt style, and more code than needed. |
| D. `uv run raconteur compare`, checked with `sys.argv`, then prompts | **Chosen** |

**Decision:** Option D.

**Rationale**
- The existing feature's input and output are unchanged, so the baseline still matches.
- Same interaction style as the existing feature (prompts).
- Two lines in `main()`. No new dependency.

**Consequences**
- ➕ Old behaviour kept exactly. The comparison is easy to find and run.
- ➖ There's no `--help`. Unrecognised arguments are ignored and the summary runs.
- ➖ The comparison can't be scripted with arguments. Input has to be piped in, as the baseline runs do.
