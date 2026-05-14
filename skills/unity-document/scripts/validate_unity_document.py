#!/usr/bin/env python3
"""Validate Unity system documentation structure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "Overview",
    "System Architecture",
    "Core Components",
    "Lifecycle & Initialization",
    "Data Models",
    "How to Setup an Event",
    "How to Fake Data for Testing",
    "Validation",
    "Debugging",
    "API Reference",
]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to the Unity system document")
    return parser.parse_args()


def _heading_order(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(2))
    return headings


def main() -> int:
    args = _parse_args()
    path = args.path

    errors: list[str] = []

    if not path.exists():
        errors.append(f"file does not exist: {path}")
    elif path.suffix.lower() != ".md":
        errors.append("document must be a markdown file")

    if "Docs/Systems" not in path.as_posix():
        errors.append("document must live under Docs/Systems/")

    text = path.read_text(encoding="utf-8") if path.exists() else ""
    headings = _heading_order(text)
    required_set = set(REQUIRED_HEADINGS)

    missing = [heading for heading in REQUIRED_HEADINGS if heading not in headings]
    if missing:
        errors.append("missing headings: " + ", ".join(missing))

    filtered = [heading for heading in headings if heading in required_set]
    if filtered != REQUIRED_HEADINGS:
        errors.append("headings are out of order")

    if "```mermaid" not in text:
        errors.append("document must include at least one Mermaid diagram")

    placeholders = ["TODO", "TBD", "FIXME"]
    found_placeholders = [token for token in placeholders if token in text]
    if found_placeholders:
        errors.append("contains placeholders: " + ", ".join(found_placeholders))

    if not re.search(r"\([^)]+:\d+\)", text):
        errors.append("missing file:line citations")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
