#!/usr/bin/env python3
"""Post a GitHub PR review with auto-injected commit_id.
Falls back to gh pr comment if PR is merged/closed.
Usage: ./post_review.py <pr_number> <review_json_file>
"""

import json
import os
import shutil
import subprocess
import sys
from typing import cast


def run_gh(args: list[str], input_data: str | None = None) -> str:
    cmd: list[str] = ["gh", *args]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        input=input_data,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "gh command failed"
        raise RuntimeError(message)
    return result.stdout.strip()


def main():
    if len(sys.argv) != 3:
        print("Usage: post_review.py <pr_number> <review_json_file>", file=sys.stderr)
        sys.exit(1)

    pr_number = sys.argv[1]
    json_file = sys.argv[2]

    if not pr_number.isdigit():
        print(f"Error: PR number must be numeric, got '{pr_number}'", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(json_file):
        print(f"Error: Review file not found: {json_file}", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("gh"):
        print("Error: gh CLI not installed", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("jq"):
        print(
            "Note: jq not installed; continuing because this Python version uses json module.",
            file=sys.stderr,
        )

    try:
        repo = run_gh(
            ["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"]
        )
    except RuntimeError:
        print(
            "Error: Could not detect repo. Run from a git repo with gh configured.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        pr_state = run_gh(["pr", "view", pr_number, "--json", "state", "-q", ".state"])
    except RuntimeError:
        print(f"Error: PR #{pr_number} not found in {repo}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(json_file, "r", encoding="utf-8") as handle:
            review_json = cast(object, json.load(handle))
    except Exception:
        print(f"Error: Failed to parse review JSON: {json_file}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(review_json, dict):
        print(
            f"Error: Failed to inject commit_id into {json_file} (invalid JSON?)",
            file=sys.stderr,
        )
        sys.exit(1)

    review_raw = cast(dict[object, object], review_json)
    review_dict: dict[str, object] = {
        str(key): value for key, value in review_raw.items()
    }

    if pr_state in {"MERGED", "CLOSED"}:
        print(f"PR #{pr_number} is {pr_state}. Posting as comment instead of review.")
        body = review_dict.get("body")
        body_text = "null" if body is None else str(body)
        comment_body = f"## Post-Merge Review\n\n{body_text}"
        try:
            _ = run_gh(["pr", "comment", pr_number, "--body", comment_body])
        except RuntimeError as exc:
            print(
                str(exc) or f"Error: Failed to post comment on PR #{pr_number}",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"Comment posted on PR #{pr_number} ({pr_state}).")
        return

    try:
        commit_id = run_gh(
            ["pr", "view", pr_number, "--json", "commits", "-q", ".commits[-1].oid"]
        )
    except RuntimeError:
        print(
            f"Error: Could not retrieve commit SHA for PR #{pr_number}", file=sys.stderr
        )
        sys.exit(1)

    if not commit_id:
        print(f"Error: Empty commit SHA for PR #{pr_number}", file=sys.stderr)
        sys.exit(1)

    final_json: dict[str, object] = dict(review_dict)
    final_json["commit_id"] = commit_id

    try:
        _ = run_gh(
            [
                "api",
                "-X",
                "POST",
                f"/repos/{repo}/pulls/{pr_number}/reviews",
                "--input",
                "-",
            ],
            input_data=json.dumps(final_json),
        )
    except RuntimeError:
        print(f"Error: Failed to post review on PR #{pr_number}", file=sys.stderr)
        sys.exit(1)

    print(f"Review posted on PR #{pr_number} (commit: {commit_id[:7]}).")


if __name__ == "__main__":
    main()
