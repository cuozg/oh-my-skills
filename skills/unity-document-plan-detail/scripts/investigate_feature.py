#!/usr/bin/env python3

import shlex
import subprocess
import sys
from pathlib import Path


def run_shell(command: str) -> str:
    result = subprocess.run(
        command,
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


def print_usage(script_name: str) -> None:
    print(f"Usage: {script_name} [keyword1] [keyword2] ...")
    print(f"       {script_name} --init <plan-name> [keyword1] [keyword2] ...")


def main() -> int:
    script_name = sys.argv[0]
    raw_args = sys.argv[1:]
    plan_output_base = Path("documents/plans")

    if not raw_args:
        print_usage(script_name)
        return 1

    if raw_args[0] == "--init":
        if len(raw_args) < 2:
            print("Error: --init requires a plan name")
            print(f"Usage: {script_name} --init <plan-name> [keyword1] [keyword2] ...")
            return 1

        plan_name = raw_args[1]
        plan_dir = plan_output_base / plan_name
        (plan_dir / "patches").mkdir(parents=True, exist_ok=True)

        print(f"=== Created plan output folder: {plan_dir.as_posix()} ===")
        print("Expected outputs:")
        print(f"  {plan_dir.as_posix()}/overview.html")
        print(f"  {plan_dir.as_posix()}/tasks.html")
        print(f"  {plan_dir.as_posix()}/patch.html")
        print(f"  {plan_dir.as_posix()}/tasks.json")
        print(f"  {plan_dir.as_posix()}/patches/T-{{id}}.patch  (one per task)")

        keywords = raw_args[2:]
        if not keywords:
            return 0
    else:
        keywords = raw_args

    keywords_str = " ".join(keywords)
    print(f"=== Investigating Keywords: {keywords_str} ===")

    for keyword in keywords:
        print(f"\n--- Finding scripts related to: {keyword} ---")
        cmd = (
            f"grep -rl {shlex.quote(keyword)} Assets/Scripts --include='*.cs' "
            "| head -n 10"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print(f"\n--- Finding prefabs related to: {keyword} ---")
        cmd = f"find Assets -name '*{keyword}*.prefab' | head -n 5"
        _ = sys.stdout.write(run_shell(cmd))

    print("\n=== Potentially Relevant Classes (Public API) ===")
    for keyword in keywords:
        cmd = (
            "grep -r "
            + shlex.quote(f"public class.*{keyword}")
            + " Assets/Scripts --include='*.cs' | sed 's/.*public //' | head -n 5"
        )
        _ = sys.stdout.write(run_shell(cmd))

    print("\n=== Search Summary ===")
    cmd = (
        "grep -rl "
        + shlex.quote(keywords_str)
        + " Assets/Scripts --include='*.cs' | wc -l"
    )
    total = run_shell(cmd).strip()
    print(f"Total relevant scripts found: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
