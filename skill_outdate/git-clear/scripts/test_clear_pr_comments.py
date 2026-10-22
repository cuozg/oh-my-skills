#!/usr/bin/env python3
import subprocess
import sys
from unittest.mock import MagicMock, call, patch

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))

from clear_pr_comments import (
    clear_pr_comments,
    delete_comment,
    list_comment_ids,
    run_gh,
)


def make_completed_process(stdout="", stderr="", returncode=0):
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=stdout, stderr=stderr
    )


class TestRunGh:
    @patch("clear_pr_comments.subprocess.run")
    def test_returns_stdout(self, mock_run):
        mock_run.return_value = make_completed_process(stdout="output\n")
        assert run_gh(["api", "/test"]) == "output"

    @patch("clear_pr_comments.subprocess.run")
    def test_raises_on_failure(self, mock_run):
        mock_run.return_value = make_completed_process(
            returncode=1, stderr="bad request"
        )
        try:
            run_gh(["api", "/test"])
            assert False, "Should have raised"
        except RuntimeError as e:
            assert "bad request" in str(e)


class TestListCommentIds:
    @patch("clear_pr_comments.run_gh")
    def test_parses_ids(self, mock_gh):
        mock_gh.return_value = "100\n200\n300"
        ids = list_comment_ids("owner", "repo", 42, "issues")
        assert ids == [100, 200, 300]
        mock_gh.assert_called_once_with(
            [
                "api",
                "/repos/owner/repo/issues/42/comments",
                "--paginate",
                "--jq",
                ".[].id",
            ]
        )

    @patch("clear_pr_comments.run_gh")
    def test_empty_output(self, mock_gh):
        mock_gh.return_value = ""
        assert list_comment_ids("owner", "repo", 1, "pulls") == []

    @patch("clear_pr_comments.run_gh")
    def test_error_returns_empty(self, mock_gh):
        mock_gh.side_effect = RuntimeError("not found")
        assert list_comment_ids("owner", "repo", 1, "issues") == []

    @patch("clear_pr_comments.run_gh")
    def test_pulls_endpoint(self, mock_gh):
        mock_gh.return_value = "500"
        ids = list_comment_ids("o", "r", 7, "pulls")
        assert ids == [500]
        mock_gh.assert_called_once_with(
            [
                "api",
                "/repos/o/r/pulls/7/comments",
                "--paginate",
                "--jq",
                ".[].id",
            ]
        )


class TestDeleteComment:
    @patch("clear_pr_comments.run_gh")
    def test_success(self, mock_gh):
        mock_gh.return_value = ""
        assert delete_comment("owner", "repo", 123, "issues") is True
        mock_gh.assert_called_once_with(
            [
                "api",
                "--method",
                "DELETE",
                "/repos/owner/repo/issues/comments/123",
            ]
        )

    @patch("clear_pr_comments.run_gh")
    def test_failure(self, mock_gh):
        mock_gh.side_effect = RuntimeError("403")
        assert delete_comment("owner", "repo", 123, "pulls") is False

    @patch("clear_pr_comments.run_gh")
    def test_pulls_endpoint(self, mock_gh):
        mock_gh.return_value = ""
        delete_comment("o", "r", 99, "pulls")
        mock_gh.assert_called_once_with(
            [
                "api",
                "--method",
                "DELETE",
                "/repos/o/r/pulls/comments/99",
            ]
        )


class TestClearPrComments:
    @patch("clear_pr_comments.delete_comment")
    @patch("clear_pr_comments.list_comment_ids")
    def test_deletes_both_types(self, mock_list, mock_delete):
        mock_list.side_effect = [[10, 20], [30]]
        mock_delete.return_value = True

        stats = clear_pr_comments("owner", "repo", 5)

        assert stats["issue_deleted"] == 2
        assert stats["review_deleted"] == 1
        assert stats["issue_failed"] == 0
        assert stats["review_failed"] == 0
        assert mock_delete.call_count == 3

    @patch("clear_pr_comments.delete_comment")
    @patch("clear_pr_comments.list_comment_ids")
    def test_dry_run_no_deletes(self, mock_list, mock_delete):
        mock_list.side_effect = [[10], [20, 30]]

        stats = clear_pr_comments("owner", "repo", 5, dry_run=True)

        mock_delete.assert_not_called()
        assert stats["issue_deleted"] == 1
        assert stats["review_deleted"] == 2

    @patch("clear_pr_comments.delete_comment")
    @patch("clear_pr_comments.list_comment_ids")
    def test_no_comments(self, mock_list, mock_delete):
        mock_list.side_effect = [[], []]

        stats = clear_pr_comments("owner", "repo", 1)

        mock_delete.assert_not_called()
        assert stats["issue_deleted"] == 0
        assert stats["review_deleted"] == 0

    @patch("clear_pr_comments.delete_comment")
    @patch("clear_pr_comments.list_comment_ids")
    def test_partial_failure(self, mock_list, mock_delete):
        mock_list.side_effect = [[10, 20], []]
        mock_delete.side_effect = [True, False]

        stats = clear_pr_comments("owner", "repo", 3)

        assert stats["issue_deleted"] == 1
        assert stats["issue_failed"] == 1
        assert stats["review_deleted"] == 0
