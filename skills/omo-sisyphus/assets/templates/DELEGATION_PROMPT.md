## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`.claude/skills/{skill-name}/SKILL.md`

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

## Requirements

### MUST DO:
- Follow `{skill-name}` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run lsp_diagnostics on changed files
- Verify build/tests pass
- Use `/handoff` if context is getting long (before compaction strikes)

### MUST NOT DO:
- **NEVER commit or push to git** (non-negotiable)
- Skip loading the skill first
- Ignore the loaded skill instructions
- Suppress type errors with `as any`, `@ts-ignore`
- Refactor while fixing bugs
- Leave code in broken state

---

<!--
DELEGATION CONSTRAINT (for the orchestrator, not the subagent):
This prompt MUST be sent via:
  call_omo_agent(subagent_type="sisyphus", ...)
Using any other subagent_type is FORBIDDEN.
-->
