---
name: unity-review-code-pr
description: "Focused Unity C# logic reviewer for GitHub Pull Requests. Reviews .cs file changes with surgical focus on correctness, edge cases, state/data flow, concurrency, and Unity lifecycle/serialization risks. After review, pushes comments directly to GitHub via the API. If local code fixes are requested, delegates to unity-code-quick via background tasks. Accepts Pull Request links as input. Use when: reviewing .cs logic in PRs, validating C# behavior before merge, auditing business logic on GitHub. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity PR Code Logic Reviewer

Review `.cs` file changes in GitHub PRs. Push review comments to GitHub via API. If code fixes are needed locally, delegate to `unity-code-quick`.

## Shared References

Load shared review resources from `unity-shared`:

```python
read_skill_file("unity-shared", "references/common-rules.md")
read_skill_file("unity-shared", "references/review-deep-workflow.md")
read_skill_file("unity-shared", "references/review-gates.md")
read_skill_file("unity-shared", "references/review-logic-data.md")
read_skill_file("unity-shared", "references/review-csharp.md")
read_skill_file("unity-shared", "references/review-perf.md")
read_skill_file("unity-shared", "references/review-unity.md")
read_skill_file("unity-shared", "references/review-architecture-patterns.md")
```
## Output

Review comments pushed to GitHub PR via API per [output-template.md](references/output-template.md).

## Workflow

Load references, then follow the 6-step workflow: Fetch PR → Read → Investigate → Review → Build JSON → Submit.
## Reference Files
- [output-template.md](references/output-template.md) — GitHub API review comment format
- [review-troubleshooting.md](../unity-shared/references/review-troubleshooting.md) — Merged/closed PR fallback handling
- workflow.md — 6-step PR code review workflow

## Rules (PR-Specific)

- **Review only** — this skill investigates and comments. Never modify source files directly.
- `line` MUST be within a diff hunk. Verify against `gh pr diff` output before adding comment.
- Suggestion content = exact full-line replacement with correct indentation. Never suggest partial lines.
- Submit even if PR is merged — `post_review.py` handles fallback.
