---
name: unity-test-case
description: >
  Use this skill to generate structured QA test cases as an HTML document — covering happy paths, edge
  cases, boundary values, and negative tests. Use when the user needs a manual test plan, says "generate
  test cases," "QA test plan," "what should we test," or wants documented test scenarios before a release.
  Outputs to Documents/TestCases/. Do not use for automated unit tests — use unity-test-unit for that.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-test-case

Generate structured QA test cases covering happy paths, edge cases, boundary values, and negative tests, saved as an HTML document.

## When to Use

- Creating a QA test plan for a new feature or system
- Documenting manual test cases before a release
- Generating test coverage for a bug fix or change set
- Producing shareable test documentation for a team or stakeholder

## Workflow

1. **Understand** — Read the feature spec, related scripts, or user description to identify testable behaviors
2. **Categorize** — Group cases by: Happy Path, Edge Cases, Boundary Values, Negative Tests, Performance/Load
3. **Write** — For each case: ID, title, preconditions, steps, expected result, priority (P1/P2/P3)
4. **Generate** — Render all cases into the HTML template from `unity-standards/references/test/test-case-format.md`
5. **Save** — Write to `Documents/TestCases/{FeatureName}_TestCases.html`

## Rules

- Cover all four categories: happy path, edge, boundary, negative
- Minimum 5 test cases per category when the feature warrants it
- Assign priority: P1 = critical path, P2 = important, P3 = nice-to-have
- Keep steps atomic — one action per step
- Expected results must be observable and unambiguous

## Output Format

`Documents/TestCases/{FeatureName}_TestCases.html` — styled HTML file with test case table, status column, and priority indicators.

## Standards

Load `unity-standards` for test case conventions. Key references:

- `test/test-case-format.md` — HTML output structure, severity, coverage
- `test/coverage-strategy.md` — what to test, boundary values, edge cases

Load via `read_skill_file("unity-standards", "references/test/<file>")`.
