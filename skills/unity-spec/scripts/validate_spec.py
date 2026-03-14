#!/usr/bin/env python3
"""Validate a Game Design Specification document against the GDD template."""

import sys
import os
import re


def validate_spec(filepath):
    errors = []

    if not os.path.exists(filepath):
        print(f"FAIL: {filepath}\n  - File not found")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    # Check minimum length
    if len(lines) < 50:
        errors.append(f"Document too short ({len(lines)} lines, expected >50)")

    # Check mandatory sections (1-12; section 13 is optional)
    mandatory_sections = [
        "## 1. Metadata",
        "## 2. Game Overview",
        "## 3. Core Mechanics",
        "## 4. Systems Design",
        "## 5. Progression",
        "## 6. Content",
        "## 7. UX/UI Flows",
        "## 8. Art Direction",
        "## 9. Audio",
        "## 10. Technical Constraints",
        "## 11. Platform Targets",
        "## 12. Risks & Mitigations",
    ]

    sections_found = 0
    for sec in mandatory_sections:
        if re.search(r"^" + re.escape(sec), content, re.MULTILINE):
            sections_found += 1
        else:
            errors.append(f"Missing section: {sec.replace('## ', '')}")

    # Check Mermaid diagrams (minimum 3 for full GDD)
    mermaid_blocks = re.findall(r"```mermaid(.*?)```", content, re.DOTALL)
    mermaid_count = len(mermaid_blocks)
    if mermaid_count < 3:
        errors.append(
            f"Insufficient Mermaid diagrams ({mermaid_count} found, minimum 3 required)"
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

    # Check for forbidden text
    content_no_checklist = re.sub(
        r"## Validation Checklist.*", "", content, flags=re.DOTALL
    )
    if re.search(r"\b(TODO|TBD|FIXME)\b", content_no_checklist):
        errors.append("Document contains TODO, TBD, or FIXME tags")

    # Check metadata fields
    metadata_fields = {
        "Title": r"\*\*Title:\*\*\s*\S+",
        "Version": r"\*\*Version:\*\*\s*\S+",
        "Date": r"\*\*Date:\*\*\s*\S+",
        "Status": r"\*\*Status:\*\*\s*(Draft|Review|Approved)",
    }
    for field, pattern in metadata_fields.items():
        if not re.search(pattern, content):
            errors.append(f"Metadata missing or empty: {field}")

    # Check for unfilled placeholders
    placeholder_count = len(re.findall(r"\{[a-z_]+\}", content))
    if placeholder_count > 0:
        errors.append(
            f"{placeholder_count} unfilled placeholders remain (e.g. {{placeholder}})"
        )

    # Report results
    if errors:
        print(f"FAIL: {os.path.basename(filepath)}")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(f"PASS: {os.path.basename(filepath)}")
        print(f"  - All {sections_found} mandatory sections present")
        print(f"  - {mermaid_count} Mermaid diagrams found")
        print(f"  - No forbidden text (TODO/TBD/FIXME)")
        print(f"  - Metadata fields valid")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_spec.py <path_to_spec.md>")
        sys.exit(1)
    success = validate_spec(sys.argv[1])
    sys.exit(0 if success else 1)
