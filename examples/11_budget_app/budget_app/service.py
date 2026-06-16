from __future__ import annotations

import csv
import re
from pathlib import Path

from .models import Summary, Transaction
from .repository import BudgetStore, CategoryStore, TransactionRepository

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


class BudgetError(Exception):
    pass


class BudgetService:
    def __init__(self, data_dir: Path):
        self.transactions = TransactionRepository(data_dir)
        self.categories = CategoryStore(data_dir)
        self.budgets = BudgetStore(data_dir)

    def add_category(self, name: str) -> None:
        if not name.strip():
            raise BudgetError("category name is required")
        rows = self.categories.list()
        rows.append(name.strip())
        self.categories.save(rows)

    def remove_category(self, name: str) -> None:
        if any(row.category == name for row in self.transactions.all()):
            raise BudgetError("category is used by transactions; delete or update them first")
        self.categories.save([row for row in self.categories.list() if row != name])

    def add_transaction(self, type_: str, date: str, amount: int, category: str, memo: str, tags: list[str]) -> Transaction:
        self._validate_transaction(type_, date, amount, category)
        row = Transaction(self.transactions.next_id(), type_, date, amount, category, memo, tags)
        rows = self.transactions.all()
        rows.append(row)
        self.transactions.save_all(rows)
        return row

    def update_transaction(self, id_: int, **changes) -> Transaction:
        rows = self.transactions.all()
        for idx, row in enumerate(rows):
            if row.id == id_:
                data = row.to_dict()
                for key, value in changes.items():
                    if value is not None:
                        data[key] = value
                updated = Transaction.from_dict(data)
                self._validate_transaction(updated.type, updated.date, updated.amount, updated.category)
                rows[idx] = updated
                self.transactions.save_all(rows)
                return updated
        raise BudgetError(f"transaction not found: {id_}")

    def delete_transaction(self, id_: int) -> bool:
        rows = self.transactions.all()
        next_rows = [row for row in rows if row.id != id_]
        if len(rows) == len(next_rows):
            raise BudgetError(f"transaction not found: {id_}")
        self.transactions.save_all(next_rows)
        return True

    def search(self, **filters):
        for row in self.transactions.stream_latest():
            if self._matches(row, filters):
                yield row

    def summary(self, month: str, top: int) -> Summary:
        if not MONTH_RE.match(month):
            raise BudgetError("month must be YYYY-MM")
        income = 0
        expense = 0
        by_category: dict[str, int] = {}
        for row in self.transactions.all():
            if not row.date.startswith(month):
                continue
            if row.type == "income":
                income += row.amount
            else:
                expense += row.amount
                by_category[row.category] = by_category.get(row.category, 0) + row.amount
        ranked = sorted(by_category.items(), key=lambda item: item[1], reverse=True)[:top]
        return Summary(income, expense, income - expense, ranked, self.budgets.all().get(month))

    def set_budget(self, month: str, amount: int) -> None:
        if not MONTH_RE.match(month):
            raise BudgetError("month must be YYYY-MM")
        if amount <= 0:
            raise BudgetError("budget amount must be positive")
        self.budgets.set(month, amount)

    def export_csv(self, path: Path, filters: dict) -> int:
        rows = list(self.search(**filters))
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=["id", "date", "type", "category", "amount", "memo", "tags"])
            writer.writeheader()
            for row in rows:
                data = row.to_dict()
                data["tags"] = ",".join(row.tags)
                writer.writerow(data)
        return len(rows)

    def import_csv(self, path: Path) -> int:
        count = 0
        with path.open("r", encoding="utf-8", newline="") as fp:
            for row in csv.DictReader(fp):
                self.add_transaction(row["type"], row["date"], int(row["amount"]), row["category"], row.get("memo", ""), row.get("tags", "").split(","))
                count += 1
        return count

    def _validate_transaction(self, type_: str, date: str, amount: int, category: str) -> None:
        if type_ not in {"income", "expense"}:
            raise BudgetError("type must be income or expense")
        if not DATE_RE.match(date):
            raise BudgetError("date must be YYYY-MM-DD")
        if amount <= 0:
            raise BudgetError("amount must be positive")
        if category not in self.categories.list():
            raise BudgetError(f"unknown category: {category}; add it first")

    def _matches(self, row: Transaction, filters: dict) -> bool:
        if filters.get("month") and not row.date.startswith(filters["month"]):
            return False
        if filters.get("from_") and row.date < filters["from_"]:
            return False
        if filters.get("to") and row.date > filters["to"]:
            return False
        if filters.get("category") and row.category != filters["category"]:
            return False
        if filters.get("type_") and row.type != filters["type_"]:
            return False
        if filters.get("q") and filters["q"].lower() not in row.memo.lower():
            return False
        if filters.get("tag") and filters["tag"] not in row.tags:
            return False
        return True
