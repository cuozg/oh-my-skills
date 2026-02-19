---
description: Generate formal Technical Design Documents for Unity features
agent: sisyphus
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity-write-tdd/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Create a Technical Design Document for the following:

$ARGUMENTS

**YOU MUST USE THE `unity-write-tdd` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Comprehensive TDD covering: Overview, Architecture, Client/Server Logic, Data Models, UI/UX, Performance, Testing, Risks, Timeline
- Existing codebase investigated for context
- Code snippets included for key interfaces
- Success criteria: TDD is complete, actionable, references existing patterns

## Context

- **Required skill**: `unity-write-tdd` — you loaded this above
- Investigate existing codebase, reference existing patterns and conventions

## Requirements

### MUST DO:

- Follow `unity-write-tdd` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Investigate existing codebase for context before writing
- Reference existing patterns and conventions
- Include code snippets for key interfaces
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.opencode/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: Reference correct naming/architecture conventions in TDD
  - `unity-asset-rules.md`: Reference asset conventions in TDD

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Write TDD without investigating existing codebase
- Leave TDD sections incomplete

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
