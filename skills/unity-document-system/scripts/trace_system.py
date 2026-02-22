#!/usr/bin/env python3
"""Trace Unity system architecture signals for a search term."""

import argparse
import os
import subprocess
import sys
import tempfile


class Args(argparse.Namespace):
    term: str | None = None


def print_section(title: str) -> None:
    print()
    print(f"=== {title} ===")


def print_matches(root: str, title: str, pattern: str, limit: int = 40) -> None:
    print(f"- {title}")

    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as tmp:
        tmp_path = tmp.name
        _ = subprocess.run(
            ["grep", "-RInE", pattern, root, "--include=*.cs"],
            stdout=tmp,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        )

    try:
        with open(tmp_path, "r", encoding="utf-8", errors="ignore") as handle:
            matches = [line.rstrip("\n") for line in handle if line.strip()]
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    total = len(matches)
    if total == 0:
        print("  (none)")
        return

    for line in matches[:limit]:
        parts = line.split(":", 2)
        if len(parts) >= 2:
            print(f"  {parts[0]}:{parts[1]}")

    if total > limit:
        print(f"  ... ({total - limit} more)")
    print(f"  Total: {total} matches")


def count_file_lines(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return 0


def main() -> int:
    script_name = sys.argv[0]
    parser = argparse.ArgumentParser(add_help=True)
    _ = parser.add_argument("term", nargs="?")
    args = parser.parse_args(sys.argv[1:], namespace=Args())

    if not args.term:
        print(f'Usage: {script_name} "SearchTerm"')
        print(f'Example: {script_name} "Inventory"')
        return 1

    term = args.term
    root = "Assets/Scripts"

    if not os.path.isdir(root):
        print("Error: 'Assets/Scripts' not found. Run this from a Unity project root.")
        return 1

    try:
        print(f"=== Unity System Trace: {term} ===")
        print(f"Search root: {root}")

        print_section("Core classes")
        print_matches(
            root,
            "Class definitions matching term",
            rf"^[[:space:]]*(public|internal|private|protected)?[[:space:]]*(abstract[[:space:]]+|sealed[[:space:]]+|partial[[:space:]]+)*class[[:space:]]+[A-Za-z0-9_]*{term}[A-Za-z0-9_]*\\b",
        )
        print_matches(
            root,
            "Interface definitions matching term",
            rf"^[[:space:]]*(public|internal)?[[:space:]]*interface[[:space:]]+[A-Za-z0-9_]*{term}[A-Za-z0-9_]*\\b",
        )
        print_matches(
            root,
            "Enum definitions matching term",
            rf"^[[:space:]]*(public|internal)?[[:space:]]*enum[[:space:]]+[A-Za-z0-9_]*{term}[A-Za-z0-9_]*\\b",
        )

        print_section("Data structures")
        print_matches(
            root,
            "Structs and records matching term",
            rf"^[[:space:]]*(public|internal)?[[:space:]]*(readonly[[:space:]]+)?(partial[[:space:]]+)?(struct|record)[[:space:]]+[A-Za-z0-9_]*{term}[A-Za-z0-9_]*\\b",
        )
        print_matches(
            root,
            "Serializable/data annotations near term",
            rf"(\\[Serializable\\]|\\[SerializeField\\]|ScriptableObject).*{term}|{term}.*(\\[Serializable\\]|\\[SerializeField\\]|ScriptableObject)",
        )

        print_section("Managers/Controllers")
        print_matches(
            root,
            "Manager classes",
            rf"^[[:space:]]*(public|internal|private|protected)?[[:space:]]*(abstract[[:space:]]+|sealed[[:space:]]+|partial[[:space:]]+)*class[[:space:]]+[A-Za-z0-9_]*({term}[A-Za-z0-9_]*Manager|Manager[A-Za-z0-9_]*{term})\\b",
        )
        print_matches(
            root,
            "Controller classes",
            rf"^[[:space:]]*(public|internal|private|protected)?[[:space:]]*(abstract[[:space:]]+|sealed[[:space:]]+|partial[[:space:]]+)*class[[:space:]]+[A-Za-z0-9_]*({term}[A-Za-z0-9_]*Controller|Controller[A-Za-z0-9_]*{term})\\b",
        )
        print_matches(
            root,
            "MonoBehaviour and ScriptableObject types with term",
            rf"class[[:space:]]+[A-Za-z0-9_]*{term}[A-Za-z0-9_]*[[:space:]]*:[[:space:]]*.*(MonoBehaviour|ScriptableObject)",
        )

        print_section("Utilities")
        print_matches(
            root,
            "Utility/helper/service classes",
            rf"^[[:space:]]*(public|internal|private|protected)?[[:space:]]*(static[[:space:]]+|abstract[[:space:]]+|sealed[[:space:]]+|partial[[:space:]]+)*class[[:space:]]+[A-Za-z0-9_]*({term}[A-Za-z0-9_]*(Utility|Utils|Helper|Service)|(Utility|Utils|Helper|Service)[A-Za-z0-9_]*{term})\\b",
        )
        print_matches(root, "General references to term", rf"\\b{term}\\b", 60)

        print_section("File line counts")
        files_result = subprocess.run(
            ["grep", "-RIlE", rf"\\b{term}\\b", root, "--include=*.cs"],
            capture_output=True,
            text=True,
            check=False,
        )
        files = [line for line in files_result.stdout.splitlines() if line.strip()]
        if not files:
            print("(none)")
        else:
            for file_path in files:
                print(f"{file_path}:{count_file_lines(file_path)}")

        print()
        print("=== System trace complete ===")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
