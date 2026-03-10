---
name: unity-debug-deep
description: Exhaustive multi-angle Unity bug analysis — read-only investigation across lifecycle, threading, state, data flow, and edge cases. Produces a structured report. Triggers — 'deep debug', 'analyze this bug', 'exhaustive analysis', 'debug report', 'root cause analysis', 'investigate this issue', 'trace this error', 'what's causing this'.
metadata:
  author: kuozg
  version: "1.1"
---
# unity-debug-deep

Exhaustive, read-only investigation that produces a structured analysis document covering all likely root causes across multiple investigation angles. Used by teams to document evidence before modifying production code.

## When to Use

- Bug is intermittent, race-condition-like, or has resisted 2+ fix attempts
- Team needs documented evidence before touching code
- Multiple systems are potentially involved
- Quick diagnosis (unity-debug-quick) looped 3+ times without resolution
- Root cause unclear; multiple hypotheses exist

## Workflow

1. **Parse symptom** — extract error message, timing, frequency, scope (editor/build/both)
2. **Select ≥3 angles** — from lifecycle, data flow, threading, state, edge cases, events, serialization (see investigation checklist)
3. **Investigate each angle** — use grep patterns, LSP, lsp_find_references to gather evidence; cite file:line
4. **Rank candidates** — sort by likelihood; mark HIGH/MED/LOW confidence per angle
5. **Propose solutions** — for each cause, describe WHAT and WHERE (not code, not HOW)
6. **Document** — write report using analysis template, citing evidence throughout

## Rules

- **Read-only** — never modify code during investigation
- **Multi-angle (≥3)** — always investigate 3+ angles (lifecycle, data flow, threading, state, edges, events, serialization)
- **Cite everything** — file:line for every cause candidate and solution location
- **Evidence first** — mark [UNCONFIRMED] for speculative claims; use grep/LSP exhaustively
- **Solutions WHAT/WHERE only** — describe the fix in plain language and exact location, not pseudocode/patches
- **Confidence scoring** — label HIGH/MED/LOW per candidate based on evidence strength
- **Template mandatory** — load analysis template BEFORE writing; follow structure exactly
- **Output path** — `Documents/Debug/ANALYSIS_{TOPIC}_{YYYYMMDD}.md`
- **2–4 solutions per cause** — multiple options with risk levels

## Output Format

`Documents/Debug/ANALYSIS_*.md` — sections: Summary, Reproduction, Root Causes (ranked), Solutions (WHAT/WHERE), Recommended Next Step. All causes cite file:line.

## Reference Files

- `references/analysis-template.md` — markdown template for the structured analysis output document

Load references on demand via `read_skill_file("unity-debug-deep", "references/{file}")`.

## Investigation Guide

Load these `unity-standards` references on demand:

- `debug/diagnosis-workflow.md` — parse symptom, categorize, solution format (read first)
- `debug/deep-investigation-checklist.md` — investigation angles, grep patterns, confidence scoring (read before investigating)
- `debug/common-unity-errors.md` — NRE, serialization, lifecycle, IL2CPP reference table
- `review/concurrency-checklist.md` — threading, race conditions, Jobs, main-thread safety
- `code-standards/lifecycle.md` — Awake/Start/OnEnable execution order, coroutine semantics

Via: `read_skill_file("unity-standards", "references/<path>")`
