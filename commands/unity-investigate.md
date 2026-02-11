---
description: Deep-dive code analysis of Unity systems, logic flow, and architecture
agent: sisyphus
skill: unity/unity-investigate
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-investigate/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Perform a deep investigation:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-investigate` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Comprehensive analysis covering: architecture overview, execution flow, data flow, dependencies
- Key entry points identified and traced
- Potential issues or improvement opportunities surfaced
- Code references with file paths and line numbers
- Success criteria: System fully understood, documented with evidence

## Context

- **Required skill**: `unity/unity-investigate` — you loaded this above
- Investigate all applicable areas: logic flow, data structures, resource management, system interactions, side effects, performance

## Requirements

### MUST DO:

- Follow `unity/unity-investigate` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Trace execution from trigger to outcome
- Provide code references with file paths and line numbers
- Use `Read` on every analyzed file to ensure accuracy
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.claude/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: Understand and reference naming/architecture conventions
  - `unity-asset-rules.md`: Understand asset conventions when analyzing resource management

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Provide analysis without reading the actual code
- Make assumptions without evidence

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
