---
description: Review pull requests on GitHub with Unity-specific best practices
agent: build
skill: unity/unity-review-pr
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-review-pr/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Review this PR: $ARGUMENTS

**YOU MUST USE THE `unity/unity-review-pr` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- PR reviewed against Unity patterns, performance, architecture, code style, asset rules, edge cases, and security
- Review comments posted directly on the GitHub PR
- Success criteria: Thorough, actionable review posted to GitHub

## Context

- **Required skill**: `unity/unity-review-pr` — you loaded this above
- Review focus: MonoBehaviour usage, GC/memory, SOLID, project conventions, asset rules, null checks, security

## Requirements

### MUST DO:

- Follow `unity/unity-review-pr` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Review against all project conventions
- Post review comments directly on the GitHub PR
- Use `Read` on every reviewed file to ensure accuracy
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.claude/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: Review code against all naming/architecture conventions
  - `unity-asset-rules.md`: Review asset changes against structure/naming/optimization conventions

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Leave review incomplete or superficial

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
