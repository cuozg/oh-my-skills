# Output Template Specification

The `unity-review-pr-local` skill generates a markdown file for local review storage.

## Output Location

`Documents/Reviews/PR_<number>_review.md`

For local branches without PR: `Documents/Reviews/<branch_name>_review.md`

## Full Template

```markdown
# PR Review: #<number> - <title>

**Date**: YYYY-MM-DD HH:MM
**Branch**: <source_branch> → <target_branch>
**Reviewer**: Claude
**Verdict**: APPROVE | COMMENT | REQUEST_CHANGES

---

## Summary

<One paragraph overall assessment of the changes>

---

## Statistics

| Severity | Count |
|----------|-------|
| 🔴 Critical | X |
| 🟡 Major | Y |
| 🔵 Minor | Z |
| 💚 Suggestion | N |

**Files Changed**: X
**Lines Added**: +Y
**Lines Removed**: -Z

---

## Findings

### 🔴 Critical Issues

> Issues that must be fixed before merge. These cause crashes, memory leaks, or game-breaking bugs.

#### [FileName.cs:L42](file:///absolute/path/to/FileName.cs#L42)

**Issue**: Clear description of the problem.

**Why it matters**: Explanation of the impact.

```csharp
// Current code
problematicCode();
```

```suggestion
// Suggested fix
fixedCode();
```

---

### 🟡 Major Issues

> Significant issues that should be addressed. Architectural problems, performance concerns in hot paths.

#### [FileName.cs:L100](file:///absolute/path/to/FileName.cs#L100)

**Issue**: Description

```suggestion
// Fix
```

---

### 🔵 Minor Issues

> Style violations, naming inconsistencies, documentation gaps.

#### [FileName.cs:L200](file:///absolute/path/to/FileName.cs#L200)

**Issue**: Naming doesn't follow conventions.

```suggestion
// Preferred naming
```

---

### 💚 Suggestions

> Optional improvements for better code quality.

#### [FileName.cs:L300](file:///absolute/path/to/FileName.cs#L300)

**Suggestion**: Consider using modern C# pattern.

```suggestion
// Modern approach
```

---

## Files Reviewed

| File | Status | Issues |
|------|--------|--------|
| [File1.cs](file:///path/File1.cs) | Modified | 🔴 1, 🟡 2 |
| [File2.cs](file:///path/File2.cs) | Added | 💚 1 |
| [File3.cs](file:///path/File3.cs) | Deleted | — |

---

## Verdict Rationale

**Verdict**: REQUEST_CHANGES

This PR requires changes because:
1. Critical issue X needs to be addressed
2. Major performance concern in Y

Once these are fixed, the PR is ready for merge.
```

## Field Descriptions

| Field | Description |
|-------|-------------|
| `number` | PR number (or "LOCAL" for local branches) |
| `title` | PR title or commit message summary |
| `date` | Review timestamp |
| `branch` | Source and target branch names |
| `verdict` | APPROVE, COMMENT, or REQUEST_CHANGES |

## Verdict Rules

| Condition | Verdict |
|-----------|---------|
| Any 🔴 Critical | REQUEST_CHANGES |
| 🟡 Major but no 🔴 | REQUEST_CHANGES or COMMENT (use judgment) |
| Only 🔵/💚 | COMMENT |
| No issues | APPROVE |
