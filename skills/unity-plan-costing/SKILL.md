---
name: unity-plan-costing
description: Detailed Markdown plan with deep investigation and full epic/task tree for XL Unity features. Parallel subagent execution for investigation. No auto task_create. Triggers — 'detailed plan', 'XL plan', 'full breakdown', 'costing plan'.
---
# unity-plan-costing

Produce a comprehensive Markdown plan for very large features — deep codebase investigation,
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
3. **Plan** — Decompose into epics → tasks with cost/type/wave per node using tree format
4. **Generate** — Write `PLAN.md`
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

## Output

`Documents/Plans/{Name}/` containing:
- `PLAN.md` — summary, architecture, tasks breakdown, risks, compatibility, acceptance

### PLAN.md Sections (9)

1. **Summary** — 1-5 bullet points (what, why, scope)
2. **Architecture Overview** — current vs proposed, what changes
3. **Technical Approach** — high-level steps to achieve the goal
4. **Epics** — table: name + 1-line purpose
5. **Tasks Breakdown** — table: ID, Epic, Title, Description (1 bullet per action), Type, Cost, Files
6. **Risks** — severity table with impact and mitigation
7. **Backward Compatibility** — breaking changes and migration steps
8. **Acceptance Criteria** — checkbox list

## Template

Read `references/output-template.md` before generating. Replace `[PLACEHOLDER]` tokens.

## Standards

Load `unity-standards` for planning methodology:
- `plan/sizing-guide.md` — XS/S/M/L/XL definitions, hour ranges
- `plan/risk-assessment.md` — risk levels, mitigation strategies
- `plan/dependency-mapping.md` — blockedBy, parallel vs sequential
- `plan/task-structure.md` — subject/description format, skill routing

Load via `read_skill_file("unity-standards", "references/<path>")`.
