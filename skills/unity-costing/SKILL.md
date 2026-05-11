---
name: unity-costing
description: >
  Create detailed Unity feature or task costing plans as self-contained HTML reports. MUST use when the user asks for
  feature costing, task breakdown, estimate, effort sizing, implementation plan with hours/days, epic/task decomposition,
  technical approach, architecture overview, risk assessment, acceptance criteria, compatibility impact, or a detailed
  Unity delivery plan before implementation. Use for small-to-XL Unity work when a costed task tree is the deliverable;
  investigate the codebase first and fire subagents when scope touches multiple systems or evidence is needed.
metadata:
  author: kuozg
  version: "2.1"
---
# unity-costing

Produce a self-contained HTML costing report for a Unity feature/refactor. Output: `Docs/Plans/{Name}/PLAN.html`. Answer "what will this cost?" — not "please implement this."

**Pre-requisite:** Read `references/output-template.html`. Replace all `[PLACEHOLDER]` tokens exactly. Use predefined CSS badge classes. Do not invent new classes. Maintain Vercel dark theme (black background, #111 cards, no JS).

## Workflow

### 1. Clarify Blocking Ambiguity
Ask only if: target platform unknown, boundaries unclear, quality bar ambiguous, unknown SDKs, or estimate unit unclear. Otherwise, state assumptions in the report.

### 2. Parallel Deep Investigation
- Fire 3-5 `explore` subagents simultaneously (never sequentially) covering different angles:
  1. Entry points, public APIs, module boundaries
  2. Cross-system dependencies (calls, shared state, events)
  3. Existing patterns (DI, lifecycle hooks, Addressables)
  4. Test coverage and infrastructure
  5. Performance-critical paths, platform risks, allocations
- Fire 1 `librarian` agent if external packages/SDKs/services influence scope (migration notes, known pitfalls).
Record `file:line` evidence. Collect all results before scoping.

### 3. Analyze Requirements & Scope
Define in-scope, out-of-scope, assumptions, dependencies, constraints, and backwards compatibility.

### 4. Scope Epics and Tasks
- **Epics:** Foundation, Runtime Logic, UI/Scene, Data/Persistence, Assets, Tests/Release.
- **Tasks:** T-N ID, epic, title, 2-5 action steps, type, cost, affected files. Split tasks >XL.
- **Types:** `Logic`, `UI`, `Data`, `API`, `Asset`, `Test`, `Config`. Use template badges (`badge-logic`, etc.).
- **Costs:** `S` (<2h), `M` (2-4h), `L` (4-8h), `XL` (1-2d), `Spike` (timeboxed). Use template badges (`badge-cost-s`, etc.).
- **Rule:** Use ranges—never single-number estimates or fake precision. If confidence is low, price a discovery spike. Apply risk multiplier only when evidence supports it.

### 5. Generate PLAN.html
Fill template sections in order:
1. **Header:** Feature name (▲ logo rendered via CSS).
2. **Summary:** 1-5 bullet points (what, why, key constraints).
3. **Architecture Overview:** Current vs proposed + what changes.
4. **Technical Approach:** Numbered steps with `<code>` refs.
5. **Epics:** Table with #, epic name, 1-line purpose.
6. **Tasks Breakdown:** Table using type and cost badges. Include total low/high hour range.
7. **Risks:** Table using severity badges (`badge-sev-high`, etc.). Detail severity, area, mitigation.
8. **Backward Compatibility:** Area, impact (save data, APIs, scenes), migration steps.
9. **Acceptance Criteria:** Checkbox list grouped by category.

### 6. Output & Summary
Create directory: `mkdir -p Docs/Plans/{Name}`
Write `PLAN.html`. **Do not run task_create** or switch to execution mode; user reviews HTML plan first.
Report to user: Output location, total effort range, confidence level, top 2-3 risks, critical path, open assumptions.
