# Detail Workflow — 10 Steps

## Step 1: Read
Load entry points, affected modules. Build file inventory table:
`| File | Role | Lines affected |`

## Step 2: Scope
Define phases (e.g. Foundation → Core → Integration → Polish).
State explicit out-of-scope items.

## Step 3: Investigate
Trace every cross-system call. Record `file:line` for each dependency.

## Step 4: Plan
Decompose: Phases → Tasks → Subtasks.
Assign size (XS/S/M/L) and risk per task node.

## Step 5: Generate Patches
For each changed file produce a unified diff `.patch` file:
`Documents/Plans/{Name}/{File}.patch`

## Step 6: overview.html
Content: project summary, phases table, risk matrix.
No JavaScript. Inline CSS only.

## Step 7: tasks.html
Content: full task tree with size, risk, skill, description per node.
No JavaScript. Inline CSS only.

## Step 8: patch.html
Content: one `<section>` per patch file with rendered diff (color-coded via CSS classes).
No JavaScript. Inline CSS only.

## Step 9: Save
Write all files to `Documents/Plans/{Name}/`.

## File Inventory

```
Documents/Plans/{Name}/
├── overview.html
├── tasks.html
├── patch.html
└── {FileName}.patch  (one per changed file)
```
