# Quality Audit Workflow

Read-only scan of a Unity project. Grade Architecture, Performance, Best Practices, and Tech Debt on an A-F scale. Generate HTML report.

## Steps

1. **Scope project** — list all `.cs`, `.prefab`, `.unity`, `.asmdef`, `.asset` files; record counts.
   - For projects >500 files: sample representative files (entry points, managers, hot paths) rather than reading everything. Note sampling strategy in report.
   - Always read: project root assemblies, main managers/singletons, entry points.
2. **Analyze architecture** — DI patterns, assembly structure, coupling, event systems, singleton count.
   - Checklist: `read_skill_file("unity-standards", "references/quality/architecture-audit.md")`
3. **Analyze performance** — hot-path allocations, `FindObjectOfType`, per-frame `GetComponent`, coroutines.
   - Checklist: `read_skill_file("unity-standards", "references/quality/performance-audit.md")`
4. **Evaluate best practices** — null handling, serialization safety, test coverage, naming conventions.
   - Checklist: `read_skill_file("unity-standards", "references/quality/best-practices-audit.md")`
5. **Measure tech debt** — TODO/FIXME count, dead code, magic numbers, file length outliers.
   - Checklist: `read_skill_file("unity-standards", "references/quality/tech-debt-audit.md")`
6. **Grade each category** — apply A-F rubric below.
   - Canonical scale: `read_skill_file("unity-standards", "references/quality/grading-criteria.md")`
7. **Generate HTML report** — structure from `read_skill_file("unity-standards", "references/quality/html-report-format.md")`

## Grading Rubric

### Architecture

| Grade | Criteria |
|-------|----------|
| A | Clear DI, typed events, proper `.asmdef` boundaries, fan-out ≤ 5 |
| B-C | Minor coupling issues; one missing `.asmdef`; one `FindObjectOfType` |
| D | Multiple `FindObjectOfType`; circular assembly refs; God objects present |
| F | No architecture pattern; all code in `Assembly-CSharp`; spaghetti dependencies |

### Performance

| Grade | Criteria |
|-------|----------|
| A | No hot-path allocations; object pooling used; draw calls managed |
| B-C | 1-3 Update-frame allocations; no pooling for frequent spawns |
| D | LINQ in Update; `FindObjectOfType` per frame; O(n²) in tick |
| F | Frame-rate-breaking patterns widespread; GC pressure visible in profiler data |

### Best Practices

| Grade | Criteria |
|-------|----------|
| A | Null guards, XML docs on public APIs, tests present, clear naming |
| B-C | Some missing null guards; sparse comments on complex logic |
| D | No tests; magic numbers widespread; `Debug.Log` in production paths |
| F | Hardcoded credentials; unsafe deserialization; no null safety anywhere |

### Tech Debt

| Grade | Criteria |
|-------|----------|
| A | < 5 TODOs; no dead code; files ≤ 300 lines |
| B-C | 5-20 TODOs; some dead code; a few large files |
| D | 20-50 TODOs; significant dead code; files > 500 lines common |
| F | 50+ TODOs; commented-out code blocks throughout; no refactoring history |

## Grading Rules

- One grade per category: Architecture, Performance, Best Practices, Tech Debt
- Every grade must cite ≥1 evidence file path + line number
- F grade requires 3+ CRITICAL violations in that category
- A grade requires zero violations and positive evidence
- Do not average — list each grade separately
- Include "Top 5 Priority Fixes" ranked by severity × frequency

## Classification Rules

- `FindObjectOfType` → performance violation (not architectural) unless used for DI wiring
- Missing `.asmdef` in project > 50 scripts → Architecture WARNING
- Test coverage < 10% by file count → Best Practices WARNING
- Static singleton access from non-manager classes → Architecture WARNING
- `Debug.Log` in Update loops → Performance WARNING + Best Practices WARNING

## Large Project Strategy

For projects with 500+ C# files:
1. **Full scan**: `.asmdef` files, project config, assembly structure (always read all)
2. **Targeted read**: Manager/Singleton classes, entry points, hot-path scripts (Update/FixedUpdate heavy)
3. **Sampling**: Randomly sample 20% of remaining files, focusing on largest files first
4. **Grep patterns**: Use `grep` for known anti-patterns across entire codebase without reading full files:
   - `FindObjectOfType` in Update methods
   - `new List` / `new Dictionary` in Update methods
   - `async void` outside event handlers
   - Missing `[FormerlySerializedAs]` near renamed fields
5. Note in report: "Audit based on full structural analysis + {N}% file sampling"

## Output

Save to `Documents/QualityAudit_{date}.html` unless user specifies a different path.
Read files only — never modify source code or assets.
