---
description: Analyze Unity console logs — classify errors, group duplicates, suggest fixes
agent: sisyphus
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity-log-analyzer/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Analyze the Unity console logs:

$ARGUMENTS

**YOU MUST USE THE `unity-log-analyzer` SKILL** that has been loaded.
Follow the skill's instructions exactly.

If no specific logs are provided, fetch them from the Unity Editor using `coplay-mcp_get_unity_logs`.

## Expected Outcome

- Logs parsed and classified by category (NullRef, MissingComponent, Network, etc.)
- Duplicate errors grouped with occurrence counts
- Fix suggestions for each error pattern
- Priority ranking from Critical to Low
- Summary report with actionable recommendations

## Context

- **Required skill**: `unity-log-analyzer` — you loaded this above
- **Analysis script**: `.opencode/tools/unity-log-analyzer.py`
- **Log source**: `coplay-mcp_get_unity_logs` or user-provided log text

## Requirements

### MUST DO:

- Follow `unity-log-analyzer` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Fetch logs via MCP if not provided
- Classify all errors into categories
- Group duplicates and count occurrences
- Provide fix suggestions for top errors
- Use `/handoff` if context is getting long
- **Comply with all `.opencode/rules/`**

### MUST NOT DO:

- **NEVER commit or push to git**
- **NEVER modify any code** — this is analysis only
- **NEVER perform destructive actions** without explicit user confirmation
- Skip loading the skill first
- Ignore the loaded skill instructions
- Fix errors without user confirmation (analysis only)
