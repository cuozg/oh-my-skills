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

Save to `Documents/Debug/ANALYSIS_{SubjectName}_{YYYYMMDD}.md` using the template in `references/analysis-template.md`.

## Rules

- Investigate thoroughly. This is NOT the quick skill — take time to be certain.
- Minimum 3 cross-cut angles explored.
- Every claim must cite `File.cs:L##`.
- Solutions describe WHAT to do and WHERE — they do NOT include implementation code. If the user needs exact code changes, suggest using `unity-debug-fix` or `unity-fix-errors` instead.
- Never speculate without labeling it as such. Use "likely" or "unverified" for uncertain claims.
- If the investigation reveals the issue is simple, still fill the template — the user asked for deep analysis.
 If the root cause cannot be determined with certainty, state this and explain what additional information would help.
- Output the document. Do NOT just explain in conversation.
