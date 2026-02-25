---
name: unity-review-prefab
description: "Review .prefab and .unity files in GitHub PRs for missing scripts, broken variant links, raycast issues, hierarchy problems, and Unity-specific YAML patterns. After review, pushes comments directly to GitHub via the API. Accepts PR number/URL as input. Use when: reviewing prefab/scene files in PRs, validating prefab integrity before merge. Triggers: 'review prefab', 'prefab review', 'scene review', 'prefab changes', 'PR prefab review', 'review PR prefabs'."
---

# Prefab & Scene PR Reviewer

Review `.prefab` and `.unity` file changes in GitHub PRs. Delegate each file to a parallel subagent, gather results, merge into one review, and push to GitHub.

## Output
Review comments pushed to GitHub PR via API. Covers missing scripts, broken variants, raycast issues, hierarchy problems.

## Input → Command

| Input | Command |
|:------|:--------|
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files,number` |

## Severity Labels

| Severity | Emoji | Meaning |
|:---------|:------|:--------|
| CRITICAL | 🔴 | Breaks functionality, data loss, crashes |
| HIGH | 🟡 | Performance, UX, or logic issues |
| MEDIUM | 🔵 | Style, maintainability, minor UX |
| LOW | 🟢 | Naming, conventions, suggestions |

Severity labels are for categorization only. This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.

## Workflow

### 1. Fetch PR & Filter Files

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
```

Filter to `.prefab` and `.unity` files ONLY. If none found, post note `No prefab/scene files to review.` and stop.

### 2. Parallel Review — One Subagent Per File

For each `.prefab`/`.unity` file, spawn a background subagent task. See [parallel-review-workflow.md](references/parallel-review-workflow.md) for prompt template, result format, and merge logic.

```python
task(
  category="quick",
  load_skills=["unity-review-prefab"],
  run_in_background=True,
  description=f"Review {filename}",
  prompt=f"<see parallel-review-workflow.md for template>"
)
```

Each subagent reads the full file, applies patterns from [PREFAB_PATTERNS.md](references/PREFAB_PATTERNS.md), and returns a JSON array of comment objects.

### 3. Collect & Merge Results

Collect all subagent results via `background_output(task_id=...)`. Merge all comment arrays into one list. Build `/tmp/review-prefab.json`:

```json
{
  "body": "## Prefab & Scene Review\n**Scope**: N files reviewed\n...",
  "event": "COMMENT",
  "comments": [ ...merged comments from all subagents... ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it automatically.

### 4. Submit

```bash
./skills/unity-review-prefab/scripts/post_review.py <pr_number> /tmp/review-prefab.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

## Rules

- Only review `.prefab` and `.unity` files. Read full files, not just diffs.
- One subagent per file. Each subagent loads `unity-review-prefab` to access patterns.
- One issue = one comment. Every comment needs severity + evidence + suggestion.
- If a subagent fails, log the error and continue with remaining results.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id` or modify source files.
- Refer to [PREFAB_PATTERNS.md](references/PREFAB_PATTERNS.md) for the complete pattern catalog.
- Refer to [parallel-review-workflow.md](references/parallel-review-workflow.md) for delegation details.
