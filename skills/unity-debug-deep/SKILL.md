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

Follow [workflow.md](references/workflow.md) — Scope → Survey → Trace Forward → Trace Backward → Cross-Cut → Root Cause → Impact → Solutions → Report.

## Output

Save to `Documents/Debug/ANALYSIS_{SubjectName}_{YYYYMMDD}.md` using the template in `references/analysis-template.md`.

## Rules

- Investigate thoroughly. This is NOT the quick skill — take time to be certain.
- Minimum 3 cross-cut angles explored.
- Every claim must cite `File.cs:L##`.
- Solutions describe WHAT to do and WHERE — they do NOT include implementation code. If the user needs exact code changes, suggest using `unity-debug-fix` or `unity-debug-quick` instead.
- Never speculate without labeling it as such. Use "likely" or "unverified" for uncertain claims.
- If the investigation reveals the issue is simple, still fill the template — the user asked for deep analysis.
 If the root cause cannot be determined with certainty, state this and explain what additional information would help.
- Output the document. Do NOT just explain in conversation.

## Reference Files
- [workflow.md](references/workflow.md) — 9-step investigation workflow and tool selection
- [analysis-template.md](references/analysis-template.md) — Output template for analysis documents
