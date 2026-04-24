---
name: unity-plan
description: >
  Use this skill for Unity cost estimation. Make sure to use it whenever the user asks what a
  Unity feature, refactor, migration, or integration will cost, how long it will take, how much
  work it is, wants an estimate, effort breakdown, risky parts, or phased delivery for pricing —
  even if they never say "costing". Investigate the codebase first with parallel `explore`
  subagents, use a `librarian` subagent only when external packages, SDKs, or services affect the
  estimate, then return evidence-backed hour ranges, task breakdowns, assumptions, risks, and
  confidence. Do not use it for implementation, design docs, or generic Unity planning without
  estimate intent.
metadata:
  author: kuozg
  version: "3.1"
---

# unity-plan

Produce evidence-backed Unity costing after investigation. This skill is for answering
"what will this cost?" rather than "please implement this".

## When to Use

- User asks for costing, effort, hours, scope, timeline, breakdown, estimate, or delivery phases
- Team needs a detailed estimate before starting a Unity feature, refactor, migration, or integration
- Request is too large or ambiguous to price without codebase investigation first

## Workflow

### Step 1: Define the costing target

Restate the feature or refactor in one line, then identify:
- goal of the estimate
- relevant constraints (platform, package, backwards compatibility, performance)
- what would materially change the price

If the request is underspecified, resolve as much ambiguity as possible from the codebase before asking anything.

### Step 2: Investigate in parallel

Launch background subagents before estimating.

Fire **3-5 `explore` agents in parallel**, each with a different angle:
1. entry points, public APIs, module boundaries
2. cross-system dependencies, events, shared state
3. existing patterns, lifecycle hooks, data flow
4. tests, coverage gaps, fragile areas
5. hot paths, allocation-sensitive or platform-sensitive code

Fire **1 `librarian` agent in parallel** when external packages, SDKs, services, or unfamiliar APIs influence scope.
Use it for migration notes, official constraints, version-specific setup cost, and known pitfalls.

Collect all background results before costing. Do not estimate from memory or from one file.

### Step 3: Turn findings into scope

Load shared planning references from `unity-standards`:
- `unity-standards/references/plan/investigation-workflow.md`
- `unity-standards/references/plan/sizing-guide.md`
- `unity-standards/references/plan/risk-assessment.md`

Use them to map:
- affected files and systems
- dependency chains and side effects
- tests that reduce or increase risk
- migration or compatibility work
- unknowns that justify lower confidence or a spike

### Step 4: Build the costing model

Break the work into **epics first, then tasks**.

For each task, include:
- ID
- Epic
- Task title
- Type (`Logic`, `UI`, `Data`, `API`, `Asset`, `Test`, `Config`, or `Spike`)
- Cost size
- Hour range
- Affected files or systems
- Dependency or sequencing note when relevant

Use `unity-standards/references/plan/sizing-guide.md` for size bands.
Use ranges instead of fake precision.
Apply a risk multiplier only when the evidence supports it, and say why.

### Step 5: Deliver detailed costing

Default to concise markdown with these sections:

1. **Costing Summary** — overall size, total hour range, confidence
2. **Assumptions** — what the estimate depends on
3. **Evidence** — `file:line` citations backing architecture or risk claims
4. **Epic Costing** — epic name, purpose, hours, dependencies
5. **Task Costing** — task-by-task breakdown with sizes and hour ranges
6. **Risks** — level, impact, mitigation, multiplier if used
7. **Critical Path** — what must happen in sequence
8. **Recommended Phases** — suggested delivery waves or spike-first plan

If confidence is low, explicitly price a discovery spike before the main work.

Epics, tasks, phases, and critical path are **estimation artifacts only**. They exist to explain
cost, sequencing pressure, and uncertainty — not to create an execution plan or authorize work.

## Rules

- Investigate first, estimate second
- Use parallel `explore` agents for internal codebase discovery
- Use `librarian` when external dependencies affect the estimate
- Cite `file:line` for every architectural, dependency, or risk claim
- Keep estimates evidence-based and expressed as ranges
- Surface assumptions, out-of-scope items, and unknowns clearly
- Never call `task_create` from this skill
- Never implement, refactor, or silently switch into execution mode
- If the request is not actually about costing, do not use this skill

## Output Heuristics

- Small costing request: inline estimate with scoped task table
- Large or architectural costing request: fuller phased breakdown with critical path and spike recommendation
- External SDK or service integration: include setup, migration, and verification cost explicitly
- Low-confidence estimate: include a discovery spike instead of pretending certainty

## Standards

Load shared references from `unity-standards`:
- `read_skill_file("unity-standards", "references/plan/investigation-workflow.md")`
- `read_skill_file("unity-standards", "references/plan/sizing-guide.md")`
- `read_skill_file("unity-standards", "references/plan/risk-assessment.md")`

Use those shared documents instead of duplicating sizing, investigation, or risk logic locally.
