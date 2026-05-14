---
status: pending          # pending | in-progress | completed | blocked
priority: medium         # critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
depends_on: []           # e.g., ["auth/setup.md"]
---

# [Feature] Task Name

## Objective
{1-3 sentences on what to achieve and why.}

## Context
{Background, existing systems, related paths.}

## Acceptance Criteria

Acceptance criteria must be verifiable by an autonomous agent without human intervention. Use 3-7 criteria per goal.

### General Format Template

```markdown
## Acceptance Criteria
- [ ] **Happy Path**: {Subject} successfully performs {action} under {condition}, resulting in {verifiable outcome}.
- [ ] **Edge/Error Case**: {Subject} handles {invalid/edge condition} by {verifiable error handling or fallback}.
- [ ] **Data/State Verification**: {Data/State} is accurately updated in {storage/UI} and persists after {action}.
- [ ] **Constraint Check**: Execution adheres to {specific constraint, e.g., performance limit, secure storage}.
- [ ] **Evidence**: {Command, test, or tool} successfully runs and outputs {expected validation result}.
```

### Key Rules
- One behavior per checkbox.
- Use concrete paths, variables, and commands.
- Avoid vague words ("properly", "correctly", "best practices").

## Constraints
- {Technical constraints, platform requirements}

## Notes
- {Optional notes, links, decisions}
