---
name: goal-verify
description: >
  Use when verifying Docs/Goals files, validating goal-execute results, checking acceptance criteria, or deciding whether a goal can be marked completed.
metadata:
  author: kuozg
  version: "1.3"
---
# Goal Verify

Verify exactly one `Docs/Goals/**.md` goal. This is a gate, not implementation:
re-check every acceptance criterion independently, audit `goal-execute` self-test
evidence, then update the goal file with honest pass/fail evidence.

## Inputs and contract

- Goal files come from `goal-create`: one file, frontmatter status `completed`, criteria under `## Acceptance criteria`.
- `goal-execute` may add `## Verification evidence`; treat that as evidence to audit, never as proof by itself.
- Verify one goal only. If no path is provided, find a likely unverified goal under `Docs/Goals/`;

## Workflow

1. Read the full goal: frontmatter, desired behavior, key interfaces, criteria, plan, evidence, dependencies.
2. Set/keep status `verifying` while verifying; use `blocked` only for external blockers. Refresh `updated` when editing.
3. Build a private matrix: criterion text, expected proof, existing self-test evidence, independent check, result, severity.
4. Audit execution self-tests for each criterion:
   - relevant to exact criterion text
   - fresh or rerunnable now
   - reproducible command/tool/log/screenshot
   - strong enough to fail if behavior is broken
   - not skipped, stale, assumed, or hidden by compile/editor errors
5. Verify every criterion independently with the narrowest proof:
   - code: cite `path:line`
   - tests: run focused unit/Edit Mode/Play Mode checks
   - scene/assets: inspect GameObjects, components, serialized values, missing refs
   - runtime/editor: record deterministic observed state/logs
   - screenshot: only for visual criteria, preferably paired with state evidence
6. Decide each criterion:
   - PASS only if direct evidence proves the exact checkbox text.
   - FAIL/BLOCKED for `UNCLEAR`, stale logs, skipped tests, missing evidence, compile errors, assumptions, or invalid self-test.
7. Edit the same goal file in Verification part:
   - passed: `- [x] ...`
   - failed/unverified: `- [ ] ...` plus an indented callout directly below
   - update `## Verification evidence` with per-criterion verdicts and accepted/rejected self-test evidence
   - set `completed` only if every criterion passes; otherwise `pending` or `blocked`
8. Report goal path, final status, criterion verdicts, self-test audit, commands/tools run, and next action.

## Failure comments

Use required severity badges directly under failed verification evidence:

- `> 🔴` = **CRITICAL/HIGH**: core criterion missing, test/compile fail, blocking runtime error, data loss/security risk.
- `> 🟠` = **MEDIUM**: partial implementation, invalid/weak self-test, missing edge case, ambiguous/unproven behavior.
- `> 🔵` = **LOW/STYLE**: non-blocking polish, docs/naming/style mismatch.
- `> ✅` = **PASS**: criterion is met and evidence is provided.

Format:

> [🔴 CRITICAL] [Criterion Text] (1 line summary)
> (Short explanations if needed)
>
> - Evidence 1
> - Evidence 2

## Rules

- Preserve criterion text and goal-create/goal-execute sections.
- Do not implement fixes unless explicitly asked.
- Do not mark `completed` without independent passing evidence for every criterion.
- Do not trust self-test evidence until audited.
- Failed verifications must be commented in the goal file, not only in chat.
