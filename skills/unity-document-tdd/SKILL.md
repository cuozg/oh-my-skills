---
name: unity-document-tdd
description: >
  Use this skill to write a Technical Design Document (TDD) — architecture decisions, implementation
  strategy, dependency analysis, and risk assessment. Use when the user is planning a new system, needs
  architecture sign-off, or says "write a design doc," "TDD for this feature," "document the architecture
  decision," or "what's the implementation strategy." Investigates the actual codebase first. Do not use
  for documenting existing systems — use unity-document-system for that.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-document-tdd

Produce an evidence-based Technical Design Document grounded in the actual codebase.

## When to Use

- Planning a new system that needs architecture sign-off
- Documenting a key architecture decision after implementation
- Cross-team alignment before a major feature starts
- Recording trade-offs for future maintainers

## Workflow

1. **Load template** — `read_skill_file("unity-document-tdd", "references/tdd-template.md")`; use it as the exact output skeleton
2. **Investigate** — Read existing related systems; understand current patterns
3. **Define** — State the problem, goals, and non-goals precisely
4. **Design** — Propose architecture; define components, interfaces, and data flow
5. **Alternatives** — Document at least 2 rejected alternatives with rationale
6. **Dependencies** — Map all affected systems with file:line evidence
7. **Risks** — List risks with mitigation strategies
8. **Write** — Fill every section of the template; no placeholder text allowed
9. **Save** — Write to `Documents/TDDs/TDD_{Name}.md`

## Rules

- **Template is mandatory** — output must follow `references/tdd-template.md` exactly: same headers, same table schemas, same Mermaid block in Data Flow
- Investigate the actual codebase before writing — no speculation
- No TODO/TBD in the output document; resolve all placeholders
- Cite `file:line` for every dependency or architectural claim
- Alternatives section is mandatory — never skip it
- Keep language imperative; avoid "we should" or "you could"
- All 8 template sections must appear in the final document

## Output Format

Save to `Documents/TDDs/TDD_{Name}.md`.

Required sections (from template — all mandatory):
`Problem` · `Goals` · `Non-Goals` · `Design` (Components table + Interfaces + Data Flow mermaid) · `Alternatives Considered` (table) · `Dependencies` (table) · `Risks` (table) · `Open Questions`

## Reference Files

- `references/tdd-template.md` — Mandatory output template; load at step 1

Load via `read_skill_file("unity-document-tdd", "references/tdd-template.md")`.

## Standards

Load `unity-standards` for architecture and design context. Key references:

- `code-standards/architecture-patterns.md` — state machine, MVC/MVP, command pattern
- `code-standards/dependencies.md` — DI, service locator, constructor injection
- `code-standards/events.md` — C# events, UnityEvent, SO channels, Action
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries

Load via `read_skill_file("unity-standards", "references/<path>")`.
