---
name: unity-debug-deep
description: "Deep investigation of Unity issues with exhaustive multi-angle analysis. Investigates the issue from multiple angles — lifecycle, threading, state, data flow, edge cases — then produces a structured analysis document with overview, impact assessment, root cause analysis, multiple proposed solutions, workarounds, verification steps, and prevention guidance. Never modifies code. Use when: (1) Complex bug that defies simple explanation, (2) Need to understand a deeply intertwined system, (3) Race conditions or timing-dependent issues, (4) Multi-system interactions causing unexpected behavior, (5) Need thorough written analysis for team review, (6) Issue has been investigated before without resolution. Triggers: 'deep debug', 'deep explain', 'analyze this thoroughly', 'investigate deeply', 'why does this really happen', 'exhaustive analysis', 'debug deep dive', 'root cause analysis', 'complex bug investigation', 'multi-system debug'."
---

# Unity Debug Deep

**Input**: Complex question, bug, or system behavior that requires exhaustive investigation

## Hard Constraints

- **READ-ONLY**: Never edit, add, or modify any project file. Analysis only.
- **Never commit**: No git operations.
- **ALWAYS output document**: Save analysis to `Documents/Debug/` directory.
- **ALWAYS use template**: Follow `references/analysis-template.md` exactly.
- **Multi-angle**: Investigate from at least 3 different angles before concluding.
- **Multiple solutions**: ALWAYS propose at least 2 solutions, maximum 4. Let the user choose.

## Workflow

1. **Scope** — Define the issue precisely. What is the subject? What is expected vs actual behavior? What are the investigation boundaries?

2. **Survey** — Broad sweep: identify all files, classes, and systems involved. Use `glob`, `grep`, `lsp_symbols` to map the landscape.

3. **Trace Forward** — Start from the trigger/entry point. Follow execution flow step by step. Document every branch, state change, and side effect.

4. **Trace Backward** — Start from the failure/symptom. Work backwards: who set this value? Who called this method? What state was required?

5. **Cross-Cut** — Investigate orthogonal angles (minimum 3):
   - **Lifecycle**: Is ordering (Awake/OnEnable/Start) a factor?
   - **Threading**: Any async/coroutine/callback boundaries?
   - **State**: Who else mutates the relevant state?
   - **Timing**: Frame-dependent? Scene-load-dependent? First-run-only?
   - **Edge Cases**: Empty collections? Null inputs? Destroyed objects?
   - **External**: Scriptable Objects? Inspector values? Prefab overrides?

6. **Determine Root Cause** — Synthesize findings into a clear explanation of WHY the issue happens. Build an evidence chain from origin to symptom. Identify reproduction steps.

7. **Assess Impact** — What does this issue break downstream? What systems are affected? Rate severity.

8. **Formulate Solutions** — Generate 2-4 solution approaches with different trade-offs (quick fix vs proper fix vs architectural). Also identify any temporary workaround. Do NOT write implementation code — describe the approach and location.

9. **Write Report** — Fill the analysis template. Save to `Documents/Debug/`.

## Tool Selection

| Need | Tool |
|:---|:---|
| Read code | `read` |
| Find definition | `lsp_goto_definition` |
| Find all usages | `lsp_find_references` |
| Search symbols | `lsp_symbols` (workspace) |
| Pattern search | `grep` / `ast_grep_search` |
| Blast radius | `impact-analyzer` |
| File discovery | `glob` |
| Cross-reference | `lsp_find_references` chained |
| Check diagnostics | `lsp_diagnostics` |

Use ALL relevant tools. This is a deep investigation — thoroughness over speed.

## Output

Structured analysis document per the Report Template below. Save to `Documents/Debug/`.

## Report Template

Save to: `Documents/Debug/ANALYSIS_{SubjectName}_{YYYYMMDD}.md`

ALWAYS use this exact structure (also in `references/analysis-template.md`):

```markdown
# Deep Analysis: {Subject}

**Date**: {YYYY-MM-DD}
**Issue**: {The exact question or issue being investigated}
**Verdict**: {1 sentence conclusion — the root cause in plain language}

---

## 1. Overview

{1-3 sentences summarizing the issue. What is wrong, where, and what the user observes. Be specific — name classes, methods, variables. Cite with `FileName.cs:L##`.}

## 2. Impact

{What does this issue cause or break? Be specific about downstream effects.}

- **{Affected system/feature}** — {how it is affected}
- **{Affected system/feature}** — {how it is affected}

**Severity**: `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` — {1 sentence justification}

## 3. Root Cause Analysis

### Why It Happens

{3-8 sentences explaining the root cause. Not just "X is null" but "X is null because Y never assigns it when Z condition occurs, which itself stems from W". Trace it to the origin. Cite `File.cs:L##` for every claim.}

### Execution Flow

1. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens at this step}
2. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens next}
3. ...{continue until the point of failure}

### Cross-Cut Analysis

#### Lifecycle
{Is Unity lifecycle ordering a factor? Evidence from code.}

#### Threading / Async
{Any async boundaries, coroutines, callbacks? Evidence from code.}

#### State Mutations
{Who else writes to the relevant fields? Evidence from code.}

#### Timing
{Frame-dependent? Load-order-dependent? Evidence from code.}

#### Edge Cases
{Empty collections, null inputs, destroyed objects? Evidence from code.}

{Only include angles that are relevant to the issue. Skip sections that add no value.}

### Steps to Reproduce

1. {Concrete step — e.g. "Open scene X"}
2. {Concrete step — e.g. "Enter Play Mode"}
3. {Concrete step — e.g. "Trigger action Y while Z is in state W"}
4. {Observe: describe the symptom}

{If reproduction steps cannot be determined with certainty, note assumptions and say what additional information would help.}

## 4. Proposed Solutions

### Solution 1: {Title} [RECOMMENDED]

- **Approach**: {2-4 sentences describing what to do and why this works}
- **Where**: `{FileName.cs:L##}` — {which method/area to change}
- **Trade-off**: {pros and cons}
- **Risk**: `LOW` / `MEDIUM` / `HIGH` — {justification}
- **Effort**: `SMALL` / `MEDIUM` / `LARGE`

### Solution 2: {Title}

- **Approach**: {2-4 sentences}
- **Where**: `{FileName.cs:L##}`
- **Trade-off**: {pros and cons}
- **Risk**: `LOW` / `MEDIUM` / `HIGH` — {justification}
- **Effort**: `SMALL` / `MEDIUM` / `LARGE`

### Solution 3: {Title} (if applicable)

...same pattern...

## 5. Workaround

{Is there a temporary workaround the user can apply right now to avoid the issue without fixing the root cause? If yes, describe it clearly — steps to apply, limitations, and when it will stop working. If no workaround exists, say "No practical workaround — the root cause must be fixed."}

## 6. Verification Steps

{How to verify the issue is fixed after applying a solution:}

1. {Step — e.g. "Apply Solution N"}
2. {Step — e.g. "Enter Play Mode and trigger the scenario from Steps to Reproduce"}
3. {Step — e.g. "Verify that {expected behavior} occurs instead of {symptom}"}
4. {Step — e.g. "Check console for absence of error/warning messages"}
5. {Step — e.g. "Run related tests: {test class/method names if known}"}

## 7. Prevention

{How to prevent this class of issue in the future:}

- {Actionable practice, pattern, or safeguard — not generic advice}
- {Additional prevention measure if applicable}
- {Additional prevention measure if applicable}
```

## Solution Ranking Criteria

| Type | Description |
|:---|:---|
| **Quick Fix** | Minimal change, stops the symptom, might not address root cause fully |
| **Proper Fix** | Addresses root cause correctly, moderate effort |
| **Architectural Fix** | Redesigns the system to prevent this class of issue entirely |

Always include at least one Quick Fix and one Proper Fix. Architectural Fix only when warranted.
Mark exactly one solution as `[RECOMMENDED]`.

## Rules

- Investigate thoroughly. This is NOT the quick skill — take time to be certain.
- Minimum 3 cross-cut angles explored.
- Every claim must cite `File.cs:L##`.
- Solutions describe WHAT to do and WHERE — they do NOT include implementation code. If the user needs exact code changes, suggest using `unity-debug-fix` or `unity-fix-errors` instead.
- Never speculate without labeling it as such. Use "likely" or "unverified" for uncertain claims.
- If the investigation reveals the issue is simple, still fill the template — the user asked for deep analysis.
- If you can't determine the root cause with certainty, say so and explain what additional information would help.
- Output the document. Do NOT just explain in conversation.
