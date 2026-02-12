---
description: WebGL build configuration, browser optimization, and deployment
agent: sisyphus
skill: unity/unity-web-deploy
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-web-deploy/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Handle WebGL deployment:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-web-deploy` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- WebGL deployment task completed (build config, C#/JS interop, browser optimization, PWA, or hosting)
- Browser-specific quirks handled (audio autoplay, WebGL context loss)
- Optimized for download size and initial load time
- Success criteria: Build succeeds, runs across major browsers, meets performance targets

## Context

- **Required skill**: `unity/unity-web-deploy` — you loaded this above
- Scope: build configuration, C#/JS interop, browser optimization, PWA features, hosting

## Requirements

### MUST DO:

- Follow `unity/unity-web-deploy` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run `lsp_diagnostics` on changed files
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.opencode/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, use `unityMCP` over shell, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: PascalCase classes/methods, _camelCase private fields, SRP components
  - `unity-asset-rules.md`: Follow asset optimization guidelines for WebGL builds

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Leave code in broken state
- Use shell commands for Unity Editor tasks (use `unityMCP` instead)

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
