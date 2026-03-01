# Investigation Checklist

Use before assessment/planning to gather evidence:

- How many files need changes? New files needed?
- How much new logic vs. wiring existing systems?
- Existing patterns to follow or greenfield?
- What other systems touch the affected code?
- Tricky edge cases, threading, lifecycle issues?

## Size Reference

| Size | Signals |
|:-----|:--------|
| Small | 1-3 files, follows existing pattern, no new systems |
| Medium | 4-10 files, some new logic, touches 2-3 systems |
| Large | 10+ files, new architecture, cross-cutting concerns |

## Time Reference

| Range | Typical Work |
|:------|:-------------|
| 1-4h | Small bug fix, config change, add field |
| 4-16h | New component, UI screen, system extension |
| 16-40h | New system, major refactor, cross-cutting feature |
| 40h+ | Architecture change, new subsystem with tests |
