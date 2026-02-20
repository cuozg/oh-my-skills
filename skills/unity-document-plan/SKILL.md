---
name: unity-document-plan
description: "Creates implementation plans for Unity features. Triggers on 'implementation plan', 'create plan', 'plan feature', 'plan implementation', 'feature plan', 'development plan', 'work breakdown', 'task breakdown'."
---
# Unity Document Plan

Senior Unity developer mindset (15+ years): practical, architecture-aware, and delivery-focused. You prioritize clarity, feasibility, and risk mitigation over rapid coding.

## Input

- Feature request to plan
- One or more attached context documents (System Document and/or TDD Document paths)
- Optional constraints (deadline, platform, tech limits)

## Output

- One markdown plan file at `Documents/Plans/PLAN_{FeatureName}.md`
- One `.patch` file per task at `Documents/Plans/patches/TASK-{#}.patch`
- Plan must follow `assets/templates/PLAN_DOCUMENT_TEMPLATE.md` exactly
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
5. **ALWAYS use the exact template structure** from `assets/templates/PLAN_DOCUMENT_TEMPLATE.md`.
6. **Produce markdown only** (`<br>` within table cells is acceptable for multi-value Acceptance Criteria fields, no other HTML).
7. **Generate one `.patch` file per task** in `Documents/Plans/patches/` using unified diff format. Each patch must be self-contained and applicable via `git apply`.

## Costing Standard

- **XS**: 1-2h (Trivial change)
- **S**: 2-4h (Small task)
- **M**: 4-8h (Standard task)
- **L**: 8-16h (Large complex task)
- **XL**: 16-32h (Major subsystem work - consider breaking down)

## Task Types

- New Feature
- Enhancement
- Bug Fix
- Refactor
- Configuration
- Testing
- Documentation

## Workflow (Sequential)

### 1) Read Context Documents (MANDATORY FIRST STEP)

- Read each user-provided System/TDD document path before any codebase investigation.
- Extract and keep a working list of:
  - architecture decisions
  - data structures and contracts
  - integration points
  - technical and product constraints
- If multiple docs conflict, record conflict explicitly in Open Questions and favor newest/explicitly authoritative source.

### 2) Scope

- Combine user request + extracted document context.
- Define:
  - in-scope outcomes
  - out-of-scope boundaries
  - assumptions and prerequisites
  - acceptance definition at plan level

### 3) Investigate

- Run `scripts/investigate_feature.sh "<feature-term>"` to discover current state.
- Use `read`, `glob`, `grep`, and LSP tools to validate:
  - what already exists
  - what is missing
  - where integration must occur
  - current test and config coverage
- Do not guess implementation details without repository evidence.

### 4) Plan

- Break work into epics, then tasks.
- For each epic, create ONE all-in-one table with columns: #, Task Name, Type, Description, Goal, Code Changes, Acceptance Criteria, Costing.
- All task data lives in the table row — no separate per-task detail sections.
- Use `<br>` within Acceptance Criteria cells for multiple items.
- Code Changes column: reference the patch file — `📎 patches/TASK-{#}.patch`.
- Generate each `.patch` file in `Documents/Plans/patches/` with unified diff format:
  ```
  --- a/Assets/Scripts/Foo.cs
  +++ b/Assets/Scripts/Foo.cs
  @@ -lineNum,count +lineNum,count @@
   context line
  +added line
  -removed line
  ```

  - For new files use `/dev/null` as the `a/` path.
  - Each patch must apply cleanly via `git apply`.
- Acceptance Criteria: short, outcome-focused. `✅ {observable result}`. No implementation steps.
- Keep tasks atomic and execution-ready.
- Add explicit dependencies and identify critical path.

### 5) Generate

- Create `Documents/Plans/PLAN_{FeatureName}.md`.
- Create `Documents/Plans/patches/` directory.
- Copy template structure from `assets/templates/PLAN_DOCUMENT_TEMPLATE.md` exactly.
- Fill all placeholders; leave no required section empty.
- Generate one `.patch` file per task: `Documents/Plans/patches/TASK-{#}.patch` (e.g., `TASK-1.1.patch`).

### 6) Validate

- Validate every task row has all 8 columns populated (#, Name, Type, Desc, Goal, Code Changes, Acceptance, Cost).
- Validate Code Changes column references a `.patch` file that exists in `Documents/Plans/patches/`.
- Validate each `.patch` file uses unified diff format with proper `---`/`+++` headers.
- Validate Acceptance Criteria are short, outcome-focused (no implementation details).
- Validate costing uses only XS/S/M/L/XL with matching hour ranges.
- Validate Source Documents section lists all read document paths.

## Quality Checklist

- [ ] Context documents read before investigation
- [ ] Architecture decisions from docs reflected in plan
- [ ] Existing vs new work explicitly identified
- [ ] Every epic has ONE all-in-one table (8 columns: #, Name, Type, Desc, Goal, Code Changes, Acceptance, Cost)
- [ ] No separate per-task detail sections — everything inline in table rows
- [ ] Code Changes column links to `.patch` file in `Documents/Plans/patches/`
- [ ] Each `.patch` file uses unified diff format and applies via `git apply`
- [ ] Acceptance Criteria are short and outcome-focused (no implementation steps)
- [ ] Dependency graph and execution order included
- [ ] Cost summary consistent with per-task estimates
- [ ] Output file path is `Documents/Plans/PLAN_{FeatureName}.md`
- [ ] Template structure matches `assets/templates/PLAN_DOCUMENT_TEMPLATE.md` exactly

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
