# Task System Output Guide

How to record assessments in the Prometheus Task System after reporting.

## Parent Task (Always Required)

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

## Metadata Schema

| Field | Type | Values |
|:------|:-----|:-------|
| `cost` | string | `XS`, `S`, `M`, `L`, `XL` |
| `costHours` | string | `"X-Yh"` |
| `risk` | string | `Low`, `Med`, `High` |
| `skillSource` | string | `"unity-plan-quick"` (always) |

## Child Tasks (from ┌ Tasks tree)

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

## Dependency Wiring

Use `blockedBy` when task ordering matters:

```
task_create(
  subject: "Testing + polish",
  parentID: "{parent-id}",
  blockedBy: ["{core-logic-task-id}"],
  metadata: { ... }
)
```

## Downstream Integration

Assessment tasks feed into:
- `unity-plan-deep` — references assessment for full planning
- `unity-plan-detail` — uses metadata to scope patch generation
- Both look for `metadata.skillSource: "unity-plan-quick"`
