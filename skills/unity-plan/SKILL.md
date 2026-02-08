---
name: unity-plan
description: "High-level planning for Unity features with multi-file output and patch generation. Use when: (1) Analyzing requirements and specs, (2) Investigating existing codebase/systems, (3) Breaking work into epics and tasks, (4) Estimating effort and identifying risks, (5) Generating implementation patches with 100% code changes. Outputs a folder of HTML files (overview, tasks, estimates, dependencies, timeline) plus a unified diff patch file."
---

# Unity Planning Skill

Create implementation plans for Unity features with architecture, task breakdown, estimates, dependencies, timeline, and complete code patches.

**IMPORTANT**: This skill is for **planning only**. Do NOT implement or execute any work — but DO generate complete code patches showing all changes.

---

## Output Structure

Plans output to a folder with one file per section:

```
documents/plans/{plan-name}/
├── overview.html
├── tasks.html
├── estimates.html
├── dependencies.html
├── timeline.html
└── changes.patch
```

`{plan-name}` = kebab-case feature name (e.g. `multi-event-daily-boss`).

---

## Templates

Each output file has a corresponding template in `assets/templates/`:

| Template | Output | Content |
|---|---|---|
| `PLAN_OVERVIEW.html` | `overview.html` | Header, summary cards, architecture diagrams, technical approach |
| `PLAN_TASKS.html` | `tasks.html` | Task table + per-task walkthrough with files and criteria |
| `PLAN_ESTIMATES.html` | `estimates.html` | Per-epic hours, resource allocation, assumptions |
| `PLAN_DEPENDENCIES.html` | `dependencies.html` | Dependency graph, dependency matrix, risks, blockers |
| `PLAN_TIMELINE.html` | `timeline.html` | Implementation phases, milestones, recommended order |
| `PLAN_PATCH_TEMPLATE.patch` | `changes.patch` | Unified diff format reference |

---

## Workflow

### 1. Read All Templates

Read every template file in `assets/templates/` and understand all `<!-- INSTRUCTION: ... -->` comments. These are the authoritative format reference.

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

Use `PLAN_OVERVIEW.html` template. Populate:
- Feature title and generation date
- Summary cards: duration, risk, task count, epic count
- Architecture overview: old vs new ASCII diagrams + key benefits
- Technical approach: numbered implementation steps with `<code>` references

### 6. Generate tasks.html

Use `PLAN_TASKS.html` template. Populate:
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

Use `PLAN_ESTIMATES.html` template. Populate:
- Aggregate totals: total hours range, total days range, complexity
- Per-epic estimation table with cost distribution (S/M/L/XL counts)
- Resource allocation cards: role, hours, assigned tasks, required skills
- Estimation assumptions

### 8. Generate dependencies.html

Use `PLAN_DEPENDENCIES.html` template. Populate:
- ASCII dependency graph showing task flow with arrows
- Dependency matrix: each task's depends-on and blocks relationships
- Risk cards with level (high/medium/low), description, mitigation
- Blocker list with severity icons

### 9. Generate timeline.html

Use `PLAN_TIMELINE.html` template. Populate:
- Implementation phases with tasks per phase and duration
- Milestone checkpoints with success criteria
- Recommended implementation order with rationale

### 10. Generate changes.patch

Use `PLAN_PATCH_TEMPLATE.patch` as format reference. Generate a unified diff file containing **100% of all code changes** for the entire plan.

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
- Total estimated effort
- Key risks or blockers
- Critical path through dependencies
- Recommended implementation order
- Patch file statistics (files changed, insertions, deletions)

---

## Output Checklist

Before completing, verify:

- [ ] All 6 templates read before generating output
- [ ] Output folder created at `documents/plans/{plan-name}/`
- [ ] overview.html: CSS copied exactly, all placeholders replaced, architecture has old/new diagrams
- [ ] tasks.html: Every task has a walkthrough section, files listed, criteria defined
- [ ] estimates.html: Per-epic totals, resource allocation cards, assumptions listed
- [ ] dependencies.html: Dependency graph, matrix, risks with mitigations, blockers
- [ ] timeline.html: Phases with tasks, milestones with criteria, recommended order
- [ ] changes.patch: Unified diff format, all tasks have code changes, applies cleanly
- [ ] Navigation links work between all HTML files
- [ ] All `<!-- INSTRUCTION: ... -->` comments removed from final output

---

## What This Skill Does NOT Do

- Execute implementations from the plan
- Modify actual project files (except creating the plan output folder)
- Run the generated patch file
- Skip any task in the walkthrough or patch
