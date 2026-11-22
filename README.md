# expense-tracker

Small offline CLI expense tracker (Software Engineering Assignment #05, KBTU).
All data in this repository is **fictional**.

## Features
- Add expenses to a local JSON file (`--file`, default `expenses.json`)
- Category normalization (`groceries` → `food`, `taxi` → `transport`, …)
- Monthly summary per category (`YYYY-MM`)
- Budgets per category and budget alerts
- Reports in `text`, `csv` or `markdown`

## Setup
```bash
python3 -m pip install --user -r requirements.txt
python3 -m pip install -e .     # optional, provides the `expense-tracker` command
```

## Usage
```bash
python3 -m expense_tracker --file /tmp/demo.json add 2026-11-01 1200 groceries --description "fictional"
python3 -m expense_tracker --file /tmp/demo.json budget food 10000
python3 -m expense_tracker --file data/sample_expenses.json summary 2026-11
python3 -m expense_tracker --file data/sample_expenses.json alerts 2026-11
python3 -m expense_tracker --file data/sample_expenses.json report 2026-11 --format markdown
```

## Checks
```bash
python3 -m pytest -q
ruff check .
mypy expense_tracker
python3 -m build
```

## Acceptance criteria
| ID | Criterion |
|---|---|
| AC1 | Adding a valid expense persists it to JSON with a normalized category; `list` shows it. |
| AC2 | `summary YYYY-MM` returns per-category totals for that month only. |
| AC3 | `alerts YYYY-MM` reports every category whose monthly spending exceeds its budget, and only those. |
| AC4 | `text`, `csv` and `markdown` reports show the same totals; `--out` uses the matching extension. |
| AC5 | Invalid input (unknown format, invalid amount, invalid month) is rejected with an error and does not modify stored data. |

AC5 was fully satisfied only after the Task 07 mitigations (see the assignment report).

## Agent instructions
See [AGENTS.md](AGENTS.md).
