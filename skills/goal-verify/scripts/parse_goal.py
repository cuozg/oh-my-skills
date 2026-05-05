#!/usr/bin/env python3
"""
parse_goal.py — Parse a goal file into structured data.

Extracts YAML frontmatter and Markdown sections (Objective, Context,
Acceptance Criteria, Constraints, Notes) from a goal file at
Docs/Goals/<feature>/<task>.md.

Usage:
    python parse_goal.py <path_to_goal.md>              # prints JSON
    from parse_goal import parse_goal                    # returns dict

Stdlib only. Hand-parses YAML frontmatter (no PyYAML dependency).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
CHECKBOX_RE = re.compile(r"^\s*-\s*\[(?P<mark>[ xX])\]\s+(?P<text>.+?)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

VALID_STATUSES = {"pending", "in-progress", "completed", "blocked"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
REQUIRED_FRONTMATTER_KEYS = ("status", "priority", "created", "updated", "depends_on")


def _parse_scalar(raw: str) -> Any:
    """Parse a YAML scalar: string, quoted string, null, or inline list."""
    s = raw.strip()
    if not s or s.lower() in {"null", "~"}:
        return None
    # Inline list: [a, b, c] or []
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
    # Quoted strings
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split frontmatter from body. Returns (frontmatter_dict, body_text)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    raw_fm = match.group(1)
    body = text[match.end():]

    data: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[str] | None = None

    for line in raw_fm.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        # Block-style list item
        stripped = line.strip()
        if stripped.startswith("- ") and current_list is not None:
            current_list.append(stripped[2:].strip().strip("'\""))
            continue

        # key: value
        if ":" in line and not line.startswith(" "):
            if current_list is not None and current_key is not None:
                data[current_key] = current_list
                current_list = None

            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()

            if not value:
                # Potential block list follows
                current_key = key
                current_list = []
                data[key] = []
            else:
                data[key] = _parse_scalar(value)
                current_key = key
                current_list = None

    if current_list is not None and current_key is not None:
        data[current_key] = current_list

    return data, body


def extract_sections(body: str) -> dict[str, str]:
    """Extract top-level (## heading) sections from Markdown body."""
    sections: dict[str, str] = {}
    current_name: str | None = None
    current_lines: list[str] = []

    for line in body.splitlines():
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 2:  # ## level only
            if current_name is not None:
                sections[current_name] = "\n".join(current_lines).strip()
            current_name = m.group(2).strip()
            current_lines = []
        else:
            if current_name is not None:
                current_lines.append(line)

    if current_name is not None:
        sections[current_name] = "\n".join(current_lines).strip()

    return sections


def extract_title(body: str) -> str:
    """Extract the first # H1 from the body."""
    for line in body.splitlines():
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 1:
            return m.group(2).strip()
    return ""


def parse_checkboxes(text: str) -> list[dict[str, Any]]:
    """Parse checkbox lines into [{text, checked, line_no}]."""
    items: list[dict[str, Any]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        m = CHECKBOX_RE.match(line)
        if m:
            items.append({
                "text": m.group("text").strip(),
                "checked": m.group("mark").lower() == "x",
                "line_no": idx,
            })
    return items


def validate(meta: dict[str, Any]) -> list[str]:
    """Return a list of validation warnings (empty if clean)."""
    warnings: list[str] = []
    for key in REQUIRED_FRONTMATTER_KEYS:
        if key not in meta:
            warnings.append(f"missing frontmatter key: {key}")
    status = meta.get("status")
    if status and status not in VALID_STATUSES:
        warnings.append(f"invalid status '{status}' (expected {sorted(VALID_STATUSES)})")
    priority = meta.get("priority")
    if priority and priority not in VALID_PRIORITIES:
        warnings.append(f"invalid priority '{priority}' (expected {sorted(VALID_PRIORITIES)})")
    return warnings


def parse_goal(path: str | Path) -> dict[str, Any]:
    """
    Parse a goal file into a structured dict.

    Returns:
        {
            "path": str,
            "title": str,
            "frontmatter": {status, priority, created, updated, depends_on, ...},
            "sections": {Objective: str, Context: str, ...},
            "acceptance_criteria": [{text, checked, line_no}, ...],
            "warnings": [str, ...],
        }
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"goal file not found: {p}")
    if not p.is_file():
        raise ValueError(f"goal path is not a file: {p}")

    text = p.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    title = extract_title(body)
    sections = extract_sections(body)
    ac_text = sections.get("Acceptance Criteria", "")
    criteria = parse_checkboxes(ac_text)
    warnings = validate(frontmatter)
    if not criteria:
        warnings.append("no acceptance criteria checkboxes found")

    return {
        "path": str(p),
        "title": title,
        "frontmatter": frontmatter,
        "sections": sections,
        "acceptance_criteria": criteria,
        "warnings": warnings,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: parse_goal.py <path_to_goal.md>", file=sys.stderr)
        return 2
    try:
        result = parse_goal(argv[1])
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
