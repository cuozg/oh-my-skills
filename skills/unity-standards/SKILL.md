---
name: unity-standards
description: "Use for Unity 6 engineering standards: C# code, asset managers, Addressables, analytics, LiveOps, config, server API, IAP, prefab, Canvas UI, material, shader, draw calls, batching, debugging, optimization, reviews, project investigation, tests, plans, todos, acceptance criteria, and technical docs."
metadata:
  author: kuozg
  version: "3.0"
---

# unity-standards

Compact Unity engineering standards router. Assumes Unity basics; this skill tells
the agent which local standards to load and what evidence proves the work is done.

## Agent Contract

Make Unity work predictable: inspect the real project first, choose the smallest
applicable standard, make the smallest correct change, and verify through
Unity-aware evidence. Every loaded reference must answer the current task.

This is the standards layer. Pair it with a task-specific skill when the primary
work is Editor tooling, unit tests, debugging, technical design, costing, docs,
or PR review (see Pair With Specialized Skills).

## Baseline

- **Unity 6.0+ (6000.x)**, latest Unity 6 LTS preferred. Read
  `ProjectSettings/ProjectVersion.txt` and `Packages/manifest.json` first; the
  project's actual version and packages override this baseline.
- **Editor access goes through the `unity` CLI** (`unity:unity-cli` skill). Run the
  preflight in `references/other/unity-cli-routing.md` before any step that needs
  a live Editor (compile, console, tests, scene/prefab edits, Play Mode proof).

## Operating Rules

1. Start from the user's named file, symbol, scene, prefab, branch, or symptom.
2. State assumptions for ambiguous work; ask only when a reasonable assumption
   would be risky.
3. Load only the smallest matching reference set (first entry of each section
   below). Add more only when the touched surface changes or evidence is missing.
4. Prefer the project's current patterns over generic Unity advice.
5. Keep changes surgical: no adjacent refactors, speculative abstractions, or
   unrelated cleanup.
6. For package, Unity-version, platform, ECS, Burst, WebGL, Addressables, or UI
   Toolkit behavior, verify against official docs via `references/other/official-source-map.md`.
7. Finish with Unity-grade proof (see Verification Defaults).

## Load References Accordingly

### Write Or Refactor Code

- General C#: `references/code-standards/core-conventions.md`
- Lifecycle, async, errors, validation: `references/code-standards/lifecycle-async-errors.md`
- Collections, LINQ, pooling, serialization: `references/code-standards/performance-data.md`
- Architecture, events, dependencies, editor tools, WebGL: `references/code-standards/architecture-systems.md`
- ECS, Jobs, Burst, NativeContainers: `references/code-standards/ecs-burst-standards.md`
- File map: `references/code-standards/README.md`

### Asset Managers, Addressables, And Assets

- Asset-manager and Addressables work:
  `references/asset-management/addressables-asset-manager.md`
- Prefab work: `references/asset-management/prefab-work.md`
- Canvas UI work: `references/asset-management/canvas-ui-work.md`
- Material work: `references/asset-management/material-work.md`
- Shader work: `references/asset-management/shader-work.md`
- Add `references/code-standards/architecture-systems.md` when ownership, dependency
  boundaries, or platform branches are involved.
- Add `references/optimization/memory-settings.md` for memory pressure, asset release, or
  loading spikes.

### Production Ownership, Analytics, And LiveOps

- Full-cycle feature ownership, analytics, LiveOps, release, and monitoring:
  `references/production/full-cycle-ownership.md`
- Add `references/code-standards/architecture-systems.md` for config, server/client, SDK,
  data ownership, or feature-boundary decisions.
- Add `references/code-standards/performance-data.md` for scalable config, player data,
  save data, and generated/procedural data structures.
- Add `references/code-standards/lifecycle-async-errors.md` for server API integration,
  retry, timeout, cancellation, and user-facing error behavior.
- Add `references/other/official-source-map.md` for IAP, billing, privacy, store review, or
  platform compliance claims.

### Review Changes Or PRs

- Main review pass: `references/review/checklist.md`
- C# implementation: `references/review/checklist_cs.md`
- Assets: `references/review/checklist_prefab.md`, `references/review/checklist_material.md`,
  `references/review/checklist_shader.md`
- ECS/Burst: `references/review/ecs-burst-review.md`
- Parallel review criteria: `references/review/parallel-review-criteria.md`

### Debug Runtime Or Compile Issues

- Start here: `references/debug/diagnosis-workflow.md`
- Compile verification: `references/debug/compile-verification.md`
- Known error patterns: `references/debug/common-unity-errors.md`
- Deep investigations: `references/debug/deep-investigation-checklist.md`,
  `references/debug/analysis-template.md`
- ECS/Burst diagnostics: `references/debug/ecs-burst-debugging.md`

### Plan, Test, Or Document Systems

- Planning flow: `references/plan/confirmation-flow.md`, `references/plan/dependency-mapping.md`
- Plan output: `references/plan/output-quick.md` or `references/plan/output-deep.md`
- Acceptance criteria: `references/test/acceptance-criteria-verification.md`
- Test strategy: `references/test/coverage-strategy.md`, `references/test/edit-mode-patterns.md`,
  `references/test/edit-mode-advanced.md`, `references/test/play-mode-patterns.md`
- Test docs and manual QA cases: `references/test/test-case-format.md`, `references/test/naming-conventions.md`
- Diagrams: `references/other/mermaid-syntax.md`

### Investigate Project Structure Or Logic

- Investigation workflow: `references/debug/deep-investigation-checklist.md`
- Report structure: `references/debug/analysis-template.md`
- Dependency and call flow: `references/plan/dependency-mapping.md`
- Diagrams: `references/other/mermaid-syntax.md`

### Optimize Performance

- Build and startup: `references/optimization/build-settings.md`,
  `references/optimization/startup-settings.md`
- Rendering: `references/optimization/rendering-settings.md`
- Canvas UI, draw calls, and batching:
  `references/optimization/canvas-ui-drawcalls-batching.md`
- Memory and loading: `references/optimization/memory-settings.md`
- Physics: `references/optimization/physics-settings.md`
- Mobile: `references/optimization/mobile-settings.md`
- Jobs/Burst/ECS: `references/optimization/jobs-burst-migration.md`,
  `references/optimization/ecs-data-oriented-design.md`
- Broader audit: `references/quality/performance-audit.md`

### Audit Quality Or Technical Debt

- Best practices: `references/quality/best-practices-audit.md`
- Architecture: `references/quality/architecture-audit.md`
- Performance: `references/quality/performance-audit.md`
- Technical debt: `references/quality/tech-debt-audit.md`
- Scoring/reporting (only when requested): `references/quality/grading-criteria.md`,
  `references/quality/html-report-format.md`

### UI Toolkit

- Setup: `references/ui-toolkit/setup.md`
- UXML/USS: `references/ui-toolkit/uxml-patterns.md`, `references/ui-toolkit/uss-styling.md`
- C# bindings and controls: `references/ui-toolkit/csharp-bindings.md`,
  `references/ui-toolkit/custom-controls.md`
- Performance: `references/ui-toolkit/performance.md`

### Cross-Cutting Helpers

- Unity Editor access (CLI first, MCP fallback): `references/other/unity-cli-routing.md`
- FlatBuffers: `references/other/flatbuffers-guide.md`

## Pair With Specialized Skills

| Primary Task | Pair With | How `unity-standards` Helps |
|--------------|-----------|-----------------------------|
| Project scaffold, asmdefs, CLAUDE.md | `unity-init` | asmdef boundaries, folder conventions |
| Unit tests | `unity-test-unit` | test mode, naming, coverage, verification rules |
| Editor tools | `unity-editor` | editor-code isolation, Undo, serialized property standards |
| Debugging | `unity-debug` / `unity-log` | diagnosis workflow, error patterns, compile verification |
| Technical design, costing, WBS | `unity-technical` / `unity-costing` / `unity-wbs` | assumptions, dependencies, risks, acceptance criteria |
| System docs | `unity-document` | investigation checklist, Mermaid |
| PR review | `unity-review-pr` | severity, evidence, changed-line discipline |
| Editor/CLI automation, tests, builds | `unity:unity-cli` | Editor routing and verification evidence |
| UI Toolkit / uGUI deep work | `unity:ui-uitk` / `unity:ui-ugui` | UI performance and binding standards |
| WebGL / Web builds | `unity:optimize-web` | platform boundaries, async/storage/build constraints |
| Packages (UPM) | `unity:unity-package-management` | package-sensitive API checks |

## Verification Defaults

Run Editor-dependent checks through `references/other/unity-cli-routing.md`.

- Code change: compile check (live Editor `recompile` + console scan, or
  `Logs/Editor.log` grep), then focused tests for the touched behavior
  (`unity test --filter <name>` or the Editor's test command).
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
