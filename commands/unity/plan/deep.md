---
description: Create an implementation plan document
agent: prometheus
subtask: true
---
Use skill unity-plan-deep to create the plan document for $ARGUMENTS (ulb ulw)

# Workflow (Sequential)

## 1) Read Context Documents (MANDATORY FIRST STEP)

- Read each user-provided System/TDD document path before codebase investigation.
- Extract: architecture decisions, data structures, integration points, constraints.
- If docs conflict, record in Open Questions; favor newest source.

## 2) Scope

- Combine user request + extracted context.
- Define: in-scope, out-of-scope, assumptions, prerequisites, acceptance.

## 3) Investigate

 Run `../../unity-shared/scripts/plan/investigate_feature.py "<feature-term>"` to discover current state.
- Use `read`, `glob`, `grep`, LSP tools to validate what exists, what's missing, integration points.
- Never guess without repository evidence.

## 4) Plan

- Break into epics → tasks. ONE table per epic (8 columns: #, Name, Type, Desc, Goal, Code Changes, Acceptance, Cost).
- Code Changes: `📎 patches/TASK-{#}.patch`. Acceptance: `✅ {observable result}`. Cost: XS/S/M/L/XL.
- Keep tasks atomic. Add dependencies and critical path.

## 5) Generate

**Keep the plan document SHORT.** Focus on: request summary, architecture impact, task list.

- Create `Documents/Plans/PLAN_{FeatureName}.md` + `patches/` directory.
- Follow template from `assets/templates/PLAN_DOCUMENT_TEMPLATE_SECTION1.md` and `SECTION2.md`.
- Generate one `.patch` per task in unified diff format.
- Trim unnecessary sections. No verbose prose — tables and bullets only.

## 6) Register Tasks in Task System

- Create parent → epic → sub-task hierarchy via `task_create`.
- Set `blockedBy` from dependency graph. Assign `wave` metadata.
- Include metadata: `wave`, `type`, `cost`, `costHours`, `patchFile`, `planTaskNumber`, `skillSource`.
- See [task-system-integration.md](task-system-integration.md) for exact call patterns.
- Output Task Registration Summary after creation.

## 7) Validate

- All task rows have 8 columns populated.
- Code Changes refs existing `.patch` files in unified diff format.
- Acceptance criteria are short, outcome-focused.
- All tasks registered via `task_create` with full metadata.
- `blockedBy` arrays match dependency graph.
