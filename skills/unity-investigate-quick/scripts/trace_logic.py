#!/usr/bin/env python3
"""Unity codebase tracer — pure Python, no shell dependencies."""

import argparse
import os
import re
import sys


class Args(argparse.Namespace):
    pattern: str | None = None
    assets: bool = False
    deep: bool = False
    root: str = "Assets/Scripts"
    asset_root: str = "Assets"
    help: bool = False


def _walk_files(directory: str, extensions: tuple[str, ...]) -> list[str]:
    """Collect files matching extensions under directory, sorted for determinism."""
    matches: list[str] = []
    if not os.path.isdir(directory):
        return matches
    for dirpath, _, filenames in os.walk(directory):
        for fname in filenames:
            if fname.endswith(extensions):
                matches.append(os.path.join(dirpath, fname))
    matches.sort()
    return matches


def _grep_lines(
    directory: str,
    extensions: tuple[str, ...],
    regex: re.Pattern[str],
    *,
    exclude_patterns: list[re.Pattern[str]] | None = None,
    limit: int = 0,
    files_only: bool = False,
) -> list[str]:
    """Search files for regex matches; return 'file:line:content' or file paths."""
    results: list[str] = []
    for fpath in _walk_files(directory, extensions):
        try:
            with open(fpath, encoding="utf-8", errors="replace") as fh:
                if files_only:
                    for line in fh:
                        if regex.search(line):
                            results.append(fpath)
                            break
                else:
                    for lineno, line in enumerate(fh, 1):
                        if regex.search(line):
                            if exclude_patterns and any(
                                ep.search(line) for ep in exclude_patterns
                            ):
                                continue
                            results.append(f"{fpath}:{lineno}:{line.rstrip()}")
                if 0 < limit <= len(results):
                    break
        except OSError:
            continue
    if 0 < limit < len(results):
        results = results[:limit]
    return results


def _print_results(results: list[str]) -> None:
    for r in results:
        print(r)


def print_usage(script_name: str) -> None:
    print(
        f"Usage: {script_name} [SearchPattern] [--assets] [--deep] [--root PATH] [--asset-root PATH]"
    )
    print("  SearchPattern   Class name, method name, or ClassName.MethodName")
    print("  --assets        Include asset search (prefabs, scenes, ScriptableObjects)")
    print("  --deep          Include animation, audio, and shader references")
    print("  --root PATH     Code search directory (default: Assets/Scripts)")
    print("  --asset-root PATH  Asset search directory (default: Assets)")


def main() -> int:
    script_name = sys.argv[0]

    parser = argparse.ArgumentParser(add_help=False)
    _ = parser.add_argument("pattern", nargs="?")
    _ = parser.add_argument("--assets", action="store_true")
    _ = parser.add_argument("--deep", action="store_true")
    _ = parser.add_argument("--root", default="Assets/Scripts")
    _ = parser.add_argument("--asset-root", default="Assets")
    _ = parser.add_argument("-h", "--help", action="store_true")

    args = parser.parse_args(sys.argv[1:], namespace=Args())

    if args.help:
        print_usage(script_name)
        return 0
    if not args.pattern:
        print_usage(script_name)
        return 1

    pattern = args.pattern
    root = args.root
    asset_root = args.asset_root
    escaped = re.escape(pattern)

    try:
        print(f"=== Unity Investigation: {pattern} ===")

        print("\n--- Direct Code References ---")
        excl = [re.compile(r"public\s+class\b"), re.compile(r"public\s+interface\b")]
        _print_results(
            _grep_lines(
                root, (".cs",), re.compile(escaped), exclude_patterns=excl, limit=30
            )
        )

        print("\n--- Definitions ---")
        defn_re = re.compile(rf"(?:class|interface|struct|enum)\s+{escaped}\b")
        _print_results(_grep_lines(root, (".cs",), defn_re))

        print("\n--- Inheritance & Implementation ---")
        if "(" not in pattern:
            clean_name = re.escape(pattern.split(".")[0])
            inherit_re = re.compile(rf":\s*.*\b{clean_name}\b")
            _print_results(_grep_lines(root, (".cs",), inherit_re, limit=20))

        print("\n--- Event/Delegate Usage ---")
        event_re = re.compile(rf"(?:event|Action|Func|UnityEvent|delegate).*{escaped}")
        _print_results(_grep_lines(root, (".cs",), event_re, limit=15))

        print("\n--- Serialization & Attributes ---")
        serial_re = re.compile(
            rf"(?:\[Serializable\]|\[SerializeField\]|ScriptableObject).*{escaped}"
        )
        _print_results(_grep_lines(root, (".cs",), serial_re, limit=10))

        if args.assets:
            print("\n--- Asset Bindings (Prefabs) ---")
            _print_results(
                _grep_lines(
                    asset_root,
                    (".prefab",),
                    re.compile(escaped),
                    files_only=True,
                    limit=10,
                )
            )

            print("\n--- Asset Bindings (Scenes) ---")
            _print_results(
                _grep_lines(
                    asset_root,
                    (".unity",),
                    re.compile(escaped),
                    files_only=True,
                    limit=10,
                )
            )

            print("\n--- ScriptableObject Assets ---")
            _print_results(
                _grep_lines(
                    asset_root,
                    (".asset",),
                    re.compile(escaped),
                    files_only=True,
                    limit=10,
                )
            )

        if args.deep:
            print("\n--- Animator Controllers ---")
            _print_results(
                _grep_lines(
                    asset_root,
                    (".controller",),
                    re.compile(escaped),
                    files_only=True,
                    limit=10,
                )
            )

            print("\n--- Animation Clips ---")
            _print_results(
                _grep_lines(
                    asset_root,
                    (".anim",),
                    re.compile(escaped),
                    files_only=True,
                    limit=10,
                )
            )

            print("\n--- Shader References ---")
            exts = (".shader", ".cginc", ".hlsl")
            _print_results(_grep_lines(asset_root, exts, re.compile(escaped), limit=10))

            print("\n--- Audio Mixer References ---")
            _print_results(
                _grep_lines(
                    asset_root,
                    (".mixer",),
                    re.compile(escaped),
                    files_only=True,
                    limit=5,
                )
            )

        print("\n=== Investigation Complete ===")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
