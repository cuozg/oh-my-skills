---
description: Diagnose and fix Unity compiler errors, exceptions, and build failures
agent: sisyphus
skill: unity/unity-fix-errors
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-fix-errors/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Fix the reported errors:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-fix-errors` SKILL** that has been loaded.
Follow the skill's instructions exactly.

If no specific errors are mentioned, check for compiler errors using `lsp_diagnostics` and Unity console logs.

## Expected Outcome

- All errors identified, diagnosed, and fixed
- Fixes compile cleanly (verified with `lsp_diagnostics`)
- Report of what was fixed and why
- Success criteria: Zero compiler errors, no regressions introduced

## Context

- **Required skill**: `unity/unity-fix-errors` — you loaded this above
- Check Unity console logs, compiler output, or user-provided stack traces

## Requirements

### MUST DO:

- Follow `unity/unity-fix-errors` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run `lsp_diagnostics` on changed files
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Verify build/tests pass
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.claude/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, use `unityMCP` over shell, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: PascalCase classes/methods, _camelCase private fields, SRP components, Awaitable over Coroutines, avoid Update(), cache references
  - `unity-asset-rules.md`: Follow `Assets/_Project/` structure, PascalCase naming, Prefab workflow

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Suppress type errors
- Refactor while fixing bugs
- Leave code in broken state
- Use shell commands for Unity Editor tasks (use `unityMCP` instead)

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
