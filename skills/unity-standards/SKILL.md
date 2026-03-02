---
name: unity-standards
description: Unity development standards — MUST be included in load_skills for all Unity task delegations. Triggers when writing, reviewing, debugging, testing, or planning Unity C# code.
---

# unity-standards

Unity C# development standards — naming, formatting, lifecycle, events, DI, serialization, null-safety, async, and more.

## When This Skill Triggers

- Writing or refactoring Unity C# code
- Implementing Unity features
- Working with events and signals
- Accessing or modifying game data
- Reviewing code changes or pull requests
- Setting up project architecture

## Usage

**Delegation rule**: Always include `unity-standards` in `load_skills` when delegating any Unity task.
Load references on demand via `read_skill_file("unity-standards", "references/<file>")`.

## Reference Catalog

### Code Standards (17)

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
- `code-standards/code-patterns.md` — MonoBehaviour, SO data, interface, UnityEvent templates
- `code-standards/architecture-patterns.md` — state machine, MVC/MVP, command pattern
- `code-standards/multi-file-workflow.md` — dependency ordering, namespace strategy, asmdef awareness
- `code-standards/refactoring-patterns.md` — extract class, introduce interface, decompose, migrate

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
