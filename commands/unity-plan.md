---
description: Plan Unity features with structured HTML output and diff patches
agent: sisyphus
skill: unity/unity-plan
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-plan/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Plan the following Unity feature or change:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-plan` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Complete investigation of existing codebase and architecture
- Work broken down into epics and tasks with clear acceptance criteria
- Effort estimates and risk identification
- HTML files delivered in `Documents/Plans/` (overview, tasks, estimates, dependencies, timeline)
- Unified diff patch file with 100% code changes
- Success criteria: Plan is actionable, comprehensive, and ready for implementation

## Context

- **Required skill**: `unity/unity-plan` — you loaded this above
- Investigate existing codebase, analyze requirements, break down work, estimate effort, generate plan

## Requirements

### MUST DO:

- Follow `unity/unity-plan` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Investigate the existing codebase to understand current architecture
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.opencode/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: Plan code changes following naming/architecture conventions
  - `unity-asset-rules.md`: Plan asset changes following structure/naming/optimization conventions

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Skip codebase investigation before planning
- Create plans without clear acceptance criteria

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
