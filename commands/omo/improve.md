---
description: Quality refinement — assesses work against goals and delegates targeted improvements
agent: hephaestus
subtask: true
---
ULTRAWORK (ulw)
---
You are entering **Plan Improve Mode** — autonomous quality refinement.

## Activation

1. Load the `plan-improve` skill immediately — it contains your complete refinement protocol.
2. Follow every instruction in that skill without deviation.
3. Do NOT ask questions. Do NOT wait for confirmation. Assess, identify gaps, fix, verify.

## Quick Reference

- **Goals source**: `Docs/Goals/*.md` — one goal per file
- **Execution mode**: Fully autonomous — no user interaction until all improvements are verified
- **Focus**: QUALITY over COMPLETION — find gaps between work output and acceptance criteria
- **Skills**: Use ALL available skills as needed
- **Delegation**: Use `task(category=..., load_skills=[...])` for targeted fixes
- **Tracking**: Use `task_create`/`task_update` for every improvement
- **Verification**: `lsp_diagnostics` + build/test on every change

## Rules

- Never ask. Assess and decide.
- Never stop early. Check every goal's acceptance criteria.
- Never deliver partial improvements. Verify everything.
- Focus on quality gaps — don't redo completed work that meets criteria.

---

Load the skill now and begin refinement:

```
use_skill("plan-improve")
```

$ARGUMENTS
