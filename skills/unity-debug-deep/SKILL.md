---
name: unity-debug-deep
description: Exhaustive multi-angle Unity bug analysis — read-only investigation across lifecycle, threading, state, data flow, and edge cases. Produces a structured report. Triggers — 'deep debug', 'analyze this bug', 'exhaustive analysis', 'debug report', 'root cause analysis'.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-debug-deep

Exhaustive, read-only investigation that produces a structured analysis document covering all likely root causes across multiple angles.

## When to Use

- A bug is intermittent, race-condition-like, or has resisted quick fixes
- Team needs documented evidence before touching production code
- Multiple systems are potentially involved
- unity-debug-quick looped 3+ times without resolution

## Workflow

1. **Scope** — define the affected system, symptom, and reproduction steps
2. **Trace lifecycle** — map Awake/OnEnable/Start/OnDisable/OnDestroy order for involved objects
3. **Trace data flow** — follow the value from source to point of failure; grep for all writers/readers
4. **Check threading** — identify coroutines, async calls, Jobs, or main-thread-only API misuse
5. **Check state** — find every place the relevant state variable is read and written; map transitions
6. **Check edge cases** — null refs, empty collections, zero-division, order-of-operations
7. **Cross-reference** — use lsp_find_references for every symbol in the call path
8. **Rank causes** — sort candidates by likelihood; label each HIGH/MED/LOW confidence
9. **Document** — write the structured report using the analysis template

## Rules

- Never modify project code during deep debug — read only
- Investigate ≥3 angles (lifecycle, data flow, plus one more relevant angle)
- Cite file:line for every cause candidate
- Provide 2–4 solutions per cause with WHAT and WHERE
- Never speculate without file evidence — mark as [UNCONFIRMED] if needed
- Use grep/lsp_find_references before concluding "no other writers"
- Save output to `Documents/Debug/ANALYSIS_{TOPIC}_{YYYYMMDD}.md`
- Load the analysis template before writing the report
- Label causes HIGH/MED/LOW confidence based on evidence strength
- Do not include fix code in the report — describe WHAT and WHERE only

## Output Format

`Documents/Debug/ANALYSIS_*.md` — sections: Summary, Reproduction, Root Causes (ranked), Solutions (WHAT/WHERE), Recommended Next Step. All causes cite file:line.

## Reference Files

- `references/analysis-template.md` — markdown template for the structured analysis output document

Load references on demand via `read_skill_file("unity-debug-deep", "references/{file}")`.

## Standards

Load `unity-standards` for analysis checklists. Key references:

- `debug/diagnosis-workflow.md` — symptom parsing, multi-angle analysis
- `debug/common-unity-errors.md` — NRE, serialization, lifecycle, physics
- `review/concurrency-checklist.md` — threading, race conditions, main thread
- `code-standards/lifecycle.md` — Awake/Start/OnEnable order, coroutine rules

Load via `read_skill_file("unity-standards", "references/<path>")`.
