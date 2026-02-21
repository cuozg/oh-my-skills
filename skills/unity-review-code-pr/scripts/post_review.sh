#!/bin/bash
set -euo pipefail

# Usage: ./post_review.sh <pr_number> <review_json_file>
# Posts a GitHub PR review with auto-injected commit_id.
# Falls back to gh pr comment if PR is merged/closed.

PR_NUMBER="${1:-}"
JSON_FILE="${2:-}"

# --- Validation ---
if [ -z "$PR_NUMBER" ] || [ -z "$JSON_FILE" ]; then
    echo "Usage: $0 <pr_number> <review_json_file>" >&2
    exit 1
fi

if ! [[ "$PR_NUMBER" =~ ^[0-9]+$ ]]; then
    echo "Error: PR number must be numeric, got '$PR_NUMBER'" >&2
    exit 1
fi

if [ ! -f "$JSON_FILE" ]; then
    echo "Error: Review file not found: $JSON_FILE" >&2
    exit 1
fi

if ! command -v gh &>/dev/null; then
    echo "Error: gh CLI not installed" >&2
    exit 1
fi

if ! command -v jq &>/dev/null; then
    echo "Error: jq not installed" >&2
    exit 1
fi

# --- Repo detection ---
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null) || {
    echo "Error: Could not detect repo. Run from a git repo with gh configured." >&2
    exit 1
}

# --- PR existence & state check ---
PR_STATE=$(gh pr view "$PR_NUMBER" --json state -q .state 2>/dev/null) || {
    echo "Error: PR #$PR_NUMBER not found in $REPO" >&2
    exit 1
}

# --- Merged/closed fallback ---
if [ "$PR_STATE" = "MERGED" ] || [ "$PR_STATE" = "CLOSED" ]; then
    echo "PR #$PR_NUMBER is $PR_STATE. Posting as comment instead of review."
    BODY=$(jq -r '.body' "$JSON_FILE")
    gh pr comment "$PR_NUMBER" --body "## Post-Merge Review

$BODY"
    echo "Comment posted on PR #$PR_NUMBER ($PR_STATE)."
    exit 0
fi

# --- Get latest commit SHA ---
COMMIT_ID=$(gh pr view "$PR_NUMBER" --json commits -q '.commits[-1].oid' 2>/dev/null) || {
    echo "Error: Could not retrieve commit SHA for PR #$PR_NUMBER" >&2
    exit 1
}

if [ -z "$COMMIT_ID" ]; then
    echo "Error: Empty commit SHA for PR #$PR_NUMBER" >&2
    exit 1
fi

# --- Inject commit_id into review JSON ---
FINAL_JSON=$(jq --arg cid "$COMMIT_ID" '. + {commit_id: $cid}' "$JSON_FILE") || {
    echo "Error: Failed to inject commit_id into $JSON_FILE (invalid JSON?)" >&2
    exit 1
}

# --- Submit review ---
echo "$FINAL_JSON" | gh api -X POST "/repos/$REPO/pulls/$PR_NUMBER/reviews" --input - || {
    echo "Error: Failed to post review on PR #$PR_NUMBER" >&2
    exit 1
}

echo "Review posted on PR #$PR_NUMBER (commit: ${COMMIT_ID:0:7})."
