# Goal Execute Specialist Prompts

Use these templates only when specialist delegation is available and useful. Keep the pipeline fixed: discover goal, plan, implement, independently verify every criterion, then sync docs.

## Discover Goal

Use when no goal path was provided.

```text
Find one incomplete goal to execute.

Search Docs/Goals/ for the first goal where:
- frontmatter status is not completed
- the acceptance criteria include at least one unchecked "- [ ]" checkbox

Read Docs/Goals/Master.md first if it exists.
Prefer higher priority only when obvious from the files.
Do not enumerate every goal if a valid target is already found.

Return:
GOAL_FILE: <path>
GOAL_TITLE: <title>
UNCHECKED_COUNT: <number>

If none exists, return exactly:
NO_INCOMPLETE_GOAL
```

## Plan

```text
Plan execution for one goal.

Goal file: {goal_file}
Goal title: {goal_title}

Acceptance criteria, verbatim:
{criteria_numbered}

Relevant goal context:
{goal_context}

Relevant spec context:
{spec_context_or_none}

Return a concise plan with:
- implementation steps
- one criterion-to-work mapping row per acceptance criterion
- a concrete verification method for every criterion
- risks, blockers, or assumptions

Do not write code. Do not drop, merge, or paraphrase criteria.
```

## Implement

```text
Implement this one goal.

Goal file: {goal_file}
Goal title: {goal_title}

Acceptance criteria, verbatim:
{criteria_numbered}

Approved plan:
{plan}

Rules:
- Keep changes scoped to this goal.
- Preserve unrelated user changes.
- Follow existing repo patterns.
- Add or update tests when needed.
- Run the strongest practical checks for this repo.
- Keep a running criterion checklist.

Return:
STATUS: DONE | BLOCKED
CHANGED_FILES: <list>
CHECKS_RUN: <commands and results>
IMPLEMENTATION_EVIDENCE:
  1. <criterion verbatim> - <file:line, command output, or test evidence>
  2. ...
BLOCKER: <only if blocked>
```

## Verify

```text
Independently verify one implemented goal.

Goal file: {goal_file}
Goal title: {goal_title}

Acceptance criteria, verbatim:
{criteria_numbered}

Implementation evidence to treat as claims, not truth:
{implementation_evidence}

Verify every criterion yourself by reading files, running commands, inspecting logs, or checking behavior.

Return:
OVERALL: PASS | FAIL
PER_CRITERION:
  1. [VERIFIED|UNMET|UNCLEAR] <criterion verbatim> - evidence: <file:line, command output, test result, screenshot, log, or observation>
  2. ...
GAPS:
  - <criterion-indexed gap, if any>

OVERALL is PASS only when every criterion is VERIFIED. UNCLEAR counts as FAIL.
```

## Document Sync

```text
Sync documentation for the completed goal.

Goal file: {goal_file}
Goal title: {goal_title}

Verified criteria and evidence:
{verified_evidence}

Implementation summary:
{implementation_summary}

Update:
- goal file checkboxes and completed status
- Docs/Goals/Master.md row, date, and counts
- README.md only if user-facing behavior, commands, APIs, setup, or documented capabilities changed
- relevant Docs/Specs/ files so they match the shipped implementation

Preserve unrelated text and unrelated rows.
```
