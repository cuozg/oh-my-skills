#!/usr/bin/env python3
import argparse
import shlex
import subprocess
import sys


class Args(argparse.Namespace):
    pattern: str | None = None
    assets: bool = False
    deep: bool = False
    root: str = "Assets/Scripts"
    asset_root: str = "Assets"
    help: bool = False


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
    print(f"Usage: {script_name} [SearchPattern] [--assets] [--deep] [--root PATH] [--asset-root PATH]")
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
    quoted_pattern = shlex.quote(pattern)
    root = args.root
    asset_root = args.asset_root
    quoted_root = shlex.quote(root)
    quoted_asset_root = shlex.quote(asset_root)

    try:
        print(f"=== Unity Investigation: {pattern} ===")

        print("\n--- Direct Code References ---")
        cmd = (
            f"grep -rn {quoted_pattern} {quoted_root} --include='*.cs' "
            "| grep -v 'public class' | grep -v 'public interface' | head -n 30"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print("\n--- Definitions ---")
        cmd = (
            "grep -rn "
            + shlex.quote(
                f"class {pattern}\\b\\|interface {pattern}\\b\\|struct {pattern}\\b\\|enum {pattern}\\b"
            )
            + f" {quoted_root} --include='*.cs'"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print("\n--- Inheritance & Implementation ---")
        if "(" not in pattern:
            clean_name = pattern.split(".")[0]
            cmd = (
                "grep -rn "
                + shlex.quote(f":.*\\b{clean_name}\\b")
                + f" {quoted_root} --include='*.cs' | head -n 20"
            )
            _ = sys.stdout.write(run_shell(cmd))

        print("\n--- Event/Delegate Usage ---")
        cmd = (
            "grep -rn "
            + shlex.quote(
                f"event.*{pattern}\\|Action.*{pattern}\\|Func.*{pattern}\\|UnityEvent.*{pattern}\\|delegate.*{pattern}"
            )
            + f" {quoted_root} --include='*.cs' | head -n 15"
        )
        _ = sys.stdout.write(run_shell(cmd))

        print("\n--- Serialization & Attributes ---")
        cmd = (
            "grep -rn "
            + shlex.quote(
                f"\\[Serializable\\].*{pattern}\\|\\[SerializeField\\].*{pattern}\\|ScriptableObject.*{pattern}"
            )
            + f" {quoted_root} --include='*.cs' | head -n 10"
        )
        _ = sys.stdout.write(run_shell(cmd))

        if args.assets:
            print("\n--- Asset Bindings (Prefabs) ---")
            cmd = f"grep -rl {quoted_pattern} {quoted_asset_root} --include='*.prefab' | head -n 10"
            _ = sys.stdout.write(run_shell(cmd))

            print("\n--- Asset Bindings (Scenes) ---")
            cmd = f"grep -rl {quoted_pattern} {quoted_asset_root} --include='*.unity' | head -n 10"
            _ = sys.stdout.write(run_shell(cmd))

            print("\n--- ScriptableObject Assets ---")
            cmd = f"grep -rl {quoted_pattern} {quoted_asset_root} --include='*.asset' | head -n 10"
            _ = sys.stdout.write(run_shell(cmd))

        if args.deep:
            print("\n--- Animator Controllers ---")
            cmd = f"grep -rl {quoted_pattern} {quoted_asset_root} --include='*.controller' | head -n 10"
            _ = sys.stdout.write(run_shell(cmd))

            print("\n--- Animation Clips ---")
            cmd = f"grep -rl {quoted_pattern} {quoted_asset_root} --include='*.anim' | head -n 10"
            _ = sys.stdout.write(run_shell(cmd))

            print("\n--- Shader References ---")
            cmd = (
                f"grep -rn {quoted_pattern} {quoted_asset_root} --include='*.shader' --include='*.cginc' --include='*.hlsl' "
                "| head -n 10"
            )
            _ = sys.stdout.write(run_shell(cmd))

            print("\n--- Audio Mixer References ---")
            cmd = f"grep -rl {quoted_pattern} {quoted_asset_root} --include='*.mixer' | head -n 5"
            _ = sys.stdout.write(run_shell(cmd))

        print("\n=== Investigation Complete ===")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
