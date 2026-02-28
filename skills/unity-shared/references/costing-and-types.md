# Costing & Types

## Costing Tiers

| Tier | Hours | Description |
|:-----|:------|:------------|
| XS | 1-2h | Trivial change |
| S | 2-4h | Small task |
| M | 4-8h | Standard task |
| L | 8-16h | Large complex task |
| XL | 16-32h | Major subsystem (consider breaking down) |

## Task Types

New Feature · Enhancement · Bug Fix · Refactor · Configuration · Testing · Documentation

## Sub-Task Metadata (Required)

| Field | Type | Example |
|-------|------|---------|
| `wave` | number | `1` |
| `type` | string | `"New Feature"` |
| `cost` | string | `"M"` |
| `costHours` | string | `"4-8h"` |
| `patchFile` | string | `"patches/TASK-1.1.patch"` |
| `planTaskNumber` | string | `"1.1"` |
| `skillSource` | string | `"unity-plan-deep"` |

Epic tasks require only: `epicNumber`, `skillSource`.
Plan tasks require only: `planFile`, `totalEpics`, `totalTasks`, `totalEstimate`, `skillSource`.

## Quality Checklist

- [ ] Every epic has task table with all required columns
- [ ] Code Changes column links to `.patch` file
- [ ] Each `.patch` uses unified diff format (applies via `git apply`)
- [ ] Acceptance criteria are short, outcome-focused
- [ ] Dependency graph and execution order included
- [ ] Cost summary consistent with per-task estimates
