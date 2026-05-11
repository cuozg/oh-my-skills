---
name: unity-review-local
description: >
  Use this skill to review locally changed Unity C# files. Use when the user asks to "review my code", "check changes", or specific file paths without PR context.
metadata:
  author: kuozg
  version: "1.0"
---
# Unity Local Code Review

Review locally changed Unity C# files by adding inline `// ── REVIEW` comments.

## 1. Determine Review Scope

| User Request                  | Diff Command          | Scope                            |
| ----------------------------- | --------------------- | -------------------------------- |
| "review my changes" (default) | `git diff HEAD`     | All unstaged + staged changes    |
| "review staged changes"       | `git diff --cached` | Only staged changes              |
| "review this file" + path     | Read full file        | Specific file(s), no diff needed |
| "review since last commit"    | `git diff HEAD~1`   | Changes in last commit           |

**If no changes found:** Check `git status`. If working tree is clean, inform user: "No local changes to review. Did you mean to review a specific file or PR?"
**If scope is big:** Ask the user which specific criteria they need to review.

## 2. Group Files by Type

From the diff output, group files by their type (e.g., `.cs`, `.prefab`, `.unity`, `.mat`, `.shader`). Ignore `.meta` files.

## 3. Read Only Changed Lines

Review only the modified lines and their directly referenced methods/fields. Do not load the complete file content. Full context should only be pulled if an issue requires deeper investigation.

## 4. Spawn Parallel Review Subagents

See `unity-standards/references/review/parallel-review-criteria.md` for the subagent prompt template.
- When reviewing criteria with a big scope, try to split the work and spawn multiple reviewer subagents.

## 5. Collect Results

Wait and collect result from all sub agent, each returns a JSON array of findings.

## 6. Aggregate and Validate

1. Merge all findings into a single list
2. Deduplicate by (path, line) — keep highest severity
3. Sort by file path → line number
4. **Validate uncertain findings**: 
   - Dead code claims — verify nothing references the symbol
   - Missing unsubscription — verify the subscription actually exists
   - Unused variable — verify it's not used via reflection or serialization

## 7. Annotate Source Files

Insert `// ── REVIEW` comments directly above the problem line:
```csharp
// ── REVIEW {icon} {LABEL} #{category}
// What: 1-line summary
// Why:  1-3 lines - impact + evidence
```
- **Labels:** 🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🔵 LOW, ⚪ STYLE
- **Categories:** `null-safety` `lifecycle` `state` `concurrency` `allocation` `serialization` `event-leak` `logic` `security` `architecture`

## 8. Apply Safe Fixes

Apply only trivial, safe, single-line fixes:

- Add null check: `if (component != null)`
- Cache GetComponent: move to `Awake`/`Start` field
- Add missing unsubscription in `OnDisable`/`OnDestroy`
- Add `CompareTag` replacement for `tag ==`
- Add `[FormerlySerializedAs]` for renamed fields

**Never apply** multi-line refactors, architectural changes, or behavioral modifications. Leave those as `// ── REVIEW` comments.
Never commit review changes — leave for inspection
