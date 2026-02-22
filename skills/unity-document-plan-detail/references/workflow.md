# Deep Planning Workflow

## Step 1: Read Templates
Read all templates in `assets/templates/` (PLAN_OVERVIEW, PLAN_TASKS, PLAN_PATCH, PLAN_PATCH_TEMPLATE).

## Step 2: Deep-Dive Investigation
Thoroughly investigate every affected system, file, entry point. Understand current behavior before planning.

## Step 3: Analyze Requirements
Goals, constraints, acceptance criteria. Ask if unclear.

## Step 4: Create Output Folder
```bash
mkdir -p documents/plans/{plan-name}/patches
```

## Step 5: Generate overview.html (Tab 1)
- Summary cards (scope, complexity, risk, effort)
- Architecture overview (current → proposed)
- Technical approach (bullets, not paragraphs)
- Risk table with severity tags
- Acceptance criteria grid

## Step 6: Generate tasks.html (Tab 2)
- Epics table with task counts and cost distribution
- Task breakdown table with all fields
- Dependency graph description
- Implementation timeline (phases, milestones)
- Task walkthrough — each task with files, effects, criteria, View Patch → links to `patch.html#TASK_ID`
- Types: `Logic`, `UI`, `Data`, `API`, `Asset`, `Test`, `Config`
- Costs: `badge-s` S (<2h), `badge-m` M (2-4h), `badge-l` L (4-8h), `badge-xl` XL (1-2d)
- Task IDs: `T-{uuid}` format (oh-my-opencode Task System)
- Per-task fields: id, subject, description, status, blockedBy, blocks, owner, wave

## Step 7: Generate Per-Task Patches
One `.patch` file per task in `patches/`:
- Unified diff format: `--- a/path` / `+++ b/path` / `@@ hunks @@`
- New files: `--- /dev/null`; deleted: `+++ /dev/null`; 3 lines context
- Every task MUST have its own `.patch` file — never skip a task
- Each patch has full information about the change and its effects
- Filename: `patches/T-{task-id}.patch`

## Step 8: Generate tasks.json
Task metadata for patch.html generation:
```json
[{"id": "T-{id}", "subject": "...", "type": "Logic", "cost": "M", "wave": 1}]
```

## Step 9: Generate patch.html (Tab 3)
Run `generate_patch_html.py`:
```
python scripts/generate_patch_html.py documents/plans/{plan-name}/patches/ documents/plans/{plan-name}/patch.html --title "Feature Name" --tasks-json documents/plans/{plan-name}/tasks.json
```

Do NOT write patch.html manually — always use the script. The script reads per-task `.patch` files + `tasks.json` metadata, generates summary stats, per-task sections with metadata/download/diff viewer.

## Step 10: Verbal Summary
Location, effort, risks, critical path, patch stats.
