---
name: unity-refactor
description: "Unity Refactoring Expert. Orchestrate investigation, safe code transformation, and verification for Unity C# codebases. Use when: (1) Extracting methods, classes, or interfaces, (2) Renaming symbols across the project, (3) Restructuring MonoBehaviour hierarchies, (4) Simplifying complex logic or deep nesting, (5) Reducing coupling between systems, (6) Replacing anti-patterns (Singleton, polling, magic numbers), (7) Moving code between files or namespaces, (8) Cleaning up dead code or obsolete patterns, (9) Performance-oriented refactoring (GC, Update, allocations). Triggers: 'refactor', 'restructure', 'extract', 'rename', 'simplify', 'clean up', 'reduce coupling', 'decouple', 'split class', 'move method', 'remove dead code', 'replace singleton'."
---

# Unity Refactoring Expert

Safe, verified refactoring of Unity C# code — from analysis through execution to verification.

## Purpose

Improve Unity C# code structure — readability, testability, performance, or architecture — without changing external behavior, using small verified steps.

## Input

- **Required**: Code to refactor (files, classes, or methods) and the refactoring goal (readability, decouple, performance, etc.)
- **Optional**: Constraints (preserve public API, backward compatibility), target architecture pattern

## Output

Two documents saved to `Documents/Refactorings/`:
1. `REFACTORING_PLAN_[Subject]_[YYYYMMDD].md` — scope, risk, investigation findings, step plan
2. `REFACTORING_CHECKLIST_[Subject]_[YYYYMMDD].md` — execution tracking across all 5 phases

Plus the refactored code itself, compiling cleanly with all tests passing.

## Examples

| User Request | Skill Action |
|:---|:---|
| "Extract the damage calculation into its own class" | Investigate callers via LSP, write characterization tests, extract to `DamageCalculator`, verify compilation + tests |
| "Replace the AudioManager singleton with DI" | Map all `AudioManager.Instance` refs, introduce `IAudioService` interface, inject via constructor, update callers |
| "Reduce nesting in `EnemyAI.UpdateBehavior()`" | Flatten 5-level nesting with guard clauses and extracted methods, verify behavior unchanged |

## Output Requirement (MANDATORY)

**Every refactoring MUST produce two documents**:

1. Read `assets/templates/REFACTORING_PLAN.md` → populate before starting changes
2. Read `assets/templates/REFACTORING_CHECKLIST.md` → track execution progress

Save outputs to:
- `Documents/Refactorings/REFACTORING_PLAN_[Subject]_[YYYYMMDD].md`
- `Documents/Refactorings/REFACTORING_CHECKLIST_[Subject]_[YYYYMMDD].md`

## Workflow Overview

```
Phase 1: Analyze     → Define scope, identify patterns, assess risk
Phase 2: Investigate → Deep code analysis via unity-investigate
Phase 3: Refactor    → Execute changes in small, compilable steps
Phase 4: Verify      → Run tests, validate scripts, confirm behavior
```

---

## Phase 1: Analyze

Define what to refactor, why, and how.

1. **Clarify scope** with the user:
   - What code needs refactoring? (files, classes, methods)
   - What is the motivation? (readability, performance, testability, architecture)
   - Are there constraints? (can't change public API, must keep backward compat)

2. **Identify applicable refactoring patterns** — consult `references/REFACTORING_PATTERNS.md`:
   - Match the code smell to a known pattern
   - If multiple patterns apply, prioritize by risk (lowest first)

3. **Assess risk level**:

   | Risk | Criteria |
   |:---|:---|
   | Low | Rename, extract method, constants — no behavior change |
   | Medium | Extract class, introduce interface — structural change |
   | High | Replace inheritance, change architecture — cross-cutting |
   | Critical | Change serialization, public API, data format |

4. **Populate REFACTORING_PLAN.md** §1 (Summary) and §2 (Scope)

---

## Phase 2: Investigate

Understand the code deeply before changing it. Use `unity-investigate` skill.

1. **Run investigation on target code**:
   - Use `lsp_find_references` to map all callers of code being refactored
   - Use `lsp_goto_definition` to trace dependencies
   - Use `lsp_symbols` to list class members and structure
   - Use `ast_grep_search` to find structural patterns and anti-patterns
   - Use `grep`/`glob` to find related prefabs, configs, and assets

2. **Map dependencies**:
   - Who calls this code? (upstream callers)
   - What does this code call? (downstream dependencies)
   - What assets reference it? (prefabs, ScriptableObjects, scenes)
   - What tests exist? (existing coverage)

3. **Write characterization tests** (pre-refactor safety net):
   - Use `unity-test` skill patterns to write tests locking current behavior
   - Cover: happy path, edge cases, error conditions
   - Run tests — all must pass before proceeding
   - Record in REFACTORING_CHECKLIST.md Phase 2

4. **Populate REFACTORING_PLAN.md** §3 (Investigation Findings) and §5 (Risk Assessment)

### MCP Tools for Investigation

| Operation | Tool |
|:---|:---|
| Check compilation | `unityMCP_check_compile_errors` |
| Scene hierarchy | `unityMCP_list_game_objects_in_hierarchy` |
| Object inspection | `unityMCP_get_game_object_info` |
| Console logs | `unityMCP_get_unity_logs` |

---

## Phase 3: Refactor

Execute changes in small, compilable steps. **Never make large, sweeping changes.**

### Execution Rules

1. **One refactoring step at a time** — each step must compile and pass tests
2. **Commit after each step** (if user has requested commits)
3. **Use LSP-powered refactoring** when available:
   - `lsp_rename` for symbol renames (workspace-wide, safe)
   - `lsp_prepare_rename` to validate rename is possible first
   - `ast_grep_replace` for structural pattern replacement
4. **Verify after each step**:
   - `lsp_diagnostics` on changed files → zero errors
   - `unityMCP_check_compile_errors` → clean compilation
   - Run relevant tests → still passing

### Refactoring Step Sequence

For each change in the plan:

```
1. Identify the smallest atomic change
2. Apply the change (edit, rename, move)
3. Run lsp_diagnostics on changed files
4. Run unityMCP_check_compile_errors
5. Run affected tests if available
6. Log in REFACTORING_CHECKLIST.md Phase 3 Step Log
7. Proceed to next change
```

### Pattern-Specific Guidance

Consult `references/REFACTORING_PATTERNS.md` for before/after examples of:
- Extract Method/Class
- Replace Inheritance with Composition
- Introduce Interface
- Replace Singleton with DI
- Consolidate Event Handling
- Replace Magic Numbers
- Extract ScriptableObject Config
- Replace Coroutine with Async
- Object Pool Extraction
- Reduce MonoBehaviour Bloat
- Flatten Deep Nesting

### What NOT to Do

- **Never** change behavior while refactoring — structure only
- **Never** skip compilation checks between steps
- **Never** refactor and add features simultaneously
- **Never** delete tests that fail due to refactoring — fix them
- **Never** suppress warnings with `#pragma warning disable`
- **Never** use unsafe casts (`dynamic`, unguarded casts)

---

## Phase 4: Verify

Confirm the refactoring preserved behavior and improved code quality.

### 4.1 Compilation Check

```
1. unityMCP_check_compile_errors → zero errors
2. lsp_diagnostics on ALL changed files → zero errors, zero new warnings
```

### 4.2 Test Verification

```
1. Run all characterization tests (from Phase 2) → must pass
2. Write new tests for refactored structure using unity-test patterns:
   - New classes/methods extracted
   - Changed interfaces or injection points
   - New composition/strategy patterns
3. Run full test suite → all pass
```

### 4.3 Run Validation Scripts

```bash
# Check for anti-patterns and code quality issues
python .opencode/skills/unity-refactor/scripts/validate_refactoring.py <path-to-changed-files>

# Or check only git-changed files
python .opencode/skills/unity-refactor/scripts/validate_refactoring.py --git-diff

# Check test coverage for refactored code
python .opencode/skills/unity-refactor/scripts/check_test_coverage.py <source-dir> <test-dir>

# Or check a single file
python .opencode/skills/unity-refactor/scripts/check_test_coverage.py \
  --source <file.cs> --test-dir <test-dir>
```

### 4.4 Behavior Regression Check

- Verify all documented behaviors from Phase 2 still work
- Check public API is unchanged (or changes are documented)
- Verify no unintended side effects

### 4.5 Complete Checklist

Fill remaining sections of `REFACTORING_CHECKLIST.md`:
- Phase 4 (Verification) — all checkboxes
- Phase 5 (Cleanup) — remove scaffolding, dead code
- Final Sign-Off — file counts, test counts, summary

---

## Completion Criteria

A refactoring is complete when:

- [ ] REFACTORING_PLAN.md fully populated
- [ ] REFACTORING_CHECKLIST.md all phases checked
- [ ] Zero compiler errors
- [ ] All pre-existing tests pass
- [ ] New tests cover refactored code
- [ ] `validate_refactoring.py` reports no issues
- [ ] `check_test_coverage.py` meets threshold
- [ ] No dead code left behind
- [ ] No TODO/HACK markers without tracking

---

## Skill Integration

| Skill | When to Use |
|:---|:---|
| `unity-investigate` | Phase 2 — deep code analysis before refactoring |
| `unity-test` | Phase 2 (characterization tests) and Phase 4 (new tests) |
| `unity-code` | Phase 3 — implementation patterns for refactored code |
| `unity-fix-errors` | When refactoring introduces compilation errors |
| `unity-debug` | When refactoring causes runtime behavior changes |

See `references/SKILL_INTEGRATION.md` for detailed integration workflows.

## References

- `references/REFACTORING_PATTERNS.md` — 13 common Unity refactoring patterns with code examples
- `references/SKILL_INTEGRATION.md` — Detailed integration guide for unity-investigate and unity-test
