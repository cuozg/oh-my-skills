---
name: unity-plan
description: "High-level planning for Unity features with multi-file output and patch generation. Use when: (1) Analyzing requirements and specs, (2) Investigating existing codebase/systems, (3) Breaking work into epics and tasks, (4) Estimating effort and identifying risks, (5) Generating implementation patches with 100% code changes. Outputs a folder of HTML files (overview, tasks, estimates, dependencies, timeline) plus a unified diff patch file."
---

# Unity Planning Skill

**Input**: Clear task/problem description, optional file paths, constraints, context
**Output**: 6 HTML files + 1 patch file at `documents/plans/{plan-name}/`

**IMPORTANT**: Planning only — do NOT implement. DO generate complete code patches.

## Architecture: Templates vs Generated Files

**Templates** (`assets/templates/`) = internal boilerplate with `[PLACEHOLDER]` values. **NEVER** access directly.
**Generated files** (`documents/plans/{plan-name}/`) = user-facing output. Users open these in browser.

| Template (internal) | Generated Output (user-facing) |
|---|---|
| `assets/templates/PLAN_OVERVIEW.html` | `documents/plans/{plan-name}/overview.html` |
| `assets/templates/PLAN_TASKS.html` | `documents/plans/{plan-name}/tasks.html` |
| `assets/templates/PLAN_ESTIMATES.html` | `documents/plans/{plan-name}/estimates.html` |
| `assets/templates/PLAN_DEPENDENCIES.html` | `documents/plans/{plan-name}/dependencies.html` |
| `assets/templates/PLAN_TIMELINE.html` | `documents/plans/{plan-name}/timeline.html` |
| `assets/templates/PLAN_PATCH.html` | `documents/plans/{plan-name}/patch.html` |
| `assets/templates/PLAN_PATCH_TEMPLATE.patch` | `documents/plans/{plan-name}/changes.patch` |

`{plan-name}` = kebab-case feature name.

## Generation Rules

1. Read template from `assets/templates/` for structure
2. Replace all `[PLACEHOLDER]` values with plan content
3. Keep sticky `<nav class="plan-nav-bar">` as first `<body>` element; hrefs use `PLAN_` prefix (e.g. `./PLAN_OVERVIEW.html`)
4. Mark correct tab with `class="nav-tab nav-tab-active"` per file
5. Remove all `<!-- INSTRUCTION: ... -->` comments
6. Write to `documents/plans/{plan-name}/`
7. **No `<script>` tags, JavaScript, event handlers** — pure HTML `<a href>` navigation only
8. Preserve CSP meta tag from template exactly as-is

## Workflow

1. **Read all templates** in `assets/templates/`
2. **Analyze requirements** — goals, constraints, acceptance criteria; ask if unclear
3. **Investigate codebase** — use `unity-investigate` skill for affected systems, files, entry points
4. **Create output folder**: `mkdir -p documents/plans/{plan-name}`
5. **Generate overview.html** — summary cards, architecture (old vs new), technical approach
6. **Generate tasks.html** — epic/task table, full walkthrough per task with files and criteria
   - Types: `Logic`, `UI`, `Data`, `API`, `Asset`, `Test`, `Config`
   - Costs: `badge-s` S (<2h), `badge-m` M (2-4h), `badge-l` L (4-8h), `badge-xl` XL (1-2d)
   - Numbering: `[Epic#].[Task#]`
7. **Generate estimates.html** — totals, per-epic table, resource allocation, assumptions
8. **Generate dependencies.html** — ASCII graph, dependency matrix, risk cards, blockers
9. **Generate timeline.html** — phases, milestones, recommended order
10. **Generate changes.patch** — unified diff with 100% code changes for all tasks
    - Unified diff format: `--- a/path` / `+++ b/path` / `@@ hunks @@`
    - New files: `--- /dev/null`; deleted: `+++ /dev/null`; 3 lines context
    - Every task MUST have corresponding code
11. **Generate patch.html** — stats, file list, GitHub-style diff viewer, download link
12. **Verbal summary** — location, effort, risks, critical path, patch stats

## Output Checklist

- [ ] All 7 templates read; output folder created
- [ ] All 6 HTML files + patch written to `documents/plans/{plan-name}/`
- [ ] Every task has walkthrough, file list, criteria
- [ ] changes.patch in unified diff format, all tasks covered
- [ ] Navigation tabs in all HTML with `PLAN_` prefix paths
- [ ] Correct `nav-tab-active` per file; navbar first in `<body>`
- [ ] **No JavaScript** in any generated file
- [ ] All `<!-- INSTRUCTION -->` comments removed

## Handoff & Boundaries

- **OWNS**: Requirement analysis, epic/task breakdown, estimation, risk, dependency mapping, timeline
- **Delegates to**: `unity-plan-detail` (per-task code), `unity-game-designer` (design concepts)
- **Does NOT**: Generate per-task implementation code, execute plans (that's `unity-plan-executor`)
