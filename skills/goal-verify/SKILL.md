---
name: goal-verify
description: Verify one goal by checking every acceptance criterion one by one against the codebase using Unity Editor tools. Searches for unverified goals if not provided. Updates goal status and records evidence directly.
---

# goal-verify

Agentic skill to independently verify goal acceptance criteria.

## Workflow

1. **Discovery**: Read the full goal file. If the user didn't provide a specific goal, search for an unverified goal in `Docs/Goals/` (one with criteria in `VALIDATION` status).
2. **State Update**: Update the goal's `status` to `verifying`.
3. **Independent Verification**: Walk through all acceptance criteria. Spawn a subagent to verify each criterion **one by one**. If a criterion has status `DONE` but the Evidences column is empty or missing, you must verify it again. Verify it in the Unity Editor (ensure code appears, unit test passes, play test passes, screenshot if available).
4. **Status & Evidence**: Update the status of each acceptance criterion in the goal file's table. Set to `DONE` if verified, or back to `TODO` if failed, and record concrete evidence in the Evidences column.

## Rules

- Every acceptance criterion MUST be satisfied (status `DONE`) before marking the goal as done.
- Do not reorder phases.
- Do not skip independent verification.
- When validating, ensure there are no missing references in Unity GameObject components.
