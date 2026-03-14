# Quality Grading Rubric — Skill Extensions

> **Canonical reference**: `unity-standards/references/quality/grading-criteria.md`
> Load via: `read_skill_file("unity-standards", "references/quality/grading-criteria.md")`

Standards defines A-F scale, weighted calculation formula, evidence requirements,
and override rules. Below are per-category grade descriptions unique to this skill.

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
