---
name: unity-review-pr
description: "Expert Unity Developer code reviewer. Reviews PRs, commits, branches, or uncommitted changes with focus on Unity-specific patterns, performance, and best practices. Accepts Pull Request links as input. Use when: reviewing PRs, checking changes, comparing branches. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity Code Reviewer

One issue = one inline comment. Submit via GitHub API.

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

Multiple types → load ALL matching.

## Workflow

1. **Fetch** diff (see Input table)
2. **Context Gathering** (parallel, `run_in_background=true`) — spawn agents **before** reading diff. ALWAYS capture and return each agent's `session_id`.

   **`@explore` agents (2-4):**

   | Agent | Task |
   |:------|:-----|
   | Codebase patterns | Read changed files + context. Identify patterns, conventions, architecture. |
   | Implementations | Find callers, subscribers, derived types, prefab/SO refs. Count call sites for modified public members. |
   | User requirement | Read PR title/body/linked issues. Extract intent, acceptance criteria. |
   | Impact analysis | *(optional, 10+ files)* Trace cross-system dependencies, event channels, serialization chains. |

   **`@librarian` agents (1-2, when external library involved):**

   | Agent | Task |
   |:------|:-----|
   | Library docs | Fetch API docs, changelog, migration guides for new/updated packages. |
   | Best practices | *(optional)* Research known issues, perf implications for library version. |

   **Evidence rules:** 🔴 needs caller count + affected files. 🟡 needs trigger conditions. **Never flag without evidence.**

3. **Review** — Collect agent results (use `session_id`). Apply reference checklists against evidence.
4. **Build** `/tmp/review.json` per [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md): summary + acceptance criteria + one comment per issue
5. **Submit** — `.opencode/skills/unity/unity-review-pr/scripts/post_review.sh <pr_number> /tmp/review.json`

**Fallback** (merged/closed): `gh pr comment <N> --body "## Post-Merge Review\n\n<body>"`

## Rules

- ✅ One issue = one comment. Investigate before flagging. Include acceptance criteria. Submit even if merged. Always return `session_id`.
- ❌ Never combine issues. Never skip submission. Never flag without evidence. Never discard `session_id`.
