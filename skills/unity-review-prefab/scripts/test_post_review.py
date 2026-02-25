#!/usr/bin/env python3
"""Unit tests for post_review.py."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Add parent dir to path so we can import post_review
sys.path.insert(0, os.path.dirname(__file__))
import post_review


def _make_run_result(stdout="", stderr="", returncode=0):
    """Create a mock subprocess.CompletedProcess."""
    r = MagicMock(spec=subprocess.CompletedProcess)
    r.stdout = stdout
    r.stderr = stderr
    r.returncode = returncode
    return r


class TestRunGh(unittest.TestCase):
    @patch("post_review.subprocess.run")
    def test_success(self, mock_run):
        mock_run.return_value = _make_run_result(stdout="ok")
        self.assertEqual(post_review.run_gh(["pr", "view"]), "ok")

    @patch("post_review.subprocess.run")
    def test_failure_raises(self, mock_run):
        mock_run.return_value = _make_run_result(stderr="not found", returncode=1)
        with self.assertRaises(RuntimeError):
            post_review.run_gh(["pr", "view"])


class TestMain(unittest.TestCase):
    def _make_json_file(self, data):
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, dir=tempfile.gettempdir()
        )
        json.dump(data, f)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def _make_bad_json_file(self, content):
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, dir=tempfile.gettempdir()
        )
        f.write(content)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    # --- Argument validation ---

    @patch("post_review.sys.argv", ["post_review.py"])
    def test_missing_args(self):
        with self.assertRaises(SystemExit) as ctx:
            post_review.main()
        self.assertEqual(ctx.exception.code, 1)

    @patch("post_review.sys.argv", ["post_review.py", "abc", "/tmp/r.json"])
    def test_invalid_pr_number(self):
        with self.assertRaises(SystemExit) as ctx:
            post_review.main()
        self.assertEqual(ctx.exception.code, 1)

    @patch("post_review.sys.argv", ["post_review.py", "42", "/nonexistent.json"])
    def test_missing_json_file(self):
        with self.assertRaises(SystemExit) as ctx:
            post_review.main()
        self.assertEqual(ctx.exception.code, 1)

    # --- gh CLI missing ---

    @patch("post_review.shutil.which", return_value=None)
    @patch("post_review.sys.argv", ["post_review.py", "42", "placeholder"])
    def test_missing_gh_cli(self, mock_which):
        jf = self._make_json_file({"body": "test", "event": "COMMENT"})
        with patch("post_review.sys.argv", ["post_review.py", "42", jf]):
            with self.assertRaises(SystemExit) as ctx:
                post_review.main()
            self.assertEqual(ctx.exception.code, 1)

    # --- Repo detection failure ---

    @patch("post_review.shutil.which", return_value="/usr/bin/gh")
    @patch("post_review.subprocess.run")
    def test_repo_detection_failure(self, mock_run, mock_which):
        jf = self._make_json_file({"body": "test"})
        mock_run.return_value = _make_run_result(stderr="error", returncode=1)
        with patch("post_review.sys.argv", ["post_review.py", "42", jf]):
            with self.assertRaises(SystemExit) as ctx:
                post_review.main()
            self.assertEqual(ctx.exception.code, 1)

    # --- Happy path: OPEN PR ---

    @patch("post_review.shutil.which", return_value="/usr/bin/gh")
    @patch("post_review.subprocess.run")
    def test_valid_review_post(self, mock_run, mock_which):
        jf = self._make_json_file(
            {"body": "review", "event": "COMMENT", "comments": []}
        )
        responses = [
            _make_run_result(stdout="owner/repo"),  # repo view
            _make_run_result(stdout="OPEN"),  # pr state
            _make_run_result(stdout="abc1234def5678"),  # commit SHA
            _make_run_result(stdout="{}"),  # API POST
        ]
        mock_run.side_effect = responses
        with patch("post_review.sys.argv", ["post_review.py", "42", jf]):
            post_review.main()  # Should not raise
        self.assertEqual(mock_run.call_count, 4)

    # --- Merged PR fallback ---

    @patch("post_review.shutil.which", return_value="/usr/bin/gh")
    @patch("post_review.subprocess.run")
    def test_merged_pr_fallback(self, mock_run, mock_which):
        jf = self._make_json_file({"body": "review body", "event": "COMMENT"})
        responses = [
            _make_run_result(stdout="owner/repo"),  # repo view
            _make_run_result(stdout="MERGED"),  # pr state
            _make_run_result(stdout=""),  # pr comment
        ]
        mock_run.side_effect = responses
        with patch("post_review.sys.argv", ["post_review.py", "42", jf]):
            post_review.main()
        # Should call pr comment, not api POST
        last_call_args = mock_run.call_args_list[-1][0][0]
        self.assertIn("comment", last_call_args)

    @patch("post_review.shutil.which", return_value="/usr/bin/gh")
    @patch("post_review.subprocess.run")
    def test_closed_pr_fallback(self, mock_run, mock_which):
        jf = self._make_json_file({"body": "review body"})
        responses = [
            _make_run_result(stdout="owner/repo"),
            _make_run_result(stdout="CLOSED"),
            _make_run_result(stdout=""),
        ]
        mock_run.side_effect = responses
        with patch("post_review.sys.argv", ["post_review.py", "42", jf]):
            post_review.main()
        last_call_args = mock_run.call_args_list[-1][0][0]
        self.assertIn("comment", last_call_args)

    # --- Empty commit SHA ---

    @patch("post_review.shutil.which", return_value="/usr/bin/gh")
    @patch("post_review.subprocess.run")
    def test_empty_commit_sha(self, mock_run, mock_which):
        jf = self._make_json_file({"body": "test"})
        responses = [
            _make_run_result(stdout="owner/repo"),
            _make_run_result(stdout="OPEN"),
            _make_run_result(stdout=""),  # empty SHA
        ]
        mock_run.side_effect = responses
        with patch("post_review.sys.argv", ["post_review.py", "42", jf]):
            with self.assertRaises(SystemExit) as ctx:
                post_review.main()
            self.assertEqual(ctx.exception.code, 1)

    # --- Invalid JSON ---

    @patch("post_review.shutil.which", return_value="/usr/bin/gh")
    @patch("post_review.subprocess.run")
    def test_invalid_json_content(self, mock_run, mock_which):
        jf = self._make_bad_json_file("{not valid json")
        responses = [
            _make_run_result(stdout="owner/repo"),
            _make_run_result(stdout="OPEN"),
        ]
        mock_run.side_effect = responses
        with patch("post_review.sys.argv", ["post_review.py", "42", jf]):
            with self.assertRaises(SystemExit) as ctx:
                post_review.main()
            self.assertEqual(ctx.exception.code, 1)

    # --- JSON is array not dict ---

    @patch("post_review.shutil.which", return_value="/usr/bin/gh")
    @patch("post_review.subprocess.run")
    def test_json_not_dict(self, mock_run, mock_which):
        jf = self._make_json_file([1, 2, 3])
        responses = [
            _make_run_result(stdout="owner/repo"),
            _make_run_result(stdout="OPEN"),
        ]
        mock_run.side_effect = responses
        with patch("post_review.sys.argv", ["post_review.py", "42", jf]):
            with self.assertRaises(SystemExit) as ctx:
                post_review.main()
            self.assertEqual(ctx.exception.code, 1)

    # --- API POST failure ---

    @patch("post_review.shutil.which", return_value="/usr/bin/gh")
    @patch("post_review.subprocess.run")
    def test_review_api_failure(self, mock_run, mock_which):
        jf = self._make_json_file({"body": "test"})
        responses = [
            _make_run_result(stdout="owner/repo"),
            _make_run_result(stdout="OPEN"),
            _make_run_result(stdout="abc1234"),
            _make_run_result(stderr="403 Forbidden", returncode=1),  # API fail
        ]
        mock_run.side_effect = responses
        with patch("post_review.sys.argv", ["post_review.py", "42", jf]):
            with self.assertRaises(SystemExit) as ctx:
                post_review.main()
            self.assertEqual(ctx.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
