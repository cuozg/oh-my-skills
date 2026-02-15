---
name: prompt-improver
description: "AI Prompt Engineer for coding agents. Auto-rewrites vague, incomplete, or poorly structured user prompts into optimized, actionable prompts that maximize agent success. Scores prompts on 5 dimensions (Specificity, Context, Constraints, Success Criteria, Actionability), then produces an improved version with structured sections. Use when: (1) User prompt is vague or underspecified, (2) Task requires multiple steps but prompt lacks structure, (3) Prompt missing success criteria or constraints, (4) Delegating complex work to sub-agents, (5) Prompt lacks technical context needed for implementation, (6) User wants to maximize first-attempt success rate. Triggers: 'improve prompt', 'rewrite prompt', 'optimize prompt', 'prompt engineer', 'make this prompt better', 'refine this request', 'structure this task', 'enhance prompt', 'prompt quality', 'prompt score'."
---

# Prompt Improver

Transform raw user requests into structured, actionable prompts for any coding agent.

## Input
Raw user prompt (vague one-liner, unstructured request, or prompt for sub-agent delegation).

## Output
Score Card (5 dimensions) + Improved Prompt + Changes Summary + Assumptions list.

## Workflow

### Step 1: Score Original (1-3 scale per dimension)

| Dimension | 1 (Weak) | 3 (Strong) |
|---|---|---|
| Specificity | Vague, no details | Precise scope, named targets |
| Context | No background | Full tech stack, file paths |
| Constraints | No boundaries | Clear boundaries, edge cases |
| Success Criteria | No definition of done | Explicit, verifiable outcomes |
| Actionability | Can't start without questions | Execute immediately |

**Total** (5-15): 5-8 = critical rewrite, 9-11 = improve, 12-15 = minor polish.

### Step 2: Rewrite (FIRST — no clarifying questions)

1. Extract intent (WHAT not HOW)
2. Structure: Goal / Context / Requirements / Constraints / Success Criteria / Out of Scope
3. Fill gaps with `[ASSUMED: ...]` markers
4. Replace vague words with concrete actions
5. Add verifiable success criteria
6. Bound scope

Template:
```
## Goal
[1-2 sentences]
## Context
[Tech context + ASSUMED markers]
## Requirements
1. [Specific, verifiable]
## Constraints
- [Boundaries]
## Success Criteria
- [ ] [Testable outcome]
## Out of Scope
- [Excluded items]
```

### Step 3: Present
Score Card table → Improved Prompt → Changes Made (bullets) → Assumptions Made

### Step 4: Refine (Optional)
Incorporate feedback, update assumptions, re-score if significant changes.

## Quick Techniques

| Technique | Transform Example |
|---|---|
| Intent Extraction | "refactor the code" → "reduce coupling between AuthService and UserRepo" |
| Gap Filling | "fix the bug" → "fix null ref in UserController.GetProfile line 42" |
| Constraint Injection | "update the API" → "update response format; maintain v2 backward compat" |
| Success Criteria | "improve performance" → "reduce P95 from 800ms to <200ms on /search" |
| Scope Bounding | "clean up codebase" → "remove dead code in src/utils/; don't refactor working code" |

> Full catalog: `references/techniques.md` · Examples: `references/examples.md`

## Anti-Patterns

| Don't | Do Instead |
|---|---|
| Ask questions before rewriting | Rewrite with `[ASSUMED]`, let user correct |
| Over-specify implementation | Specify WHAT/WHY, not HOW |
| Skip scope boundaries | Always include Out of Scope |
| Generic "it works" criteria | Specific: "P95 < 200ms", "all tests pass" |
| Remove user's intent | Preserve intent; ADD structure |

## Adapt by Target

| Target | Emphasize | De-emphasize |
|---|---|---|
| Coding agent | File paths, criteria, constraints | Background |
| Review agent | What to look for, standards | Implementation |
| Planning agent | Goals, dependencies | Code specifics |
| Sub-agent | Complete context, skill loading | Tone |
