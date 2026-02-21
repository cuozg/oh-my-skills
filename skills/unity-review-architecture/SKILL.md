---
name: unity-review-architecture
description: "Review Unity project architecture in PRs — dependency management, event systems, assembly structure, cross-system coupling, and architectural pattern compliance. Sub-skill of unity-review-code-pr orchestrator. Use when: delegated by unity-review-code-pr for architecture review. Triggers: 'review architecture', 'architecture review', 'DI review', 'coupling review'."
---

# Architecture Reviewer

Review architecture patterns across PR changes. Output partial review JSON for the orchestrator.

## Input

Receives from orchestrator: PR number, full file list (all types), diff context. Architecture review is cross-cutting — examines relationships between files, not individual file content.

## Severity Levels

| Level | Emoji | Meaning |
|:------|:------|:--------|
| CRITICAL | :red_circle: | Breaks functionality, data loss, crashes |
| HIGH | :yellow_circle: | Performance, UX, or logic issues |
| MEDIUM | :large_blue_circle: | Style, maintainability, minor UX |
| LOW | :green_circle: | Naming, conventions, suggestions |

## Key Concern Areas

| Area | What to Check |
|:-----|:-------------|
| Dependency Management | Proper DI usage, no service locators, no `FindObjectOfType` for service resolution, no manual `new` for injected services |
| Event Architecture | Event subscribe/unsubscribe pairing, no direct coupling between systems that should communicate via events |
| Assembly Structure | No circular dependencies, correct `.asmdef` references, internal vs public visibility |
| Cross-system Coupling | Services don't reference MonoBehaviours directly, proper abstraction layers |
| Data Flow | Interface-based data access, no direct field mutation across systems |

## Workflow

1. Load `unity-code-standards` skill for architecture patterns reference: `use_skill("unity-code-standards")`
2. Read full diff to understand scope of changes
3. Spawn explore agents to trace: dependency injection usage, event subscriptions, assembly references, cross-system calls
4. Check each changed `.cs` file for architecture violations using [ARCHITECTURE_PATTERNS.md](references/ARCHITECTURE_PATTERNS.md)
5. Check for new circular dependencies introduced by the PR
6. Classify findings, create comment objects
7. Return `{ "comments": [...], "max_severity": "..." }`

## Output Format

**ALWAYS use this exact output template:**

Each comment object:

```json
{
  "path": "Assets/Scripts/Services/MatchService.cs",
  "line": 15,
  "side": "RIGHT",
  "body": "**:red_circle: Manual Instantiation of Injected Service**: `new LobbyService()` bypasses the dependency injection graph.\n**Evidence**: Line 15 — constructor creates service directly instead of receiving it as a dependency.\n**Why**: Dependencies won't be resolved; class becomes untestable without manual setup.\n```suggestion\n// Receive via constructor injection instead of manual instantiation:\nprivate readonly ILobbyService _lobbyService;\npublic MatchService(ILobbyService lobbyService) { _lobbyService = lobbyService; }\n```"
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

- One issue = one comment object.
- Every comment MUST have: severity emoji, issue title, evidence (line/pattern), why, suggestion block.
- Architecture issues that are pre-existing should only be flagged if the PR makes them worse.
- Always load `unity-code-standards` for the authoritative architecture patterns.
- Batch pattern: full explanation on first occurrence, short reference on subsequent.
- Never handle `commit_id` or review submission — the orchestrator owns that.
- Refer to [ARCHITECTURE_PATTERNS.md](references/ARCHITECTURE_PATTERNS.md) for the complete pattern catalog.
