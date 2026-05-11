---
name: unity-debug
description: >
  Unified Unity debugging skill — diagnose and fix any Unity bug, from compile errors to complex
  intermittent issues. Automatically triages into the right mode: Fix (compile errors, auto-fix loop),
  Quick (runtime bugs, interactive 2-3 solution proposals), Deep (intermittent/multi-system, read-only
  investigation report), or Log (generate formatted Debug.Log snippets). Use when the user says
  "fix this bug," "fix this error," "why is this broken," "debug this," "root cause analysis,"
  "auto fix," "resolve these compile errors," "add debug logs," "trace this value," "something is
  wrong," "this isn't working," or describes unexpected behavior, pastes a stack trace, or reports
  "works in editor but not in build." Also use when a bug has resisted 2+ fix attempts and needs
  documented analysis.
metadata:
  author: kuozg
  version: "2.1"
---
# unity-debug

Detect bug type, select mode, execute the right workflow. Always propose 2–3 solutions before touching code.

## Step 1 — Detect Mode

| Signal | Mode | Action |
|--------|------|--------|
| `CS####` codes, red console, compiler errors | **Fix** | `references/fix-mode.md` |
| Runtime bug, NRE, wrong behavior, first encounter | **Quick** | Inline below |
| Intermittent, 2+ failed fixes, multi-system, "root cause" | **Deep** | `references/deep-mode.md` |
| "Add debug logs", "trace this value" | **Log** | Inline below |

When uncertain, start in Quick. State triage: "This looks like a [type]. I'll [approach]. Sound right?"

## Step 2 — Execute

### Fix Mode
Follow `references/fix-mode.md`: Parse error → locate root → propose 2–3 approaches → apply chosen → `lsp_diagnostics` → loop until zero errors. Stop and report after 5 iterations without progress.

### Quick Mode
1. **Parse** — symptom, affected object/system, reproduction steps
2. **Investigate** — read affected files, `lsp_find_references`, grep ≥3 angles from `debug/diagnosis-workflow.md`
3. **Propose** — 2–3 numbered solutions with risk and effort:
   ```
   1. [Safest] Guard null + lazy init in PlayerController.cs:42 — Low risk, 5 min
   2. [Proper] Re-acquire ref in OnEnable — Med risk, 15 min
   3. [Architectural] Inject via SO — High risk, 1 hr
   ```
4. **Await** user pick (never auto-apply)
5. **Fix** minimally, `lsp_diagnostics` on changed files
6. **Verify** — if symptom persists, loop from step 1

### Deep Mode
Follow `references/deep-mode.md`: Read-only, ≥3 angles investigation. Cite `file:line`. Rank causes HIGH/MED/LOW. Write report to `Documents/Debug/ANALYSIS_{TOPIC}_{YYYYMMDD}.md`. Propose 2–3 solutions per cause (WHAT/WHERE only, no code patches).

### Log Mode
1. Identify what to trace and which class
2. Format: `[DBG]` prefix · `<color=cyan>` tag · `$"..."` interpolation · `#if UNITY_EDITOR` guard
3. Output as code block — **never write to project files**
   - `Debug.LogWarning` for unexpected-but-handled · `Debug.LogError` for failures · Include `this` for click-to-select

## Rules

- **Always propose ≥2 solutions before touching any code**
- Never apply multiple solutions at once without user consent
- Never refactor unrelated code while fixing
- Read affected files before editing
- `lsp_diagnostics` after every code change
- Cite `file:line` for every cause identified
- Keep fixes minimal — change only what is needed

## MCP Console Tools

| Need | Tool |
|------|------|
| Quick error check | `Unity.GetConsoleLogs` |
| Filter by text/timestamp | `Unity.ReadConsole(Get)` with `FilterText`, `SinceTimestamp` |
| Clear console | `Unity.ReadConsole(Clear)` |
| Verify fix after change | `Unity.ReadConsole(Get)` with `SinceTimestamp` |

Full decision tree: `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")` → Debugging Branch.

## Escalation

| From | To | Trigger |
|------|-----|---------|
| Fix | Quick | Errors cleared but behavioral bug remains |
| Quick | Deep | 3 loops without resolution, or multi-system |
| Deep | Quick | Report identifies clear single-system fix |

## Standards

`read_skill_file("unity-standards", "references/<path>")`:
- `debug/diagnosis-workflow.md` · `debug/deep-investigation-checklist.md`
- `debug/common-unity-errors.md` · `debug/analysis-template.md`
- `debug/log-format.md` · `other/unity-mcp-routing-matrix.md`
