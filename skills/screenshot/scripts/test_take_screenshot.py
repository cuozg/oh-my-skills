"""Tests for take_screenshot.py — all subprocess and platform ops are mocked."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

# ---------------------------------------------------------------------------
# Import the module under test
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
import take_screenshot as ts  # noqa: E402


# ===========================================================================
# parse_region
# ===========================================================================


class TestParseRegion:
    def test_valid_region(self):
        assert ts.parse_region("10,20,640,480") == (10, 20, 640, 480)

    def test_negative_xy_allowed(self):
        # negative x/y are valid (multi-monitor offsets)
        assert ts.parse_region("-10,-20,800,600") == (-10, -20, 800, 600)

    def test_zero_width_raises(self):
        with pytest.raises(argparse.ArgumentTypeError, match="positive"):
            ts.parse_region("0,0,0,100")

    def test_zero_height_raises(self):
        with pytest.raises(argparse.ArgumentTypeError, match="positive"):
            ts.parse_region("0,0,100,0")

    def test_non_integer_raises(self):
        with pytest.raises(argparse.ArgumentTypeError, match="integers"):
            ts.parse_region("a,b,c,d")

    def test_wrong_number_of_parts_raises(self):
        with pytest.raises(argparse.ArgumentTypeError, match="x,y,w,h"):
            ts.parse_region("10,20,30")

    def test_extra_spaces_tolerated(self):
        assert ts.parse_region(" 5 , 5 , 100 , 200 ") == (5, 5, 100, 200)


# ===========================================================================
# test_mode_enabled
# ===========================================================================


class TestTestModeEnabled:
    def _env(self, value):
        return {ts.TEST_MODE_ENV: value}

    def test_not_set_returns_false(self, monkeypatch):
        monkeypatch.delenv(ts.TEST_MODE_ENV, raising=False)
        assert ts.test_mode_enabled() is False

    @pytest.mark.parametrize(
        "value", ["1", "true", "TRUE", "True", "yes", "YES", "on", "ON"]
    )
    def test_truthy_values(self, monkeypatch, value):
        monkeypatch.setenv(ts.TEST_MODE_ENV, value)
        assert ts.test_mode_enabled() is True

    @pytest.mark.parametrize("value", ["0", "false", "no", "off", ""])
    def test_falsy_values(self, monkeypatch, value):
        monkeypatch.setenv(ts.TEST_MODE_ENV, value)
        assert ts.test_mode_enabled() is False


# ===========================================================================
# normalize_platform
# ===========================================================================


class TestNormalizePlatform:
    @pytest.mark.parametrize(
        "raw", ["darwin", "mac", "macos", "osx", "Darwin", "macOS"]
    )
    def test_macos_variants(self, raw):
        assert ts.normalize_platform(raw) == "Darwin"

    @pytest.mark.parametrize("raw", ["linux", "ubuntu", "Linux"])
    def test_linux_variants(self, raw):
        assert ts.normalize_platform(raw) == "Linux"

    @pytest.mark.parametrize("raw", ["windows", "win", "Windows"])
    def test_windows_variants(self, raw):
        assert ts.normalize_platform(raw) == "Windows"

    def test_unknown_returned_as_is(self):
        assert ts.normalize_platform("FreeBSD") == "FreeBSD"


# ===========================================================================
# test_platform_override
# ===========================================================================


class TestTestPlatformOverride:
    def test_not_set_returns_none(self, monkeypatch):
        monkeypatch.delenv(ts.TEST_PLATFORM_ENV, raising=False)
        assert ts.test_platform_override() is None

    def test_set_returns_normalized(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_PLATFORM_ENV, "mac")
        assert ts.test_platform_override() == "Darwin"

    def test_linux(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_PLATFORM_ENV, "ubuntu")
        assert ts.test_platform_override() == "Linux"


# ===========================================================================
# parse_int_list
# ===========================================================================


class TestParseIntList:
    def test_basic(self):
        assert ts.parse_int_list("1,2,3") == [1, 2, 3]

    def test_non_int_skipped(self):
        assert ts.parse_int_list("1,abc,3") == [1, 3]

    def test_empty_string_returns_empty(self):
        assert ts.parse_int_list("") == []

    def test_spaces_stripped(self):
        assert ts.parse_int_list(" 10 , 20 ") == [10, 20]


# ===========================================================================
# test_window_ids / test_display_ids
# ===========================================================================


class TestTestWindowIds:
    def test_default(self, monkeypatch):
        monkeypatch.delenv(ts.TEST_WINDOWS_ENV, raising=False)
        ids = ts.test_window_ids()
        assert ids == [101, 102]

    def test_custom(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_WINDOWS_ENV, "200,201,202")
        assert ts.test_window_ids() == [200, 201, 202]

    def test_empty_falls_back_to_default_101(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_WINDOWS_ENV, "abc")
        assert ts.test_window_ids() == [101]


class TestTestDisplayIds:
    def test_default(self, monkeypatch):
        monkeypatch.delenv(ts.TEST_DISPLAYS_ENV, raising=False)
        assert ts.test_display_ids() == [1, 2]

    def test_custom(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_DISPLAYS_ENV, "3,4")
        assert ts.test_display_ids() == [3, 4]

    def test_empty_falls_back_to_1(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_DISPLAYS_ENV, "xyz")
        assert ts.test_display_ids() == [1]


# ===========================================================================
# write_test_png
# ===========================================================================


class TestWriteTestPng:
    def test_writes_valid_png_bytes(self, tmp_path):
        dest = tmp_path / "sub" / "shot.png"
        ts.write_test_png(dest)
        assert dest.exists()
        assert dest.read_bytes() == ts.TEST_PNG

    def test_creates_parent_directories(self, tmp_path):
        dest = tmp_path / "a" / "b" / "c" / "shot.png"
        ts.write_test_png(dest)
        assert dest.exists()


# ===========================================================================
# resolve_output_path
# ===========================================================================


class TestResolveOutputPath:
    def test_explicit_file_path(self, tmp_path):
        target = tmp_path / "myshot.png"
        path = ts.resolve_output_path(str(target), "default", "png", "Linux")
        assert path == target

    def test_explicit_directory_appends_filename(self, tmp_path):
        path = ts.resolve_output_path(str(tmp_path), "default", "png", "Linux")
        assert path.parent == tmp_path
        assert path.suffix == ".png"

    def test_explicit_path_without_extension_gets_one(self, tmp_path):
        target = tmp_path / "myshot"
        path = ts.resolve_output_path(str(target), "default", "jpg", "Linux")
        assert path.suffix == ".jpg"

    def test_temp_mode_uses_temp_dir(self):
        tmp_dir = Path(tempfile.gettempdir())
        path = ts.resolve_output_path(None, "temp", "png", "Linux")
        assert path.parent == tmp_dir
        assert path.stem.startswith("codex-shot-")

    def test_default_mode_linux_uses_pictures_if_exists(self, tmp_path, monkeypatch):
        pictures = tmp_path / "Pictures"
        pictures.mkdir()
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        path = ts.resolve_output_path(None, "default", "png", "Linux")
        assert path.parent == pictures

    def test_default_mode_linux_falls_back_to_home(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        path = ts.resolve_output_path(None, "default", "png", "Linux")
        assert path.parent == tmp_path

    def test_format_in_filename(self, tmp_path):
        path = ts.resolve_output_path(None, "temp", "jpg", "Linux")
        assert path.suffix == ".jpg"


# ===========================================================================
# multi_output_paths
# ===========================================================================


class TestMultiOutputPaths:
    def test_single_suffix_returns_base(self, tmp_path):
        base = tmp_path / "shot.png"
        result = ts.multi_output_paths(base, ["w101"])
        assert result == [base]

    def test_multiple_suffixes(self, tmp_path):
        base = tmp_path / "shot.png"
        result = ts.multi_output_paths(base, ["w101", "w102"])
        assert len(result) == 2
        assert result[0].name == "shot-w101.png"
        assert result[1].name == "shot-w102.png"

    def test_empty_suffix_list_returns_base(self, tmp_path):
        base = tmp_path / "shot.png"
        result = ts.multi_output_paths(base, [])
        assert result == [base]


# ===========================================================================
# run (subprocess wrapper)
# ===========================================================================


class TestRun:
    def test_raises_systemexit_on_file_not_found(self):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(SystemExit, match="required command not found"):
                ts.run(["nonexistent_command"])

    def test_raises_systemexit_on_nonzero_exit(self):
        err = subprocess.CalledProcessError(1, ["cmd"])
        with patch("subprocess.run", side_effect=err):
            with pytest.raises(SystemExit, match="command failed"):
                ts.run(["cmd"])

    def test_succeeds_silently(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            ts.run(["echo", "hello"])  # should not raise


# ===========================================================================
# mac_default_dir
# ===========================================================================


class TestMacDefaultDir:
    def test_returns_custom_location_if_set(self, tmp_path):
        custom = tmp_path / "Screenshots"
        custom.mkdir()
        proc_mock = MagicMock()
        proc_mock.stdout = str(custom) + "\n"
        with patch("subprocess.run", return_value=proc_mock):
            result = ts.mac_default_dir()
        assert result == custom

    def test_falls_back_to_desktop_on_empty_stdout(self, tmp_path):
        proc_mock = MagicMock()
        proc_mock.stdout = ""
        with patch("subprocess.run", return_value=proc_mock):
            with patch.object(Path, "home", return_value=tmp_path):
                result = ts.mac_default_dir()
        assert result == tmp_path / "Desktop"

    def test_falls_back_on_oserror(self, tmp_path):
        with patch("subprocess.run", side_effect=OSError):
            with patch.object(Path, "home", return_value=tmp_path):
                result = ts.mac_default_dir()
        assert result == tmp_path / "Desktop"


# ===========================================================================
# capture_macos
# ===========================================================================


class TestCaptureMacos:
    def _args(self, **kwargs):
        defaults = {
            "format": "png",
            "interactive": False,
            "window_id": None,
            "region": None,
            "app": None,
            "window_name": None,
            "active_window": False,
        }
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    def test_basic_fullscreen(self, tmp_path):
        output = tmp_path / "shot.png"
        with patch.object(ts, "run") as mock_run:
            ts.capture_macos(self._args(), output)
        cmd = mock_run.call_args[0][0]
        assert "screencapture" in cmd
        assert str(output) in cmd

    def test_with_region(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(region=(10, 20, 300, 400))
        with patch.object(ts, "run") as mock_run:
            ts.capture_macos(args, output)
        cmd = mock_run.call_args[0][0]
        assert "-R10,20,300,400" in cmd

    def test_with_window_id(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(window_id=42)
        with patch.object(ts, "run") as mock_run:
            ts.capture_macos(args, output)
        cmd = mock_run.call_args[0][0]
        assert "-l42" in cmd

    def test_with_display(self, tmp_path):
        output = tmp_path / "shot.png"
        with patch.object(ts, "run") as mock_run:
            ts.capture_macos(self._args(), output, display=2)
        cmd = mock_run.call_args[0][0]
        assert "-D2" in cmd

    def test_interactive_flag(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(interactive=True)
        with patch.object(ts, "run") as mock_run:
            ts.capture_macos(args, output)
        cmd = mock_run.call_args[0][0]
        assert "-i" in cmd

    def test_window_id_arg_overrides_args_window_id(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(window_id=99)
        with patch.object(ts, "run") as mock_run:
            ts.capture_macos(args, output, window_id=7)
        cmd = mock_run.call_args[0][0]
        assert "-l7" in cmd
        assert "-l99" not in cmd


# ===========================================================================
# capture_linux
# ===========================================================================


class TestCaptureLinux:
    def _args(self, **kwargs):
        defaults = {
            "region": None,
            "window_id": None,
            "active_window": False,
        }
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    def test_fullscreen_with_scrot(self, tmp_path):
        output = tmp_path / "shot.png"
        with patch(
            "shutil.which",
            side_effect=lambda x: "/usr/bin/scrot" if x == "scrot" else None,
        ):
            with patch.object(ts, "run") as mock_run:
                ts.capture_linux(self._args(), output)
        mock_run.assert_called_once_with(["scrot", str(output)])

    def test_fullscreen_with_gnome_screenshot_when_no_scrot(self, tmp_path):
        output = tmp_path / "shot.png"

        def which_side(x):
            return "/usr/bin/gnome-screenshot" if x == "gnome-screenshot" else None

        with patch("shutil.which", side_effect=which_side):
            with patch.object(ts, "run") as mock_run:
                ts.capture_linux(self._args(), output)
        mock_run.assert_called_once_with(["gnome-screenshot", "-f", str(output)])

    def test_no_tool_raises(self, tmp_path):
        output = tmp_path / "shot.png"
        with patch("shutil.which", return_value=None):
            with pytest.raises(SystemExit, match="no supported screenshot tool"):
                ts.capture_linux(self._args(), output)

    def test_region_with_scrot(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(region=(10, 20, 300, 400))
        with patch(
            "shutil.which",
            side_effect=lambda x: "/usr/bin/scrot" if x == "scrot" else None,
        ):
            with patch.object(ts, "run") as mock_run:
                ts.capture_linux(args, output)
        mock_run.assert_called_once_with(["scrot", "-a", "10,20,300,400", str(output)])

    def test_region_no_tool_raises(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(region=(0, 0, 100, 100))
        with patch("shutil.which", return_value=None):
            with pytest.raises(SystemExit, match="region capture requires"):
                ts.capture_linux(args, output)

    def test_window_id_with_imagemagick(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(window_id=55)
        with patch(
            "shutil.which",
            side_effect=lambda x: "/usr/bin/import" if x == "import" else None,
        ):
            with patch.object(ts, "run") as mock_run:
                ts.capture_linux(args, output)
        mock_run.assert_called_once_with(["import", "-window", "55", str(output)])

    def test_window_id_no_imagemagick_raises(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(window_id=55)
        with patch("shutil.which", return_value=None):
            with pytest.raises(SystemExit, match="window-id capture requires"):
                ts.capture_linux(args, output)

    def test_active_window_with_scrot(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(active_window=True)
        with patch(
            "shutil.which",
            side_effect=lambda x: "/usr/bin/scrot" if x == "scrot" else None,
        ):
            with patch.object(ts, "run") as mock_run:
                ts.capture_linux(args, output)
        mock_run.assert_called_once_with(["scrot", "-u", str(output)])

    def test_active_window_no_tool_raises(self, tmp_path):
        output = tmp_path / "shot.png"
        args = self._args(active_window=True)
        with patch("shutil.which", return_value=None):
            with pytest.raises(SystemExit, match="active-window capture requires"):
                ts.capture_linux(args, output)


# ===========================================================================
# swift_json (error paths only — never runs real swift)
# ===========================================================================


class TestSwiftJson:
    def test_swift_not_found_raises(self, tmp_path):
        fake_script = tmp_path / "fake.swift"
        fake_script.touch()
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(SystemExit, match="swift not found"):
                ts.swift_json(fake_script)

    def test_non_zero_exit_raises(self, tmp_path):
        fake_script = tmp_path / "fake.swift"
        fake_script.touch()
        err = subprocess.CalledProcessError(1, ["swift"])
        err.stderr = "compilation error"
        err.stdout = ""
        with patch("subprocess.run", side_effect=err):
            with pytest.raises(SystemExit, match="compilation error"):
                ts.swift_json(fake_script)

    def test_invalid_json_raises(self, tmp_path):
        fake_script = tmp_path / "fake.swift"
        fake_script.touch()
        proc_mock = MagicMock()
        proc_mock.stdout = "NOT_JSON"
        with patch("subprocess.run", return_value=proc_mock):
            with pytest.raises(SystemExit, match="invalid JSON"):
                ts.swift_json(fake_script)

    def test_valid_json_returned(self, tmp_path):
        fake_script = tmp_path / "fake.swift"
        fake_script.touch()
        proc_mock = MagicMock()
        proc_mock.stdout = '{"key": "value"}'
        with patch("subprocess.run", return_value=proc_mock):
            result = ts.swift_json(fake_script)
        assert result == {"key": "value"}


# ===========================================================================
# main() argument validation (mutual-exclusion checks)
# ===========================================================================


class TestMainMutualExclusion:
    """Test that conflicting argument combos cause SystemExit before any capture."""

    def _run_main(self, argv):
        with patch("sys.argv", ["take_screenshot.py"] + argv):
            with pytest.raises(SystemExit):
                ts.main()

    def test_region_and_window_id_conflict(self):
        self._run_main(["--region", "0,0,100,100", "--window-id", "5"])

    def test_region_and_active_window_conflict(self):
        self._run_main(["--region", "0,0,100,100", "--active-window"])

    def test_window_id_and_active_window_conflict(self):
        self._run_main(["--window-id", "5", "--active-window"])

    def test_app_and_window_id_conflict(self):
        self._run_main(["--app", "Safari", "--window-id", "5"])

    def test_region_and_app_conflict(self):
        self._run_main(["--region", "0,0,100,100", "--app", "Safari"])

    def test_interactive_and_app_conflict(self):
        self._run_main(["--interactive", "--app", "Safari"])

    def test_interactive_and_window_id_conflict(self):
        self._run_main(["--interactive", "--window-id", "5"])

    def test_interactive_and_active_window_conflict(self):
        self._run_main(["--interactive", "--active-window"])

    def test_list_windows_with_region_conflict(self):
        self._run_main(["--list-windows", "--region", "0,0,100,100"])

    def test_list_windows_with_window_id_conflict(self):
        self._run_main(["--list-windows", "--window-id", "5"])

    def test_app_flag_on_non_macos_raises(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_MODE_ENV, "1")
        monkeypatch.setenv(ts.TEST_PLATFORM_ENV, "linux")
        with patch("sys.argv", ["take_screenshot.py", "--app", "Terminal"]):
            with pytest.raises(SystemExit, match="macOS only"):
                ts.main()

    def test_list_windows_on_non_macos_raises(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_MODE_ENV, "1")
        monkeypatch.setenv(ts.TEST_PLATFORM_ENV, "linux")
        with patch("sys.argv", ["take_screenshot.py", "--list-windows"]):
            with pytest.raises(SystemExit, match="macOS only"):
                ts.main()


# ===========================================================================
# main() test-mode happy paths (no real subprocess)
# ===========================================================================


class TestMainTestMode:
    def _run(self, argv, env_extra=None):
        env = {ts.TEST_MODE_ENV: "1"}
        if env_extra:
            env.update(env_extra)
        with patch.dict(os.environ, env, clear=False):
            with patch("sys.argv", ["take_screenshot.py"] + argv):
                ts.main()

    def test_linux_fullscreen_writes_png(self, tmp_path):
        out = tmp_path / "shot.png"
        self._run(["--path", str(out)], {ts.TEST_PLATFORM_ENV: "linux"})
        assert out.exists()
        assert out.read_bytes() == ts.TEST_PNG

    def test_temp_mode_creates_file(self):
        tmp_dir = Path(tempfile.gettempdir())
        with patch.dict(
            os.environ, {ts.TEST_MODE_ENV: "1", ts.TEST_PLATFORM_ENV: "linux"}
        ):
            with patch("sys.argv", ["take_screenshot.py", "--mode", "temp"]):
                ts.main()
        # find any codex-shot file written
        candidates = list(tmp_dir.glob("codex-shot-*.png"))
        assert len(candidates) >= 1

    def test_darwin_single_display(self, tmp_path, capsys):
        out = tmp_path / "shot.png"
        self._run(
            ["--path", str(out)],
            {
                ts.TEST_PLATFORM_ENV: "darwin",
                ts.TEST_DISPLAYS_ENV: "1",
            },
        )
        # Single display → base path used directly
        assert out.exists()
        captured = capsys.readouterr()
        assert str(out) in captured.out

    def test_darwin_multiple_displays(self, tmp_path, capsys):
        out = tmp_path / "shot.png"
        self._run(
            ["--path", str(out)],
            {
                ts.TEST_PLATFORM_ENV: "darwin",
                ts.TEST_DISPLAYS_ENV: "1,2",
            },
        )
        assert (tmp_path / "shot-d1.png").exists()
        assert (tmp_path / "shot-d2.png").exists()

    def test_darwin_window_mode(self, tmp_path, capsys):
        out = tmp_path / "shot.png"
        self._run(
            ["--path", str(out), "--active-window"],
            {
                ts.TEST_PLATFORM_ENV: "darwin",
                ts.TEST_WINDOWS_ENV: "200",
            },
        )
        assert (tmp_path / "shot.png").exists() or (tmp_path / "shot-w200.png").exists()

    def test_darwin_list_windows_prints_table(self, capsys):
        with patch.dict(
            os.environ,
            {
                ts.TEST_MODE_ENV: "1",
                ts.TEST_PLATFORM_ENV: "darwin",
                ts.TEST_WINDOWS_ENV: "101,102",
            },
        ):
            with patch("sys.argv", ["take_screenshot.py", "--list-windows"]):
                ts.main()
        out = capsys.readouterr().out
        assert "101" in out
        assert "102" in out

    def test_windows_platform_raises(self, tmp_path):
        # Windows/unsupported-platform errors are in the non-test-mode branch;
        # mock platform.system and capture to a temp path so no real screencapture runs.
        out = tmp_path / "shot.png"
        with patch("platform.system", return_value="Windows"):
            with patch("sys.argv", ["take_screenshot.py", "--path", str(out)]):
                with pytest.raises(SystemExit, match="PowerShell"):
                    ts.main()

    def test_unknown_platform_raises(self, tmp_path):
        out = tmp_path / "shot.png"
        with patch("platform.system", return_value="FreeBSD"):
            with patch("sys.argv", ["take_screenshot.py", "--path", str(out)]):
                with pytest.raises(SystemExit, match="unsupported platform"):
                    ts.main()


# ===========================================================================
# macos_display_indexes
# ===========================================================================


class TestMacosDisplayIndexes:
    def test_parses_display_list(self):
        payload = {"displays": [1, 2, 3]}
        with patch.object(ts, "swift_json", return_value=payload):
            result = ts.macos_display_indexes()
        assert result == [1, 2, 3]

    def test_ignores_zero_and_negatives(self):
        payload = {"displays": [-1, 0, 1, 2]}
        with patch.object(ts, "swift_json", return_value=payload):
            result = ts.macos_display_indexes()
        assert result == [1, 2]

    def test_empty_falls_back_to_1(self):
        with patch.object(ts, "swift_json", return_value={"displays": []}):
            result = ts.macos_display_indexes()
        assert result == [1]

    def test_non_int_items_skipped(self):
        payload = {"displays": ["bad", 3, None]}
        with patch.object(ts, "swift_json", return_value=payload):
            result = ts.macos_display_indexes()
        assert result == [3]


# ===========================================================================
# macos_window_ids
# ===========================================================================


class TestMacosWindowIds:
    def _args(self, **kwargs):
        defaults = {"active_window": False, "app": None, "window_name": None}
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    def test_selected_window_returned(self):
        payload = {"selected": {"id": 77}}
        with patch.object(ts, "macos_window_payload", return_value=payload):
            result = ts.macos_window_ids(
                self._args(active_window=True), capture_all=False
            )
        assert result == [77]

    def test_all_windows_listed(self):
        payload = {"windows": [{"id": 10}, {"id": 20}]}
        with patch.object(ts, "macos_window_payload", return_value=payload):
            result = ts.macos_window_ids(self._args(), capture_all=True)
        assert result == [10, 20]

    def test_no_window_raises(self):
        payload = {"windows": [], "selected": {}}
        with patch.object(ts, "macos_window_payload", return_value=payload):
            with pytest.raises(SystemExit, match="no matching macOS window"):
                ts.macos_window_ids(self._args(), capture_all=False)


# ===========================================================================
# ensure_macos_permissions
# ===========================================================================


class TestEnsureMacosPermissions:
    def test_sandbox_env_raises(self, monkeypatch):
        monkeypatch.setenv("CODEX_SANDBOX", "1")
        with pytest.raises(SystemExit, match="sandbox"):
            ts.ensure_macos_permissions()

    def test_already_granted_returns_early(self, monkeypatch):
        monkeypatch.delenv("CODEX_SANDBOX", raising=False)
        with patch.object(ts, "macos_screen_capture_granted", return_value=True):
            with patch("subprocess.run") as mock_run:
                ts.ensure_macos_permissions()
        mock_run.assert_not_called()

    def test_not_granted_after_request_raises(self, monkeypatch):
        monkeypatch.delenv("CODEX_SANDBOX", raising=False)
        with patch.object(ts, "macos_screen_capture_granted", return_value=False):
            with patch("subprocess.run"):
                with pytest.raises(SystemExit, match="Screen Recording permission"):
                    ts.ensure_macos_permissions()


# ===========================================================================
# resolve_test_macos_windows
# ===========================================================================


class TestResolveTestMacosWindows:
    def _args(self, **kwargs):
        defaults = {"active_window": False, "app": None, "window_name": None}
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    def test_active_window_returns_first_only(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_WINDOWS_ENV, "101,102,103")
        result = ts.resolve_test_macos_windows(self._args(active_window=True))
        assert result == [101]

    def test_not_active_window_returns_all(self, monkeypatch):
        monkeypatch.setenv(ts.TEST_WINDOWS_ENV, "101,102")
        result = ts.resolve_test_macos_windows(self._args(active_window=False))
        assert result == [101, 102]
