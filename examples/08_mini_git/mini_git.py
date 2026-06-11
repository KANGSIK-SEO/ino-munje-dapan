#!/usr/bin/env python3
from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class Commit:
    hash: str
    message: str
    author: str
    timestamp: float
    parents: list[str]


class MiniGit:
    def __init__(self):
        self.user = ""
        self.commits: dict[str, Commit] = {}
        self.branches: dict[str, str | None] = {}
        self.head = ""
        self.next_id = 1

    def init(self, user: str) -> str:
        self.user = user
        self.branches = {"main": None}
        self.head = "main"
        return "OK"

    def commit(self, message: str) -> str:
        parent = self.branches[self.head]
        hash_value = f"c{self.next_id:04d}"
        self.next_id += 1
        parents = [parent] if parent else []
        self.commits[hash_value] = Commit(hash_value, message, self.user, time.time(), parents)
        self.branches[self.head] = hash_value
        return f"commit {hash_value}"

    def branch(self, name: str) -> str:
        self.branches[name] = self.branches[self.head]
        return "OK"

    def switch(self, name: str) -> str:
        if name not in self.branches:
            return "ERROR no branch"
        self.head = name
        return "OK"

    def log(self) -> str:
        result = []
        current = self.branches[self.head]
        while current:
            commit = self.commits[current]
            result.append(f"{commit.hash} {commit.message}")
            current = commit.parents[0] if commit.parents else None
        return "\n".join(result)

    def search(self, keyword: str) -> str:
        rows = [f"{c.hash} {c.message}" for c in self.commits.values() if keyword.lower() in c.message.lower()]
        return "\n".join(rows) or "No results"


def main():
    repo = MiniGit()
    while True:
        line = input("mini-git> ").strip()
        if line in {"exit", "quit"}:
            break
        parts = line.split(maxsplit=1)
        cmd = parts[0].upper() if parts else ""
        arg = parts[1] if len(parts) > 1 else ""
        if cmd == "INIT":
            print(repo.init(arg))
        elif cmd == "COMMIT":
            print(repo.commit(arg.strip('"')))
        elif cmd == "BRANCH":
            print(repo.branch(arg))
        elif cmd == "SWITCH":
            print(repo.switch(arg))
        elif cmd == "LOG":
            print(repo.log())
        elif cmd == "SEARCH":
            print(repo.search(arg))
        else:
            print("ERROR unknown command")


if __name__ == "__main__":
    main()
