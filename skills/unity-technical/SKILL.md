---
name: unity-technical
description: >
  Create Unity technical solution documents from user requirements, feature ideas, bug goals, specs,
  or codebase problems. Use when the user asks for a technical approach, architecture, implementation
  strategy, solution options, feasibility analysis, system design, or "how should we build/fix this"
  for Unity runtime, Editor, tools, assets, data, UI, WebGL, SDKs, or production pipelines.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-technical

Turn a Unity requirement into a shared technical understanding and a decision-ready solution document.

**Required output:** Read and follow `references/output-template.md`.

## Workflow

### 1. Capture the Goal
- Extract the desired outcome, constraints, success criteria, target platform, quality bar, and deadline.
- Read every user-provided document, spec, screenshot summary, log, or linked local file before asking.
- If the request names existing code, scenes, prefabs, packages, or systems, inspect them first.

### 2. Explore Before Asking
- Search the codebase for relevant systems, call paths, assets, tests, settings, and conventions.
- Use `explore` subagents when the answer spans multiple files or systems.
- Research Unity best practices, official docs, package guidance, and production patterns when the solution depends on Unity APIs, tooling, performance, platform behavior, or third-party packages.
- If codebase exploration can answer a question, do that before asking the user.

### 3. Interview Relentlessly
- Ask precise questions until the requirement is unambiguous enough to design.
- Include suggested answers or tradeoff-based options for each question.
- Ask one decision group at a time: player outcome, content/data model, runtime flow, editor workflow, platform constraints, testing, rollout.
- Stop interviewing only when both you and the user can state the same problem, boundaries, and acceptance criteria.

### 4. Generate Multiple Approaches
- Provide at least two viable technical approaches; include a minimal 80/20 option whenever possible.
- Explain which approach you prefer, why, and when that preference would change.
- Compare tradeoffs: effort, risk, extensibility, performance, maintainability, testability, designer workflow, and migration cost.
- Do not hide uncertainty; mark assumptions and unknowns clearly.

### 5. Write the Technical Document
- Use `references/output-template.md` exactly as the structure unless the user requests another format.
- Ground claims in evidence: cite codebase files, Unity docs, package docs, or observed project settings.
- Include implementation steps, affected files/systems, verification plan, and open decisions.
- Keep the document practical enough that another engineer can implement from it.

## Rules

- Do not implement unless the user explicitly asks; this skill designs the technical solution.
- Do not speculate about existing code; inspect it or label the point unknown.
- Prefer simple, shippable designs over abstract architecture.
- If no saved document path is specified, ask whether to save it or provide the document inline.
