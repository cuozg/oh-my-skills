---
description: Refactor Unity C# code - extract, rename, restructure, decouple
agent: sisyphus
skill: unity-refactor
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity-refactor/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Perform the requested refactoring:

$ARGUMENTS

**YOU MUST USE THE `unity-refactor` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Code safely refactored without changing functionality
- All callers and dependencies identified and updated
- No compiler errors (verified with `lsp_diagnostics`)
- Success criteria: Behavior preserved, code improved, zero regressions

## Context

- **Required skill**: `unity-refactor` — you loaded this above
- Refactoring types: extract, rename, restructure, simplify, decouple, replace anti-patterns, move, clean up, optimize

## Requirements

### MUST DO:

- Follow `unity-refactor` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Investigate before changing — understand all callers and dependencies
- Use LSP tools (find references, goto definition) to ensure safety
- Run `lsp_diagnostics` on changed files after each change
- Preserve existing behavior — refactoring must not change functionality
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.opencode/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, use `unityMCP` over shell, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: PascalCase classes/methods, _camelCase private fields, SRP components, Awaitable over Coroutines
  - `unity-asset-rules.md`: Follow `Assets/_Project/` structure, PascalCase naming, Prefab workflow

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Change functionality while refactoring
- Leave code in broken state
- Use shell commands for Unity Editor tasks (use `unityMCP` instead)

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
