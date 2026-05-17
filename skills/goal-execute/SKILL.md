---
name: goal-execute
description: >
  Execute one goal file created by goal-create. Use when a user says to run,
  implement, finish, or ship a goal in Docs/Goals, or wants one goal taken from
  pending to verified completion. Do not use for creating goals or read-only audits.
metadata:
  author: kuozg
  version: "1.1"
---

# Goal Execute

Execute exactly one goal file from `goal-create`, then prove every acceptance criterion with evidence.

## Workflow

### 1. Read the goal

- If a path is provided, read that file in full.
- If no path is provided, scan `Docs/Goals/` for incomplete goals and pick one only when the user's intent is clear; otherwise ask.
- Parse frontmatter, summary, current behavior, desired behavior, key interfaces, acceptance criteria, out of scope, notes, and `depends_on`.

### 2. Understand the work

- Confirm dependencies are complete or already satisfied.
- Spawn a subagent to index the codebase when the relevant files, patterns, or tests are not obvious.
- If the goal is ambiguous, report the ambiguity and stop.
- If a dependency blocks execution, set status `blocked`, refresh `updated`, record why, and stop.

### 3. Plan and track

- Create a concise todo list mapped to the acceptance criteria.
- Set status `in-progress` and refresh `updated` before implementation.
- Keep the plan small: implement only what the criteria require.
- Update ## Implement plan into goal file.

### 4. Implement

- Make focused changes that satisfy the goal.
- Add or update the most direct tests/checks when the repo supports them.
- Avoid unrelated cleanup, speculative abstractions, or broad refactors.

### 5. Self-verify

- Re-check every acceptance criterion against the final code and behavior.
- Use direct evidence only: file paths, commands, test names, logs, screenshots, or observed behavior.
- Treat `UNCLEAR`, partial evidence, stale logs, and assumptions as failures.

### 6. Independent verify

- Spawn a separate subagent to re-read the final files and verify each criterion independently.
- Only check off a criterion when both self-verification and independent verification prove the exact checkbox text.
- Update ## Verification evidence into goal file.

### 7. Sync and report

- If every criterion is verified, change verified criteria from `- [ ]` to `- [x]`, add/update `## Verification evidence`, set status `completed`, and refresh `updated`.
- If anything remains unverified, leave it unchecked, keep status `in-progress` or `blocked`, and record the missing evidence or blocker.
- Sync goal indexes, docs, specs, or README only when the repo already uses them and implementation changed their truth.
- Report criterion status, evidence, files changed, verification commands, and final goal status.

## Rules

- Execute one goal only.
- Never mark a goal complete without evidence for every acceptance criterion.
- Preserve goal-create status values: `pending`, `in-progress`, `completed`, `blocked`.
