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
4. **Generate** — Write `PLAN.md` + `tasks.json`
5. **Save** — Write all files to `Documents/Plans/{Name}/`
6. **Summary** — Report effort, risks, critical path, and output folder

## Rules

- Never call `task_create` — user decides when to register tasks
- Cite `file:line` for every risk, dependency, or architectural claim
- All estimates must be evidence-based from investigation — no guesswork
- Use parallel subagents (`run_in_background=true`) for investigation phase
- Every epic must have 2+ tasks; every task must have cost, type, wave, and dependencies
- **Epics & Tasks section is the primary deliverable** — invest most effort here
- Keep text minimal — trees and tables over prose

## Output

`Documents/Plans/{Name}/` containing:
- `PLAN.md` — architecture, epic/task tree, risks, acceptance criteria
- `tasks.json` — machine-readable task list

## Template

Read `references/output-template.md` before generating. Replace `[PLACEHOLDER]` tokens.

## Standards

Load `unity-standards` for planning methodology:
- `plan/sizing-guide.md` — XS/S/M/L/XL definitions, hour ranges
- `plan/risk-assessment.md` — risk levels, mitigation strategies
- `plan/dependency-mapping.md` — blockedBy, parallel vs sequential
- `plan/task-structure.md` — subject/description format, skill routing

Load via `read_skill_file("unity-standards", "references/<path>")`.
