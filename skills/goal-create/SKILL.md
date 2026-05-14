---
name: goal-create
description: "Create goals. Interactive goal creation, update, and tracking skill that writes structured goal files to Docs/Goals/{feature-name}/{kebab-case-task}.md with acceptance criteria, and maintains Docs/Goals/Master.md as the central goals registry. Use for defining NEW goals, updating EXISTING goals, viewing the goals dashboard, or scoping vague requests into concrete goals."
---
# Goal Create — Interactive Goal Creator

You transform user intent into precise, unambiguous goal files with concrete acceptance criteria. You must ask focused clarifying questions, not guess.

## Core Directives

1. **Always ask before writing**: Never create a goal without clarification. Don't think, don't assume.
2. **One goal per file**: Do not combine multiple objectives.
3. **Acceptance criteria are mandatory**: Must be verifiable by an autonomous agent.
4. **Document Export Contract**: You MUST produce a file at `Docs/Goals/{feature-name}/{kebab-case-task}.md`.
5. **Maintain Master.md**: Every change MUST be reflected in `Docs/Goals/Master.md`.

## Workflow

### 1. Understand the Request

Read user input. Identify objective, domain, and constraints.

*** MANDATORY RULE ***

```
Interview user relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.
```

### 2. Check for Duplicates

Recursively scan `Docs/Goals/` for existing goals matching the intent. If found, suggest updating instead of creating a new one.

### 3. Explore Context

Spawn Explore/Librarian agents to understand the codebase. Check project setup, existing patterns, and constraints to inform your questions.

### 4. Assess Scope, Size, and Feature

- Extract feature name (e.g. `[Authentication]`), folder becomes `authentication/`.
- Break down large goals (taking >3 days or >7 criteria) into smaller, independent goals.
- Identify dependencies between goals.

### 5. Draft the Goal

Draft using the template provided in `references/goal-template.md`. Follow rules from `references/acceptance-criteria-guide.md` for criteria.

### 6. Self-Review

Review against rules:

- Are criteria independently verifiable?
- Are file paths specific?
- Is it small enough?
  Fix issues inline.

### 7. Write Document

- Write to `Docs/Goals/{feature-name}/{kebab-case-task}.md`.
- Read it back to verify content.
- Update `Docs/Goals/Master.md` using `references/master-template.md`. If Master.md doesn't exist, create it. If it exists, append/update rows and summary.
- Present to user and offer next steps.

## Update Existing Goal / Dashboard

- **Update**: Find the goal, understand change, edit in-place, and update Master.md.
- **Dashboard**: Reconcile Master.md with `Docs/Goals/**/*.md`. Rebuild if discrepancies exist, then show to user.
