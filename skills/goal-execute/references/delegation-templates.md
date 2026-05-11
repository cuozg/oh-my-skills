# Goal Execute Specialist Prompts

Use these prompts to delegate specific phases of the `goal-execute` workflow sequentially.

## 1. Discover & Update
**Prompt:**
- Find an incomplete goal in `Docs/Goals/` (or via `Master.md`).
- Read it fully and update its frontmatter status to `processing`.
- Return the `GOAL_FILE` and exact criteria. 
- If none exist, return `NO_INCOMPLETE_GOAL`.

## 2. Plan
**Prompt:**
- Given goal `{goal_file}` and its criteria, produce a step-by-step implementation plan.
- Map every criterion to specific work.
- Define a concrete verification method for each criterion.

## 3. Implement
**Prompt:**
- NEVER delegate a task to implement an entire goal. Break it down strictly by individual acceptance criteria.
- Spawn a subagent to implement each acceptance criterion one by one sequentially.
- Never allow one subagent task to do multiple acceptance criteria.
- Keep changes scoped.
- Return `CHANGED_FILES`, `CHECKS_RUN`, and `IMPLEMENTATION_EVIDENCE` for each criterion.

## 4. Verify
**Prompt:**
- Independently verify every criterion using the implementation evidence as a guide.
- Return `PASS` only if every single criterion is proven `VERIFIED` via files, commands, logs, or behavior.

## 5. Sync
**Prompt:**
- Once all criteria are verified, tick the checkboxes in the goal file with evidence links.
- Update status to `completed`.
- Sync `Docs/Goals/Master.md`, `README.md`, and relevant `Docs/Specs/`.
