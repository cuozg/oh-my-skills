# Workflow (Sequential)

## 1) Read Context Documents (MANDATORY FIRST STEP)

- Read each user-provided System/TDD document path before any codebase investigation.
- Extract and keep a working list of:
  - architecture decisions
  - data structures and contracts
  - integration points
  - technical and product constraints
- If multiple docs conflict, record conflict explicitly in Open Questions and favor newest/explicitly authoritative source.

## 2) Scope

- Combine user request + extracted document context.
- Define:
  - in-scope outcomes
  - out-of-scope boundaries
  - assumptions and prerequisites
  - acceptance definition at plan level

## 3) Investigate

- Run `scripts/investigate_feature.sh "<feature-term>"` to discover current state.
- Use `read`, `glob`, `grep`, and LSP tools to validate:
  - what already exists
  - what is missing
  - where integration must occur
  - current test and config coverage
- Do not guess implementation details without repository evidence.

## 4) Plan

- Break work into epics, then tasks.
- For each epic, create ONE all-in-one table with columns: #, Task Name, Type, Description, Goal, Code Changes, Acceptance Criteria, Costing.
- All task data lives in the table row — no separate per-task detail sections.
- Use `<br>` within Acceptance Criteria cells for multiple items.
- Code Changes column: reference the patch file — `📎 patches/TASK-{#}.patch`.
- Generate each `.patch` file in `Documents/Plans/patches/` with unified diff format.
- Acceptance Criteria: short, outcome-focused. `✅ {observable result}`. No implementation steps.
- Keep tasks atomic and execution-ready.
- Add explicit dependencies and identify critical path.

## 5) Generate

- Create `Documents/Plans/PLAN_{FeatureName}.md`.
- Create `Documents/Plans/patches/` directory.
- Copy template structure from `assets/templates/PLAN_DOCUMENT_TEMPLATE.md` exactly.
- Fill all placeholders; leave no required section empty.
- Generate one `.patch` file per task: `Documents/Plans/patches/TASK-{#}.patch` (e.g., `TASK-1.1.patch`).

## 6) Validate

- Validate every task row has all 8 columns populated (#, Name, Type, Desc, Goal, Code Changes, Acceptance, Cost).
- Validate Code Changes column references a `.patch` file that exists in `Documents/Plans/patches/`.
- Validate each `.patch` file uses unified diff format with proper `---`/`+++` headers.
- Validate Acceptance Criteria are short, outcome-focused (no implementation details).
- Validate costing uses only XS/S/M/L/XL with matching hour ranges.
- Validate Source Documents section lists all read document paths.
