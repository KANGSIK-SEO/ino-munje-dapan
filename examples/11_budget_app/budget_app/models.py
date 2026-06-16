from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Transaction:
    id: int
    type: str
    date: str
    amount: int
    category: str
    memo: str
    tags: list[str]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, row: dict) -> "Transaction":
        tags = row.get("tags", [])
        if isinstance(tags, str):
            tags = [tag for tag in tags.split(",") if tag]
        return cls(
            id=int(row["id"]),
            type=str(row["type"]),
            date=str(row["date"]),
            amount=int(row["amount"]),
            category=str(row["category"]),
            memo=str(row.get("memo", "")),
            tags=list(tags),
        )


@dataclass
class Summary:
    income: int
    expense: int
    balance: int
    by_category: list[tuple[str, int]]
    budget: int | None
