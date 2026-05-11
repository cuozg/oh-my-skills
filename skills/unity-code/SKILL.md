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

Detect scope, load code-standards, discover local patterns, implement complete runtime code, verify via Unity console.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| One `.cs` file, narrow runtime edit, single component/type | **Quick** |
| 2+ files, new feature/system, cross-class refactor | **Deep** |
| "Clean up," "simplify," behavior unchanged | **Quick** or **Deep** (by file count) |

State triage: "This is [mode] — [reason]."

## Step 2 — Load References (In Order)

1. **Routing table** — `read_skill_file("unity-code", "references/reference-routing.md")` — identifies 1–3 code-standards files for this task
2. **Mode workflow** — `read_skill_file("unity-code", "references/quick-mode.md")` or `references/deep-mode.md`
3. **Code standards** — `read_skill_file("unity-standards", "references/code-standards/<file>.md")`
4. **MCP tools** (first use per session) — `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")`

Code-standards = single source of truth for all patterns, naming, conventions. Mode reference = procedural workflow only.

## Step 3 — Discover Local Patterns

Before writing any code, read target file + 1–2 nearby files. Capture:
- **Namespace** pattern (`Company.Project.Feature`)
- **Field style** (`_camelCase` vs `m_camelCase`)
- **Serialization** (`[SerializeField]` vs `[field: SerializeField]` auto-props)
- **Component caching** (`Awake()` GetComponent vs lazy properties)
- **Event pattern** (C# events, UnityEvent, SO channels)
- **DI approach** (constructor injection, `[Inject]`, Inspector drag-drop)

**Local style wins. Match what neighboring files do.**

## Step 4 — Execute

- **Quick:** Qualify → Discover → Implement → Verify → Handoff
- **Deep:** Qualify → Discover → Plan → Implement → Verify → Handoff

## Step 5 — Console Verification (MANDATORY — No Exceptions)

After every code change:
1. `lsp_diagnostics` on all changed files
2. `Unity.ReadConsole` via Unity MCP
3. **Errors (CS####)** → fix immediately, repeat · **Warnings** → note in handoff · **Clean** → handoff

**Fallbacks:** MCP only → note LSP limitation · LSP only → note "Console verification unavailable — verify in Unity Editor" · Both unavailable → manual review, note both limitations.

**Never declare complete without console verification or explicit fallback note.**

## Rules

- Code-standards is the single source of truth — do not invent patterns
- Local style wins over standards
- Never bulk-load all code-standards — routing table picks 1–3
- Never leave `TODO`, stubs, or half-wired code
- One type per file
- Bug fixes: minimal diff, no mixed refactors
- Ambiguity → simplest implementation; state assumption in handoff

## Escalation

| To | When |
|----|------|
| `unity-editor` | Target is editor domain |
| `unity-optimize` | User wants performance optimization |
| Quick → Deep | Work requires a second file |
| Deep → Quick | Plan reveals single-file scope |
