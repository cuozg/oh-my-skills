---
name: unity-review-general
description: "Review PRs against general quality checklists — security, correctness, testing, code quality, performance, lifecycle, and documentation. Technology-agnostic checks applied alongside Unity-specific sub-skills. Sub-skill of unity-review-code-pr orchestrator. Use when: delegated by unity-review-code-pr for general review. Triggers: 'general review', 'security review', 'testing review', 'code quality review'."
---

# General Reviewer

Apply technology-agnostic quality checklists to PR changes. Output partial review JSON for the orchestrator.

## Input

Receives from orchestrator: PR number, full file list (all types), diff context, PR title/body for intent matching.

## Severity Levels

| Level | Emoji | Meaning |
|:------|:------|:--------|
| CRITICAL | :red_circle: | Breaks functionality, data loss, security vulnerability |
| HIGH | :yellow_circle: | Performance, correctness, or logic issue |
| MEDIUM | :large_blue_circle: | Best practice violation, maintainability risk |
| LOW | :green_circle: | Style, naming, documentation gap |

## PR Size Focus

| Changed Lines | Focus |
|:--------------|:------|
| < 50 | Security + Correctness + Testing only |
| 50-300 | All 7 checklists |
| > 300 | Request split. If not possible, prioritize Security + Correctness. Note scope risk in summary. |

## Checklists

Details in [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md). Brief overview:

1. :lock: **Security** — secrets, injection, auth, deserialization
2. :white_check_mark: **Correctness** — logic vs intent, state transitions, error paths
3. :test_tube: **Testing** — coverage for new/modified API, determinism
4. :broom: **Code Quality** — SRP, method length, duplication, naming
5. :zap: **Performance** — hot path allocations, data structures, async
6. :arrows_counterclockwise: **Lifecycle** — OnEnable/OnDisable pairs, teardown, quit flow
7. :books: **Documentation** — XML docs, inline comments, breaking change notes

## Workflow

1. Read PR title/body to extract intent and acceptance criteria.
2. Count changed lines to determine checklist focus (see size table).
3. Read diff for all changed files.
4. Apply each applicable checklist from [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md) against the changes.
5. For each violation, classify severity and create comment object.
6. Check: does the PR actually accomplish what the title/body says? Flag gaps.
7. Return `{ "comments": [...], "max_severity": "..." }`.

## Output Format

**ALWAYS use this exact output template:**

Each finding becomes one comment object:

```json
{
  "path": "Assets/Scripts/Auth/LoginManager.cs",
  "line": 45,
  "side": "RIGHT",
  "body": "**:red_circle: Hardcoded API Key**: API key string literal found in source.\n**Evidence**: Line 45 — `private string apiKey = \"sk-...\"`\n**Why**: Secrets in source are exposed in version control and builds.\n```suggestion\nMove to environment config or ScriptableObject excluded from version control.\n```"
}
```

**Return envelope** (MANDATORY — always return this exact JSON structure):

```json
{
  "comments": [ "...array of comment objects above..." ],
  "max_severity": "CRITICAL|HIGH|MEDIUM|LOW|CLEAN"
}
```

- `comments`: Array of comment objects. Empty array `[]` if no issues found.
- `max_severity`: The highest severity found across all comments. `"CLEAN"` if no issues.
```

## Rules

- One issue = one comment. Never combine multiple issues in a single comment.
- Every comment MUST include: severity emoji + title, **Evidence** (file + line), **Why** (impact), and a `suggestion` block.
- Correctness check: verify PR logic matches stated intent from PR title/body.
- Security findings are always :red_circle: Critical.
- For PRs > 300 lines, add a comment recommending split.
- If no issues found, return `{ "comments": [], "max_severity": "CLEAN" }`.
- Never handle `commit_id` or review submission — the orchestrator owns that.
- Refer to [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md) for the complete checklist catalog.
