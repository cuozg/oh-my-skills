---
name: unity-review-code-pr
description: "Focused Unity C# logic reviewer for GitHub Pull Requests. Reviews .cs file changes with surgical focus on correctness, edge cases, state/data flow, concurrency, and Unity lifecycle/serialization risks. After review, pushes comments directly to GitHub via the API. Accepts Pull Request links as input. Use when: reviewing .cs logic in PRs, validating C# behavior before merge, auditing business logic on GitHub. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity PR Code Logic Reviewer

Review `.cs` file changes in GitHub PRs with surgical focus on code logic - correctness, edge cases, state management, data flow, concurrency, and Unity-specific patterns. After review, push comments directly to GitHub via the API.

## Output
Review comments pushed to GitHub PR via API. Covers correctness, edge cases, state/data flow, and Unity-specific risks.

## Input → Command

| Input | Command |
|:------|:--------|
| None | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Branch | `git diff <branch>...HEAD` |
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files` |

## Severity Labels

| Severity | Emoji | Meaning |
|:---------|:------|:--------|
| CRITICAL | 🔴 | Crash, data loss, security, breaking API |
| HIGH | 🟡 | Logic bugs, missing tests, arch violations |
| MEDIUM | 🔵 | Code quality, conventions, minor perf |
| LOW | 🟢 | Style preferences, typos, micro-optimization |

Severity labels are for categorization only. This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.

## Workflow

### 1. Fetch PR

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
gh pr diff <N>               # Full diff
```

Filter to `.cs` files ONLY. If no `.cs` files, APPROVE with note `No C# files to review.`

### 2. Load Review Checklists

```python
read_skill_file("unity-code-standards", "references/review/logic-review-patterns.md")
read_skill_file("unity-code-standards", "references/review/csharp-quality.md")
read_skill_file("unity-code-standards", "references/review/performance-review.md")
read_skill_file("unity-code-standards", "references/review/unity-specifics.md")
```

### 3. Read Full File Context

For each changed `.cs` file, read the ENTIRE file (not just the diff). Logic bugs hide in surrounding context.

### 4. Deep Investigate (Parallel)

Spawn 2-3 `@explore` agents to gather evidence: call-site analysis, state flow tracing, data contract checks.

### 5. Logic Review

Apply loaded checklists. Focus: control flow, state management, data flow, edge cases, Unity lifecycle, serialization safety, memory safety, async patterns.

### 6. Build `/tmp/review-code-pr.json`
Assemble the final review JSON per [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md). Always set `"event": "COMMENT"`. Do NOT include `commit_id` — `post_review.py` injects it automatically.

### 7. Submit

```bash
./skills/unity-review-code-pr/scripts/post_review.py <pr_number> /tmp/review-code-pr.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

## Evidence Rules

- 🔴 Critical: caller count + affected files + reproduction scenario
- 🟡 High: trigger conditions + what state leads to the bug
- 🔵 Medium: brief explanation of why current code is suboptimal
- 🟢 Low: brief note
- Never flag without evidence

## Rules

- Only review `.cs` files. Read full files, not just diffs.
- Trace data flow end-to-end. One issue = one comment (severity + evidence + suggestion).
- Same issue in N files → full explanation on first, short ref on rest (batch pattern).
- Check assumptions violated: null, empty, concurrent, out-of-order.
- Verify event subscribe/unsubscribe pairs and lifecycle ordering.
- If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points.
- For serialization findings, check whether the project has migration/versioning support.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id`, modify source files, review non-`.cs` files, or delegate to sub-skills.
