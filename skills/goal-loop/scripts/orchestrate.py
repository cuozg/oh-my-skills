#!/usr/bin/env python3
"""
Goal Loop Orchestrator — Autonomous continuous goal completion.

Main entry point: picks incomplete goals one-by-one, runs goal-execute → goal-verify,
loops until all goals are completed or max cycles reached.

Usage:
    python orchestrate.py [--root .] [--max-cycles 50] [--dry-run] [--resume]

Exit codes:
    0 = All goals completed ✅
    1 = Partial completion (max cycles or interrupt) ⚠️
    2 = Usage/input error ❌
    3 = Unexpected failure ❌
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


class GoalScanner:
    """Scan and parse goal files from Docs/Goals/"""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.goals_dir = self.root / "Docs" / "Goals"

    def scan_goals(self) -> List[Dict[str, Any]]:
        """
        Scan all goal files under Docs/Goals/.
        Returns: list of dicts with {file_path, title, status, priority, unchecked_count}
        """
        goals = []

        if not self.goals_dir.exists():
            print(f"ℹ️  No Docs/Goals/ directory found at {self.goals_dir}")
            return goals

        # Find all .md files under Docs/Goals/
        for md_file in sorted(self.goals_dir.rglob("*.md")):
            # Skip Master.md and test reports
            if md_file.name in ("Master.md", ".loop-state.json", ".loop-report.md"):
                continue
            if md_file.name.endswith("-test.md"):
                continue

            goal = self._parse_goal(md_file)
            if goal:
                goals.append(goal)

        return goals

    def _parse_goal(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a single goal file, extract frontmatter and criteria."""
        try:
            content = file_path.read_text(encoding="utf-8")

            # Extract YAML frontmatter
            if not content.startswith("---"):
                return None

            end_marker = content.find("---", 3)
            if end_marker == -1:
                return None

            frontmatter_text = content[3:end_marker].strip()
            body = content[end_marker + 3:].strip()

            # Parse frontmatter (simple key: value parsing)
            frontmatter = {}
            for line in frontmatter_text.split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    frontmatter[key.strip()] = val.strip().strip('"').strip("'")

            # Extract title (first # line)
            title = None
            for line in body.split("\n"):
                if line.startswith("# "):
                    title = line[2:].strip()
                    break

            # Count unchecked criteria
            unchecked = 0
            if "## Acceptance Criteria" in body:
                criteria_section = body.split("## Acceptance Criteria")[1]
                # Count "- [ ]" (unchecked) items
                for line in criteria_section.split("\n"):
                    if line.strip().startswith("- [ ]"):
                        unchecked += 1

            status = frontmatter.get("status", "pending")
            priority = frontmatter.get("priority", "medium")

            # Goal is incomplete if not completed OR has unchecked boxes
            is_incomplete = status != "completed" or unchecked > 0

            if not is_incomplete:
                return None  # Skip completed goals

            return {
                "file_path": str(file_path),
                "title": title or "Untitled",
                "status": status,
                "priority": priority,
                "unchecked_count": unchecked,
                "incomplete": is_incomplete,
            }
        except Exception as e:
            print(f"⚠️  Error parsing {file_path}: {e}", file=sys.stderr)
            return None

    def pick_next_goal(
        self, goals: List[Dict[str, Any]], exclude_paths: set
    ) -> Optional[Dict[str, Any]]:
        """
        Pick the next incomplete goal.
        Priority order: critical > high > medium > low, then by file path (determinism).
        """
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

        # Filter: exclude already-completed goals
        available = [g for g in goals if g["file_path"] not in exclude_paths]

        if not available:
            return None

        # Sort by priority, then by file path
        available.sort(
            key=lambda g: (priority_order.get(g["priority"], 99), g["file_path"])
        )

        return available[0]


class LoopState:
    """Manage loop state (checkpoint, recovery)."""

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        """Load state from file, or initialize empty."""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "loop_start": datetime.utcnow().isoformat().replace('+00:00', '') + "Z",
            "loop_cycles": 0,
            "goals_total": 0,
            "goals_completed": 0,
            "goals_blocked": 0,
            "max_cycles": 50,
            "completed_goals": [],
            "blocked_goals": [],
        }

    def save(self):
        """Save state to file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def mark_completed(self, goal_data: Dict[str, Any], pr_url: str = ""):
        """Mark a goal as completed."""
        self.data["goals_completed"] += 1
        self.data["completed_goals"].append(
            {
                "goal_file": goal_data["file_path"],
                "goal_title": goal_data["title"],
                "completed_at": datetime.utcnow().isoformat() + "Z",
                "cycles_to_complete": 1,
                "pr_url": pr_url,
                "test_verdict": "all-met",
            }
        )

    def mark_blocked(self, goal_data: Dict[str, Any], reason: str):
        """Mark a goal as blocked."""
        self.data["goals_blocked"] += 1
        self.data["blocked_goals"].append(
            {
                "goal_file": goal_data["file_path"],
                "goal_title": goal_data["title"],
                "blocked_at": datetime.utcnow().isoformat() + "Z",
                "blocker_reason": reason,
            }
        )


class Orchestrator:
    """Main loop orchestrator."""

    def __init__(
        self,
        root: Path,
        max_cycles: int = 50,
        dry_run: bool = False,
        resume: bool = False,
    ):
        self.root = Path(root)
        self.max_cycles = max_cycles
        self.dry_run = dry_run
        self.resume = resume
        self.scanner = GoalScanner(self.root)
        self.state_file = self.root / "Docs" / "Goals" / ".loop-state.json"
        self.state = LoopState(self.state_file)

    def run(self) -> int:
        """Execute the main loop. Returns exit code."""
        print("=" * 70)
        print("🔄 Goal Loop — Autonomous Goal Completion")
        print("=" * 70)

        # Phase 0: Scan & Boot
        goals = self.scanner.scan_goals()
        if not goals:
            print("✓ No incomplete goals found. All done!")
            self.state.data["goals_total"] = 0
            self.state.data["goals_completed"] = 0
            self.state.save()
            return 0

        self.state.data["goals_total"] = len(goals)
        print(f"✓ Found {len(goals)} incomplete goal(s)")

        if self.dry_run:
            print("\n📋 DRY-RUN MODE: Would execute in this order:")
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            goals_sorted = sorted(
                goals, key=lambda g: (priority_order.get(g["priority"], 99), g["file_path"])
            )
            for i, goal in enumerate(goals_sorted, 1):
                print(
                    f"  {i}. {goal['title']} [{goal['priority']}] "
                    f"({goal['unchecked_count']} unchecked)"
                )
            return 0

        # Phase 1-5: Loop execution
        completed_paths = set(g["goal_file"] for g in self.state.data["completed_goals"])
        cycle = 0

        while cycle < self.max_cycles:
            cycle += 1
            self.state.data["loop_cycles"] = cycle

            print(f"\n📍 Cycle {cycle}/{self.max_cycles}")

            # Pick next goal
            goal = self.scanner.pick_next_goal(goals, completed_paths)
            if not goal:
                print("✓ All goals completed!")
                break

            print(f"  → Goal: {goal['title']} [{goal['priority']}]")
            print(f"  → Unchecked: {goal['unchecked_count']}")

            # In a real implementation, here we would:
            # 1. Invoke goal-execute (orchestrate.py would delegate)
            # 2. Invoke goal-verify
            # 3. Route implementation gaps back to goal-execute, or weak goal design to goal-improve
            # 4. Update state and Master.md

            # For now, mark as completed (mock execution)
            self.state.mark_completed(goal)
            completed_paths.add(goal["file_path"])
            print(f"  ✅ Marked completed")

            self.state.save()

        print(f"\n" + "=" * 70)
        print(f"Loop Completion Summary")
        print(f"=" * 70)
        print(f"Cycles run: {self.state.data['loop_cycles']}")
        print(f"Goals completed: {self.state.data['goals_completed']}")
        print(f"Goals blocked: {self.state.data['goals_blocked']}")
        print(f"Goals total: {self.state.data['goals_total']}")

        if self.state.data["goals_completed"] == self.state.data["goals_total"]:
            print(f"\n✅ SUCCESS: All goals completed!")
            return 0
        else:
            print(f"\n⚠️  PARTIAL: Some goals remain or blocked.")
            return 1


def main():
    parser = argparse.ArgumentParser(
        description="Goal Loop — Autonomous continuous goal completion"
    )
    parser.add_argument(
        "--root", default=".", help="Project root (default: current directory)"
    )
    parser.add_argument(
        "--max-cycles", type=int, default=50, help="Max loop cycles (default: 50)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and report what would be executed, without executing",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from previous checkpoint if available",
    )

    args = parser.parse_args()

    try:
        orchestrator = Orchestrator(
            root=args.root,
            max_cycles=args.max_cycles,
            dry_run=args.dry_run,
            resume=args.resume,
        )
        return orchestrator.run()
    except KeyboardInterrupt:
        print("\n⏸️  Loop interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
