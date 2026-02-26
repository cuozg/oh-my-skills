"""Tests for trace_unified.py — subcommand routing, help, delegation."""

import subprocess
import sys
import os
from unittest.mock import patch, MagicMock

# conftest.py adds scripts/ to sys.path
from trace_unified import build_parser, main, _run_logic, _run_system, _run_architecture

SCRIPT = os.path.join(os.path.dirname(__file__), os.pardir, "trace_unified.py")


def run_unified(args: list[str]) -> subprocess.CompletedProcess:
    """Helper: invoke trace_unified.py as subprocess."""
    return subprocess.run(
        [sys.executable, SCRIPT] + args,
        capture_output=True,
        text=True,
        timeout=30,
    )


# ══════════════════════════════════════════════════════════
# Top-level help and no-args
# ══════════════════════════════════════════════════════════


def test_no_args_exits_one():
    r = run_unified([])
    assert r.returncode == 1


def test_no_args_prints_help():
    r = run_unified([])
    assert "logic" in r.stdout
    assert "system" in r.stdout
    assert "architecture" in r.stdout


def test_help_flag_exits_zero():
    r = run_unified(["--help"])
    assert r.returncode == 0


def test_help_flag_shows_subcommands():
    r = run_unified(["--help"])
    assert "logic" in r.stdout
    assert "system" in r.stdout
    assert "architecture" in r.stdout
    assert "Tracing mode" in r.stdout


# ══════════════════════════════════════════════════════════
# Logic subcommand help
# ══════════════════════════════════════════════════════════


def test_logic_help_exits_zero():
    r = run_unified(["logic", "--help"])
    assert r.returncode == 0


def test_logic_help_shows_all_flags():
    r = run_unified(["logic", "--help"])
    assert "--assets" in r.stdout
    assert "--deep" in r.stdout
    assert "--root" in r.stdout
    assert "--asset-root" in r.stdout
    assert "pattern" in r.stdout.lower()


def test_logic_no_pattern_exits_one():
    """trace_logic.main() returns 1 when no pattern given."""
    r = run_unified(["logic"])
    assert r.returncode == 1


def test_logic_with_pattern_exits_zero():
    r = run_unified(["logic", "TestPattern"])
    assert r.returncode == 0


def test_logic_with_pattern_prints_header():
    r = run_unified(["logic", "TestPattern"])
    assert "=== Unity Investigation: TestPattern ===" in r.stdout


def test_logic_with_pattern_prints_sections():
    r = run_unified(["logic", "TestPattern"])
    assert "--- Direct Code References ---" in r.stdout
    assert "--- Definitions ---" in r.stdout
    assert "=== Investigation Complete ===" in r.stdout


def test_logic_assets_flag():
    r = run_unified(["logic", "TestPattern", "--assets"])
    assert r.returncode == 0
    assert "--- Asset Bindings (Prefabs) ---" in r.stdout


def test_logic_deep_flag():
    r = run_unified(["logic", "TestPattern", "--deep"])
    assert r.returncode == 0
    assert "--- Animator Controllers ---" in r.stdout


def test_logic_root_flag():
    r = run_unified(["logic", "TestPattern", "--root", "src/scripts"])
    assert r.returncode == 0


def test_logic_asset_root_flag():
    r = run_unified(["logic", "TestPattern", "--assets", "--asset-root", "src/assets"])
    assert r.returncode == 0


# ══════════════════════════════════════════════════════════
# System subcommand help
# ══════════════════════════════════════════════════════════


def test_system_help_exits_zero():
    r = run_unified(["system", "--help"])
    assert r.returncode == 0


def test_system_help_shows_term():
    r = run_unified(["system", "--help"])
    assert "term" in r.stdout.lower()


def test_system_no_term_exits_one():
    r = run_unified(["system"])
    assert r.returncode == 1


def test_system_with_term_exits_one_no_assets_dir():
    """trace_system.main() returns 1 when Assets/Scripts doesn't exist."""
    r = run_unified(["system", "Inventory"])
    # Will exit 1 because Assets/Scripts doesn't exist in this repo
    assert r.returncode == 1


# ══════════════════════════════════════════════════════════
# Architecture subcommand help
# ══════════════════════════════════════════════════════════


def test_architecture_help_exits_zero():
    r = run_unified(["architecture", "--help"])
    assert r.returncode == 0


def test_architecture_help_shows_term():
    r = run_unified(["architecture", "--help"])
    assert "term" in r.stdout.lower()


def test_architecture_no_term_exits_one():
    r = run_unified(["architecture"])
    assert r.returncode == 1


def test_architecture_with_term_exits_one_no_assets_dir():
    """trace_architecture.main() returns 1 when Assets/Scripts doesn't exist."""
    r = run_unified(["architecture", "Inventory"])
    assert r.returncode == 1


# ══════════════════════════════════════════════════════════
# Invalid subcommand
# ══════════════════════════════════════════════════════════


def test_invalid_subcommand_exits_nonzero():
    r = run_unified(["bogus"])
    assert r.returncode != 0


# ══════════════════════════════════════════════════════════
# build_parser unit tests
# ══════════════════════════════════════════════════════════


def test_build_parser_returns_parser():
    parser = build_parser()
    assert hasattr(parser, "parse_args")


def test_build_parser_logic_subcommand():
    parser = build_parser()
    args = parser.parse_args(["logic", "Player"])
    assert args.subcommand == "logic"
    assert args.pattern == "Player"
    assert args.assets is False
    assert args.deep is False
    assert args.root == "Assets/Scripts"
    assert args.asset_root == "Assets"


def test_build_parser_logic_all_flags():
    parser = build_parser()
    args = parser.parse_args(
        [
            "logic",
            "Player",
            "--assets",
            "--deep",
            "--root",
            "src",
            "--asset-root",
            "res",
        ]
    )
    assert args.assets is True
    assert args.deep is True
    assert args.root == "src"
    assert args.asset_root == "res"


def test_build_parser_system_subcommand():
    parser = build_parser()
    args = parser.parse_args(["system", "Inventory"])
    assert args.subcommand == "system"
    assert args.term == "Inventory"


def test_build_parser_architecture_subcommand():
    parser = build_parser()
    args = parser.parse_args(["architecture", "Quest"])
    assert args.subcommand == "architecture"
    assert args.term == "Quest"


def test_build_parser_no_subcommand():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.subcommand is None


# ══════════════════════════════════════════════════════════
# main() routing tests (mocked)
# ══════════════════════════════════════════════════════════


def test_main_no_subcommand_returns_one():
    with patch("sys.argv", ["trace_unified"]):
        assert main() == 1


def test_main_routes_to_logic():
    mock_mod = MagicMock()
    mock_mod.main.return_value = 0
    with patch("sys.argv", ["trace_unified", "logic", "Player"]):
        with patch("trace_unified._get_trace_logic", return_value=mock_mod):
            result = main()
    assert result == 0
    mock_mod.main.assert_called_once()


def test_main_routes_to_system():
    mock_mod = MagicMock()
    mock_mod.main.return_value = 0
    with patch("sys.argv", ["trace_unified", "system", "Inventory"]):
        with patch("trace_unified._get_trace_system", return_value=mock_mod):
            result = main()
    assert result == 0
    mock_mod.main.assert_called_once()


def test_main_routes_to_architecture():
    mock_mod = MagicMock()
    mock_mod.main.return_value = 0
    with patch("sys.argv", ["trace_unified", "architecture", "Quest"]):
        with patch("trace_unified._get_trace_architecture", return_value=mock_mod):
            result = main()
    assert result == 0
    mock_mod.main.assert_called_once()


# ══════════════════════════════════════════════════════════
# _run_* restores sys.argv
# ══════════════════════════════════════════════════════════


def test_run_logic_restores_sysargv():
    original = sys.argv[:]
    mock_mod = MagicMock()
    mock_mod.main.return_value = 0
    parser = build_parser()
    args = parser.parse_args(["logic", "Test"])
    with patch("trace_unified._get_trace_logic", return_value=mock_mod):
        _run_logic(args)
    assert sys.argv == original


def test_run_system_restores_sysargv():
    original = sys.argv[:]
    mock_mod = MagicMock()
    mock_mod.main.return_value = 0
    parser = build_parser()
    args = parser.parse_args(["system", "Test"])
    with patch("trace_unified._get_trace_system", return_value=mock_mod):
        _run_system(args)
    assert sys.argv == original


def test_run_architecture_restores_sysargv():
    original = sys.argv[:]
    mock_mod = MagicMock()
    mock_mod.main.return_value = 0
    parser = build_parser()
    args = parser.parse_args(["architecture", "Test"])
    with patch("trace_unified._get_trace_architecture", return_value=mock_mod):
        _run_architecture(args)
    assert sys.argv == original


# ══════════════════════════════════════════════════════════
# sys.argv forwarding correctness
# ══════════════════════════════════════════════════════════


def test_logic_forwards_all_flags_via_sysargv():
    """Verify _run_logic builds correct sys.argv for trace_logic.main()."""
    captured_argv = []
    mock_mod = MagicMock()

    def capture_main():
        captured_argv.extend(sys.argv[:])
        return 0

    mock_mod.main.side_effect = capture_main
    parser = build_parser()
    args = parser.parse_args(
        [
            "logic",
            "Player",
            "--assets",
            "--deep",
            "--root",
            "src/scripts",
            "--asset-root",
            "src/assets",
        ]
    )
    with patch("trace_unified._get_trace_logic", return_value=mock_mod):
        _run_logic(args)

    # argv[0] is the script name, rest are forwarded flags
    assert "Player" in captured_argv
    assert "--assets" in captured_argv
    assert "--deep" in captured_argv
    assert "--root" in captured_argv
    assert "src/scripts" in captured_argv
    assert "--asset-root" in captured_argv
    assert "src/assets" in captured_argv


def test_logic_omits_default_root():
    """When root is default, don't pass --root to keep CLI clean."""
    captured_argv = []
    mock_mod = MagicMock()

    def capture_main():
        captured_argv.extend(sys.argv[:])
        return 0

    mock_mod.main.side_effect = capture_main
    parser = build_parser()
    args = parser.parse_args(["logic", "Player"])
    with patch("trace_unified._get_trace_logic", return_value=mock_mod):
        _run_logic(args)

    assert "--root" not in captured_argv
    assert "--asset-root" not in captured_argv
    assert "--assets" not in captured_argv
    assert "--deep" not in captured_argv


def test_system_forwards_term():
    captured_argv = []
    mock_mod = MagicMock()

    def capture_main():
        captured_argv.extend(sys.argv[:])
        return 0

    mock_mod.main.side_effect = capture_main
    parser = build_parser()
    args = parser.parse_args(["system", "Inventory"])
    with patch("trace_unified._get_trace_system", return_value=mock_mod):
        _run_system(args)

    assert "Inventory" in captured_argv


def test_architecture_forwards_term():
    captured_argv = []
    mock_mod = MagicMock()

    def capture_main():
        captured_argv.extend(sys.argv[:])
        return 0

    mock_mod.main.side_effect = capture_main
    parser = build_parser()
    args = parser.parse_args(["architecture", "Quest"])
    with patch("trace_unified._get_trace_architecture", return_value=mock_mod):
        _run_architecture(args)

    assert "Quest" in captured_argv
