---
name: unity-document
description: >
  Unified Unity documentation skill — write system documentation or technical design documents from
  real codebase state. Auto-triages: System (existing system → architecture diagrams, API reference,
  extension guides with mandatory 8-section template and validation) or TDD (pre-implementation →
  architecture decisions, alternatives analysis, risk assessment). Use when the user says "document
  this system," "write docs for X," "architecture documentation," "write a design doc," "TDD for
  this feature," "document the architecture decision," "what's the implementation strategy," or wants
  any form of technical documentation for a Unity codebase module. Covers both documenting what exists
  and planning what will be built.
metadata:
  author: kuozg
  version: "2.0"
---

# unity-document

Write evidence-based technical documentation grounded in the actual codebase. Auto-triage into the right mode.

## Triage

Classify the request before starting:

| Signal | Mode |
|--------|------|
| "document this system," "write docs for X," "architecture docs" | **System** |
| Existing system needs a reference document | **System** |
| User wants API reference, data flows, extension guides | **System** |
| "write a design doc," "TDD for this feature," "design document" | **TDD** |
| Planning a new system or major feature | **TDD** |
| Architecture sign-off, trade-off analysis, implementation strategy | **TDD** |

When ambiguous, ask: "Are you documenting an existing system or planning a new one?"

---

## System Mode

Document an existing system with mandatory template enforcement.

### Workflow

1. **Identify** — Locate core entry points, data models, and managers for the target system
2. **Trace** — Follow data flow from input to output, noting dependencies and events
3. **Map** — Identify the architectural pattern (Event Bus, Singleton, ECS, etc.)
4. **Diagram** — Formulate Mermaid sequence and architecture diagrams from code
5. **Write** — Load template: `read_skill_file("unity-document", "references/system-doc-template.md")`. Follow it exactly — no renaming, reordering, or skipping sections
6. **Validate** — Run: `run_skill_script("unity-document", "scripts/validate_system_doc.py", arguments=[<path>])`

### Output

Save to `Documents/Systems/{SystemName}.md`. All 8 sections mandatory, all claims cited `(file.cs:line)`, at least 2 Mermaid diagrams, owner assigned, review date set (max 90 days).

---

## TDD Mode

Produce a Technical Design Document for a planned system or feature.

### Workflow

1. **Load template** — `read_skill_file("unity-document", "references/tdd-template.md")`; use as exact skeleton
2. **Investigate** — Read existing related systems; understand current patterns and constraints
3. **Define** — State problem, goals, and non-goals precisely
4. **Design** — Propose architecture: components, interfaces, data flow (Mermaid required)
5. **Alternatives** — Document at least 2 rejected alternatives with rationale (mandatory)
6. **Dependencies** — Map all affected systems with `file:line` evidence
7. **Risks** — List risks with likelihood, impact, and mitigation
8. **Write** — Fill every section; no placeholder text
9. **Validate** — Run: `run_skill_script("unity-document", "scripts/validate_tdd.py", arguments=[<path>])`
10. **Save** — Write to `Documents/TDDs/TDD_{Name}.md`

### Output

All 8 template sections mandatory: Problem, Goals, Non-Goals, Design (Components + Interfaces + Data Flow mermaid), Alternatives Considered, Dependencies, Risks, Open Questions.

---

## Shared Rules

- Investigate the actual codebase before writing — no speculation
- Cite `file:line` for every dependency, API reference, and architectural claim
- No TODO/TBD/FIXME in the output document
- Use imperative language; avoid "we should" or "you could"
- Include at least one Mermaid diagram per document

## Standards

Load `unity-standards` for architecture context. Key references:

- `code-standards/architecture-patterns.md` — state machine, MVC/MVP, command pattern
- `code-standards/dependencies.md` — DI, service locator, constructor injection
- `code-standards/events.md` — C# events, UnityEvent, SO channels, Action
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries

Load via `read_skill_file("unity-standards", "references/<path>")`.
