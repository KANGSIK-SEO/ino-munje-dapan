#!/usr/bin/env python3
"""AI Git commit and PR draft generator.

This is a safe starter version. It reads git changes and creates a local draft.
Replace `call_ai` with a real AI API call when an API key is ready.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?[^'\"\s]+"),
]


def run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def mask_secrets(text: str) -> str:
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(r"\1=***MASKED***", text)
    return text


def collect_changes(safe_mode: bool) -> tuple[str, str]:
    status = run_git(["status", "--short"])
    if not status:
        raise SystemExit("No git changes. Nothing to generate.")

    diff = run_git(["diff", "--", "."])
    if safe_mode:
        diff = mask_secrets(diff[:8000])
    return status, diff


def call_ai(status: str, diff: str, model: str, temperature: float, max_tokens: int) -> str:
    api_key = os.getenv("AI_API_KEY")
    if not api_key:
        return make_local_draft(status)

    # Real API integration point.
    # Send status, diff, model, temperature, and max_tokens to the AI provider here.
    return make_local_draft(status)


def make_local_draft(status: str) -> str:
    files = [line[3:] if len(line) > 3 else line for line in status.splitlines()]
    file_list = "\n".join(f"- {name}" for name in files[:5])
    return f"""Commit Message
docs: update project files

PR Title
Update project files

PR Body
Why
- Keep the repository contents up to date.

What
{file_list}

How to Test
- Review changed files with git diff.
- Run project-specific checks if available.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4.1-mini")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=800)
    parser.add_argument("--safe-mode", action="store_true")
    args = parser.parse_args()

    status, diff = collect_changes(args.safe_mode)
    print(call_ai(status, diff, args.model, args.temperature, args.max_tokens))


if __name__ == "__main__":
    main()
