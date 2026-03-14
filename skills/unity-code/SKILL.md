---
name: unity-code
description: >
  Unified Unity C# coding skill — write, extend, or optimize Unity code across all domains.
  Auto-triages: Quick (single-file MonoBehaviour, SO, interface, enum, struct, helper), Deep
  (multi-file features, services, state machines, refactors spanning 2+ classes), Editor
  (EditorWindow, CustomEditor, PropertyDrawer, Gizmos, MenuItem), Optimize (simplify/clean up
  without behavior change). MUST use for ANY Unity C# code request — writing scripts, adding
  components, implementing features, building systems, refactoring, creating inspectors, editor
  windows, gizmos, cleaning up code, reducing allocations. Triggers: "write a script," "quick
  component," "build a system," "implement feature," "refactor," "custom inspector," "editor
  window," "gizmo," "clean up," "simplify," "optimize this." Do not use for UI Toolkit
  (unity-uitoolkit-create), tests (unity-test-unit), or debugging (unity-debug).
metadata:
  author: kuozg
  version: "1.0"
---
# unity-code

Detect scope, pick mode, implement. Match local patterns, verify compilation, deliver complete code.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| One `.cs` file, quick script, narrow edit, single component | **Quick** |
| 2+ files, build system, implement feature, refactor across classes | **Deep** |
| Inspector, EditorWindow, PropertyDrawer, Gizmo, MenuItem | **Editor** |
| "Clean up," "simplify," "optimize," "reduce allocations," behavior unchanged | **Optimize** |

State triage: "This is [mode] — [reason]."

## Step 2 — Execute

### Quick Mode

1. **Qualify** — confirm one runtime `.cs` file suffices; escalate if scope grows
2. **Discover** — read target + 1-2 nearby files for namespace, serialization, attribute style
3. **Implement** — smallest complete change matching local style. For type templates (MB, SO, interface, enum, struct), load `code-standards/code-patterns.md`
4. **Verify** — `lsp_diagnostics` on changed file
5. **Handoff** — file path, what changed, diagnostics, editor follow-up (drag-drop, asset creation)

### Deep Mode

1. **Qualify** — confirm 2+ runtime files needed; switch to Quick if single-file
2. **Discover** — read affected files + 2-3 nearby for namespaces, asmdefs, registration style
3. **Plan** — list every file, responsibility, dependency order. Map ALL files before writing.
4. **Implement** — interfaces first → data/config → concrete logic → bootstrap/registration
5. **Verify** — `lsp_diagnostics` per dependency tier, then all files
6. **Handoff** — changed paths, verification, editor follow-up (SO assets, scene wiring, installer registration)

### Editor Mode

Load `read_skill_file("unity-code", "references/editor-mode.md")` for workflow, rules, and placement conventions.

Key points: save under `Editor/`, use `SerializedProperty` for Undo/Prefab support, `serializedObject.Update()`/`ApplyModifiedProperties()` around edits, register windows via `[MenuItem]` + `GetWindow<T>()`.

### Optimize Mode

1. **Read** — load file(s); fully understand current behavior before touching anything
2. **Identify** — dead code, redundant allocations, complex control flow, missing `readonly`/`sealed`, LINQ in hot paths, inconsistent style
3. **Refactor** — preserve behavior: cache `GetComponent`/`Find`, pool per-frame allocations, simplify conditionals, extract methods, add `sealed`/`readonly`, replace hot-path LINQ with loops
4. **Verify** — `lsp_diagnostics` on every changed file
5. **Report** — what changed, why, estimated perf impact

## Rules

- Local style wins — project patterns trump references
- Never leave `TODO`, stubs, or partially wired code
- One type per file, file name = type name (Deep/Editor)
- Bug fixes: minimal diff, no mixed refactors
- `lsp_diagnostics` after every code change
- Ambiguity → simplest implementation; state assumption in handoff

## Escalation

| From | To | When |
|------|----|------|
| Quick | Deep | Work requires a second file |
| Deep | Quick | Plan reveals single-file scope |
| Any | Editor | Target is editor domain |
| Any | Optimize | User pivots to cleanup-only |

Carry forward context; tell user why.

## Standards

Load on demand via `read_skill_file("unity-standards", "references/<path>")`:

- `code-standards/single-file-runtime-workflow.md` — Quick scope checks
- `code-standards/multi-file-workflow.md` — Deep dependency ordering, asmdef awareness
- `code-standards/code-patterns.md` — MB, SO, interface, enum templates
- `code-standards/architecture-patterns.md` — state machine, MVP, command
- `code-standards/refactoring-patterns.md` — extract, decompose, migrate
- `code-standards/naming.md` · `serialization.md` · `null-safety.md` · `lifecycle.md` · `events.md` · `dependencies.md`
- `code-standards/editor-patterns.md` · `gizmos-handles.md` — Editor boilerplate
