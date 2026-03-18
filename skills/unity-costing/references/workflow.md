# unity-costing — Workflow

## Deliverables

1 HTML file.

```
Documents/Plans/{Name}/
└── PLAN.html   — Vercel-themed plan with summary, architecture, tasks, risks, acceptance
```

## Step 1: Read Template

Read `references/output-template.html` before generating. Replace `[PLACEHOLDER]` tokens exactly.
Use badge CSS classes for types and costs — do not invent new classes.

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

- **Types**: `Logic`, `UI`, `Data`, `API`, `Asset`, `Test`, `Config`
- **Costs**: `S` (<2h), `M` (2-4h), `L` (4-8h), `XL` (1-2d)
- Every task needs: ID, epic, title, description, type, cost, affected files

## Step 5: Generate PLAN.html

Fill template sections in order:
1. **Header** — feature name (▲ logo rendered via CSS)
2. **Summary** — 1-5 bullet points: what, why, key constraints
3. **Architecture Overview** — side-by-side current vs proposed + what changes
4. **Technical Approach** — numbered steps with `<code>` refs
5. **Epics** — table: #, epic name, 1-line purpose
6. **Tasks Breakdown** — table with badge classes:
   - Type badges: `badge-logic`, `badge-ui`, `badge-data`, `badge-api`, `badge-asset`, `badge-test`, `badge-config`
   - Cost badges: `badge-cost-s`, `badge-cost-m`, `badge-cost-l`, `badge-cost-xl`
7. **Risks** — table with severity badges: `badge-sev-high`, `badge-sev-med`, `badge-sev-low`
8. **Backward Compatibility** — table: area, impact, migration steps
9. **Acceptance Criteria** — checkbox list grouped by category

## Step 6: Create Output + Summary

```bash
mkdir -p Documents/Plans/{Name}
```

Write PLAN.html. Report: location, total effort, top risks, critical path.

## Style

- Vercel dark theme — black background, #111 cards, subtle borders
- Type/cost/severity use colored pill badges (CSS classes in template)
- No JavaScript — CSS-only, self-contained HTML
- Keep text minimal — tables over prose, bullets over paragraphs
- Print-friendly via `@media print` (white bg, black text)

## No task_create

User reviews HTML plan first, then decides when to register tasks.
