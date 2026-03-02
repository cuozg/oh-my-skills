---
name: unity-plan-deep
description: SHORT plan document and task hierarchy for M/L Unity features. Triggers — 'plan feature', 'deep plan', 'feature plan', 'complex plan', 'plan this feature'.
---
# unity-plan-deep

Produce a concise plan document and register a full task hierarchy for a medium-to-large feature.

## When to Use

- Feature spans 2+ systems or files (M: 1-3 days, L: 3-10 days)
- Dependencies between tasks require explicit ordering
- Team needs a brief written record before implementation starts

## Workflow

1. **Read** — Scan entry points and relevant modules with `glob`, `lsp_goto_definition`
2. **Scope** — Define what is in/out of scope; list affected files
3. **Investigate** — Trace key dependencies; flag integration risks
4. **Plan** — Break into ordered tasks; assign sizes and skills
5. **Write** — Save SHORT plan to `Documents/Plans/PLAN_{Name}.md`
6. **Create tasks** — Call `task_create` for parent then children; wire `blockedBy`
7. **Validate** — Confirm all blockers reference real task IDs

## Rules

- Keep the plan document SHORT: request, impact, ordered task list only — no padding
- Set `blockedBy` accurately to enable maximum parallel execution
- Investigate before estimating — no guesswork
- One `task_create` per parallelizable unit of work

## Output Format

`Documents/Plans/PLAN_{Name}.md` (request, impact, task list) + task hierarchy in task system.
Print task IDs and subjects to chat after creation.

## Reference Files

- `references/plan-workflow.md` — Planning methodology and scoping checklist
- `references/task-system-integration.md` — task_create usage patterns and blockedBy wiring

Load references on demand via `read_skill_file("unity-plan-deep", "references/plan-workflow.md")`.
