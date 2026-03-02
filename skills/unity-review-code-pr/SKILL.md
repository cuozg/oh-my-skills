---
name: unity-review-code-pr
description: GitHub PR C# logic review — posts inline comments via gh api. Triggers — 'review PR', 'review pull request', 'PR review', 'check this PR'.
---
# unity-review-code-pr

Fetch a GitHub PR diff, review changed C# files for logic correctness and Unity-specific risks, then post inline comments via the GitHub API.

## When to Use

- Reviewing a teammate's open GitHub PR
- Running automated review on a PR before merge
- Need review feedback attached directly to PR lines on GitHub

## Workflow

1. **Fetch PR diff** — `gh api repos/{owner}/{repo}/pulls/{pr}/files` to list changed files
2. **Fetch raw diff** — `gh api repos/{owner}/{repo}/pulls/{pr}` with `Accept: application/vnd.github.v3.diff`
3. **Read changed files** — checkout or fetch raw content for each `.cs` file
4. **Investigate context** — use `lsp_goto_definition` / `lsp_find_references` for callers and state owners
5. **Review** — evaluate logic correctness, Unity lifecycle/serialization risks, null paths, event leaks, allocations
6. **Build comment payload** — construct JSON per `references/gh-api-comments.md`
7. **Post comments** — submit via `gh api repos/{owner}/{repo}/pulls/{pr}/reviews`

## Rules

- Always fetch the full file content, not just diff hunks
- Map every comment to the exact `position` in the diff (not line number)
- Use severity prefix: `[CRITICAL]`, `[WARNING]`, `[NOTE]` in every comment body
- Cover at minimum: null guards, lifecycle order, event subscription leaks, serialization, allocation in hot paths
- Never approve or request-changes — post comments only; leave the decision to unity-review-general
- Flag `[SerializeField]` mutation from multiple systems as WARNING
- Flag missing `OnDestroy` unsubscription when `OnEnable` subscribes to events
- Flag `Update()` LINQ/string-concat/closure allocations as WARNING or higher
- Do not post duplicate comments for the same line
- Follow exact API payload format from `references/gh-api-comments.md`

## Output Format

Inline comments posted to the GitHub PR. Print a local summary of comment count and any CRITICAL findings.

## Reference Files

- `references/pr-review-workflow.md` — step-by-step PR fetch and review process
- `references/gh-api-comments.md` — gh api command format for posting PR comments

Load references on demand via `read_skill_file("unity-review-code-pr", "references/{file}")`.
