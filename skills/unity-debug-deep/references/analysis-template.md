# analysis-template.md

Use this template when writing the output document for unity-debug-deep.

---

```markdown
# Bug Analysis: {SHORT_TOPIC}

**Date**: YYYY-MM-DD  
**Reporter**: {name or "user"}  
**Status**: OPEN | RESOLVED  

---

## Summary

One-paragraph description of the symptom and the investigation scope.

## Reproduction Steps

1. {Step 1}
2. {Step 2}
3. {Observed result vs expected result}

---

## Root Cause Candidates

### [HIGH] Candidate 1 — {short name}

**Evidence**: `{File.cs:line}` — {what the code does that causes this}  
**Angle**: lifecycle | threading | state | data-flow | edge-case  

> Quote the relevant 1-3 lines from the file if they fit.

---

### [MED] Candidate 2 — {short name}

**Evidence**: `{File.cs:line}` — {description}  
**Angle**: {angle}  

---

### [LOW] Candidate 3 — {short name} _(optional)_

**Evidence**: `{File.cs:line}` — {description}  
**Angle**: {angle}  

---

## Solutions

### For Candidate 1

- **WHAT**: {describe the change in plain language}  
- **WHERE**: `{File.cs:line}` — {specific location}  
- **Risk**: LOW | MED | HIGH  

### For Candidate 2

- **WHAT**: {describe the change}  
- **WHERE**: `{File.cs:line}`  
- **Risk**: LOW | MED | HIGH  

---

## Recommended Next Step

{One sentence: which solution to try first and why.}
```

---

## Notes

- Save to `Documents/Debug/ANALYSIS_{TOPIC}_{YYYYMMDD}.md`
- Mark unconfirmed causes with `[UNCONFIRMED]` label
- Solutions describe WHAT and WHERE only — no code patches
- Keep each candidate section under 10 lines
