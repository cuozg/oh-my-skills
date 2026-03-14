#!/usr/bin/env python3
import sys
import os
import re
from datetime import datetime, timedelta


def validate_doc(filepath):
    errors = []

    if not os.path.exists(filepath):
        print(f"❌ FAIL: {filepath}\n  - File not found")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    required_sections = [
        "### 1. Overview",
        "### 2. Architecture",
        "### 3. Public API",
        "### 4. Decision Drivers",
        "### 5. Data Flow",
        "### 6. Extension Guide",
        "### 7. Dependencies",
        "### 8. Known Limitations",
    ]

    for sec in required_sections:
        if not re.search(r"^" + re.escape(sec), content, re.MULTILINE):
            errors.append(f"Missing section: {sec.replace('### ', '')}")

    owner = "Unknown"
    owner_match = re.search(r"- Owner:\s*(.+)", content)
    if (
        not owner_match
        or "{name}" in owner_match.group(1)
        or not owner_match.group(1).strip()
        or "{name or team}" in owner_match.group(1)
    ):
        errors.append("Owner unassigned")
    else:
        owner = owner_match.group(1).strip()

    review_match = re.search(r"- Next Review Due:\s*(\d{4}-\d{2}-\d{2})", content)
    review_due = "Unknown"
    if not review_match:
        errors.append("Missing or invalid Next Review Due date (Expected YYYY-MM-DD)")
    else:
        review_due = review_match.group(1)
        try:
            review_date = datetime.strptime(review_due, "%Y-%m-%d")
            if review_date < datetime.now():
                errors.append(f"Review date is in the past ({review_due})")
            if review_date > datetime.now() + timedelta(days=100):
                errors.append(f"Review date is too far in the future (>90 days)")
        except ValueError:
            errors.append(f"Invalid Next Review Due date format ({review_due})")

    mermaid_blocks = re.findall(r"```mermaid(.*?)```", content, re.DOTALL)
    if len(mermaid_blocks) < 2:
        errors.append(
            "Missing required Mermaid diagrams (Expected at least Architecture and Data Flow)"
        )

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
            errors.append(
                f"Mermaid diagram {i + 1} missing valid diagram type or has syntax error"
            )

    citation_pattern = re.compile(r"\([\w\.\-]+\.\w+:\d+\)")
    claims_missing = []
    claims_found = 0

    in_claim_section = False
    for i, line in enumerate(lines):
        if re.match(r"^### [3467]\.", line):
            in_claim_section = True
        elif re.match(r"^### \d\.", line) or re.match(r"^## ", line):
            in_claim_section = False

        if in_claim_section:
            clean_line = line.strip()
            if (
                clean_line.startswith("|")
                and not "---" in clean_line
                and not "Signature" in clean_line
                and not "Location" in clean_line
                and not "Evidence" in clean_line
                and clean_line != "|"
            ):
                if citation_pattern.search(line):
                    claims_found += 1
                else:
                    claims_missing.append(i + 1)
            elif clean_line.startswith("- ") and "**" in clean_line:
                if citation_pattern.search(line):
                    claims_found += 1
                else:
                    claims_missing.append(i + 1)

    if claims_missing:
        errors.append(
            f"{len(claims_missing)} claims missing file:line citations (lines {', '.join(map(str, claims_missing))})"
        )

    content_no_checklist = content.replace("No TODO/TBD/FIXME", "")
    if re.search(r"\b(TODO|TBD|FIXME)\b", content_no_checklist):
        errors.append("Document contains TODO, TBD, or FIXME tags")

    if errors:
        print(f"❌ FAIL: {os.path.basename(filepath)}")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(f"✅ PASS: {os.path.basename(filepath)}")
        print(f"  - All 8 sections present")
        print(f"  - {claims_found} claims cited with file:line")
        print(f"  - Mermaid diagrams valid")
        print(f"  - Owner: {owner}")
        print(f"  - Review due: {review_due}")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_system_doc.py <path_to_doc.md>")
        sys.exit(1)
    success = validate_doc(sys.argv[1])
    sys.exit(0 if success else 1)
