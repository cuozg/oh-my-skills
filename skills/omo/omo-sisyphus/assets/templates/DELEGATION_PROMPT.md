## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill.

Load the skill from: `{skill-path}`

> **Path Resolution**: The skill path above is an absolute filesystem path.
> If loading fails, try these fallback resolutions in order:
> 1. Absolute path as-is: `{skill-path}`
> 2. Project-relative: `<project-root>/.opencode/skills/{category}/{skill-name}/SKILL.md`
> 3. Skill name lookup: use `skill(name="{category}/{skill-name}")` tool
>
> **IMPORTANT**: Skills live under `.opencode/skills/`, NOT `.claude/skills/`.

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task
{Clear, atomic description - one action per delegation}

**YOU MUST USE THE `{skill-name}` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome
- {Concrete deliverable 1}
- {Concrete deliverable 2}
- Success criteria: {what "done" looks like}

## Context
- Existing patterns: {reference files}
- Constraints: {tech stack, style}
- **Required skill**: `{skill-name}` - you loaded this above
- **Skill location**: `.opencode/skills/{category}/{skill-name}/SKILL.md`

## Requirements

### MUST DO:
- Follow `{skill-name}` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run lsp_diagnostics on changed files
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Verify build/tests pass
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.opencode/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, use `unityMCP` over shell, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: PascalCase classes/methods, _camelCase private fields, SRP components, Awaitable over Coroutines, avoid Update(), cache references
  - `unity-asset-rules.md`: Follow `Assets/_Project/` structure, PascalCase naming, texture/model optimization, Prefab workflow (nested, variants, verify in Prefab Mode)

### MUST NOT DO:
- **NEVER push to git remotes or add AI metadata to commits** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Suppress type errors with `as any`, `@ts-ignore`
- Refactor while fixing bugs
- Leave code in broken state
- Use shell commands for Unity Editor tasks (use `unityMCP` instead)

---

## Path Format Reference

### Skill Paths
Skills are located under `.opencode/skills/` with this structure:
```
.opencode/skills/{category}/{skill-name}/SKILL.md
```
Categories: `unity/`, `omo/`, `other/`, `bash/`, `git/`

### Asset DEEPLINK Paths
Unity asset references use `@` prefix with project-relative paths:
```
@Assets/Scripts/Path/To/Script.cs
```
These are resolved relative to the Unity project root, NOT the skill directory.

### Rule Paths
Project rules are at `.opencode/rules/`:
```
.opencode/rules/agent-behavior.md
.opencode/rules/unity-csharp-conventions.md
.opencode/rules/unity-asset-rules.md
```

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
