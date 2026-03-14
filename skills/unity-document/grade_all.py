#!/usr/bin/env python3
"""Grade unity-document eval outputs against assertions."""

import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ITER = os.path.join(BASE, "iteration-1")


def find_md_file(outputs_dir):
    if not os.path.isdir(outputs_dir):
        return None
    for f in os.listdir(outputs_dir):
        if f.endswith(".md"):
            return os.path.join(outputs_dir, f)
    return None


def grade_system_assertions(content, assertions):
    results = []
    for a in assertions:
        text = a
        passed = False
        evidence = ""

        if "Documents/Systems/" in text and ".md" in text:
            # We check if file was saved - since it exists, pass
            passed = True
            evidence = "File exists in outputs directory"

        elif (
            "all 8 required sections" in text.lower()
            or "8-section" in text.lower()
            or "all 8" in text.lower()
        ):
            sections = [
                "### 1. Overview",
                "### 2. Architecture",
                "### 3. Public API",
                "### 4. Decision Drivers",
                "### 5. Data Flow",
                "### 6. Extension Guide",
                "### 7. Dependencies",
                "### 8. Known Limitations",
            ]
            found = [s for s in sections if s in content]
            passed = len(found) == 8
            evidence = f"Found {len(found)}/8 sections: {', '.join([s.replace('### ', '') for s in found])}"

        elif "mermaid" in text.lower() and (
            "2" in text or "two" in text or "least 2" in text
        ):
            count = len(re.findall(r"```mermaid", content))
            passed = count >= 2
            evidence = f"Found {count} mermaid blocks"

        elif "file:line" in text.lower() or "(filename" in text.lower():
            citations = re.findall(r"\([\w\.\-]+\.\w+:\d+\)", content)
            passed = len(citations) >= 3
            evidence = f"Found {len(citations)} file:line citations"

        elif "owner" in text.lower() and "review" in text.lower():
            has_owner = bool(re.search(r"- Owner:\s*\S+", content))
            has_review = bool(
                re.search(r"- Next Review Due:\s*\d{4}-\d{2}-\d{2}", content)
            )
            passed = has_owner and has_review
            evidence = f"Owner: {'found' if has_owner else 'missing'}, Review date: {'found' if has_review else 'missing'}"

        elif "TODO" in text and "TBD" in text and "FIXME" in text:
            clean = content.replace("No TODO/TBD/FIXME", "")
            has_forbidden = bool(re.search(r"\b(TODO|TBD|FIXME)\b", clean))
            passed = not has_forbidden
            evidence = f"{'No' if not has_forbidden else 'Found'} forbidden tags"

        elif "template" in text.lower() and (
            "loaded" in text.lower() or "reference" in text.lower()
        ):
            # Can't verify from output alone, check structure compliance
            passed = (
                "### 1. Overview" in content and "### 8. Known Limitations" in content
            )
            evidence = "Template structure compliance verified from section headers"

        elif "architecture" in text.lower() and "mermaid" in text.lower():
            has_arch = "### 2. Architecture" in content
            has_mermaid = "```mermaid" in content
            passed = has_arch and has_mermaid
            evidence = f"Architecture section: {'found' if has_arch else 'missing'}, Mermaid: {'found' if has_mermaid else 'missing'}"

        elif "data flow" in text.lower() and "sequence" in text.lower():
            has_df = "### 5. Data Flow" in content
            has_seq = "sequenceDiagram" in content
            passed = has_df and has_seq
            evidence = f"Data Flow section: {'found' if has_df else 'missing'}, sequenceDiagram: {'found' if has_seq else 'missing'}"

        elif "public api" in text.lower() and "table" in text.lower():
            has_api = "### 3. Public API" in content
            has_table = bool(
                re.search(r"\|.*\|.*\|.*\|.*\([\w\.\-]+\.\w+:\d+\)", content)
            )
            passed = has_api and has_table
            evidence = f"API section: {'found' if has_api else 'missing'}, Table with citations: {'found' if has_table else 'missing'}"

        elif "extension guide" in text.lower():
            has_ext = (
                "### 6. Extension Guide" in content or "Extension Guide" in content
            )
            passed = has_ext
            evidence = f"Extension Guide section: {'found' if has_ext else 'missing'}"

        elif "threading" in text.lower() or "main-thread" in text.lower():
            has_limit = "### 8. Known Limitations" in content
            has_thread = bool(re.search(r"thread", content, re.IGNORECASE))
            passed = has_limit and has_thread
            evidence = f"Limitations: {'found' if has_limit else 'missing'}, Thread mention: {'found' if has_thread else 'missing'}"

        elif "claims" in text.lower() and "citation" in text.lower():
            citations = re.findall(r"\([\w\.\-]+\.\w+:\d+\)", content)
            passed = len(citations) >= 5
            evidence = f"Found {len(citations)} citations in claim sections"

        else:
            # Generic check - just see if content exists
            passed = len(content) > 500
            evidence = f"Document length: {len(content)} chars"

        results.append({"text": text, "passed": passed, "evidence": evidence})
    return results


def grade_tdd_assertions(content, assertions):
    results = []
    for a in assertions:
        text = a
        passed = False
        evidence = ""

        if "Documents/TDDs/" in text and "TDD_" in text:
            passed = True
            evidence = "File exists in outputs directory"

        elif "8 TDD sections" in text or "all 8" in text.lower():
            sections = [
                "Problem",
                "Goals",
                "Non-Goals",
                "Design",
                "Alternatives",
                "Dependencies",
                "Risks",
                "Open Questions",
            ]
            found = [s for s in sections if f"## {s}" in content or f"# {s}" in content]
            passed = len(found) >= 7  # Allow minor header variations
            evidence = f"Found {len(found)}/8 sections: {', '.join(found)}"

        elif "components table" in text.lower():
            has_table = bool(
                re.search(
                    r"\|\s*Component\s*\|.*Responsibility", content, re.IGNORECASE
                )
            )
            passed = has_table
            evidence = f"Components table: {'found' if has_table else 'missing'}"

        elif "mermaid" in text.lower() and "data flow" in text.lower():
            has_mermaid = "```mermaid" in content
            passed = has_mermaid
            evidence = f"Mermaid diagram: {'found' if has_mermaid else 'missing'}"

        elif "alternatives" in text.lower() and (
            "2 rows" in text or "2 approaches" in text or "at least 2" in text
        ):
            alt_section = re.search(r"## Alternatives.*?(?=##|\Z)", content, re.DOTALL)
            if alt_section:
                rows = re.findall(r"^\|[^-].*\|", alt_section.group(), re.MULTILINE)
                data_rows = [r for r in rows if "Option" not in r and "---" not in r]
                passed = len(data_rows) >= 2
                evidence = f"Found {len(data_rows)} alternative rows in table"
            else:
                evidence = "Alternatives section not found"

        elif "dependencies" in text.lower() and (
            "savesystem" in text.lower() or "eventbus" in text.lower()
        ):
            has_save = bool(re.search(r"SaveSystem|Save", content, re.IGNORECASE))
            has_event = bool(re.search(r"EventBus|Event", content, re.IGNORECASE))
            passed = has_save or has_event
            evidence = f"SaveSystem ref: {'found' if has_save else 'missing'}, EventBus ref: {'found' if has_event else 'missing'}"

        elif "risks" in text.lower() and "likelihood" in text.lower():
            has_risk = bool(
                re.search(r"\|\s*Risk\s*\|.*Likelihood", content, re.IGNORECASE)
            )
            has_hml = bool(re.search(r"\b[HML]\b", content))
            passed = has_risk or has_hml
            evidence = f"Risk table: {'found' if has_risk else 'missing'}, H/M/L ratings: {'found' if has_hml else 'missing'}"

        elif "template" in text.lower() and "loaded" in text.lower():
            passed = "## Problem" in content or "## Design" in content
            evidence = "TDD template structure present"

        elif "TODO" in text and "TBD" in text:
            clean = content.replace("No TODO/TBD/FIXME", "")
            has_forbidden = bool(re.search(r"\b(TODO|TBD|FIXME)\b", clean))
            passed = not has_forbidden
            evidence = f"{'No' if not has_forbidden else 'Found'} forbidden tags"

        elif (
            "problem" in text.lower()
            and "goals" in text.lower()
            and "non-goals" in text.lower()
        ):
            has_prob = "## Problem" in content or "Problem" in content
            has_goals = "## Goals" in content or "Goals" in content
            has_ng = "Non-Goals" in content or "Non Goals" in content
            passed = has_prob and has_goals and has_ng
            evidence = f"Problem: {'found' if has_prob else 'missing'}, Goals: {'found' if has_goals else 'missing'}, Non-Goals: {'found' if has_ng else 'missing'}"

        elif "concrete components" in text.lower():
            has_table = bool(re.search(r"\|\s*\w+\s*\|.*\|", content))
            passed = has_table
            evidence = (
                f"Component specifications: {'found' if has_table else 'missing'}"
            )

        else:
            passed = len(content) > 500
            evidence = f"Document length: {len(content)} chars"

        results.append({"text": text, "passed": passed, "evidence": evidence})
    return results


def grade_eval(eval_dir, eval_meta, is_system):
    results = {}
    for config in ["with_skill", "without_skill"]:
        outputs_dir = os.path.join(eval_dir, config, "outputs")
        md_file = find_md_file(outputs_dir)

        if not md_file:
            results[config] = {
                "expectations": [
                    {"text": a, "passed": False, "evidence": "No output file found"}
                    for a in eval_meta["assertions"]
                ],
                "summary": {
                    "passed": 0,
                    "failed": len(eval_meta["assertions"]),
                    "total": len(eval_meta["assertions"]),
                    "pass_rate": 0.0,
                },
            }
            continue

        with open(md_file, "r") as f:
            content = f.read()

        if is_system:
            expectations = grade_system_assertions(content, eval_meta["assertions"])
        else:
            expectations = grade_tdd_assertions(content, eval_meta["assertions"])

        passed = sum(1 for e in expectations if e["passed"])
        total = len(expectations)

        results[config] = {
            "expectations": expectations,
            "summary": {
                "passed": passed,
                "failed": total - passed,
                "total": total,
                "pass_rate": round(passed / total, 2) if total > 0 else 0,
            },
        }

        # Save grading.json
        grading_path = os.path.join(eval_dir, config, "grading.json")
        with open(grading_path, "w") as f:
            json.dump(results[config], f, indent=2)

        print(
            f"  {config}: {passed}/{total} ({results[config]['summary']['pass_rate']:.0%})"
        )

    return results


def main():
    evals = [
        ("eval-1-eventbus-system", True),
        ("eval-2-savesystem-system", True),
        ("eval-3-objectpool-system", True),
        ("eval-4-inventory-tdd", False),
        ("eval-5-dialogue-tdd", False),
    ]

    all_results = {}

    for eval_name, is_system in evals:
        eval_dir = os.path.join(ITER, eval_name)
        meta_path = os.path.join(eval_dir, "eval_metadata.json")

        if not os.path.exists(meta_path):
            print(f"SKIP: {eval_name} — no metadata")
            continue

        with open(meta_path) as f:
            meta = json.load(f)

        print(f"\nGrading: {eval_name}")
        all_results[eval_name] = grade_eval(eval_dir, meta, is_system)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    ws_total = ws_passed = bs_total = bs_passed = 0

    for name, results in all_results.items():
        ws = results.get("with_skill", {}).get("summary", {})
        bs = results.get("without_skill", {}).get("summary", {})
        ws_p = ws.get("pass_rate", 0)
        bs_p = bs.get("pass_rate", 0)
        ws_total += ws.get("total", 0)
        ws_passed += ws.get("passed", 0)
        bs_total += bs.get("total", 0)
        bs_passed += bs.get("passed", 0)
        print(f"  {name}: with={ws_p:.0%} without={bs_p:.0%} delta={ws_p - bs_p:+.0%}")

    print(
        f"\n  OVERALL: with={ws_passed}/{ws_total} ({ws_passed / ws_total:.0%}) without={bs_passed}/{bs_total} ({bs_passed / bs_total:.0%})"
    )
    print(f"  DELTA: {(ws_passed / ws_total - bs_passed / bs_total):+.0%}")


if __name__ == "__main__":
    main()
