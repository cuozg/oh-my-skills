---
description: Review code changes locally and generate a markdown review report
agent: sisyphus
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity-review-pr-local/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Review changes locally:

$ARGUMENTS

**YOU MUST USE THE `unity-review-pr-local` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Local markdown review file generated (NOT posted to GitHub)
- Findings categorized by severity: critical, major, minor, suggestion
- Summary, per-file comments, performance considerations, architecture feedback
- Success criteria: Comprehensive review completed, actionable feedback provided

## Context

- **Required skill**: `unity-review-pr-local` — you loaded this above
- Analyze uncommitted changes, a specific branch, or commit range

## Requirements

### MUST DO:

- Follow `unity-review-pr-local` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Review against Unity conventions, performance patterns, and best practices
- Use `Read` on every analyzed file to ensure accuracy
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.opencode/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: Review code against naming/architecture conventions
  - `unity-asset-rules.md`: Review asset changes against structure/naming/optimization conventions

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Post review comments to GitHub (this is a LOCAL review)
- Leave review incomplete

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
