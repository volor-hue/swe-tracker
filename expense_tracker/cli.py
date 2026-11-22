import argparse
import sys

from . import report, storage, tracker


def main(argv=None):
    p = argparse.ArgumentParser(prog="expense-tracker")
    p.add_argument("--file", default=storage.DEFAULT_PATH)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("date")
    a.add_argument("amount")
    a.add_argument("category")
    a.add_argument("--description", default="")
    sub.add_parser("list")
    s = sub.add_parser("summary")
    s.add_argument("month")
    r = sub.add_parser("report")
    r.add_argument("month")
    r.add_argument("--format", default="text", choices=sorted(report.FORMATTERS))
    r.add_argument("--out")
    b = sub.add_parser("budget")
    b.add_argument("category")
    b.add_argument("limit", type=float)
    al = sub.add_parser("alerts")
    al.add_argument("month")
    args = p.parse_args(argv)
    try:
        return _run(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _run(args):
    if args.cmd == "add":
        e = tracker.add_expense(args.file, args.date, args.amount, args.category, args.description)
        print(f"added {e.date} {e.amount:.2f} {e.category}")
    elif args.cmd == "list":
        for e in storage.load_data(args.file)["expenses"]:
            print(f"{e.date}  {e.amount:>10.2f}  {e.category:<14} {e.description}")
    elif args.cmd == "summary":
        data = storage.load_data(args.file)
        for cat, total in sorted(tracker.monthly_summary(data["expenses"], args.month).items()):
            print(f"{cat:<15}{total:>10.2f}")
    elif args.cmd == "report":
        data = storage.load_data(args.file)
        text = report.render_report(data["expenses"], args.month, args.format)
        if args.out:
            out = args.out + report.report_extension(args.format)
            with open(out, "w") as f:
                f.write(text + "\n")
            print(f"wrote {out}")
        else:
            print(text)
    elif args.cmd == "budget":
        tracker.set_budget(args.file, args.category, args.limit)
        print(f"budget set: {args.category} = {args.limit:.2f}")
    elif args.cmd == "alerts":
        data = storage.load_data(args.file)
        for line in tracker.budget_alerts(data["expenses"], data["budgets"], args.month):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
