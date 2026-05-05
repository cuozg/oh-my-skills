#!/usr/bin/env python3
"""
Goal Scanner — Scan and parse goal files from Docs/Goals/

Provides utilities to:
- List all goals under Docs/Goals/
- Parse goal frontmatter and acceptance criteria
- Filter by status, priority, completeness
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class GoalScanner:
    """Scan and parse goal files from Docs/Goals/"""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.goals_dir = self.root / "Docs" / "Goals"

    def scan_all_goals(self) -> List[Dict[str, Any]]:
        """
        Scan all goal files (including completed).
        Returns: list of dicts with {file_path, title, status, priority, unchecked_count}
        """
        goals = []

        if not self.goals_dir.exists():
            return goals

        for md_file in sorted(self.goals_dir.rglob("*.md")):
            if md_file.name in ("Master.md", ".loop-state.json"):
                continue
            if md_file.name.endswith("-test.md"):
                continue

            goal = self._parse_goal(md_file)
            if goal:
                goals.append(goal)

        return goals

    def scan_incomplete_goals(self) -> List[Dict[str, Any]]:
        """Scan only incomplete goals (status != completed OR unchecked > 0)."""
        all_goals = self.scan_all_goals()
        return [g for g in all_goals if g.get("incomplete", False)]

    def _parse_goal(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a single goal file, extract frontmatter and criteria."""
        try:
            content = file_path.read_text(encoding="utf-8")

            if not content.startswith("---"):
                return None

            end_marker = content.find("---", 3)
            if end_marker == -1:
                return None

            frontmatter_text = content[3:end_marker].strip()
            body = content[end_marker + 3:].strip()

            # Parse frontmatter
            frontmatter = {}
            for line in frontmatter_text.split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    frontmatter[key.strip()] = val.strip().strip('"').strip("'")

            # Extract title
            title = None
            for line in body.split("\n"):
                if line.startswith("# "):
                    title = line[2:].strip()
                    break

            # Count unchecked criteria
            unchecked = 0
            checked = 0
            if "## Acceptance Criteria" in body:
                criteria_section = body.split("## Acceptance Criteria")[1]
                for line in criteria_section.split("\n"):
                    if line.strip().startswith("- [ ]"):
                        unchecked += 1
                    elif line.strip().startswith("- [x]"):
                        checked += 1

            status = frontmatter.get("status", "pending")
            priority = frontmatter.get("priority", "medium")

            is_incomplete = status != "completed" or unchecked > 0

            return {
                "file_path": str(file_path),
                "title": title or "Untitled",
                "status": status,
                "priority": priority,
                "unchecked_count": unchecked,
                "checked_count": checked,
                "total_criteria": checked + unchecked,
                "incomplete": is_incomplete,
            }
        except Exception as e:
            print(f"⚠️  Error parsing {file_path}: {e}", file=sys.stderr)
            return None


if __name__ == "__main__":
    # Simple CLI for testing
    import argparse

    parser = argparse.ArgumentParser(description="Scan goal files")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--incomplete-only", action="store_true", help="Show only incomplete goals")

    args = parser.parse_args()

    scanner = GoalScanner(Path(args.root))
    goals = scanner.scan_incomplete_goals() if args.incomplete_only else scanner.scan_all_goals()

    print(f"Found {len(goals)} goal(s):")
    for goal in goals:
        status_mark = "⏳" if goal["status"] != "completed" else "✅"
        print(
            f"  {status_mark} {goal['title']} [{goal['priority']}] "
            f"({goal['checked_count']}/{goal['total_criteria']} complete)"
        )
