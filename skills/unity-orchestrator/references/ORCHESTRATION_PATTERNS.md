# Orchestration Patterns

Coordination patterns for complex Unity development tasks.

## 1. Feature Implementation Pipeline

Full pipeline for large features:

```
unity-plan          → High-level roadmap, epics, costing
       ↓
unity-plan-brainstorm → Critique, refine with user, finalize tasks
       ↓
unity-plan-tasks   → Create task skeletons in Documents/Tasks/
       ↓
unity-task-brainstorm → Code-level investigation, specific changes
       ↓
unity-task-executor → Implement using specialists
```

**When to use full pipeline:** Complex features with unknown scope, multiple systems involved, or significant architectural decisions.

**Shortcut for medium tasks:** Skip directly to `unity-task-brainstorm` → `unity-task-executor`.

## 2. Debug-Fix-Verify Loop

```
unity-fix-errors    → Diagnose from console/stack trace
       ↓
[Can't find cause?]
       ↓
unity-investigate-code → Trace execution, find root cause
       ↓
unity-implement-logic  → Apply targeted fix
       ↓
unity-test          → Verify fix, add regression test
```

**Alternative entry point:** If user describes unexpected behavior without errors, start with `unity-debug` for strategic investigation.

## 3. Documentation Flow

```
[Feature complete?]
       ↓
unity-write-docs    → Architecture docs, README updates
       +
mermaid            → Flow diagrams, component maps
       ↓
[Need formal spec?]
       ↓
unity-write-tdd    → Technical Design Document
```

## 4. Platform-Specific Implementation

```
unity-implement-logic → Core feature logic
       +
unity-mobile-deploy   → Mobile adaptations (iOS/Android)
       OR
unity-web-deploy      → WebGL adaptations
       ↓
unity-optimize-performance → Platform-specific optimization
```

## 5. Editor Tooling Flow

```
unity-editor-tools → Custom window/inspector design
       +
unity-mcp-basics   → unityMCP automation integration
       ↓
unity-test         → Editor test coverage
```

## 6. Tech Lead Findings Template

Use for high-level project analysis:

```markdown
## Current State
- Summary of codebase and relevant assets
- Existing patterns and conventions

## Architectural Risks
- Performance concerns
- Technical debt
- Platform limitations

## Task Route
| Task | Skill | Notes |
|:-----|:------|:------|
| [Task 1] | `skill-name` | Brief context |
| [Task 2] | `skill-name` | Brief context |

## Definition of Done
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Tests pass
```

## 7. Cross-Cutting Verification

After any implementation, verify:

| Concern | Check With |
|:--------|:-----------|
| No new errors | `unity-fix-errors` (console scan) |
| Performance acceptable | `unity-optimize-performance` (quick audit) |
| Tests pass | `unity-test` (run existing suite) |
| Code quality | `unity-review-pr` (self-review) |

## 8. Skill Chaining Signals

When a skill recommends chaining:

| Signal | Chain To |
|:-------|:---------|
| "Root cause unclear" | `unity-investigate-code` |
| "Need architectural decision" | `unity-plan` or `unity-write-tdd` |
| "Performance concern identified" | `unity-optimize-performance` |
| "Platform-specific behavior" | `unity-mobile-deploy` or `unity-web-deploy` |
| "Missing test coverage" | `unity-test` |
| "Documentation needed" | `unity-write-docs` + `mermaid` |
