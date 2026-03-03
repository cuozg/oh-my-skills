# unity-plan-costing — Workflow

## Deliverables

1 Markdown file.

```
Documents/Plans/{Name}/
└── PLAN.md     — Summary, architecture, tasks breakdown, risks, compatibility, acceptance
```

## Step 1: Read Template

Read `references/output-template.md` before generating. Replace `[PLACEHOLDER]` tokens exactly.

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
- Every task needs: ID, epic, title, description (1 bullet per action — short, meaningful), type, cost, affected files

## Step 5: Generate PLAN.md

Fill template sections in order:
1. **Header** — feature name + summary stats (duration, tasks, epics, risk)
2. **Summary** — 1-5 bullet points: what, why, key constraints
3. **Architecture Overview** — current vs proposed diagrams + what changes
4. **Technical Approach** — numbered steps with `code` refs
5. **Epics** — table: #, epic name, 1-line purpose
6. **Tasks Breakdown** — table: ID, Epic, Title (short), Description (1 bullet per action), Type, Cost, Files
7. **Risks** — severity table: HIGH/MED/LOW, impact, mitigation, cite `file:line`
8. **Backward Compatibility** — table: area, impact (breaking/non-breaking), migration steps
9. **Acceptance Criteria** — checkbox list grouped by category

## Step 6: Create Output + Summary

```bash
mkdir -p Documents/Plans/{Name}
```

Write PLAN.md. Report: location, total effort, top risks, critical path.

## Style

- Use `▲` Vercel header. Bold **important** items.
- Severity: **HIGH** · **MED** · **LOW**
- Cost in backtick badges: `S` `M` `L` `XL`
- Keep text minimal — tables over prose, bullets over paragraphs
- Tasks use table format with bullet-per-action description (not tree or `<details>`)

## No task_create

User reviews Markdown first, then decides when to register tasks.
