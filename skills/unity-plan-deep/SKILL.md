---
name: unity-plan-deep
description: "Plan big/complex Unity features. Investigates codebase, produces a SHORT markdown plan document (request, impact, task list) at Documents/Plans/, registers tasks in Task System via task_create. Use when: (1) Planning a complex feature with multiple systems, (2) Need implementation plan with task breakdown, (3) Full work breakdown with cost estimates, (4) Architecture-aware planning with patch generation. Triggers: 'create plan', 'plan feature', 'implementation plan', 'plan this', 'work breakdown', 'plan big task'."
---
# Deep Task Plan

Senior Unity developer (15+ years): practical, architecture-aware, delivery-focused.

## Input

- Feature request to plan
- Optional: System Document and/or TDD Document paths
- Optional: constraints (deadline, platform, tech limits)
- Optional: assessment task ID from `unity-plan-quick` (e.g., `T-abc123`)

## Output

- **Short** plan document at `Documents/Plans/PLAN_{FeatureName}.md` — focus on request, impact, task list
- One `.patch` file per task at `Documents/Plans/patches/TASK-{#}.patch`
- Follow template from `assets/templates/PLAN_DOCUMENT_TEMPLATE_SECTION1.md` and `SECTION2.md`
- Tasks registered in Task System via `task_create` (parent → epics → sub-tasks with dependencies)
- Planning only — no implementation, no Unity project mutation

## Workflow

Execute steps sequentially. See [references/workflow.md](references/workflow.md) for full detail.

1. **Read** context documents (mandatory first step)
2. **Scope** in/out boundaries, assumptions, prerequisites
3. **Investigate** real codebase via `../unity-shared/scripts/plan/investigate_feature.py`, LSP, grep
4. **Plan** epics and tasks with 8-column tables
5. **Generate** SHORT markdown plan + `.patch` files — no verbose prose, tables and bullets only
6. **Register** all tasks in Task System
7. **Validate** document + tasks

## Task Table Format

Each epic has ONE all-in-one table. Every row must include all 8 columns:

| # | Task Name | Type | Description | Goal | Code Changes | Acceptance Criteria | Costing |
|---|-----------|------|-------------|------|--------------|---------------------|---------|

- **#**: `{epic}.{task}` (e.g., 1.1, 1.2, 2.1)
- **Type**: New Feature / Enhancement / Bug Fix / Refactor / Configuration / Testing / Documentation
- **Code Changes**: `📎 patches/TASK-{#}.patch`
- **Acceptance Criteria**: `✅ {observable outcome}`, use `<br>` for multiple
- **Costing**: XS(1-2h), S(2-4h), M(4-8h), L(8-16h), XL(16-32h)

For costing standards and types, see [../unity-shared/references/costing-and-types.md](../unity-shared/references/costing-and-types.md).

## Task System Integration

Register ALL plan elements after generating the document. Create parent → epic → sub-task hierarchy via `task_create`. Set `blockedBy` from dependency graph. Include metadata on every sub-task.

See [../unity-shared/references/task-system-integration.md](../unity-shared/references/task-system-integration.md) for exact `task_create` patterns.

## Cross-Skill Pipeline

Middle stage of the Prometheus planning pipeline. If assessment task ID provided, store in `metadata.assessmentTaskId`.
For full pipeline details, see [../unity-shared/references/prometheus-pipeline.md](../unity-shared/references/prometheus-pipeline.md).

## Rules

1. Read attached System/TDD documents before investigation
2. Investigate real codebase state — never hallucinate files or classes
3. Use 8-column task tables — no separate per-task detail sections
4. **Keep plan document SHORT** — request, impact, task list. No verbose prose.
5. Generate one `.patch` per task in unified diff format
6. Register every plan element via `task_create` with full metadata

## Boundaries

- **OWNS**: Investigation, planning, plan document, patches, task registration
- **Does NOT**: Write gameplay code, modify scenes/prefabs, generate HTML, execute tasks
