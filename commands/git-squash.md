---
description: Squash and organize commits into clean, well-documented history
agent: sisyphus
skill: git-squash
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/git-squash/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Squash and organize the commit history:

$ARGUMENTS

**YOU MUST USE THE `git-squash` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Related commits grouped by feature, bugfix, or logical unit
- Squashed commits with clear, well-documented messages explaining "why" not just "what"
- Clean, organized commit history ready for PR or merge
- Success criteria: History is clean, no commits lost, messages are meaningful

## Context

- **Required skill**: `git-squash` — you loaded this above
- Analyze commit history, group related changes, squash safely

## Requirements

### MUST DO:

- Follow `git-squash` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Verify the result with `git log` before completing
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.opencode/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, require confirmation for destructive operations
  - `unity-csharp-conventions.md`: Follow conventions when analyzing code changes
  - `unity-asset-rules.md`: Understand asset conventions when grouping changes

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- **NEVER force push to main/master** without explicit confirmation
- **NEVER modify commits that have been pushed** to shared branches without confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
