# Quick Mode — Single-File Runtime C#

Write one complete `.cs` file: MonoBehaviour, ScriptableObject, interface, enum, struct, or helper class.

For code templates, naming conventions, and pattern details, refer to code-standards (loaded via the routing table). This file covers only the workflow.

## Workflow

1. **Qualify** — confirm one runtime `.cs` file suffices; escalate to Deep if scope grows
2. **Discover** — read target + 1-2 nearby runtime files for local patterns (see below)
3. **Implement** — smallest complete change following code-standards + local style
4. **Verify** — `lsp_diagnostics` on changed file, then `Unity.ReadConsole` for Unity console errors (see below)
5. **Handoff** — file path, what changed, diagnostics result, console verification result, editor follow-up if needed

## Discovery

Before writing, read the target file and 1-2 neighbors. Capture:

| What to capture | Where to find it |
|-----------------|-----------------|
| Namespace pattern | Top of any `.cs` file in the same folder |
| Field naming style | `_camelCase` vs `m_camelCase` vs `camelCase` |
| Serialization approach | Explicit `[SerializeField]` or `[field: SerializeField]` auto-props |
| Component caching | `Awake()` for `GetComponent`, or lazy in properties |
| Event pattern | C# `event Action<T>`, `UnityEvent`, or SO event channels |
| DI approach | Constructor injection, `[Inject]`, or `[SerializeField]` drag-drop |
| Null handling | Guard clauses, `TryGetComponent`, `?.` operator usage |

Match whatever the neighboring files do. Local style wins.

## Implementation Rules

- One type per file; file name matches type name
- Solve the requested behavior completely — no partial implementations
- No `TODO`, stubs, placeholder returns, or "wire this later" notes
- Keep surface minimal; avoid invented namespaces, XML docs, or attribute polish unless the prompt or local files call for them
- For code patterns and templates → code-standards `core-conventions.md` § Code Patterns
- For naming, access modifiers → code-standards `core-conventions.md` § Naming / § Access Modifiers

## Bug Fix Rules

- Minimal diff — change only what fixes the bug
- No mixed refactors — fix first, refactor separately
- One logical change per edit
- If the fix touches a second file, escalate to Deep mode

## Refactoring Rules

When the task is cleanup/simplification (not new code):
- Read the file fully before touching anything
- Identify issues by category (dead code, naming, access control, caching, duplication)
- One refactoring type per pass — do not extract, rename, and restructure simultaneously
- Preserve existing behavior — if you notice a bug, note it but do not fix it (separate concern)
- Use `[FormerlySerializedAs]` when renaming serialized fields
- Check callers via `lsp_find_references` before changing any public member

## Console Verification (MANDATORY)

After every code change, run the two-step verification:

1. **`lsp_diagnostics`** on the changed file — catches type errors, syntax issues instantly
2. **`Unity.ReadConsole`** `{ Action: "Get", Types: ["Error", "Warning"], Count: 50, Format: "Detailed" }` — reads the Unity console for compilation errors

**Parse console output:**
- `error CS####` → fix immediately, do not proceed to handoff
- `warning CS####` → note in handoff; fix if it indicates a real bug
- Assembly errors → check asmdef files and package dependencies
- Clean → proceed to handoff

**If Unity MCP is not available:** Run `lsp_diagnostics` only and add to handoff: "Console verification unavailable — verify in Unity Editor console."
**If LSP is not available but MCP is:** `Unity.ReadConsole` becomes the primary check; note LSP limitation in handoff.

This step is non-negotiable. `lsp_diagnostics` misses assembly reference issues, Unity-specific API problems, and package version mismatches that only Unity's compiler catches.

### Refactoring Standards to Load

Load these code-standards sections based on issue categories found:

| Issue category | Code-standards section |
|---------------|----------------------|
| Refactoring workflow, extraction, composition | `architecture-systems.md` § Refactoring Patterns |
| Access control (`sealed`, `readonly`, `private`, reduce API surface) | `core-conventions.md` § Access Modifiers |
| Null safety (`TryGetComponent`, guard clauses, `?.` chains) | `core-conventions.md` § Null Safety |
| Caching (`GetComponent`, `Camera.main`, repeated lookups) | `core-conventions.md` § Code Patterns |
| Dead code removal, naming fixes | `core-conventions.md` § Naming Conventions |
