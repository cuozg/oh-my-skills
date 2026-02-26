---
name: unity-review-architecture
description: "Review Unity project architecture in GitHub PRs — dependency management, event systems, assembly structure, cross-system coupling, and architectural pattern compliance. After review, pushes comments directly to GitHub via the API. Accepts PR number/URL as input. Use when: reviewing architecture in PRs, validating dependency/coupling changes before merge. Triggers: 'review architecture', 'architecture review', 'DI review', 'coupling review', 'PR architecture review', 'review PR architecture'."
---

# Architecture PR Reviewer

Review architecture patterns across PR changes in `.cs` files. Push review comments directly to GitHub via the API.

## Output
Review comments pushed to GitHub PR via API. Covers dependency management, event systems, assembly structure, cross-system coupling.

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

## Key Concern Areas

| Area | What to Check |
|:-----|:-------------|
| Dependency Management | Proper DI, no service locators, no `FindObjectOfType` for service resolution |
| Event Architecture | Subscribe/unsubscribe pairing, no direct coupling via events |
| Assembly Structure | No circular dependencies, correct `.asmdef` references |
| Cross-system Coupling | Services don't reference MonoBehaviours directly, proper abstractions |
| Data Flow | Interface-based data access, no direct field mutation across systems |

## Workflow

### 1. Fetch PR

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
gh pr diff <N>               # Full diff
```

Filter to `.cs` files. If none found, APPROVE with note `No C# files to review for architecture.`

### 2. Load Architecture Standards

```python
use_skill("unity-code-shared")  # Load authoritative architecture patterns
```

### 3. Deep Investigate (Parallel)

Spawn 2-3 `@explore` agents to trace: dependency injection usage, event subscriptions, assembly references, cross-system calls.

### 4. Architecture Review

For each changed `.cs` file, read the ENTIRE file (not just diff). Apply patterns from [ARCHITECTURE_PATTERNS.md](references/ARCHITECTURE_PATTERNS.md). Check for new circular dependencies introduced by the PR. Architecture issues that are pre-existing should only be flagged if the PR makes them worse.

### 5. Build `/tmp/review-architecture.json`

```json
{
  "body": "## Architecture Review\n**Scope**: [N files reviewed]\n...",
  "event": "COMMENT",
  "comments": [
    {
      "path": "Assets/Scripts/Services/MatchService.cs",
      "line": 15,
      "side": "RIGHT",
      "body": "**🔴 Manual Instantiation of Injected Service**: `new LobbyService()` bypasses DI.\n- **Why**: Dependencies won't be resolved; class becomes untestable.\n- **Fix**:\n```suggestion\nprivate readonly ILobbyService _lobbyService;\npublic MatchService(ILobbyService lobbyService) { _lobbyService = lobbyService; }\n```"
    }
  ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it automatically. Always set `event` to `"COMMENT"`.

### 6. Submit

```bash
./skills/unity-review-shared/scripts/post_review.py <pr_number> /tmp/review-architecture.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

## Rules

- Only review `.cs` files for architecture concerns. Read full files, not just diffs.
- One issue = one comment. Every comment needs severity + evidence + suggestion.
- Always load `unity-code-shared` for authoritative architecture patterns.
- Pre-existing issues: only flag if the PR makes them worse.
- Batch pattern: full explanation on first occurrence, short reference on subsequent. Submit even if PR is merged.
- Never hardcode `commit_id` or modify source files. Refer to [ARCHITECTURE_PATTERNS.md](references/ARCHITECTURE_PATTERNS.md) for the complete pattern catalog.
