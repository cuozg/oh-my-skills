# Unity Code Review Checklist

Check changed files first. Report only issues with concrete user impact,
regression risk, data-loss risk, build/runtime failure, or maintainability cost.
Severity order: CRITICAL > HIGH > MEDIUM > LOW > STYLE.

---

This checklist has been divided by Unity file type:

- [C# Scripts (.cs)](checklist_cs.md)
- [Prefabs & Scenes (.prefab, .unity)](checklist_prefab.md)
- [Materials (.mat)](checklist_material.md)
- [Shaders (.shader, .shadergraph)](checklist_shader.md)
- [ECS, Jobs & Burst (.cs)](ecs-burst-review.md) - also load when C# touches Entities, Jobs, Burst, or NativeContainers

Large multi-type diffs: split passes per `references/review/parallel-review-criteria.md`.
Obsolete Unity 6 APIs: `references/quality/best-practices-audit.md`.

For PR mode, prefer findings on changed lines. For large prefab/scene changes
where inline comments are not practical, report body findings with object path,
component, serialized field, current value, and expected fix.

When a change touches analytics, LiveOps, remote config, server APIs, IAP,
release, or monitoring, also load `references/production/full-cycle-ownership.md` and
review whether the feature can be operated and observed after release.
