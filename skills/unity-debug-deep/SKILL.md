---
name: unity-debug-deep
description: "Deep investigation of Unity issues with exhaustive multi-angle analysis. Explores every avenue — lifecycle, threading, state, data flow, edge cases — then produces a structured analysis document. Never modifies code. Use when: (1) Complex bug that defies simple explanation, (2) Need to understand a deeply intertwined system, (3) Race conditions or timing-dependent issues, (4) Multi-system interactions causing unexpected behavior, (5) Need thorough written analysis for team review, (6) Issue has been investigated before without resolution. Triggers: 'deep debug', 'deep explain', 'analyze this thoroughly', 'investigate deeply', 'why does this really happen', 'exhaustive analysis', 'debug deep dive', 'root cause analysis', 'complex bug investigation', 'multi-system debug'."
---

# Unity Debug Deep

**Input**: Complex question, bug, or system behavior that requires exhaustive investigation
**Output**: Analysis document at `Documents/Debug/ANALYSIS_{SubjectName}_{YYYYMMDD}.md` using the template from `references/analysis-template.md`. NEVER modify project files.

## Hard Constraints

- **READ-ONLY**: Never edit, add, or modify any project file. Analysis only.
- **Never commit**: No git operations.
- **ALWAYS output document**: Save analysis to `Documents/Debug/` directory.
- **ALWAYS use template**: Follow `references/analysis-template.md` exactly.
- **Multi-angle**: Investigate from at least 3 different angles before concluding.

## Workflow

1. **Scope** — Define the question precisely. What is the subject? What is the expected vs actual behavior? What are the boundaries of investigation?
2. **Survey** — Broad sweep: identify all files, classes, and systems involved. Use `glob`, `grep`, `lsp_symbols` to map the landscape.
3. **Trace Forward** — Start from the trigger/entry point. Follow execution flow step by step. Document every branch, state change, and side effect.
4. **Trace Backward** — Start from the failure/symptom. Work backwards: who set this value? Who called this method? What state was required?
5. **Cross-Cut** — Investigate orthogonal angles:
   - **Lifecycle**: Is ordering (Awake/OnEnable/Start) a factor?
   - **Threading**: Any async/coroutine/callback boundaries?
   - **State**: Who else mutates the relevant state?
   - **Timing**: Frame-dependent? Scene-load-dependent? First-run-only?
   - **Edge Cases**: Empty collections? Null inputs? Destroyed objects?
   - **External**: Scriptable Objects? Inspector values? Prefab overrides?
6. **Hypothesize** — Form 2-4 hypotheses about the root cause. For each, find confirming or disproving evidence in the code.
7. **Conclude** — Select the most supported hypothesis. Document the evidence chain. Note remaining uncertainties.
8. **Write Report** — Fill the analysis template. Save to `Documents/Debug/`.

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

Use ALL relevant tools. This is a deep investigation — thoroughness over speed.

## Hypothesis Testing

For each hypothesis:

| Step | Action |
|:---|:---|
| **State** | One sentence: "The bug occurs because {X}" |
| **Predict** | "If true, we should see {Y} in the code" |
| **Search** | Use tools to find evidence for/against |
| **Verdict** | `CONFIRMED` / `DISPROVED` / `INCONCLUSIVE` + evidence |

Minimum 2 hypotheses. Maximum 4. Always test the "obvious" one AND at least one non-obvious alternative.

## Report Template

Save to: `Documents/Debug/ANALYSIS_{SubjectName}_{YYYYMMDD}.md`

ALWAYS use this exact structure (also in `references/analysis-template.md`):

```markdown
# Deep Analysis: {Subject}

**Date**: {YYYY-MM-DD}
**Question**: {The exact question or issue being investigated}
**Verdict**: {1 sentence conclusion}

---

## 1. Scope

**Subject**: {class/method/system being investigated}
**Expected Behavior**: {what should happen}
**Actual Behavior**: {what actually happens}
**Boundaries**: {what is in/out of scope}

## 2. System Map

**Files Involved**:
- `{File1.cs}` — {role in the issue}
- `{File2.cs}` — {role in the issue}

**Key Dependencies**:
- {ClassName} depends on {OtherClass} via {mechanism}

## 3. Forward Trace

Starting from {entry point}:

1. `{Class}.{Method}` (`File.cs:L##`) — {what happens}
2. `{Class}.{Method}` (`File.cs:L##`) — {what happens}
3. ... {continue full chain}

**Observations**: {what stands out in the forward trace}

## 4. Backward Trace

Starting from {failure point}:

1. `{Class}.{Method}` (`File.cs:L##`) — {the failure/symptom}
2. `{Class}.{Method}` (`File.cs:L##`) — {who called/set the failing value}
3. ... {continue backwards}

**Observations**: {what stands out in the backward trace}

## 5. Cross-Cut Analysis

### Lifecycle
{Is Unity lifecycle ordering a factor? Evidence.}

### Threading / Async
{Any async boundaries, coroutines, callbacks? Evidence.}

### State Mutations
{Who else writes to the relevant fields? Evidence.}

### Timing
{Frame-dependent? Load-order-dependent? Evidence.}

### Edge Cases
{Empty collections, null inputs, destroyed objects? Evidence.}

## 6. Hypotheses

### Hypothesis A: {title}
- **Claim**: {one sentence}
- **Prediction**: {what we'd expect to see if true}
- **Evidence**: {what we found}
- **Verdict**: `CONFIRMED` / `DISPROVED` / `INCONCLUSIVE`

### Hypothesis B: {title}
- **Claim**: {one sentence}
- **Prediction**: {what we'd expect to see if true}
- **Evidence**: {what we found}
- **Verdict**: `CONFIRMED` / `DISPROVED` / `INCONCLUSIVE`

{...more hypotheses if needed...}

## 7. Conclusion

**Root Cause**: {1-2 sentences explaining the definitive root cause}

**Evidence Chain**:
1. {fact} → 2. {fact} → 3. {fact} → {conclusion}

**Confidence**: `HIGH` / `MEDIUM` / `LOW` — {justification}

**Remaining Uncertainties**:
- {anything that couldn't be fully verified}

## 8. Recommended Next Steps

- {actionable recommendation 1}
- {actionable recommendation 2}
- {actionable recommendation 3}
```

## Rules

- Investigate thoroughly. This is NOT the quick skill — take time to be certain.
- Minimum 3 cross-cut angles explored.
- Minimum 2 hypotheses tested.
- Every claim must cite `File.cs:L##`.
- Never speculate without labeling it as such. Use "I believe" or "likely" for uncertain claims.
- If the investigation reveals the issue is simple, still fill the template — the user asked for deep analysis.
- Output the document. Do NOT just explain in conversation.
