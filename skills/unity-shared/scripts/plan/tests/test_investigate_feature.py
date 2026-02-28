#!/usr/bin/env python3
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "investigate_feature.py"

import investigate_feature as mod


def test_run_capture_returns_stdout():
    out = mod.run_capture("echo hello")
    assert out.strip() == "hello"


def test_run_capture_returns_empty_on_failure():
    out = mod.run_capture("false")
    assert out == ""


def test_print_section_with_output(capsys):
    result = mod.print_section("Title", "some output\n", "fallback")
    captured = capsys.readouterr()
    assert "=== Title ===" in captured.out
    assert "some output" in captured.out
    assert "fallback" not in captured.out
    assert result == "some output\n"


def test_print_section_with_fallback(capsys):
    result = mod.print_section("Title", "", "fallback msg")
    captured = capsys.readouterr()
    assert "=== Title ===" in captured.out
    assert "fallback msg" in captured.out
    assert result == ""


def test_init_plan_folder_creates_structure():
    with tempfile.TemporaryDirectory() as tmpdir:
        with mock.patch("investigate_feature.Path") as MockPath:
            real_plan_dir = Path(tmpdir) / "documents" / "plans" / "test-feature"
            mock_div = mock.MagicMock()
            mock_div.__truediv__ = lambda s, o: real_plan_dir
            mock_div.as_posix.return_value = str(real_plan_dir)
            MockPath.return_value = mock_div

        real_plan_dir.mkdir(parents=True, exist_ok=True)
        (real_plan_dir / "patches").mkdir(exist_ok=True)
        assert real_plan_dir.exists()
        assert (real_plan_dir / "patches").exists()


def test_main_no_args(capsys):
    with mock.patch("sys.argv", ["investigate_feature.py"]):
        ret = mod.main()
    assert ret == 1
    captured = capsys.readouterr()
    assert "Usage" in captured.out


def test_main_init_no_plan_name(capsys):
    with mock.patch("sys.argv", ["investigate_feature.py", "--init"]):
        ret = mod.main()
    assert ret == 1
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_main_init_creates_folder(capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        with mock.patch("investigate_feature.Path") as MockPath:
            real_plan_dir = Path(tmpdir) / "documents" / "plans" / "my-plan"
            real_plan_dir.mkdir(parents=True, exist_ok=True)
            (real_plan_dir / "patches").mkdir(exist_ok=True)

            mock_instance = mock.MagicMock()
            mock_instance.__truediv__ = (
                lambda s, o: real_plan_dir if o == "my-plan" else Path(tmpdir) / o
            )
            mock_instance.as_posix.return_value = str(real_plan_dir)

            MockPath.return_value = mock_instance

        assert real_plan_dir.exists()


def test_investigate_runs_without_assets(capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        with mock.patch("investigate_feature.run_capture", return_value=""):
            mod.investigate("SomeFeature")

        captured = capsys.readouterr()
        assert "Existing Classes" in captured.out
        assert "Test Files" in captured.out
        assert "Config/Data Files" in captured.out
        assert "Related Prefabs" in captured.out
        assert "Integration Points" in captured.out
        assert "Existing vs Needs Creation" in captured.out


def test_investigate_with_results(capsys):
    def fake_capture(cmd):
        if "class" in cmd:
            return "Assets/Scripts/Player.cs:10: public class PlayerController\n"
        return ""

    with mock.patch("investigate_feature.run_capture", side_effect=fake_capture):
        results = mod.investigate("Player")

    assert "PlayerController" in results["classes"]
    captured = capsys.readouterr()
    assert "Feature-related classes appear to exist" in captured.out


def test_cli_runs_as_subprocess():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "Usage" in result.stdout
