---
name: goal-detail
description: >
  Expand a goal-create file into a detailed, implementation-ready task breakdown. Use when a user has
  a goal under Docs/Goals and wants it expanded into per-Task blocks (files, interfaces, code snippets,
  bash commands, acceptance criteria) ready to hand to goal-execute. Triggers: "detail this goal",
  "expand the goal", "break the goal into tasks", "create task breakdown", "plan the goal",
  "write implementation steps for this goal", "make an epic-style plan from this goal".
  Do not use for executing the goal, writing test cases, or verifying completed work.
metadata:
  author: kuozg
  version: "1.0"
---

# Goal Detail

Take one `goal-create` output and produce a per-Task implementation breakdown, modeled on the
`Epic-NN-*.md` documents in `Docs/Features/TacticsMode/plan/`.

## Output contract

- Write exactly one Markdown file.
- Default path: `Docs/Goals/{feature-name}/detail/{kebab-case-task}.md`.
- Preserve the source goal file unchanged.
- Use the structure in `references/task-template.md`.
- One Task per logical commit; one Task = one goal-execute run.

## Workflow

### 1. Resolve the input

- If a path is provided, read that goal file in full.
- If not, scan `Docs/Goals/` for goals with `status: pending` and pick the most recent;
  if multiple plausible candidates, ask the user which one to expand.
- Parse frontmatter (`status`, `priority`, `depends_on`), `## Acceptance criteria`,
  `## Key interfaces`, `## Desired behavior`, `## Current behavior`, `## Out of scope`.

### 2. Gather context

- Read the parent feature spec when one exists:
  `Docs/Features/{feature-name}/TacticsModeGDD.md` or equivalent.
- Read the parent TODO if one exists:
  `Docs/Features/{feature-name}/TacticsMode-todo.md` (carries feature-level grouping).
- Read sibling detail files in `Docs/Goals/{feature-name}/detail/` to avoid Task-id collisions
  and reuse Task-id numbering (T-1, T-2, ...).
- Index the actual codebase to verify every file path, line number, signature, and class
  the goal references. If a reference is wrong or stale, mark it `TODO: verify path` in
  the output and surface the conflict to the user — never silently invent paths.
- For Unity: split client vs server references per the `AGENTS.md` rule
  (server logic in `WWEBattleServer`, client in `WP_Unity_Live`).

### 3. Plan the Task split

Group the goal's acceptance criteria into the smallest Tasks that are:

- independently verifiable (each Task has its own Acceptance block)
- atomic (one Task = one commit; a fresh agent should be able to ship it in one session)
- ordered by dependency (Task N+1 may depend on Task N's interfaces)

Each Task gets a stable id (`T-1`, `T-2`, ...). When the goal carries cross-repo work,
add a `-mirror` suffix for the client half (`T-1-mirror`) and a `-parse` suffix for
wire parsers, mirroring the convention in `Epic-03-Damage-Credit.md`.

### 4. Write the detail document

For every Task, fill these blocks (see `references/task-template.md`):

- **Files** — absolute paths, line numbers, action verb (`Create` / `Modify` / `Delete`).
- **Interfaces** — Consumes: ... / Produces: ... with type signatures.
- **Steps** — numbered checkboxes `- [ ]` with code in fenced blocks (csharp/xml/bash).
  Each step = one logical change. Cite `file:line` for existing code that is replaced.
- **Acceptance** — one bullet per verifiable outcome, copied/refined from the goal's
  acceptance criteria, plus any extra criteria the Task split adds.
- **Commit** — one bash block per Task with `git add` + a clean imperative message.

After the last Task, add a **Cross-Repo Notes** section when the work spans both
`WWEBattleServer` and `WP_Unity_Live` (e.g. enum mirrored on both sides, JSON config
parser changes that must match). End with a **Verification** block listing the final
invariants the whole detail doc must satisfy.

### 5. Self-check before reporting

Verify that:

- every goal acceptance criterion maps to one or more Task acceptance items
- every Task has at least one Acceptance bullet, one commit, and one bash build/test line
- file paths and line numbers were re-verified against the current source
- Tasks are ordered so dependents come last
- no implementation code was changed
- output path follows `Docs/Goals/{feature-name}/detail/{kebab-case-task}.md`

Report the output path, Task count, and the highest-severity risk surfaced.

## Rules

- Planning only — never run `git commit`, `dotnet build`, or `dotnet test`.
- Re-verify every file path and line number against the actual codebase before writing.
- When the goal conflicts with the current codebase, surface the conflict in the
  detail doc as a `TODO: verify` callout; do not pick a side silently.
- Do not duplicate content from sibling detail files. Reference them by Task id instead.
- Match the verb density of the existing `Docs/Features/TacticsMode/plan/Epic-*.md` files —
  imperative, file-anchored, code-first, no essay paragraphs.
