---
name: goal-create
description: >
  An interactive goal creation, update, and tracking skill that writes structured goal files to Docs/Goals/{feature-name}/{kebab-case-task}.md with acceptance criteria.
  Use for defining NEW goals, updating EXISTING goals, or scoping vague requests into concrete goals.
metadata:
  author: kuozg
  version: "1.0"
---
# Goal Create — Interactive Goal Creator

You transform user intent into precise, unambiguous goal files with concrete acceptance criteria. You must ask focused clarifying questions, not guess.

## Workflow

### 1. Understand the Request

Read user input. Identify objective, domain, and constraints.

***INSTRUCTION***
Interview user relentlessly about every aspect of this goal until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

If a question can be answered by exploring the codebase, explore the codebase instead.

### 2. Check for Duplicates

Recursively scan `Docs/Goals/` for existing goals matching the intent. If found, suggest updating instead of creating a new one.

### 3. Assess Scope, Size, and Feature

- Extract feature name (e.g. `[Authentication]`), folder becomes `authentication/`.
- Break down large goals (taking >3 days or >7 criteria) into smaller, independent goals.
- Identify dependencies between goals.

### 4. Draft the Goal

Use the template provided in `references/goal-template.md`.

### 5. Self-Review

- Review goal against rules independently.
- Fix issues inline.
- Repeat until review is passed.

### 6. Write Document

- Write to `Docs/Goals/{feature-name}/{kebab-case-task}.md`.