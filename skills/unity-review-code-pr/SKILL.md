---
name: unity-review-code-pr
description: "Focused Unity C# logic reviewer for GitHub Pull Requests. Reviews .cs file changes with surgical focus on correctness, edge cases, state/data flow, concurrency, and Unity lifecycle/serialization risks. After review, pushes comments directly to GitHub via the API. If local code fixes are requested, delegates to unity-code-quick via background tasks. Accepts Pull Request links as input. Use when: reviewing .cs logic in PRs, validating C# behavior before merge, auditing business logic on GitHub. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity PR Code Logic Reviewer

Review `.cs` file changes in GitHub PRs. Push review comments to GitHub via API. If code fixes are needed locally, delegate to `unity-code-quick`.

## Output

Review comments pushed to GitHub PR via API per [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md).

## Input → Command

See [tool-usage.md](references/tool-usage.md) for input-to-diff command mapping.

## Severity

Four levels: 🔴 CRITICAL, 🟡 HIGH, 🔵 MEDIUM, 🟢 LOW. See [tool-usage.md](references/tool-usage.md) for severity definitions.
Severity labels are for categorization only. This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.

## Workflow

Load references, then follow the 6-step workflow: Fetch PR → Read → Investigate → Review → Build JSON → Submit.
Read [workflow.md](references/workflow.md) before starting any review.

## Reference Files
- [workflow.md](references/workflow.md) — Load references + 6-step PR review workflow
- [tool-usage.md](references/tool-usage.md) — Input-to-command mapping + severity definitions
- [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md) — GitHub API review comment format
- [review-troubleshooting.md](references/review-troubleshooting.md) — Merged/closed PR fallback handling

## Rules

- **Review only** — this skill investigates and comments. Never modify source files directly.
- Only review `.cs` files. Read full files, not just diffs. Trace data flow end-to-end.
- One issue = one comment (severity + evidence + suggestion).
- Same issue in N files → full explanation on first, short ref on rest (batch pattern).
- `line` MUST be within a diff hunk. Verify against `gh pr diff` output before adding comment.
- Suggestion content = exact full-line replacement with correct indentation. Never suggest partial lines.
- If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points.
- Submit even if PR is merged — `post_review.py` handles fallback.
- If local code fixes are requested (e.g., "fix this PR"), delegate to `unity-code-quick` via `task(category="quick", load_skills=["unity-code-quick"], run_in_background=true)` — one task per file.
- Never comment without evidence. Investigate first — see `VERIFICATION_GATES.md`.
