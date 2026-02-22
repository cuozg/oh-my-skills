# Response Template

ALWAYS use this exact structure:

```
## Error Analysis: {ErrorType}

### Error Summary

| Field | Value |
|:---|:---|
| **Type** | {NullReferenceException / CS0246 / etc.} |
| **Message** | {exact error message} |
| **File** | `{FileName.cs:L##}` |
| **Method** | `{ClassName.MethodName}` |
| **Frequency** | {every frame / on action / once / unknown} |

### What's Happening

{2-4 sentences explaining what the error means in the context of THIS code. Not generic — specific to the user's code. Reference actual variable names, method names, class names. Cite `File.cs:L##`.}

### Root Cause

{2-4 sentences explaining WHY this error occurs. Trace it back to the origin — not just "X is null" but "X is null because Y never assigns it because Z". Cite evidence.}

### Call Chain

{Trigger} -> {Step 1} -> {Step 2} -> {Crash Site}

1. `{Class}.{Method}` (`File.cs:L##`) — {what happens}
2. `{Class}.{Method}` (`File.cs:L##`) — {what happens}
3. **CRASH** -> `{Class}.{Method}` (`File.cs:L##`) — {the failure}

---

### Solution 1: {Title} [RECOMMENDED]

**Approach**: {1 sentence describing the approach}
**Trade-off**: {quick fix / proper fix / architectural change} — {pros and cons}
**Risk**: `LOW` / `MEDIUM` / `HIGH`

```csharp
// {FileName.cs} — Line {N}
// BEFORE:
{existing code}

// AFTER:
{fixed code}
```

{1-2 sentences explaining why this works.}

### Solution 2: {Title}

**Approach**: {1 sentence}
**Trade-off**: {description}
**Risk**: `LOW` / `MEDIUM` / `HIGH`

```csharp
// {FileName.cs} — Line {N}
// BEFORE:
{existing code}

// AFTER:
{fixed code}
```

{1-2 sentences explaining why this works.}

### Solution 3: {Title} (if applicable)

...same pattern...

---

### Recommendation

{2-3 sentences: which solution you recommend and why. Consider: minimal disruption, correctness, future-proofing.}

### Prevention

- {How to prevent this class of error in the future — 1-3 bullet points}
```
