---
name: unity-refactor
description: "Unity Refactoring Expert. Orchestrate investigation, safe code transformation, and verification for Unity C# codebases. Use when: (1) Extracting methods, classes, or interfaces, (2) Renaming symbols across the project, (3) Restructuring MonoBehaviour hierarchies, (4) Simplifying complex logic or deep nesting, (5) Reducing coupling between systems, (6) Replacing anti-patterns (Singleton, polling, magic numbers), (7) Moving code between files or namespaces, (8) Cleaning up dead code or obsolete patterns, (9) Performance-oriented refactoring (GC, Update, allocations). Triggers: 'refactor', 'restructure', 'extract', 'rename', 'simplify', 'clean up', 'reduce coupling', 'decouple', 'split class', 'move method', 'remove dead code', 'replace singleton'."
---

# Unity Refactoring Expert

**Input**: Code to refactor (files/classes/methods) and goal (readability, decouple, performance, etc.)
**Output**: REFACTORING_PLAN + REFACTORING_CHECKLIST in `Documents/Refactorings/`, plus refactored code compiling cleanly

## Workflow Overview

```
Phase 1: Analyze     → Define scope, identify patterns, assess risk
Phase 2: Investigate → Deep code analysis via unity-investigate
Phase 3: Refactor    → Execute changes in small, compilable steps
Phase 4: Verify      → Tests pass, compilation clean, behavior preserved
```

## Phase 1: Analyze

1. **Clarify scope** — what code, what motivation, constraints?
2. **Identify patterns** — consult `references/REFACTORING_PATTERNS.md`, match smell to pattern
3. **Assess risk**:
   - Low: rename, extract method, constants
   - Medium: extract class, introduce interface
   - High: replace inheritance, change architecture
   - Critical: change serialization, public API, data format
4. **Populate** REFACTORING_PLAN.md §1-2

## Phase 2: Investigate

1. **Map code** via `lsp_find_references`, `lsp_goto_definition`, `lsp_symbols`, `ast_grep_search`
2. **Map dependencies** — callers, downstream deps, asset references, existing tests
3. **Write characterization tests** — lock current behavior (use `unity-test` patterns)
4. **Populate** REFACTORING_PLAN.md §3, §5

## Phase 3: Refactor

### Execution Rules
- **One step at a time** — each must compile and pass tests
- Use `lsp_rename` for symbol renames, `ast_grep_replace` for patterns
- After each step: `lsp_diagnostics` → `unityMCP_check_compile_errors` → run tests

### What NOT to Do
- Never change behavior while refactoring
- Never skip compilation checks between steps
- Never refactor and add features simultaneously
- Never delete failing tests — fix them
- Never suppress warnings with `#pragma warning disable`

Consult `references/REFACTORING_PATTERNS.md` for before/after examples of: Extract Method/Class, Replace Inheritance with Composition, Introduce Interface, Replace Singleton with DI, Flatten Deep Nesting, and more.

## Phase 4: Verify

1. `unityMCP_check_compile_errors` → zero errors
2. `lsp_diagnostics` on ALL changed files → zero errors/warnings
3. All characterization tests pass
4. Write new tests for refactored structure
5. Run validation scripts:
   ```bash
   python .opencode/skills/unity/unity-refactor/scripts/validate_refactoring.py --git-diff
   python .opencode/skills/unity/unity-refactor/scripts/check_test_coverage.py <source-dir> <test-dir>
   ```
6. Verify public API unchanged, no unintended side effects
7. Complete REFACTORING_CHECKLIST.md (all phases)

## Completion Criteria

- [ ] REFACTORING_PLAN.md fully populated
- [ ] REFACTORING_CHECKLIST.md all phases checked
- [ ] Zero compiler errors, all tests pass
- [ ] `validate_refactoring.py` reports no issues
- [ ] No dead code, no untracked TODO/HACK markers

## Output Documents

Read templates, save populated versions to `Documents/Refactorings/`:
1. `assets/templates/REFACTORING_PLAN.md` → `REFACTORING_PLAN_[Subject]_[YYYYMMDD].md`
2. `assets/templates/REFACTORING_CHECKLIST.md` → `REFACTORING_CHECKLIST_[Subject]_[YYYYMMDD].md`

## Skill Integration

| Skill | When |
|:---|:---|
| `unity-investigate` | Phase 2 — deep code analysis |
| `unity-test` | Phase 2 (characterization) + Phase 4 (new tests) |
| `unity-code` | Phase 3 — implementation patterns |
| `unity-fix-errors` | Compilation errors during refactoring |

## References

- `references/REFACTORING_PATTERNS.md` — 13 Unity refactoring patterns with code
- `references/SKILL_INTEGRATION.md` — Integration workflows
