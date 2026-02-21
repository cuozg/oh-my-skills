---
name: unity-debug-fix
description: "Analyze Unity console errors and stack traces to understand the root cause, then suggest multiple fix solutions for the user to choose from. Never modifies code — presents solutions only. Use when: (1) Console shows an error or exception with stack trace, (2) Runtime crash or unexpected exception, (3) Compiler error with traceback, (4) Need to understand what a stack trace means, (5) Want fix options ranked by trade-offs, (6) Error keeps recurring and needs proper resolution. Triggers: 'fix this error', 'explain this stack trace', 'what does this error mean', 'how to fix', 'console error', 'stack trace help', 'exception fix', 'error solution', 'suggest fix', 'fix options for this error'."
---

# Unity Debug Fix

**Input**: Console error output — stack trace, error message, compiler error, or exception log

## Hard Constraints

- **READ-ONLY**: Never edit, add, or modify any project file. Suggest fixes only.
- **Never commit**: No git operations.
- **Multiple solutions**: ALWAYS provide at least 2 solutions, maximum 4. Let the user choose.
- **ALWAYS use template**: Follow the Response Template exactly.

## Workflow

1. **Parse Error** — Extract from the console output: error type, message, file:line, full stack trace, frequency hints.
2. **Read Crash Site** — Open the file at the error line. Read ±50 lines of context. Understand what the code is trying to do.
3. **Trace Cause** — Follow the call chain upward. Who called this? What value was expected? Where did the bad state originate?
4. **Map Context** — Understand the broader system: what triggers this code path? What state is required? Are there other callers?
5. **Formulate Solutions** — Generate 2-4 fix approaches with different trade-offs (quick vs proper, minimal vs architectural).
6. **Present** — Output using the Response Template. Rank solutions. Include code snippets showing the exact fix.

## Error Parsing Guide

### From Stack Trace
```
NullReferenceException: Object reference not set to an instance of an object
  at PlayerController.TakeDamage (System.Int32 damage) [0x00012] in /Assets/Scripts/PlayerController.cs:42
  at EnemyAI.Attack () [0x00034] in /Assets/Scripts/EnemyAI.cs:87
  at EnemyAI.Update () [0x00056] in /Assets/Scripts/EnemyAI.cs:31
```

Extract:
- **Error**: NullReferenceException
- **Crash Site**: `PlayerController.cs:42` — `TakeDamage` method
- **Call Chain**: `EnemyAI.Update:31` → `EnemyAI.Attack:87` → `PlayerController.TakeDamage:42`
- **Direction**: Read bottom-to-top (trigger → crash)

### From Compiler Error
```
Assets/Scripts/GameManager.cs(15,25): error CS0246: The type or namespace name 'PlayerData' could not be found
```

Extract:
- **Error**: CS0246 — missing type
- **File**: `GameManager.cs:15`
- **Subject**: `PlayerData` type

## Tool Selection

| Need | Tool |
|:---|:---|
| Read crash site | `read` |
| Find definition | `lsp_goto_definition` |
| Find all usages | `lsp_find_references` |
| Search symbols | `lsp_symbols` (workspace) |
| Pattern match | `grep` / `ast_grep_search` |
| Check diagnostics | `lsp_diagnostics` |
| File discovery | `glob` |

## Output

Structured diagnosis with ranked fix solutions per the Response Template below.

## Response Template

ALWAYS use this exact structure:

```
## Error Analysis: {ErrorType}

### Error Summary

| Field | Value |
|:---|:---|
| **Type** | {NullReferenceException / CS0246 / etc.} |
| **Message** | {exact error message} |
| **File** | `{FileName.cs:L##}` |
| **Method** | `{ClassName.MethodName}` |
| **Frequency** | {every frame / on action / once / unknown} |

### What's Happening

{2-4 sentences explaining what the error means in the context of THIS code. Not generic — specific to the user's code. Reference actual variable names, method names, class names. Cite `File.cs:L##`.}

### Root Cause

{2-4 sentences explaining WHY this error occurs. Trace it back to the origin — not just "X is null" but "X is null because Y never assigns it because Z". Cite evidence.}

### Call Chain

```
{Trigger} → {Step 1} → {Step 2} → {Crash Site}
```

1. `{Class}.{Method}` (`File.cs:L##`) — {what happens}
2. `{Class}.{Method}` (`File.cs:L##`) — {what happens}
3. **CRASH** → `{Class}.{Method}` (`File.cs:L##`) — {the failure}

---

### Solution 1: {Title} [RECOMMENDED]

**Approach**: {1 sentence describing the approach}
**Trade-off**: {quick fix / proper fix / architectural change} — {pros and cons}
**Risk**: `LOW` / `MEDIUM` / `HIGH`

```csharp
// {FileName.cs} — Line {N}
// BEFORE:
{existing code}

// AFTER:
{fixed code}
```

{1-2 sentences explaining why this works.}

### Solution 2: {Title}

**Approach**: {1 sentence}
**Trade-off**: {description}
**Risk**: `LOW` / `MEDIUM` / `HIGH`

```csharp
// {FileName.cs} — Line {N}
// BEFORE:
{existing code}

// AFTER:
{fixed code}
```

{1-2 sentences explaining why this works.}

### Solution 3: {Title} (if applicable)

...same pattern...

---

### Recommendation

{2-3 sentences: which solution you recommend and why. Consider: minimal disruption, correctness, future-proofing.}

### Prevention

- {How to prevent this class of error in the future — 1-3 bullet points}
```

## Solution Ranking Criteria

| Criteria | Description |
|:---|:---|
| **Quick Fix** | Minimal change, stops the crash, might not address root cause |
| **Proper Fix** | Addresses root cause, correct engineering, moderate effort |
| **Architectural Fix** | Redesigns the system to prevent this class of error entirely |

Always include at least one Quick Fix and one Proper Fix. Architectural Fix only when warranted.

## Rules

- Parse the EXACT error from the user's console output. Don't guess error types.
- Read the actual code at the crash site. Don't assume what the code does.
- Every solution must show BEFORE/AFTER code. No hand-wavy suggestions.
- Solutions must be ordered: recommended first.
- Mark exactly one solution as `[RECOMMENDED]`.
- If you can't determine the root cause with certainty, say so and explain what additional information would help.
- If the error is a simple typo or missing reference, still provide the full template — the user expects this format.
- Never say "just add a null check" without explaining WHY the value is null and whether the null check is the right fix.
