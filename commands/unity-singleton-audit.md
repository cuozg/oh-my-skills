---
description: Audit Singleton<T> usage — detect circular dependencies, unsafe access, and anti-patterns
agent: sisyphus
skill: unity/unity-singleton-auditor
subtask: true
---

## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/unity/unity-singleton-auditor/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task

Audit Singleton usage in the project:

$ARGUMENTS

**YOU MUST USE THE `unity/unity-singleton-auditor` SKILL** that has been loaded.
Follow the skill's instructions exactly.

If no specific focus is mentioned, run the full audit (dependencies, null-checks, init-order, anti-patterns).

## Expected Outcome

- Singleton registry listing all Singleton<T> classes
- Dependency graph with circular dependency detection
- Unsafe access points identified (missing null-checks)
- Anti-pattern violations flagged with severity
- Prioritized recommendations saved to `Documents/Audits/`

## Context

- **Required skill**: `unity/unity-singleton-auditor` — you loaded this above
- **Audit script**: `.opencode/skills/unity/unity-singleton-auditor/scripts/audit_singletons.py`
- **Project uses**: `Singleton<T>` base class extensively (100+ singletons)
- **Key pattern**: `Instance` property access, `HasInstance` checks

## Requirements

### MUST DO:

- Follow `unity/unity-singleton-auditor` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Run the audit script first, then analyze results
- Use LSP tools to verify critical findings
- Generate a markdown report in `Documents/Audits/`
- Use `/handoff` if context is getting long
- **Comply with all `.claude/rules/`**

### MUST NOT DO:

- **NEVER commit or push to git**
- **NEVER modify any Singleton code** — this is a read-only audit
- **NEVER perform destructive actions** without explicit user confirmation
- Skip loading the skill first
- Refactor while auditing
