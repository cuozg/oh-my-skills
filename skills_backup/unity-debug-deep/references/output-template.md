# Analysis Report Template

Save to: `Documents/Debug/ANALYSIS_{SubjectName}_{YYYYMMDD}.md`

```markdown
# Deep Analysis: {Subject}

**Date**: {YYYY-MM-DD}  |  **Issue**: {The exact question or issue}
**Verdict**: {1 sentence root cause in plain language}

---

## 1. Overview
{1-3 sentences: what is wrong, where, what the user observes. Cite `FileName.cs:L##`.}

## 2. Impact
- **{Affected system}** — {how affected}

**Severity**: `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` — {justification}

## 3. Root Cause Analysis

### Why It Happens
{3-8 sentences tracing root cause to origin. Cite `File.cs:L##` for every claim.}

### Execution Flow
1. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens}
2. ...{continue until point of failure}

### Cross-Cut Analysis
#### Lifecycle
{Is Unity lifecycle ordering a factor?}
#### Threading / Async
{Any async boundaries, coroutines, callbacks?}
#### State Mutations
{Who else writes to the relevant fields?}
#### Timing
{Frame-dependent? Load-order-dependent?}
#### Edge Cases
{Empty collections, null inputs, destroyed objects?}

{Only include relevant angles. Skip sections that add no value.}

### Steps to Reproduce
1. {Concrete step}
2. {Observe: describe symptom}

{If uncertain, note assumptions.}

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
- **Risk**: `LOW` / `MEDIUM` / `HIGH`
- **Effort**: `SMALL` / `MEDIUM` / `LARGE`

{Add Solution 3 if applicable, same pattern.}

## 5. Workaround

{Temporary workaround if available. Steps, limitations, when it stops working. If none: "No practical workaround — root cause must be fixed."}

## 6. Verification Steps

1. {Apply Solution N}
2. {Trigger scenario from Steps to Reproduce}
3. {Verify expected behavior}
4. {Check console for absence of errors}

## 7. Prevention

- {Actionable practice or safeguard}
```

## Solution Ranking Criteria

| Type | Description |
|:---|:---|
| **Quick Fix** | Minimal change, stops the symptom, might not address root cause fully |
| **Proper Fix** | Addresses root cause correctly, moderate effort |
| **Architectural Fix** | Redesigns the system to prevent this class of issue entirely |

Always include at least one Quick Fix and one Proper Fix. Architectural Fix only when warranted.
Mark exactly one solution as `[RECOMMENDED]`.
