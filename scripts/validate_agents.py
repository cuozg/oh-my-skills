#!/usr/bin/env python3
"""Validate OpenCode agent markdown files in this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("PyYAML is required. Install with: python -m pip install PyYAML")
    sys.exit(2)


ALLOWED_FIELDS = {
    "name",
    "model",
    "variant",
    "description",
    "mode",
    "hidden",
    "color",
    "steps",
    "options",
    "permission",
    "disable",
    "temperature",
    "top_p",
}

VALID_MODES = {"primary", "subagent", "all"}
VALID_ACTIONS = {"allow", "ask", "deny"}
SHORTHAND_ONLY_PERMISSIONS = {"todowrite", "question", "webfetch", "websearch", "doom_loop"}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def validate_permission_value(key: str, value: object) -> list[str]:
    errors: list[str] = []

    if isinstance(value, str):
        if value not in VALID_ACTIONS:
            errors.append(f"permission.{key} has invalid action '{value}'")
        return errors

    if key in SHORTHAND_ONLY_PERMISSIONS:
        errors.append(f"permission.{key} must be a shorthand action, not an object")
        return errors

    if not isinstance(value, dict):
        errors.append(f"permission.{key} must be an action or pattern object")
        return errors

    for pattern, action in value.items():
        if not isinstance(pattern, str):
            errors.append(f"permission.{key} contains a non-string pattern")
        if action not in VALID_ACTIONS:
            errors.append(f"permission.{key}.{pattern} has invalid action '{action}'")

    return errors


def validate_agent(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return ["missing YAML frontmatter"]

    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        return [f"invalid YAML frontmatter: {exc}"]

    errors: list[str] = []
    unknown_fields = sorted(set(frontmatter) - ALLOWED_FIELDS)
    if unknown_fields:
        errors.append(f"unknown frontmatter fields: {', '.join(unknown_fields)}")

    name = frontmatter.get("name", path.stem)
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        errors.append("name must be lowercase hyphen-case")
    elif name != path.stem:
        errors.append(f"name '{name}' must match filename stem '{path.stem}'")

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("description is required")

    mode = frontmatter.get("mode")
    if mode is not None and mode not in VALID_MODES:
        errors.append(f"mode must be one of: {', '.join(sorted(VALID_MODES))}")

    permission = frontmatter.get("permission")
    if permission is not None:
        if isinstance(permission, str):
            if permission not in VALID_ACTIONS:
                errors.append(f"permission has invalid action '{permission}'")
        elif isinstance(permission, dict):
            for key, value in permission.items():
                errors.extend(validate_permission_value(str(key), value))
        else:
            errors.append("permission must be an action or object")

    body = content[match.end() :].strip()
    if not body:
        errors.append("agent prompt body is empty")

    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "agents"
    paths = sorted(root.glob("*.md"))
    if not paths:
        print(f"No agent files found in {root}")
        return 1

    failed = False
    for path in paths:
        errors = validate_agent(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
