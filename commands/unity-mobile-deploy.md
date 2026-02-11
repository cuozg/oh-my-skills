---
description: iOS/Android build configuration, optimization, and deployment
agent: build
skill: unity/unity-mobile-deploy
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-mobile-deploy/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Handle mobile deployment:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-mobile-deploy` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Mobile deployment task completed (touch controls, optimization, native features, or build pipeline)
- Platform-specific requirements addressed (iOS App Store / Google Play)
- Performance within mobile budget constraints
- Success criteria: Build succeeds, passes platform requirements, runs within resource budgets

## Context

- **Required skill**: `unity/unity-mobile-deploy` — you loaded this above
- Scope: touch controls, mobile optimization, native features (IAP, notifications), build pipeline (Xcode/Gradle)

## Requirements

### MUST DO:

- Follow `unity/unity-mobile-deploy` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run `lsp_diagnostics` on changed files
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Consider backward compatibility
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.claude/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, use `unityMCP` over shell, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: PascalCase classes/methods, _camelCase private fields, SRP components
  - `unity-asset-rules.md`: Textures max 2048 mobile (ASTC 6x6), models <100k tris/scene, follow `Assets/_Project/` structure

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
