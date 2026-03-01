---
name: unity-shared
description: "Shared references, scripts, and standards for all Unity skills. Consolidates code standards, plan pipeline, debug fixes, review engine, investigation scripts, and documentation utilities. Not intended to be activated directly — loaded by domain skills as needed."
---

# Unity Shared References

Consolidated shared library for all Unity skills. Load specific references by domain.

## Code Standards (`references/code/`)

### C# Standards
- `code/coding-standards.md` — **INDEX** — Quick-reference navigation table + DO/DO NOT summary. Points to all `code/*.md` files.
- `code/csharp-hygiene.md` — Nullable refs, access modifiers, naming, sealed/readonly, dispose, strings
- `code/csharp-modern.md` — Expression-bodied, pattern matching, records, namespaces, Span
- `code/csharp-linq.md` — Core LINQ operations, chaining, materialization, anti-patterns
- `code/csharp-perf.md` — Cache allocations, string optimizations, struct vs class, ArrayPool
- `code/unity-lifecycle.md` — Init/cleanup order, Update/FixedUpdate/LateUpdate rules, coroutines, SO rules, async decision matrix

### Unity
- `code/unitask.md` — UniTask async patterns, cancellation, waiting, error handling, cheat sheet

### Patterns & Templates
- `code/template.md` — Starting template for new scripts
- `code/patterns-service.md` — Service, state, view patterns
- `code/patterns-async-state.md` — Async, state machine, SO config, cleanup
- `code/editor-patterns.md` — Editor scripting patterns
- `code/security.md` — Serialization safety, data integrity, anti-cheat, network, build security
- `code/architecture.md` — SOLID, DI (VContainer), SO event channels, assembly defs, folder structure

## Review Checklists (`references/review/`)

5 review checklist files loaded by review skills: `review-architecture-patterns.md`, `review-csharp.md`, `review-deep-workflow.md`, `review-gates.md`, `review-logic-data.md`

- `review/common-rules.md` — Common review rules
- `review/review-approval-criteria.md` — Approval criteria
- `review/review-asset-patterns.md` — Asset review patterns
- `review/review-general-checklists.md` — General review checklists
- `review/review-parallel-workflow.md` — Parallel review workflow
- `review/review-prefab-patterns.md` — Prefab review patterns
- `review/review-troubleshooting.md` — Review troubleshooting

## Quality Checklists (`references/quality/`)

- `quality/quality-unity-best-practices.md` — Unity lifecycle, serialization, prefab, input best practices
- `quality/quality-performance-checklist.md` — Full performance audit (CPU, GPU, memory, rendering)
- `quality/quality-code-checklist.md` — Code quality checklist
- `quality/quality-architecture-checklist.md` — Architecture checklist
- `quality/quality-project-health-checklist.md` — Project health checklist
- `quality/quality-review-workflow.md` — Quality review workflow

## Plan Pipeline (`references/planning/`)

- `planning/costing-and-types.md` — Cost/type definitions
- `planning/investigation-checklist.md` — Pre-plan investigation checklist
- `planning/investigation-analysis-rules.md` — Analysis rules
- `planning/prometheus-pipeline.md` — Pipeline flow reference
- `planning/task-system.md` — Task registration patterns (quick assessments + deep plans)
- `planning/task-patch-requirements.md` — Patch requirements
- `planning/plan-quick-example.md` — Quick plan example

## Debug (`references/debug/`)

- `debug/common-fixes.md` — Frequent Unity error fixes
- `debug/debug-fix-loop.md` — Fix loop workflow
- `debug/debug-log-reference.md` — Debug log reference

## Testing (`references/testing/`)

- `testing/test-patterns.md` — Test patterns
- `testing/test-examples.md` — Test examples
- `testing/test-assembly-setup.md` — Assembly setup for tests
- `testing/test-case-patterns.md` — Test case patterns
- `testing/qa-methodology.md` — QA methodology

## Other (`references/other/`)

- `other/bash-patterns.md` — Bash scripting patterns
- `other/flatbuffers-schema-pattern.md` — FlatBuffers schema patterns
- `other/mermaid-patterns.md` — Mermaid diagram patterns

## Scripts — `scripts/`
- `plan/investigate_feature.py` — Automated investigation script
- `investigate/trace_logic.py` — Logic tracing script
- `investigate/trace_unified.py` — Unified trace script
- `review/post_review.py` — GitHub API review posting
