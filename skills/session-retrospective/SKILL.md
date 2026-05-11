---
name: session-retrospective
description: "Post-session retrospective engine — automatically triggered after a session or task completes. Reads what was done, identifies patterns, gaps, and recurring friction, then improves the relevant skills and standards so the next similar task runs better. Use when the user says 'retrospective', 'improve the skills', 'learn from this session', 'make it better next time', 'post-mortem', 'update skills', or when invoked via /omo/retrospective. Also triggered automatically after every session idle event. ALWAYS use this skill for any request about learning from completed work and upgrading agent capabilities."
---

# Session Retrospective — Continuous Improvement Engine

You are an agent trainer. Output: improved SKILL.md files and reference docs — not code changes.

## Workflow

### Phase 1 — Analyze Session

Read the session conversation. Identify:
- Main task, skills/agents used, tools called
- Where the agent hesitated, backtracked, retried, or asked unnecessary questions
- What the user corrected or redirected
- Domain: Unity · Flutter · Git · bash · web · skills · general

Build internal Friction Report (do not show user unless asked):
```
Domain: <domain>  |  Skills used: <list>
Friction Points: [HIGH/MED/LOW] <specific step + tool>
What worked: <describe>
Missing in skills: <specific rule/instruction>
Improvement candidates: skills/<name>: <reason>
```

### Phase 2 — Identify Targets

| Type | Where to write |
|------|----------------|
| Missing rule | SKILL.md — Rules section |
| Missing step | SKILL.md — relevant phase |
| Wrong default | SKILL.md — amend the instruction |
| Missing reference | `references/<topic>.md` |
| New skill needed | Create via `skill-creator` |
| Standards update | Relevant `*-standards` skill |

Skip improvements that are: too session-specific · already covered · micro-optimizations with negligible impact.

### Phase 3 — Execute (Surgical Edits Only)

- **SKILL.md edits:** add the missing rule/step/correction only. Preserve voice and style. Explain the why in 1 sentence.
- **New reference file:** `skills/<name>/references/<topic>.md` with brief header, patterns, anti-patterns, cross-ref.
- **Standards update:** append discovered conventions matching existing format.
- **New skill (rare):** only for a whole new recurring domain. Use `skill-creator`.

### Phase 4 — Verify & Report

Re-read every modified SKILL.md: content integrates naturally · no contradictions · no scope expansion · still concise.

Report to user:
```
## 🔁 Session Retrospective Complete
Skills improved: <count>
| Skill | Change Type | Summary |
| <name> | Missing rule | Added: "Always X before Y" |
Key Lessons: <1-line each>
What's Better Next Time: <task type> → <how it improves>
```

## Rules

1. Never ask the user for input — analyze from session history
2. Never modify code files — only skills and reference docs
3. Never expand skill scope beyond its existing domain
4. Always read before writing
5. Always run Phase 4 verification
6. Never rewrite a working skill — surgical edits only
7. Always report what changed and why

## Improvement Principles

- **Generalize:** one bad event → a rule preventing the whole class of problem
- **Explain why:** smart agents follow reasoning better than mandates
- **Keep lean:** remove obvious instructions, add only what changes behavior
- **Never overfit:** look for the pattern beneath the mistake
- **Test counterfactual:** "If this rule existed, would the friction have been prevented?"
