---
type: reference
name: Skill Integration
description: How unity-refactor integrates with unity-investigate and unity-test skills.
---

# Skill Integration Guide

## Workflow

```
Phase 1: Analyze ──── User requirements + scope
Phase 2: Investigate ── unity-investigate → deep code analysis
Phase 3: Refactor ───── unity-code-deep patterns → execute changes
Phase 4: Verify ─────── unity-test → run/create tests
```

## unity-investigate Integration

Invoke at Phase 2 start to understand code before changing it.

| Investigation Type | Use For |
|---|---|
| Logic Flow | Tracing call chains before extracting methods |
| Data Structures | Understanding serialization before restructuring |
| Resource Management | Mapping asset loading before splitting code |
| Performance | Profiling hot paths before optimization |

**Use investigation output for**: Architecture → target design, Dependencies → ripple effects, Code smells → prioritization, Entry points → characterization tests, Side effects → preservation.

## unity-test Integration

Invoke at two points:
1. **Phase 2** (pre-refactor): Write characterization tests locking existing behavior
2. **Phase 4** (post-refactor): New tests + run all to verify

**Pre-refactor**: Identify public API → write tests (happy path, edge cases, errors) → verify all pass → safety net established.

**Post-refactor**: Run characterization tests (must pass) → write new tests for extracted classes/interfaces → full suite → check coverage.

## Tool Reference

### LSP Tools
| Tool | Use |
|---|---|
| `lsp_goto_definition` | Find definition before renaming |
| `lsp_find_references` | Find ALL callers before changing signatures |
| `lsp_symbols` | List class members |
| `lsp_prepare_rename` / `lsp_rename` | Safe workspace-wide rename |
| `lsp_diagnostics` | Verify no errors after changes |

### Code Search
`grep` (string patterns), `ast_grep_search/replace` (structural patterns), `glob` (related files)

### MCP Tools
`check_compile_errors`, `get_unity_logs`, `run_tests`, `get_test_job`, `validate_script`

### Validation Scripts
`validate_refactoring.py` (after Phase 3), `check_test_coverage.py` (after Phase 4)
