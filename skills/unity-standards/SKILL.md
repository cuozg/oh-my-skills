---
name: unity-standards
description: Unity development standards — MUST be included in load_skills for all Unity task delegations. Triggers when writing, reviewing, debugging, testing, or planning Unity C# code.
metadata:
  author: kuozg
  version: "1.1"
---

# unity-standards

Unity C# shared reference hub for code, review, debug, testing, planning, and UI Toolkit work.

## When This Skill Triggers

- Writing or refactoring Unity C# code
- Reviewing local changes or pull requests
- Debugging Unity runtime or compile issues
- Planning, testing, or documenting Unity systems

## Usage

- Always include `unity-standards` in `load_skills` for delegated Unity work.
- Load only the needed reference: `read_skill_file("unity-standards", "references/<path>")`.

## Reference Catalog

### Code Standards (20)

- `code-standards/naming.md` — naming, casing, file and namespace rules
- `code-standards/formatting.md` · `comments.md` · `access-modifiers.md`
- `code-standards/null-safety.md` · `serialization.md` · `lifecycle.md`
- `code-standards/events.md` · `error-handling.md` · `collections.md` · `linq.md`
- `code-standards/async.md` · `dependencies.md` · `code-patterns.md`
- `code-standards/architecture-patterns.md` · `refactoring-patterns.md`
- `code-standards/multi-file-workflow.md` · `single-file-runtime-workflow.md`
- `code-standards/unity-attributes.md` · `object-pooling.md`

### Review (12)

- `review/logic-checklist.md` · `unity-lifecycle-risks.md` · `serialization-risks.md`
- `review/performance-checklist.md` · `security-checklist.md` · `concurrency-checklist.md`
- `review/architecture-checklist.md` · `asset-checklist.md` · `prefab-checklist.md`
- `review/comment-format.md` · `pr-submission.md` · `parallel-review-criteria.md`

### Quality (6)

- `quality/grading-criteria.md` · `architecture-audit.md` · `performance-audit.md`
- `quality/best-practices-audit.md` · `tech-debt-audit.md` · `html-report-format.md`

### Plan (6)

- `plan/sizing-guide.md` · `risk-assessment.md` · `task-structure.md`
- `plan/investigation-workflow.md` · `dependency-mapping.md` · `output-quick.md`

### Debug (3)

- `debug/diagnosis-workflow.md` · `common-unity-errors.md` · `log-format.md`

### Test (5)

- `test/edit-mode-patterns.md` · `play-mode-patterns.md` · `test-case-format.md`
- `test/coverage-strategy.md` · `naming-conventions.md`

### Other (3)

- `other/mermaid-syntax.md` · `flatbuffers-guide.md` · `skill-authoring.md`

### UI Toolkit (6)

- `ui-toolkit/setup.md` · `performance.md` · `uxml-patterns.md`
- `ui-toolkit/uss-styling.md` · `csharp-bindings.md` · `custom-controls.md`
