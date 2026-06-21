# Architecture, Systems, And Platform

Use this file for feature structure, asmdefs, dependency direction, events, refactoring, editor code, and platform boundaries.

## Architecture Principles

- Fit the existing project architecture before introducing a new pattern.
- Organize around features and ownership, not generic type folders.
- Keep runtime code independent from editor-only APIs.
- Keep dependencies visible through constructors, serialized fields, or composition roots.
- Use interfaces for real boundaries, tests, or alternate implementations; do not add them for every class by default.
- Prefer explicit data flow over global state.
- Keep platform-specific code behind a small boundary.

## Project Layout

A scalable Unity project usually benefits from feature-based organization:

```text
Assets/
  _Project/
    Core/
    Features/
      Combat/
        Scripts/
        Prefabs/
        Tests/
      Player/
        Scripts/
        Prefabs/
        Tests/
    Infrastructure/
    UI/
    Settings/
    Scenes/
  Plugins/
```

Rules:

- Keep feature runtime code, prefabs, tests, and local assets close together.
- Put shared interfaces, value types, and cross-feature contracts in `Core`.
- Put bootstrapping, DI installation, scene loading, and platform adapters in `Infrastructure`.
- Keep third-party packages isolated under `Plugins`, `Packages`, or the project's established convention.
- Avoid `Resources` for large or dynamic content; prefer Addressables or direct references when the project uses them.

## Assembly Definitions

Use asmdefs to keep compile boundaries and dependency direction clear.

```text
Game.Core              <- no feature dependencies
Game.Combat           -> Game.Core
Game.UI               -> Game.Core
Game.Infrastructure   -> Game.Core, Game.Combat, Game.UI
Game.Combat.Editor    -> Game.Combat, UnityEditor
Game.Combat.Tests     -> Game.Combat, test framework
```

Standards:

- Runtime assemblies must not reference Editor assemblies.
- Feature assemblies should not reference each other casually. Route shared contracts through Core or an explicit integration layer.
- Test assemblies reference the code under test, not the whole game by default.
- Match namespace and assembly names when practical.
- Do not add asmdefs during a tiny fix unless the project already uses them for that area.

## Dependencies

Choose the lightest dependency mechanism that keeps ownership clear:

| Need | Good Fit |
| --- | --- |
| Pure C# service | Constructor injection |
| Scene-authored reference | `[SerializeField]` |
| Unity component on same object | `GetComponent` in `Awake` plus `[RequireComponent]` |
| Cross-scene service | Existing DI/composition root |
| Designer-authored tuning | ScriptableObject asset |
| Legacy/static integration | Small adapter around the static API |

Avoid adding service locators or singletons for new code. If the project already has global access patterns, keep new usage narrow and do not spread the dependency further.

```csharp
public sealed class DamageService
{
    private readonly IArmorTable _armorTable;

    public DamageService(IArmorTable armorTable)
    {
        _armorTable = armorTable ?? throw new ArgumentNullException(nameof(armorTable));
    }
}
```

For MonoBehaviours, dependencies are usually serialized references or injected by the project's established DI framework. Do not introduce VContainer, Zenject, or another framework unless the project already uses it or the user asked for architecture work.

## Events And Messaging

Use the narrowest event mechanism that fits:

| Mechanism | Use |
| --- | --- |
| C# event | Code-to-code notifications in the same runtime domain. |
| UnityEvent | Designer-wired Inspector reactions. |
| ScriptableObject event channel | Decoupled scene/asset-driven notifications when the project already uses the pattern. |
| Message bus/mediator | Cross-feature messaging with many publishers/subscribers and clear ownership. |

Event standards:

- Name events by what happened: `HealthChanged`, `Died`, `PurchaseCompleted`.
- Subscribe and unsubscribe at matching lifetimes.
- Avoid event payloads that expose mutable internals.
- Keep event handlers small; dispatch to explicit methods for real work.
- Avoid global event buses for local relationships.

## State And Feature Boundaries

Keep state ownership explicit:

- A component owns only the state it can initialize, validate, and reset.
- UI views display state; presenters/controllers decide what state means.
- Save systems own persistence format and migrations, not gameplay rules.
- Network/server response handlers hydrate from authoritative responses instead of recomputing local truth.
- Feature flags should guard the smallest behavior surface that actually changes.

When a feature crosses systems, write down the integration points before changing code: data source, owner, events, UI, persistence, analytics, assets, and tests.

## Production Feature Boundaries

For features that affect product goals, LiveOps, analytics, IAP, server APIs, or
release behavior, load `../production/full-cycle-ownership.md` before changing
architecture. These features need more than clean code boundaries:

- Product goal and success signal should be known before implementation.
- Client/server authority must be explicit for economy, purchases, inventory,
  progression, attribution, and other business-critical state.
- Remote config and blueprint systems need validation, defaults, rollback, and
  expired-data cleanup, not just a deserializer.
- Analytics instrumentation belongs in the feature design and test plan, with
  event meaning and timing clarified before code.
- Post-launch monitoring and rollback paths are part of ownership for risky
  features.

## Patterns Worth Using

Use patterns when they reduce concrete complexity:

- Strategy: interchangeable algorithms or tuning assets.
- State machine: explicit states with controlled transitions.
- Command: undo/redo, input replay, queued actions.
- Adapter: isolate platform, SDK, static API, or third-party code.
- Presenter/controller: keep UI Toolkit, uGUI, or scene views from owning business rules.

Do not introduce patterns as ceremony. A single `switch` can be better than a class hierarchy when behavior is small and stable.

## Refactoring Standards

Before refactoring:

1. Identify the behavior that must not change.
2. Find existing tests, scenes, prefabs, or logs that prove it.
3. Make one structural change at a time.
4. Compile and run the narrowest meaningful verification after each risky step.

Prefer these safe moves:

- Extract pure methods from large MonoBehaviours.
- Extract data into ScriptableObjects when values are shared and designer-authored.
- Extract interfaces only at real seams: tests, alternate implementations, package/platform boundaries.
- Replace inheritance with components when behavior combinations are growing.
- Move editor-only code into `Editor` folders or editor assemblies.

Do not combine behavior changes with cleanup unless the cleanup is required to make the behavior change safely.

## Editor Code

Editor scripts must be isolated from runtime builds.

Standards:

- Place editor scripts in an `Editor` folder or editor-only asmdef.
- Wrap editor-only code with `#if UNITY_EDITOR` only for small runtime-adjacent helpers; do not scatter it through gameplay logic.
- Use `SerializedObject` and `SerializedProperty` in inspectors so Undo, prefab overrides, and multi-object editing work.
- Record Undo before mutating scene objects or assets.
- Mark modified assets dirty only when needed.
- Keep editor tools deterministic and safe for dirty scenes.

```csharp
Undo.RecordObject(target, "Update Spawn Radius");
serializedObject.ApplyModifiedProperties();
```

## Gizmos And Scene Handles

- Use gizmos for passive visualization.
- Use handles for interactive editing in custom editors.
- Keep gizmo drawing cheap and guarded by selection when possible.
- Do not mutate runtime state from `OnDrawGizmos`.

## WebGL And Platform Boundaries

WebGL and mobile platforms impose real constraints. Keep platform behavior behind interfaces or small adapters.

Common WebGL considerations:

- No normal background threads in player builds.
- Browser storage and file access differ from desktop.
- Networking, compression, and caching depend on server/browser configuration.
- Reflection-heavy and dynamically loaded code can be affected by IL2CPP stripping.
- Memory is more constrained; large synchronous loads are risky.

Use platform branches near composition:

```csharp
#if UNITY_WEBGL && !UNITY_EDITOR
    ISaveStorage storage = new WebGlSaveStorage();
#else
    ISaveStorage storage = new FileSaveStorage();
#endif
```

## Verification Expectations

Architecture changes need evidence beyond compilation:

- asmdef/reference changes: compile affected assemblies and tests.
- scene/prefab dependency changes: inspect affected assets or run scene smoke checks.
- event/lifecycle changes: verify subscribe/unsubscribe paths.
- platform branches: run or at least compile the target-specific branch when available.
- refactors: show tests or direct behavior checks for the behavior that should remain unchanged.
