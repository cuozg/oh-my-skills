## Task
{Clear, atomic description of what to accomplish}

**YOU MUST USE THE `{skill-name}` SKILL** that has been loaded for you.
Follow the skill's instructions exactly.

## Expected Outcome
- {Concrete deliverable 1}
- {Concrete deliverable 2}
- Success criteria: {what "done" looks like}

## Context
- Existing patterns: {reference files}
- Constraints: {tech stack, style}
- **Loaded skill**: `{skill-name}` - {brief description}
- **Session context**: {previous session_id if follow-up, or "new delegation"}

## Metadata (v3.3.0 — for transparency and inspectability)
- **Delegation reason**: {why this task is being delegated}
- **Skill justification**: {why these skills were selected/omitted}
- **Background/Sync decision**: {why this execution mode was chosen}
- **Parent session**: {orchestrator session_id for traceability}

## Requirements

### MUST DO:
- **FOLLOW `{skill-name}` skill instructions**
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run lsp_diagnostics on changed files
- Verify build/tests pass
- Store session_id for potential follow-up continuity

### MUST NOT DO:
- Ignore the loaded skill instructions
- Suppress type errors with `as any`, `@ts-ignore`
- Commit unless explicitly requested
- Refactor while fixing bugs
- Leave code in broken state
