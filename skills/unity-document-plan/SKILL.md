---
name: unity-document-plan
description: "Creates implementation plans for Unity features. Triggers on 'implementation plan', 'create plan', 'plan feature', 'plan implementation', 'feature plan', 'development plan', 'work breakdown', 'task breakdown'."
---
# Unity Document Plan

Senior Unity developer mindset (15+ years): practical, architecture-aware, and delivery-focused. Prioritize clarity, feasibility, and risk mitigation over rapid coding.

## Input

- Feature request to plan
- One or more attached context documents (System Document and/or TDD Document paths)
- Optional constraints (deadline, platform, tech limits)

## Output

- One markdown plan file at `Documents/Plans/PLAN_{FeatureName}.md`
- One `.patch` file per task at `Documents/Plans/patches/TASK-{#}.patch`
- Plan must follow split template parts `assets/templates/PLAN_DOCUMENT_TEMPLATE_SECTION1.md` and `assets/templates/PLAN_DOCUMENT_TEMPLATE_SECTION2.md` exactly
- Planning only; no implementation, no Unity project mutation

## Non-Negotiable Rules

1. **Always read attached System/TDD documents** before investigation. Your plan must align with existing architecture decisions.
2. **Always investigate real codebase state** before planning tasks. Do not hallucinate files or classes.
3. **Every task must include all 8 columns in a single table row**:
   1. **#** — epic.task number (e.g., 1.1, 1.2, 2.1)
   2. **Task Name** — clear, descriptive name
   3. **Type** — New Feature / Enhancement / Bug Fix / Refactor / Configuration / Testing / Documentation
   4. **Description** — detailed description of what the task involves
   5. **Goal** — what this task achieves when complete
   6. **Code Changes** — `.patch` file reference. Format: `📎 patches/TASK-{#}.patch`. Generate one `.patch` file per task in `Documents/Plans/patches/` using unified diff format.
   7. **Acceptance Criteria** — short, testable conditions. One line each with `✅`. Focus on observable outcomes, not implementation steps.
   8. **Costing** — XS(1-2h), S(2-4h), M(4-8h), L(8-16h), XL(16-32h)
4. **Each epic has ONE all-in-one table** (columns: #, Task Name, Type, Description, Goal, Code Changes, Acceptance Criteria, Costing). No separate per-task detail sections — everything lives in the table row.
5. **ALWAYS use the exact template structure** from `assets/templates/PLAN_DOCUMENT_TEMPLATE_SECTION1.md` and `assets/templates/PLAN_DOCUMENT_TEMPLATE_SECTION2.md`.
6. **Produce markdown only** (`<br>` within table cells is acceptable for multi-value Acceptance Criteria fields, no other HTML).
7. **Generate one `.patch` file per task** in `Documents/Plans/patches/` using unified diff format. Each patch must be self-contained and applicable via `git apply`.

For detailed costing standards, task types, and quality checklist, see [references/costing-and-types.md](references/costing-and-types.md).

For sequential workflow steps (Read, Scope, Investigate, Plan, Generate, Validate), see [references/workflow.md](references/workflow.md).

## Boundaries

- Owns: investigation for planning, plan decomposition, cost estimation, risk framing, per-task `.patch` generation
- Does not: write Unity gameplay code, modify scenes/prefabs/assets, generate HTML deliverables

## Quick Runbook

1. Read provided System/TDD docs.
2. Extract decisions/constraints.
3. Investigate codebase with helper script + tools.
4. Decompose into epics/tasks (all-in-one table per epic, 8 columns).
5. Generate per-task `.patch` files in `Documents/Plans/patches/`.
6. Fill mandatory markdown template exactly.
7. Validate completeness, patch format, and costing consistency.
