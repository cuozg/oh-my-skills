---
name: unity-standards
description: "Use for Unity engineering standards: C# code, asset managers, Addressables, analytics, LiveOps, config, server API, IAP, prefab, Canvas UI, material, shader, draw calls, batching, debugging, optimization, reviews, project investigation, tests, plans, todos, acceptance criteria, and technical docs."
metadata:
  author: kuozg
  version: "2.1"
---

# unity-standards

Use this as the compact Unity engineering standards router. Codex already knows
Unity basics; this skill tells the agent which local standards to load and what
evidence proves the work is done.

## Agent Contract

Use this skill to make Unity work predictable: inspect the real project first,
choose the smallest applicable standard, make the smallest correct change, and
verify through Unity-aware evidence. Do not turn this skill into a generic Unity
tutorial; every loaded reference should answer the current task.

This is the standards layer, not a replacement for specialized Unity skills. Pair
it with a task-specific skill when the primary work is asset generation, audio
clip preparation, UI Toolkit implementation, Editor tooling, WebGL integration,
manual QA test cases, unit-test authoring, technical design, costing, or PR
review automation.

## When This Skill Triggers

- Writing or refactoring Unity C# code
- Reviewing local changes or pull requests
- Debugging Unity runtime or compile issues
- Investigating Unity project structure, logic, or data flow
- Planning, breaking down, testing, or documenting Unity systems
- Optimizing Unity project performance
- Product ownership, analytics, LiveOps, remote config, server API, IAP,
  release, or post-launch monitoring work
- Asset-manager, Addressables, prefab, material, shader, Canvas UI, draw-call,
  batching, or asset-pipeline work

## Operating Rules

1. Start from the user's named file, symbol, scene, prefab, branch, or symptom.
2. State assumptions for ambiguous work; ask only when a reasonable assumption
   would be risky.
3. Load only the smallest matching reference set. Add more only when the touched
   surface changes or evidence is missing.
4. Prefer the project's current patterns over generic Unity advice.
5. Keep changes surgical: no adjacent refactors, speculative abstractions, or
   unrelated cleanup.
6. For package, Unity-version, platform, ECS, Burst, WebGL, Addressables, or UI
   Toolkit behavior, verify against official docs via `other/official-source-map.md`.
7. Finish with Unity-grade proof: compile result, targeted tests, console scan,
   Play Mode/Edit Mode validation, scene/prefab inspection, profiler evidence, or
   PR diff verification as appropriate.

## Task Router

| Task | Load first | Add when needed |
|------|------------|-----------------|
| C# code or refactor | `code-standards/core-conventions.md` | lifecycle, data/perf, architecture, ECS refs by surface |
| Asset manager or Addressables | `asset-management/addressables-asset-manager.md` | memory/loading refs, architecture, platform docs |
| Analytics, LiveOps, config, server API, IAP, release, or monitoring | `production/full-cycle-ownership.md` | architecture, data/perf, lifecycle/errors, official docs |
| Prefab asset work | `asset-management/prefab-work.md` | Canvas UI, material, shader, Addressables, or review refs by touched asset |
| Canvas UI asset work | `asset-management/canvas-ui-work.md` | draw-call/batching, prefab, material, shader, or UI Toolkit refs by surface |
| Material asset work | `asset-management/material-work.md` | shader, rendering settings, batching, or review refs |
| Shader asset work | `asset-management/shader-work.md` | material, rendering settings, batching, or official render-pipeline docs |
| Canvas UI draw calls or batching | `optimization/canvas-ui-drawcalls-batching.md` | Canvas UI asset, rendering settings, material, shader, or prefab refs |
| Debug issue | `debug/diagnosis-workflow.md` | compile, common errors, deep investigation, ECS debugging |
| Optimize | matching optimization reference below | `quality/performance-audit.md` for broader audits |
| Review code or PR | `review/checklist.md` | C#, prefab, material, shader, ECS, parallel criteria |
| Investigate project logic | `debug/deep-investigation-checklist.md` | `debug/analysis-template.md`, dependency mapping, Mermaid |
| Plan or break down work | `plan/confirmation-flow.md` | dependency map plus quick/deep output template |
| Write Unity Test Framework tests | `test/coverage-strategy.md` | Edit Mode, Play Mode, advanced patterns, naming |
| Acceptance criteria | `test/acceptance-criteria-verification.md` | test-case format if manual QA is requested |
| Quality audit | matching quality reference below | grading and HTML report only when requested |
| UI Toolkit | `ui-toolkit/setup.md` | UXML, USS, bindings, controls, performance |

## Pair With Specialized Skills

| Primary Task | Pair With | How `unity-standards` Helps |
|--------------|-----------|-----------------------------|
| Unit tests | `unity-test-unit` | test mode, naming, coverage, verification rules |
| Manual QA cases | `unity-test-case` | acceptance criteria and evidence expectations |
| Runtime UI Toolkit | `unity-uitoolkit` | UI Toolkit architecture, performance, binding standards |
| Editor tools | `unity-editor` | editor-code isolation, Undo, serialized property standards |
| WebGL work | `unity-webgl` | platform boundaries, async/storage/build constraints |
| Asset/image/audio generation | relevant asset/audio skills | validation, placement, performance, and proof requirements |
| Technical plans/costing | `unity-technical` / `unity-costing` | assumptions, dependencies, risks, acceptance criteria |
| PR review or local review | Unity review skills | severity, evidence, changed-line discipline |

## Load References Accordingly

### Write Or Refactor Code

- General C#: `code-standards/core-conventions.md`
- Lifecycle, async, errors, validation: `code-standards/lifecycle-async-errors.md`
- Collections, LINQ, pooling, serialization: `code-standards/performance-data.md`
- Architecture, events, dependencies, editor tools, WebGL: `code-standards/architecture-systems.md`
- ECS, Jobs, Burst, NativeContainers: `code-standards/ecs-burst-standards.md`

### Asset Managers, Addressables, And Assets

- Asset-manager and Addressables work:
  `asset-management/addressables-asset-manager.md`
- Prefab work: `asset-management/prefab-work.md`
- Canvas UI work: `asset-management/canvas-ui-work.md`
- Material work: `asset-management/material-work.md`
- Shader work: `asset-management/shader-work.md`
- Legacy combined map for mixed tasks:
  `asset-management/prefab-material-shader-work.md`
- Add `code-standards/architecture-systems.md` when ownership, dependency
  boundaries, or platform branches are involved.
- Add `optimization/memory-settings.md` for memory pressure, asset release, or
  loading spikes.

### Production Ownership, Analytics, And LiveOps

- Full-cycle feature ownership, analytics, LiveOps, release, and monitoring:
  `production/full-cycle-ownership.md`
- Add `code-standards/architecture-systems.md` for config, server/client, SDK,
  data ownership, or feature-boundary decisions.
- Add `code-standards/performance-data.md` for scalable config, player data,
  save data, and generated/procedural data structures.
- Add `code-standards/lifecycle-async-errors.md` for server API integration,
  retry, timeout, cancellation, and user-facing error behavior.
- Add `other/official-source-map.md` for IAP, billing, privacy, store review, or
  platform compliance claims.

### Review Changes Or PRs

- Main review pass: `review/checklist.md`
- C# implementation: `review/checklist_cs.md`
- Assets: `review/checklist_prefab.md`, `review/checklist_material.md`,
  `review/checklist_shader.md`
- ECS/Burst: `review/ecs-burst-review.md`
- Parallel review criteria: `review/parallel-review-criteria.md`

### Debug Runtime Or Compile Issues

- Start here: `debug/diagnosis-workflow.md`
- Compile verification: `debug/compile-verification.md`
- Known error patterns: `debug/common-unity-errors.md`
- Deep investigations: `debug/deep-investigation-checklist.md`,
  `debug/analysis-template.md`
- ECS/Burst diagnostics: `debug/ecs-burst-debugging.md`

### Plan, Test, Or Document Systems

- Planning flow: `plan/confirmation-flow.md`, `plan/dependency-mapping.md`
- Plan output: `plan/output-quick.md` or `plan/output-deep.md`
- Acceptance criteria: `test/acceptance-criteria-verification.md`
- Test strategy: `test/coverage-strategy.md`, `test/edit-mode-patterns.md`,
  `test/edit-mode-advanced.md`, `test/play-mode-patterns.md`
- Test docs: `test/test-case-format.md`, `test/naming-conventions.md`
- Diagrams: `other/mermaid-syntax.md`

### Investigate Project Structure Or Logic

- Investigation workflow: `debug/deep-investigation-checklist.md`
- Report structure: `debug/analysis-template.md`
- Dependency and call flow: `plan/dependency-mapping.md`
- Diagrams: `other/mermaid-syntax.md`

### Optimize Performance

- Build and startup: `optimization/build-settings.md`,
  `optimization/startup-settings.md`
- Rendering: `optimization/rendering-settings.md`
- Canvas UI, draw calls, and batching:
  `optimization/canvas-ui-drawcalls-batching.md`
- Memory and loading: `optimization/memory-settings.md`
- Physics: `optimization/physics-settings.md`
- Mobile: `optimization/mobile-settings.md`
- Jobs/Burst/ECS: `optimization/jobs-burst-migration.md`,
  `optimization/ecs-data-oriented-design.md`

### Audit Quality Or Technical Debt

- Best practices: `quality/best-practices-audit.md`
- Architecture: `quality/architecture-audit.md`
- Performance: `quality/performance-audit.md`
- Technical debt: `quality/tech-debt-audit.md`
- Scoring/reporting: `quality/grading-criteria.md`,
  `quality/html-report-format.md`

### UI Toolkit

- Setup: `ui-toolkit/setup.md`
- UXML/USS: `ui-toolkit/uxml-patterns.md`, `ui-toolkit/uss-styling.md`
- C# bindings and controls: `ui-toolkit/csharp-bindings.md`,
  `ui-toolkit/custom-controls.md`
- Performance: `ui-toolkit/performance.md`

### Cross-Cutting Helpers

- Unity MCP routing: `other/unity-mcp-routing-matrix.md`
- FlatBuffers: `other/flatbuffers-guide.md`
- Skill authoring: `other/skill-authoring.md`
- Code-standard reference map: `code-standards/README.md`

## Verification Defaults

- Code change: run compile or the repo's fastest equivalent, then focused tests
  for the touched behavior when practical.
- Bug fix: prove the old failure path and the fixed path; use logs only when a
  test or direct editor validation is not practical.
- Review: inspect committed diff or PR files, report findings first with
  severity and file/line evidence, and avoid unrelated local changes.
- Optimization: capture before/after evidence with profiler, frame timing,
  memory, build size, or platform-specific metrics.
- Production feature: verify the runtime behavior plus analytics schema, remote
  config or LiveOps controls, server/API failure paths, release risk, and
  post-launch monitoring plan when those surfaces are touched.
- Planning/todos: include assumptions, dependencies, risks, acceptance criteria,
  and concrete verification steps.

## Output Standards

- Be direct: answer the exact Unity question before broad guidance.
- Be evidence-based: cite files, symbols, scenes, prefabs, console lines, or test
  names instead of hand-waving.
- Be compact: prefer short checklists and task tables over long essays.
- Be honest about limits: if Unity Editor, platform hardware, or profiler data is
  unavailable, say what was not verified and what evidence was used instead.
