---
name: unity-code
description: >
  Unified Unity runtime C# coding skill — write, extend, or refactor runtime code
  using code-standards as the single source of truth for patterns and conventions.
  Integrates with Unity MCP for mandatory console verification after every code change.
  Auto-triages: Quick (single-file MonoBehaviour, ScriptableObject, interface, enum,
  struct, helper), Deep (multi-file features, services, state machines, refactors
  spanning 2+ classes). MUST use for ANY Unity runtime code request — creating scripts,
  adding components, implementing features, building systems, refactoring, or cleanup.
  Triggers: "write a script," "add a component," "build a system," "implement feature,"
  "refactor," "clean up," "simplify." Do not use for performance optimization
  (unity-optimize), Editor scripts (unity-editor), UI Toolkit (unity-uitoolkit),
  tests (unity-test-unit), or debugging (unity-debug).
metadata:
  author: kuozg
  version: "5.0"
---
# unity-code

Detect scope, load code-standards for the right conventions, discover local patterns, implement complete runtime code, and verify via Unity console.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| One `.cs` file, narrow runtime edit, single component/type | **Quick** |
| 2+ files, new feature/system, cross-class refactor | **Deep** |
| "Clean up," "simplify," behavior unchanged | **Quick** or **Deep** (by file count) — load refactoring standards |

State triage: "This is [mode] — [reason]."

## Step 2 — Load References

Load in this order — standards identification first, then mode workflow:

1. **Routing table** — `read_skill_file("unity-code", "references/reference-routing.md")` — scan task clues to identify which code-standards files apply (1-3 max)
2. **Mode workflow** — `read_skill_file("unity-code", "references/quick-mode.md")` or `references/deep-mode.md`
3. **Code standards** — load the identified files via `read_skill_file("unity-standards", "references/code-standards/<file>.md")`
4. **MCP tools** (on first use per session) — `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")` — load if unfamiliar with MCP console verification protocol

The routing table maps task clues → specific code-standards files and sections. Code-standards is the single source of truth for all patterns, templates, naming, and conventions. The mode reference provides only the procedural workflow.

**Budget**: mode workflow + 1-3 code-standards files + MCP tools reference (once per session). Reassess after discovery or scope changes.

## Step 3 — Discover Local Patterns

Before writing any code, read the target file and 1-2 nearby files. Capture:

- **Namespace** — `Company.Project.Feature` pattern
- **Field style** — `_camelCase` vs `m_camelCase`
- **Serialization** — explicit `[SerializeField]` or `[field: SerializeField]` auto-props
- **Component caching** — `Awake()` GetComponent or lazy properties
- **Event pattern** — C# events, UnityEvent, or SO channels
- **DI approach** — constructor injection, `[Inject]`, or Inspector drag-drop

Local style wins. Match whatever the neighboring files do.

## Step 4 — Execute

Follow the workflow in the loaded mode reference:

- **Quick** → Qualify → Discover → Implement → Verify → Handoff
- **Deep** → Qualify → Discover → Plan → Implement → Verify → Handoff

Apply patterns and conventions from code-standards within the mode workflow. Code-standards provides what to write; mode workflow provides how to organize the work.

## Step 5 — Console Verification (MANDATORY)

After every code change — no exceptions:

1. Run `lsp_diagnostics` on all changed files (fast, catches type errors and syntax issues)
2. Call `Unity.ReadConsole` via Unity MCP to read the Unity console output
3. Parse the result:
   - **Errors (CS####)** → fix immediately, repeat from Step 4
   - **Warnings** → note in handoff; fix if warning indicates a real bug
   - **Clean** → proceed to handoff

**Fallback scenarios:**
- MCP available, LSP unavailable → `Unity.ReadConsole` is the primary check; note LSP limitation in handoff
- MCP unavailable, LSP available → `lsp_diagnostics` only; note "Console verification unavailable — verify in Unity Editor console"
- Both unavailable → manual standards review; note both limitations in handoff

This catches what LSP misses: assembly reference issues, Unity-specific API problems, package version mismatches, serialization errors.

**Never skip this step. Never declare a task complete without console verification or an explicit fallback note.**

## Rules

- Code-standards is the single source of truth — do not invent patterns
- Local style wins when it conflicts with standards
- Never bulk-load all code-standards files — use routing table to pick 1-3
- Never leave `TODO`, stubs, or half-wired code
- One type per file when creating new runtime types
- Bug fixes: minimal diff, no mixed refactors
- `lsp_diagnostics` after every code change
- `Unity.ReadConsole` after every code change (mandatory when MCP available)
- Ambiguity → simplest implementation; state assumption in handoff

## Escalation

| From | To | When |
|------|----|------|
| Quick | Deep | Work requires a second file |
| Deep | Quick | Plan reveals single-file scope |
| Any | unity-editor | Target is editor domain |
| Any | unity-optimize | User wants performance optimization |

Carry forward context; tell user why.

## Standards

Load shared refs via `read_skill_file("unity-standards", "references/code-standards/<path>")`.
Use `read_skill_file("unity-code", "references/reference-routing.md")` to choose the smallest relevant set.
For MCP tools reference → `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")`.
For editor scripts (inspectors, windows, drawers, gizmos) → use **unity-editor**.
For performance optimization (GC, allocations, hot paths, draw calls) → use **unity-optimize**.
