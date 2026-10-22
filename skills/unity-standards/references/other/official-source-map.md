# Official Unity Source Map

Use these docs when a reference depends on Unity version, package version, or platform behavior. Prefer the official page before making claims about support windows, platform limits, or package APIs.

## How To Use This Map

- Pair topic-specific references with the matching official docs below when behavior is version-sensitive.
- Prefer Manual pages for workflows and constraints; prefer Scripting API pages for exact API behavior.
- Package pages matter for Addressables, Burst, Collections, and the Test Framework because package versions vary by editor version.
- URLs below target Unity 6.0 (`6000.0`); swap the segment for the project's Editor
  version (`ProjectSettings/ProjectVersion.txt`) or drop it (`https://docs.unity3d.com/Manual/<page>.html`) for the latest.
- Package `@x.y` pins are examples; open the Manual `com.unity.<pkg>.html` page for the
  versions released for the Editor, then match `Packages/manifest.json`.

## Core Runtime And Serialization

- Script serialization manual:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/script-serialization.html`
- MonoBehaviour API:
  `https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MonoBehaviour.html`
- SerializeField API:
  `https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SerializeField.html`

Use these for:
- Serialized field rules and inspector behavior
- `destroyCancellationToken`, `didAwake`, and destroyed-object null semantics
- Confirming that inspector editing targets serialized backing fields, not property accessors

## Async And Concurrency

- Awaitable manual:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/async-await-support.html`
- Awaitable API:
  `https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Awaitable.html`
- C# Job System overview:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/job-system-overview.html`
- Burst package docs:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/com.unity.burst.html` (version list), `https://docs.unity3d.com/Packages/com.unity.burst@1.8/manual/index.html`
- Collections package docs:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/com.unity.collections.html` (version list)

Use these for:
- `Awaitable` availability and semantics
- The fact that `Awaitable` instances are pooled and must not be awaited multiple times
- Job scheduling, dependencies, NativeContainer safety, and Burst package support

## UI Toolkit

- Runtime UI setup:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-render-runtime-ui.html`
- Panel Settings reference:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-Runtime-Panel-Settings.html`
- UI Document component:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-create-ui-document-component.html`
- Runtime and editor data binding:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-runtime-binding.html`
- Binding mode and update trigger:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-runtime-binding-mode-update.html`
- Custom controls (`[UxmlElement]`, `[UxmlAttribute]`):
  `https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-create-custom-controls.html`
- USS custom properties (variables):
  `https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS-CustomProperties.html`
- Hiding and managing elements (performance):
  `https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-best-practices-for-managing-elements.html`

Use these for:
- `UIDocument`, `PanelSettings`, sort order, and runtime rendering
- Runtime UI data binding support and current limitations

## Performance, Pooling, And Asset Loading

- ObjectPool API:
  `https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Pool.ObjectPool_1.html`
- IObjectPool API:
  `https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Pool.IObjectPool_1.html`
- Addressables package docs:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/com.unity.addressables.html` (version list)
- Addressables memory management:
  `https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/MemoryManagement.html`
- Addressables asset loading:
  `https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/load-assets.html`
- Addressables operations and handles:
  `https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/AddressableAssetsAsyncOperationHandle.html`

Use these for:
- Built-in object pooling support windows and API semantics
- Addressables package version compatibility with the current editor
- Addressables handle ownership, release rules, async loading, labels, groups,
  and content update behavior

## Rendering, Materials, Shaders, Prefabs, And Canvas UI

- SRP Batcher manual:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/SRPBatcher.html`
- Draw call batching manual:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/DrawCallBatching.html`
- GPU instancing manual:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/GPUInstancing.html`
- Shader variants manual:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/shader-variants.html`
- Prefab variants manual:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/PrefabVariants.html`
- Nested prefabs manual:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/NestedPrefabs.html`
- Unity UI optimization guide:
  `https://unity.com/how-to/unity-ui-optimization-tips`

Use these for:
- SRP Batcher, static batching, dynamic batching, GPU instancing, and shader
  variant claims
- Prefab variant and nested prefab workflow rules
- Canvas rebuild, raycast target, layout, atlas, mask, and UI batching guidance

## Web Platform

- Web platform technical limitations:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/webgl-technical-overview.html`
- Unity 6 system requirements:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/system-requirements.html`

Use these for:
- Current Web platform limitations, including filesystem and threading constraints
- Whether a target browser or device class is officially supported

## IAP, Billing, Store Review, And Compliance

- Unity IAP docs:
  `https://docs.unity.com/en-us/iap`
- Unity IAP package docs:
  `https://docs.unity3d.com/Packages/com.unity.purchasing@5.3/manual/index.html`
- Unity IAP v5 upgrade guide:
  `https://docs.unity.com/en-us/iap/upgrade-to-iap-v5`
- Google Play Billing:
  `https://developer.android.com/google/play/billing`
- Google Play alternative billing:
  `https://developer.android.com/google/play/billing/alternative/alternative-billing-with-user-choice-in-app`
- Apple App Review Guidelines:
  `https://developer.apple.com/app-store/review/guidelines/`
- Apple App Review overview:
  `https://developer.apple.com/distribute/app-review/`

Use these for:
- Current Unity IAP package APIs and migration behavior
- Billing, alternative billing, store policy, privacy, tracking, metadata, and
  app-review requirements
- Avoiding stale assumptions about regional billing rules, review timing, or
  compliance checklists

## Testing

- Test Framework (core package in Unity 6, version fixed to the Editor):
  `https://docs.unity3d.com/6000.0/Documentation/Manual/com.unity.test-framework.html`
- Test Framework 1.4 manual (Unity 6 uses 1.4+; the Unity 6 Manual page above links the matching version):
  `https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/index.html`
- Edit Mode vs Play Mode:
  `https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/edit-mode-vs-play-mode-tests.html`
- Async tests:
  `https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-async-tests.html`
- Test assembly setup:
  `https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/workflow-create-test-assembly.html`

Use these for:
- Edit Mode vs Play Mode guidance and test asmdef rules
- Package-version-specific Test Framework capabilities

## Unity CLI

- Plugin skill `unity:unity-cli` (full CLI reference); local routing:
  `references/other/unity-cli-routing.md`

Use these for:
- Running tests (`unity test`), builds, live-Editor commands, and Editor/project version checks

## Notes For AI Output

- Do not state exact Unity version cutoffs unless they are confirmed against the official docs above.
- Treat package-backed systems as package-version-dependent even when the editor version is known.
- If a local project uses older APIs or older docs conventions, preserve project consistency and call out the version assumption explicitly.
