#!/usr/bin/env python3
"""
Skill Validator - Deep structural validation with parallel checks.

Goes beyond quick_validate.py's frontmatter-only checks:
  - Validates frontmatter (name, description, allowed keys)
  - Checks SKILL.md body integrity (line count, unfilled TODOs, broken refs)
  - Detects orphaned files (in scripts/references/assets but never referenced)
  - Validates referenced files exist on disk
  - Checks naming, description quality, progressive disclosure

Usage:
    python skill-validator.py <skill-directory> [--fix] [--json]

Flags:
    --fix   Auto-fix trivially fixable issues (trailing whitespace, permissions)
    --json  Output results as JSON instead of human-readable text
"""

import sys
import os
import re
import json
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def extract_frontmatter(skill_md_path):
    content = skill_md_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None, content, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---\n?(.*)", content, re.DOTALL)
    if not match:
        return None, content, "Invalid frontmatter format"

    try:
        fm = yaml.safe_load(match.group(1))
        if not isinstance(fm, dict):
            return None, content, "Frontmatter must be a YAML dict"
        return fm, match.group(2), None
    except yaml.YAMLError as e:
        return None, content, f"YAML parse error: {e}"


ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
MAX_BODY_LINES = 500


def check_frontmatter(fm):
    issues = []

    unexpected = set(fm.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        issues.append(
            ("error", f"Unexpected frontmatter keys: {', '.join(sorted(unexpected))}")
        )

    name = fm.get("name", "")
    if not name:
        issues.append(("error", "Missing 'name' in frontmatter"))
    elif not isinstance(name, str):
        issues.append(("error", f"name must be a string, got {type(name).__name__}"))
    else:
        name = name.strip()
        if not re.match(r"^[a-z0-9-]+$", name):
            issues.append(("error", f"Name '{name}' must be hyphen-case"))
        if name.startswith("-") or name.endswith("-") or "--" in name:
            issues.append(("error", f"Name '{name}' has invalid hyphens"))
        if len(name) > MAX_NAME_LEN:
            issues.append(("error", f"Name too long ({len(name)} > {MAX_NAME_LEN})"))

    desc = fm.get("description", "")
    if not desc:
        issues.append(("error", "Missing 'description' in frontmatter"))
    elif not isinstance(desc, str):
        issues.append(
            ("error", f"description must be a string, got {type(desc).__name__}")
        )
    else:
        desc = desc.strip()
        if "<" in desc or ">" in desc:
            issues.append(("error", "Description contains angle brackets"))
        if len(desc) > MAX_DESC_LEN:
            issues.append(
                ("error", f"Description too long ({len(desc)} > {MAX_DESC_LEN})")
            )
        if len(desc) < 30:
            issues.append(
                (
                    "warning",
                    f"Description very short ({len(desc)} chars) — may not trigger well",
                )
            )

    return issues


def check_body(body, skill_dir):
    issues = []
    lines = body.split("\n")

    if len(lines) > MAX_BODY_LINES:
        issues.append(
            ("warning", f"Body has {len(lines)} lines (guideline: <{MAX_BODY_LINES})")
        )

    todo_lines = [
        (i + 1, line.strip()) for i, line in enumerate(lines) if "[TODO" in line
    ]
    if todo_lines:
        issues.append(
            ("warning", f"{len(todo_lines)} unfilled [TODO] placeholder(s) in body")
        )
        for lineno, text in todo_lines[:3]:
            issues.append(("info", f"  Line {lineno}: {text[:80]}"))

    # Skip backtick-wrapped example paths and code blocks
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        for m in re.finditer(
            r"(?:\.\./)*(scripts|references|assets)/[^\s\)\"'`]+", line
        ):
            ref = m.group(0)
            pre = line[: m.start()]
            if pre.count("`") % 2 == 1:
                continue
            ref = ref.rstrip(".,;:)")
            if not ref or ref.endswith("/"):
                continue
            # Strip markdown anchor fragments (#section) and trailing ](...) artifacts
            ref = re.split(r"[#\]]", ref)[0]
            if not ref:
                continue
            ref_path = (skill_dir / ref).resolve()
            if not ref_path.exists():
                issues.append(("error", f"Referenced file missing: {ref}"))

    return issues


def check_orphaned_files(skill_dir, body):
    issues = []
    resource_dirs = ["scripts", "references", "assets"]
    body_lower = body.lower()

    for rdir in resource_dirs:
        dir_path = skill_dir / rdir
        if not dir_path.is_dir():
            continue
        for fpath in dir_path.rglob("*"):
            if fpath.is_file() and not fpath.name.startswith("."):
                rel = str(fpath.relative_to(skill_dir))
                if (
                    fpath.name.lower() not in body_lower
                    and rel.lower() not in body_lower
                ):
                    issues.append(("info", f"Unreferenced file: {rel}"))

    return issues


def check_structure(skill_dir):
    issues = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        issues.append(("error", "SKILL.md not found"))
        return issues

    bad_docs = [
        "README.md",
        "CHANGELOG.md",
        "INSTALLATION_GUIDE.md",
        "QUICK_REFERENCE.md",
    ]
    for bad in bad_docs:
        if (skill_dir / bad).exists():
            issues.append(
                ("warning", f"Extraneous doc file: {bad} (should not exist in skills)")
            )

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for script in scripts_dir.glob("*.py"):
            if not os.access(script, os.X_OK):
                issues.append(("info", f"Script not executable: {script.name}"))

    return issues


def auto_fix(skill_dir, issues):
    fixes = []
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for script in scripts_dir.glob("*.py"):
            if not os.access(script, os.X_OK):
                script.chmod(0o755)
                fixes.append(f"Fixed permissions on {script.name}")
    return fixes


def validate_skill(skill_path, do_fix=False):
    skill_dir = Path(skill_path).resolve()
    all_issues = []

    struct_issues = check_structure(skill_dir)
    all_issues.extend(struct_issues)
    if any(sev == "error" for sev, _ in struct_issues):
        return False, all_issues, []

    skill_md = skill_dir / "SKILL.md"
    fm, body, fm_error = extract_frontmatter(skill_md)
    if fm_error:
        all_issues.append(("error", fm_error))
        return False, all_issues, []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(check_frontmatter, fm): "frontmatter",
            executor.submit(check_body, body, skill_dir): "body",
            executor.submit(check_orphaned_files, skill_dir, body): "orphans",
        }
        for future in as_completed(futures):
            label = futures[future]
            try:
                all_issues.extend(future.result())
            except Exception as e:
                all_issues.append(("error", f"Check '{label}' failed: {e}"))

    fixes = auto_fix(skill_dir, all_issues) if do_fix else []

    has_errors = any(sev == "error" for sev, _ in all_issues)
    return not has_errors, all_issues, fixes


def format_human(passed, issues, fixes, skill_path):
    lines = [f"# Skill Validation: {Path(skill_path).name}", ""]

    if passed:
        lines.append("✅ PASSED")
    else:
        lines.append("❌ FAILED")

    for sev in ("error", "warning", "info"):
        sev_issues = [(s, m) for s, m in issues if s == sev]
        if sev_issues:
            icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[sev]
            lines.append(f"\n## {sev.upper()}S ({len(sev_issues)})")
            for _, msg in sev_issues:
                lines.append(f"  {icon} {msg}")

    if fixes:
        lines.append(f"\n## AUTO-FIXES ({len(fixes)})")
        for f in fixes:
            lines.append(f"  🔧 {f}")

    return "\n".join(lines)


def format_json(passed, issues, fixes, skill_path):
    return json.dumps(
        {
            "skill": Path(skill_path).name,
            "passed": passed,
            "errors": [m for s, m in issues if s == "error"],
            "warnings": [m for s, m in issues if s == "warning"],
            "info": [m for s, m in issues if s == "info"],
            "fixes": fixes,
        },
        indent=2,
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: skill-validator.py <skill-directory> [--fix] [--json]")
        sys.exit(1)

    skill_path = sys.argv[1]
    do_fix = "--fix" in sys.argv
    use_json = "--json" in sys.argv

    passed, issues, fixes = validate_skill(skill_path, do_fix)

    if use_json:
        print(format_json(passed, issues, fixes, skill_path))
    else:
        print(format_human(passed, issues, fixes, skill_path))

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
