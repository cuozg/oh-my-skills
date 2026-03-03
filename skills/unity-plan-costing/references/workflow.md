# unity-plan-costing — Workflow

## Deliverables

1 Markdown file + JSON.

```
Documents/Plans/{Name}/
├── PLAN.md     — Architecture, epics/tasks tree, risks, acceptance criteria
└── tasks.json  — Machine-readable task list
```

## Step 1: Read Template

Read `assets/templates/PLAN.md` before generating. Replace `[PLACEHOLDER]` tokens exactly.

## Step 2: Parallel Deep Investigation

Fire 3-5 `explore` subagents in background simultaneously — never sequentially:

```
Agent 1: "Entry points, public APIs, module boundaries for {feature}"
Agent 2: "Cross-system dependencies — calls, shared state, events"
Agent 3: "Existing patterns — DI, lifecycle hooks, data flow"
Agent 4: "Test coverage and infrastructure for affected areas"
Agent 5: "Performance-critical paths, allocations, hot loops"
```

Each agent targets a DIFFERENT angle. Collect all results before scoping.
Record `file:line` evidence for every finding.

## Step 3: Analyze Requirements

Define goals, acceptance criteria, constraints (backwards compat, perf budget),
out-of-scope items. Ask user if anything is unclear.

## Step 4: Scope Epics and Tasks

```
Feature
├── Epic 1 ── T-001 [Subject]  S · W1 · Logic
├── Epic 1 ── T-002 [Subject]  M · W1 · Data
├── Epic 2 ── T-003 [Subject]  L · W2 · UI   ⛓ T-002
└── Epic 3 ── T-004 [Subject]  M · W3 · Test  ⛓ T-003
```

- **Types**: `Logic`, `UI`, `Data`, `API`, `Asset`, `Test`, `Config`
- **Costs**: S (<2h), M (2-4h), L (4-8h), XL (1-2d)
- **Waves**: parallel tasks share a wave. Every task needs cost, type, wave, blockedBy

## Step 5: Generate PLAN.md

Fill template sections in order:
1. Header — feature name + summary stats (duration, tasks, epics, risk, complexity)
2. Architecture Overview — current vs proposed diagrams + key benefits
3. Technical Approach — numbered steps with `code` refs
4. **Epics & Tasks** (main focus) — epic summary table + task tree per epic + dependency graph + task details
5. Risks — severity table with 🔴🟡🟢 markers, cite `file:line`
6. Acceptance Criteria — checkbox list grouped by category

## Step 6: Generate tasks.json

```json
[{"id":"T-001","epic":"Name","subject":"...","type":"Logic","cost":"M","wave":1,"blockedBy":[],"blocks":["T-003"],"files":["Assets/Scripts/Foo.cs"]}]
```

## Step 7: Create Output + Summary

```bash
mkdir -p Documents/Plans/{Name}
```

Write all files. Report: location, total effort, top risks, critical path, wave count.

## Style

- Use `▲` Vercel header. Tree chars: `├── ─ └── │`
- Severity: 🔴 HIGH · 🟡 MEDIUM · 🟢 LOW
- Cost in backtick badges: `S` `M` `L` `XL`
- Keep text minimal — trees and tables over prose
- Use `<details>` for task walkthrough cards
- Mermaid optional — ASCII dependency graphs preferred

## No task_create

User reviews Markdown first, then decides when to register tasks.
