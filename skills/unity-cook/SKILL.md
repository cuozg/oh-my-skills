---
name: unity-cook
description: >
  Implement a Unity task with a trust trail: write the agent's understanding and test cases to
  Docs/Tasks/{task-name}.md, wait for approval, implement (with unit tests for logic), run an
  independent review and impact sweep, hand off to unity-validate for evidence, then record the
  changes in the same file. Use when the user says "cook" or hands off a Unity feature, logic
  change, or prefab/UI task to implement. Do not use for bug diagnosis (unity-debug), validation
  only (unity-validate), questions, costing, or docs work.
metadata:
  author: kuozg
  version: "2.0"
---

# unity-cook

Implement a Unity task so the user can trust it without re-checking. The user approves the
spec before any code, and the change list in the task file can be traced to that spec. An
independent `unity-validate` run supplies the proof that it works.

*** MANDATORY: Build `Docs/Tasks/<task-name>.md` from `references/task-template.md`. Keep its
section order and status icons. `<task-name>` is kebab-case. ***

Engineering rules come from `unity-standards`. Editor access (compile, console, tests,
scene/prefab edits) goes through `../unity-standards/references/other/unity-cli-routing.md`.
`Docs/` means `<unity-project>/Docs/`, next to `Assets/`.

## Workflow

### 1. Collect
- Read the request, the named files/scenes/prefabs, and the related code (spawn an `Explore`
  subagent, model `haiku`, when it needs more than 3 searches).
- Ask for the **design source** (image path, Figma link, or "none") when the task touches UI.
- Ask only about gaps the codebase cannot answer. Use `mattpocock-skills:grilling` when the
  request has several open decisions.
- **Done when:** every requirement bullet can be written without "maybe", and every open
  decision is either answered or listed as an assumption.

### 2. Spec gate
- Create `Docs/Tasks/<task-name>.md` with the **Spec** half of the template: Type, Request (as
  understood), Out of scope, Assumptions, Design source, Test cases. Short bullets only.
- Type: `ui-prefab` (prefab / Canvas / UI Toolkit work), `logic` (C# behaviour), or `mixed`.
- Test cases cover the happy path, each edge/empty/error state, and each existing flow the
  change could break (regression, `R*`). Give each case a planned Method from
  `../unity-validate/references/recipes.md`.
- Show the user the file path plus the bullets, then **stop**. Wait for approval.
- On corrections: update the file, show it again, wait again.
- **Done when:** the user approves. Set status to `🔵 In progress`.

### 3. Implement
- Run the routing preflight. Write the console's current errors/warnings into the task file's
  **Console baseline** line, before any change. unity-validate compares against it.
- Make the smallest change that satisfies the approved spec. Follow `unity-standards`
  (load only the matching references).
- Change `.unity` / `.prefab` / `.asset` through Editor commands while a live Editor is reachable.
- **Logic changes ship with unit tests**: at least one per logic test case, named after the case
  (`T1_…`, `R1_…`), written with `unity-test-unit`. If the project has no test assembly, create
  `Assets/Tests/EditMode` (plus `PlayMode` when needed) with asmdefs.
- When the spec turns out wrong or incomplete mid-task, stop, update the Spec section, and
  re-ask before continuing.
- **Done when:** the code compiles, the console shows nothing beyond the baseline, and every
  logic case has a passing test.

### 4. Review + impact
- Dispatch a **fresh** subagent (`general-purpose`, model `opus`) with the brief in
  `references/review-brief.md`. Fill `{task-file}`, `{diff}` (diff range plus untracked files from
  `git status --porcelain`), and `{review-dir}` (absolute path of
  `../unity-standards/references/review/` resolved from this skill's base directory). Give it
  the facts only, not your opinion of the change.
- Fix every `Critical` / `Major` finding. For each `Minor` finding, either fix it or write why
  you kept it. After fixes, re-run the compile check and the tests.
  When a `Critical` / `Major` fix changes more than a few lines, dispatch a new reviewer on it.
- **Done when:** every finding is marked `fixed` or `kept: <reason>` in the task file.

### 5. Validate
- Dispatch a **fresh** subagent (`general-purpose`, model `sonnet`) with the prompt
  "Use skill unity-validate on `Docs/Tasks/<task-name>.md`". Give it only the task file path; it
  checks the result without your reasoning.
- `❌ Failed` (including any design mismatch) → fix in step 3 → run step 4 for the fix → dispatch a
  new validator. Repeat until the verdict is `✅ Validated` or `🟠 Not validated`.
- A `❌` that needs the user (a missing asset, a design decision, or a third attempt failing the
  same way) → stop, set `❌ Blocked`, and go to step 6.
- **Done when:** the task file's `## Validation` section holds a fresh verdict for the final code.

### 6. Report
- Fill **What was done**, **Changed files**, and **Review & impact** in the task file.
- Set the final status from the validation verdict:
  - `✅ Done` for `✅ Validated`.
  - `🟠 Not validated` for `🟠 Not validated`.
  - `❌ Blocked` when a `❌` can't be fixed without the user (say what is needed).
- Reply to the user with the file link, the status, and the `⚠️` / `❌` items only.
- **Done when:** no template placeholder is left, and every changed file is listed with a one-line why.
