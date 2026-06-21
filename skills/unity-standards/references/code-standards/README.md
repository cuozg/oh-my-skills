# Code Standards Reference Map

These files are compact Unity coding standards for agents writing, reviewing, or refactoring production C#.
Load only the file that matches the work surface, then apply the target repository's existing style first.

## How To Use These Standards

1. Inspect the current project before applying a rule. Existing architecture, Unity version, packages, and team conventions override generic guidance.
2. Prefer the smallest change that satisfies the request and keeps behavior verifiable.
3. Treat examples as patterns, not code to paste blindly. Rename, trim, and adapt to the surrounding code.
4. Verify with the narrowest meaningful check: compile, focused unit/Edit Mode test, Play Mode smoke, prefab/scene inspection, or profiler evidence.
5. For package-sensitive APIs, check `Packages/manifest.json` and load `references/other/official-source-map.md`.

## Files

| File | Load When |
| --- | --- |
| `core-conventions.md` | Naming, formatting, fields, serialization attributes, null safety, comments, and basic Unity C# shape. |
| `lifecycle-async-errors.md` | MonoBehaviour lifecycle, subscriptions, async/coroutines, cancellation, validation, logging, and error handling. |
| `performance-data.md` | Runtime allocations, collections, LINQ, pooling, serialization, ScriptableObject data, and save data. |
| `architecture-systems.md` | Folder layout, asmdefs, dependencies, events, feature boundaries, editor code, refactoring, and WebGL constraints. |
| `ecs-burst-standards.md` | Entities, Jobs, Burst, NativeContainers, Bakers, structural changes, and DOTS migration decisions. |

Related non-code standards:

| File | Load When |
| --- | --- |
| `../asset-management/addressables-asset-manager.md` | Asset manager, Addressables, runtime loading, catalogs, labels, handles, and release ownership. |
| `../asset-management/prefab-material-shader-work.md` | Prefab, material, shader, sprite atlas, and renderer asset work. |
| `../optimization/canvas-ui-drawcalls-batching.md` | uGUI Canvas optimization, UI draw calls, batching, masks, atlases, and overdraw. |
| `../production/full-cycle-ownership.md` | Product goals, analytics, LiveOps, remote config, server APIs, IAP, release readiness, and monitoring. |

## Senior-Engineer Baseline

- Match local style before imposing a generic rule.
- Keep behavior explicit: public API is intentional, serialized state is private, dependencies are visible.
- Avoid speculative abstraction. Add an interface, service, event channel, or base class only when it removes concrete coupling or enables tests.
- Fail early in authoring/configuration paths; degrade gracefully only for expected runtime conditions.
- Keep hot paths allocation-free unless profiler data says the cost is irrelevant.
- Use Unity APIs on the main thread unless the API explicitly supports jobs or worker threads.
- Prefer tests and direct Unity validation over confidence from inspection alone.
- For production features, include analytics correctness, LiveOps maintainability,
  release risk, and post-launch observability in the definition of done.
