#!/usr/bin/env python3
"""Unified Unity codebase tracer — routes to logic, system, or architecture sub-tracers."""

import argparse
import importlib.util
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Dynamic import helpers — load sibling skill scripts without modifying
# sys.path globally or requiring them to be installed packages.
# ---------------------------------------------------------------------------

_SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent  # skills/


def _import_from_path(module_name: str, file_path: Path):
    """Import a Python module from an absolute file path."""
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _get_trace_logic():
    """Import trace_logic from the same scripts/ directory."""
    return _import_from_path(
        "trace_logic",
        Path(__file__).resolve().parent / "trace_logic.py",
    )


def _get_trace_system():
    """Import trace_system from unity-document-system/scripts/."""
    return _import_from_path(
        "trace_system",
        _SKILLS_ROOT / "unity-document-system" / "scripts" / "trace_system.py",
    )


def _get_trace_architecture():
    """Import trace_architecture from unity-document-tdd/scripts/."""
    return _import_from_path(
        "trace_architecture",
        _SKILLS_ROOT / "unity-document-tdd" / "scripts" / "trace_architecture.py",
    )


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


def _run_logic(args: argparse.Namespace) -> int:
    """Run trace_logic with the original CLI interface."""
    mod = _get_trace_logic()
    # Reconstruct sys.argv as trace_logic.main() parses it directly
    argv = [sys.argv[0]]
    if args.pattern:
        argv.append(args.pattern)
    if args.assets:
        argv.append("--assets")
    if args.deep:
        argv.append("--deep")
    if args.root != "Assets/Scripts":
        argv.extend(["--root", args.root])
    if args.asset_root != "Assets":
        argv.extend(["--asset-root", args.asset_root])

    saved = sys.argv[:]
    try:
        sys.argv = argv
        return mod.main()
    finally:
        sys.argv = saved


def _run_system(args: argparse.Namespace) -> int:
    """Run trace_system with the original CLI interface."""
    mod = _get_trace_system()
    argv = [sys.argv[0]]
    if args.term:
        argv.append(args.term)

    saved = sys.argv[:]
    try:
        sys.argv = argv
        return mod.main()
    finally:
        sys.argv = saved


def _run_architecture(args: argparse.Namespace) -> int:
    """Run trace_architecture with the original CLI interface."""
    mod = _get_trace_architecture()
    argv = [sys.argv[0]]
    if args.term:
        argv.append(args.term)

    saved = sys.argv[:]
    try:
        sys.argv = argv
        return mod.main()
    finally:
        sys.argv = saved


# ---------------------------------------------------------------------------
# Argparse setup
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build the unified argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="trace_unified",
        description="Unified Unity codebase tracer. Routes to logic, system, or architecture sub-tracers.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Tracing mode")

    # -- logic subcommand (mirrors trace_logic.py interface) --
    logic = subparsers.add_parser(
        "logic",
        help="Trace logic flows, find callers/callees, analyze code patterns",
        description="Trace logic flows — wraps trace_logic.py. "
        "Searches for class/method references, inheritance, events, serialization.",
    )
    logic.add_argument(
        "pattern",
        nargs="?",
        help="Class name, method name, or ClassName.MethodName",
    )
    logic.add_argument(
        "--assets",
        action="store_true",
        help="Include asset search (prefabs, scenes, ScriptableObjects)",
    )
    logic.add_argument(
        "--deep",
        action="store_true",
        help="Include animation, audio, and shader references",
    )
    logic.add_argument(
        "--root",
        default="Assets/Scripts",
        help="Code search directory (default: Assets/Scripts)",
    )
    logic.add_argument(
        "--asset-root",
        default="Assets",
        help="Asset search directory (default: Assets)",
    )
    logic.set_defaults(func=_run_logic)

    # -- system subcommand (mirrors trace_system.py interface) --
    system = subparsers.add_parser(
        "system",
        help="Trace system architecture — managers, data structures, utilities",
        description="Trace system architecture — wraps trace_system.py. "
        "Finds core classes, data structures, managers/controllers, utilities.",
    )
    system.add_argument(
        "term",
        nargs="?",
        help="Search term (e.g. Inventory, Player, Quest)",
    )
    system.set_defaults(func=_run_system)

    # -- architecture subcommand (mirrors trace_architecture.py interface) --
    arch = subparsers.add_parser(
        "architecture",
        help="Trace architecture patterns — interfaces, abstracts, dependencies",
        description="Trace architecture patterns — wraps trace_architecture.py. "
        "Finds interfaces, abstract classes, concrete implementations, data models, events.",
    )
    arch.add_argument(
        "term",
        nargs="?",
        help="Search term (e.g. Inventory, Player, Quest)",
    )
    arch.set_defaults(func=_run_architecture)

    return parser


def main() -> int:
    """Entry point for the unified tracer."""
    parser = build_parser()
    args = parser.parse_args()

    if args.subcommand is None:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
