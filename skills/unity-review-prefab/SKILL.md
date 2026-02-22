---
name: unity-review-prefab
description: "Review .prefab and .unity files in GitHub PRs for missing scripts, broken variant links, raycast issues, hierarchy problems, and Unity-specific YAML patterns. After review, pushes comments directly to GitHub via the API. Accepts PR number/URL as input. Use when: reviewing prefab/scene files in PRs, validating prefab integrity before merge. Triggers: 'review prefab', 'prefab review', 'scene review', 'prefab changes', 'PR prefab review', 'review PR prefabs'."
---

# Prefab & Scene PR Reviewer

Review `.prefab` and `.unity` file changes in GitHub PRs. Push review comments directly to GitHub via the API.

## Output
Review comments pushed to GitHub PR via API. Covers missing scripts, broken variants, raycast issues, hierarchy problems.

## Input → Command

| Input | Command |
|:------|:--------|
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files,number` |

## Severity → Approval

| Severity | Emoji | Meaning | Approval |
|:---------|:------|:--------|:---------|
| CRITICAL | 🔴 | Breaks functionality, data loss, crashes | `REQUEST_CHANGES` (block) |
| HIGH | 🟡 | Performance, UX, or logic issues | `REQUEST_CHANGES` |
| MEDIUM | 🔵 | Style, maintainability, minor UX | `COMMENT` (allow merge) |
| LOW | 🟢 | Naming, conventions, suggestions | `APPROVE` (with suggestions) |
| CLEAN | — | No issues | `APPROVE` |

## Workflow

### 1. Fetch PR

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
gh pr diff <N>               # Full diff
```

Filter to `.prefab` and `.unity` files ONLY. If none found, APPROVE with note `No prefab/scene files to review.`

### 2. Read Full YAML

Read the ENTIRE file for each changed `.prefab`/`.unity` file — not just the diff. YAML pattern matching requires full context.

### 3. Run Grep Patterns

Apply patterns from [PREFAB_PATTERNS.md](references/PREFAB_PATTERNS.md) against each file. Key patterns: missing scripts (`m_Script: {fileID: 0}`), broken variant links, disabled raycast targets on non-interactive elements, deep nesting.

### 4. Classify & Build Comments

One issue = one comment. Every comment MUST include: severity emoji + title, **Evidence** (file + line), **Why** (impact), and a `suggestion` block with a fix.

- `m_RaycastTarget: 1` — check if the GO has `Button`, `Toggle`, or `InputField`. If not, flag as 🔴 Critical.
- Batch pattern: full explanation on first occurrence, short reference on subsequent.

### 5. Build `/tmp/review.json`

```json
{
  "body": "## Prefab & Scene Review\n**Scope**: [N files reviewed]\n...",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [
    {
      "path": "Assets/Prefabs/Player.prefab",
      "line": 42,
      "side": "RIGHT",
      "body": "**🔴 Missing Script Reference**: `m_Script: {fileID: 0}`\n**Evidence**: Line 42\n**Why**: MissingReferenceException at runtime\n```suggestion\nRemove the component or restore the script GUID\n```"
    }
  ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it automatically. Set `event` based on highest severity using the Severity → Approval table above.

### 6. Submit

```bash
./skills/unity-review-prefab/scripts/post_review.py <pr_number> /tmp/review.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

## Rules

- Only review `.prefab` and `.unity` files. Read full files, not just diffs.
- One issue = one comment. Every comment needs severity + evidence + suggestion.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id` or modify source files.
- Refer to [PREFAB_PATTERNS.md](references/PREFAB_PATTERNS.md) for the complete pattern catalog.
