---
name: unity-spec
description: >
  Investigate Unity projects and generate per-feature Game Design Specification docs
  in Docs/Specs/. Supports Full GDD, single Feature Spec, and Update mode that diffs
  existing specs against the codebase. MUST use when the user asks for a game spec,
  GDD, game design document, feature specification, stale spec update, per-feature
  spec split, or structured design documentation for a game concept. Also use to
  document mechanics, systems design, progression, UX/UI flows, or technical constraints.
  Do not use for technical design docs or system docs (unity-document), task planning
  (unity-plan), codebase investigation without spec output, or project scaffolding.
metadata:
  author: kuozg
  version: "2.0"
---

# unity-spec

Investigate Unity projects and produce per-feature Game Design Specifications. Each feature gets its own file in `Docs/Specs/`.

## Triage

| Signal | Mode |
|--------|------|
| New game concept, multiple features | **Full GDD** — index + per-feature files |
| Single feature for an existing game | **Feature Spec** — one `FEATURE_NAME.md` |
| Existing spec outdated after code changes | **Update** — diff codebase vs spec, patch |

When ambiguous, ask: "Full game spec or just one feature?"

## Output Rules (non-negotiable)

- **Directory**: `Docs/Specs/`
- **Feature files**: `Docs/Specs/FEATURE_NAME.md` (e.g., `Combat_System.md`, `Inventory.md`)
- **Index file** (Full GDD only): `Docs/Specs/_INDEX.md`
- **Naming**: PascalCase with underscores for multi-word features
- One feature per file — never combine unrelated features

## Workflow

After triage, load the mode workflow:
`read_skill_file("unity-spec", "references/workflows.md")`

Follow the steps for the selected mode exactly. Every mode shares these gates:

1. **Scan** — check `Docs/Specs/` for existing specs
2. **Investigate** — deep codebase scan before writing (cite `file:line`)
3. **Draft** — fill templates completely, mark gaps `[ASSUMED]`
4. **Review ⛔ BLOCK** — present to user, wait for approval
5. **Save & Validate** — `run_skill_script("unity-spec", "scripts/validate_spec.py", arguments=[<path>])`

### Templates

- **Index**: `read_skill_file("unity-spec", "references/gdd-template.md")`
- **Feature**: `read_skill_file("unity-spec", "references/feature-template.md")`

## Shared Rules

- Investigate actual codebase before writing — no speculation
- Cite `file:line` for every reference to existing code
- Mark assumptions `[ASSUMED]`, updates `[UPDATED: reason]`
- No TODO/TBD/FIXME in output
- Imperative language; no "we should" or "you could"
- Full GDD: at least 3 Mermaid diagrams across all files
- Feature Spec: at least 1 Mermaid diagram
- No C# code stubs — architecture-level descriptions only

## Standards

Load `unity-standards` for architecture context:

- `code-standards/architecture-systems.md` — patterns, dependencies, events
- `plan/investigation-workflow.md` — file tracing, call chains
- `other/mermaid-syntax.md` — diagram syntax
- `other/unity-mcp-routing-matrix.md` — MCP tool routing

Load via `read_skill_file("unity-standards", "references/<path>")`.
