---
name: unity-plan-deep
description: >
  Use this skill to create a concise plan document and task hierarchy for medium-to-large Unity features
  (M: 1-3 days, L: 3-10 days) spanning 2+ systems or files. Use when the user says "plan this feature,"
  "I need a feature plan," "break this down into tasks," or describes a feature with dependencies between
  implementation steps. Outputs a short markdown plan with a registered task tree. For smaller tasks, use
  unity-plan-quick (XS/S). For very large features (10+ days), use unity-plan-costing.
metadata:
  author: kuozg
  version: "1.0"
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
5. **Write** — Save plan to `Documents/Plans/PLAN_{Name}.md` using the output template
6. **Create tasks** — Call `task_create` for parent then children; wire `blockedBy`
7. **Validate** — Confirm all blockers reference real task IDs

## Rules

- **MANDATORY**: Output MUST follow the template in `references/output-template.md` — no deviation
- Keep the plan document SHORT: request, scope, impact, risks, ordered task list — no padding
- Set `blockedBy` accurately to enable maximum parallel execution
- Investigate before estimating — no guesswork
- One `task_create` per parallelizable unit of work
- Every claim in Impact/Risks must cite a real file path

## Output

Read `references/output-template.md` before writing. Save to `Documents/Plans/PLAN_{Name}.md`.
Print task IDs and subjects to chat after creation.

## Standards

Load `unity-standards` for planning methodology. Key references:

- `plan/sizing-guide.md` — XS/S/M/L/XL definitions, hour ranges
- `plan/risk-assessment.md` — risk levels, mitigation strategies
- `plan/dependency-mapping.md` — blockedBy, parallel vs sequential
- `plan/task-structure.md` — subject/description format, skill routing

Load via `read_skill_file("unity-standards", "references/plan/<file>")`.
