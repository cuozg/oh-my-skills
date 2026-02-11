---
description: Find and fix Unity performance bottlenecks (FPS, memory, load times)
agent: build
skill: unity/unity-optimize-performance
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-optimize-performance/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Optimize the specified area:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-optimize-performance` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Performance bottlenecks identified and fixed (CPU, Memory, Loading, Rendering, or Mobile)
- Targeted optimizations applied with measurable impact
- No functionality broken by optimizations
- Success criteria: Measurable performance improvement, verified with `lsp_diagnostics`

## Context

- **Required skill**: `unity/unity-optimize-performance` — you loaded this above
- Optimization areas: CPU frame time, memory/GC, scene loading, rendering/draw calls, mobile budgets

## Requirements

### MUST DO:

- Follow `unity/unity-optimize-performance` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Profile first, then fix — never optimize blindly
- Match existing codebase patterns
- Run `lsp_diagnostics` on changed files
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Verify build/tests pass
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.claude/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, use `unityMCP` over shell, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: Avoid Update(), cache references, avoid GC allocations in hot paths, use Object Pooling
  - `unity-asset-rules.md`: Texture optimization (max 2048 mobile/4096 PC), model budgets (<100k tris mobile), LOD

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Optimize without profiling first
- Break functionality while optimizing
- Leave code in broken state
- Use shell commands for Unity Editor tasks (use `unityMCP` instead)

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
