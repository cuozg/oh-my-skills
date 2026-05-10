# Goal Execute Specialist Prompts

Use these prompts to delegate specific phases of the `goal-execute` workflow sequentially.

## 1. Discover & Update
**Prompt:** Find an incomplete goal in `Docs/Goals/` (or via `Master.md`). Read it fully, update its frontmatter status to `processing`, and return the `GOAL_FILE` and exact criteria. If none, return `NO_INCOMPLETE_GOAL`.

## 2. Plan
**Prompt:** Given goal `{goal_file}` and its criteria, produce a step-by-step implementation plan. Map every criterion to specific work and define a concrete verification method.

## 3. Implement
**Prompt:** NEVER delegate a task to implement an entire goal. Break it down and delegate strictly by individual acceptance criteria. Spawn a subagent to implement each acceptance criterion one by one sequentially. Never allow one subagent task to do multiple acceptance criteria. Keep changes scoped. Return `CHANGED_FILES`, `CHECKS_RUN`, and `IMPLEMENTATION_EVIDENCE` for each criterion.

## 4. Verify
**Prompt:** Independently verify every criterion using the implementation evidence as a guide. Return `PASS` only if every single criterion is proven `VERIFIED` via files, commands, logs, or behavior.

## 5. Sync
**Prompt:** Once all criteria are verified, tick the checkboxes in the goal file with evidence links, update status to `completed`. Then sync `Docs/Goals/Master.md`, `README.md`, and relevant `Docs/Specs/`.
