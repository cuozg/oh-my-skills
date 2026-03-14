# Confirmation Flow

Two mandatory blocking checkpoints in every planning session.

## Checkpoint 1: Scope Confirmation

After scope detection, STOP and wait for user input.

### What to Present

Use the format from `scope-detection-guide.md` — size, confidence, signals, and a clear question asking the user to confirm or adjust.

### User Responses

| Response | Action |
|----------|--------|
| Confirms (yes, looks good, proceed) | Continue to plan generation |
| Adjusts size (make it M, this is bigger) | Update scope, re-present for confirmation |
| Adds context (also need X, forgot about Y) | Re-evaluate scope with new info, re-present |
| Questions (why M? what about Z?) | Answer, then re-present scope for confirmation |

### Rules

- NEVER proceed to plan generation without explicit user confirmation
- NEVER assume silence means approval
- If user adjusts scope, re-present the updated detection for confirmation
- Keep re-presenting until user explicitly confirms

---

## Checkpoint 2: Plan Review

After generating the plan, STOP and wait for user input.

### What to Present

After printing the plan (Quick inline report or Deep markdown), ask:

```
📋 Plan ready. Want me to:
1. ✅ Create tasks from this plan
2. ✏️ Adjust the plan (tell me what to change)
3. ❌ Discard and start over
```

### User Responses

| Response | Action |
|----------|--------|
| Create tasks (yes, go, create) | Call `task_create` per task item |
| Adjust (change X, add Y, remove Z) | Modify plan, re-present for review |
| Discard (no, start over, scrap it) | Acknowledge, wait for new direction |

### Task Creation Rules

| Mode | Behavior |
|------|----------|
| Quick (XS/S) | Create tasks immediately after user confirms |
| Deep (M/L) | Ask "Create tasks now?" — wait for explicit yes |

### Rules

- NEVER create tasks before user confirms the plan
- NEVER skip the review checkpoint
- If user requests changes, update plan and re-present
- Keep the confirmation question short and actionable

---

## Anti-Patterns

- Auto-proceeding past scope detection without user input
- Creating tasks immediately after plan generation
- Treating "hmm" or partial responses as confirmation
- Skipping checkpoint 2 for "obvious" small tasks
- Generating plan before scope is confirmed
