#!/usr/bin/env python3
from __future__ import annotations

import time


class MiniRedis:
    def __init__(self):
        self.store = {}
        self.expires = {}
        self.used_at = {}
        self.maxmemory = 0
        self.evicted = 0

    def _cleanup(self):
        now = time.time()
        for key, expire_at in list(self.expires.items()):
            if expire_at <= now:
                self.store.pop(key, None)
                self.expires.pop(key, None)
                self.used_at.pop(key, None)

    def _memory(self):
        return sum(len(k.encode()) + len(v.encode()) for k, v in self.store.items())

    def _evict_lru(self):
        if not self.used_at:
            return
        key = min(self.used_at, key=self.used_at.get)
        self.store.pop(key, None)
        self.expires.pop(key, None)
        self.used_at.pop(key, None)
        self.evicted += 1

    def set(self, key, value):
        self._cleanup()
        if self.maxmemory and len(key.encode()) + len(value.encode()) > self.maxmemory:
            return "(error) OOM"
        self.store[key] = value
        self.expires.pop(key, None)
        self.used_at[key] = time.time()
        while self.maxmemory and self._memory() > self.maxmemory:
            self._evict_lru()
        return "OK"

    def get(self, key):
        self._cleanup()
        if key not in self.store:
            return "(nil)"
        self.used_at[key] = time.time()
        return self.store[key]

    def delete(self, key):
        self._cleanup()
        existed = key in self.store
        self.store.pop(key, None)
        self.expires.pop(key, None)
        self.used_at.pop(key, None)
        return f"(integer) {1 if existed else 0}"

    def expire(self, key, seconds):
        self._cleanup()
        if key not in self.store:
            return "(integer) 0"
        self.expires[key] = time.time() + int(seconds)
        return "(integer) 1"

    def ttl(self, key):
        self._cleanup()
        if key not in self.store:
            return "(integer) -2"
        if key not in self.expires:
            return "(integer) -1"
        return f"(integer) {max(0, int(self.expires[key] - time.time()))}"


def main():
    db = MiniRedis()
    while True:
        line = input("mini-redis> ").strip()
        if line in {"exit", "quit"}:
            break
        parts = line.split()
        cmd = parts[0].upper() if parts else ""
        if cmd == "SET" and len(parts) >= 3:
            print(db.set(parts[1], " ".join(parts[2:])))
        elif cmd == "GET" and len(parts) == 2:
            print(db.get(parts[1]))
        elif cmd == "DEL" and len(parts) == 2:
            print(db.delete(parts[1]))
        elif cmd == "EXPIRE" and len(parts) == 3:
            print(db.expire(parts[1], parts[2]))
        elif cmd == "TTL" and len(parts) == 2:
            print(db.ttl(parts[1]))
        elif cmd == "INFO":
            print(f"used_memory:{db._memory()}\nevicted_keys:{db.evicted}")
        elif cmd == "CONFIG" and parts[1:3] == ["SET", "maxmemory"]:
            db.maxmemory = int(parts[3])
            print("OK")
        else:
            print("(error) unknown command")


if __name__ == "__main__":
    main()
