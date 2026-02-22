#!/usr/bin/env python3

import subprocess
import sys


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


def main() -> int:
    if len(sys.argv) > 1:
        print(f"Usage: {sys.argv[0]}")
        return 1

    try:
        print("=== Public Classes & Interfaces ===")
        cmd = "grep -r 'public class\\|public interface' Assets/Scripts --include='*.cs' | sed 's/.*public //' | sort -u"
        _ = sys.stdout.write(run_shell(cmd))

        print("\n=== Serialized Fields ===")
        cmd = "grep -r '\\[SerializeField\\]' Assets/Scripts --include='*.cs' | cut -d: -f1 | sort | uniq -c"
        _ = sys.stdout.write(run_shell(cmd))

        print("\n=== Scriptable Objects ===")
        cmd = "grep -r 'ScriptableObject' Assets/Scripts --include='*.cs' | cut -d: -f1 | sort -u"
        _ = sys.stdout.write(run_shell(cmd))

        print("\n=== Custom Editors ===")
        cmd = "grep -r '\\[CustomEditor\\|\\[CanEditMultipleObjects\\]' Assets/Scripts --include='*.cs' | cut -d: -f1 | sort -u"
        _ = sys.stdout.write(run_shell(cmd))
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
