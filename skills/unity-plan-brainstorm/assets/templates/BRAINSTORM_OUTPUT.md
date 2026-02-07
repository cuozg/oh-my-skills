# Brainstorm: {TASK_NAME}

**Task File**: `Documents/Tasks/{Number}{Epic}{Task}.md`
**Date**: {YYYY-MM-DD}
**Status**: {Draft | User Reviewed | Execution Ready}

---

## 1. Investigation Summary

| Item | Details |
|------|---------|
| Classes traced | {list of classes investigated} |
| Dependencies found | {key dependencies} |
| Gaps identified | {missing pieces or ambiguities} |

---

## 2. Questions & Decisions

| # | Question | User Answer | Impact |
|---|----------|-------------|--------|
| 1 | {e.g., "Should cooldown be global or per-instance?"} | {answer} | {how it affects implementation} |

---

## 3. Code Changes

### Change 1: {Description}

- **File**: `{absolute/path/to/file.cs}`
- **Line**: {line number}
- **Original**:
```csharp
{existing code}
```
- **New**:
```csharp
{replacement code}
```
- **Rationale**: {Why this change is needed}

### Change 2: {Description}

- **File**: `{absolute/path/to/file.cs}`
- **Line**: {line number}
- **Original**:
```csharp
{existing code}
```
- **New**:
```csharp
{replacement code}
```
- **Rationale**: {Why this change is needed}

---

## 4. Test Cases

| # | Test | Input | Expected Output |
|---|------|-------|-----------------|
| 1 | {test name} | {setup} | {assertion} |

---

## 5. Execution Readiness

- [ ] All questions answered by user
- [ ] All code changes specified with file, line, and rationale
- [ ] Test cases defined
- [ ] Ready for `unity-plan-executor`
