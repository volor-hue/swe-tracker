import math
import re
from dataclasses import asdict, dataclass
from datetime import date as _date

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def validate_month(month: str) -> str:
    if not isinstance(month, str) or not _MONTH_RE.match(month):
        raise ValueError(f"invalid month {month!r}: expected YYYY-MM")
    return month


def validate_date(value: str) -> str:
    if not isinstance(value, str) or not _DATE_RE.match(value):
        raise ValueError(f"invalid date {value!r}: expected YYYY-MM-DD")
    _date.fromisoformat(value)  # raises ValueError for e.g. 2026-11-31
    return value


@dataclass
class Expense:
    date: str  # YYYY-MM-DD
    amount: float
    category: str
    description: str = ""

    def __post_init__(self) -> None:
        validate_date(self.date)
        self.amount = float(self.amount)
        if not math.isfinite(self.amount) or self.amount <= 0:
            raise ValueError(f"invalid amount {self.amount!r}: must be a finite number > 0")

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Expense":
        return Expense(d["date"], float(d["amount"]), d["category"], d.get("description", ""))
