---
description: Autonomous goal execution — scans Docs/Goals/*.md and executes all uncompleted goals
agent: sisyphus
subtask: true
---
ULTRAWORK (ulw)
---
You are entering **Plan Work Mode** — fully autonomous goal execution.

## Activation

1. Load the `plan-work` skill immediately — it contains your complete execution protocol.
2. Follow every instruction in that skill without deviation.
3. Do NOT ask questions. Do NOT wait for confirmation. Think, decide, execute.

## Quick Reference

- **Goals source**: `Docs/Goals/*.md` — one goal per file
- **Execution mode**: Fully autonomous — no user interaction until all goals are complete
- **Scope**: Process all uncompleted goals (status != completed), unless a specific goal file is provided
- **Skills**: Use ALL available skills as needed
- **Delegation**: Use `task(category=..., load_skills=[...])` for implementation
- **Tracking**: Use `task_create`/`task_update` for every goal
- **Verification**: Check Unity Console and Run Play Test after every goal complete

## Rules

- Never ask. Think and decide.
- Never stop early. Process every uncompleted goal.
- Never deliver partial work. Verify everything.
- Update each goal file's `status` frontmatter and checkboxes as goals complete.

---

Load the skill now and begin execution:

```
use_skill("plan-work")
```

$ARGUMENTS
