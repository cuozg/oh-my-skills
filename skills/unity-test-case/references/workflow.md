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

## Quality Checklist

- [ ] Every user interaction has at least one test case
- [ ] Happy path + error/failure path covered for each flow
- [ ] Boundary values tested for numeric inputs
- [ ] Steps are atomic, expected results are observable
- [ ] Summary statistics are accurate, HTML renders correctly
