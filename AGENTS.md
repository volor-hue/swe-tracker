# AGENTS.md — expense-tracker

> Instructions for AI coding agents (and humans) working in this repository.
> Disclosure: the assistant used for Assignment #05 (Grok Bot v4.7) does not load this
> file automatically. Its relevant sections were pasted explicitly into the AI context
> before every review or change request.

## Purpose
Small, offline CLI expense tracker for coursework. It records expenses in a local JSON
file, normalizes categories, prints monthly summaries, budget alerts and reports
(text / csv / markdown). **Fictional data only**: no real personal or financial data.

## Architecture
| Path | Responsibility |
|---|---|
| `expense_tracker/models.py` | `Expense` dataclass, dict (de)serialization |
| `expense_tracker/categories.py` | category alias normalization |
| `expense_tracker/storage.py` | load/save JSON (`{"expenses": [...], "budgets": {...}}`) |
| `expense_tracker/tracker.py` | business rules: add, budget, monthly summary, alerts |
| `expense_tracker/report.py` | report formatting (Strategy registry after Task 03) |
| `expense_tracker/cli.py` | argparse CLI only; no business logic |
| `tests/` | pytest suite (acceptance criteria AC1–AC5 + regression tests) |
| `data/sample_expenses.json` | fictional sample data |

## Setup
```bash
python3 -m pip install --user -r requirements.txt   # pinned dev tools
python3 -m pip install -e .                          # optional editable install
```

## Safe commands (allowed without asking)
- `python3 -m pytest -q`
- `ruff check .`
- `mypy expense_tracker`
- `python3 -m build` (writes only to `dist/`, which is git-ignored)
- `python3 -m expense_tracker --file /tmp/<scratch>.json ...` (scratch files only)
- `git status`, `git diff`, `git log`, creating commits on a feature branch

## Coding conventions
- Python ≥ 3.10, type hints on public functions, `ruff` clean, `mypy` clean.
- Business logic stays in `tracker.py`/`report.py`; `cli.py` only parses and prints.
- Money is `float`, rounded to 2 decimals for output; amounts must be finite and > 0.
- Months are strings `YYYY-MM`; dates are `YYYY-MM-DD`.
- Small, focused commits; one concern per commit.

## Test expectations
- Every behavior change needs a test; every bug fix needs a regression test that fails
  before the fix and passes after it.
- Acceptance criteria AC1–AC5 (see README) must stay green.
- Run the full check set before proposing a merge: pytest, ruff, mypy, build.
- Never claim a check passed unless its output was actually produced in this session.

## Forbidden actions
- No secrets, tokens, API keys, `.env` files or real personal/financial data in the repo.
- No production deployments, publishing to PyPI or pushing tags/releases.
- No destructive commands: `rm -rf` outside `/tmp`, `git push --force`, `git reset --hard`
  on shared branches, rewriting history, deleting `data/` or tests.
- No unreviewed dependency changes: do not add/upgrade/remove packages in
  `pyproject.toml` or `requirements.txt` without explicit human approval.
- No network calls from the application code.
- Do not weaken, skip or delete tests to make a check pass.

## Review gates
1. Agent works on a feature branch, never directly on `main`.
2. Agent provides: change summary, diff, pytest/ruff/mypy/build output, risk notes.
3. A human (owner: Lashbayev Nurbek) reviews the diff and re-runs the checks.
4. Only the human merges. Dependency or storage-format changes need explicit approval.
