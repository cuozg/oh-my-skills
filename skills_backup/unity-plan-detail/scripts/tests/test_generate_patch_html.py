#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "generate_patch_html.py"

import generate_patch_html as mod

SAMPLE_PATCH = """--- a/Assets/Scripts/Player.cs
+++ b/Assets/Scripts/Player.cs
@@ -10,6 +10,7 @@ public class Player : MonoBehaviour
     private int health;
     private float speed;
     private bool isAlive;
+    private int armor;
 
     void Start()
     {
"""

NEW_FILE_PATCH = """--- /dev/null
+++ b/Assets/Scripts/NewFile.cs
@@ -0,0 +1,5 @@
+using UnityEngine;
+
+public class NewFile : MonoBehaviour
+{
+}
"""

DELETE_PATCH = """--- a/Assets/Scripts/OldFile.cs
+++ /dev/null
@@ -1,3 +0,0 @@
-using UnityEngine;
-
-public class OldFile {}
"""


def test_esc_html_entities():
    assert mod.esc("<div>") == "&lt;div&gt;"
    assert mod.esc("a&b") == "a&amp;b"


def test_parse_patch_modified_file():
    files = mod.parse_patch(SAMPLE_PATCH)
    assert len(files) == 1
    f = files[0]
    assert f["path"] == "Assets/Scripts/Player.cs"
    assert f["status"] == "modified"
    assert f["additions"] == 1
    assert f["deletions"] == 0
    assert len(f["hunks"]) == 1


def test_parse_patch_new_file():
    files = mod.parse_patch(NEW_FILE_PATCH)
    assert len(files) == 1
    f = files[0]
    assert f["status"] == "added"
    assert f["path"] == "Assets/Scripts/NewFile.cs"
    assert f["additions"] == 5
    assert f["deletions"] == 0


def test_parse_patch_deleted_file():
    files = mod.parse_patch(DELETE_PATCH)
    assert len(files) == 1
    f = files[0]
    assert f["status"] == "deleted"
    assert f["path"] == "Assets/Scripts/OldFile.cs"
    assert f["deletions"] == 3


def test_parse_patch_empty():
    files = mod.parse_patch("")
    assert files == []


def test_parse_patch_multi_file():
    combined = SAMPLE_PATCH + "\n" + NEW_FILE_PATCH
    files = mod.parse_patch(combined)
    assert len(files) == 2


def test_render_file_row():
    f = {"path": "test.cs", "additions": 3, "deletions": 1}
    html = mod.render_file_row(f)
    assert "test.cs" in html
    assert "+3" in html
    assert "-1" in html


def test_render_diff_section():
    files = mod.parse_patch(SAMPLE_PATCH)
    html = mod.render_diff_section(files[0])
    assert "Player.cs" in html
    assert "Modified" in html
    assert "private int armor" in html


def test_render_task_section():
    files = mod.parse_patch(SAMPLE_PATCH)
    meta = {"subject": "Add armor field", "type": "Logic", "cost": "S", "wave": 1}
    html = mod.render_task_section("TASK-1.1", files, meta, "./patches/TASK-1.1.patch")
    assert "TASK-1.1" in html
    assert "Add armor field" in html
    assert "Logic" in html
    assert "badge-s" in html
    assert "W1" in html


def test_render_task_section_no_meta():
    files = mod.parse_patch(SAMPLE_PATCH)
    html = mod.render_task_section("TASK-2.1", files, None, "./patches/TASK-2.1.patch")
    assert "TASK-2.1" in html


def test_load_tasks_meta_none():
    result = mod.load_tasks_meta(None)
    assert result == {}


def test_load_tasks_meta_missing_file():
    result = mod.load_tasks_meta(Path("/nonexistent/file.json"))
    assert result == {}


def test_load_tasks_meta_list_format():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([{"id": "TASK-1.1", "subject": "Test", "type": "Logic"}], f)
        f.flush()
        result = mod.load_tasks_meta(Path(f.name))
    assert "TASK-1.1" in result
    assert result["TASK-1.1"]["subject"] == "Test"
    Path(f.name).unlink()


def test_generate_per_task_html():
    files = mod.parse_patch(SAMPLE_PATCH)
    template = "<html>{{FEATURE_TITLE}} {{TASK_COUNT}} {{FILE_COUNT}} {{ADDITIONS}} {{DELETIONS}} {{PLAN_DATE}} {{TASK_SECTIONS}}</html>"
    task_patches = [("TASK-1.1", files, "./patches/TASK-1.1.patch")]
    result = mod.generate_per_task_html(
        task_patches, {}, "TestFeature", "2025-01-01", template
    )
    assert "TestFeature" in result
    assert "1" in result
    assert "TASK-1.1" in result


def test_generate_legacy_html():
    files = mod.parse_patch(SAMPLE_PATCH)
    template = "<html>{{FEATURE_TITLE}} {{TASK_SECTIONS}}</html>"
    result = mod.generate_legacy_html(files, "Legacy", "2025-01-01", template)
    assert "Legacy" in result


def test_cli_no_args():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0


def test_cli_per_task_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        patches_dir = Path(tmpdir) / "patches"
        patches_dir.mkdir()
        (patches_dir / "TASK-1.1.patch").write_text(SAMPLE_PATCH)

        tasks_json = Path(tmpdir) / "tasks.json"
        tasks_json.write_text(
            json.dumps(
                [
                    {
                        "id": "TASK-1.1",
                        "subject": "Test",
                        "type": "Logic",
                        "cost": "M",
                        "wave": 1,
                    }
                ]
            )
        )

        template = Path(tmpdir) / "template.html"
        template.write_text(
            "<html>{{FEATURE_TITLE}} {{TASK_COUNT}} {{FILE_COUNT}} {{ADDITIONS}} {{DELETIONS}} {{PLAN_DATE}} {{TASK_SECTIONS}}</html>"
        )

        output = Path(tmpdir) / "output.html"

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(patches_dir),
                str(output),
                "--title",
                "TestFeature",
                "--tasks-json",
                str(tasks_json),
                "--template",
                str(template),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert output.exists()
        content = output.read_text()
        assert "TestFeature" in content
        assert "TASK-1.1" in content
