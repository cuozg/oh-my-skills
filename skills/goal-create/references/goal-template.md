---
status: pending          # pending | in-progress | completed | blocked | verifying | done
priority: medium         # critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
depends_on: []           # e.g., ["auth/setup.md"]
---

# [bug / update / task] Summary (one-line description of what needs to happen)

## Current behavior

(Short, bullet type)
Describe what happens now. For bugs, this is the broken behavior.
For enhancements, this is the status quo the feature builds on.

## Desired behavior

(Short, bullet type)
Describe what should happen after the agent's work is complete.
Be specific about edge cases and error conditions.

## Key interfaces

(Short, bullet type)

- `TypeName` — what needs to change and why
- `functionName()` return type — what it currently returns vs what it should return
- Config shape — any new configuration options needed

## Acceptance criteria

(Short, compact, one line one criteria)

- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3

## Implementation plan

(Fill when plan to execute this goal)
Step by step to complete this goal

1. Do step 1
2. Do step 2
...

## Verification evidence

(Fill when verify all the acceptance criteria)
Provide the real evidences for each acceptance criteria (runtime log, editor unit test, logic code, ...)

- [ ] [code/tests/scene/screenshot] Evidence 1
- [ ] [code/tests/scene/screenshot] Evidence 2
