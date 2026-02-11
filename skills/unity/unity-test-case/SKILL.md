---
name: unity-test-case
description: "Expert QA professional for Unity game projects. Deep investigate game features, understand game logic and systems, and generate comprehensive test case documents in HTML format. Use when: (1) Creating test cases for a game feature or system, (2) Analyzing a feature for QA coverage, (3) Generating test case documentation, (4) Reviewing test completeness for game mechanics, (5) Creating QA plans for Unity gameplay systems. Triggers: 'test cases', 'QA', 'test plan', 'test coverage', 'create test cases for', 'generate test cases', 'quality assurance', 'test document', 'test case document'."
---

# Unity Test Case Generator

Generate test case documents in HTML for Unity game features. The template uses a dark theme, responsive layout, and interactive checkboxes for quick Pass/Fail marking.

## Purpose

Generate comprehensive QA test case documents for Unity game features — analyzing game logic, state transitions, edge cases, and integrations to ensure thorough manual test coverage.

## Input

- **Required**: Game feature or system to create test cases for (e.g., "daily reward system", "PvP matchmaking")
- **Optional**: Feature spec document, existing test cases to extend, priority areas

## Examples

| User Request | Skill Action |
|:---|:---|
| "Create test cases for the daily reward system" | Investigate reward logic, generate cases for: first claim, streak, missed day, timezone edge, server sync |
| "QA plan for the new PvP mode" | Analyze matchmaking + combat + scoring, generate cases covering queue, match, disconnect, rank update |
| "Test cases for IAP purchase flow" | Trace purchase → verify → grant, generate cases for: success, cancel, network error, duplicate receipt |

## Workflow

1. **Investigate** the feature using `unity-investigate` skill or by reading code
2. **Analyze** logic, state transitions, edge cases, and integrations
3. **Design** test cases using `references/test-case-patterns.md`
4. **Apply** edge case heuristics from `references/qa-methodology.md`
5. **Generate** HTML using `assets/test-case-template.html`
6. **Save** to `Documents/TestCases/{FeatureName}_TestCases.html`

## Investigation Phase

Before writing test cases, investigate the feature:

1. Read all relevant C# scripts
2. Map state machines and logic flows
3. Identify entry points and triggers
4. List configurable parameters and valid ranges
5. Find integration points with other systems
6. Note server communication or data persistence

Key questions:
- How can a user interact with this feature?
- What data drives behavior? (configs, server data, player state)
- What other systems does this depend on or affect?
- What happens at boundaries? (zero, max, overflow, timeout)
- What happens during interruptions? (disconnect, backgrounding, crash)

## Test Case Design

### Sections

Use only relevant sections:

| Section | Code | Focus |
|---------|------|-------|
| Surfacing Points | SP | Where/when the feature appears |
| UI/UX | UI | Layout, badges, animations |
| Functional | FUNC | Logic, rules, calculations |
| Integration | INTG | Interaction with other systems |
| Edge Cases | EDGE | Boundaries, errors, interruptions |
| Performance | PERF | FPS, memory, load times |
| Data Integrity | DATA | Save/load, sync, persistence |

### ID Convention

Format: `{MODULE}-{SECTION}-{SEQ}` (e.g. `SSL-SP-001`, `MATCH-FUNC-012`)

### Priority

- **Critical**: Crash, data loss, payment failure, core loop broken
- **High**: Major feature broken, progression blocker
- **Medium**: Minor deviation, non-blocking UI issue
- **Low**: Cosmetic, rare edge case with workaround

### Continuation Rows

Group multi-phase scenarios under one test using continuation rows (same section, no Title).

## HTML Output

Read `assets/test-case-template.html` and generate the document:

1. Replace all `{{PLACEHOLDER}}` values with actual data
2. Repeat section blocks for each test section
3. Repeat table rows for each test case
4. Calculate summary stats (totals by priority)
5. Calculate coverage percentages per section
6. Result column uses interactive checkboxes — leave unchecked (shows "Fail" by default; checking marks "Pass")
7. For print output, a static "Not Run" badge is shown instead of checkboxes

### Template Features

- **Dark theme**: Dark background with light text for comfortable reading
- **Responsive columns**: Flexbox layout with percentage widths and min-widths — adjusts to screen size
- **Result checkboxes**: Interactive Pass/Fail toggle per test case (screen only)
- **Print support**: Reverts to light theme with static result badges when printed
- **Horizontal scroll**: Table wraps in a scrollable container on narrow screens

### Output Location

Save to: `Documents/TestCases/{FeatureName}_TestCases.html`

Create `Documents/TestCases/` if it does not exist.

## References

- **QA methodology**: `references/qa-methodology.md` — edge case heuristics, CRUCSPIC-STMP mnemonic
- **Test patterns**: `references/test-case-patterns.md` — ID conventions, writing style, common patterns
- **HTML template**: `assets/test-case-template.html` — dark-themed responsive template with checkboxes

## Output

Successful test case generation produces:
1. **HTML document** — saved to `Documents/TestCases/{FeatureName}_TestCases.html`
2. **Summary statistics** — total cases by priority (Critical/High/Medium/Low), coverage percentage per section
3. **Interactive checkboxes** — each test case has Pass/Fail toggle for manual QA execution
4. **Print-ready** — light theme with static result badges when printed

Create `Documents/TestCases/` directory if it does not exist.

## Quality Checklist

- [ ] Every user interaction has at least one test case
- [ ] Happy path covered for each flow
- [ ] Error/failure path covered for each transaction
- [ ] Boundary values tested for numeric inputs
- [ ] State transitions verified (invalid transitions blocked)
- [ ] Multi-step scenarios use continuation rows
- [ ] Priority assignments are consistent
- [ ] Preconditions are specific enough to reproduce
- [ ] Steps are atomic (one action per step)
- [ ] Expected results are observable and verifiable
- [ ] Summary statistics are accurate
- [ ] HTML renders correctly with no broken layout
