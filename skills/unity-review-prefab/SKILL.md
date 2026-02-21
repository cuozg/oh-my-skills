---
name: unity-review-prefab
description: "Review .prefab and .unity files in PRs for missing scripts, broken variant links, raycast issues, hierarchy problems, and Unity-specific YAML patterns. Sub-skill of unity-review-code-pr orchestrator. Use when: delegated by unity-review-code-pr to review prefab/scene files. Triggers: 'review prefab', 'prefab review', 'scene review', 'prefab changes'."
---

# Prefab & Scene Reviewer

Review `.prefab` and `.unity` files. Output partial review JSON for the orchestrator.

## Input

Receives from orchestrator: PR number, list of `.prefab`/`.unity` file paths, diff context.

## Severity Levels

| Level | Emoji | Meaning |
|:------|:------|:--------|
| CRITICAL | :red_circle: | Breaks functionality, data loss, crashes |
| HIGH | :yellow_circle: | Performance, UX, or logic issues |
| MEDIUM | :large_blue_circle: | Style, maintainability, minor UX |
| LOW | :green_circle: | Naming, conventions, suggestions |

## Workflow

1. **Read full YAML** of each changed `.prefab`/`.unity` file (not just diff — full context needed for YAML pattern matching)
2. **Run grep patterns** from [PREFAB_PATTERNS.md](references/PREFAB_PATTERNS.md) against each file
3. **Classify each hit** by severity and construct a comment object
4. **Return JSON array** of comments + overall severity to orchestrator

## Output Format

**ALWAYS use this exact output template:**

Each comment object:

```json
{
  "path": "Assets/Prefabs/Player.prefab",
  "line": 42,
  "side": "RIGHT",
  "body": "**:red_circle: Missing Script Reference**: `m_Script: {fileID: 0}` — component will throw MissingReferenceException at runtime.\n**Evidence**: Line 42 in prefab YAML.\n**Why**: Missing script GUID means the MonoBehaviour was deleted or its .meta file changed.\n```suggestion\n(Remove the component or restore the script GUID)\n```"
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
- `m_RaycastTarget: 1` hits — check if the GO has `Button`, `Toggle`, or `InputField`. If not, severity is :red_circle: Critical.
- Batch pattern: full explanation on first occurrence, short reference on subsequent.
- Never handle `commit_id` or review submission — the orchestrator owns that.
- Refer to [PREFAB_PATTERNS.md](references/PREFAB_PATTERNS.md) for the complete pattern catalog.
