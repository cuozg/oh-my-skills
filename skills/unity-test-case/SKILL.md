---
name: unity-test-case
description: "Expert QA professional for Unity game projects. Deep investigate game features, understand game logic and systems, and generate comprehensive test case documents in HTML format. Use when: (1) Creating test cases for a game feature or system, (2) Analyzing a feature for QA coverage, (3) Generating test case documentation, (4) Reviewing test completeness for game mechanics, (5) Creating QA plans for Unity gameplay systems. Triggers: 'test cases', 'QA', 'test plan', 'test coverage', 'create test cases for', 'generate test cases', 'quality assurance', 'test document', 'test case document'."
---

# Unity Test Case Generator

Generate comprehensive, professional test case documents in HTML format for Unity game features and systems.

## Workflow

1. **Investigate** the target feature/system using `unity-investigate` skill or by reading relevant code
2. **Analyze** game logic, state transitions, edge cases, and integration points
3. **Design** test cases using patterns from `references/test-case-patterns.md`
4. **Apply** QA methodology from `references/qa-methodology.md` for edge case identification
5. **Generate** HTML document using the template in `assets/test-case-template.html`
6. **Save** output to `Documents/TestCases/{FeatureName}_TestCases.html`

## Investigation Phase

Before generating test cases, deeply investigate the feature:

1. Read all relevant C# scripts for the feature
2. Map the complete state machine / logic flow
3. Identify all entry points (surfacing points, triggers)
4. List all configurable parameters and their valid ranges
5. Find integration points with other systems
6. Note any server communication or data persistence

Key questions to answer:
- What are ALL the ways a user can interact with this feature?
- What data drives the feature behavior? (configs, server data, player state)
- What other systems does this feature depend on or affect?
- What happens at boundaries? (zero, max, overflow, timeout)
- What happens during interruptions? (disconnect, backgrounding, crash)

## Test Case Design

### Section Organization

Organize test cases into these sections (include only relevant sections):

| Section | Code | Focus |
|---------|------|-------|
| Surfacing Points | SP | Where/when the feature appears or triggers |
| UI/UX | UI | Visual correctness, layout, badges, animations |
| Functional | FUNC | Business logic, rules, calculations, state transitions |
| Integration | INTG | Interaction with other game systems |
| Edge Cases | EDGE | Boundary conditions, error states, interruptions |
| Performance | PERF | Frame rate, memory, loading times |
| Data Integrity | DATA | Save/load, server sync, persistence |

### ID Convention

Format: `{MODULE}-{SECTION}-{SEQ}`

Derive MODULE as 2-5 uppercase chars from feature name. Examples:
- `SSL-SP-001` (Sale System Lite, Surfacing Points, #1)
- `MATCH-FUNC-012` (Match System, Functional, #12)

### Priority Assignment

- **Critical**: Core loop broken, data loss, crash, payment failure
- **High**: Major feature broken, progression blocker, significant UI break
- **Medium**: Minor deviation, non-blocking UI, edge case failure
- **Low**: Cosmetic, typo, rare edge case with workaround

### Continuation Rows

For multi-phase test scenarios, use continuation rows (same section, no Title) to group related steps under one logical test. This matches the reference CSV pattern.

## HTML Output Generation

Read the template from `assets/test-case-template.html` and generate the complete HTML document by:

1. Replace all `{{PLACEHOLDER}}` values with actual data
2. Repeat the section block for each test section
3. Repeat the table row block for each test case
4. Calculate summary statistics (totals by priority)
5. Calculate coverage percentages per section
6. Set all Result badges to "Not Run" (default state)

### Output Location

Save to: `Documents/TestCases/{FeatureName}_TestCases.html`

Create the `Documents/TestCases/` directory if it does not exist.

## References

- **QA methodology and edge case heuristics**: Read `references/qa-methodology.md` for test design techniques, priority classification, and the CRUCSPIC-STMP edge case mnemonic
- **Test case patterns and writing style**: Read `references/test-case-patterns.md` for ID conventions, section organization patterns, writing style guide, and common test patterns by feature type
- **HTML template**: Use `assets/test-case-template.html` as the base template for output generation

## Quality Checklist

Before finalizing, verify:

- [ ] Every user-facing interaction has at least one test case
- [ ] Happy path covered for each flow
- [ ] Error/failure path covered for each transaction
- [ ] Boundary values tested for numeric inputs
- [ ] State transitions verified (especially invalid transitions blocked)
- [ ] Multi-step scenarios use continuation rows properly
- [ ] Priority assignments are consistent and justified
- [ ] Preconditions are specific enough to reproduce
- [ ] Steps are atomic (one action per step)
- [ ] Expected results are observable and verifiable
- [ ] Summary statistics are accurate
- [ ] HTML renders correctly with no broken layout
