---
name: unity-plan
description: "High-level planning for Unity features with multi-file output and patch generation. Use when: (1) Analyzing requirements and specs, (2) Investigating existing codebase/systems, (3) Breaking work into epics and tasks, (4) Estimating effort and identifying risks, (5) Generating implementation patches with 100% code changes. Outputs a folder of HTML files (overview, tasks, estimates, dependencies, timeline) plus a unified diff patch file."
---

# Unity Planning Skill

Create implementation plans for Unity features with architecture, task breakdown, estimates, dependencies, timeline, and complete code patches.

**IMPORTANT**: This skill is for **planning only**. Do NOT implement or execute any work — but DO generate complete code patches showing all changes.

---

## Architecture: Templates vs Generated Files

This skill uses a **template-to-output** architecture. Understanding the distinction prevents `ERR_FILE_NOT_FOUND` errors.

**Templates** (`assets/templates/`) are **internal boilerplate** containing HTML structure, CSS, `[PLACEHOLDER]` values, and `<!-- INSTRUCTION: ... -->` comments. They exist solely as input to the generation process. **NEVER** access template files directly — opening them in a browser shows placeholder text and navigation links break because sibling files don't exist at that path.

**Generated files** (`documents/plans/{plan-name}/`) are the **actual user-facing output** created by processing templates with real plan data. Users open these files in their browser.

| Template (internal — do not access) | Generated Output (user-facing) |
|---|---|
| `assets/templates/PLAN_OVERVIEW.html` | `documents/plans/{plan-name}/overview.html` |
| `assets/templates/PLAN_TASKS.html` | `documents/plans/{plan-name}/tasks.html` |
| `assets/templates/PLAN_ESTIMATES.html` | `documents/plans/{plan-name}/estimates.html` |
| `assets/templates/PLAN_DEPENDENCIES.html` | `documents/plans/{plan-name}/dependencies.html` |
| `assets/templates/PLAN_TIMELINE.html` | `documents/plans/{plan-name}/timeline.html` |
| `assets/templates/PLAN_PATCH_TEMPLATE.patch` | `documents/plans/{plan-name}/changes.patch` |

`{plan-name}` = kebab-case feature name (e.g. `multi-event-daily-boss`).

---

## Generation Process

When generating output from a template:

1. Read the template from `assets/templates/` to understand structure
2. Replace all `[PLACEHOLDER]` values with actual plan content
3. Keep the `<nav class="nav-links">` section — paths are already relative (`./`)
4. Mark the correct tab as `class="active"` for each output file
5. Remove all `<!-- INSTRUCTION: ... -->` comments from final output
6. Write the completed HTML to `documents/plans/{plan-name}/`

---

## Workflow

### 1. Read All Templates

Read every template file in `assets/templates/`. Note the `<!-- INSTRUCTION: ... -->` comments — they describe what content goes where. The navigation bar uses relative `./` paths with the active tab pre-marked.

### 2. Analyze Requirements

- Read the provided spec/requirements
- Identify goals, constraints, and acceptance criteria
- Note ambiguities — **ask clarifying questions** if specs are unclear

### 3. Investigate Codebase

Use the **`unity-investigate-code`** skill:

```
Read and follow: .claude/skills/unity-investigate-code/SKILL.md
```

Focus on: existing systems affected, files needing modification, technical debt, reusable components, entry points and execution flows.

### 4. Create Output Folder

```bash
mkdir -p documents/plans/{plan-name}
```

### 5. Generate overview.html

Read `assets/templates/PLAN_OVERVIEW.html`. Replace placeholders and write to `documents/plans/{plan-name}/overview.html`. Populate:
- Feature title and generation date
- Summary cards: duration, risk, task count, epic count
- Architecture overview: old vs new ASCII diagrams + key benefits
- Technical approach: numbered implementation steps with `<code>` references

### 6. Generate tasks.html

Read `assets/templates/PLAN_TASKS.html`. Replace placeholders and write to `documents/plans/{plan-name}/tasks.html`. Populate:
- Task table grouped by epic (columns: #, Epic, Task, Description, Type, Cost)
- **Full walkthrough for EVERY task** — each task gets:
  - Detailed description of what to implement
  - Step-by-step implementation instructions
  - List of every file to modify/create
  - Task-specific acceptance criteria

Valid Types: `Logic`, `UI`, `Data`, `API`, `Asset`, `Test`, `Config`

Cost badges: `badge-s` S (<2h), `badge-m` M (2-4h), `badge-l` L (4-8h), `badge-xl` XL (1-2d)

Task numbering: `[Epic#].[Task#]` (e.g. 1.1, 1.2, 2.1)

### 7. Generate estimates.html

Read `assets/templates/PLAN_ESTIMATES.html`. Replace placeholders and write to `documents/plans/{plan-name}/estimates.html`. Populate:
- Aggregate totals: total hours range, total days range, complexity
- Per-epic estimation table with cost distribution (S/M/L/XL counts)
- Resource allocation cards: role, hours, assigned tasks, required skills
- Estimation assumptions

### 8. Generate dependencies.html

Read `assets/templates/PLAN_DEPENDENCIES.html`. Replace placeholders and write to `documents/plans/{plan-name}/dependencies.html`. Populate:
- ASCII dependency graph showing task flow with arrows
- Dependency matrix: each task's depends-on and blocks relationships
- Risk cards with level (high/medium/low), description, mitigation
- Blocker list with severity icons

### 9. Generate timeline.html

Read `assets/templates/PLAN_TIMELINE.html`. Replace placeholders and write to `documents/plans/{plan-name}/timeline.html`. Populate:
- Implementation phases with tasks per phase and duration
- Milestone checkpoints with success criteria
- Recommended implementation order with rationale

### 10. Generate changes.patch

Read `assets/templates/PLAN_PATCH_TEMPLATE.patch` as format reference. Generate a unified diff at `documents/plans/{plan-name}/changes.patch` containing **100% of all code changes** for the entire plan.

**Patch generation rules:**
1. Include every file that any task modifies, creates, or deletes
2. Use unified diff format: `--- a/path` / `+++ b/path` / `@@ hunks @@`
3. New files: `--- /dev/null` / `+++ b/path`
4. Deleted files: `--- a/path` / `+++ /dev/null`
5. Include 3 lines of context around each change
6. Order: new files, then modified files, then deleted files
7. Every task in the plan MUST have corresponding code in the patch
8. The patch must apply cleanly: `patch -p1 --dry-run < changes.patch`

### 11. Verbal Summary

After generating all files, provide:
- Location of generated files: `documents/plans/{plan-name}/`
- Instruction to open `overview.html` in a browser
- Total estimated effort
- Key risks or blockers
- Critical path through dependencies
- Recommended implementation order
- Patch file statistics (files changed, insertions, deletions)

---

## How to Access Generated Plans

After generation, files are in `documents/plans/{plan-name}/`:

```
documents/plans/{plan-name}/
├── overview.html       ← Start here
├── tasks.html
├── estimates.html
├── dependencies.html
├── timeline.html
└── changes.patch
```

1. Open `documents/plans/{plan-name}/overview.html` in a browser
2. Use navigation tabs to switch between sections
3. All navigation uses relative paths (`./tasks.html`, `./estimates.html`, etc.)

**WARNING**: Do NOT open files from `.claude/skills/unity-plan/assets/templates/`. Those are internal templates with placeholder text. Clicking navigation tabs will cause `ERR_FILE_NOT_FOUND` because sibling files don't exist at that location.

---

## Output Checklist

Before completing, verify:

- [ ] All 6 templates read from `assets/templates/` before generating output
- [ ] Output folder created at `documents/plans/{plan-name}/`
- [ ] All 5 HTML files written to output folder (NOT to `assets/templates/`)
- [ ] overview.html: CSS copied exactly, all placeholders replaced, architecture has old/new diagrams
- [ ] tasks.html: Every task has a walkthrough section, files listed, criteria defined
- [ ] estimates.html: Per-epic totals, resource allocation cards, assumptions listed
- [ ] dependencies.html: Dependency graph, matrix, risks with mitigations, blockers
- [ ] timeline.html: Phases with tasks, milestones with criteria, recommended order
- [ ] changes.patch: Unified diff format, all tasks have code changes, applies cleanly
- [ ] Navigation tabs present in all 5 HTML files with relative `./` paths
- [ ] Correct tab marked `class="active"` in each file
- [ ] Patch tab links to `./changes.patch` in all HTML files
- [ ] All `<!-- INSTRUCTION: ... -->` comments removed from final output
- [ ] Summary includes path to generated files for user to open

---

## What This Skill Does NOT Do

- Execute implementations from the plan
- Modify actual project files (except creating the plan output folder)
- Run the generated patch file
- Skip any task in the walkthrough or patch
- Serve files from `assets/templates/` to users
