---
name: unity-plan-detail
description: Detailed HTML plan with per-task patch files for XL Unity features. No auto task_create. Triggers — 'detailed plan', 'XL plan', 'full plan with patches', 'generate plan HTML'.
---
# unity-plan-detail

Generate a full HTML plan package with patch files for very large features requiring manual task registration.

## When to Use

- Feature is XL (10+ days) or a major refactor
- Team needs to review the plan before registering any tasks
- Per-file patch previews required for sign-off

## Workflow

1. **Read** — Load all affected modules; build a full file inventory
2. **Scope** — Define phases, milestones, and explicit out-of-scope boundaries
3. **Investigate** — Trace every cross-system dependency; record file:line evidence
4. **Plan** — Decompose into phases → tasks → subtasks with size/risk per node
5. **Patches** — Generate one `.patch` file per changed file (unified diff format)
6. **Overview HTML** — Write `overview.html`: summary, phases, risk table
7. **Tasks HTML** — Write `tasks.html`: full task tree with metadata
8. **Patches HTML** — Write `patch.html`: rendered diff viewer per file
9. **Save** — Write all files to `Documents/Plans/{Name}/`

## Rules

- No JavaScript in any HTML output — pure HTML + inline CSS only
- Never call `task_create` — user decides when to register tasks
- Cite file:line for every risk or dependency listed
- All estimates must be evidence-based; no placeholder ranges

## Output Format

`Documents/Plans/{Name}/` containing `overview.html`, `tasks.html`, `patch.html`, and `*.patch` files.

## Reference Files

- `references/detail-workflow.md` — 10-step workflow with phase definitions
- `references/html-generation-guide.md` — HTML output rules, no-JS constraint, inline CSS patterns

Load references on demand via `read_skill_file("unity-plan-detail", "references/detail-workflow.md")`.

## Standards

Load `unity-standards` for planning and output standards. Key references:

- `plan/sizing-guide.md` — XS/S/M/L/XL definitions, hour ranges
- `plan/risk-assessment.md` — risk levels, mitigation strategies
- `plan/output-detail.md` — HTML plan structure for detail plans
- `quality/html-report-format.md` — report structure, CSS, no JavaScript

Load via `read_skill_file("unity-standards", "references/<path>")`.
