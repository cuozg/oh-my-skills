---
description: Deep investigation and debugging of Unity errors with root cause analysis
agent: sisyphus
skill: unity-debug
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity-debug/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Perform a deep debug investigation:

$ARGUMENTS

**YOU MUST USE THE `unity-debug` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Root cause identified (not just symptoms)
- Detailed debug report with reproduction steps, root cause analysis, affected systems
- Recommended fix with code changes
- Fix applied if straightforward, or escalated with detailed findings
- Success criteria: Root cause understood, fix verified or clear action plan provided

## Context

- **Required skill**: `unity-debug` — you loaded this above
- Input may include: stack traces, error messages, unexpected behavior descriptions, reproduction steps

## Requirements

### MUST DO:

- Follow `unity-debug` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run `lsp_diagnostics` on changed files
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Verify build/tests pass
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.opencode/rules/`** — specifically:
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
