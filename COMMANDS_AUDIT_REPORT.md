# Commands Audit Report

**Date**: 2026-02-11
**Scope**: All 16 command files in `.opencode/commands/`
**Reference**: Sisyphus Orchestrator pattern (`omo/omo-sisyphus` SKILL.md)
**Skills Audited**: 32 skills across 5 categories (read-only, NOT modified)

---

## Summary

All 16 command files have been updated to comply with the Sisyphus Orchestrator delegation pattern. Every command now includes mandatory skill loading, structured task sections, MUST DO/MUST NOT DO guardrails, git safety constraints, and delegation metadata.

**Result: 16/16 PASS**

---

## Command-to-Skill Mapping

| # | Command File | Skill | Verified |
|---|---|---|---|
| 1 | `git-comment.md` | `git/git-comment` | ✅ |
| 2 | `git-squash.md` | `git/git-squash` | ✅ |
| 3 | `unity-debug.md` | `unity/unity-debug` | ✅ |
| 4 | `unity-documentation.md` | `unity/unity-write-docs` | ✅ |
| 5 | `unity-fix-errors.md` | `unity/unity-fix-errors` | ✅ |
| 6 | `unity-implement-logic.md` | `unity/unity-code` | ✅ |
| 7 | `unity-investigate.md` | `unity/unity-investigate` | ✅ |
| 8 | `unity-mobile-deploy.md` | `unity/unity-mobile-deploy` | ✅ |
| 9 | `unity-optimize-performance.md` | `unity/unity-optimize-performance` | ✅ |
| 10 | `unity-plan.md` | `unity/unity-plan` | ✅ |
| 11 | `unity-refactor.md` | `unity/unity-refactor` | ✅ |
| 12 | `unity-review-pr-local.md` | `unity/unity-review-pr-local` | ✅ |
| 13 | `unity-review-pr.md` | `unity/unity-review-pr` | ✅ |
| 14 | `unity-test.md` | `unity/unity-test` | ✅ |
| 15 | `unity-web-deploy.md` | `unity/unity-web-deploy` | ✅ |
| 16 | `unity-write-tdd.md` | `unity/unity-write-tdd` | ✅ |

---

## Gaps Identified and Fixed

All 16 commands had the **same 8 gap categories** before the audit:

| # | Gap | Before | After |
|---|---|---|---|
| 1 | `skill:` field in YAML frontmatter | ❌ Missing | ✅ Added (e.g., `skill: unity/unity-code`) |
| 2 | `## FIRST: Load Required Skill` section | ❌ Missing | ✅ Added with exact `@.opencode/skills/<path>/SKILL.md` |
| 3 | `### MUST DO:` section | ❌ Missing | ✅ Added (todos, lsp_diagnostics, Read, /handoff, .claude/rules/) |
| 4 | `### MUST NOT DO:` section | ❌ Missing | ✅ Added (git restrictions, destructive actions guard, skill gate) |
| 5 | Git safety constraint | ❌ Missing | ✅ "NEVER commit or push to git" in every command |
| 6 | Destructive action guard | ❌ Missing | ✅ "NEVER perform destructive actions without confirmation" |
| 7 | `/handoff` context preservation | ❌ Missing | ✅ "Use /handoff if context is getting long" |
| 8 | `.claude/rules/` compliance | ❌ Missing | ✅ All 3 rules referenced: agent-behavior, unity-csharp-conventions, unity-asset-rules |
| 9 | Delegation constraint comment | ❌ Missing | ✅ HTML comment with `call_omo_agent(subagent_type="sisyphus", ...)` |

---

## Compliance Checklist

Each command was verified against all required elements:

| Element | All 16 Commands |
|---|---|
| YAML `description:` | ✅ |
| YAML `agent: build` | ✅ |
| YAML `skill:` | ✅ |
| `## FIRST: Load Required Skill` | ✅ |
| Correct `@.opencode/skills/<path>/SKILL.md` reference | ✅ |
| `## Task` with `$ARGUMENTS` | ✅ |
| Skill enforcement reminder in Task | ✅ |
| `## Expected Outcome` with success criteria | ✅ |
| `## Context` with required skill reference | ✅ |
| `### MUST DO:` — skill compliance | ✅ |
| `### MUST DO:` — todo creation | ✅ |
| `### MUST DO:` — `Read` modified files | ✅ |
| `### MUST DO:` — `/handoff` mention | ✅ |
| `### MUST DO:` — `.claude/rules/` compliance (3 rules) | ✅ |
| `### MUST NOT DO:` — git restrictions | ✅ |
| `### MUST NOT DO:` — destructive actions guard | ✅ |
| `### MUST NOT DO:` — skill loading gate | ✅ |
| HTML delegation constraint comment | ✅ |

---

## Before/After Structure

### BEFORE (typical command structure)
```markdown
---
description: <description>
agent: build
---

<task instructions>
$ARGUMENTS
```

### AFTER (Sisyphus-compliant structure)
```markdown
---
description: <description>
agent: build
skill: <category>/<skill-name>
---

## FIRST: Load Required Skill
**BEFORE you do anything**, you MUST read and follow this skill:
`@.opencode/skills/<category>/<skill-name>/SKILL.md`

## Task
<task description>
$ARGUMENTS
**YOU MUST USE THE `<skill>` SKILL** that has been loaded.

## Expected Outcome
- <concrete deliverables>
- Success criteria: <what done looks like>

## Context
- **Required skill**: `<skill>` — you loaded this above

## Requirements
### MUST DO:
- Follow skill EXACTLY
- Create todos, mark progress
- Run lsp_diagnostics, Read modified files
- /handoff if context long
- Comply with .claude/rules/

### MUST NOT DO:
- NEVER commit or push to git
- NEVER destructive actions without confirmation
- Skip skill loading

<!-- DELEGATION CONSTRAINT: call_omo_agent(subagent_type="sisyphus", ...) -->
```

---

## Domain-Specific Customizations

While all commands follow the same base pattern, each includes **domain-specific details** in MUST DO/MUST NOT DO:

| Command | Domain-Specific Additions |
|---|---|
| `git-squash` | NEVER force push main/master, NEVER modify pushed commits |
| `unity-debug` | Suppress type errors ❌, Refactor while fixing ❌, Use unityMCP |
| `unity-fix-errors` | Suppress type errors ❌, Refactor while fixing ❌, Verify build/tests |
| `unity-implement-logic` | No anti-patterns (polling Update, magic numbers, tight coupling, GC in hot paths) |
| `unity-investigate` | Provide code refs with file paths/line numbers, no assumptions without evidence |
| `unity-mobile-deploy` | Mobile budgets (ASTC 6x6, <100k tris), backward compatibility |
| `unity-optimize-performance` | Profile first then fix, Object Pooling, LOD, texture budgets |
| `unity-plan` | Skip codebase investigation ❌, plans need acceptance criteria |
| `unity-refactor` | Use LSP tools, preserve behavior, no functionality changes |
| `unity-review-pr-local` | LOCAL only — never post to GitHub |
| `unity-review-pr` | Post review comments directly on GitHub PR |
| `unity-test` | Test naming convention, Edit/Play Mode selection, mock dependencies |
| `unity-documentation` | Investigate codebase before writing |
| `unity-write-tdd` | Reference existing patterns, include code snippets |

---

## Files NOT Modified

The following were read for reference but **NOT modified** (read-only audit):

- All 32 skill `SKILL.md` files in `.opencode/skills/`
- `.opencode/skills/omo/omo-sisyphus/SKILL.md` (canonical pattern)
- `.opencode/skills/omo/omo-sisyphus/assets/templates/DELEGATION_PROMPT.md` (template)
- `.claude/rules/agent-behavior.md`
- `.claude/rules/unity-csharp-conventions.md`
- `.claude/rules/unity-asset-rules.md`

---

## Verification

All 16 command files were:
1. ✅ Read before editing (to understand original structure)
2. ✅ Updated with Sisyphus-compliant pattern
3. ✅ Read again after editing (Atlas manual review verification)
4. ✅ Verified against 18-point compliance checklist

**Audit complete. All 16 commands are Sisyphus-compliant.**
