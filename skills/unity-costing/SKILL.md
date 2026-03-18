---
name: unity-costing
description: >
  Use this skill to create a detailed HTML plan for XL Unity features (10+ days) or major refactors —
  deep codebase investigation, full epic/task tree with dependencies, architecture analysis, and risk
  assessment. Use when the user says "I need a full breakdown," "detailed plan for this feature,"
  "costing plan," or describes a very large feature that needs thorough analysis before work begins. Does
  not auto-create tasks — the user decides when to register them. For smaller features, use
  unity-plan-deep (M/L) or unity-plan-quick (XS/S).
metadata:
  author: kuozg
  version: "1.0"
---
# unity-costing

Produce a comprehensive HTML plan for very large features — deep codebase investigation,
architecture analysis, full epic/task tree with dependencies, waves, and risk assessment.

## When to Use

- Feature is XL (10+ days) or a major refactor/new system
- Team needs a detailed plan with epics, tasks, dependencies before any work
- Deep cross-system investigation required before scoping

## Workflow

Read `references/workflow.md` for the full step-by-step process with parallel execution strategy.

Summary:
1. **Investigate** — Parallel subagent exploration of affected modules, dependencies, patterns
2. **Scope** — Define phases, epics, boundaries, and out-of-scope items
3. **Plan** — Decompose into epics → tasks with cost/type/wave per node
4. **Generate** — Write `PLAN.html` using the HTML template
5. **Save** — Write to `Documents/Plans/{Name}/`
6. **Summary** — Report effort, risks, critical path, and output folder

## Rules

- Never call `task_create` — user decides when to register tasks
- Cite `file:line` for every risk, dependency, or architectural claim
- All estimates must be evidence-based from investigation — no guesswork
- Use parallel subagents (`run_in_background=true`) for investigation phase
- Every epic must have 2+ tasks; every task must have type, cost, and affected files
- **Tasks Breakdown table is the primary deliverable** — invest most effort here
- Keep text minimal — tables over prose, bullets over paragraphs
- No JavaScript in HTML output — CSS-only, self-contained

## Output

`Documents/Plans/{Name}/` containing:
- `PLAN.html` — Vercel-themed HTML with summary, architecture, tasks, risks, acceptance

### PLAN.html Sections (8)

1. **Summary** — 1-5 bullet points (what, why, scope)
2. **Architecture Overview** — current vs proposed side-by-side, what changes
3. **Technical Approach** — numbered steps with code references
4. **Epics** — table: name + 1-line purpose
5. **Tasks Breakdown** — table: ID, Epic, Title, Description, Type (badge), Cost (badge), Files
6. **Risks** — table: risk, severity badge (HIGH/MED/LOW), impact, mitigation
7. **Backward Compatibility** — table: area, impact, migration steps
8. **Acceptance Criteria** — styled checkbox list by category

## Template

Read `references/output-template.html` before generating. Replace `[PLACEHOLDER]` tokens.
Use badge CSS classes for types (`badge-logic`, `badge-ui`, etc.) and costs (`badge-cost-s`, etc.).

## Standards

Load `unity-standards` for planning methodology:
- `plan/sizing-guide.md` — XS/S/M/L/XL definitions, hour ranges
- `plan/risk-assessment.md` — risk levels, mitigation strategies
- `plan/dependency-mapping.md` — blockedBy, parallel vs sequential
- `plan/task-structure.md` — subject/description format, skill routing

Load via `read_skill_file("unity-standards", "references/<path>")`.
