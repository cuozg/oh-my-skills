#!/usr/bin/env python3
"""Validate Game Design Specification documents.

Supports three modes:
  - Feature spec: validate a single FEATURE_NAME.md
  - Index: validate _INDEX.md and check referenced feature files exist
  - Batch: validate all .md files in a Docs/Specs/ directory
"""

import sys
import os
import re
import glob as globmod


def validate_feature_spec(filepath):
    """Validate a per-feature spec file."""
    errors = []

    if not os.path.exists(filepath):
        print(f"FAIL: {filepath}\n  - File not found")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    filename = os.path.basename(filepath)

    # Check minimum length
    if len(lines) < 30:
        errors.append(f"Document too short ({len(lines)} lines, expected >30)")

    # Check mandatory sections (1-6 are required; 7-10 are conditional)
    mandatory_sections = [
        ("## 1. Overview", "Overview"),
        ("## 2. Core Mechanics", "Core Mechanics"),
        ("## 3. Systems Design", "Systems Design"),
        ("## 4. Data Model", "Data Model"),
        ("## 5. UX/UI Flows", "UX/UI Flows"),
        ("## 6. Dependencies & Integration", "Dependencies & Integration"),
    ]

    sections_found = 0
    for pattern, name in mandatory_sections:
        if re.search(r"^" + re.escape(pattern), content, re.MULTILINE):
            sections_found += 1
        else:
            errors.append(f"Missing mandatory section: {name}")

    # Check at least 1 Mermaid diagram
    mermaid_blocks = re.findall(r"```mermaid(.*?)```", content, re.DOTALL)
    mermaid_count = len(mermaid_blocks)
    if mermaid_count < 1:
        errors.append(
            f"No Mermaid diagrams found (minimum 1 required for feature spec)"
        )

    # Validate Mermaid diagram types
    valid_types = [
        "classDiagram",
        "sequenceDiagram",
        "flowchart",
        "graph",
        "stateDiagram",
        "erDiagram",
        "gantt",
        "pie",
    ]
    for i, block in enumerate(mermaid_blocks):
        block_lines = block.strip().split("\n")
        has_type = any(any(t in line for t in valid_types) for line in block_lines[:3])
        if not has_type:
            errors.append(
                f"Mermaid diagram {i + 1} missing valid diagram type declaration"
            )

    # Check for forbidden text (exclude validation checklist)
    content_no_checklist = re.sub(
        r"## Validation Checklist.*", "", content, flags=re.DOTALL
    )
    if re.search(r"\b(TODO|TBD|FIXME)\b", content_no_checklist):
        errors.append("Document contains TODO, TBD, or FIXME tags")

    # Check overview metadata fields
    overview_fields = {
        "Feature": r"\*\*Feature\*\*:\s*\S+",
        "Status": r"\*\*Status\*\*:\s*(Draft|Review|Approved)",
    }
    for field, pattern in overview_fields.items():
        if not re.search(pattern, content):
            errors.append(f"Overview missing or empty: {field}")

    # Check for unfilled placeholders
    placeholder_count = len(re.findall(r"\{[a-z_]+\}", content))
    if placeholder_count > 0:
        errors.append(
            f"{placeholder_count} unfilled placeholders remain (e.g. {{placeholder}})"
        )

    # Check for summary sentence
    if not re.search(r"\*\*Summary\*\*:", content):
        errors.append("Missing Summary field in Overview section")

    # Report results
    if errors:
        print(f"FAIL: {filename}")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(f"PASS: {filename}")
        print(f"  - {sections_found} mandatory sections present")
        print(f"  - {mermaid_count} Mermaid diagram(s) found")
        print(f"  - No forbidden text (TODO/TBD/FIXME)")
        print(f"  - Overview metadata valid")
        return True


def validate_index(filepath):
    """Validate the _INDEX.md game overview document."""
    errors = []

    if not os.path.exists(filepath):
        print(f"FAIL: {filepath}\n  - File not found")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    # Check minimum length
    if len(lines) < 40:
        errors.append(f"Index too short ({len(lines)} lines, expected >40)")

    # Check mandatory sections
    mandatory_sections = [
        "## Metadata",
        "## Game Overview",
        "## Feature Map",
        "## Primary Gameplay Loop",
        "## Platform Targets",
        "## Risks & Mitigations",
    ]

    sections_found = 0
    for sec in mandatory_sections:
        if re.search(r"^" + re.escape(sec), content, re.MULTILINE):
            sections_found += 1
        else:
            errors.append(f"Missing section: {sec.replace('## ', '')}")

    # Check for at least 1 Mermaid diagram (gameplay loop)
    mermaid_blocks = re.findall(r"```mermaid(.*?)```", content, re.DOTALL)
    if len(mermaid_blocks) < 1:
        errors.append("No Mermaid diagrams found (gameplay loop required)")

    # Check metadata fields
    metadata_fields = {
        "Title": r"\*\*Title\*\*:\s*\S+",
        "Version": r"\*\*Version\*\*:\s*\S+",
        "Date": r"\*\*Date\*\*:\s*\S+",
        "Status": r"\*\*Status\*\*:\s*(Draft|Review|Approved)",
    }
    for field, pattern in metadata_fields.items():
        if not re.search(pattern, content):
            errors.append(f"Metadata missing or empty: {field}")

    # Check feature map references
    spec_dir = os.path.dirname(filepath)
    feature_links = re.findall(r"\[([^\]]+\.md)\]\(([^\)]+\.md)\)", content)
    missing_features = []
    for display, link in feature_links:
        feature_path = os.path.join(spec_dir, link)
        if not os.path.exists(feature_path):
            missing_features.append(link)
    if missing_features:
        errors.append(
            f"Feature Map references missing files: {', '.join(missing_features)}"
        )

    # Check for forbidden text
    content_no_checklist = re.sub(
        r"## Validation Checklist.*", "", content, flags=re.DOTALL
    )
    if re.search(r"\b(TODO|TBD|FIXME)\b", content_no_checklist):
        errors.append("Document contains TODO, TBD, or FIXME tags")

    # Check for unfilled placeholders
    placeholder_count = len(re.findall(r"\{[a-z_]+\}", content))
    if placeholder_count > 0:
        errors.append(
            f"{placeholder_count} unfilled placeholders remain (e.g. {{placeholder}})"
        )

    # Report
    if errors:
        print(f"FAIL: {os.path.basename(filepath)}")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(f"PASS: {os.path.basename(filepath)}")
        print(f"  - {sections_found} mandatory sections present")
        print(f"  - {len(mermaid_blocks)} Mermaid diagram(s)")
        print(f"  - {len(feature_links)} feature file(s) referenced")
        if feature_links:
            print(f"  - All referenced feature files exist")
        return True


def validate_batch(dirpath):
    """Validate all spec files in a directory."""
    if not os.path.isdir(dirpath):
        print(f"FAIL: {dirpath} is not a directory")
        return False

    md_files = sorted(globmod.glob(os.path.join(dirpath, "*.md")))
    if not md_files:
        print(f"FAIL: No .md files found in {dirpath}")
        return False

    results = {}
    for fpath in md_files:
        fname = os.path.basename(fpath)
        if fname == "_INDEX.md":
            results[fname] = validate_index(fpath)
        else:
            results[fname] = validate_feature_spec(fpath)
        print()  # blank line between files

    # Summary
    passed = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)
    total = len(results)

    print("=" * 50)
    print(f"SUMMARY: {passed}/{total} passed, {failed}/{total} failed")
    for fname, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {fname}")

    return failed == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_spec.py <path>")
        print()
        print("  <path> can be:")
        print("    - A single .md file (feature spec or _INDEX.md)")
        print("    - A directory (validates all .md files inside)")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isdir(target):
        success = validate_batch(target)
    elif os.path.basename(target) == "_INDEX.md":
        success = validate_index(target)
    else:
        success = validate_feature_spec(target)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
