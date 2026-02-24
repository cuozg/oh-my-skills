---
name: unity-plan-shared
description: "Shared references, scripts, and standards for the Prometheus planning pipeline (unity-plan-quick, unity-plan-deep, unity-plan-detail). Contains investigation script, costing standards, pipeline flow, and investigation checklist. Not intended to be activated directly — loaded by planning skills as needed."
---
# Planning Shared Resources

Shared by `unity-plan-quick`, `unity-plan-deep`, `unity-plan-detail`.

## References

| File | Content |
|------|---------|
| [prometheus-pipeline.md](references/prometheus-pipeline.md) | Pipeline flow, task hierarchy, unified metadata schema, dependency wiring |
| [investigation-checklist.md](references/investigation-checklist.md) | Pre-planning investigation questions, size/time reference tables |
| [costing-and-types.md](references/costing-and-types.md) | Costing tiers (XS-XL), task types, metadata schema |

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/investigate_feature.py "<term>"` | Search codebase for feature-related classes, tests, config, prefabs, integration points |
| `scripts/investigate_feature.py --init <plan-name> [keywords]` | Create plan output folder + run investigation |

## Pipeline Overview

```
unity-plan-quick  →  Assessment (inline report + task_create)
        ↓ assessmentTaskId
unity-plan-deep   →  Markdown plan + patches + task_create
   — OR —
unity-plan-detail →  HTML plan (3 tabs) + patches (no task_create)
```

`plan-deep` and `plan-detail` are alternatives, not sequential. Both accept an assessment task ID from `plan-quick`.
