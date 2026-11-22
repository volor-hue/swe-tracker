"""Acceptance criteria AC1-AC5 (characterization tests, fictional data)."""
import json
import shutil
from pathlib import Path

import pytest

from expense_tracker import cli, storage, tracker
from expense_tracker.report import render_report, report_extension

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample_expenses.json"


@pytest.fixture
def sample(tmp_path):
    dst = tmp_path / "sample.json"
    shutil.copy(SAMPLE, dst)
    return str(dst)


def test_ac1_add_persists_and_lists(tmp_path, capsys):
    path = str(tmp_path / "e.json")
    assert cli.main(["--file", path, "add", "2026-11-05", "2500", "Taxi", "--description", "fictional"]) == 0
    raw = json.loads(Path(path).read_text())
    assert raw["expenses"][0]["category"] == "transport"
    cli.main(["--file", path, "list"])
    assert "transport" in capsys.readouterr().out


def test_ac2_monthly_summary_only_that_month(sample):
    data = storage.load_data(sample)
    assert tracker.monthly_summary(data["expenses"], "2026-11") == {
        "food": 12500.0, "housing": 90000.0, "transport": 4200.0, "entertainment": 6000.0,
    }


def test_ac3_budget_alerts(sample):
    data = storage.load_data(sample)
    alerts = tracker.budget_alerts(data["expenses"], data["budgets"], "2026-11")
    assert alerts == ["ALERT: food spent 12500.00 > budget 10000.00"]


@pytest.mark.parametrize("fmt,ext", [("text", ".txt"), ("csv", ".csv"), ("markdown", ".md")])
def test_ac4_reports_consistent_totals(sample, fmt, ext):
    data = storage.load_data(sample)
    out = render_report(data["expenses"], "2026-11", fmt)
    assert "112700.00" in out
    assert report_extension(fmt) == ext


def test_ac5_unknown_format_rejected(sample, tmp_path):
    before = Path(sample).read_text()
    with pytest.raises(SystemExit) as exc:
        cli.main(["--file", sample, "report", "2026-11", "--format", "pdf", "--out", str(tmp_path / "r")])
    assert exc.value.code == 2
    assert Path(sample).read_text() == before
    assert not list(tmp_path.glob("r.*"))
