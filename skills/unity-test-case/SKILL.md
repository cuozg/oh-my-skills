---
name: unity-test-case
description: Generate QA test cases as HTML — use for 'test cases', 'QA test cases', 'generate test cases', 'test plan', 'manual test cases'
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
4. **Generate** — Render all cases into the HTML template from `references/test-case-template.md`
5. **Save** — Write to `Documents/TestCases/{FeatureName}_TestCases.html`

## Rules

- Cover all four categories: happy path, edge, boundary, negative
- Minimum 5 test cases per category when the feature warrants it
- Assign priority: P1 = critical path, P2 = important, P3 = nice-to-have
- Keep steps atomic — one action per step
- Expected results must be observable and unambiguous

## Output Format

`Documents/TestCases/{FeatureName}_TestCases.html` — styled HTML file with test case table, status column, and priority indicators.

## Reference Files

- `references/test-case-template.md` — HTML template for test case documents

Load references on demand via `read_skill_file("unity-test-case", "references/{file}")`.
