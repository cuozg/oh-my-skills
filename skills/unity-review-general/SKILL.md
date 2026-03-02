---
name: unity-review-general
description: PR quality gate — sole APPROVE or REQUEST_CHANGES authority. Triggers — 'approve PR', 'final review', 'quality gate', 'approve or reject'.
---
# unity-review-general

Act as the sole approval authority for a GitHub PR — evaluate security, correctness, test coverage, performance, and documentation, then submit a final APPROVE or REQUEST_CHANGES decision.

## When to Use

- All specialist reviews (code-pr, architecture, asset, prefab) have run
- A PR needs a final merge decision
- Running a standalone quality gate on any PR

## Workflow

1. **Fetch PR metadata** — `gh api repos/{owner}/{repo}/pulls/{pr}` for title, body, labels
2. **Fetch all changed files** — list files and load full content for each
3. **Check existing reviews** — `gh api repos/{owner}/{repo}/pulls/{pr}/reviews` to see prior comments
4. **Evaluate security** — hardcoded credentials, unsafe deserialization, input validation, PlayerPrefs abuse
5. **Evaluate correctness** — critical bugs, data loss paths, crash vectors, broken contracts
6. **Evaluate testing** — new code has tests or PR description justifies why not
7. **Evaluate performance** — hot path allocations, O(n²) loops, excessive Draw Calls introduced
8. **Evaluate documentation** — public APIs have XML doc comments; complex logic has inline comments
9. **Decide** — APPROVE if no blockers; REQUEST_CHANGES if any CRITICAL issue found
10. **Post final review** — submit via `gh api repos/{owner}/{repo}/pulls/{pr}/reviews` with `event` field

## Rules

- Never submit APPROVE if any CRITICAL issue is unresolved
- Never post individual line comments from this skill — use the review body only
- Summarize all specialist review findings in the review body before the decision
- State the decision explicitly: "APPROVE" or "REQUEST_CHANGES" as the first word of the body
- If prior reviews already flagged issues, acknowledge them — do not re-flag
- Flag hardcoded API keys or passwords as CRITICAL (auto REQUEST_CHANGES)
- Flag missing null check on deserialized data touching gameplay state as CRITICAL
- Flag PRs with no description and >200 changed lines as WARNING in the review body
- Use `event: "APPROVE"` or `event: "REQUEST_CHANGES"` — never `"COMMENT"`
- One final review per run — do not call the reviews API twice

## Output Format

A single GitHub PR review posted with APPROVE or REQUEST_CHANGES decision, containing a structured summary of all quality criteria evaluated.
