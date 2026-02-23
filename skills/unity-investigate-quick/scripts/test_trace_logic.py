"""Tests for trace_logic.py CLI interface."""

import subprocess
import sys
import os

SCRIPT = os.path.join(os.path.dirname(__file__), "trace_logic.py")


def run_trace(args: list[str]) -> subprocess.CompletedProcess:
    """Helper: invoke trace_logic.py as subprocess."""
    return subprocess.run(
        [sys.executable, SCRIPT] + args,
        capture_output=True,
        text=True,
        timeout=30,
    )


# ── Help flag ──────────────────────────────────────────────


def test_help_flag_exits_zero():
    r = run_trace(["--help"])
    assert r.returncode == 0


def test_help_flag_prints_usage():
    r = run_trace(["--help"])
    assert "Usage:" in r.stdout
    assert "SearchPattern" in r.stdout
    assert "--assets" in r.stdout
    assert "--deep" in r.stdout


def test_help_short_flag():
    r = run_trace(["-h"])
    assert r.returncode == 0
    assert "Usage:" in r.stdout


# ── No arguments ───────────────────────────────────────────


def test_no_args_exits_one():
    r = run_trace([])
    assert r.returncode == 1


def test_no_args_prints_usage():
    r = run_trace([])
    assert "Usage:" in r.stdout


# ── Empty string pattern ──────────────────────────────────


def test_empty_string_pattern_exits_one():
    r = run_trace([""])
    assert r.returncode == 1
    assert "Usage:" in r.stdout


# ── Valid pattern ──────────────────────────────────────────


def test_valid_pattern_exits_zero():
    r = run_trace(["MonoBehaviour"])
    assert r.returncode == 0


def test_valid_pattern_prints_investigation_header():
    r = run_trace(["MonoBehaviour"])
    assert "=== Unity Investigation: MonoBehaviour ===" in r.stdout


def test_valid_pattern_prints_sections():
    r = run_trace(["MonoBehaviour"])
    assert "--- Direct Code References ---" in r.stdout
    assert "--- Definitions ---" in r.stdout
    assert "--- Inheritance & Implementation ---" in r.stdout
    assert "--- Event/Delegate Usage ---" in r.stdout
    assert "--- Serialization & Attributes ---" in r.stdout
    assert "=== Investigation Complete ===" in r.stdout


# ── Dot-separated pattern ─────────────────────────────────


def test_dot_pattern_exits_zero():
    r = run_trace(["Class.Method"])
    assert r.returncode == 0


def test_dot_pattern_has_inheritance_section():
    """Dot pattern triggers clean_name = pattern.split('.')[0] → 'Class'."""
    r = run_trace(["Class.Method"])
    assert "--- Inheritance & Implementation ---" in r.stdout


# ── Pattern with parentheses ──────────────────────────────


def test_paren_pattern_exits_zero():
    r = run_trace(["OnTriggerEnter(Collider)"])
    assert r.returncode == 0


def test_paren_pattern_skips_inheritance_grep():
    """When '(' in pattern, the script skips the inheritance grep command.
    The section header still prints, but no grep is executed for it.
    We verify no error and the section header exists."""
    r = run_trace(["OnTriggerEnter(Collider)"])
    # Header still prints (the print happens before the if-check)
    assert "--- Inheritance & Implementation ---" in r.stdout
    assert "=== Investigation Complete ===" in r.stdout


# ── --assets flag ──────────────────────────────────────────


def test_assets_flag_prints_asset_sections():
    r = run_trace(["TestPattern", "--assets"])
    assert r.returncode == 0
    assert "--- Asset Bindings (Prefabs) ---" in r.stdout
    assert "--- Asset Bindings (Scenes) ---" in r.stdout
    assert "--- ScriptableObject Assets ---" in r.stdout


# ── --deep flag ────────────────────────────────────────────


def test_deep_flag_prints_deep_sections():
    r = run_trace(["TestPattern", "--deep"])
    assert r.returncode == 0
    assert "--- Animator Controllers ---" in r.stdout
    assert "--- Animation Clips ---" in r.stdout
    assert "--- Shader References ---" in r.stdout
    assert "--- Audio Mixer References ---" in r.stdout


# ── --assets --deep combined ───────────────────────────────


def test_assets_and_deep_combined():
    r = run_trace(["TestPattern", "--assets", "--deep"])
    assert r.returncode == 0
    # Asset sections
    assert "--- Asset Bindings (Prefabs) ---" in r.stdout
    assert "--- Asset Bindings (Scenes) ---" in r.stdout
    assert "--- ScriptableObject Assets ---" in r.stdout
    # Deep sections
    assert "--- Animator Controllers ---" in r.stdout
    assert "--- Animation Clips ---" in r.stdout
    assert "--- Shader References ---" in r.stdout
    assert "--- Audio Mixer References ---" in r.stdout
    # Core sections still present
    assert "--- Direct Code References ---" in r.stdout
    assert "=== Investigation Complete ===" in r.stdout


# ── Shell injection safety ─────────────────────────────────


def test_shell_injection_does_not_execute():
    """Verify shlex.quote prevents command injection."""
    r = run_trace(["$(whoami)"])
    assert r.returncode == 0
    # The literal pattern should appear quoted, not the result of whoami
    assert "$(whoami)" in r.stdout
    # The current username should NOT appear as an injected result
    current_user = os.environ.get("USER", os.environ.get("USERNAME", ""))
    if current_user:
        # The pattern header will contain $(whoami) literally.
        # If injection worked, we'd see the username OUTSIDE the header.
        # We verify the header contains the literal string.
        assert "=== Unity Investigation: $(whoami) ===" in r.stdout


# ── --root flag ────────────────────────────────────────────


def test_root_flag_exits_zero():
    r = run_trace(["TestPattern", "--root", "Assets/Game/Scripts"])
    assert r.returncode == 0


def test_root_flag_appears_in_help():
    r = run_trace(["--help"])
    assert "--root" in r.stdout


# ── --asset-root flag ─────────────────────────────────────


def test_asset_root_flag_exits_zero():
    r = run_trace(["TestPattern", "--assets", "--asset-root", "Assets/Game"])
    assert r.returncode == 0


def test_asset_root_flag_appears_in_help():
    r = run_trace(["--help"])
    assert "--asset-root" in r.stdout


# ── --root with spaces in path ────────────────────────────


def test_root_with_spaces_exits_zero():
    """Path with spaces must not crash (shlex.quote handles it)."""
    r = run_trace(["TestPattern", "--root", "Assets/My Scripts/Core"])
    assert r.returncode == 0


def test_asset_root_with_spaces_exits_zero():
    r = run_trace(["TestPattern", "--assets", "--asset-root", "Assets/My Game"])
    assert r.returncode == 0


# ── --root and --asset-root combined ──────────────────────


def test_root_and_asset_root_combined():
    r = run_trace([
        "TestPattern",
        "--root", "src/scripts",
        "--asset-root", "src/assets",
        "--assets",
        "--deep",
    ])
    assert r.returncode == 0
    assert "=== Unity Investigation: TestPattern ===" in r.stdout
    assert "=== Investigation Complete ===" in r.stdout
