---
description: Create and run Unity tests with Edit/Play Mode support
agent: sisyphus
skill: unity/unity-test
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-test/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Create tests for the specified target:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-test` SKILL** that has been loaded.
Follow the skill's instructions exactly.

## Expected Outcome

- Comprehensive test suites covering happy path, edge cases, error handling, and integration points
- Appropriate test mode used (Edit Mode for logic, Play Mode for runtime)
- Dependencies mocked where needed for isolation
- Tests compile cleanly (verified with `lsp_diagnostics`)
- Success criteria: Tests pass, cover critical paths, follow Unity Test Framework conventions

## Context

- **Required skill**: `unity/unity-test` — you loaded this above
- Test framework: NUnit attributes, Assert patterns, Unity Test Framework conventions

## Requirements

### MUST DO:

- Follow `unity/unity-test` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Analyze target code to understand testable behaviors
- Use appropriate test mode (Edit Mode for logic, Play Mode for runtime)
- Mock dependencies where needed for isolation
- Run `lsp_diagnostics` on changed files
- Use `Read` on every modified file before reporting completion _(Atlas manual review requirement)_
- Use `/handoff` if context is getting long (before compaction strikes)
- **Comply with all `.claude/rules/`** — specifically:
  - `agent-behavior.md`: Safety First, Proactive suggestions, Discover → Plan → Execute → Collaborate
  - `unity-csharp-conventions.md`: Test naming `[Subject]_[Scenario]_[ExpectedResult]`, `Tests/EditMode/` and `Tests/PlayMode/`
  - `unity-asset-rules.md`: Follow `Assets/_Project/` structure for test placement

### MUST NOT DO:

- **NEVER commit or push to git** (non-negotiable)
- **NEVER perform destructive actions** (file/asset deletion, scene overwrites) without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Write tests that don't compile
- Leave tests incomplete or non-functional

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
