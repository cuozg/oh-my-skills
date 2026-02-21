---
name: unity-debug-quick
description: "Investigate Unity issues to understand root cause, impact, and propose solutions — never modifies code. Use when: (1) User asks 'why does X happen?', (2) Need to understand a bug or unexpected behavior, (3) Tracing data flow to find where things go wrong, (4) Understanding why a value is wrong or null, (5) Explaining lifecycle or timing issues, (6) Need impact analysis of a bug, (7) Want proposed solutions without code changes. Triggers: 'explain why', 'why does this happen', 'explain this bug', 'what causes this', 'trace this issue', 'understand this behavior', 'why is this null', 'explain the flow', 'walk me through this', 'what is the impact', 'how to reproduce'."
---

# Unity Debug Quick

**Input**: User question about a bug, unexpected behavior, or issue they want investigated

## Hard Constraints

- **READ-ONLY**: Never edit, add, or modify any project file. Investigate and explain only.
- **Never commit**: No git operations.
- **Direct answer**: No report documents. Answer the user directly in conversation.
- **ALWAYS use template**: Follow the Response Template exactly.
- **Multiple solutions**: ALWAYS propose at least 2 solutions. Let the user choose.

## Workflow

1. **Parse Issue** — What exactly is wrong? Extract: the subject (class/method/system), the symptom (what user observes), and the expected behavior (what should happen instead).
2. **Read Code** — Open the relevant file(s). Read ±50 lines around the target. Understand what the code is doing.
3. **Trace Root Cause** — Follow the execution path using LSP tools. Trace callers, definitions, references. Map the data flow from source to the point of failure. Ask: who set this value? When? Under what conditions?
4. **Assess Impact** — What does this issue break? What systems depend on the affected code? Use `impact-analyzer` and `lsp_find_references` to map downstream effects.
5. **Find Solutions** — Propose 2-4 solutions with different trade-offs. Also consider workarounds. Do NOT write code — describe the approach.
6. **Respond** — Deliver the investigation using the Response Template.

## Tool Selection

| Need | Tool |
|:---|:---|
| Read target code | `read` |
| Find definition | `lsp_goto_definition` |
| Find who calls it | `lsp_find_references` |
| Find symbols | `lsp_symbols` (workspace) |
| Pattern search | `grep` / `ast_grep_search` |
| Blast radius | `impact-analyzer` |
| Broad sweep | `glob` |
| Check diagnostics | `lsp_diagnostics` |

Chain tools to build a complete picture. Stop when you have enough evidence to explain the root cause.

## Output

Structured investigation response per the Response Template below.

## Response Template

ALWAYS use this exact structure:

```
## Issue: {Short descriptive title of the issue}

### Overview

{1-3 sentences summarizing the issue. What is wrong, where, and what the user observes. Be specific — name classes, methods, variables. Cite with `FileName.cs:L##`.}

### Impact

{What does this issue cause or break? Be specific about downstream effects.}

- **{Affected system/feature}** — {how it is affected}
- **{Affected system/feature}** — {how it is affected}
- **Severity**: `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` — {1 sentence justification}

### Root Cause Analysis

**Why it happens**:

{2-5 sentences explaining the root cause. Not just "X is null" but "X is null because Y never assigns it when Z condition occurs". Trace it to the origin. Cite `File.cs:L##` for every claim.}

**Execution flow**:

1. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens at this step}
2. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens next}
3. ...{continue until the point of failure}

**Steps to reproduce**:

1. {Concrete step — e.g. "Open scene X"}
2. {Concrete step — e.g. "Enter Play Mode"}
3. {Concrete step — e.g. "Click button Y before Z finishes loading"}
4. {Observe: describe the symptom}

### Proposed Solutions

#### Solution 1: {Title} [RECOMMENDED]

- **Approach**: {1-2 sentences describing what to do}
- **Where**: `{FileName.cs:L##}` — {which method/area to change}
- **Trade-off**: {pros and cons — quick vs proper, risk level}
- **Effort**: `SMALL` / `MEDIUM` / `LARGE`

#### Solution 2: {Title}

- **Approach**: {1-2 sentences}
- **Where**: `{FileName.cs:L##}`
- **Trade-off**: {pros and cons}
- **Effort**: `SMALL` / `MEDIUM` / `LARGE`

#### Solution 3: {Title} (if applicable)

...same pattern...

### Workaround

{Is there a temporary workaround the user can apply right now to avoid the issue? If yes, describe it. If no workaround exists, say "No practical workaround — the root cause must be fixed."}

### Verification Steps

{How to verify the issue is fixed after applying a solution:}

1. {Step — e.g. "Apply Solution N"}
2. {Step — e.g. "Enter Play Mode and trigger X"}
3. {Step — e.g. "Verify that Y behaves correctly"}
4. {Step — e.g. "Check console for absence of error Z"}

### Prevention

- {How to prevent this class of issue in the future — coding practice, pattern, or safeguard}
- {Additional prevention measure if applicable}
- {Additional prevention measure if applicable}
```

## Template Rules

- **Overview**: 1-3 sentences max. Factual. No speculation. Cite file:line.
- **Impact**: List affected systems with bold labels. Always include Severity rating.
- **Root Cause Analysis**: Trace to the origin — not surface symptoms. Every claim cites `File.cs:L##`. Include execution flow (2-8 steps) and reproduction steps.
- **Proposed Solutions**: Minimum 2, maximum 4. Mark exactly one `[RECOMMENDED]`. Describe approach and location — do NOT write code. Include effort estimate.
- **Workaround**: A temporary bypass if one exists. Be honest if none exists.
- **Verification Steps**: Concrete steps to confirm the fix works. Minimum 2 steps.
- **Prevention**: 1-3 bullet points. Actionable practices, not generic advice.

## Rules

- Investigate the issue directly. No preamble, no narration.
- Cite with `FileName.cs:L##` inline throughout.
- Code snippets only when they clarify the explanation — never dump full methods.
- If the issue spans multiple systems, focus on the path that explains the root cause. Don't explain everything.
- If you can't determine the root cause with certainty, say "I'm not certain because {reason}" and note what additional information would help.
- If the user provides a stack trace, extract the error type, crash site, and call chain before investigating.
- If the user actually wants code fixes applied, suggest using `unity-debug-fix` or `unity-fix-errors` instead.
- Solutions describe WHAT to do and WHERE — they do NOT include code changes. That's `unity-debug-fix`'s job.
