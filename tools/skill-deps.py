#!/usr/bin/env python3
"""
Skill Deps - Analyze skill dependencies and asset integration points.

Scans a skill directory to build a dependency graph:
  - Scripts that import other modules
  - SKILL.md references to other skills (load_skills, skill paths)
  - Asset references (file paths mentioned in SKILL.md/scripts)
  - Cross-skill dependencies (skills referencing each other)
  - Missing dependencies detected in single pass

Usage:
    python skill-deps.py <skill-path> [--skills-root <root>] [--json]

Examples:
    python skill-deps.py .opencode/skills/unity/unity-code
    python skill-deps.py .opencode/skills/other/skill-creator --skills-root .opencode/skills --json
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


# ---------------------------------------------------------------------------
# Dependency extraction
# ---------------------------------------------------------------------------


def extract_python_imports(file_path):
    """Extract import targets from a Python file."""
    imports = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(
            r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", content, re.MULTILINE
        ):
            module = match.group(1) or match.group(2)
            imports.append(
                {"module": module, "file": str(file_path.name), "type": "python_import"}
            )
    except Exception:
        pass
    return imports


def extract_bash_sources(file_path):
    """Extract sourced files from a bash script."""
    sources = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(
            r"^\s*(?:source|\.)\s+[\"']?([^\s\"']+)", content, re.MULTILINE
        ):
            sources.append(
                {
                    "path": match.group(1),
                    "file": str(file_path.name),
                    "type": "bash_source",
                }
            )
    except Exception:
        pass
    return sources


def extract_skill_references(content):
    """Extract references to other skills from SKILL.md or script content."""
    refs = []

    skill_path_pattern = re.findall(
        r"(?:skills/|load_skills\s*=\s*\[)[\"']?([\w/-]+)[\"']?", content
    )
    for ref in skill_path_pattern:
        if "/" in ref and not ref.startswith("http"):
            refs.append({"skill": ref, "type": "skill_reference"})

    load_skills = re.findall(r"load_skills\s*=\s*\[(.*?)\]", content, re.DOTALL)
    for match in load_skills:
        for skill in re.findall(r'["\']([^"\']+)["\']', match):
            refs.append({"skill": skill, "type": "load_skills"})

    return refs


def extract_file_references(content, skill_dir):
    """Extract file path references and check existence."""
    refs = []
    patterns = [
        r'(?:scripts|references|assets)/[^\s\)\]"\'`>,{}]+',
        r'\.opencode/[^\s\)\]"\'`>,{}]+',
        r'Assets/[^\s\)\]"\'`>,{}]+',
    ]
    seen = set()
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            path_str = match.group(0).rstrip(".")
            # Skip directory-only references (ending with /)
            if path_str.endswith("/"):
                continue
            if path_str in seen:
                continue
            seen.add(path_str)
            full_path = skill_dir / path_str
            refs.append(
                {
                    "path": path_str,
                    "exists": full_path.exists(),
                    "type": "file_reference",
                }
            )
    return refs


# ---------------------------------------------------------------------------
# Dependency graph builder
# ---------------------------------------------------------------------------


def analyze_skill(skill_path, skills_root=None):
    """Build complete dependency graph for a skill."""
    skill_dir = Path(skill_path).resolve()

    if not skill_dir.is_dir():
        return {"error": f"Not a directory: {skill_dir}"}

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {"error": f"SKILL.md not found in {skill_dir}"}

    skill_name = skill_dir.name
    result = {
        "skill": skill_name,
        "path": str(skill_dir),
        "script_deps": [],
        "skill_refs": [],
        "file_refs": [],
        "missing": [],
        "summary": {},
    }

    all_content = ""

    try:
        md_content = skill_md.read_text(encoding="utf-8", errors="replace")
        all_content += md_content
    except Exception as e:
        return {"error": f"Cannot read SKILL.md: {e}"}

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {}

        scripts_dir = skill_dir / "scripts"
        if scripts_dir.is_dir():
            for script in scripts_dir.rglob("*"):
                if script.is_file() and not script.name.startswith("."):
                    if script.suffix == ".py":
                        futures[executor.submit(extract_python_imports, script)] = (
                            "py_import"
                        )
                    elif script.suffix in (".sh", ".bash"):
                        futures[executor.submit(extract_bash_sources, script)] = (
                            "bash_source"
                        )
                    try:
                        script_content = script.read_text(
                            encoding="utf-8", errors="replace"
                        )
                        all_content += "\n" + script_content
                    except Exception:
                        pass

        refs_dir = skill_dir / "references"
        if refs_dir.is_dir():
            for ref_file in refs_dir.rglob("*.md"):
                try:
                    ref_content = ref_file.read_text(encoding="utf-8", errors="replace")
                    all_content += "\n" + ref_content
                except Exception:
                    pass

        futures[executor.submit(extract_skill_references, all_content)] = "skill_ref"
        futures[executor.submit(extract_file_references, all_content, skill_dir)] = (
            "file_ref"
        )

        for future in as_completed(futures):
            label = futures[future]
            try:
                items = future.result()
                if label in ("py_import", "bash_source"):
                    result["script_deps"].extend(items)
                elif label == "skill_ref":
                    result["skill_refs"].extend(items)
                elif label == "file_ref":
                    result["file_refs"].extend(items)
            except Exception:
                pass

    seen_skills = set()
    unique_skill_refs = []
    for ref in result["skill_refs"]:
        key = ref["skill"]
        if key not in seen_skills:
            seen_skills.add(key)
            unique_skill_refs.append(ref)
    result["skill_refs"] = unique_skill_refs

    missing = []
    for ref in result["file_refs"]:
        if not ref["exists"]:
            missing.append(ref["path"])

    if skills_root:
        root = Path(skills_root).resolve()
        if root.is_dir():
            for ref in result["skill_refs"]:
                parts = ref["skill"].split("/")
                if len(parts) >= 2:
                    candidate = root / parts[0] / parts[1] / "SKILL.md"
                    if not candidate.exists():
                        candidate = root / ref["skill"] / "SKILL.md"
                    if not candidate.exists():
                        missing.append(f"skill:{ref['skill']}")

    result["missing"] = missing

    stdlib_modules = {
        "sys",
        "os",
        "re",
        "json",
        "yaml",
        "pathlib",
        "argparse",
        "subprocess",
        "typing",
        "collections",
        "datetime",
        "zipfile",
        "shutil",
        "io",
        "concurrent",
        "threading",
        "multiprocessing",
        "functools",
        "itertools",
        "textwrap",
        "hashlib",
        "math",
        "copy",
        "tempfile",
        "glob",
        "unittest",
    }
    external_deps = [
        d
        for d in result["script_deps"]
        if d["module"].split(".")[0] not in stdlib_modules
    ]

    result["summary"] = {
        "total_script_imports": len(result["script_deps"]),
        "external_dependencies": len(external_deps),
        "skill_references": len(result["skill_refs"]),
        "file_references": len(result["file_refs"]),
        "missing_count": len(missing),
        "status": "clean" if not missing else "has_missing",
    }
    if external_deps:
        result["summary"]["external_modules"] = list(
            {d["module"].split(".")[0] for d in external_deps}
        )

    return result


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------


def format_human(report):
    """Human-readable output."""
    if "error" in report:
        return f"❌ {report['error']}"

    lines = [f"# Dependency Report: {report['skill']}", ""]

    summary = report["summary"]
    status_icon = "✅" if summary["status"] == "clean" else "⚠️"
    lines.append(f"Status: {status_icon} {summary['status']}")
    lines.append(
        f"Script imports: {summary['total_script_imports']} ({summary['external_dependencies']} external)"
    )
    lines.append(f"Skill references: {summary['skill_references']}")
    lines.append(f"File references: {summary['file_references']}")
    lines.append(f"Missing: {summary['missing_count']}")

    if summary.get("external_modules"):
        lines.append(f"\n## External Modules")
        for mod in summary["external_modules"]:
            lines.append(f"  • {mod}")

    if report["skill_refs"]:
        lines.append(f"\n## Skill References")
        for ref in report["skill_refs"]:
            lines.append(f"  • {ref['skill']} ({ref['type']})")

    if report["missing"]:
        lines.append(f"\n## Missing Dependencies")
        for m in report["missing"]:
            lines.append(f"  ❌ {m}")

    if report["script_deps"]:
        lines.append(f"\n## Script Imports")
        for dep in report["script_deps"][:20]:
            lines.append(f"  • {dep['file']}: {dep['module']}")
        if len(report["script_deps"]) > 20:
            lines.append(f"  ... and {len(report['script_deps']) - 20} more")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Analyze skill dependencies and integration points"
    )
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument(
        "--skills-root",
        default=None,
        help="Root skills directory for cross-skill validation",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    report = analyze_skill(args.skill_path, args.skills_root)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(format_human(report))

    if "error" in report or report.get("summary", {}).get("missing_count", 0) > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
