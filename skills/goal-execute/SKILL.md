---
name: goal-execute
description: "Execute one goal end-to-end. Discovers an uncompleted goal, updates state, plans, implements, independently verifies every criterion, and syncs documentation."
---

# Goal Execute

Use this skill to execute one goal file end-to-end. Do NOT use for creating goals (`goal-create`) or read-only verification (`goal-verify`).

## Workflow

Follow this fixed sequence. Do not reorder phases. Do not skip independent verification.

### 1. Discover Goal
- Read the provided goal file in full.
- If no specific goal is provided, search `Docs/Goals/` for the first goal that is not `completed` and has criteria with status `TODO` or `IN PROGRESS` (check `Docs/Goals/Master.md` first).
- If no incomplete goal is found, stop and report `NO_INCOMPLETE_GOAL`.

### 2. Update State
- Change the goal's frontmatter status to `processing`.

### 3. Create Plan
- Identify the goal, verbatim acceptance criteria from the table, and relevant specs (`Docs/Specs/`).
- Create an implementation plan detailing steps, criterion-to-work mapping, and intended verification evidence.

### 4. Implement Plan
- Execute the plan sequentially (do NOT parallelize).
- **MANDATORY DELEGATION RULE**: NEVER delegate a task to implement an entire goal. You MUST break/split the goal and delegate work strictly at the level of individual acceptance criteria.
- Spawn a subagent to implement each acceptance criterion one by one. Update the criterion's status to `IN PROGRESS` in the table.
- **NO MULTIPLE CRITERIA**: Never process multiple acceptance criteria in a single task/thread or subagent. This is non-negotiable. If you find the session is processing multiple acceptance criteria simultaneously, STOP IT immediately.
- **COMPACTION**: Perform context compaction after completing each acceptance criterion to keep the context small.
- Once a criterion is implemented, update its status to `VALIDATION`.
- Keep changes strictly scoped to the goal. Add/update necessary tests.

### 5. Independently Verify
- Every acceptance criterion MUST be independently verified before marking it `VALIDATION`.
- Verify by re-reading changed files, running tests, or checking behavior.
- *Rule*: Every acceptance criteria must be satisfied with concrete evidence. `UNCLEAR` counts as unmet.

### 6. Sync Documents
- Once all criteria are verified, update their status to `DONE` in the table with concrete evidence in the Evidences column.
- Update the goal frontmatter status to `completed`.
- Sync `Docs/Goals/Master.md` (status, date, counts).
- Sync `README.md` if user-facing behavior changed.
- Sync `Docs/Specs/` so they match the shipped implementation.
- Output a final report.
