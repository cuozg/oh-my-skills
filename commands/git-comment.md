---
description: Generate structured commit comments from PRs or commit hashes
agent: build
skill: git/git-comment
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/git/git-comment/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Generate structured commit documentation for the following:

$ARGUMENTS

**YOU MUST USE THE `git/git-comment` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- A structured comment with **High Level Summary** and **Specific Details** sections
- Per-file breakdown of changes with key logic explained
- Breaking changes and migration notes highlighted
- Success criteria: Complete, accurate, well-formatted commit documentation

## Context

- **Required skill**: `git/git-comment` — you loaded this above
- Analyze PRs, commits, or branch diffs to produce documentation

## Requirements

### MUST DO:

- Follow `git/git-comment` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.claude/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: Follow naming/architecture conventions when analyzing code
  - `unity-asset-rules.md`: Understand asset conventions when documenting asset-related changes

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Leave documentation incomplete or inaccurate

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
