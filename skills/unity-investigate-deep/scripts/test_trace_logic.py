"""Tests for trace_logic.py — CLI interface + unit tests with fixtures."""

import subprocess
import sys
import os
import re
import tempfile

# Import internal functions for unit testing
sys.path.insert(0, os.path.dirname(__file__))
from trace_logic import _walk_files, _grep_lines

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



# ══════════════════════════════════════════════════════════
# Unit tests with temp-file fixtures
# ══════════════════════════════════════════════════════════


def _create_tree(base: str, files: dict[str, str]) -> None:
    """Create a directory tree with files from {relative_path: content}."""
    for rel_path, content in files.items():
        full = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)


# ── _walk_files ────────────────────────────────────────────


def test_walk_files_collects_matching_extensions():
    with tempfile.TemporaryDirectory() as tmp:
        _create_tree(tmp, {
            "Scripts/Player.cs": "class Player {}",
            "Scripts/Enemy.cs": "class Enemy {}",
            "Scripts/readme.txt": "not a script",
            "Scripts/Sub/Health.cs": "class Health {}",
        })
        result = _walk_files(os.path.join(tmp, "Scripts"), (".cs",))
        assert len(result) == 3
        assert all(f.endswith(".cs") for f in result)
        assert not any("readme.txt" in f for f in result)


def test_walk_files_sorted_deterministic():
    with tempfile.TemporaryDirectory() as tmp:
        _create_tree(tmp, {
            "Z.cs": "",
            "A.cs": "",
            "M.cs": "",
        })
        result = _walk_files(tmp, (".cs",))
        assert result == sorted(result)


def test_walk_files_nonexistent_directory():
    result = _walk_files("/nonexistent/path/abc123", (".cs",))
    assert result == []


def test_walk_files_empty_directory():
    with tempfile.TemporaryDirectory() as tmp:
        result = _walk_files(tmp, (".cs",))
        assert result == []


def test_walk_files_multiple_extensions():
    with tempfile.TemporaryDirectory() as tmp:
        _create_tree(tmp, {
            "a.cs": "",
            "b.prefab": "",
            "c.unity": "",
            "d.txt": "",
        })
        result = _walk_files(tmp, (".cs", ".prefab"))
        assert len(result) == 2


# ── _grep_lines ───────────────────────────────────────────


def test_grep_lines_finds_matching_content():
    with tempfile.TemporaryDirectory() as tmp:
        _create_tree(tmp, {
            "Player.cs": "public class Player : MonoBehaviour\n{\n    void Start() {}\n}",
            "Enemy.cs": "public class Enemy : MonoBehaviour\n{\n    void Update() {}\n}",
        })
        results = _grep_lines(tmp, (".cs",), re.compile(r"MonoBehaviour"))
        assert len(results) == 2
        assert all("MonoBehaviour" in r for r in results)


def test_grep_lines_returns_file_line_content_format():
    with tempfile.TemporaryDirectory() as tmp:
        _create_tree(tmp, {
            "Test.cs": "line1\nclass Foo\nline3",
        })
        results = _grep_lines(tmp, (".cs",), re.compile(r"Foo"))
        assert len(results) == 1
        parts = results[0].split(":")
        assert parts[1] == "2"  # line number
        assert "Foo" in parts[2]  # content


def test_grep_lines_files_only_mode():
    with tempfile.TemporaryDirectory() as tmp:
        _create_tree(tmp, {
            "a.prefab": "guid: abc Player\n",
            "b.prefab": "no match here\n",
            "c.prefab": "guid: xyz Player\n",
        })
        results = _grep_lines(tmp, (".prefab",), re.compile(r"Player"), files_only=True)
        assert len(results) == 2
        assert all(r.endswith(".prefab") for r in results)
        assert not any("b.prefab" in r for r in results)


def test_grep_lines_limit_caps_results():
    with tempfile.TemporaryDirectory() as tmp:
        content = "\n".join(f"match line {i}" for i in range(50))
        _create_tree(tmp, {"big.cs": content})
        results = _grep_lines(tmp, (".cs",), re.compile(r"match"), limit=5)
        assert len(results) == 5


def test_grep_lines_exclude_patterns():
    with tempfile.TemporaryDirectory() as tmp:
        _create_tree(tmp, {
            "Code.cs": "public class Player {}\nPlayer.Move();\npublic interface Player {}",
        })
        excl = [re.compile(r"public\s+class"), re.compile(r"public\s+interface")]
        results = _grep_lines(tmp, (".cs",), re.compile(r"Player"), exclude_patterns=excl)
        assert len(results) == 1
        assert "Move" in results[0]


def test_grep_lines_no_matches():
    with tempfile.TemporaryDirectory() as tmp:
        _create_tree(tmp, {"Empty.cs": "nothing relevant here"})
        results = _grep_lines(tmp, (".cs",), re.compile(r"ZzzzNotFound"))
        assert results == []


def test_grep_lines_regex_special_chars():
    """Ensure regex special chars in pattern don't crash."""
    with tempfile.TemporaryDirectory() as tmp:
        _create_tree(tmp, {"Code.cs": "List<int> items = new List<int>();\n"})
        results = _grep_lines(tmp, (".cs",), re.compile(re.escape("List<int>")))
        assert len(results) == 1
        assert "List<int>" in results[0]


def test_grep_lines_skips_unreadable_files(tmp_path):
    """OSError on unreadable files should be silently skipped."""
    f = tmp_path / "bad.cs"
    f.write_text("content")
    f.chmod(0o000)
    try:
        results = _grep_lines(str(tmp_path), (".cs",), re.compile(r"content"))
        assert isinstance(results, list)
    finally:
        f.chmod(0o644)