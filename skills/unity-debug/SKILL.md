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

| Signal                                                             | Mode            | Action                      |
| ------------------------------------------------------------------ | --------------- | --------------------------- |
| `CS####` codes, red console, compiler errors, "fix this error"   | **Fix**   | `references/fix-mode.md`  |
| Runtime bug, NRE, wrong behavior, "fix this bug", first encounter  | **Quick** | Inline below                |
| Intermittent, 2+ failed fixes, multi-system, "root cause analysis" | **Deep**  | `references/deep-mode.md` |
| "Add debug logs", "trace this value", "logging for this method"    | **Log**   | Inline below                |

When uncertain, start in Quick — cheaper to escalate than over-invest. State the triage:

> "This looks like a [type]. I'll [approach]. Sound right?"

## Step 2 — Execute

### Fix Mode (Auto-Fix Loop)

Follow `references/fix-mode.md`: Parse error → locate root cause → propose 2–3 fix approaches → apply chosen fix → verify with `lsp_diagnostics` → loop until zero errors. Stop and report after 5 iterations without progress.

### Quick Mode (Interactive Fix Loop)

1. **Parse** — extract symptom, affected object/system, reproduction steps
2. **Investigate** — read affected files, `lsp_find_references`, grep. Check ≥3 angles from `debug/diagnosis-workflow.md`
3. **Propose** — present 2–3 numbered solutions with risk and effort:
   ```
   1. [Safest] Guard null + lazy init in PlayerController.cs:42 — Low risk, 5 min
   2. [Proper] Re-acquire ref in OnEnable — Med risk, 15 min
   3. [Architectural] Inject dependency via SO — High risk, 1 hr
   ```
4. **Await** — user picks (never auto-apply)
5. **Fix** — apply minimally; `lsp_diagnostics` on changed files
6. **Verify** — if symptom persists, loop back to step 1

### Deep Mode (Investigation Report)

Follow `references/deep-mode.md`: Read-only, multi-angle (≥3) investigation. Cite `file:line` for all findings. Rank causes HIGH/MED/LOW. Write report to `Documents/Debug/ANALYSIS_{TOPIC}_{YYYYMMDD}.md`. Propose 2–3 solutions per cause (WHAT/WHERE only, no code patches).

### Log Mode (Debug Snippets)

1. **Identify** — what value/event/method to trace, which class
2. **Format** — `[DBG]` prefix, `<color=cyan>` tag, `$"..."` interpolation, `#if UNITY_EDITOR` guard
3. **Output** — print as code block. **Never write to project files.**

Use `Debug.LogWarning` for unexpected-but-handled states, `Debug.LogError` for failures. Include `this` as context object for click-to-select. Load `debug/log-format.md` for color codes and compound formats.

## Core Rules

- **Always propose ≥2 solutions** before touching any code (Fix, Quick, and Deep modes)
- Never apply multiple solutions at once without user consent
- Never refactor unrelated code while fixing
- Read affected files before editing
- Run `lsp_diagnostics` after every code change
- Cite `file:line` for every cause identified
- Keep fixes minimal — change only what is needed
- If root cause is ambiguous after investigation, ask one clarifying question

## MCP Console Tools

When Unity MCP is available, use console tools to read errors and verify fixes. Pick the right tool:

| Need | Tool | Why |
|------|------|-----|
| Quick error check (what errors exist?) | `Unity.GetConsoleLogs` | Fast, returns errors/warnings/messages with stack traces |
| Filter by text/timestamp | `Unity.ReadConsole(Get)` | Supports `FilterText`, `SinceTimestamp`, structured output (Json format) |
| Clear console before a test run | `Unity.ReadConsole(Clear)` | Only way to clear — `GetConsoleLogs` is read-only |
| Verify fix after code change | `Unity.ReadConsole(Get)` with `SinceTimestamp` | Checks only NEW errors since the fix was applied |

**Guard clauses:**
- Don't use `GetConsoleLogs` if you need text filtering — use `ReadConsole(Get)` with `FilterText`
- Don't use `GetConsoleLogs` to clear console — use `ReadConsole(Clear)`
- Use `ReadConsole` with `Format=Json` when you need structured output for programmatic parsing

For the full console tool decision tree, load `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")` — see the **Debugging Branch**.

## Escalation

| From  | To    | Trigger                                                 |
| ----- | ----- | ------------------------------------------------------- |
| Fix   | Quick | Errors cleared but behavioral bug remains               |
| Quick | Deep  | 3 loops without resolution, or multi-system involvement |
| Deep  | Quick | Report identifies clear single-system fix               |

On escalation, carry forward all evidence gathered. Tell the user why you're switching.

## Standards

Load `unity-standards` references on demand via `read_skill_file("unity-standards", "references/<path>")`:

- `debug/diagnosis-workflow.md` — symptom parsing, categorization, multi-angle rule, solution format
- `debug/deep-investigation-checklist.md` — investigation angles, grep patterns, confidence scoring
- `debug/common-unity-errors.md` — NRE, serialization, lifecycle, IL2CPP reference table
- `debug/analysis-template.md` — structured report template for Deep Mode output
- `debug/log-format.md` — Debug.Log format, color tags, UNITY_EDITOR guard
- `other/unity-mcp-routing-matrix.md` — MCP console tool decision tree, guard clauses (GetConsoleLogs vs ReadConsole)
