---
name: unity-shared
description: Shared Unity C# reference library — code standards, review checklists, quality criteria, planning guides, debug patterns, test conventions. Not activated directly. Other skills load refs via read_skill_file.
---

# unity-shared

Centralized reference files for Unity AI skills. Never triggered directly — consumer skills load specific files on demand.

## Usage

```
read_skill_file("unity-shared", "references/code-standards/naming.md")
read_skill_file("unity-shared", "references/review/logic-checklist.md")
```

## Reference Catalog

### Code Standards (13)

- `code-standards/naming.md` — casing, prefixes, namespace, file naming
- `code-standards/formatting.md` — braces, spacing, line length, regions
- `code-standards/comments.md` — XML docs, inline comments, TODO format
- `code-standards/access-modifiers.md` — visibility, sealed, readonly, const
- `code-standards/null-safety.md` — null checks, TryGet, nullable patterns
- `code-standards/serialization.md` — SerializeField, field:, JsonUtility, SO data
- `code-standards/lifecycle.md` — Awake/Start/OnEnable order, coroutine rules
- `code-standards/events.md` — C# events, UnityEvent, SO channels, Action
- `code-standards/error-handling.md` — try/catch, Debug.LogException, assertions
- `code-standards/collections.md` — List vs array, Dictionary, ReadOnlyCollection
- `code-standards/async.md` — UniTask, async/await, cancellation tokens
- `code-standards/linq.md` — when to use, allocation warnings, hot path rules
- `code-standards/dependencies.md` — DI, service locator, constructor injection

### Review (11)

- `review/logic-checklist.md` — correctness, edge cases, state, data flow
- `review/unity-lifecycle-risks.md` — order-of-execution, null timing, scene load
- `review/serialization-risks.md` — missing fields, type changes, prefab overrides
- `review/performance-checklist.md` — allocations, Update, physics, rendering
- `review/security-checklist.md` — input validation, injection, data exposure
- `review/concurrency-checklist.md` — threading, race conditions, main thread
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries
- `review/asset-checklist.md` — texture, shader, animation, import settings
- `review/prefab-checklist.md` — missing scripts, variants, nested prefabs
- `review/comment-format.md` — inline review comment syntax and severity
- `review/pr-submission.md` — gh api format, comment batching, approval flow

### Quality (6)

- `quality/grading-criteria.md` — A-F scale definitions, evidence requirements
- `quality/architecture-audit.md` — coupling, layering, assembly structure
- `quality/performance-audit.md` — profiler markers, memory, frame budget
- `quality/best-practices-audit.md` — Unity API usage, deprecated calls
- `quality/tech-debt-audit.md` — TODO density, code duplication, complexity
- `quality/html-report-format.md` — report structure, CSS, no JavaScript

### Plan (7)

- `plan/sizing-guide.md` — XS/S/M/L/XL definitions, hour ranges
- `plan/risk-assessment.md` — risk levels, mitigation strategies
- `plan/task-structure.md` — subject/description format, skill routing
- `plan/investigation-workflow.md` — codebase scan steps before planning
- `plan/dependency-mapping.md` — blockedBy, parallel vs sequential
- `plan/output-quick.md` — inline report format for quick plans
- `plan/output-detail.md` — HTML plan structure for detail plans

### Debug (3)

- `debug/diagnosis-workflow.md` — symptom parsing, multi-angle analysis
- `debug/common-unity-errors.md` — NRE, serialization, lifecycle, physics
- `debug/log-format.md` — [DBG] prefix, color tags, UNITY_EDITOR guard

### Test (5)

- `test/edit-mode-patterns.md` — [Test], Assert, mocking, setup/teardown
- `test/play-mode-patterns.md` — [UnityTest], yield, scene loading
- `test/test-case-format.md` — HTML output structure, severity, coverage
- `test/coverage-strategy.md` — what to test, boundary values, edge cases
- `test/naming-conventions.md` — MethodName_Scenario_Expected format

### Other (3)

- `other/mermaid-syntax.md` — flowchart, sequence, state, class diagrams
- `other/flatbuffers-guide.md` — schema definition, codegen, serialization
- `other/skill-authoring.md` — SKILL.md rules, ref limits, progressive disclosure
