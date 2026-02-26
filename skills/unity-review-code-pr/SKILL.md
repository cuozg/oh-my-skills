---
name: unity-review-code-pr
description: "Focused Unity C# logic reviewer for GitHub Pull Requests. Reviews .cs file changes with surgical focus on correctness, edge cases, state/data flow, concurrency, and Unity lifecycle/serialization risks. After review, pushes comments directly to GitHub via the API. If local code fixes are requested, delegates to unity-code-quick via background tasks. Accepts Pull Request links as input. Use when: reviewing .cs logic in PRs, validating C# behavior before merge, auditing business logic on GitHub. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity PR Code Logic Reviewer

Review `.cs` file changes in GitHub PRs. Push review comments to GitHub via API. If code fixes are needed locally, delegate to `unity-code-quick`.

## Shared References

Load shared review resources from `unity-review-code-shared`:
- [tool-usage.md](../unity-review-code-shared/references/tool-usage.md) — Input-to-command mapping + severity
- [review-engine.md](../unity-review-code-shared/references/review-engine.md) — Review logic references to load
- [common-rules.md](../unity-review-code-shared/references/common-rules.md) — Shared review rules

## Output

Review comments pushed to GitHub PR via API per [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md).

## Workflow

Load references, then follow the 6-step workflow: Fetch PR → Read → Investigate → Review → Build JSON → Submit.
Read [workflow.md](references/workflow.md) before starting any review.

## Reference Files
- [workflow.md](references/workflow.md) — 6-step PR review workflow
- [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md) — GitHub API review comment format
- [review-troubleshooting.md](references/review-troubleshooting.md) — Merged/closed PR fallback handling

## Rules (PR-Specific)

- **Review only** — this skill investigates and comments. Never modify source files directly.
- `line` MUST be within a diff hunk. Verify against `gh pr diff` output before adding comment.
- Suggestion content = exact full-line replacement with correct indentation. Never suggest partial lines.
- Submit even if PR is merged — `post_review.py` handles fallback.
