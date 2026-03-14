# Quality Audit Workflow

Read-only scan of a Unity project. Grade architecture, performance, best practices, and tech debt on an A-F scale. Generate HTML report.

## Steps

1. **Scope project** — list all `.cs`, `.prefab`, `.unity`, `.asmdef`, `.asset` files; record counts
2. **Analyze architecture** — DI patterns, assembly structure, coupling, event systems, singleton count
   - Checklist: `unity-standards/references/quality/architecture-audit.md`
3. **Analyze performance** — hot-path allocations, `FindObjectOfType`, per-frame `GetComponent`, coroutines
   - Checklist: `unity-standards/references/quality/performance-audit.md`
4. **Evaluate best practices** — null handling, serialization safety, test coverage, naming conventions
   - Checklist: `unity-standards/references/quality/best-practices-audit.md`
5. **Measure tech debt** — TODO/FIXME count, dead code, magic numbers, file length outliers
   - Checklist: `unity-standards/references/quality/tech-debt-audit.md`
6. **Grade each category** — apply A-F rubric from `quality-grading-rubric.md`
   - Canonical scale: `unity-standards/references/quality/grading-criteria.md`
7. **Generate HTML report** — structure from `unity-standards/references/quality/html-report-format.md`

## Grading Rules

- One grade per category: Architecture, Performance, Best Practices, Tech Debt
- Every grade must cite ≥1 evidence file path + line number
- F grade requires 3+ CRITICAL violations in that category
- A grade requires zero violations and positive evidence
- Do not average — list each grade separately
- Include "Top 5 Priority Fixes" ranked by severity × frequency

## Classification Rules

- `FindObjectOfType` → performance violation (not architectural)
- Missing `.asmdef` in project > 50 scripts → Architecture WARNING
- Test coverage < 10% by file count → Best Practices WARNING

## Output

Save to `Documents/QualityAudit_{date}.html` unless user specifies a different path.
Read files only — never modify source code or assets.
