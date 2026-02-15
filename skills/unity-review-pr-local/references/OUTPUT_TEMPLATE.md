# Output Template Specification

## Output Location

`Documents/Reviews/PR_<number>_review.md` or `Documents/Reviews/<branch_name>_review.md`

## Template

```markdown
# PR Review: #<number> - <title>

**Date**: YYYY-MM-DD HH:MM
**Branch**: <source_branch> → <target_branch>
**Reviewer**: Claude
**Verdict**: APPROVE | COMMENT | REQUEST_CHANGES

---

## Summary
<One paragraph overall assessment>

## Statistics
| Severity | Count |
|----------|-------|
| 🔴 Critical | X |
| 🟡 Major | Y |
| 🔵 Minor | Z |
| 💚 Suggestion | N |

**Files Changed**: X | **Lines**: +Y / -Z

## Findings

### 🔴 Critical Issues
#### [FileName.cs:L42](file:///path/FileName.cs#L42)
**Issue**: Description. **Why**: Impact.
```suggestion
fixedCode();
```

### 🟡 Major Issues
#### [FileName.cs:L100](file:///path/FileName.cs#L100)
**Issue**: Description.

### 🔵 Minor Issues
#### [FileName.cs:L200](file:///path/FileName.cs#L200)
**Issue**: Description.

### 💚 Suggestions
#### [FileName.cs:L300](file:///path/FileName.cs#L300)
**Suggestion**: Description.

## Files Reviewed
| File | Status | Issues |
|------|--------|--------|
| [File1.cs](file:///path) | Modified | 🔴 1, 🟡 2 |

## Verdict Rationale
**Verdict**: REQUEST_CHANGES
1. Critical issue X
2. Major concern Y
```

## Verdict Rules

| Condition | Verdict |
|---|---|
| Any 🔴 Critical | REQUEST_CHANGES |
| 🟡 Major only | REQUEST_CHANGES or COMMENT |
| Only 🔵/💚 | COMMENT |
| No issues | APPROVE |
