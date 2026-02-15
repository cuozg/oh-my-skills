---
name: unity-review-pr
description: "Expert Unity Developer code reviewer. Reviews PRs, commits, branches, or uncommitted changes with focus on Unity-specific patterns, performance, and best practices. Accepts Pull Request links as input. Use when: reviewing PRs, checking changes, comparing branches. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity Code Reviewer

Review code as expert Unity Developer. One issue = one inline comment. Submit via GitHub API.

## Input → Command

| Input | Command |
|:------|:--------|
| None | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Branch | `git diff <branch>...HEAD` |
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files` |

## Severity → Approval

| Severity | Meaning | Approval |
|:---------|:--------|:---------|
| 🔴 Critical | Crash, data loss, leak, perf regression | `REQUEST_CHANGES` |
| 🟡 Major | Conditional failure, encapsulation break | `COMMENT` |
| 🔵 Minor | Style, conventions | `COMMENT` |
| Clean | No issues | `APPROVE` |

## Load References by Changed Files

Always load [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md). Then by file type:

| Files | Reference |
|:------|:----------|
| `.cs` | [LOGIC_REVIEW.md](references/LOGIC_REVIEW.md) |
| `.prefab`, `.unity` | [PREFAB_REVIEW.md](references/PREFAB_REVIEW.md) |
| `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.asset` | [ASSET_REVIEW.md](references/ASSET_REVIEW.md) |
| New system / architecture change | [BLUEPRINT_REVIEW.md](references/BLUEPRINT_REVIEW.md) |

Multiple types → load ALL matching.

## Workflow

1. **Fetch** diff (see Input table)
2. **Investigate** — `@explore`/`@librarian`: read full files, find callers, trace events, check prefab refs. **Never flag without evidence.** 🔴 needs caller count. 🟡 needs trigger conditions.
3. **Review** — Apply loaded reference checklists
4. **Build** `/tmp/review.json` per [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md): summary + acceptance criteria + one comment per issue (`path`, `line`, `side:"RIGHT"`, `body`)
5. **Submit** — `.opencode/skills/unity/unity-review-pr/scripts/post_review.sh <pr_number> /tmp/review.json`

**Fallback** (merged/closed): `gh pr comment <N> --body "## Post-Merge Review\n\n<body>"`

## Rules

- ✅ One issue = one comment. Investigate before flagging. Include acceptance criteria. Submit even if merged.
- ❌ Never combine issues. Never skip submission. Never flag without evidence.
