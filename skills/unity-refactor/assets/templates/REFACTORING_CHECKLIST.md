---
type: template
name: Refactoring Checklist
description: Step-by-step checklist for executing and verifying a Unity refactoring task.
---

# Refactoring Checklist: [Subject Name]

**Plan Reference**: `Documents/Refactorings/REFACTORING_PLAN_[Subject]_[Date].md`
**Started**: [YYYY-MM-DD]
**Completed**: [YYYY-MM-DD]

---

## Phase 1: Pre-Flight

- [ ] Refactoring plan reviewed and approved
- [ ] Working branch created (`refactor/[subject-name]`)
- [ ] All existing tests pass before changes
- [ ] No compiler errors or warnings
- [ ] Dependencies mapped (who calls what)
- [ ] Backup/commit point established

---

## Phase 2: Safety Net

- [ ] Write characterization tests for existing behavior
- [ ] Verify characterization tests pass against current code
- [ ] Document observable behavior (inputs → outputs)
- [ ] Identify all callers of code being refactored

### Characterization Tests Created

| Test File | Tests | Status |
|:---|:---|:---|
| `Test/EditMode/[Name]Tests.cs` | [count] | Pass/Fail |

---

## Phase 3: Refactoring Execution

Execute changes in small, compilable steps. After EACH step:
1. Compile — fix any errors immediately
2. Run tests — ensure nothing broke
3. Commit — create a checkpoint

### Step Log

| # | Change Description | Compiles | Tests Pass | Committed |
|:---|:---|:---|:---|:---|
| 1 | [Description] | [ ] | [ ] | [ ] |
| 2 | [Description] | [ ] | [ ] | [ ] |
| 3 | [Description] | [ ] | [ ] | [ ] |

---

## Phase 4: Verification

### 4.1 Compilation
- [ ] Zero compiler errors
- [ ] Zero new compiler warnings
- [ ] No suppressed warnings (`#pragma warning disable`)

### 4.2 Test Results
- [ ] All pre-existing tests pass
- [ ] Characterization tests pass
- [ ] New tests for refactored code pass
- [ ] No test execution order dependencies

### 4.3 Behavior Regression
- [ ] All documented behaviors preserved
- [ ] No unintended side effects
- [ ] Public API unchanged (or changes documented)

### 4.4 Code Quality
- [ ] No code smells introduced
- [ ] Naming follows project conventions
- [ ] No dead code left behind
- [ ] No TODO/HACK comments without tracking

### 4.5 Performance
- [ ] No new per-frame allocations
- [ ] No boxing/unboxing introduced
- [ ] No LINQ in hot paths (Update/FixedUpdate)
- [ ] No string concatenation in loops

---

## Phase 5: Cleanup

- [ ] Remove any temporary scaffolding code
- [ ] Delete obsolete files
- [ ] Update `.meta` files tracked correctly
- [ ] Verify prefab/scene references not broken
- [ ] Run `validate_refactoring.py` — all checks pass
- [ ] Run `check_test_coverage.py` — coverage adequate

---

## Final Sign-Off

- [ ] All phases complete
- [ ] Changes ready for code review
- [ ] Refactoring plan updated with actual outcomes
- [ ] Summary of changes documented

### Summary

**Files Modified**: [count]
**Files Created**: [count]
**Files Deleted**: [count]
**Tests Added**: [count]
**Total Test Count**: [count]
