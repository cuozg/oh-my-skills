---
description: Generate project documentation (README, architecture, API references)
agent: sisyphus
skill: unity/unity-write-docs
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-write-docs/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Create documentation for the following:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-write-docs` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Appropriate documentation type generated (README, Architecture, API Reference, Onboarding Guide, or Prefab/Scene Setup)
- Thorough codebase investigation completed before writing
- Code examples included where relevant
- Clear headings, formatting, and maintainable structure
- Success criteria: Documentation is accurate, complete, and immediately useful

## Context

- **Required skill**: `unity/unity-write-docs` — you loaded this above
- Documentation types: README, Architecture, API Reference, Onboarding Guide, Prefab/Scene Setup

## Requirements

### MUST DO:

- Follow `unity/unity-write-docs` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Investigate the codebase thoroughly before writing
- Include code examples where relevant
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.claude/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: Reference correct naming conventions in documentation
  - `unity-asset-rules.md`: Document asset conventions accurately

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Write documentation without investigating the codebase first
- Leave documentation incomplete or inaccurate

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
