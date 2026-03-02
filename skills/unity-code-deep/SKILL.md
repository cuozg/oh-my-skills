---
name: unity-code-deep
description: Implement multi-file Unity C# features — cross-system architecture, refactors, patterns spanning 2+ files. Use when a task touches multiple classes, introduces new systems, or restructures existing code. Triggers — 'build a system', 'implement feature', 'refactor', 'multi-file', 'architecture', 'cross-system', 'add a system'.
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
6. **Verify** — Run `coplay-mcp_check_compile_errors`. Fix until zero errors across all new/modified files.

## Rules

- Map all affected files BEFORE writing any code. No ad-hoc file creation mid-implementation.
- Write interfaces and base types first, implementations second, wiring/registration last.
- One class per file. File name = class name. Match existing namespace conventions.
- Respect assembly definition boundaries — never add cross-asmdef references without checking.
- All rules from `unity-code-quick` apply per-file (SerializeField, sealed, no empty lifecycle, etc.).
- Load `unity-code-quick` references for per-file coding standards: `read_skill_file("unity-code-quick", "references/<file>")`.
- Prefer composition over inheritance. Extract interfaces for testability.
- Use ScriptableObject event channels for cross-system communication (avoid direct coupling).
- Never introduce a new dependency pattern that conflicts with existing project conventions.
- If refactoring, preserve public API signatures unless explicitly asked to change them.
- Run `coplay-mcp_check_compile_errors` after every 2-3 files written, not just at the end.
- Never add `// TODO` — deliver complete code or state limitations.

## Output Format

Write all files directly using edit/write tools. No markdown code blocks as final output — actual files only.
Report: file count, file list with paths, and compilation status.

## Reference Files

- `references/architecture-patterns.md` — Multi-file Unity patterns (service locator, event bus, state machine, MVC)
- `references/multi-file-workflow.md` — Dependency ordering, namespace strategy, asmdef awareness
- `references/refactoring-patterns.md` — Safe refactoring: extract class, introduce interface, decompose, migrate

Load references on demand via `read_skill_file("unity-code-deep", "references/<file>")` when pattern guidance is needed.
For per-file coding standards, load from `unity-code-quick`: `read_skill_file("unity-code-quick", "references/<file>")`.
