from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable

from .models import Transaction


class JsonFile:
    def __init__(self, path: Path, default):
        self.path = path
        self.default = default

    def ensure(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write(self.default)

    def read(self):
        self.ensure()
        with self.path.open("r", encoding="utf-8") as fp:
            return json.load(fp)

    def write(self, data) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        with temp.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)
            fp.write("\n")
        os.replace(temp, self.path)


class TransactionRepository:
    def __init__(self, data_dir: Path):
        self.path = data_dir / "transactions.jsonl"

    def ensure(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def all(self) -> list[Transaction]:
        self.ensure()
        rows: list[Transaction] = []
        with self.path.open("r", encoding="utf-8") as fp:
            for line in fp:
                if line.strip():
                    rows.append(Transaction.from_dict(json.loads(line)))
        return rows

    def stream_latest(self) -> Iterable[Transaction]:
        rows = self.all()
        for item in reversed(rows):
            yield item

    def save_all(self, rows: list[Transaction]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".jsonl.tmp")
        with temp.open("w", encoding="utf-8") as fp:
            for row in rows:
                fp.write(json.dumps(row.to_dict(), ensure_ascii=False) + "\n")
        os.replace(temp, self.path)

    def next_id(self) -> int:
        rows = self.all()
        return max((row.id for row in rows), default=0) + 1


class CategoryStore:
    def __init__(self, data_dir: Path):
        self.file = JsonFile(data_dir / "categories.json", [])

    def list(self) -> list[str]:
        return list(self.file.read())

    def save(self, categories: list[str]) -> None:
        self.file.write(sorted(set(categories)))


class BudgetStore:
    def __init__(self, data_dir: Path):
        self.file = JsonFile(data_dir / "budgets.json", {})

    def all(self) -> dict[str, int]:
        return {key: int(value) for key, value in self.file.read().items()}

    def set(self, month: str, amount: int) -> None:
        rows = self.all()
        rows[month] = amount
        self.file.write(rows)
