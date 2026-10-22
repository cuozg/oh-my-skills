# Mode Workflows

## Full GDD Mode

Creates an index document plus one spec file per feature.

### Step 1: Scan

Check `Docs/Specs/` for existing specs. Report what exists and what is missing.

### Step 2: Investigate

Deep codebase investigation — load `read_skill_file("unity-standards", "references/plan/investigation-workflow.md")` and follow its tracing methodology. Use Unity MCP tools (`ManageScene(GetHierarchy)`, `FindProjectAssets`, `ReadResource`, `ListResources`) alongside LSP and grep. Map every existing system, its classes, and integration points.

### Step 3: Interview

Present the feature list extracted from investigation. Ask the user to confirm, add, or remove features. For each feature, ask what they already know — the skill fills the rest.

### Step 4: Draft Index

Load `read_skill_file("unity-spec", "references/gdd-template.md")` and create `Docs/Specs/_INDEX.md` with game-level overview, feature map, art/audio direction, platform targets, and global constraints.

### Step 5: Draft Features

For each feature, load `read_skill_file("unity-spec", "references/feature-template.md")` and produce `Docs/Specs/FEATURE_NAME.md`. Use codebase evidence where it exists, mark gaps with `[ASSUMED]`.

### Step 6: Review ⛔ BLOCK

Present all drafted files. Wait for user approval before saving. Do NOT save until approved.

### Step 7: Save & Validate

Save all files. Run validation:
`run_skill_script("unity-spec", "scripts/validate_spec.py", arguments=["Docs/Specs/"])`

---

## Feature Spec Mode

Creates or replaces a single feature spec file.

### Step 1: Scan

Check `Docs/Specs/` for existing spec of this feature. If found, load it as context.

### Step 2: Investigate

Scan the codebase for this feature's implementation. Trace entry points, classes, state machines, data models, event subscriptions, and dependencies on other systems. Cite `file:line` for every finding.

### Step 3: Draft

Load `read_skill_file("unity-spec", "references/feature-template.md")`. Fill every section. Include at least 1 Mermaid diagram (architecture or state). Mark assumptions with `[ASSUMED]`.

### Step 4: Review ⛔ BLOCK

Present the spec. Wait for user approval.

### Step 5: Save & Validate

Save to `Docs/Specs/FEATURE_NAME.md`. Run:
`run_skill_script("unity-spec", "scripts/validate_spec.py", arguments=["Docs/Specs/FEATURE_NAME.md"])`

---

## Update Mode

Diffs an existing spec against the current codebase and patches it.

### Step 1: Load Existing

Read the target spec from `Docs/Specs/FEATURE_NAME.md`.

### Step 2: Investigate Current State

Scan the codebase for the feature. Compare what the spec says vs what the code actually does. Build a diff list: added systems, removed systems, changed behavior, new dependencies.

### Step 3: Patch

Update each section where the code has diverged. Preserve user-authored design intent — only change sections where code reality contradicts the spec. Add `[UPDATED]` tag next to changed sections with a brief reason.

### Step 4: Review ⛔ BLOCK

Present the diff summary and updated spec. Wait for approval.

### Step 5: Save & Validate

Overwrite the existing file. Run validation.
