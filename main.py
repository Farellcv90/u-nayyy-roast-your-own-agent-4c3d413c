#!/usr/bin/env python3
"""Roast Your Own Agent — writes the one-line roast to /output/entry.txt."""

import os
import sys

ENTRY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
OUTPUT_PATH = "/output/entry.txt"


def validate(text: str) -> str | None:
    """Return an error message if the roast line fails the gate, else None."""
    if not text.strip():
        return "invalid entry: blank or only whitespace"
    if text != text.strip():
        return "invalid entry: leading or trailing whitespace"
    if not (1 <= len(text) <= 200):
        return f"invalid entry: {len(text)} characters (must be 1-200)"
    if len(text.splitlines()) != 1:
        return "invalid entry: must be a single line"
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        return "invalid entry: contains control characters"
    # UTF-8 round-trip: the file must be clean, decodable text.
    text.encode("utf-8").decode("utf-8")
    return None


def main() -> int:
    with open(ENTRY_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    error = validate(text)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
