---
name: unity-review-pr-local
description: "Local PR reviews for Unity projects without GitHub posting. Use when: (1) Reviewing code changes against conventions, (2) Identifying performance/memory issues, (3) Generating review as local markdown file, (4) Offline or draft reviews."
---

# Unity PR Reviewer (Local)

Review PRs against Unity coding standards and output results as a markdown file.

## Output Requirement (MANDATORY)

**Every review MUST follow the template**: [OUTPUT_TEMPLATE.md](.claude/skills/unity-review-pr-local/references/OUTPUT_TEMPLATE.md)

Save output to: `Documents/Reviews/PR_<number>_review.md`

Read the template first, then populate all sections.

## Severity Levels

| Level | Use When |
|-------|----------|
| 🔴 **Critical** | Memory leaks, crashes, game-breaking bugs |
| 🟡 **Major** | Architectural issues, missing error handling, `GetComponent` in Update |
| 🔵 **Minor** | Naming inconsistencies, style violations |
| 💚 **Suggestion** | Readability improvements, modern C# patterns |

## Quality Targets

- Method: < 30 lines
- Class: < 300 lines  
- Duplication: < 5%

## Review Workflow

1. **Fetch**: `gh pr diff --patch <number> > pr_diff.patch` (or `git diff main...HEAD` for local branches)
2. **Analyze**: Check against `.claude/rules/` conventions
3. **Audit**: Flag manifest changes, memory patterns, Update allocations
4. **Draft**: Categorize issues, write suggestion blocks
5. **Generate**: Create `Documents/Reviews/PR_<number>_review.md` using the template
6. **Summary**: Provide concise summary to user

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

## Output Format

Generate markdown file at `Documents/Reviews/PR_<number>_review.md`:

```markdown
# PR Review: #<number> - <title>

**Date**: <date>
**Reviewer**: Claude
**Verdict**: APPROVE | COMMENT | REQUEST_CHANGES

## Summary

<overall assessment>

## Statistics

| Severity | Count |
|----------|-------|
| 🔴 Critical | X |
| 🟡 Major | Y |
| 🔵 Minor | Z |
| 💚 Suggestion | N |

## Findings

### 🔴 Critical Issues

#### [File.cs:L42](file:///path/to/file.cs#L42)
**Issue**: Description
```suggestion
// Fix code here
```

### 🟡 Major Issues
...

### 🔵 Minor Issues
...

### 💚 Suggestions
...

## Verdict Rationale

<why APPROVE/COMMENT/REQUEST_CHANGES>
```

## Approval Logic

- **APPROVE**: No 🔴 or 🟡 issues
- **COMMENT**: Only 🔵/💚 issues
- **REQUEST_CHANGES**: Any 🔴 issues

See [OUTPUT_TEMPLATE.md](.claude/skills/unity-review-pr-local/references/OUTPUT_TEMPLATE.md) for full template.

---

## MCP Tools Integration

Optionally verify compilation and runtime behavior during local review.

| Operation | MCP Tool | Use Case |
| --------- | -------- | -------- |
| Check compilation | `coplay-mcp_check_compile_errors` | Verify changes compile before reviewing |
| Read console | `coplay-mcp_get_unity_logs(show_errors=true)` | Check for runtime errors |
| Play/stop game | `coplay-mcp_play_game` / `coplay-mcp_stop_game` | Smoke-test changes in Editor |
| Inspect hierarchy | `coplay-mcp_list_game_objects_in_hierarchy()` | Verify scene structure |
| Get object details | `coplay-mcp_get_game_object_info(gameObjectPath="...")` | Validate component changes |

### Review Verification Flow

```
1. coplay-mcp_check_compile_errors         → confirm code compiles
2. coplay-mcp_get_unity_logs(show_errors=true) → scan for warnings/errors
3. coplay-mcp_play_game                    → smoke-test if relevant
4. coplay-mcp_stop_game                    → end test session
```
