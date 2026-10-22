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
