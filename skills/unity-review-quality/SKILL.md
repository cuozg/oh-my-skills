---
name: unity-review-quality
description: Full Unity project audit — A-F graded HTML report covering architecture, performance, best practices, tech debt. Triggers — 'project audit', 'quality audit', 'project review', 'code quality report', 'tech debt audit'.
---
# unity-review-quality

Scan a Unity project read-only, grade architecture, performance, best practices, and tech debt on an A–F scale with evidence, and generate a comprehensive HTML report.

## When to Use

- Onboarding to an unfamiliar Unity codebase
- Pre-release quality gate for a shipped title
- Quarterly tech debt audit for a live game

## Workflow

1. **Scope project** — list all `.cs`, `.prefab`, `.unity`, `.asmdef`, `.asset` files; record counts
2. **Analyze architecture** — check DI patterns, assembly structure, coupling, event systems, singleton count
3. **Analyze performance** — scan for hot-path allocations, `FindObjectOfType`, per-frame `GetComponent`, excessive coroutines
4. **Evaluate best practices** — null handling, serialization safety, test coverage presence, naming conventions
5. **Measure tech debt** — TODO/FIXME count, dead code, magic numbers, file length outliers
6. **Grade each category** — apply A–F rubric from `references/quality-grading-rubric.md`
7. **Generate HTML report** — use structure from `unity-standards/references/quality/html-report-format.md`; embed evidence snippets

## Rules

- Read files only — never modify source code or assets
- Assign one grade per category: Architecture, Performance, Best Practices, Tech Debt
- Every grade must cite at least one evidence file path + line number
- F grade requires 3+ CRITICAL violations in that category
- A grade requires zero violations and positive evidence
- Include a "Top 5 Priority Fixes" section ranked by severity × frequency
- Do not average grades into an overall score — list each separately
- Flag `FindObjectOfType` calls as performance violations (not architectural)
- Flag missing `.asmdef` files in a project > 50 scripts as Architecture WARNING
- Flag test coverage below 10% (by file count) as Best Practices WARNING
- Save report to `Documents/QualityAudit_{date}.html` unless path overridden

## Output Format

**MANDATORY**: When posting findings to a PR, use `unity-standards/references/review/pr-submission.md` as the output template — JSON payload, event decision, batching rules, and gh CLI commands. All PR comments MUST be submitted in a single review `POST` call following that template exactly.

HTML report file at `Documents/QualityAudit_{date}.html` with A-F grades per category, evidence table, and prioritized fix list.

## Reference Files

- `references/quality-grading-rubric.md` — per-category A-F descriptions (loads `unity-standards/references/quality/grading-criteria.md` for scale + formula)

Load references on demand via `read_skill_file("unity-review-quality", "references/{file}")` and `read_skill_file("unity-standards", "references/quality/grading-criteria.md")`.

## Standards

Load `unity-standards` for audit criteria. Key references:

- `review/pr-submission.md` — **MANDATORY** output template for PR submissions: JSON payload, event decision, batching, gh CLI
- `quality/grading-criteria.md` — A-F scale definitions, evidence requirements
- `quality/architecture-audit.md` — coupling, layering, assembly structure
- `quality/performance-audit.md` — profiler markers, memory, frame budget
- `quality/best-practices-audit.md` — Unity API usage, deprecated calls
- `quality/tech-debt-audit.md` — TODO density, code duplication, complexity

Load via `read_skill_file("unity-standards", "references/quality/<file>")` and `read_skill_file("unity-standards", "references/review/pr-submission.md")`.
