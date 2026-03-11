---
name: unity-code-deep
description: "Use this skill for Unity runtime work that needs multiple C# files or a safe refactor across classes: services, interfaces, ScriptableObject data, event channels, presenters, installer/bootstrap wiring, or breaking a large runtime class into smaller ones. Also use it when the user wants the implementation approach or file plan for that multi-file runtime work. Do not use it for editor tooling, UI Toolkit, tests, or one-file edits."
metadata:
  author: kuozg
  version: "1.2"
---

# unity-code-deep

Deliver multi-file Unity runtime C# changes, or the implementation plan for them, with an explicit file plan, dependency-aware implementation order, and concrete integration handoff.

## When to Use

- Runtime feature spanning 2+ `.cs` files such as manager + data + events + presenter
- New shared abstractions: interfaces, services, event channels, ScriptableObject data, bootstrapping
- Refactors that split responsibilities across multiple runtime files while preserving behavior
- Cross-system integration where file boundaries, asmdefs, or registration order matter
- Requests for the implementation approach, file plan, or safe structure of multi-file runtime work

## Do Not Use

- One-file runtime work or narrow bug fixes → `unity-code-quick`
- Editor tooling, inspectors, drawers, gizmos, menu items → `unity-code-editor`
- UI Toolkit screens, UXML, USS, runtime UI composition → `unity-uitoolkit-create`
- Unit or Play Mode tests → `unity-test-unit`

## Workflow

1. **Qualify** — Confirm the request truly needs multiple runtime files. If it collapses to one file or another domain, switch skills.
2. **Discover** — Read the affected files plus 2-3 nearby runtime files for namespaces, field patterns, asmdefs, registration style, and editor wiring conventions.
3. **Plan** — List every file to modify or create, each file's responsibility, dependency order, and any assets or scene wiring the code relies on.
4. **Implement** — Write shared abstractions first, data/config next, concrete logic after that, and bootstrap or registration last.
5. **Verify** — Run diagnostics on every changed `.cs` file. For larger changes, verify after each dependency tier instead of waiting until the end.
6. **Handoff** — Report exactly what was changed and any Unity Editor follow-up: drag-drop refs, ScriptableObject assets, bootstrap registration, scene or prefab wiring.

## Rules

- Map all affected files before writing code. Do not drift into ad-hoc extra files mid-implementation.
- Match local project patterns first; use `unity-standards` when the repo is silent or inconsistent.
- Write interfaces and base types first, implementations second, wiring or registration last.
- Keep one type per file and match file name to type name.
- Respect asmdef boundaries. Do not add new asmdefs or cross-asmdef references unless the task explicitly requires it.
- Preserve public API and serialized-field behavior during refactors unless the user asked to change them.
- If the design needs ScriptableObject assets, inspector assignments, or installer registration, implement the code and state the required editor steps explicitly.
- Never leave placeholder logic, `TODO`, or partially wired code.

## Output Format

Edit the real files. End with a short report covering changed paths, verification status, and required Unity Editor follow-up.

## Standards

Load `unity-standards` for all coding conventions and patterns. Key references:

- `references/code-standards/multi-file-workflow.md` — routing, dependency ordering, asmdef awareness, handoff checklist
- `references/code-standards/architecture-patterns.md` — state machine, MVP, command, strategy
- `references/code-standards/refactoring-patterns.md` — extract interface, decompose safely, preserve API
- `references/code-standards/dependencies.md` — DI, installers, service locator fallback, asmdef boundaries
- `references/code-standards/events.md` — C# events, UnityEvent, ScriptableObject channels
- `references/code-standards/code-patterns.md` — MonoBehaviour, ScriptableObject, interface templates
- `references/code-standards/naming.md` — namespaces, type names, field ordering

Load only the references the task needs via `read_skill_file("unity-standards", "references/<path>")`.
