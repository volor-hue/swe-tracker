import json
import os

from .models import Expense

DEFAULT_PATH = "expenses.json"


def load_data(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return {"expenses": [], "budgets": {}}
    with open(path) as f:
        raw = json.load(f)
    return {
        "expenses": [Expense.from_dict(d) for d in raw.get("expenses", [])],
        "budgets": raw.get("budgets", {}),
    }


def save_data(data, path=DEFAULT_PATH):
    with open(path, "w") as f:
        json.dump(
            {
                "expenses": [e.to_dict() for e in data["expenses"]],
                "budgets": data["budgets"],
            },
            f,
            indent=2,
        )
