---
description: Implement C# game logic with Unity best practices
agent: sisyphus
skill: unity/unity-code
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-code/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Implement the requested feature:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-code` SKILL** that has been loaded.
Follow the skill's instructions exactly.

If a plan exists in `Documents/Plans/` or `Documents/Tasks/`, follow it exactly.

## Expected Outcome

- Clean, commented, performant C# code implementing the requested feature
- Code follows project conventions and Unity best practices
- No compiler errors (verified with `lsp_diagnostics`)
- Success criteria: Feature implemented, compiles cleanly, follows conventions

## Context

- **Required skill**: `unity/unity-code` — you loaded this above
- Follow project conventions from `.opencode/rules/unity-csharp-conventions.md`
- Follow asset rules from `.opencode/rules/unity-asset-rules.md`

## Requirements

### MUST DO:

- Follow `unity/unity-code` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run `lsp_diagnostics` on changed files
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Verify build/tests pass
- Use Unity 6 features where appropriate (Awaitable, New Input System)
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.opencode/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, use `unityMCP` over shell, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: PascalCase classes/methods, _camelCase private fields, SRP components, Awaitable over Coroutines, avoid Update(), cache references
  - `unity-asset-rules.md`: Follow `Assets/_Project/` structure, PascalCase naming, texture/model optimization, Prefab workflow

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Suppress type errors
- Use anti-patterns: polling in Update, magic numbers, tight coupling, GC allocations in hot paths
- Leave code in broken state
- Use shell commands for Unity Editor tasks (use `unityMCP` instead)

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
