---
name: unity-review-code-pr
description: "Focused Unity C# logic reviewer for GitHub Pull Requests. Reviews .cs file changes with surgical focus on correctness, edge cases, state/data flow, concurrency, and Unity lifecycle/serialization risks. After review, pushes comments directly to GitHub via the API. Accepts Pull Request links as input. Use when: reviewing .cs logic in PRs, validating C# behavior before merge, auditing business logic on GitHub. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity PR Code Logic Reviewer

Review `.cs` file changes in GitHub PRs. After review, push comments directly to GitHub via the API.

## Output

Review comments pushed to GitHub PR via API per [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md).

## Input → Command

| Input | Command |
|:------|:--------|
| None | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Branch | `git diff <branch>...HEAD` |
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files` |

## Severity

| Severity | Emoji | Meaning |
|:---------|:------|:--------|
| CRITICAL | 🔴 | Crash, data loss, security, breaking API |
| HIGH | 🟡 | Logic bugs, missing tests, arch violations |
| MEDIUM | 🔵 | Code quality, conventions, minor perf |
| LOW | 🟢 | Style preferences, typos, micro-optimization |

Severity labels are for categorization only. This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.

## Load References

Load shared review engine from `unity-code-standards`:

```python
read_skill_file("unity-code-standards", "references/review/deep-review-workflow.md")
read_skill_file("unity-code-standards", "references/review/VERIFICATION_GATES.md")
read_skill_file("unity-code-standards", "references/review/logic-review-patterns.md")
read_skill_file("unity-code-standards", "references/review/csharp-quality.md")
read_skill_file("unity-code-standards", "references/review/performance-review.md")
read_skill_file("unity-code-standards", "references/review/unity-specifics.md")
read_skill_file("unity-code-standards", "references/review/architecture-review.md")
```

## Workflow

### 1. Fetch PR

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
gh pr diff <N>               # Full diff
```

Filter to `.cs` files ONLY. If no `.cs` files, APPROVE with note `No C# files to review.`

### 2. Read Full File Context

For each changed `.cs` file, read the ENTIRE file (not just the diff). Logic bugs hide in surrounding context.

### 3. Deep Investigate (Parallel)

Spawn explore agents per `deep-review-workflow.md`: call-site analysis, state flow tracing, data contract checks. Enforce `VERIFICATION_GATES.md` evidence rules.

### 4. Logic Review

Apply all loaded review checklists + `deep-review-workflow.md` focus areas (control flow, state management, data flow, edge cases, Unity lifecycle, serialization safety, memory safety).

### 5. Build `/tmp/review-code-pr.json`

Parse the diff output to determine which lines are commentable (see [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md) "How to Determine `line`"). For each comment:
1. `line` = new-file line number, must be within a diff hunk (`@@ +START,COUNT @@`)
2. `path` = exact path from `gh pr diff --name-only`
3. Suggestion content must be the EXACT full-line replacement for the targeted line(s), preserving indentation
4. Multi-line: include `start_line` and `start_side: "RIGHT"`

Always set `"event": "COMMENT"`. Do NOT include `commit_id` — `post_review.py` injects it.
### 6. Submit

```bash
./skills/unity-review-code-pr/scripts/post_review.py <pr_number> /tmp/review-code-pr.json
```

Fallback (merged/closed): handled automatically by `post_review.py`. See [review-troubleshooting.md](references/review-troubleshooting.md).

## Rules

- Only review `.cs` files. Read full files, not just diffs.
- Trace data flow end-to-end. One issue = one comment (severity + evidence + suggestion).
- Same issue in N files → full explanation on first, short ref on rest (batch pattern).
- `line` MUST be within a diff hunk. Verify against `gh pr diff` output before adding comment.
- Suggestion content = exact full-line replacement with correct indentation. Never suggest partial lines.
- If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points.
- For serialization findings, check whether the project has migration/versioning support.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id`, modify source files, review non-`.cs` files, or delegate to sub-skills.
- Never comment without evidence. Investigate first — see `VERIFICATION_GATES.md`.
