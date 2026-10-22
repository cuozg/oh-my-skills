---
name: unity-validate
description: >
  Validate Unity work in the real project with evidence: a task is implemented in the game, a bug
  reproduces or is fixed, or a generated image meets its requirements. Runs each case through
  Editor tools (prefab/scene trees, prefab and game shots including overlay UI, Play Mode clicks,
  live value probes, texture facts, unit tests) and writes the verdict with evidence. Use when the
  user says "validate", "verify", "check it works", "reproduce", "is the bug fixed", or when
  unity-cook or unity-debug hands off a validation. Do not use to implement or to diagnose root cause.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-validate

Prove, in the running project, whether the requirement holds. The output is a **verdict** backed
by **evidence** for every case: a screenshot, a tree, a probed value, a test result, or a console
excerpt. A case without evidence is not passed.

Validate and report; leave fixing to the implementer. When validation finds a problem, it
records the failure with its evidence and hands it back.

*** MANDATORY: Write results with `references/report-template.md`. Choose the recipe from
`references/recipes.md`, and the commands from `references/tools.md`. ***

Editor access goes through `../unity-standards/references/other/unity-cli-routing.md`. `Docs/`
means `<unity-project>/Docs/`, next to `Assets/`.

## Workflow

### 1. Load the target
- **Task file** (`Docs/Tasks/<task-name>.md`, from unity-cook): its Request bullets and Test
  cases are the requirements. If a requirement has no case, add one as `V1`, `V2`, … and mark
  it `(added by validator)`.
- **Bug** (from unity-debug or the user): the symptom, the steps, and the expected vs actual
  behaviour. The mode is `reproduce` before a fix and `verify fix` after it.
- **Image**: the file path(s), plus every stated requirement (size, transparency, style, sprite
  settings, where it is used).
- Write each requirement as one checkable line. Ask the user only when a requirement can't be
  made checkable.
- **Done when:** every requirement maps to at least one case, and each case has a Method.

### 2. Preflight
- Run the routing preflight. If no live Editor is found, ask the user to open it. If they decline,
  use batch mode and note it.
- Compile. Take the console baseline from the task file, or record it if there is no task file.
  Install the tools (`tools.md` → Install).
- If `Docs/Validations/tools-selftest.md` is missing, or its Unity/Pipeline versions differ from
  this project's, run the self-test (`tools.md` → Validate the tools). It needs the Editor closed;
  if the user keeps it open, skip the self-test and say so in the report.
- **Done when:** the project compiles, the baseline is recorded, and `unity command --query validate_`
  lists all seven commands.

### 3. Run every case
- Follow the recipe for the target: feature (ui-prefab / logic / gameplay), bug reproduce,
  bug verify fix, image, design compare.
- Save images to the evidence folder from `report-template.md`, named `<case-id>[-state].png`.
  Read each PNG back and confirm it shows what the case claims. An image you haven't looked at is
  not evidence.
- Keep a failure as a failure: record it, then keep going with the rest of the cases.
- **Done when:** every case is `✅`, `❌`, or `⚠️` with an Evidence cell, and the console is checked
  against the baseline.

### 4. Verdict and report
- Feature/image:
  - `✅ Validated` when all cases are `✅`.
  - `❌ Failed` when any case is `❌`.
  - `🟠 Not validated` when the only gaps are `⚠️`.
- Bug: `🔴 Reproduced` / `⚪ Not reproduced` before a fix, `🟢 Fixed` / `❌ Still reproduces` after it.
- Write the report (into the task file, or to `Docs/Validations/<name>.md`).
- Restore every temporary edit (the bite-check backups, with checksums matching). Then confirm
  with `git status` that only the **allowed paths** changed:
  - The evidence folder.
  - The task file's case cells and `## Validation` section, or the `Docs/Validations/` report.
  - `Assets/Editor/UnityValidate/`.
  - `Docs/Validations/tools-selftest.md`.
  - Kept bug repro tests.
- Return to the caller: the verdict, the report path, and each `❌` / `⚠️` case in one line.
- **Done when:** the report has no placeholders, every case links to evidence, and `git status`
  shows changes only in the allowed paths.
