#!/usr/bin/env python3
"""Validate a plain-text Gmail body before GOG transmission."""

from __future__ import annotations

import sys
import re
from pathlib import Path


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if not text.strip():
        errors.append("body is empty")
    if "\\n" in text:
        errors.append("body contains literal \\n sequences instead of line breaks")
    if "\r" in text:
        errors.append("body contains carriage returns; use UTF-8 LF line endings")
    if text and not text.endswith("\n"):
        errors.append("body must end with a newline")

    lines = text.splitlines()
    for index, line in enumerate(lines, start=1):
        if line.rstrip() != line:
            errors.append(f"line {index} has trailing whitespace")
        if line and len(line) > 1_000:
            errors.append(f"line {index} is too long to be a natural email paragraph")

    def is_list_item(line: str) -> bool:
        return line.startswith("- ") or bool(re.match(r"^\d+\. ", line))

    for index, line in enumerate(lines):
        is_item = is_list_item(line)
        if is_item and index > 0 and lines[index - 1] and not is_list_item(lines[index - 1]):
            errors.append(f"line {index + 1} needs a blank line before the list")
        if (
            is_item
            and index + 1 < len(lines)
            and not is_list_item(lines[index + 1])
            and lines[index + 1]
        ):
            errors.append(f"line {index + 1} needs a blank line after the list")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_email_body.py EMAIL_BODY.txt", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    errors = validate(path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
