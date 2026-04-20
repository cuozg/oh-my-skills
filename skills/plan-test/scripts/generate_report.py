#!/usr/bin/env python3
"""
generate_report.py — Render a Markdown test report from verification results.

Produces a document at Docs/Goals/<goal_name>-test.md with:
  - YAML frontmatter
  - Objective (echoed from goal)
  - Criteria Matrix (table: # | Criterion | Status | Evidence)
  - Per-criterion Test Results (detailed)
  - Summary Stats (pass rate, coverage)
  - Recommendations

Usage:
    python generate_report.py <parsed_goal.json> <results.json> <out.md>
    from generate_report import render_report
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATUS_GLYPH = {"met": "✅", "partial": "⚠️", "unmet": "❌"}
STATUS_LABEL = {"met": "Met", "partial": "Partial", "unmet": "Unmet"}


def _fmt_evidence(result: dict[str, Any]) -> str:
    bits: list[str] = []
    for hit in result.get("code_hits", [])[:2]:
        bits.append(f"`{hit['file']}:{hit['line_no']}`")
    for pc in result.get("path_checks", []):
        if pc["exists"]:
            bits.append(f"`{pc['path']}` ({pc['kind']})")
    for tf in result.get("test_files", [])[:2]:
        bits.append(f"test: `{tf}`")
    if not bits:
        return "_no evidence_"
    return ", ".join(bits)


def _summary_stats(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    met = sum(1 for r in results if r["status"] == "met")
    partial = sum(1 for r in results if r["status"] == "partial")
    unmet = sum(1 for r in results if r["status"] == "unmet")
    with_tests = sum(1 for r in results if r.get("test_files"))
    pass_rate = round(100.0 * met / total, 1) if total else 0.0
    coverage = round(100.0 * with_tests / total, 1) if total else 0.0
    return {
        "total": total,
        "met": met,
        "partial": partial,
        "unmet": unmet,
        "pass_rate": pass_rate,
        "test_coverage": coverage,
    }


def _recommendations(results: list[dict[str, Any]]) -> list[str]:
    recs: list[str] = []
    for r in results:
        if r["status"] == "unmet":
            recs.append(f"❌ Implement: _{r['text']}_ — {r['reasoning']}")
        elif r["status"] == "partial":
            if not r.get("test_files"):
                recs.append(f"⚠️ Add tests for: _{r['text']}_")
            else:
                recs.append(f"⚠️ Strengthen: _{r['text']}_ — {r['reasoning']}")
    return recs


def render_report(goal: dict[str, Any], results: list[dict[str, Any]], mode: str = "quick") -> str:
    stats = _summary_stats(results)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = goal.get("title") or "(untitled goal)"
    objective = goal.get("sections", {}).get("Objective", "").strip() or "_not specified_"
    fm = goal.get("frontmatter", {})

    lines: list[str] = []

    # Frontmatter
    lines.append("---")
    lines.append(f"kind: test-report")
    lines.append(f"goal: {Path(goal.get('path','')).name}")
    lines.append(f"mode: {mode}")
    lines.append(f"generated: {now}")
    lines.append(f"pass_rate: {stats['pass_rate']}%")
    lines.append(f"test_coverage: {stats['test_coverage']}%")
    lines.append("---")
    lines.append("")

    # Title
    lines.append(f"# Test Report — {title}")
    lines.append("")
    lines.append(f"> Generated {now} in **{mode}** mode from `{goal.get('path','')}`")
    lines.append(
        f"> Goal status: `{fm.get('status','?')}` · priority: `{fm.get('priority','?')}`"
    )
    lines.append("")

    # Objective
    lines.append("## Objective")
    lines.append("")
    lines.append(objective)
    lines.append("")

    # Criteria Matrix
    lines.append("## Criteria Matrix")
    lines.append("")
    if not results:
        lines.append("_No acceptance criteria found in goal._")
        lines.append("")
    else:
        lines.append("| # | Criterion | Status | Evidence |")
        lines.append("|---|-----------|--------|----------|")
        for i, r in enumerate(results, start=1):
            glyph = STATUS_GLYPH[r["status"]]
            label = STATUS_LABEL[r["status"]]
            text = r["text"].replace("|", "\\|")
            lines.append(f"| {i} | {text} | {glyph} {label} | {_fmt_evidence(r)} |")
        lines.append("")

    # Summary Stats
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total criteria:** {stats['total']}")
    lines.append(f"- **Met:** {stats['met']} ✅")
    lines.append(f"- **Partial:** {stats['partial']} ⚠️")
    lines.append(f"- **Unmet:** {stats['unmet']} ❌")
    lines.append(f"- **Pass rate:** {stats['pass_rate']}%")
    lines.append(f"- **Test coverage (criteria with tests):** {stats['test_coverage']}%")
    lines.append("")

    # Detailed Results
    lines.append("## Test Results (Detailed)")
    lines.append("")
    for i, r in enumerate(results, start=1):
        glyph = STATUS_GLYPH[r["status"]]
        label = STATUS_LABEL[r["status"]]
        lines.append(f"### {i}. {glyph} {label} — {r['text']}")
        lines.append("")
        lines.append(f"- **Reasoning:** {r['reasoning']}")
        lines.append(f"- **Originally checked in goal:** {'yes' if r['checked'] else 'no'}")

        if r.get("code_hits"):
            lines.append("- **Code evidence:**")
            for hit in r["code_hits"]:
                snippet = hit["text"].replace("`", "ʼ")
                lines.append(
                    f"  - `{hit['file']}:{hit['line_no']}` — "
                    f"matched `{hit['matched']}` → `{snippet}`"
                )

        if r.get("path_checks"):
            lines.append("- **Path checks:**")
            for pc in r["path_checks"]:
                mark = "✓" if pc["exists"] else "✗"
                lines.append(f"  - {mark} `{pc['path']}` ({pc['kind']})")

        if r.get("test_files"):
            lines.append("- **Test files:**")
            for tf in r["test_files"]:
                lines.append(f"  - `{tf}`")
        else:
            lines.append("- **Test files:** _none found_")

        lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    recs = _recommendations(results)
    if not recs:
        lines.append("_All acceptance criteria met. Ship it._")
    else:
        for rec in recs:
            lines.append(f"- {rec}")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append(
        "_Generated by the `plan-test` skill. "
        "Re-run after implementation changes to refresh this report._"
    )
    lines.append("")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render test report markdown.")
    parser.add_argument("goal_json", help="path to JSON from parse_goal.py")
    parser.add_argument("results_json", help="path to JSON list of results from verify_implementation.py")
    parser.add_argument("out_md", help="output .md path")
    parser.add_argument("--mode", default="quick", choices=("quick", "deep"))
    args = parser.parse_args(argv[1:])

    try:
        goal = json.loads(Path(args.goal_json).read_text(encoding="utf-8"))
        payload = json.loads(Path(args.results_json).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    results = payload.get("results", payload) if isinstance(payload, dict) else payload
    markdown = render_report(goal, results, mode=args.mode)
    Path(args.out_md).write_text(markdown, encoding="utf-8")
    print(f"wrote {args.out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
