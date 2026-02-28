---
name: unity-shared
description: "Shared references, scripts, and standards for all Unity skills. Consolidates code standards, plan pipeline, debug fixes, review engine, investigation scripts, and documentation utilities. Not intended to be activated directly — loaded by domain skills as needed."
---

# Unity Shared References

Consolidated shared library for all Unity skills. Load specific references by domain.

## Code Standards

### C# Standards
- `csharp-hygiene.md` — Nullable refs, access modifiers, naming, sealed/readonly, dispose, strings
- `csharp-modern.md` — Expression-bodied, pattern matching, records, namespaces, Span
- `csharp-linq.md` — Core LINQ operations, chaining, materialization, anti-patterns
- `csharp-perf.md` — Cache allocations, string optimizations, struct vs class, ArrayPool

### Unity
- `unitask.md` — UniTask async patterns, cancellation, waiting, error handling, cheat sheet

### Patterns & Templates
- `template.md` — Starting template for new scripts
- `patterns-service.md` — Service, state, view patterns
- `patterns-async-state.md` — Async, state machine, SO config, cleanup

### Review Checklists
7 review checklist files loaded directly by review skills: `review-architecture-patterns.md`, `review-csharp.md`, `review-deep-workflow.md`, `review-gates.md`, `review-logic-data.md`, `review-perf.md`, `review-unity.md`

## Review Code
- `common-rules.md` — Common review rules

## Plan Pipeline
- `costing-and-types.md` — Cost/type definitions
- `investigation-checklist.md` — Pre-plan investigation checklist
- `prometheus-pipeline.md` — Pipeline flow reference

## Debug
- `common-fixes.md` — Frequent Unity error fixes

## Scripts — `scripts/`
- `plan/investigate_feature.py` — Automated investigation script
- `investigate/trace_logic.py` — Logic tracing script
- `investigate/trace_unified.py` — Unified trace script
- `review/post_review.py` — GitHub API review posting
