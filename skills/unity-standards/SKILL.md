---
name: unity-standards
description: >
  Use this skill as the shared reference hub for all Unity C# development — coding standards, naming
  conventions, review checklists, debug patterns, test patterns, and UI Toolkit guidelines. MUST be
  included in load_skills for any Unity task delegation. Triggers automatically when writing, reviewing,
  debugging, testing, or planning Unity C# code.   Contains 80+ reference files across 9 categories that
  other skills pull from on demand. Includes editor patterns for CustomEditor, EditorWindow,
  PropertyDrawer, Gizmos, and Handles. Also covers optimization settings for build, rendering,
  memory, physics, mobile, startup, and Jobs/Burst migration.
metadata:
  author: kuozg
  version: "1.2"
---

# unity-standards

Unity C# shared reference hub for code, review, debug, testing, planning, and UI Toolkit work.

## When This Skill Triggers

- Writing or refactoring Unity C# code
- Reviewing local changes or pull requests
- Debugging Unity runtime or compile issues
- Planning, testing, or documenting Unity systems
- Optimizing Unity project performance

## Usage

- Always include `unity-standards` in `load_skills` for delegated Unity work.
- Load only the needed reference: `read_skill_file("unity-standards", "references/<path>")`.

## Reference Catalog

### Code Standards (34)

- `code-standards/naming.md` — naming, casing, file and namespace rules
- `code-standards/project-structure.md` — folder layout, feature-based organization, .asmdef, .gitignore
- `code-standards/formatting.md` · `comments.md` · `access-modifiers.md`
- `code-standards/null-safety.md` · `null-safety-advanced.md`
- `code-standards/serialization.md` · `lifecycle.md` · `lifecycle-advanced.md`
- `code-standards/events.md` · `error-handling.md` · `error-handling-advanced.md`
- `code-standards/collections.md` · `collections-advanced.md` · `linq.md`
- `code-standards/async.md` · `async-advanced.md`
- `code-standards/dependencies.md` · `dependencies-advanced.md` · `code-patterns.md`
- `code-standards/architecture-patterns.md` · `architecture-patterns-advanced.md`
- `code-standards/refactoring-patterns.md` · `multi-file-workflow.md` · `single-file-runtime-workflow.md`
- `code-standards/unity-attributes.md` · `unity-attributes-advanced.md`
- `code-standards/object-pooling.md` · `object-pooling-advanced.md`
- `code-standards/editor-patterns.md` · `gizmos-handles.md`
- `code-standards/webgl-restrictions.md` — WebGL platform restrictions, unsupported APIs, workaround patterns

### Review (15)

- `review/logic-checklist.md` · `unity-lifecycle-risks.md` · `serialization-risks.md`
- `review/performance-checklist.md` · `performance-checklist-advanced.md`
- `review/security-checklist.md` · `security-checklist-advanced.md`
- `review/concurrency-checklist.md` · `concurrency-checklist-advanced.md`
- `review/architecture-checklist.md` · `asset-checklist.md` · `prefab-checklist.md`
- `review/comment-format.md` · `pr-submission.md` · `parallel-review-criteria.md`

### Quality (6)

- `quality/grading-criteria.md` · `architecture-audit.md` · `performance-audit.md`
- `quality/best-practices-audit.md` · `tech-debt-audit.md` · `html-report-format.md`

### Plan (7)

- `plan/sizing-guide.md` · `risk-assessment.md` · `task-structure.md`
- `plan/investigation-workflow.md` · `dependency-mapping.md` · `output-quick.md`
- `plan/investigation-template.md` — markdown template for system investigation reports

### Debug (4)

- `debug/diagnosis-workflow.md` · `common-unity-errors.md` · `log-format.md`
- `debug/analysis-template.md` — structured report template for deep bug analysis output

### Test (6)

- `test/edit-mode-patterns.md` · `edit-mode-advanced.md`
- `test/play-mode-patterns.md` · `test-case-format.md`
- `test/coverage-strategy.md` · `naming-conventions.md`

### Other (3)

- `other/mermaid-syntax.md` · `flatbuffers-guide.md` · `skill-authoring.md`

### UI Toolkit (6)

- `ui-toolkit/setup.md` · `performance.md` · `uxml-patterns.md`
- `ui-toolkit/uss-styling.md` · `csharp-bindings.md` · `custom-controls.md`

### Optimization (7)

- `optimization/build-settings.md` — code stripping, IL2CPP, compression, texture/audio/mesh settings
- `optimization/rendering-settings.md` — SRP Batcher, GPU instancing, batching, shader variants, LOD, occlusion culling
- `optimization/memory-settings.md` — texture streaming, audio memory, asset lifecycle, Addressables, scene loading
- `optimization/physics-settings.md` — layer collision matrix, fixed timestep, collision shapes, auto sync transforms
- `optimization/mobile-settings.md` — target frame rate, thermal throttling, resolution scaling, battery-conscious design
- `optimization/startup-settings.md` — Enter Play Mode settings, domain reload, preloading, script execution order
- `optimization/jobs-burst-migration.md` — Jobs system, Burst compiler, data layout, migration checklist
