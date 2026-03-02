#!/usr/bin/env python3
"""
Delete all comments from a GitHub Pull Request.

Removes both issue comments (timeline thread) and review comments (inline diff).
Requires: gh CLI authenticated with `repo` scope.

Usage:
    clear_pr_comments.py <owner> <repo> <pr_number> [--dry-run]
"""

import subprocess
import sys


def run_gh(args: list[str]) -> str:

    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"gh command failed: {' '.join(args)}\n{result.stderr.strip()}"
        )
    return result.stdout.strip()


def list_comment_ids(owner: str, repo: str, pr: int, comment_type: str) -> list[int]:
    """
    List all comment IDs for a PR.

    Args:
        comment_type: "issues" for timeline comments, "pulls" for review comments.
    """
    endpoint = f"/repos/{owner}/{repo}/{comment_type}/{pr}/comments"
    try:
        output = run_gh(["api", endpoint, "--paginate", "--jq", ".[].id"])
    except RuntimeError:
        return []
    if not output:
        return []
    return [int(line) for line in output.splitlines() if line.strip()]


def delete_comment(owner: str, repo: str, comment_id: int, comment_type: str) -> bool:
    """
    Delete a single comment.

    Args:
        comment_type: "issues" for timeline comments, "pulls" for review comments.
    Returns:
        True if deleted successfully, False otherwise.
    """
    endpoint = f"/repos/{owner}/{repo}/{comment_type}/comments/{comment_id}"
    try:
        run_gh(["api", "--method", "DELETE", endpoint])
        return True
    except RuntimeError as e:
        print(
            f"  ⚠ Failed to delete {comment_type} comment {comment_id}: {e}",
            file=sys.stderr,
        )
        return False


def clear_pr_comments(owner: str, repo: str, pr: int, dry_run: bool = False) -> dict:
    """
    Delete all comments from a PR.

    Returns:
        Dict with counts: {issue_deleted, issue_failed, review_deleted, review_failed}
    """
    stats = {
        "issue_deleted": 0,
        "issue_failed": 0,
        "review_deleted": 0,
        "review_failed": 0,
    }

    # Issue comments (timeline thread)
    issue_ids = list_comment_ids(owner, repo, pr, "issues")
    print(f"Found {len(issue_ids)} issue comment(s)")

    for cid in issue_ids:
        if dry_run:
            print(f"  [dry-run] Would delete issue comment {cid}")
            stats["issue_deleted"] += 1
        else:
            if delete_comment(owner, repo, cid, "issues"):
                print(f"  ✓ Deleted issue comment {cid}")
                stats["issue_deleted"] += 1
            else:
                stats["issue_failed"] += 1

    # Review comments (inline diff)
    review_ids = list_comment_ids(owner, repo, pr, "pulls")
    print(f"Found {len(review_ids)} review comment(s)")

    for cid in review_ids:
        if dry_run:
            print(f"  [dry-run] Would delete review comment {cid}")
            stats["review_deleted"] += 1
        else:
            if delete_comment(owner, repo, cid, "pulls"):
                print(f"  ✓ Deleted review comment {cid}")
                stats["review_deleted"] += 1
            else:
                stats["review_failed"] += 1

    return stats


def main():
    if len(sys.argv) < 4:
        print("Usage: clear_pr_comments.py <owner> <repo> <pr_number> [--dry-run]")
        sys.exit(1)

    owner = sys.argv[1]
    repo = sys.argv[2]
    try:
        pr = int(sys.argv[3])
    except ValueError:
        print(
            f"Error: PR number must be an integer, got '{sys.argv[3]}'", file=sys.stderr
        )
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print(f"[DRY RUN] Listing comments on {owner}/{repo}#{pr}...")
    else:
        print(f"Deleting all comments on {owner}/{repo}#{pr}...")

    stats = clear_pr_comments(owner, repo, pr, dry_run=dry_run)

    total_deleted = stats["issue_deleted"] + stats["review_deleted"]
    total_failed = stats["issue_failed"] + stats["review_failed"]

    action = "Would delete" if dry_run else "Deleted"
    print(
        f"\n{action} {stats['issue_deleted']} issue comment(s) and {stats['review_deleted']} review comment(s) from PR #{pr}"
    )
    if total_failed > 0:
        print(f"Failed to delete {total_failed} comment(s)")
        sys.exit(1)

    if total_deleted == 0:
        print("No comments to delete.")


if __name__ == "__main__":
    main()
