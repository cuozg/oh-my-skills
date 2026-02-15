---
type: template
name: Refactoring Checklist
description: Step-by-step checklist for executing and verifying a Unity refactoring task.
---

# Refactoring Checklist: [Subject Name]

**Plan**: `Documents/Refactorings/REFACTORING_PLAN_[Subject]_[Date].md`
**Started**: [YYYY-MM-DD] | **Completed**: [YYYY-MM-DD]

---

## Phase 1: Pre-Flight
- [ ] Plan reviewed, branch created (`refactor/[subject]`)
- [ ] All tests pass, no compiler errors
- [ ] Dependencies mapped, backup commit established

## Phase 2: Safety Net
- [ ] Characterization tests written for existing behavior
- [ ] All characterization tests pass, observable behavior documented

| Test File | Tests | Status |
|:---|:---|:---|
| `Test/EditMode/[Name]Tests.cs` | [count] | Pass/Fail |

## Phase 3: Execution

After EACH step: Compile → Run tests → Commit

| # | Change | Compiles | Tests Pass | Committed |
|:---|:---|:---|:---|:---|
| 1 | [Description] | [ ] | [ ] | [ ] |

## Phase 4: Verification

- [ ] Zero compiler errors/warnings (no `#pragma` suppression)
- [ ] All pre-existing + characterization + new tests pass
- [ ] All documented behaviors preserved, public API unchanged
- [ ] No code smells, dead code, or TODO/HACK without tracking
- [ ] No new per-frame allocations, boxing, LINQ in hot paths, string concat in loops

## Phase 5: Cleanup
- [ ] Temporary code removed, obsolete files deleted
- [ ] `.meta` files tracked, prefab/scene references intact
- [ ] `validate_refactoring.py` + `check_test_coverage.py` pass

## Final Sign-Off
- [ ] All phases complete, ready for review
- [ ] Plan updated with outcomes

**Files**: Modified [n] | Created [n] | Deleted [n] | **Tests Added**: [n]
