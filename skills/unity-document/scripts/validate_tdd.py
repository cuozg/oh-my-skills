#!/usr/bin/env python3
"""Validate a Technical Design Document against the mandatory TDD template."""

import sys
import os
import re


def validate_tdd(filepath):
    errors = []

    if not os.path.exists(filepath):
        print(f"\u274c FAIL: {filepath}\n  - File not found")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Required sections (header variations accepted)
    required_sections = {
        "Problem": r"^##\s+Problem",
        "Goals": r"^##\s+Goals",
        "Non-Goals": r"^##\s+Non[- ]Goals",
        "Design": r"^##\s+Design",
        "Alternatives Considered": r"^##\s+Alternatives",
        "Dependencies": r"^##\s+Dependencies",
        "Risks": r"^##\s+Risks",
        "Open Questions": r"^##\s+Open\s+Questions",
    }

    found_sections = []
    for name, pattern in required_sections.items():
        if re.search(pattern, content, re.MULTILINE):
            found_sections.append(name)
        else:
            errors.append(f"Missing section: {name}")

    # Check for Components table in Design section
    design_match = re.search(
        r"^##\s+Design(.*?)(?=^##\s+[A-Z]|\Z)", content, re.DOTALL | re.MULTILINE
    )
    if design_match:
        design_content = design_match.group(1)
        if not re.search(
            r"\|\s*Component\s*\|.*Responsibility", design_content, re.IGNORECASE
        ):
            errors.append("Design section missing Components table")
    else:
        errors.append("Design section not found for Components table check")

    # Check for Mermaid diagram (at least 1)
    mermaid_blocks = re.findall(r"```mermaid(.*?)```", content, re.DOTALL)
    if len(mermaid_blocks) < 1:
        errors.append("Missing required Mermaid diagram (at least 1 required)")

    for i, block in enumerate(mermaid_blocks):
        lines_in_block = block.strip().split("\n")
        valid_types = [
            "classDiagram",
            "sequenceDiagram",
            "flowchart",
            "graph",
            "stateDiagram",
        ]
        has_type = any(any(t in l for t in valid_types) for l in lines_in_block[:2])
        if not has_type:
            errors.append(f"Mermaid diagram {i + 1} missing valid diagram type")

    # Check Alternatives table has at least 2 data rows
    alt_match = re.search(
        r"^##\s+Alternatives(.*?)(?=^##\s+[A-Z]|\Z)", content, re.DOTALL | re.MULTILINE
    )
    if alt_match:
        alt_content = alt_match.group(1)
        table_rows = re.findall(r"^\|[^-].*\|", alt_content, re.MULTILINE)
        # Filter header rows
        data_rows = [
            r
            for r in table_rows
            if "Option" not in r and "Pros" not in r and "---" not in r
        ]
        if len(data_rows) < 2:
            errors.append(
                f"Alternatives table needs at least 2 options (found {len(data_rows)})"
            )
    else:
        errors.append("Alternatives section not found for table check")

    # Check Risks table has likelihood/impact
    risk_match = re.search(
        r"^##\s+Risks(.*?)(?=^##\s+[A-Z]|\Z)", content, re.DOTALL | re.MULTILINE
    )
    if risk_match:
        risk_content = risk_match.group(1)
        has_header = bool(
            re.search(r"\|\s*Risk\s*\|.*Likelihood", risk_content, re.IGNORECASE)
        ) or bool(re.search(r"\|\s*Risk\s*\|.*Impact", risk_content, re.IGNORECASE))
        has_data = bool(re.search(r"\b[HML]\b", risk_content))
        if not (has_header or has_data):
            errors.append("Risks table missing likelihood/impact ratings")

    # Check Dependencies table has file:line evidence
    dep_match = re.search(
        r"^##\s+Dependencies(.*?)(?=^##\s+[A-Z]|\Z)", content, re.DOTALL | re.MULTILINE
    )
    if dep_match:
        dep_content = dep_match.group(1)
        citation_pattern = re.compile(r"[\w\.\-]+\.\w+:\d+")
        if not citation_pattern.search(dep_content):
            errors.append("Dependencies section missing file:line evidence")

    # No TODO/TBD/FIXME
    content_clean = content.replace("No TODO/TBD/FIXME", "")
    if re.search(r"\b(TODO|TBD|FIXME)\b", content_clean):
        errors.append("Document contains TODO, TBD, or FIXME tags")

    # Check Date and Status metadata
    if not re.search(r"\*\*Date\*\*:\s*\d{4}-\d{2}-\d{2}", content):
        errors.append("Missing Date metadata (Expected **Date**: YYYY-MM-DD)")

    if not re.search(r"\*\*Status\*\*:\s*(Draft|Review|Approved)", content):
        errors.append("Missing Status metadata (Expected Draft, Review, or Approved)")

    if errors:
        print(f"\u274c FAIL: {os.path.basename(filepath)}")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(f"\u2705 PASS: {os.path.basename(filepath)}")
        print(f"  - All {len(found_sections)} sections present")
        print(f"  - {len(mermaid_blocks)} Mermaid diagram(s)")
        print(f"  - Alternatives table validated")
        print(f"  - No forbidden tags")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_tdd.py <path_to_tdd.md>")
        sys.exit(1)
    success = validate_tdd(sys.argv[1])
    sys.exit(0 if success else 1)
