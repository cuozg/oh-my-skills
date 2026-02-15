---
name: unity-test-case
description: "Expert QA professional for Unity game projects. Deep investigate game features, understand game logic and systems, and generate comprehensive test case documents in HTML format. Use when: (1) Creating test cases for a game feature or system, (2) Analyzing a feature for QA coverage, (3) Generating test case documentation, (4) Reviewing test completeness for game mechanics, (5) Creating QA plans for Unity gameplay systems. Triggers: 'test cases', 'QA', 'test plan', 'test coverage', 'create test cases for', 'generate test cases', 'quality assurance', 'test document', 'test case document'."
---

# Unity Test Case Generator

**Input**: Game feature/system to test + optional feature spec, existing test cases, priority areas
**Output**: HTML at `Documents/TestCases/{FeatureName}_TestCases.html` using `assets/test-case-template.html`

## Workflow

1. **Investigate** — read relevant C# scripts, map state machines/logic flows, identify entry points/triggers
2. **Analyze** — list configurable params, integration points, server/persistence dependencies
3. **Design** — test cases using `references/test-case-patterns.md` + edge case heuristics from `references/qa-methodology.md`
4. **Generate** — HTML from `assets/test-case-template.html`, replace `{{PLACEHOLDER}}` values, calculate summary stats
5. **Save** to `Documents/TestCases/{FeatureName}_TestCases.html`

## Investigation Questions

- How can a user interact with this feature?
- What data drives behavior? (configs, server data, player state)
- What other systems does this depend on or affect?
- What happens at boundaries? (zero, max, overflow, timeout)
- What happens during interruptions? (disconnect, backgrounding, crash)

## Test Sections

| Section | Code | Focus |
|---------|------|-------|
| Surfacing Points | SP | Where/when feature appears |
| UI/UX | UI | Layout, badges, animations |
| Functional | FUNC | Logic, rules, calculations |
| Integration | INTG | Interaction with other systems |
| Edge Cases | EDGE | Boundaries, errors, interruptions |
| Performance | PERF | FPS, memory, load times |
| Data Integrity | DATA | Save/load, sync, persistence |

**ID format**: `{MODULE}-{SECTION}-{SEQ}` (e.g. `SSL-SP-001`)

## Priority

- **Critical**: Crash, data loss, payment failure, core loop broken
- **High**: Major feature broken, progression blocker
- **Medium**: Minor deviation, non-blocking UI issue
- **Low**: Cosmetic, rare edge case with workaround

## Template Features

- Dark theme with responsive flexbox layout
- Interactive Pass/Fail checkboxes per test case (screen only)
- Print support with light theme and static result badges

## References

- `references/qa-methodology.md` — edge case heuristics, CRUCSPIC-STMP
- `references/test-case-patterns.md` — ID conventions, writing style
- `assets/test-case-template.html` — dark-themed responsive template

## Quality Checklist

- [ ] Every user interaction has at least one test case
- [ ] Happy path + error/failure path covered for each flow
- [ ] Boundary values tested for numeric inputs
- [ ] Steps are atomic, expected results are observable
- [ ] Summary statistics are accurate, HTML renders correctly
