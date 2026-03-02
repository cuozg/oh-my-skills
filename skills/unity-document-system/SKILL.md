---
name: unity-document-system
description: Write system documentation with architecture diagrams, data flows, and usage guides for Unity systems. Triggers — 'document system', 'system documentation', 'write system docs', 'architecture docs'.
---
# unity-document-system

Produce cited, diagram-backed documentation for a Unity system or subsystem.

## When to Use

- A system lacks any written documentation
- Onboarding new contributors to a non-trivial subsystem
- Post-refactor documentation update
- Architecture review preparation

## Workflow

1. **Identify** — Locate all files in the system via `glob` and `lsp_find_references`
2. **Trace** — Follow initialization, runtime, and teardown paths
3. **Map** — Identify public API surface, events emitted/consumed, and dependencies
4. **Diagram** — Draw Mermaid class diagram and sequence/flow diagram
5. **Write** — Populate template from `references/system-doc-template.md`
6. **Review** — Verify every claim has a cited `file:line`

## Rules

- Cite `file:line` for every factual claim
- Include at least one Mermaid diagram
- Bullets over prose; avoid padding sentences
- Document the public API first, internals second
- No TODO/TBD in the output

## Output Format

Save to `Documents/Systems/{SystemName}.md`.
Sections: Overview, Architecture (Mermaid), Public API, Data Flow, Extension Guide, Dependencies.

## Reference Files

- `references/system-doc-template.md` — Markdown template with all required sections

Load references on demand via `read_skill_file("unity-document-system", "references/system-doc-template.md")`.

## Standards

Load `unity-standards` for architecture and pattern context. Key references:

- `code-standards/architecture-patterns.md` — state machine, MVC/MVP, command pattern
- `code-standards/events.md` — C# events, UnityEvent, SO channels, Action
- `code-standards/dependencies.md` — DI, service locator, constructor injection

Load via `read_skill_file("unity-standards", "references/code-standards/<file>")`.
