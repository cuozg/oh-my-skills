#!/usr/bin/env python3
"""
Check Plan Loop Status — Query current loop state and checkpoint.

Usage:
    python check_status.py [--root .] [--verbose]

Shows:
    - Current loop cycle
    - Completed/blocked goals so far
    - Next incomplete goal
    - Path to checkpoint file
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any


def load_state(state_file: Path) -> Optional[Dict[str, Any]]:
    """Load loop state from checkpoint file."""
    if not state_file.exists():
        return None
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"⚠️  Error loading state: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Check Plan Loop Status")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed info"
    )

    args = parser.parse_args()
    root = Path(args.root)
    state_file = root / "Docs" / "Goals" / ".loop-state.json"

    state = load_state(state_file)

    if not state:
        print("ℹ️  No active loop checkpoint found.")
        print(f"   (Expected at: {state_file})")
        return 0

    print("📊 Plan Loop Status")
    print("=" * 60)
    print(f"Loop start: {state.get('loop_start', 'unknown')}")
    print(f"Cycles: {state.get('loop_cycles', 0)} / {state.get('max_cycles', 50)}")
    print(f"Goals total: {state.get('goals_total', 0)}")
    print(f"Goals completed: {state.get('goals_completed', 0)}")
    print(f"Goals blocked: {state.get('goals_blocked', 0)}")

    if args.verbose:
        print("\n📝 Completed Goals:")
        for goal in state.get("completed_goals", []):
            print(f"  ✅ {goal['goal_title']}")
            if goal.get("pr_url"):
                print(f"     PR: {goal['pr_url']}")

        if state.get("blocked_goals"):
            print("\n⛔ Blocked Goals:")
            for goal in state.get("blocked_goals", []):
                print(f"  ❌ {goal['goal_title']}")
                print(f"     Reason: {goal.get('blocker_reason', 'unknown')}")

    print(f"\n📁 Checkpoint: {state_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
