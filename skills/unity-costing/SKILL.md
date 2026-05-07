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
  version: "2.0"
---
# unity-costing

Create a detailed Unity costing report for a feature, refactor, integration, or task set. The output is an HTML plan that summarizes the change, explains architecture and technical approach, decomposes work into epics and detailed tasks, estimates effort, and lists risks, acceptance criteria, and compatibility impacts.

## Core Deliverable

Write one self-contained HTML file using the exact section structure from:

`references/output-template.html`

Default output path:

`Docs/Plans/{FeatureName}_costing/PLAN.html`

If the repo already uses a different planning folder, follow the repo convention and state the path.

## Required Sections

Follow the template order and preserve its visual structure:

1. **Summary** — what changes, why it matters, scope/constraints, total estimate.
2. **Architecture Overview** — current architecture vs proposed architecture, plus concrete component changes.
3. **Technical Approach** — ordered implementation strategy with code references.
4. **Epics** — high-level work streams with one-line purpose.
5. **Tasks Breakdown** — primary section: task ID, epic, title, action steps, type, cost, files.
6. **Risks** — risk, severity, impact, mitigation.
7. **Backward Compatibility** — affected area, impact, migration/guardrail.
8. **Acceptance Criteria** — grouped checklist covering behavior, tests, compatibility, release readiness.

## Workflow

### 1. Clarify only blocking ambiguity

Ask concise questions before investigating only when missing info changes the estimate materially:

- target platform or Unity version is unknown and platform constraints matter
- feature boundaries are unclear
- quality bar is ambiguous (prototype vs production)
- required integrations, SDKs, backend contracts, or design assets are unknown
- estimate unit is unclear (hours, days, story points) and user did not imply one

Do not ask if a reasonable assumption can be stated in the report.

### 2. Investigate before estimating

Read enough code and project files to ground the plan. Look for:

- entry points and affected scenes/prefabs/scripts
- current architecture, ownership boundaries, events, services, data flow
- existing patterns for DI, lifecycle, serialization, Addressables, UI, input, tests
- platform constraints and package dependencies
- tests and validation infrastructure

For cross-system or uncertain work, fire parallel subagents. Use different investigation angles, for example:

- existing feature/module boundaries and entry points
- data flow, events, save/load, networking, or backend dependencies
- UI/scene/prefab/asset impact
- test coverage and validation strategy
- performance, platform, build, or compatibility risk

Every architectural claim, risk, dependency, or compatibility concern should cite evidence as `path:line` when available. If no code exists yet, mark the item as assumption.

### 3. Scope the change

Define:

- **In scope** — what the estimate covers
- **Out of scope** — what it explicitly excludes
- **Assumptions** — unknowns that affect confidence
- **Dependencies** — assets, packages, services, design, backend, approvals
- **Confidence** — High / Medium / Low with reason

Keep this concise; put long detail in tables.

### 4. Build epics

Create epics as delivery slices, not vague categories. Good epics produce shippable progress:

- Foundation / integration setup
- Runtime logic / systems
- UI / scene / prefab wiring
- Data / persistence / migration
- Assets / content setup
- Tests / validation / release readiness

Each epic needs:

- short name
- one-line purpose
- dependency notes if blocked by another epic

### 5. Break epics into detailed tasks

The task table is the main deliverable. Each task must include:

- stable ID: `T-1`, `T-2`, ...
- epic name
- short imperative title
- 2-5 concrete action steps
- type badge
- cost badge and hour range
- affected files or likely file paths
- dependency/blocker note when relevant

Prefer many clear tasks over one broad task. Split any task larger than XL unless it is intentionally a research spike.

## Costing Model

Use this default scale unless the user specifies another:

| Size | Effort | Use when |
| --- | --- | --- |
| XS | < 1h | trivial config, small code edit, tiny validation |
| S | 1-2h | single-file or simple prefab/UI work |
| M | 2-4h | focused task with tests or limited wiring |
| L | 4-8h | multi-file change, significant integration, complex validation |
| XL | 1-2d | broad slice, uncertain integration, cross-system task |
| Spike | timeboxed | investigation needed before reliable estimate |

The provided template has CSS cost badges for `S`, `M`, `L`, `XL`. If using `XS` or `Spike`, either map visually to the nearest existing class and label clearly, or add minimal CSS only if needed. Do not invent complex styling.

Always include:

- per-task size
- per-task hour range
- total low/high estimate
- confidence level
- critical path or sequencing note

## Task Types

Use template badge classes:

- `Logic` — runtime C# behavior, systems, gameplay, services
- `UI` — UI Toolkit/uGUI/screens/HUD/menu work
- `Data` — save data, schemas, configs, ScriptableObjects, migrations
- `API` — SDK/backend/service integration boundaries
- `Asset` — prefabs, scenes, Addressables, audio, sprites, materials
- `Test` — EditMode/PlayMode tests, smoke checks, QA validation
- `Config` — project settings, packages, build/player settings, asmdefs

## Risk Rules

List concrete risks only. For each risk include:

- severity: HIGH / MED / LOW
- why it matters
- affected area
- mitigation
- evidence or assumption marker

Common Unity risks to check:

- scene/prefab reference breakage
- serialized data migration
- platform-specific behavior
- Addressables/catalog compatibility
- input/backend/SDK contract mismatch
- performance/GC/frame budget
- package or Unity version constraints
- missing tests or hard-to-automate validation

## Compatibility Rules

Always include compatibility, even if impact is low. Cover:

- existing save data and serialized fields
- public APIs and assembly definitions
- scenes/prefabs/assets already in use
- platform/build settings
- Addressables or remote content
- analytics/liveops/backend contracts when relevant

If no migration is needed, say why.

## Template Use

Before writing `PLAN.html`, read `references/output-template.html` and replace all placeholder rows/tokens with real content. Preserve:

- section IDs and order
- CSS-only, self-contained HTML
- badge class names from the template
- dark Vercel-style layout

Do not leave `[PLACEHOLDER]` tokens in output.
Do not add JavaScript.
Do not create project tasks or tickets automatically; the user decides after reviewing the costing.

## Output Quality Bar

A good report is:

- evidence-backed, with code/file references where possible
- compact but specific
- task-heavy, not prose-heavy
- clear about assumptions and confidence
- useful for a lead developer to approve, sequence, and assign work
- safe for Unity projects: no destructive changes, no unapproved package/settings edits

## Final Response

After creating the report, answer with:

- output file path
- total estimate range
- confidence level
- top 2-3 risks
- any questions or assumptions that still affect estimate
