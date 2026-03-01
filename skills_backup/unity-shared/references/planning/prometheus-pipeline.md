# Prometheus Planning Pipeline

Shared reference for `unity-plan-quick`, `unity-plan-deep`, `unity-plan-detail`.

## Pipeline Flow

```
unity-plan-quick  →  Assessment task (T-{id})
        ↓ assessmentTaskId
unity-plan-deep   →  PLAN task + EPICs + sub-tasks (with patches)
   — OR —
unity-plan-detail →  PLAN task + EPICs + sub-tasks (with patches + HTML)
```

`plan-deep` and `plan-detail` are alternatives, not sequential.

## Task Hierarchy

```
Assessment: {Feature}                    ← unity-plan-quick
├── {work area child}                    ← optional child tasks

PLAN: {Feature}                          ← unity-plan-deep OR unity-plan-detail
│  metadata.assessmentTaskId = T-{id}
├── EPIC 1: {Name}                       ← parentID = plan
│   ├── TASK 1.1: {Name}                 ← parentID = epic, blockedBy = []
│   ├── TASK 1.2: {Name}                 ← blockedBy = [1.1]
│   └── TASK 1.3: {Name}                 ← blockedBy = [1.1]
└── EPIC 2: {Name}
    └── TASK 2.1: {Name}                 ← blockedBy = [1.2, 1.3]
```

## Unified Metadata Schema

### Common Fields (All Skills)

| Field | Type | Values |
|:------|:-----|:-------|
| `size` | string | `Small`, `Medium`, `Large` |
| `timeEstimate` | string | `"X-Y hours"` |
| `risk` | string | `Low`, `Medium`, `High` |
| `skillSource` | string | `"unity-plan-quick"` \| `"unity-plan-deep"` \| `"unity-plan-detail"` |

### Planning Fields (deep + detail only)

| Field | Type | Level |
|:------|:-----|:------|
| `assessmentTaskId` | string | Plan task |
| `planFile` / `planFolder` | string | Plan task |
| `totalEpics`, `totalTasks`, `totalEstimate` | number/string | Plan task |
| `epicNumber` | number | Epic task |
| `wave`, `type`, `cost`, `costHours` | mixed | Sub-task |
| `patchFile`, `planTaskNumber` | string | Sub-task |

## How Prometheus Reads Task Data

- **Find assessments**: `task_list` → filter `metadata.skillSource == "unity-plan-quick"`
- **Find plans for assessment**: filter `metadata.assessmentTaskId == "T-{id}"`
- **Find sub-tasks**: `task_get(planTaskId)` → traverse children via `parentID`
- **Execution order**: sort by `metadata.wave`, respect `blockedBy`
- **Critical path**: longest `blockedBy` chain by `costHours`

## Dependency Wiring Rules

| Pattern | blockedBy | Example |
|:--------|:----------|:--------|
| Sequential | B after A | `blockedBy: ["T-001"]` |
| Fan-out | Many after one | Each has `blockedBy: ["T-001"]` |
| Fan-in | One after many | `blockedBy: ["T-002", "T-003"]` |
| Independent | No constraint | `blockedBy: []` (Wave 1) |
