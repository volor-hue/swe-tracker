# Task 04 — Read-only AI risk review (raw record)

- Tool: Grok Bot v4.7 (acting as the reviewer). Date: 22 Nov 2026 (Asia/Almaty).
- Reviewed revision: `b9464e1` (after the Strategy refactor, before mitigations).
- Mode: read-only. The reviewer was told not to modify files; `git status` was clean before and after the review.

## Prompt (verbatim)

```
You are a READ-ONLY code reviewer. Do not modify, create or delete any file and do not
run commands that write to the repository.
Context pasted explicitly (the tool does not auto-load AGENTS.md):
  - AGENTS.md (full text), README.md
  - repository tree (git ls-files) and all files in expense_tracker/ and tests/
  - requirements.txt, pyproject.toml
  - baseline outputs: pytest (3 passed), ruff (2 errors), mypy (1 error), build (ok), pip-audit (no known vulns)
Task: propose candidate risks across these categories: correctness, maintainability,
security, dependency, agent operations. For each candidate give: ID, category, claim,
file:line, a command or test that would confirm or refute it, and your confidence.
Do not claim anything was executed unless the output is in the context.
```

## Raw output (verbatim, before human verification)

```
F1  correctness  add_expense() converts amount with float(amount) and never checks it
    (tracker.py:10, models.py:16). Negative, zero, "nan" and "inf" are accepted. NaN makes
    `spent > limit` False (tracker.py:39), so budget alerts are silently suppressed.
    Verify: add -5000 and nan, then run `alerts`. Confidence: high.
F2  correctness  monthly_summary() uses e.date.startswith(month) (tracker.py:25). Month
    "2026-1" matches 2026-10 and 2026-11. Verify: `summary 2026-1` on sample data. High.
F3  correctness  storage.load_data() calls json.load without error handling (storage.py:13);
    a corrupt file crashes with a traceback. Verify: write '{broken' and run `list`. High.
F4  correctness  save_data() truncates the file with open(path,"w") before writing
    (storage.py:21); a crash mid-write could lose all data. Verify: fault injection. Medium.
F5  maintainability  ruff reports an unused import (tracker.py:1) and unused variable
    (cli.py:15); mypy reports an Optional return (tracker.py:31). Verify: ruff, mypy. High.
F6  dependency  requirements.txt lists pytest, ruff, mypy without versions; builds are not
    reproducible and tool upgrades may change results. Verify: cat requirements.txt. High.
F7  security  CSV export is vulnerable to formula injection: a description such as
    =HYPERLINK(...) is written into the CSV report. Verify: add such an expense and export
    csv. Medium.
F8  security  --file accepts any path, allowing path traversal / arbitrary file overwrite.
    Medium.
F9  agent operations  there is no CI configuration (.github/ missing); AGENTS.md review gates
    depend on a human remembering to run checks. Verify: ls .github. High.
F10 maintainability  categories.py normalizes aliases with a 5-branch if/elif chain; adding
    a category requires editing code. Low.
F11 correctness  dates are not validated; "2026-13-45" or "yesterday" are stored and later
    excluded from every monthly summary. Verify: add such dates and list. High.
```
