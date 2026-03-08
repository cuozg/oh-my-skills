---
name: unity-code-deep
description: Implement multi-file Unity C# features — cross-system architecture, refactors, patterns spanning 2+ files. Use when a task touches multiple classes, introduces new systems, or restructures existing code. Triggers — 'build a system', 'implement feature', 'refactor', 'multi-file', 'architecture', 'cross-system', 'add a system'.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-code-deep

Multi-file C# implementation for Unity. Understand scope → plan file structure → implement → verify compilation.

## When to Use

- Feature spanning 2+ .cs files (e.g., manager + data + UI + events)
- Introducing architectural patterns (state machine, event bus, service locator)
- Refactoring: extract class, introduce interface, decompose god class
- Cross-system integration (new system wiring into existing ones)
- Any task where file dependencies and creation order matter

## Workflow

1. **Parse** — Extract: what system? which files affected? what patterns needed?
2. **Scope** — Map affected files, namespaces, assemblies. Identify creation order and dependencies.
3. **Discover** — Check codebase for existing patterns, conventions, related systems (grep/glob/lsp, max 5 searches)
4. **Plan** — Define file list with responsibilities. Interfaces first, then implementations, then wiring.
5. **Implement** — Write files in dependency order. Match project conventions per file.

## Rules

- Map all affected files BEFORE writing any code. No ad-hoc file creation mid-implementation.
- Write interfaces and base types first, implementations second, wiring/registration last.
- One class per file. File name = class name.
- Respect assembly definition boundaries — never add cross-asmdef references without checking.
- If refactoring, preserve public API signatures unless explicitly asked to change them.
- Never add `// TODO` — deliver complete code or state limitations.
- For all per-file coding standards — follow `unity-standards`.

## Output Format

Write all files directly using edit/write tools. No markdown code blocks as final output — actual files only.
Report: file count, file list with paths, and compilation status.

## Standards

Load `unity-standards` for all coding conventions and patterns. Key references:

- `code-standards/architecture-patterns.md` — state machine, MVC/MVP, command pattern
- `code-standards/multi-file-workflow.md` — dependency ordering, namespace strategy, asmdef awareness
- `code-standards/refactoring-patterns.md` — extract class, introduce interface, decompose, migrate
- `code-standards/code-patterns.md` — MonoBehaviour, SO, interface templates
- `code-standards/dependencies.md` — DI, service locator, constructor injection
- `code-standards/events.md` — C# events, UnityEvent, SO channels

Load via `read_skill_file("unity-standards", "references/code-standards/<file>")`.
