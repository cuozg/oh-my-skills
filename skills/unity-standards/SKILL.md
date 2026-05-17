---
name: unity-standards
description: "Shared Unity reference hub for writing, reviewing, debugging, planning, testing, documenting, and optimizing Unity C# systems."
metadata:
  author: kuozg
  version: "2.0"
---

# unity-standards

Use this skill as the compact router for Unity engineering standards. Keep the main
context small; load only the reference files that match the task.

## When This Skill Triggers

- Writing or refactoring Unity C# code
- Reviewing local changes or pull requests
- Debugging Unity runtime or compile issues
- Planning, testing, or documenting Unity systems
- Optimizing Unity project performance

## How To Use

1. Identify the Unity task type and touched surface.
2. Load the smallest matching references with
   `read_skill_file("unity-standards", "references/<path>")`.
3. For package/version-sensitive behavior, also load
   `other/official-source-map.md`.
4. Apply the repo's existing patterns first; use these references to catch gaps,
   risks, and verification requirements.

## Load References Accordingly

### Write Or Refactor Code

- General C#: `code-standards/core-conventions.md`
- Lifecycle, async, errors, validation: `code-standards/lifecycle-async-errors.md`
- Collections, LINQ, pooling, serialization: `code-standards/performance-data.md`
- Architecture, events, dependencies, editor tools, WebGL: `code-standards/architecture-systems.md`
- ECS, Jobs, Burst, NativeContainers: `code-standards/ecs-burst-standards.md`

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

### Optimize Performance

- Build and startup: `optimization/build-settings.md`,
  `optimization/startup-settings.md`
- Rendering: `optimization/rendering-settings.md`
- Memory and loading: `optimization/memory-settings.md`
- Physics: `optimization/physics-settings.md`
- Mobile: `optimization/mobile-settings.md`
- Jobs/Burst/ECS: `optimization/jobs-burst-migration.md`,
  `optimization/ecs-data-oriented-design.md`

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
- Code-standard consolidation map: `code-standards/README.md`
