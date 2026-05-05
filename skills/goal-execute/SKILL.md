---
name: goal-execute
description: "Execute one goal end-to-end. Read the goal and every acceptance criterion, plan the work, implement it, update goal status and criterion checkboxes, and verify every acceptance criterion is done before changing the goal state to completed. Runs the fixed specialist pipeline: discover goal, then plan, then implement, independently verify every criterion with concrete evidence, then sync goal docs, Master.md, README, and specs. Do NOT use for creating goals; use goal-create. Do NOT use for verification-only reports; use goal-verify."
---

# Goal Execute

Use this skill to execute one existing goal file end-to-end. The source of truth is the goal document and every acceptance criterion inside it.

Do not use this skill to create a new goal. Use `goal-create`.
Do not use this skill for a read-only verification report. Use `goal-verify`.

## Required Outcome

The run is complete only when all of these are true:

- The selected goal file was read in full, including frontmatter and every acceptance criterion.
- The work was planned before implementation.
- The implementation satisfies every acceptance criterion.
- Each criterion has fresh concrete evidence from files, commands, tests, logs, screenshots, or observed behavior.
- The goal file checkboxes and status reflect only verified work.
- `Docs/Goals/Master.md`, relevant `README.md` content, and relevant `Docs/Specs/` files are synchronized with the implementation.

Do not mark a goal completed because the implementation "looks done". Completion requires criterion-by-criterion evidence.

## Fixed Pipeline

Run the phases in this order:

1. Discover goal
2. Plan
3. Implement
4. Independently verify every criterion
5. Sync goal docs, `Master.md`, `README.md`, and specs
6. Report the evidence

Do not reorder phases. Do not skip independent verification.

## 1. Discover Goal

If the user gave a goal path, use that file.

If no path was given:

- Read `Docs/Goals/Master.md` first when it exists.
- Search `Docs/Goals/` for the first goal whose status is not `completed` and whose acceptance criteria include at least one unchecked `- [ ]` checkbox.
- Prefer higher-priority goals when priority is obvious, but do not spend time building a full scheduler.
- If no incomplete goal exists, stop and report `NO_INCOMPLETE_GOAL`. Do not fabricate a goal.

After selecting a goal:

- Read the entire file.
- Count every acceptance-criteria checkbox.
- Preserve the exact criterion text for planning, implementation, verification, and final reporting.
- Identify relevant specs under `Docs/Specs/` and read them if present.

## 2. Plan

Create a short execution plan before editing files. The plan must include:

- The goal file path and title.
- The exact acceptance criteria, numbered in their original order.
- The implementation steps.
- A criterion-to-work mapping, with one row per criterion.
- The intended verification evidence for each criterion.
- Risks, blockers, or assumptions.

If the plan cannot map every criterion to work and verification, improve the plan before implementation.

## 3. Implement

Implement only the selected goal. Keep changes scoped to the goal, related docs, and necessary tests.

During implementation:

- Track criterion progress continuously.
- Preserve unrelated user changes.
- Follow the repo's established coding, testing, and documentation patterns.
- Add or update tests when the criterion or risk level warrants it.
- Run the strongest practical checks available for the project.
- Capture command output or concrete evidence for later verification.

If a criterion cannot be completed because of a real blocker, stop implementation for that goal and take the blocked path.

## 4. Independently Verify Every Criterion

After implementation, verify each criterion independently from the implementation notes. Re-read changed files and re-run commands instead of trusting the implementation summary.

For every criterion, record:

- `VERIFIED`, `UNMET`, or `UNCLEAR`.
- The exact criterion text.
- Concrete evidence, such as `file:line`, command output, test name and result, screenshot path, log excerpt, or observed runtime behavior.

`UNCLEAR` is not good enough for completion. Treat it as unmet until evidence is gathered.

The goal may become `completed` only when every criterion is `VERIFIED`.

## 5. Sync Documents

When every criterion is verified:

- In the goal file, tick only verified criteria.
- Set frontmatter `status: completed`.
- Add or update completion metadata when the repo's goal format uses it.
- Update `Docs/Goals/Master.md` so the row, status, date, and summary counts match the goal file.
- Update `README.md` only when the completed work changes user-facing behavior, commands, APIs, setup, or documented capabilities.
- Update or create relevant `Docs/Specs/` files so they describe what was actually implemented.

Preserve unrelated goal text and unrelated rows.

## Blocked Path

If the goal cannot be completed:

- Do not mark the goal completed.
- Do not tick unverified criteria.
- Set the goal status to `blocked` only when the blocker is real and current.
- Add a concise blocker section naming the unmet criteria and evidence gathered.
- Update `Docs/Goals/Master.md` to match the blocked status.
- Do not update specs as if the feature shipped.

## Final Report

Report the result with:

- Goal title and file path.
- Final status: `completed`, `blocked`, or `NO_INCOMPLETE_GOAL`.
- Changed files.
- Verification commands run.
- One evidence row per acceptance criterion.
- Document sync summary for goal file, `Master.md`, `README.md`, and specs.
- Any remaining risks or follow-up required.

Keep completion claims strict: if a criterion lacks concrete evidence, the goal is not completed.
