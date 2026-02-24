#!/usr/bin/env python3
"""
Investigate Unity codebase for feature planning.

Usage:
    investigate_feature.py "<search term>"
    investigate_feature.py --init <plan-name> [keyword1] [keyword2] ...

Shared by: unity-plan-deep, unity-plan-detail
"""

import shlex
import subprocess
import sys
from pathlib import Path


def run_capture(command: str) -> str:
    result = subprocess.run(
        command,
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


def print_section(title: str, output: str, fallback: str) -> str:
    """Print a section with output or fallback message. Returns output for reuse."""
    print(f"\n=== {title} ===")
    if output.strip():
        sys.stdout.write(output)
    else:
        print(fallback)
    return output


def investigate(search_term: str) -> dict[str, str]:
    """Run all investigation searches. Returns dict of section->output."""
    results: dict[str, str] = {}

    results["classes"] = print_section(
        "Existing Classes",
        run_capture(
            "grep -Rni --include='*.cs' -E "
            + shlex.quote(
                f"class[[:space:]]+.*{search_term}"
                f"|interface[[:space:]]+.*{search_term}"
                f"|struct[[:space:]]+.*{search_term}"
            )
            + " Assets/Scripts || true"
        ),
        "No class/interface/struct definitions matched by name.",
    )

    results["tests"] = print_section(
        "Test Files",
        run_capture(
            "grep -Rni --include='*.cs' -E "
            + shlex.quote(search_term)
            + " Assets | grep -E '(/Tests?/|Test\\.cs$|Tests\\.cs$)' || true"
        ),
        "No related test files found.",
    )

    results["config"] = print_section(
        "Config/Data Files",
        run_capture(
            "grep -Rni --include='*.asset' --include='*.json' --include='*.yaml' "
            "--include='*.yml' --include='*.asmdef' --include='*.inputactions' -E "
            + shlex.quote(search_term)
            + " Assets ProjectSettings Packages 2>/dev/null || true"
        ),
        "No related config/data files found.",
    )

    results["prefabs"] = print_section(
        "Related Prefabs",
        run_capture(
            f"find Assets -name '*{search_term}*.prefab' 2>/dev/null | head -n 10"
        ),
        "No related prefabs found.",
    )

    results["integration"] = print_section(
        "Integration Points",
        run_capture(
            "grep -Rni --include='*.cs' -E "
            + shlex.quote(
                f"{search_term}|SerializeField|UnityEvent|event[[:space:]]"
                f"|OnEnable\\(|Awake\\(|Start\\(|ScriptableObject"
                f"|Addressables|Resources\\.Load|GetComponent"
            )
            + " Assets/Scripts || true"
        ),
        "No integration points found from heuristic search.",
    )

    print("\n=== Existing vs Needs Creation (Heuristic) ===")
    if results["classes"].strip():
        print("Existing: Feature-related classes appear to exist.")
        print("Needs Creation: Focus on enhancements, integrations, tests, or config.")
    else:
        print("Existing: No obvious feature classes found.")
        print("Needs Creation: New feature classes and wiring likely required.")
    if not results["tests"].strip():
        print("Testing Gap: No matching tests; plan should add or extend tests.")
    if not results["config"].strip():
        print("Config/Data Gap: Verify whether new assets/config are needed.")

    return results


def init_plan_folder(plan_name: str) -> Path:
    """Create plan output folder structure. Returns plan directory path."""
    plan_dir = Path("documents/plans") / plan_name
    (plan_dir / "patches").mkdir(parents=True, exist_ok=True)
    print(f"=== Created plan output folder: {plan_dir.as_posix()} ===")
    print("Expected outputs:")
    print(f"  {plan_dir}/overview.html")
    print(f"  {plan_dir}/tasks.html")
    print(f"  {plan_dir}/patch.html")
    print(f"  {plan_dir}/tasks.json")
    print(f"  {plan_dir}/patches/TASK-{{epic.task}}.patch")
    return plan_dir


def main() -> int:
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} "<search term>"')
        print(f"       {sys.argv[0]} --init <plan-name> [keyword1] ...")
        return 1

    args = sys.argv[1:]

    if args[0] == "--init":
        if len(args) < 2:
            print("Error: --init requires a plan name")
            return 1
        init_plan_folder(args[1])
        keywords = args[2:]
        if not keywords:
            return 0
        search_term = " ".join(keywords)
    else:
        search_term = " ".join(args)

    scripts_root = Path("Assets/Scripts")
    if not scripts_root.is_dir():
        print(f"Warning: {scripts_root} not found in {Path.cwd()}")
        print("Searching available directories instead...")

    print(f"=== Feature Investigation: {search_term} ===")
    print(f"Root: {Path.cwd()}")

    investigate(search_term)

    print("\n=== Investigation Complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
