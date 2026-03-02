---
name: unity-document-tdd
description: Write a Technical Design Document — architecture decisions, implementation strategy, dependency analysis. Triggers — 'write TDD', 'technical design document', 'design doc', 'architecture decision'.
---
# unity-document-tdd

Produce an evidence-based Technical Design Document grounded in the actual codebase.

## When to Use

- Planning a new system that needs architecture sign-off
- Documenting a key architecture decision after implementation
- Cross-team alignment before a major feature starts
- Recording trade-offs for future maintainers

## Workflow

1. **Investigate** — Read existing related systems; understand current patterns
2. **Define** — State the problem, goals, and non-goals precisely
3. **Design** — Propose architecture; define components, interfaces, and data flow
4. **Alternatives** — Document at least 2 rejected alternatives with rationale
5. **Dependencies** — Map all affected systems with file:line evidence
6. **Risks** — List risks with mitigation strategies
7. **Write** — Fill `references/tdd-template.md` with all findings
8. **Save** — Write to `Documents/TDDs/TDD_{Name}.md`

## Rules

- Investigate the actual codebase before writing — no speculation
- No TODO/TBD in the output document
- Cite `file:line` for every dependency or architectural claim
- Alternatives section is mandatory — never skip it
- Keep language imperative; avoid "we should" or "you could"

## Output Format

Save to `Documents/TDDs/TDD_{Name}.md`.
Sections: Problem, Goals, Non-Goals, Design, Alternatives, Dependencies, Risks, Open Questions.

## Reference Files

- `references/tdd-template.md` — Markdown template with all required TDD sections

Load references on demand via `read_skill_file("unity-document-tdd", "references/tdd-template.md")`.

## Standards

Load `unity-standards` for architecture and design context. Key references:

- `code-standards/architecture-patterns.md` — state machine, MVC/MVP, command pattern
- `code-standards/dependencies.md` — DI, service locator, constructor injection
- `code-standards/events.md` — C# events, UnityEvent, SO channels, Action
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries

Load via `read_skill_file("unity-standards", "references/<path>")`.
