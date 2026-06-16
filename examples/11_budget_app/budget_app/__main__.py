from __future__ import annotations

import argparse
import sys
from functools import wraps
from pathlib import Path

from .service import BudgetError, BudgetService


def handled(fn):
    @wraps(fn)
    def wrapper(args):
        try:
            fn(args)
            return 0
        except BudgetError as exc:
            print(f"error: {exc}\nhint: run with --help or check category/date/type options", file=sys.stderr)
            return 2
        except OSError as exc:
            print(f"error: file operation failed: {exc}", file=sys.stderr)
            return 1
    return wrapper


def service(args) -> BudgetService:
    return BudgetService(Path(args.data_dir))


def print_row(row) -> None:
    print(f"{row.id}\t{row.date}\t{row.type}\t{row.category}\t{row.amount}\t{row.memo}\t{','.join(row.tags)}")


@handled
def cmd_add(args) -> None:
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    row = service(args).add_transaction(args.type, args.date, args.amount, args.category, args.memo, tags)
    print(f"created id={row.id}")


@handled
def cmd_list(args) -> None:
    count = 0
    for row in service(args).search():
        print_row(row)
        count += 1
        if args.limit and count >= args.limit:
            break


@handled
def cmd_search(args) -> None:
    filters = vars(args)
    filters["type_"] = filters.pop("type")
    filters["from_"] = filters.pop("from_date")
    for row in service(args).search(**filters):
        print_row(row)


@handled
def cmd_summary(args) -> None:
    result = service(args).summary(args.month, args.top)
    print(f"income={result.income}")
    print(f"expense={result.expense}")
    print(f"balance={result.balance}")
    if result.budget is not None:
        rate = result.expense / result.budget * 100
        state = "WARNING over budget" if result.expense > result.budget else "OK"
        print(f"budget={result.budget} used={rate:.1f}% {state}")
    print("category_top")
    for name, amount in result.by_category:
        print(f"- {name}: {amount}")


@handled
def cmd_budget_set(args) -> None:
    service(args).set_budget(args.month, args.amount)
    print("OK")


@handled
def cmd_category_add(args) -> None:
    service(args).add_category(args.name)
    print("OK")


@handled
def cmd_category_list(args) -> None:
    for name in service(args).categories.list():
        print(name)


@handled
def cmd_category_remove(args) -> None:
    service(args).remove_category(args.name)
    print("OK")


@handled
def cmd_update(args) -> None:
    changes = {
        "type": args.type,
        "date": args.date,
        "amount": args.amount,
        "category": args.category,
        "memo": args.memo,
        "tags": args.tags.split(",") if args.tags else None,
    }
    row = service(args).update_transaction(args.id, **changes)
    print_row(row)


@handled
def cmd_delete(args) -> None:
    service(args).delete_transaction(args.id)
    print("deleted")


@handled
def cmd_export(args) -> None:
    filters = {"month": args.month, "from_": args.from_date, "to": args.to}
    if not any(filters.values()):
        raise BudgetError("export requires --month or --from/--to")
    count = service(args).export_csv(Path(args.out), filters)
    print(f"exported {count} rows")


@handled
def cmd_import(args) -> None:
    count = service(args).import_csv(Path(args.from_csv))
    print(f"imported {count} rows")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m budget_app")
    parser.add_argument("--data-dir", default="data")
    sub = parser.add_subparsers(required=True)

    add = sub.add_parser("add")
    add.add_argument("--type", required=True, choices=["income", "expense"])
    add.add_argument("--date", required=True)
    add.add_argument("--amount", required=True, type=int)
    add.add_argument("--category", required=True)
    add.add_argument("--memo", default="")
    add.add_argument("--tags", default="")
    add.set_defaults(func=cmd_add)

    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--limit", type=int, default=0)
    list_cmd.set_defaults(func=cmd_list)

    search = sub.add_parser("search")
    search.add_argument("--month")
    search.add_argument("--from", dest="from_date")
    search.add_argument("--to")
    search.add_argument("--category")
    search.add_argument("--type", choices=["income", "expense"])
    search.add_argument("--q")
    search.add_argument("--tag")
    search.set_defaults(func=cmd_search)

    summary = sub.add_parser("summary")
    summary.add_argument("--month", required=True)
    summary.add_argument("--top", type=int, default=5)
    summary.set_defaults(func=cmd_summary)

    budget = sub.add_parser("budget")
    budget_sub = budget.add_subparsers(required=True)
    budget_set = budget_sub.add_parser("set")
    budget_set.add_argument("--month", required=True)
    budget_set.add_argument("--amount", required=True, type=int)
    budget_set.set_defaults(func=cmd_budget_set)

    category = sub.add_parser("category")
    category_sub = category.add_subparsers(required=True)
    category_add = category_sub.add_parser("add")
    category_add.add_argument("name")
    category_add.set_defaults(func=cmd_category_add)
    category_list = category_sub.add_parser("list")
    category_list.set_defaults(func=cmd_category_list)
    category_remove = category_sub.add_parser("remove")
    category_remove.add_argument("name")
    category_remove.set_defaults(func=cmd_category_remove)

    update = sub.add_parser("update")
    update.add_argument("--id", required=True, type=int)
    update.add_argument("--type", choices=["income", "expense"])
    update.add_argument("--date")
    update.add_argument("--amount", type=int)
    update.add_argument("--category")
    update.add_argument("--memo")
    update.add_argument("--tags")
    update.set_defaults(func=cmd_update)

    delete = sub.add_parser("delete")
    delete.add_argument("--id", required=True, type=int)
    delete.set_defaults(func=cmd_delete)

    export = sub.add_parser("export")
    export.add_argument("--out", required=True)
    export.add_argument("--month")
    export.add_argument("--from", dest="from_date")
    export.add_argument("--to")
    export.set_defaults(func=cmd_export)

    import_cmd = sub.add_parser("import")
    import_cmd.add_argument("--from", dest="from_csv", required=True)
    import_cmd.set_defaults(func=cmd_import)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
