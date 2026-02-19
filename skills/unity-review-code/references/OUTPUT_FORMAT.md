# Output Format

Review report template. Output to `Documents/Reviews/<identifier>_review.md`.

## Identifier Naming

| Input | Filename |
|:------|:---------|
| Uncommitted changes | `uncommitted_YYYYMMDD_review.md` |
| Branch name | `<branch_name>_review.md` (slashes → underscores) |
| Task/ticket ID | `<ticket>_review.md` |

## Template

```markdown
# Code Review: <identifier>

**Date**: YYYY-MM-DD HH:MM
**Branch**: <current_branch>
**Reviewer**: AI Pre-Commit Review
**Verdict**: ✅ CLEAN | ✅ READY | ⚠️ NEEDS WORK | ❌ NOT READY

---

## Summary

<One paragraph: what was changed, overall quality assessment, key concerns if any.>

## Statistics

| Severity | Count |
|:---------|:------|
| 🔴 Critical | X |
| 🟡 Major | Y |
| 🔵 Minor | Z |
| 💚 Suggestion | N |

**Files Changed**: X | **Lines**: +Y / -Z

## Findings

### 🔴 Critical Issues

#### [FileName.cs:L42](file:///absolute/path/FileName.cs#L42)
**Issue**: Description of the problem.
**Evidence**: Caller count, affected files, grep results.
**Why**: Impact — what breaks, what data is lost, what crashes.
```suggestion
fixedCode();
```

### 🟡 Major Issues

#### [FileName.cs:L100](file:///absolute/path/FileName.cs#L100)
**Issue**: Description.
**Evidence**: Trigger conditions, affected paths.
**Why**: Impact.
```suggestion
fixedCode();
```

### 🔵 Minor Issues

#### [FileName.cs:L200](file:///absolute/path/FileName.cs#L200)
**Issue**: Description.
```suggestion
fixedCode();
```

### 💚 Suggestions

#### [FileName.cs:L300](file:///absolute/path/FileName.cs#L300)
**Suggestion**: Description of improvement.
```suggestion
improvedCode();
```

## Verification

- **Compile**: ✅/❌ [evidence]
- **Tests**: ✅/❌/⚠️ [evidence]
- **Diff check**: ✅/⚠️ [evidence]
- **Asset integrity**: ✅/❌ [evidence] (if applicable)

## Files Reviewed

| File | Status | Issues |
|:-----|:-------|:-------|
| File1.cs | Modified | 🔴 1, 🟡 2 |
| File2.prefab | Added | 💚 1 |

## Verdict Rationale

**Verdict**: [VERDICT]

1. [Primary reason]
2. [Secondary reason]

### Action Items (if not CLEAN)
- [ ] Fix: [Critical issue description]
- [ ] Fix: [Major issue description]
- [ ] Consider: [Minor/suggestion description]
```

## Verdict Rules

| Condition | Verdict |
|:----------|:--------|
| Any 🔴 Critical | ❌ **NOT READY** — must fix before commit |
| 🟡 Major only | ⚠️ **NEEDS WORK** — fix or justify |
| Only 🔵/💚 | ✅ **READY** — safe to commit |
| No issues + verification passes | ✅ **CLEAN** — commit |

## Batch Pattern

When the same issue appears in multiple files, write full explanation on the **first** occurrence, then short references on subsequent files:

```markdown
#### [Second.cs:L55](file:///path/Second.cs#L55)
**Same issue as First.cs:L42** — cache GetComponent in Awake.
```suggestion
private Rigidbody _rb;
void Awake() => _rb = GetComponent<Rigidbody>();
```
```

## Finding Quality Rules

- **DO**: One issue per finding. Show evidence (caller count, file:line, grep results). Explain *why*, not just *what*. Provide exact replacement code.
- **DON'T**: Combine multiple fixes in one finding. Flag style-only as 🔴/🟡. Flag without evidence. Suggest rewrites > 20 lines inline (use `<details>` block for large changes).
