---
name: unity-code-quick
description: Write single-file Unity C# fast — MonoBehaviours, ScriptableObjects, interfaces, data models, utility functions. Use for any small coding task that fits one file. Triggers — 'write a script', 'create a component', 'add a function', 'make a SO', 'quick script', 'single file', 'boilerplate'.
metadata:
  author: kuozg
  version: "1.0"
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

## Rules

- Match existing project conventions first. If none found, follow `unity-standards`.
- Always include `using` directives — never assume implicit usings.
- Never add `// TODO` — deliver complete code or state limitations.
- Inline XML docs `/// <summary>` on public API only. No noise comments.
- For all coding standards (naming, access modifiers, serialization, lifecycle, formatting) — follow `unity-standards`.

## Output Format

Write the file directly using edit/write tools. No markdown code blocks as final output — actual files only.

## Standards

Load `unity-standards` for all coding conventions. Key references:

- `code-standards/code-patterns.md` — MonoBehaviour, SO data, interface, UnityEvent templates
- `code-standards/naming.md`, `formatting.md`, `serialization.md` — per-file conventions
- `code-standards/lifecycle.md`, `null-safety.md`, `events.md` — Unity-specific patterns

Load via `read_skill_file("unity-standards", "references/code-standards/<file>")`.
