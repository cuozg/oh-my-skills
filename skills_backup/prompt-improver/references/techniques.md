# Prompt Engineering Techniques

Compact reference for transforming raw prompts into actionable coding agent prompts.

## Techniques Summary

| # | Technique | Core Action | When to Use |
|---|---|---|---|
| 1 | Specificity | Replace vague words with names, paths, numbers | Always — vague prompts → vague results |
| 2 | Structure | Organize into Goal/Context/Requirements/Constraints/Criteria | Multi-step or complex tasks |
| 3 | Context Injection | Add file paths, patterns, data shapes, business rules | Agent lacks project knowledge |
| 4 | Constraint Definition | MUST DO / MUST NOT DO lists | Prevent assumptions and drift |
| 5 | Role Framing | Set persona/expertise | Domain-specific or review tasks |
| 6 | Chain-of-Thought | Break into numbered sequential/parallel/conditional steps | Complex multi-step tasks |
| 7 | Example Seeding | Provide input/output pairs | Format or style matters |
| 8 | Scope Bounding | Explicit In Scope / Out of Scope lists | Risk of scope creep |
| 9 | Verification Criteria | Measurable "done" conditions | Always — enables self-verification |
| 10 | Anti-Pattern Fixes | Fix vague/verbose/ambiguous prompts | Reviewing existing prompts |

## 1. Specificity — Vague Word Replacements

| Vague | Replace With |
|---|---|
| "it", "the thing" | Exact name, path, identifier |
| "better", "improve" | Measurable target or baseline |
| "handle", "deal with" | Specific action (validate, reject, retry, log) |
| "some", "a few" | Exact count or enumerated list |
| "like before" | Reference to specific file or convention |
| "clean up" | Extract method, rename, remove dead code |

## 2. Structure — Section Guide

| Task Complexity | Sections Needed |
|---|---|
| Simple (single file) | Goal + Requirements |
| Feature | Goal + Context + Scope + Requirements + Constraints |
| Bug fix | Goal + Context (repro) + Requirements + Success Criteria |
| Refactoring | Goal + Scope + Constraints + Success Criteria |
| Complex multi-step | All sections + MUST DO / MUST NOT DO |

## 3. Context Injection — Checklist

1. What files/systems are involved?
2. What patterns should be followed?
3. What has been tried/decided already?
4. What are the data shapes/types?
5. What domain rules apply?

## 4. Constraint Definition

Use `MUST DO` / `MUST NOT DO` format. Categories: style, architecture, performance, compatibility, safety, scope.

## 6. Chain-of-Thought — Patterns

- **Sequential**: Numbered steps, each depends on previous
- **Parallel**: Checkbox list, independent steps
- **Conditional**: `If X → do A, else → do B`

## 10. Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Too vague ("fix the login") | Add exact error, file path, repro steps |
| Too verbose (buried request) | Move background to Context; Goal at top |
| Missing context | Add file paths, patterns, data shapes |
| Ambiguous scope | Add In Scope / Out of Scope |
| No success criteria | Add specific, testable conditions |
| Multiple unrelated tasks | Split into separate focused prompts |
| Prescribing implementation | Specify WHAT and WHY, not HOW |
