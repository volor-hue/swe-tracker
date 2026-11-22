from . import storage
from .categories import normalize_category
from .models import Expense, validate_month


def add_expense(path, date, amount, category, description=""):
    data = storage.load_data(path)
    exp = Expense(date, float(amount), normalize_category(category), description)
    data["expenses"].append(exp)
    storage.save_data(data, path)
    return exp


def set_budget(path, category, limit):
    data = storage.load_data(path)
    data["budgets"][normalize_category(category)] = float(limit)
    storage.save_data(data, path)


def monthly_summary(expenses, month):
    validate_month(month)
    totals = {}
    for e in expenses:
        if e.date[:7] == month:
            totals[e.category] = round(totals.get(e.category, 0.0) + e.amount, 2)
    return totals


def get_budget(budgets: dict[str, float], category: str) -> float | None:
    return budgets.get(category)


def budget_alerts(expenses, budgets, month):
    alerts = []
    summary = monthly_summary(expenses, month)
    for cat, spent in sorted(summary.items()):
        limit = get_budget(budgets, cat)
        if limit is not None and spent > limit:
            alerts.append(f"ALERT: {cat} spent {spent:.2f} > budget {limit:.2f}")
    return alerts
