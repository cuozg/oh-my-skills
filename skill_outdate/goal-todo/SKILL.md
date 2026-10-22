---
name: goal-todo
description: >
  Convert a spec document into an implementation TODO list in the same spec folder. U
  se when the user says goal-todo, todo from spec, generate tasks from spec, turn this spec into todos, create implementation checklist, extract tasks, or asks to read a Docs/Specs design doc and produce what must be implemented. 
  Includes UI/UX review and codebase investigation before writing the checklist. 
  Do not use for implementing the tasks, creating new goal files, writing test cases, or verifying completed work.
metadata:
  author: kuozg
  version: "1.0"
---

# Goal Todo

Read one spec document, investigate the current product/codebase, then write an implementation checklist in the same spec folder.

## Output contract

- Write exactly one Markdown file beside the input spec unless the user gives an explicit output path.
- Default output name: `<spec-stem>-todo.md`.
- Preserve the spec file unchanged unless the user explicitly asks to update it.
- Use the exact structure in `references/todo-template.md`.

## Workflow

### 1. Resolve the input

- If the user provides a path, read that spec first.
- If no path is provided, scan `Docs/Specs/`, `Docs/Goals/`, and nearby docs for likely specs. If more than one plausible file exists, ask the user which one to use.
- Read large specs in targeted ranges, but cover every requirement-bearing section before writing.

### 2. Extract requirements

Build a private matrix from the spec:

- feature goals and user flows
- screens, UI states, empty/loading/error states, and responsive behavior
- data models, persistence, migrations, analytics, config, assets, and integrations
- acceptance criteria, constraints, out-of-scope notes, and open questions

Treat ambiguous requirements as TODOs only when implementation can proceed safely. Otherwise add a short `Needs clarification:` item inside `## Todo`.

### 3. Review UI/UX implications

For any visible UI or interaction requirement:

- identify screens, components, navigation, feedback states, accessibility, localization, and responsiveness that must be implemented
- include UI tasks only when they are traceable to the spec or necessary for a complete user flow

Do not redesign the product beyond the spec. The UI/UX pass exists to prevent missing required states, not to invent scope.

### 4. Investigate the codebase

Before writing the final list:

- Search for existing implementations, components, services, data stores, tests, prefabs/scenes, or assets related to the spec.
- Use a subagent for broad investigation when relevant files are not obvious or the spec spans multiple systems.
- Prefer tasks that adapt existing code over creating parallel systems.
- Cite concrete existing interfaces in task text when that makes the task actionable.

If the codebase lacks an obvious location, write the task with the intended responsibility rather than guessing an exact file.

### 5. Write the TODO document

Use the format in `references/todo-template.md`.

Rules for `## Todo`:

- Group checklist items under `###` headings by task type or related feature area.
- Choose the grouping that makes implementation easiest: task type for small specs, feature area for multi-flow specs.
- Every item starts with one category tag: `[Logic]`, `[UI]`, or `[Data]`.
- Write each item as a short actionable command: **verb + important target + outcome**.
- Keep each item compact. Prefer one line under ~14 words when possible.
- Highlight important terms with bold markdown: the target object, required state, limit, or user-visible outcome.
- Focus on action, not explanation. Avoid background, rationale, and repeated spec wording.
- Make each item implementable: specific object, behavior, state, or integration.
- Split mixed work into separate items. UI rendering, business logic, and persistence should not be hidden in one item.
- Include dependency/setup tasks only if the spec requires them.
- If a spec requirement is already implemented in the current codebase, still list it and mark it done (`[x]`).
- Exclude verification-only work from Todo.
- Do not generate a `## Test cases` section.

### 6. Self-check before reporting

Verify that:

- the output file is in the same folder as the spec
- every task maps to a requirement or necessary codebase integration
- every requirement has either a TODO or a clarification item
- TODO items are grouped by task type or related feature area
- no implementation code was changed

Report the output path and summarize only the main task counts.

## Rules

- This is a planning skill only; do not implement the TODOs.
- Do not create `Docs/Goals` files unless the user explicitly asks to convert the TODO into goals.
- Keep the list practical and finite. Avoid speculative polish, broad refactors, or duplicate tasks.
- If the spec conflicts with the current codebase, note the conflict as a TODO or clarification rather than silently choosing one side.
