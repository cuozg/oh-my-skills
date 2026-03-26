---
name: unity-code
description: >
  Unified Unity runtime C# coding skill — write, extend, refactor, or structurally optimize
  runtime code. Auto-triages: Quick (single-file MonoBehaviour, ScriptableObject, interface,
  enum, struct, helper), Deep (multi-file features, services, state machines, refactors
  spanning 2+ classes), Optimize (behavior-preserving cleanup only). MUST use for ANY Unity
  runtime code request — creating scripts, adding components, implementing features, building
  systems, refactoring, or cleanup. Triggers: "write a script," "add a component," "build a
  system," "implement feature," "refactor," "clean up," "simplify." Do not use for performance
  optimization (unity-optimize), Editor scripts (unity-editor), UI Toolkit (unity-uitoolkit),
  tests (unity-test-unit), or debugging (unity-debug).
metadata:
  author: kuozg
  version: "2.1"
---
# unity-code

Detect scope, route references minimally, implement complete runtime code that matches local patterns.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| One `.cs` file, narrow runtime edit, single component/type | **Quick** |
| 2+ files, new feature/system, cross-class refactor | **Deep** |
| "Clean up," "simplify," behavior unchanged | **Optimize** |

State triage: "This is [mode] — [reason]."

## Step 2 — Route References

1. Read target files first; capture namespace, serialization, DI, event, lifecycle, asmdef, and naming patterns
2. Load one workflow ref only:
   - Quick → `code-standards/architecture-systems.md` (§ Single-File Runtime Workflow)
   - Deep → `code-standards/architecture-systems.md` (§ Multi-File Workflow)
   - Optimize → `code-standards/architecture-systems.md` (§ Refactoring Patterns)
3. Load only the refs directly implied by the work; use `read_skill_file("unity-code", "references/reference-routing.md")`
4. Keep the active ref set small: baseline + at most 2-3 targeted refs before writing. Re-load only if scope expands.
5. Prefer base refs over `*-advanced.md`; load advanced refs only for version-sensitive, package-specific, or genuinely complex work

## Step 3 — Execute

### Quick Mode

1. **Qualify** — confirm one runtime `.cs` file suffices; escalate if scope grows
2. **Discover** — read target + 1-2 nearby runtime files
3. **Implement** — smallest complete change matching local style. For new `MonoBehaviour`, `ScriptableObject`, or interface skeletons, load `code-standards/core-conventions.md`
4. **Verify** — `lsp_diagnostics` on changed file
5. **Handoff** — path, what changed, diagnostics, editor follow-up

### Deep Mode

1. **Qualify** — confirm 2+ runtime files are needed; switch to Quick if not
2. **Discover** — read affected files + nearby files for namespaces, asmdefs, registration, and folder layout
3. **Plan** — list every file, responsibility, dependency order, and required refs
4. **Implement** — contracts/data first → concrete logic → wiring/registration
5. **Verify** — `lsp_diagnostics` per dependency tier, then all files
6. **Handoff** — changed paths, verification, editor follow-up

### Optimize Mode

Structural cleanup only. For GC/allocation/frame-budget work, escalate to `unity-optimize`.

1. **Read** — understand current behavior fully before touching code
2. **Identify** — dead code, duplication, overgrown methods, weak naming, missing `readonly`/`sealed`, style drift
3. **Refactor** — preserve behavior with small safe transforms. Load only the targeted refs needed for the current smell.
4. **Verify** — `lsp_diagnostics` on every changed file
5. **Report** — what changed, why, and what complexity was reduced

## Rules

- Local style wins — project patterns trump refs
- Never bulk-load the whole `code-standards/` folder
- Never leave `TODO`, stubs, or half-wired code
- One type per file when creating new runtime types
- Bug fixes: minimal diff, no mixed refactors
- `lsp_diagnostics` after every code change
- Ambiguity → simplest implementation; state assumption in handoff

## Escalation

| From | To | When |
|------|----|------|
| Quick | Deep | Work requires a second file |
| Deep | Quick | Plan reveals single-file scope |
| Any | unity-editor | Target is editor domain |
| Any | unity-optimize | User wants performance optimization |
| Any | Optimize | User pivots to cleanup-only |

Carry forward context; tell user why.

## Standards

Load shared refs via `read_skill_file("unity-standards", "references/<path>")`.
Use `read_skill_file("unity-code", "references/reference-routing.md")` to choose the smallest relevant set, then pull only the exact `code-standards/*.md` files needed for the task.
For editor scripts (inspectors, windows, drawers, gizmos) → use **unity-editor**.
For performance optimization (GC, allocations, hot paths, draw calls) → use **unity-optimize**.
