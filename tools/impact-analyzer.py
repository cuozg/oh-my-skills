#!/usr/bin/env python3
"""
Impact Analyzer - Trace C# class references across a Unity project.

Given a file path or class name, finds all files that reference it,
categorizes references (singleton access, inheritance, type usage),
and produces a blast-radius report.

Usage:
  impact-analyzer.py <target> <scripts_dir> [--depth N] [--scope subdir]

  target:      C# file path or class name
  scripts_dir: Root scripts directory (e.g., Assets/Scripts)
  --depth N:   1 = direct only, 2 = direct + transitive (default: 1)
  --scope:     Subdirectory to limit search (relative to scripts_dir)
"""

import sys
import os
import re
from pathlib import Path
from collections import defaultdict


def find_class_file(class_name, scripts_dir):
    """Find the .cs file defining a class by name."""
    pattern = re.compile(
        rf"(?:class|struct|interface|enum)\s+{re.escape(class_name)}\b"
    )
    for root, dirs, files in os.walk(scripts_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if not f.endswith(".cs"):
                continue
            filepath = Path(root) / f
            try:
                content = filepath.read_text(encoding="utf-8", errors="replace")
                if pattern.search(content):
                    return filepath
            except Exception:
                continue
    return None


def extract_class_info(filepath):
    """Extract class name, base class, and interfaces from a C# file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    info = {
        "file": str(filepath),
        "class_name": None,
        "base_class": None,
        "interfaces": [],
        "is_singleton": False,
        "singleton_type": None,
    }

    # Regex: match class decl with optional generics and inheritance list
    class_match = re.search(
        r"(?:public\s+|internal\s+|abstract\s+|sealed\s+|partial\s+|static\s+)*"
        r"class\s+(\w+)"
        r"(?:\s*<[^>]*>)?"
        r"(?:\s*:\s*(.+?))?(?:\s*\{|\s*where\b)",
        content,
    )

    if class_match:
        info["class_name"] = class_match.group(1)
        if class_match.group(2):
            bases = [b.strip() for b in class_match.group(2).split(",")]
            if bases:
                first = bases[0]
                if first.startswith("I") and first[1:2].isupper():
                    info["interfaces"] = bases
                else:
                    info["base_class"] = first
                    info["interfaces"] = bases[1:]

        singleton_match = re.search(r"Singleton<(\w+)>", content)
        if singleton_match:
            info["is_singleton"] = True
            info["singleton_type"] = singleton_match.group(1)

    return info


def find_references(class_name, scripts_dir, exclude_file=None, scope=None):
    """Find all files referencing a class name."""
    search_dir = scripts_dir
    if scope:
        search_dir = scripts_dir / scope

    if not search_dir.exists():
        return {}

    references = defaultdict(list)
    # Patterns to search for
    patterns = [
        re.compile(re.escape(class_name) + r"(?:\s|\.|\(|<|,|\)|\[|\]|;)"),
    ]

    for root, dirs, files in os.walk(search_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if not f.endswith(".cs"):
                continue
            filepath = Path(root) / f
            if exclude_file and filepath.resolve() == exclude_file.resolve():
                continue

            try:
                lines = filepath.read_text(
                    encoding="utf-8", errors="replace"
                ).splitlines()
            except Exception:
                continue

            file_refs = []
            for line_num, line in enumerate(lines, 1):
                for pattern in patterns:
                    if pattern.search(line):
                        file_refs.append({"line": line_num, "text": line.strip()[:120]})
                        break  # one match per line is enough

            if file_refs:
                rel_path = str(filepath)
                references[rel_path] = file_refs

    return references


def categorize_reference(line_text, class_name):
    """Categorize a reference line."""
    text = line_text

    # Singleton instance access
    if f"{class_name}.Instance" in text:
        if f"{class_name}.HasInstance" in text:
            return "HasInstance check"
        return "Singleton access"

    # Inheritance
    if re.search(rf":\s*.*{re.escape(class_name)}", text):
        return "Inheritance"

    # Generic type parameter
    if re.search(rf"<.*{re.escape(class_name)}.*>", text):
        return "Generic type param"

    # Method parameter or variable type
    if re.search(rf"\b{re.escape(class_name)}\s+\w+", text):
        return "Type reference"

    # Cast or typeof
    if re.search(rf"(as|is|\btypeof\b)\s*\(?\s*{re.escape(class_name)}", text):
        return "Type check/cast"

    # Using/import (rare in this codebase since no namespaces)
    if text.strip().startswith("using"):
        return "Using directive"

    # Comment
    if text.strip().startswith("//") or text.strip().startswith("/*"):
        return "Comment"

    return "Other reference"


def assess_risk(total_refs, has_singleton, file_count):
    """Assess risk level based on reference count and patterns."""
    if has_singleton and file_count > 20:
        return (
            "HIGH",
            "Widely-used singleton — changes will cascade across many systems",
        )
    if file_count > 20:
        return "HIGH", f"{file_count} files reference this class — high blast radius"
    if file_count > 5:
        return (
            "MEDIUM",
            f"{file_count} files reference this class — moderate blast radius",
        )
    if file_count > 0:
        return (
            "LOW",
            f"Only {file_count} files reference this class — limited blast radius",
        )
    return "NONE", "No external references found — safe to modify"


def build_report(class_info, references, class_name, depth):
    """Build the markdown report."""
    report = []
    report.append(f"# Impact Analysis: {class_name}")

    # Target info
    report.append("\n## Target")
    report.append(f"  File: {class_info['file']}")
    report.append(f"  Class: {class_info['class_name']}")
    report.append(f"  Base class: {class_info['base_class'] or 'none'}")
    if class_info["interfaces"]:
        report.append(f"  Interfaces: {', '.join(class_info['interfaces'])}")
    else:
        report.append("  Interfaces: none")
    if class_info["is_singleton"]:
        report.append(f"  Singleton: Yes (Singleton<{class_info['singleton_type']}>)")

    # Categorize all references
    categories = defaultdict(list)
    total_ref_count = 0
    for filepath, refs in references.items():
        for ref in refs:
            cat = categorize_reference(ref["text"], class_name)
            categories[cat].append({"file": filepath, **ref})
            total_ref_count += 1

    # Direct references
    report.append(
        f"\n## Direct References ({len(references)} files, {total_ref_count} total)"
    )
    for filepath, refs in sorted(references.items()):
        report.append(f"  {filepath}")
        for ref in refs[:5]:  # limit lines per file
            cat = categorize_reference(ref["text"], class_name)
            report.append(f"    L{ref['line']:>4}: [{cat}] {ref['text']}")
        if len(refs) > 5:
            report.append(f"    ... and {len(refs) - 5} more references")

    # Category summary
    report.append(f"\n## Reference Categories")
    for cat, refs in sorted(categories.items(), key=lambda x: -len(x[1])):
        unique_files = len(set(r["file"] for r in refs))
        report.append(f"  {cat}: {len(refs)} refs across {unique_files} files")

    # Singleton access summary
    singleton_refs = categories.get("Singleton access", [])
    has_instance_refs = categories.get("HasInstance check", [])
    if singleton_refs or has_instance_refs:
        report.append(f"\n## Singleton Access Pattern")
        report.append(
            f"  .Instance access: {len(singleton_refs)} refs in "
            f"{len(set(r['file'] for r in singleton_refs))} files"
        )
        report.append(
            f"  .HasInstance checks: {len(has_instance_refs)} refs in "
            f"{len(set(r['file'] for r in has_instance_refs))} files"
        )

    # Inheritance
    inherit_refs = categories.get("Inheritance", [])
    if inherit_refs:
        report.append(f"\n## Inheritance ({len(inherit_refs)} subclasses)")
        for ref in inherit_refs:
            report.append(f"  {ref['file']} (line {ref['line']})")

    # Risk assessment
    risk_level, risk_reason = assess_risk(
        total_ref_count,
        class_info["is_singleton"],
        len(references),
    )
    report.append(f"\n## Risk Assessment")
    report.append(
        f"  Blast radius: {len(references)} files, {total_ref_count} references"
    )
    report.append(f"  Risk level: {risk_level}")
    report.append(f"  Reason: {risk_reason}")

    if risk_level == "HIGH":
        report.append(
            "  Recommendation: Create a detailed plan before modifying. "
            "Consider deprecation pattern for API changes."
        )
    elif risk_level == "MEDIUM":
        report.append(
            "  Recommendation: Review all referencing files. Run tests after changes."
        )
    elif risk_level == "LOW":
        report.append("  Recommendation: Standard review process is sufficient.")
    else:
        report.append("  Recommendation: Safe to modify freely.")

    return "\n".join(report)


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: impact-analyzer.py <target> <scripts_dir> [--depth N] [--scope subdir]"
        )
        print("  target:      C# file path or class name")
        print("  scripts_dir: Root scripts directory (e.g., Assets/Scripts)")
        sys.exit(1)

    target = sys.argv[1]
    scripts_dir = Path(sys.argv[2])

    # Parse optional args
    depth = 1
    scope = None
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--depth" and i + 1 < len(sys.argv):
            depth = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--scope" and i + 1 < len(sys.argv):
            scope = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    if not scripts_dir.exists():
        print(f"Scripts directory not found: {scripts_dir}")
        sys.exit(1)

    # Resolve target to file + class name
    target_file = None
    class_name = None

    if target.endswith(".cs"):
        # It's a file path
        target_path = Path(target)
        if not target_path.exists():
            # Try relative to CWD
            target_path = Path.cwd() / target
        if not target_path.exists():
            print(f"File not found: {target}")
            sys.exit(1)
        target_file = target_path
        info = extract_class_info(target_file)
        if info and info["class_name"]:
            class_name = info["class_name"]
        else:
            # Fallback: use filename without extension
            class_name = target_path.stem
    else:
        # It's a class name
        class_name = target
        target_file = find_class_file(class_name, scripts_dir)
        if not target_file:
            print(f"Could not find a file defining class: {class_name}")
            print("Searching for references anyway...")

    # Get class info
    if target_file:
        class_info = extract_class_info(target_file)
        if not class_info:
            class_info = {
                "file": str(target_file),
                "class_name": class_name,
                "base_class": None,
                "interfaces": [],
                "is_singleton": False,
                "singleton_type": None,
            }
    else:
        class_info = {
            "file": "(not found)",
            "class_name": class_name,
            "base_class": None,
            "interfaces": [],
            "is_singleton": False,
            "singleton_type": None,
        }

    # Find references
    references = find_references(class_name, scripts_dir, target_file, scope)

    # Depth 2: transitive references
    if depth >= 2 and references:
        transitive = {}
        for ref_file in list(references.keys()):
            ref_path = Path(ref_file)
            ref_info = extract_class_info(ref_path)
            if ref_info and ref_info["class_name"]:
                trans_refs = find_references(
                    ref_info["class_name"],
                    scripts_dir,
                    ref_path,
                    scope,
                )
                for k, v in trans_refs.items():
                    if k not in references and k not in transitive:
                        transitive[k] = v
        if transitive:
            for k, v in transitive.items():
                references[k] = v

    # Build and print report
    report = build_report(class_info, references, class_name, depth)
    print(report)


if __name__ == "__main__":
    main()
