# Grading Criteria

## Grade Scale

| Grade | Label | Description |
|-------|-------|-------------|
| A | Exemplary | Production-ready, follows all conventions, well-tested |
| B | Good | Minor issues only, no functional impact |
| C | Acceptable | Moderate issues, works but needs improvement |
| D | Below Standard | Significant issues affecting maintainability or correctness |
| F | Failing | Critical defects, broken patterns, or dangerous code |

## Evidence Requirements

| Grade | Min Evidence |
|-------|-------------|
| A | State "no issues found" with areas inspected |
| B | List each minor issue with file:line reference |
| C | List each issue, categorize as style/logic/perf, cite code |
| D | List each issue with severity, cite code, explain impact |
| F | List each critical issue, explain risk, provide fix guidance |

## Category Grades

Score each audit category independently:
- **Architecture** — coupling, boundaries, dependency direction
- **Performance** — frame budget, GC, draw calls, memory
- **Best Practices** — API usage, null safety, lifecycle
- **Tech Debt** — TODOs, duplication, complexity, dead code

## Overall Grade Calculation

1. Assign letter grade per category (A=4, B=3, C=2, D=1, F=0)
2. Apply weights:

| Category | Weight |
|----------|--------|
| Architecture | 0.30 |
| Performance | 0.25 |
| Best Practices | 0.25 |
| Tech Debt | 0.20 |

3. Weighted average → final grade:
   - 3.5–4.0 → A
   - 2.5–3.4 → B
   - 1.5–2.4 → C
   - 0.5–1.4 → D
   - 0.0–0.4 → F

## Grade Override Rules

- Any **F** category → overall capped at **D**
- Two or more **D** categories → overall capped at **C**
- Critical security issue → automatic **F** override
