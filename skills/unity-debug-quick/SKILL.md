---
name: unity-debug-quick
description: >
  Use this skill to interactively diagnose Unity bugs — parse the symptom, investigate the codebase,
  propose 2+ solutions, let the user pick, apply the fix, and loop until resolved. Use when the user
  says "why is this broken," "fix this bug," "something is wrong," "this isn't working," or describes
  unexpected runtime behavior without a clear error. Do not use for compile errors with clear messages
  (unity-debug-fix) or for deep documented analysis (unity-debug-deep).
metadata:
  author: kuozg
  version: "1.0"
---
# unity-debug-quick

Interactive bug-diagnosis loop: surface root causes, offer choices, fix the chosen path, repeat until the issue is gone.

## When to Use

- A feature or system is behaving unexpectedly at runtime
- A quick "why is X not working" question with no clear cause yet
- NullReferenceException, missing reference, or logic regression
- Behavior differs between Editor and build

## Workflow

1. **Parse** — extract symptom, affected object, reproduction steps from the user's message
2. **Investigate** — use lsp_find_references, grep, or read the failing file to locate root cause candidates
3. **Analyze** — identify 2–4 possible causes ranked by likelihood
4. **Propose** — present ≥2 numbered solutions with impact and effort estimate
5. **Await** — wait for user to pick a solution (never auto-apply all)
6. **Fix** — apply the chosen fix minimally; run lsp_diagnostics on changed files
7. **Loop** — if issue persists or new symptom appears, return to step 1

## Rules

- Always propose ≥2 solutions before touching any code
- Never apply multiple solutions at once without user consent
- Never refactor unrelated code while fixing
- Read affected files before editing them
- Run lsp_diagnostics after every code change
- Cite file:line for every cause identified
- Keep fixes minimal — change only what is needed
- If root cause is ambiguous, ask one clarifying question before proposing solutions
- Escalate to unity-debug-deep if investigation exceeds 3 loops without resolution
- Surface the most likely cause first in the proposal list

## Output Format

Numbered solution list (cause + fix + effort) followed by the applied fix. Loop continues until zero symptoms remain.

## Standards

Load `unity-standards` for diagnosis guidance. Key references:

- `debug/diagnosis-workflow.md` — symptom parsing, multi-angle analysis
- `debug/common-unity-errors.md` — NRE, serialization, lifecycle, physics
- `code-standards/lifecycle.md` — Awake/Start/OnEnable order, coroutine rules

Load via `read_skill_file("unity-standards", "references/<path>")`.
