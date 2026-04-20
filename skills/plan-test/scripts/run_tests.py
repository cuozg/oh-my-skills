#!/usr/bin/env python3
"""
run_tests.py — End-to-end orchestrator for the plan-test skill.

Pipeline:
    1. parse_goal(goal.md)              → structured dict
    2. verify_criteria(criteria, root)  → per-criterion results
    3. render_report(goal, results)     → Markdown
    4. write to Docs/Goals/<goal_name>-test.md

Usage:
    python run_tests.py <path_to_goal.md> [--root <repo>] [--mode quick|deep]
                        [--out <path>] [--print]

Exit codes:
    0  report generated, all criteria met
    1  report generated, some criteria partial/unmet
    2  usage / input error
    3  unexpected failure
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from parse_goal import parse_goal  # type: ignore  # noqa: E402
from verify_implementation import verify_criteria  # type: ignore  # noqa: E402
from generate_report import render_report  # type: ignore  # noqa: E402


QUICK_MAX = 5  # <=5 criteria → quick; >=10 criteria → deep; between = auto


def _pick_mode(explicit: str | None, n: int) -> str:
    if explicit:
        return explicit
    if n <= QUICK_MAX:
        return "quick"
    return "deep"


def _default_out(goal_path: Path, repo_root: Path) -> Path:
    """Derive Docs/Goals/<goal_name>-test.md."""
    goals_root = repo_root / "Docs" / "Goals"
    goals_root.mkdir(parents=True, exist_ok=True)

    try:
        rel = goal_path.resolve().relative_to(goals_root.resolve())
        stem = rel.with_suffix("").as_posix().replace("/", "-")
    except ValueError:
        stem = goal_path.stem
    return goals_root / f"{stem}-test.md"


def run(
    goal_file: str | Path,
    repo_root: str | Path = ".",
    mode: str | None = None,
    out_path: str | Path | None = None,
) -> tuple[Path, dict[str, int]]:
    """Run the full pipeline. Returns (report_path, counts)."""
    goal_path = Path(goal_file).resolve()
    root = Path(repo_root).resolve()

    goal = parse_goal(goal_path)
    criteria = goal["acceptance_criteria"]
    results = verify_criteria(criteria, root)

    chosen_mode = _pick_mode(mode, len(criteria))
    report = render_report(goal, results, mode=chosen_mode)

    target = Path(out_path).resolve() if out_path else _default_out(goal_path, root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(report, encoding="utf-8")

    counts = {
        "total": len(results),
        "met": sum(1 for r in results if r["status"] == "met"),
        "partial": sum(1 for r in results if r["status"] == "partial"),
        "unmet": sum(1 for r in results if r["status"] == "unmet"),
    }
    return target, counts


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="run_tests.py",
        description="Run plan-test pipeline over a goal file.",
    )
    parser.add_argument("goal", help="path to goal .md file under Docs/Goals/")
    parser.add_argument("--root", default=".", help="repo root (default: cwd)")
    parser.add_argument("--mode", choices=("quick", "deep"), default=None,
                        help="verification depth (auto by default)")
    parser.add_argument("--out", default=None,
                        help="output path (default: Docs/Goals/<goal_name>-test.md)")
    parser.add_argument("--print", action="store_true",
                        help="print report to stdout in addition to writing")
    args = parser.parse_args(argv[1:])

    try:
        path, counts = run(args.goal, args.root, args.mode, args.out)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"unexpected failure: {exc}", file=sys.stderr)
        return 3

    print(f"✓ report: {path}")
    print(
        f"  {counts['met']} met · {counts['partial']} partial · "
        f"{counts['unmet']} unmet · {counts['total']} total"
    )
    if args.print:
        print()
        print(path.read_text(encoding="utf-8"))

    return 0 if counts["partial"] == 0 and counts["unmet"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
