# Deep Mode — Investigation Report

Read-only, multi-angle investigation producing a structured analysis document. No code modifications.

## When to Use

- Bug is intermittent, timing-dependent, or race-condition-like
- 2+ fix attempts have already failed
- Multiple systems or threads are potentially involved
- User asks for "root cause analysis," "deep debug," or documented investigation
- Quick Mode looped 3+ times without resolution (auto-escalation)
- Team needs documented evidence before modifying production code

## Workflow

1. **Parse symptom** — extract error message, timing, frequency, scope (editor/build/both)
2. **Load references** — read `debug/deep-investigation-checklist.md` and `debug/analysis-template.md` from unity-standards BEFORE proceeding
3. **Select ≥3 angles** — from: lifecycle, data flow, threading, state transitions, edge cases, events, serialization (checklist has grep patterns per angle)
4. **Investigate each angle** — use grep, LSP, `lsp_find_references` to gather evidence; cite `file:line` for every finding
5. **Rank candidates** — sort by likelihood:
   - **HIGH**: Direct code evidence at `file:line` + reproducible pattern
   - **MED**: Likely candidate but indirect evidence; alternatives possible
   - **LOW**: Speculative — mark `[UNCONFIRMED]`
6. **Propose solutions** — 2–3 per cause, describe WHAT and WHERE (plain language, no code patches):
   ```
   WHAT: Re-acquire component reference in OnEnable instead of Awake
   WHERE: PlayerController.cs:42
   Risk: LOW
   ```
7. **Write report** — follow the analysis template exactly

## Rules

- **Read-only** — never modify project code during investigation
- **Multi-angle (≥3)** — always investigate 3+ angles from the checklist
- **Cite everything** — `file:line` for every cause candidate and solution location
- **Evidence first** — mark `[UNCONFIRMED]` for speculative claims without file evidence
- **Solutions describe WHAT/WHERE only** — no pseudocode, no patches
- **Template mandatory** — load `debug/analysis-template.md` before writing; follow structure exactly
- **2–3 solutions per cause** — multiple options with risk levels (LOW/MED/HIGH)

## Output

Save to `Documents/Debug/ANALYSIS_{TOPIC}_{YYYYMMDD}.md`

Sections: Summary → Root Cause Candidates (ranked HIGH/MED/LOW) → Solutions (WHAT/WHERE/Risk) → Recommended Next Step. All causes cite `file:line`.

## Standards

Load on demand from `unity-standards`:
- `debug/deep-investigation-checklist.md` — angles, grep patterns, confidence scoring
- `debug/analysis-template.md` — report template
- `debug/common-unity-errors.md` — error reference table
- `review/concurrency-checklist.md` — threading, race conditions, Jobs
- `code-standards/lifecycle.md` — execution order, coroutine semantics
