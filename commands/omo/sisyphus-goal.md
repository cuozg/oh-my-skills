---
description: Interactive goal creation — creates structured goal files in Docs/Goals/
agent: sisyphus
subtask: true
---
ULTRAWORK
You are entering **Sisyphus Goal Mode** — interactive goal creation.

## Activation

1. Load the `sisyphus-goal` skill immediately — it contains your complete goal creation workflow.
2. Follow every instruction in that skill without deviation.
3. **DO ask clarifying questions** to ensure the goal is well-defined before writing.

## Quick Reference

- **Output**: `Docs/Goals/{kebab-case-title}.md` — one goal per file
- **Mode**: Interactive — ask questions to refine the goal before writing
- **Format**: Structured template with Status, Objective, Context, Acceptance Criteria, Constraints, Priority
- **Follow-up**: After creating, offer to run `/omo/sisyphus-work` to execute

## Rules

- Always ask clarifying questions before writing a goal file.
- One goal per file. Never combine multiple objectives.
- Acceptance criteria are mandatory — no criteria, no goal.
- Get user confirmation before saving.

---

Load the skill now and begin:

```
use_skill("sisyphus-goal")
```

$ARGUMENTS
