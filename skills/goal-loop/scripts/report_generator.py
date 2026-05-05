#!/usr/bin/env python3
"""
Report Generator — Format and write goal-loop completion report.

Usage:
    python report_generator.py --state <loop-state.json> [--output Docs/Goals/.loop-report.md]

Generates a markdown report with:
- Summary (completed/blocked counts, time)
- Completed goals (in order, with PR links)
- Blocked goals (with reasons)
- Timeline/log
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


def parse_iso_timestamp(ts: str) -> Optional[datetime]:
    """Parse ISO 8601 timestamp."""
    try:
        # Remove 'Z' and parse
        return datetime.fromisoformat(ts.rstrip('Z'))
    except Exception:
        return None


def format_duration(start_ts: str, end_ts: str) -> str:
    """Format duration between two ISO timestamps."""
    start = parse_iso_timestamp(start_ts)
    end = parse_iso_timestamp(end_ts)

    if not start or not end:
        return "unknown"

    delta = end - start
    hours = delta.total_seconds() // 3600
    minutes = (delta.total_seconds() % 3600) // 60
    seconds = delta.total_seconds() % 60

    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m"
    elif minutes > 0:
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        return f"{int(seconds)}s"


def generate_report(state_file: Path, output_file: Optional[Path] = None) -> str:
    """
    Generate report markdown from loop state.
    Returns the report as a string.
    """
    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Error loading state: {e}", file=sys.stderr)
        return ""

    # Calculate totals
    total = state.get("goals_total", 0)
    completed = len(state.get("completed_goals", []))
    blocked = len(state.get("blocked_goals", []))
    remaining = total - completed - blocked

    # Calculate completion percentage
    completion_pct = (completed / total * 100) if total > 0 else 0

    # Calculate duration
    start_ts = state.get("loop_start", "")
    end_ts = datetime.utcnow().isoformat() + "Z"
    duration = format_duration(start_ts, end_ts)

    # Build report
    report = []
    report.append("# Goal Loop Completion Report\n")
    report.append(f"**Generated:** {datetime.utcnow().isoformat(timespec='seconds')}Z\n")
    report.append(f"**Duration:** {duration}\n")
    report.append(f"**Cycles:** {state.get('loop_cycles', 0)} / {state.get('max_cycles', 50)}\n")
    report.append("")

    # Summary section
    report.append("## Summary\n")
    report.append(f"- **Total goals:** {total}\n")
    report.append(f"- **Completed:** {completed} ({completion_pct:.0f}%)\n")
    report.append(f"- **Blocked:** {blocked}\n")
    report.append(f"- **Remaining:** {remaining}\n")
    report.append("")

    # Completed goals section
    if completed > 0:
        report.append("## Completed Goals ✅\n")
        for i, goal in enumerate(state.get("completed_goals", []), 1):
            report.append(
                f"{i}. **{goal['goal_title']}**\n"
            )
            if goal.get("pr_url"):
                report.append(f"   - PR: [{goal['pr_url']}]({goal['pr_url']})\n")
            report.append(f"   - Test verdict: {goal.get('test_verdict', 'unknown')}\n")
            if goal.get("completed_at"):
                report.append(f"   - Completed at: {goal['completed_at']}\n")
            report.append("")

    # Blocked goals section
    if blocked > 0:
        report.append("## Blocked Goals ⛔\n")
        for goal in state.get("blocked_goals", []):
            report.append(f"- **{goal['goal_title']}**\n")
            report.append(f"  - Reason: {goal.get('blocker_reason', 'unknown')}\n")
            if goal.get("blocked_at"):
                report.append(f"  - Blocked at: {goal['blocked_at']}\n")
            report.append("")

    # Timeline section
    report.append("## Loop Details\n")
    report.append(f"- **Loop started:** {start_ts}\n")
    report.append(f"- **Loop completed:** {end_ts}\n")
    report.append(f"- **Total cycles:** {state.get('loop_cycles', 0)}\n")

    if remaining == 0:
        report.append("\n✅ **All goals completed successfully!**\n")
    elif blocked > 0 or remaining > 0:
        report.append(f"\n⚠️ **{blocked + remaining} goal(s) not yet completed.**\n")
        report.append("Resume the loop with `--resume` flag to continue.\n")

    report_text = "".join(report)

    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(report_text, encoding="utf-8")

    return report_text


def main():
    parser = argparse.ArgumentParser(description="Generate Goal Loop Completion Report")
    parser.add_argument("--state", required=True, help="Path to .loop-state.json")
    parser.add_argument(
        "--output",
        help="Output file (default: print to stdout)",
    )

    args = parser.parse_args()

    state_file = Path(args.state)
    if not state_file.exists():
        print(f"❌ State file not found: {state_file}", file=sys.stderr)
        return 1

    output_file = Path(args.output) if args.output else None
    report = generate_report(state_file, output_file)

    if output_file:
        print(f"✓ Report written to {output_file}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
