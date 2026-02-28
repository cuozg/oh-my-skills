# unity-plan-detail — Deep Planning Workflow

## Step 1: Read Templates

Read all templates in `../assets/templates/` (PLAN_OVERVIEW, PLAN_TASKS, PLAN_PATCH, PLAN_PATCH_TEMPLATE).

## Step 2: Deep-Dive Investigation

Run `../../unity-shared/scripts/plan/investigate_feature.py --init <plan-name> <keywords>` to create output folder and discover existing code.
Also use `read`, `glob`, `grep`, LSP tools to understand current behavior before planning.

## Step 3: Analyze Requirements

Goals, constraints, acceptance criteria. Ask if unclear.

## Step 4: Create Output Folder (if not done via --init)

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
- Task breakdown table — sequential labels (TASK-1.1, TASK-1.2, etc.)
- Dependency graph description
- Implementation timeline (phases, milestones)
- Task walkthrough — files, effects, criteria, View Patch → `patch.html#TASK_ID`
- Types: `Logic`, `UI`, `Data`, `API`, `Asset`, `Test`, `Config`
- Costs: S (<2h), M (2-4h), L (4-8h), XL (1-2d)
- Per-task fields: id, subject, description, wave, type, cost, blockedBy

## Step 7: Generate Per-Task Patches

One `.patch` file per task in `patches/`:
- Unified diff format: `--- a/path` / `+++ b/path` / `@@ hunks @@`
- New files: `--- /dev/null`; deleted: `+++ /dev/null`; 3 lines context
- Every task MUST have its own `.patch` file — never skip a task
- Filename: `patches/TASK-{epic}.{task}.patch`

## Step 8: Generate tasks.json

```json
[{"id": "TASK-1.1", "subject": "...", "type": "Logic", "cost": "M", "wave": 1}]
```

## Step 9: Generate patch.html (Tab 3)

```bash
python3 scripts/generate_patch_html.py documents/plans/{plan-name}/patches/ documents/plans/{plan-name}/patch.html --title "Feature Name" --tasks-json documents/plans/{plan-name}/tasks.json
```

Do NOT write patch.html manually — always use the script.

## Step 10: Verbal Summary

Location, effort, risks, critical path, patch stats, output folder path.
