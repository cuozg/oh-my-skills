# Analysis Report Template

Save to: `Documents/Debug/ANALYSIS_{SubjectName}_{YYYYMMDD}.md`

```markdown
# Deep Analysis: {Subject}

**Date**: {YYYY-MM-DD}
**Question**: {The exact question or issue being investigated}
**Verdict**: {1 sentence conclusion}

---

## 1. Scope

**Subject**: {class/method/system being investigated}
**Expected Behavior**: {what should happen}
**Actual Behavior**: {what actually happens}
**Boundaries**: {what is in/out of scope}

## 2. System Map

**Files Involved**:
- `{File1.cs}` — {role in the issue}
- `{File2.cs}` — {role in the issue}

**Key Dependencies**:
- {ClassName} depends on {OtherClass} via {mechanism}

## 3. Forward Trace

Starting from {entry point}:

1. `{Class}.{Method}` (`File.cs:L##`) — {what happens}
2. `{Class}.{Method}` (`File.cs:L##`) — {what happens}
3. ... {continue full chain}

**Observations**: {what stands out in the forward trace}

## 4. Backward Trace

Starting from {failure point}:

1. `{Class}.{Method}` (`File.cs:L##`) — {the failure/symptom}
2. `{Class}.{Method}` (`File.cs:L##`) — {who called/set the failing value}
3. ... {continue backwards}

**Observations**: {what stands out in the backward trace}

## 5. Cross-Cut Analysis

### Lifecycle
{Is Unity lifecycle ordering a factor? Evidence.}

### Threading / Async
{Any async boundaries, coroutines, callbacks? Evidence.}

### State Mutations
{Who else writes to the relevant fields? Evidence.}

### Timing
{Frame-dependent? Load-order-dependent? Evidence.}

### Edge Cases
{Empty collections, null inputs, destroyed objects? Evidence.}

## 6. Hypotheses

### Hypothesis A: {title}
- **Claim**: {one sentence}
- **Prediction**: {what we'd expect to see if true}
- **Evidence**: {what we found}
- **Verdict**: `CONFIRMED` / `DISPROVED` / `INCONCLUSIVE`

### Hypothesis B: {title}
- **Claim**: {one sentence}
- **Prediction**: {what we'd expect to see if true}
- **Evidence**: {what we found}
- **Verdict**: `CONFIRMED` / `DISPROVED` / `INCONCLUSIVE`

{...more hypotheses if needed...}

## 7. Conclusion

**Root Cause**: {1-2 sentences explaining the definitive root cause}

**Evidence Chain**:
1. {fact} → 2. {fact} → 3. {fact} → {conclusion}

**Confidence**: `HIGH` / `MEDIUM` / `LOW` — {justification}

**Remaining Uncertainties**:
- {anything that couldn't be fully verified}

## 8. Recommended Next Steps

- {actionable recommendation 1}
- {actionable recommendation 2}
- {actionable recommendation 3}
```
