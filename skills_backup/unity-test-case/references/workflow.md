# unity-test-case — Workflow

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

## Workflow Steps

1. **Investigate** — read relevant C# scripts, map state machines/logic flows, identify entry points/triggers
2. **Analyze** — list configurable params, integration points, server/persistence dependencies
3. **Design** — test cases using `../../unity-shared/references/test-case-patterns.md` + edge case heuristics from `../../unity-shared/references/qa-methodology.md`
4. **Generate** — HTML from `../assets/test-case-template.html`, replace `{{PLACEHOLDER}}` values, calculate summary stats
5. **Save** to `Documents/TestCases/{FeatureName}_TestCases.html`

## Quality Checklist

- [ ] Every user interaction has at least one test case
- [ ] Happy path + error/failure path covered for each flow
- [ ] Boundary values tested for numeric inputs
- [ ] Steps are atomic, expected results are observable
- [ ] Summary statistics are accurate, HTML renders correctly
