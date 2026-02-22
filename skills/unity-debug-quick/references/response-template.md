---
name: response-template
---

# Response Template

Output investigation results using this exact structure.

## Template

```
## Issue: {Short descriptive title of the issue}

### Overview

{1-3 sentences summarizing the issue. What is wrong, where, and what the user observes. Be specific — name classes, methods, variables. Cite with `FileName.cs:L##`.}

### Impact

{What does this issue cause or break? Be specific about downstream effects.}

- **{Affected system/feature}** — {how it is affected}
- **{Affected system/feature}** — {how it is affected}
- **Severity**: `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` — {1 sentence justification}

### Root Cause Analysis

**Why it happens**:

{2-5 sentences explaining the root cause. Not just "X is null" but "X is null because Y never assigns it when Z condition occurs". Trace it to the origin. Cite `File.cs:L##` for every claim.}

**Execution flow**:

1. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens at this step}
2. `{ClassName}.{Method}` (`File.cs:L##`) — {what happens next}
3. ...{continue until the point of failure}

**Steps to reproduce**:

1. {Concrete step — e.g. "Open scene X"}
2. {Concrete step — e.g. "Enter Play Mode"}
3. {Concrete step — e.g. "Click button Y before Z finishes loading"}
4. {Observe: describe the symptom}

### Proposed Solutions

#### Solution 1: {Title} [RECOMMENDED]

- **Approach**: {1-2 sentences describing what to do}
- **Where**: `{FileName.cs:L##}` — {which method/area to change}
- **Trade-off**: {pros and cons — quick vs proper, risk level}
- **Effort**: `SMALL` / `MEDIUM` / `LARGE`

#### Solution 2: {Title}

- **Approach**: {1-2 sentences}
- **Where**: `{FileName.cs:L##}`
- **Trade-off**: {pros and cons}
- **Effort**: `SMALL` / `MEDIUM` / `LARGE`

#### Solution 3: {Title} (if applicable)

...same pattern...

### Workaround

{Is there a temporary workaround the user can apply right now to avoid the issue? If yes, describe it. If no workaround exists, say "No practical workaround — the root cause must be fixed."}

### Verification Steps

{How to verify the issue is fixed after applying a solution:}

1. {Step — e.g. "Apply Solution N"}
2. {Step — e.g. "Enter Play Mode and trigger X"}
3. {Step — e.g. "Verify that Y behaves correctly"}
4. {Step — e.g. "Check console for absence of error Z"}

### Prevention

- {How to prevent this class of issue in the future — coding practice, pattern, or safeguard}
- {Additional prevention measure if applicable}
- {Additional prevention measure if applicable}
```

## Template Rules

- **Overview**: 1-3 sentences max. Factual. No speculation. Cite file:line.
- **Impact**: List affected systems with bold labels. Always include Severity rating.
- **Root Cause Analysis**: Trace to the origin — not surface symptoms. Every claim cites `File.cs:L##`. Include execution flow (2-8 steps) and reproduction steps.
- **Proposed Solutions**: Minimum 2, maximum 4. Mark exactly one `[RECOMMENDED]`. Describe approach and location — do NOT write code. Include effort estimate.
- **Workaround**: A temporary bypass if one exists. Be honest if none exists.
- **Verification Steps**: Concrete steps to confirm the fix works. Minimum 2 steps.
- **Prevention**: 1-3 bullet points. Actionable practices, not generic advice.
