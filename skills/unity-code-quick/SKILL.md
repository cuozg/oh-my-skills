---
name: unity-code-quick
description: Write single-file Unity C# fast — MonoBehaviours, ScriptableObjects, interfaces, data models, utility functions. Use for any small coding task that fits one file. Triggers — 'write a script', 'create a component', 'add a function', 'make a SO', 'quick script', 'single file', 'boilerplate'.
---

# unity-code-quick

Fast single-file C# delivery for Unity. Receive request → match project conventions → write code → done.

## When to Use

- Single MonoBehaviour, ScriptableObject, interface, enum, struct, or static utility
- Adding/modifying a single function or method
- Boilerplate generation (data models, event channels, simple managers)
- Any coding task completable in one .cs file

## Workflow

1. **Parse** — Extract: what type? what behavior? any constraints?
2. **Discover** — Check existing codebase for naming, namespace, folder conventions (grep/glob, max 2 searches)
3. **Write** — Produce the .cs file matching project style
4. **Verify** — Run `coplay-mcp_check_compile_errors` to confirm zero errors

## Rules

- Match existing project conventions (namespaces, folders, naming). If none found, use PascalCase + company namespace.
- Always include `using` directives — never assume implicit usings.
- Prefer `[SerializeField] private` over `public` fields.
- Use `#region` only if file exceeds 80 lines.
- Add `[Header("Section")]` to group inspector fields (3+ fields).
- Add `[Tooltip("...")]` when field purpose isn't obvious from name.
- No empty Unity lifecycle methods (remove unused `Start`/`Update`).
- Mark classes `sealed` unless inheritance is explicitly needed.
- Use `TryGetComponent` over `GetComponent` where null is possible.
- Return early to reduce nesting.
- Never add `// TODO` — deliver complete code or state limitations.
- Inline XML docs `/// <summary>` on public API only. No noise comments.

## Output Format

Write the file directly using edit/write tools. No markdown code blocks as final output — actual files only.

## Reference Files

- `references/code-patterns.md` — Common Unity C# patterns (MonoBehaviour, SO, events)
- `references/naming-conventions.md` — Unity C# naming and folder standards
- `references/csharp-tips.md` — Performance and safety micro-patterns

Load references on demand via `read_skill_file("unity-code-quick", "references/<file>")` when pattern guidance is needed.
