#!/usr/bin/env python3
"""Trace architecture patterns for a Unity search term."""

import argparse
import os
import shlex
import subprocess
import sys


class Args(argparse.Namespace):
    term: str | None = None


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


def print_section(title: str) -> None:
    print()
    print(f"=== {title} ===")


def main() -> int:
    script_name = sys.argv[0]
    parser = argparse.ArgumentParser(add_help=True)
    _ = parser.add_argument("term", nargs="?")
    args = parser.parse_args(sys.argv[1:], namespace=Args())

    if not args.term:
        print(f"Usage: {script_name} [SearchTerm]")
        print(f"Example: {script_name} Inventory")
        return 1

    term = args.term
    root = "Assets/Scripts"

    if not os.path.isdir(root):
        print(f"Error: {root} not found. Run from Unity project root.")
        return 1

    try:
        print(f"Unity Architecture Trace: {term}")
        print(f"Root: {root}")

        print_section("Interfaces")
        cmd = (
            "grep -RIn --include='*.cs' -E "
            + shlex.quote(
                f"interface[[:space:]]+.*{term}|class[[:space:]]+.*:[[:space:]]*.*I[A-Za-z0-9_]*{term}|class[[:space:]]+.*:[[:space:]]*.*{term}.*I[A-Za-z0-9_]*"
            )
            + f" {shlex.quote(root)} || true"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print_section("Abstract Classes")
        cmd = (
            "grep -RIn --include='*.cs' -E "
            + shlex.quote(
                f"abstract[[:space:]]+class[[:space:]]+.*{term}|class[[:space:]]+.*:[[:space:]]*.*{term}|class[[:space:]]+{term}[[:space:]]*:[[:space:]]*"
            )
            + f" {shlex.quote(root)} || true"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print_section("Concrete Implementations")
        cmd = (
            "grep -RIn --include='*.cs' -E "
            + shlex.quote(
                f"class[[:space:]]+.*{term}.*:[[:space:]]*|:[[:space:]]*.*{term}|class[[:space:]]+.*:[[:space:]]*MonoBehaviour|GetComponent<|FindObjectOfType<"
            )
            + f" {shlex.quote(root)} | grep -i {shlex.quote(term)} || true"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print_section("Data Models")
        cmd = (
            "grep -RIn --include='*.cs' -E "
            + shlex.quote(
                r"\[Serializable\]|ScriptableObject|CreateAssetMenu|JsonUtility|Newtonsoft|ISerializationCallbackReceiver|\[SerializeField\].*ScriptableObject|:[[:space:]]*ScriptableObject"
            )
            + f" {shlex.quote(root)} | grep -i {shlex.quote(term)} || true"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print_section("Managers")
        cmd = (
            "grep -RIn --include='*.cs' -E "
            + shlex.quote("class[[:space:]]+.*Manager|Singleton|Service|Controller")
            + f" {shlex.quote(root)} | grep -i {shlex.quote(term)} || true"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print_section("Events")
        cmd = (
            "grep -RIn --include='*.cs' -E "
            + shlex.quote(
                r"event[[:space:]]+|UnityEvent|\+=|-=|Invoke\(|Publish\(|Subscribe\(|MessageBus|EventBus|Signal"
            )
            + f" {shlex.quote(root)} | grep -i {shlex.quote(term)} || true"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print()
        print("Trace complete.")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
