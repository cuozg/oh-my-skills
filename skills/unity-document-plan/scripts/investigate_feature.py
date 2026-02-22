#!/usr/bin/env python3

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


def main() -> int:
    script_name = sys.argv[0]

    if len(sys.argv) < 2:
        print(f'Usage: {script_name} "<search term>"')
        return 1

    search_term = " ".join(sys.argv[1:])
    scripts_root = Path("Assets/Scripts")

    if not scripts_root.is_dir():
        print(
            f"Error: {scripts_root.as_posix()} not found from current directory: {Path.cwd()}"
        )
        return 1

    print(f"=== Feature Investigation: {search_term} ===")
    print(f"Root: {Path.cwd()}")

    print()
    print("=== Existing Classes ===")
    class_matches = run_capture(
        "grep -Rni --include='*.cs' -E "
        + subprocess.list2cmdline(
            [
                f"class[[:space:]]+.*{search_term}|interface[[:space:]]+.*{search_term}|struct[[:space:]]+.*{search_term}"
            ]
        )
        + " Assets/Scripts || true"
    )
    if class_matches.strip():
        _ = sys.stdout.write(class_matches)
    else:
        print("No class/interface/struct definitions matched by name.")

    print()
    print("=== Test Files ===")
    test_matches = run_capture(
        "grep -Rni --include='*.cs' -E "
        + subprocess.list2cmdline([search_term])
        + " Assets | grep -E '(/Tests?/|Test\\.cs$|Tests\\.cs$)' || true"
    )
    if test_matches.strip():
        _ = sys.stdout.write(test_matches)
    else:
        print("No related test files found.")

    print()
    print("=== Config/Data Files ===")
    config_matches = run_capture(
        "grep -Rni --include='*.asset' --include='*.json' --include='*.yaml' --include='*.yml' "
        + "--include='*.asmdef' --include='*.inputactions' -E "
        + subprocess.list2cmdline([search_term])
        + " Assets ProjectSettings Packages 2>/dev/null || true"
    )
    if config_matches.strip():
        _ = sys.stdout.write(config_matches)
    else:
        print("No related config/data files found.")

    print()
    print("=== Integration Points ===")
    integration_matches = run_capture(
        "grep -Rni --include='*.cs' -E "
        + subprocess.list2cmdline(
            [
                f"{search_term}|SerializeField|UnityEvent|event[[:space:]]|OnEnable\\(|Awake\\(|Start\\(|Update\\(|ScriptableObject|Addressables|Resources\\.Load|FindObjectOfType|GetComponent|SendMessage"
            ]
        )
        + " Assets/Scripts || true"
    )
    if integration_matches.strip():
        _ = sys.stdout.write(integration_matches)
    else:
        print("No integration points found from heuristic search.")

    print()
    print("=== Existing vs Needs Creation (Heuristic) ===")
    if class_matches.strip():
        print("Existing: Feature-related classes appear to exist.")
        print(
            "Needs Creation: Focus likely on enhancements, integrations, tests, or config updates."
        )
    else:
        print("Existing: No obvious feature classes found.")
        print("Needs Creation: New feature classes and wiring likely required.")

    if not test_matches.strip():
        print("Testing Gap: No matching tests found; plan should add or extend tests.")

    if not config_matches.strip():
        print(
            "Config/Data Gap: No matching config/data detected; verify whether new assets/config are needed."
        )

    print()
    print("=== Investigation Complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
