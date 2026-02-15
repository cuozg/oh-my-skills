---
name: unity-review-pr-local
description: "Local PR reviews for Unity projects without GitHub posting. Use when: (1) Reviewing code changes against conventions, (2) Identifying performance/memory issues, (3) Generating review as local markdown file, (4) Offline or draft reviews."
---

# Unity PR Reviewer (Local)

**Input**: PR number (`gh pr diff --patch <N>`), branch name (`git diff main...HEAD`), or uncommitted changes (`git diff`)
**Output**: Review at `Documents/Reviews/PR_<number>_review.md` per [OUTPUT_TEMPLATE.md](.opencode/skills/unity/unity-review-pr-local/references/OUTPUT_TEMPLATE.md)

## Severity Levels

| Level | Use When |
|-------|----------|
| 🔴 Critical | Memory leaks, crashes, game-breaking bugs |
| 🟡 Major | Architectural issues, missing error handling, `GetComponent` in Update |
| 🔵 Minor | Naming inconsistencies, style violations |
| 💚 Suggestion | Readability improvements, modern C# patterns |

## Quality Targets

Method: <30 lines | Class: <300 lines | Duplication: <5%

## Workflow

1. **Fetch** — `gh pr diff --patch <number>` or `git diff main...HEAD`
2. **Analyze** — check against `.opencode/rules/` conventions
3. **Audit** — flag manifest changes, memory patterns, Update allocations
4. **Draft** — categorize issues by severity, write suggestion blocks
5. **Generate** — create review markdown using template
6. **Summary** — provide concise summary to user

## Critical Patterns to Flag

```csharp
// 🔴 GetComponent in Update
void Update() { GetComponent<Rigidbody>(); }
// 🔴 Camera.main in loop
void Update() { Camera.main.transform; }
// 🟡 String concat in hot path
void Update() { label.text = "Score: " + score; }
// 🔴 Missing null after await
async Awaitable DoAsync() {
    await Awaitable.WaitForSecondsAsync(1f);
    transform.position = Vector3.zero; // May be destroyed!
}
```

## Approval Logic

- **APPROVE**: No 🔴 or 🟡 issues
- **COMMENT**: Only 🔵/💚 issues
- **REQUEST_CHANGES**: Any 🔴 issues
