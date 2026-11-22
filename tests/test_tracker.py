from expense_tracker import storage, tracker
from expense_tracker.report import render_report


def test_add_expense_persists(tmp_path):
    path = tmp_path / "e.json"
    tracker.add_expense(str(path), "2026-11-03", "1200", "groceries", "fictional")
    data = storage.load_data(str(path))
    assert len(data["expenses"]) == 1
    assert data["expenses"][0].category == "food"


def test_monthly_summary_totals(tmp_path):
    path = str(tmp_path / "e.json")
    tracker.add_expense(path, "2026-11-01", "1000", "food")
    tracker.add_expense(path, "2026-11-02", "500", "taxi")
    tracker.add_expense(path, "2026-10-30", "999", "food")
    data = storage.load_data(path)
    assert tracker.monthly_summary(data["expenses"], "2026-11") == {"food": 1000.0, "transport": 500.0}


def test_text_report_has_total(tmp_path):
    path = str(tmp_path / "e.json")
    tracker.add_expense(path, "2026-11-01", "1000", "food")
    data = storage.load_data(path)
    assert "TOTAL" in render_report(data["expenses"], "2026-11", "text")
