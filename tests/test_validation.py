"""Regression tests for the top-2 risks (R1 invalid amounts, R2 month/date format)."""
import math
from pathlib import Path

import pytest

from expense_tracker import cli, storage, tracker
from expense_tracker.models import Expense


# ---- R1: invalid amounts -------------------------------------------------
@pytest.mark.parametrize("amount", ["-5000", "0", "nan", "inf", "-inf"])
def test_r1_add_rejects_non_positive_or_non_finite(tmp_path, amount):
    path = tmp_path / "e.json"
    with pytest.raises(ValueError):
        tracker.add_expense(str(path), "2026-11-01", amount, "food")
    assert not path.exists()


def test_r1_load_rejects_nan_in_stored_file(tmp_path):
    path = tmp_path / "e.json"
    path.write_text('{"expenses": [{"date": "2026-11-01", "amount": NaN, "category": "food"}], "budgets": {}}')
    with pytest.raises(ValueError):
        storage.load_data(str(path))


def test_r1_cli_invalid_amount_exit_1_and_no_write(tmp_path, capsys):
    path = tmp_path / "e.json"
    assert cli.main(["--file", str(path), "add", "2026-11-01", "nan", "food"]) == 1
    assert "error" in capsys.readouterr().err.lower()
    assert not path.exists()


def test_r1_valid_amount_still_accepted():
    e = Expense("2026-11-01", 10.5, "food")
    assert math.isclose(e.amount, 10.5)


# ---- R2: month / date format ---------------------------------------------
@pytest.mark.parametrize("month", ["2026-1", "2026-13", "2026-00", "nov", "2026/11", ""])
def test_r2_monthly_summary_rejects_malformed_month(month):
    with pytest.raises(ValueError):
        tracker.monthly_summary([Expense("2026-11-01", 1.0, "food")], month)


def test_r2_month_prefix_does_not_mix_months():
    expenses = [Expense("2026-10-05", 1.0, "food"), Expense("2026-01-05", 2.0, "food")]
    assert tracker.monthly_summary(expenses, "2026-01") == {"food": 2.0}


@pytest.mark.parametrize("date", ["2026-13-45", "yesterday", "2026-11-31", "26-11-01"])
def test_r2_add_rejects_invalid_date(tmp_path, date):
    path = tmp_path / "e.json"
    with pytest.raises(ValueError):
        tracker.add_expense(str(path), date, "100", "food")
    assert not path.exists()


def test_r2_cli_invalid_month_exit_1(tmp_path, capsys):
    sample = Path(__file__).resolve().parent.parent / "data" / "sample_expenses.json"
    assert cli.main(["--file", str(sample), "summary", "2026-1"]) == 1
    assert "month" in capsys.readouterr().err.lower()
