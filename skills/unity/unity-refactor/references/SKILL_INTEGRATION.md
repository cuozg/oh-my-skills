---
type: reference
name: Skill Integration
description: How unity-refactor integrates with unity-investigate and unity-test skills.
---

# Skill Integration Guide

## Table of Contents

1. [Integration Overview](#integration-overview)
2. [unity-investigate Integration](#unity-investigate-integration)
3. [unity-test Integration](#unity-test-integration)
4. [Tool Reference](#tool-reference)

---

## Integration Overview

```
┌─────────────────────────────────────────────────────────┐
│                   unity-refactor                        │
│                (Orchestrator Skill)                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Phase 1: Analyze ────────────────────────────────────  │
│     └─ User requirements + scope definition             │
│                                                         │
│  Phase 2: Investigate ────── unity-investigate ───────  │
│     └─ Deep code analysis, dependency mapping           │
│                                                         │
│  Phase 3: Refactor ──────── unity-code patterns ──────  │
│     └─ Execute changes with safety checks               │
│                                                         │
│  Phase 4: Verify ────────── unity-test ───────────────  │
│     └─ Run/create tests, validate behavior              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## unity-investigate Integration

### When to Invoke

Invoke investigation at the start of Phase 2 to understand the code before changing it.

### What to Request

| Investigation Type | Use For |
|:---|:---|
| Logic Flow | Tracing call chains before extracting methods |
| Data Structures | Understanding serialization before restructuring |
| Resource Management | Mapping asset loading before moving/splitting code |
| Performance | Profiling hot paths before optimization refactoring |

### How to Use Investigation Output

1. **Architecture diagrams** → Inform target architecture in refactoring plan
2. **Dependencies map** → Identify ripple effects of changes
3. **Code smells** → Prioritize which refactorings to apply
4. **Entry points** → Know where to add characterization tests
5. **Side effects** → Ensure refactoring preserves all effects

### Investigation Workflow Integration

```
1. Define refactoring scope (from user request)
2. Run unity-investigate on target code:
   - trace_logic.sh for reference mapping
   - LSP tools for call graph
   - grep/glob for asset references
3. Extract from investigation report:
   - §3 Architecture → current state diagram
   - §5 Logic Deep-Dive → methods to refactor
   - §9 Dependencies → impact assessment
   - §10 Risks → refactoring risks
4. Feed findings into REFACTORING_PLAN.md §3
```

---

## unity-test Integration

### When to Invoke

Invoke testing at two points:
1. **Phase 2** (pre-refactor): Write characterization tests to lock existing behavior
2. **Phase 4** (post-refactor): Write new tests + run all tests to verify

### Pre-Refactor Testing

Create characterization tests that document existing behavior WITHOUT changing it:

1. Identify public API surface of target code
2. Write tests covering: happy path, edge cases, error conditions
3. Verify all characterization tests pass against current code
4. These tests become the safety net for refactoring

### Post-Refactor Testing

After refactoring is complete:

1. Run all characterization tests — must still pass
2. Write new tests for refactored structure:
   - New classes/methods extracted
   - Changed interfaces
   - New injection points
3. Run full test suite
4. Check test coverage with `check_test_coverage.py`

### Testing Workflow Integration

```
Pre-Refactor:
1. Use unity-test Step 1 (Analyze) on target code
2. Use unity-test Step 2 (Investigate) — already done via unity-investigate
3. Use unity-test Step 3 (Generate) — characterization tests only
4. Run tests → all must pass

Post-Refactor:
1. Run characterization tests → verify no regression
2. Use unity-test Step 3 (Generate) — new tests for refactored code
3. Run all tests → verify complete coverage
4. Run check_test_coverage.py → validate coverage metrics
```

---

## Tool Reference

### LSP Tools (Code Navigation)

| Tool | Use In Refactoring |
|:---|:---|
| `lsp_goto_definition` | Find where a method/class is defined before renaming |
| `lsp_find_references` | Find ALL callers before changing signatures |
| `lsp_symbols` | List class members to understand structure |
| `lsp_prepare_rename` | Check if a rename is safe |
| `lsp_rename` | Execute workspace-wide rename |
| `lsp_diagnostics` | Verify no errors after each change |

### Code Search Tools

| Tool | Use In Refactoring |
|:---|:---|
| `grep` | Find string patterns (string refs, hardcoded values) |
| `ast_grep_search` | Find structural code patterns (anti-patterns) |
| `ast_grep_replace` | Structural search-and-replace across files |
| `glob` | Find related files (prefabs, configs, tests) |

### MCP Tools (Unity Editor)

| Tool | Use In Refactoring |
|:---|:---|
| `unityMCP_check_compile_errors` | Verify compilation after changes |
| `unityMCP_get_unity_logs` | Check for runtime errors |
| `unityMCP_run_tests` | Execute test suite |
| `unityMCP_get_test_job` | Poll test results |
| `unityMCP_validate_script` | Validate script structure |

### Validation Scripts

| Script | When to Run |
|:---|:---|
| `validate_refactoring.py` | After Phase 3 (refactoring execution) |
| `check_test_coverage.py` | After Phase 4 (verification) |
