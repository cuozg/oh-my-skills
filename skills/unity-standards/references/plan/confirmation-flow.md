# Confirmation Flow

Use this only when the user asks for a plan, costing, technical approach, or
goal breakdown. For direct implementation requests, make reasonable assumptions
and execute; do not add artificial approval gates.

## Checkpoint 1: Scope Confirmation

After scope detection, pause only when scope is ambiguous, risky, or user asked
for approval before execution.

### What to Present

Present size, confidence, signals, assumptions, and a clear question asking the
user to confirm or adjust.

For production features, also surface unresolved product and operations
assumptions: KPI, analytics event meaning, LiveOps controls, backend readiness,
SDK limitations, platform/store constraints, QA scope, and post-release
monitoring.

### User Responses

| Response | Action |
|----------|--------|
| Confirms (yes, looks good, proceed) | Continue to plan generation |
| Adjusts size (make it M, this is bigger) | Update scope, re-present for confirmation |
| Adds context (also need X, forgot about Y) | Re-evaluate scope with new info, re-present |
| Questions (why M? what about Z?) | Answer, then re-present scope for confirmation |

### Rules

- Do not proceed past unresolved ambiguity
- Do not assume silence means approval when approval was requested
- If user adjusts scope, re-present the updated detection for confirmation
- Keep re-presenting until scope is concrete enough to plan

---

## Checkpoint 2: Plan Review

After generating the plan, stop when the deliverable is the plan itself. If the
user asked for implementation, continue after sharing the plan unless approval
was explicitly required.

### What to Present

After printing the plan (Quick inline report or Deep markdown), ask:

```
Plan ready. Want me to:
1. Create goal/todo tasks from this plan
2. Adjust the plan
3. Discard and start over
```

### User Responses

| Response | Action |
|----------|--------|
| Create tasks (yes, go, create) | Use the relevant goal/todo skill output format |
| Adjust (change X, add Y, remove Z) | Modify plan, re-present for review |
| Discard (no, start over, scrap it) | Acknowledge, wait for new direction |

### Task Creation Rules

| Mode | Behavior |
|------|----------|
| Quick (XS/S) | Create tasks immediately after user confirms |
| Deep (M/L) | Ask "Create tasks now?" - wait for explicit yes |

### Rules

- Do not create task files before user confirms the plan
- Do not skip the review checkpoint when the user asked for planning only
- If user requests changes, update plan and re-present
- Keep the confirmation question short and actionable

---

## Anti-Patterns

- Auto-proceeding past unresolved scope ambiguity
- Creating tasks immediately after plan generation
- Treating "hmm" or partial responses as confirmation
- Skipping checkpoint 2 for "obvious" small tasks
- Generating plan before scope is confirmed
