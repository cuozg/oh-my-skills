---
name: unity-code-quick
description: >
  Use this skill whenever the user wants a small Unity runtime C# change that stays inside one .cs file —
  a MonoBehaviour, ScriptableObject, interface, enum, struct, data model, static helper, or a narrow edit
  to an existing runtime script. Reach for it even when they ask for "a quick script," "one-file fix," or
  "write me a simple component." Do not use for editor tooling (unity-code-editor), UI Toolkit
  (unity-uitoolkit-create), tests (unity-test-unit), optimization-only passes (unity-code-optimize), or
  anything needing multiple files (unity-code-deep).
metadata:
  author: kuozg
  version: "2.0"
---

# unity-code-quick

Deliver small runtime Unity C# work inside one file. Match local patterns, keep the diff narrow, finish with a compilable handoff.

## Scope

**Use when:** New MonoBehaviour, ScriptableObject, interface, enum, struct, utility class — or a narrow edit to one existing runtime `.cs` file.

**Switch out if:** Work needs 2+ files (`unity-code-deep`), editor tooling (`unity-code-editor`), UI Toolkit (`unity-uitoolkit-create`), tests (`unity-test-unit`), or optimization-only cleanup (`unity-code-optimize`).

## Workflow

1. **Gate** — Confirm one runtime `.cs` file is enough. Switch immediately if scope grows.

2. **Discover** — Read the target file plus 1-2 nearby runtime files. Capture:
   - Namespace style (file-scoped vs block-scoped)
   - Using directives already present
   - Serialization pattern: `[SerializeField] private` vs `[field: SerializeField]`
   - Attribute usage: `[Header]`, `[RequireComponent]`, `[DisallowMultipleComponent]`
   - Access modifier conventions (sealed? explicit private?)
   - Comment and XML doc density

   If the project has no nearby files, load `read_skill_file("unity-standards", "references/code-standards/single-file-runtime-workflow.md")`.

3. **Implement** — Write the smallest complete change. Follow type-specific guidance:

   - **MonoBehaviour** — Pick the correct lifecycle method: `Awake` for caching refs, `FixedUpdate` for physics, `LateUpdate` for follow cameras. Expose designer data via `[SerializeField]` with `[Header]`/`[Tooltip]` when it aids inspector clarity. Add `[RequireComponent]` for hard dependencies. Subscribe events in `OnEnable`, unsubscribe in `OnDisable`.
   - **ScriptableObject** — Always add `[CreateAssetMenu]`. Prefer `[field: SerializeField] public T Prop { get; private set; }` for runtime-immutable data. Keep it a data container — logic belongs in consumers.
   - **Interface** — Properties and methods only. No default implementations unless the project already uses C# 8+ default interface methods.
   - **Enum** — Use `[Flags]` only when bitwise combinations are needed; assign power-of-2 values explicitly with `None = 0`. Standard enums start at 0 by default.
   - **Struct** — Prefer `readonly struct` for immutable data. Keep small (under 4 fields) to avoid copy overhead.
   - **Static utility** — Seal the class, make it static, hide construction. Pure functions, no state.

4. **Verify** — Run `lsp_diagnostics` on the changed file. Fix any introduced errors before reporting done.

5. **Handoff** — Report: file path, what changed, diagnostics status, any Unity Editor follow-up (drag-drop refs, asset creation, scene wiring).

## Rules

- **One file only.** A second file means switching to `unity-code-deep`. Single-file discipline prevents half-wired systems.
- **Local style wins.** Project patterns trump standard references — consistency in a codebase matters more than "correct" style in isolation.
- **Minimal surface.** Skip namespaces, XML docs, attributes, or polish the prompt doesn't request and neighbors don't use. Extra ceremony adds maintenance noise.
- **Complete, not placeholder.** No `TODO`, stub returns, or "wire this later" notes. A file that compiles but doesn't work is worse than no file.
- **Bug fixes: minimal diff.** Change only the broken code path. Mixing refactors with fixes makes verification harder and raises regression risk.
- **Ambiguity -> simplest path.** When the prompt is vague, pick the implementation with the fewest moving parts. State the assumption in the handoff.

## Standards

Load only what the task needs via `read_skill_file("unity-standards", "references/<path>")`:

| When you need | Load |
|---|---|
| Workflow routing, scope checks | `code-standards/single-file-runtime-workflow.md` |
| Type templates (MB, SO, interface) | `code-standards/code-patterns.md` |
| Naming and casing | `code-standards/naming.md` |
| Serialization patterns | `code-standards/serialization.md` |
| Null safety and guards | `code-standards/null-safety.md` |
| Unity lifecycle order | `code-standards/lifecycle.md` |
| Events and callbacks | `code-standards/events.md` |
