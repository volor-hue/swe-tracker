"""Report formatting using a small Strategy registry.

Each output format is one ReportFormatter strategy that owns both its rendering
and its file extension, so adding a format is one class plus one registry entry
instead of editing several if/elif chains.
"""
from dataclasses import dataclass
from typing import Protocol

from .tracker import monthly_summary


class ReportFormatter(Protocol):
    @property
    def extension(self) -> str: ...

    def render(self, month: str, summary: dict[str, float], total: float) -> str: ...


@dataclass(frozen=True)
class TextFormatter:
    extension: str = ".txt"

    def render(self, month: str, summary: dict[str, float], total: float) -> str:
        lines = [f"Expense report for {month}"]
        lines += [f"{cat:<15}{summary[cat]:>10.2f}" for cat in sorted(summary)]
        lines.append(f"{'TOTAL':<15}{total:>10.2f}")
        return "\n".join(lines)


@dataclass(frozen=True)
class CsvFormatter:
    extension: str = ".csv"

    def render(self, month: str, summary: dict[str, float], total: float) -> str:
        lines = ["category,amount"]
        lines += [f"{cat},{summary[cat]:.2f}" for cat in sorted(summary)]
        lines.append(f"TOTAL,{total:.2f}")
        return "\n".join(lines)


@dataclass(frozen=True)
class MarkdownFormatter:
    extension: str = ".md"

    def render(self, month: str, summary: dict[str, float], total: float) -> str:
        lines = [f"# Expense report for {month}", "", "| Category | Amount |", "|---|---:|"]
        lines += [f"| {cat} | {summary[cat]:.2f} |" for cat in sorted(summary)]
        lines.append(f"| **TOTAL** | **{total:.2f}** |")
        return "\n".join(lines)


FORMATTERS: dict[str, ReportFormatter] = {
    "text": TextFormatter(),
    "csv": CsvFormatter(),
    "markdown": MarkdownFormatter(),
}


def get_formatter(fmt: str) -> ReportFormatter:
    try:
        return FORMATTERS[fmt]
    except KeyError:
        raise ValueError(f"unknown format: {fmt}") from None


def render_report(expenses, month: str, fmt: str) -> str:
    formatter = get_formatter(fmt)
    summary = monthly_summary(expenses, month)
    total = round(sum(summary.values()), 2)
    return formatter.render(month, summary, total)


def report_extension(fmt: str) -> str:
    return get_formatter(fmt).extension
