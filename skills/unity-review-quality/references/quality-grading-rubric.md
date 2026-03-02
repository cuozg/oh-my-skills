# Quality Grading Rubric (A–F)

## Grading Scale

| Grade | Meaning |
|-------|---------|
| A | No violations; positive evidence of best practice |
| B | 1–2 minor violations (NOTE level); no WARNINGs |
| C | 1–3 WARNINGs; no CRITICALs |
| D | 1–2 CRITICALs or 4+ WARNINGs |
| F | 3+ CRITICALs in this category |

Every grade must cite at least one `file:line` evidence reference.

## Category: Architecture

- A: Clear DI, typed events, proper `.asmdef` boundaries, fan-out ≤ 5
- B–C: Minor coupling issues; one missing `.asmdef`; one `FindObjectOfType`
- D: Multiple `FindObjectOfType`; circular assembly refs; God objects present
- F: No architecture pattern; all code in `Assembly-CSharp`; spaghetti dependencies

## Category: Performance

- A: No hot-path allocations; object pooling used; draw calls managed
- B–C: 1–3 Update-frame allocations; no pooling for frequent spawns
- D: LINQ in Update; `FindObjectOfType` per frame; O(n²) in tick
- F: Frame-rate-breaking patterns widespread; GC pressure visible in profiler data

## Category: Best Practices

- A: Null guards, XML docs on public APIs, tests present, clear naming
- B–C: Some missing null guards; sparse comments on complex logic
- D: No tests; magic numbers widespread; `Debug.Log` in production paths
- F: Hardcoded credentials; unsafe deserialization; no null safety anywhere

## Category: Tech Debt

- A: < 5 TODOs; no dead code; files ≤ 300 lines
- B–C: 5–20 TODOs; some dead code; a few large files
- D: 20–50 TODOs; significant dead code; files > 500 lines common
- F: 50+ TODOs; commented-out code blocks throughout; no refactoring history
