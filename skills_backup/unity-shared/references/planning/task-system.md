# Task System Reference

Complete guide to registering plans and assessments via `task_create`.

---

## Part 1 — Quick Assessment Output (unity-plan-quick)

How to record assessments in the Prometheus Task System after reporting.

### Parent Task (Always Required)

One parent per assessment. Subject uses `▲` prefix.

```
task_create(
  subject: "▲ {Feature/Task Name}",
  description: "<full assessment tree text>",
  metadata: {
    cost: "XS" | "S" | "M" | "L" | "XL",
    costHours: "X-Yh",
    risk: "Low" | "Med" | "High",
    skillSource: "unity-plan-quick"
  }
)
```

**Subject format**: Always prefix with `▲` so downstream skills (`unity-plan-deep`, `unity-plan-detail`) can find it.

### Metadata Schema

| Field | Type | Values |
|:------|:-----|:-------|
| `cost` | string | `XS`, `S`, `M`, `L`, `XL` |
| `costHours` | string | `"X-Yh"` |
| `risk` | string | `Low`, `Med`, `High` |
| `skillSource` | string | `"unity-plan-quick"` (always) |

### Child Tasks (from ┌ Tasks tree)

One child per `┌ Tasks` entry. Include `skill` in metadata.

```
task_create(
  subject: "{task subject}",
  description: "{short description from tree}",
  parentID: "{parent-task-id}",
  metadata: {
    cost: "XS" | "S" | "M" | "L" | "XL",
    costHours: "X-Yh",
    risk: "Low" | "Med" | "High",
    skill: "{recommended-skill-name}",
    skillSource: "unity-plan-quick"
  }
)
```

**When to create children**: Assessment has 2+ distinct work areas in `┌ Tasks`.
**Skip children**: Single-task assessments or sequential steps (not parallel work).

### Dependency Wiring

Use `blockedBy` when task ordering matters:

```
task_create(
  subject: "Testing + polish",
  parentID: "{parent-id}",
  blockedBy: ["{core-logic-task-id}"],
  metadata: { ... }
)
```

### Downstream Integration

Assessment tasks feed into:
- `unity-plan-deep` — references assessment for full planning
- `unity-plan-detail` — uses metadata to scope patch generation
- Both look for `metadata.skillSource: "unity-plan-quick"`

---

## Part 2 — Deep Plan Registration (unity-plan-deep)

Register every plan element as a task via `task_create` after generating the markdown plan.

### Task Hierarchy

Create tasks in this order (parent must exist before children):
```
Plan Task (parent=none)
├── Epic 1 Task (parentID=Plan)
│   ├── Task 1.1 (parentID=Epic 1)
│   ├── Task 1.2 (parentID=Epic 1)
│   └── Task 1.3 (parentID=Epic 1)
├── Epic 2 Task (parentID=Plan)
│   ├── Task 2.1 (parentID=Epic 2)
│   └── Task 2.2 (parentID=Epic 2)
└── ...
```

### Step-by-Step Registration

#### 1. Create Plan Task
```
task_create(
  subject: "PLAN: {FeatureName}",
  description: "Implementation plan for {FeatureName}. See Documents/Plans/PLAN_{FeatureName}.md",
  metadata: {
    size: "Small" | "Medium" | "Large",
    timeEstimate: "X-Y hours",
    risk: "Low" | "Medium" | "High",
    planFile: "Documents/Plans/PLAN_{FeatureName}.md",
    totalEpics: N, totalTasks: N,
    totalEstimate: "{X-Yh}",
    skillSource: "unity-plan-deep",
    assessmentTaskId: "T-{uuid}"  // optional — from unity-plan-quick
  }
)
```
Store the returned `T-{uuid}` as `planTaskId`.

#### 2. Create Epic Tasks
For each epic in the plan:
```
task_create(
  subject: "EPIC {N}: {EpicName}",
  parentID: planTaskId,
  description: "Epic {N} of {FeatureName} plan. {taskCount} tasks, {estimateRange}.",
  metadata: { epicNumber: N, skillSource: "unity-plan-deep" }
)
```
Store returned ID as `epicTaskId[N]`.

#### 3. Create Sub-Tasks
For each task row in each epic table:
```
task_create(
  subject: "TASK {epic.task}: {TaskName}",
  parentID: epicTaskId[N],
  description: "{Description from table row}",
  blockedBy: [taskIds of dependencies],
  metadata: {
    wave: W,
    type: "{Task Type}",
    cost: "{XS|S|M|L|XL}",
    costHours: "{X-Yh}",
    patchFile: "patches/TASK-{epic.task}.patch",
    planTaskNumber: "{epic.task}",
    skillSource: "unity-plan-deep"
  }
)
```

#### 4. Set Dependencies
Map the plan's dependency graph to `blockedBy` arrays:
- Read Section 5.1 (Execution Order) "Depends On" column.
- Translate `Task 1.1` references to their corresponding `T-{uuid}` IDs.
- Pass as `blockedBy` during `task_create` (preferred) or `addBlockedBy` via `task_update`.

#### 5. Wave Assignment
Derive `wave` from the execution order:
- **Wave 1**: Tasks with no dependencies (can start immediately).
- **Wave 2**: Tasks that depend only on Wave 1 tasks.
- **Wave N**: Tasks whose dependencies are all in waves < N.

### Post-Registration Summary
After all tasks are created, output:
```
## Task Registration Summary
- Plan Task: T-{uuid} ({FeatureName})
- Epics: {count} created
- Tasks: {count} created
- Dependency chains: {count}
- Critical path: Task {a.b} → Task {c.d} → ... ({total hours})
- Waves: {count} (Wave 1: {n} tasks, Wave 2: {n} tasks, ...)
```
