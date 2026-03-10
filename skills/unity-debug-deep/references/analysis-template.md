# analysis-template.md

Template for unity-debug-deep analysis output. Load this BEFORE writing the report.

---

```markdown
# Bug Analysis: {SHORT_TOPIC}

**Date**: YYYY-MM-DD  
**Status**: OPEN | RESOLVED  

---

## Summary

1-paragraph description: what broke, when, and which systems involved. Include reproduction frequency (always/intermittent/first-time-only).

## Root Cause Candidates

### [HIGH] Candidate 1 — {short name}

**Evidence**: `{File.cs:line}` — {brief description of code causing this}  
**Angle**: [lifecycle | data-flow | threading | state | edge-case | events | serialization]  
**Confidence**: HIGH — direct code evidence + reproducible pattern

> Optional: 1-3 line quote from the offending code

---

### [MED] Candidate 2 — {short name}

**Evidence**: `{File.cs:line}` — {description}  
**Angle**: [angle]  
**Confidence**: MED — likely but indirect evidence

---

### [LOW] Candidate 3 — {short name} _(optional)_

**Evidence**: `{File.cs:line}` — {description}  
**Angle**: [angle]  
**Confidence**: LOW — speculative; minimal supporting evidence _(optional: [UNCONFIRMED])_

---

## Solutions

### For Candidate 1

- **WHAT**: {plain-language description of the fix}  
- **WHERE**: `{File.cs:line}` — {specific location or context}  
- **Risk**: LOW | MED | HIGH

### For Candidate 2

- **WHAT**: {description}  
- **WHERE**: `{File.cs:line}`  
- **Risk**: LOW | MED | HIGH

---

## Recommended Next Step

{One sentence: which candidate to investigate/fix first and why.}
```

---

## Notes

- Save to `Documents/Debug/ANALYSIS_{TOPIC}_{YYYYMMDD}.md`
- Keep each candidate section ≤10 lines
- Solutions describe WHAT and WHERE only — NO code patches
- Include file:line for every claim
- Use [UNCONFIRMED] for speculative causes without file evidence

