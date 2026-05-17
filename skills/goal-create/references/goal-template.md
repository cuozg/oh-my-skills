---
status: pending          # pending | in-progress | completed | blocked
priority: medium         # critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
depends_on: []           # e.g., ["auth/setup.md"]
---

# [bug / update / task] Summary (one-line description of what needs to happen)

## Mandatory Rules

- **One goal per file**: Do not combine multiple objectives.
- **Every agent goal must have concrete, testable acceptance criteria**. Each criterion should be independently verifiable.
- **Describe what the system should do, not how to implement it**. The agent will explore the codebase fresh and make its own implementation decisions.
- **Acceptance criteria are mandatory**: Must be verifiable by an autonomous agent.

## Current behavior

Describe what happens now. For bugs, this is the broken behavior.
For enhancements, this is the status quo the feature builds on.

## Desired behavior

Describe what should happen after the agent's work is complete.
Be specific about edge cases and error conditions.

## Key interfaces

- `TypeName` — what needs to change and why
- `functionName()` return type — what it currently returns vs what it should return
- Config shape — any new configuration options needed

## Acceptance criteria

- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3

## Out of scope

- Thing that should NOT be changed or addressed in this issue
- Adjacent feature that might seem related but is separate

## Notes

{Optional notes, links, decisions}
