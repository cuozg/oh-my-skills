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
| 🔴 Critical | Crash, data loss, security, breaking API | `REQUEST_CHANGES` (block) |
| 🟡 High | Logic bugs, missing tests, arch violations | `REQUEST_CHANGES` |
| 🔵 Medium | Code quality, conventions, minor perf | `COMMENT` (allow merge) |
| 🟢 Low | Style preferences, typos, micro-optimization | `APPROVE` (with suggestions) |
| Clean | No issues | `APPROVE` |

Full decision tree and classification: [APPROVAL_CRITERIA.md](references/APPROVAL_CRITERIA.md).

## Load References by Changed Files

Always load:
- [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md) — output JSON format, suggestion syntax, troubleshooting
- [APPROVAL_CRITERIA.md](references/APPROVAL_CRITERIA.md) — severity decision tree
- [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md) — security, correctness, testing, quality, perf, docs

Then by file type:

| Files | Reference |
|:------|:----------|
| `.cs` | [LOGIC_REVIEW.md](references/LOGIC_REVIEW.md) |
| `.prefab`, `.unity` | [PREFAB_REVIEW.md](references/PREFAB_REVIEW.md) |
| `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` | [ASSET_REVIEW.md](references/ASSET_REVIEW.md) |

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

3. **Review** — Collect agent results (use `session_id`). Apply reference checklists against evidence. Cross-reference findings between agents; if one agent found a caller chain and another found state mutation on the same field/path, merge into one stronger, higher-severity finding with combined evidence.
4. **Missing-Things Pass** — Explicitly check for missing safeguards: null guards, event unsubscribe, `Dispose`/release calls, required tests, and documentation on public API changes.
5. **Build** `/tmp/review.json` per [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md): summary + acceptance criteria + one comment per issue. Do NOT include `commit_id` — the post script injects it.
6. **Submit** — `./skills/unity-review-pr/scripts/post_review.sh <pr_number> /tmp/review.json`

**Fallback** (merged/closed): handled automatically by `post_review.sh` — posts as comment.

## Suggestion Syntax Quick Reference

| Type | JSON fields | Notes |
|:-----|:------------|:------|
| Single-line | `"line": 42` | Suggestion replaces that one line |
| Multi-line | `"start_line": 10, "line": 15` | Suggestion replaces lines 10–15 |
| Large rewrite | Single `"line"` | Use `<details>` block instead of suggestion |

`line` = file line number (not diff position). `side` always `"RIGHT"`. Full syntax in [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md).

## Rules

- ✅ One issue = one comment. Investigate before flagging. Include acceptance criteria. Submit even if merged. Always return `session_id`.
- ✅ Same issue in N files → full explanation on first, short ref + suggestion on rest (batch pattern).
- ✅ For each 🔴 issue, verify it is not already handled by base class/wrapper/framework conventions used by the project.
- ✅ If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points (do not treat as `async void` by default).
- ✅ For serialization-related findings, check whether the project has migration/versioning support before classifying as breaking.
- ❌ Never combine issues. Never skip submission. Never flag without evidence. Never discard `session_id`.
- ❌ Never suggest code that changes behavior beyond the flagged issue. Never hardcode `commit_id`.
