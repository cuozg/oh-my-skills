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
- **ALWAYS use template**: Follow `references/response-template.md` exactly.

## Workflow

1. **Parse Error** — Extract error type, message, file:line, stack trace, frequency. See `references/error-parsing.md`.
2. **Read Crash Site** — Open the file at the error line. Read +/-50 lines of context.
3. **Trace Cause** — Follow the call chain upward. Who called this? Where did the bad state originate?
4. **Map Context** — What triggers this code path? What state is required? Other callers?
5. **Formulate Solutions** — Generate 2-4 fix approaches with different trade-offs.
6. **Present** — Output using `references/response-template.md`. Rank solutions. Include BEFORE/AFTER code.

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
- Solutions must be ordered: recommended first. Mark exactly one as `[RECOMMENDED]`.
- If you can't determine root cause with certainty, say so and explain what additional info would help.
- If the error is a simple typo or missing reference, still provide the full template.
- Never say "just add a null check" without explaining WHY the value is null and whether null check is the right fix.
