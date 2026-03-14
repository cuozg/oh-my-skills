---
name: flutter-debug
description: >
  Unified Flutter/Dart debugging skill — diagnose and fix any Flutter bug, from Dart analysis errors
  to complex intermittent issues. Automatically triages into the right mode: Fix (Dart compile/analysis
  errors, auto-fix loop), Quick (runtime crashes, widget errors, interactive 2-3 solution proposals),
  Deep (intermittent/multi-system, read-only investigation report), or Log (generate structured logging
  snippets). Use when the user says "fix this bug," "fix this error," "why is this broken," "debug this,"
  "root cause analysis," "auto fix," "resolve these analysis errors," "add debug logs," "trace this value,"
  "something is wrong," "this isn't working," or describes unexpected behavior, pastes a stack trace,
  or reports "works on emulator but not on device." Also use when a bug has resisted 2+ fix attempts
  and needs documented analysis.
metadata:
  author: kuozg
  version: "1.0"
---
# flutter-debug

Detect bug type, select mode, execute the right workflow. Always propose 2-3 solutions before touching code.

## Step 1 — Detect Mode

| Signal | Mode | Action |
|--------|------|--------|
| Dart analysis errors, `dart analyze` failures, "fix this error" | **Fix** | `references/fix-mode.md` |
| Runtime crash, null assertion, widget error, "fix this bug", first encounter | **Quick** | `references/quick-mode.md` |
| Intermittent, 2+ failed fixes, multi-system, "root cause analysis" | **Deep** | `references/deep-mode.md` |
| "Add debug logs", "trace this value", "logging for this method" | **Log** | `references/log-mode.md` |

When uncertain, start in Quick — cheaper to escalate than over-invest. State the triage:
> "This looks like a [type]. I'll [approach]. Sound right?"

## Step 2 — Execute

### Fix Mode (Auto-Fix Loop)

Follow `references/fix-mode.md`: Run `dart analyze` → parse errors → locate root cause → propose 2-3 fix approaches → apply chosen fix → re-run `dart analyze` → loop until zero errors. Stop and report after 5 iterations without progress.

### Quick Mode (Interactive Fix Loop)

1. **Parse** — extract symptom, affected widget/provider/service, stack trace, reproduction steps
2. **Investigate** — read affected files, trace call chain, grep for related patterns. Check state management, lifecycle, async, and widget tree angles
3. **Propose** — present 2-3 numbered solutions with risk and effort:
   ```
   1. [Safest] Add null check + fallback in UserProfile.build():42 — Low risk, 5 min
   2. [Proper] Initialize provider in correct scope — Med risk, 15 min
   3. [Architectural] Restructure state with AsyncValue — High risk, 1 hr
   ```
4. **Await** — user picks (never auto-apply)
5. **Fix** — apply minimally; run `dart analyze` on changed files
6. **Verify** — if symptom persists, loop back to step 1

### Deep Mode (Investigation Report)

Follow `references/deep-mode.md`: Read-only, multi-angle (>=3) investigation. Cite `file:line` for all findings. Rank causes HIGH/MED/LOW. Write report to `Documents/Debug/ANALYSIS_{TOPIC}_{YYYYMMDD}.md`. Propose 2-3 solutions per cause (WHAT/WHERE only, no code patches).

### Log Mode (Debug Snippets)

Follow `references/log-mode.md`:
1. **Identify** — what value/event/method to trace, which class
2. **Format** — use `package:logger` (log.d/i/w/e), structured `[ClassName.method]` prefix
3. **Guard** — wrap with `assert()` or `kDebugMode` check for production safety
4. **Output** — print as code block. **Never write to project files.**

## Core Rules

- **Always propose >=2 solutions** before touching any code (Fix, Quick, and Deep modes)
- Never apply multiple solutions at once without user consent
- Never refactor unrelated code while fixing
- Read affected files before editing
- Run `dart analyze` after every code change
- Cite `file:line` for every cause identified
- Keep fixes minimal — change only what is needed
- Never suppress errors with `// ignore:` directives
- If root cause is ambiguous after investigation, ask one clarifying question

## Escalation

| From | To | Trigger |
|------|----|---------|
| Fix | Quick | Analysis errors cleared but runtime bug remains |
| Quick | Deep | 3 loops without resolution, or multi-system involvement |
| Deep | Quick | Report identifies clear single-system fix |

On escalation, carry forward all evidence gathered. Tell the user why you're switching.

## Standards

Load `flutter-standards` references on demand via `read_skill_file("flutter-standards", "references/<path>")`:

- `error-handling.md` — exception hierarchies, Result pattern, error boundaries
- `debug-logging.md` — structured logging, log levels, production safety
- `async-streams.md` — Future/Stream patterns, cancellation, error propagation
- `performance-optimization.md` — rebuild profiling, DevTools, const widgets
- `state-management-guide.md` — Riverpod patterns, provider scoping, lifecycle
