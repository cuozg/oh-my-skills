# Analysis Report Template

Save to: `Documents/Debug/ANALYSIS_{SubjectName}_{YYYYMMDD}.md`

```markdown
# Deep Analysis: {Subject}

**Date**: {YYYY-MM-DD}
**Issue**: {The exact question or issue being investigated}
**Verdict**: {1 sentence conclusion — the root cause in plain language}

---

## 1. Overview

{1-3 sentences summarizing the issue. What is wrong, where, and what the user observes. Be specific — name classes, methods, variables. Cite with `FileName.cs:L##`.}

## 2. Impact

{What does this issue cause or break? Be specific about downstream effects.}

- **{Affected system/feature}** — {how it is affected}
- **{Affected system/feature}** — {how it is affected}

**Severity**: `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` — {1 sentence justification}

## 3. Root Cause Analysis

### Why It Happens

{3-8 sentences explaining the root cause. Not just "X is null" but "X is null because Y never assigns it when Z condition occurs, which itself stems from W". Trace it to the origin. Cite `File.cs:L##` for every claim.}

### Execution Flow

1. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens at this step}
2. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens next}
3. ...{continue until the point of failure}

### Cross-Cut Analysis

#### Lifecycle
{Is Unity lifecycle ordering a factor? Evidence from code.}

#### Threading / Async
{Any async boundaries, coroutines, callbacks? Evidence from code.}

#### State Mutations
{Who else writes to the relevant fields? Evidence from code.}

#### Timing
{Frame-dependent? Load-order-dependent? Evidence from code.}

#### Edge Cases
{Empty collections, null inputs, destroyed objects? Evidence from code.}

{Only include angles that are relevant to the issue. Skip sections that add no value.}

### Steps to Reproduce

1. {Concrete step — e.g. "Open scene X"}
2. {Concrete step — e.g. "Enter Play Mode"}
3. {Concrete step — e.g. "Trigger action Y while Z is in state W"}
4. {Observe: describe the symptom}

{If reproduction steps cannot be determined with certainty, note assumptions and say what additional information would help.}

## 4. Proposed Solutions

### Solution 1: {Title} [RECOMMENDED]

- **Approach**: {2-4 sentences describing what to do and why this works}
- **Where**: `{FileName.cs:L##}` — {which method/area to change}
- **Trade-off**: {pros and cons}
- **Risk**: `LOW` / `MEDIUM` / `HIGH` — {justification}
- **Effort**: `SMALL` / `MEDIUM` / `LARGE`

### Solution 2: {Title}

- **Approach**: {2-4 sentences}
- **Where**: `{FileName.cs:L##}`
- **Trade-off**: {pros and cons}
- **Risk**: `LOW` / `MEDIUM` / `HIGH` — {justification}
- **Effort**: `SMALL` / `MEDIUM` / `LARGE`

### Solution 3: {Title} (if applicable)

...same pattern...

## 5. Workaround

{Is there a temporary workaround the user can apply right now to avoid the issue without fixing the root cause? If yes, describe it clearly — steps to apply, limitations, and when it will stop working. If no workaround exists, say "No practical workaround — the root cause must be fixed."}

## 6. Verification Steps

{How to verify the issue is fixed after applying a solution:}

1. {Step — e.g. "Apply Solution N"}
2. {Step — e.g. "Enter Play Mode and trigger the scenario from Steps to Reproduce"}
3. {Step — e.g. "Verify that {expected behavior} occurs instead of {symptom}"}
4. {Step — e.g. "Check console for absence of error/warning messages"}
5. {Step — e.g. "Run related tests: {test class/method names if known}"}

## 7. Prevention

{How to prevent this class of issue in the future:}

- {Actionable practice, pattern, or safeguard — not generic advice}
- {Additional prevention measure if applicable}
- {Additional prevention measure if applicable}
```
