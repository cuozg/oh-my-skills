# Official Unity Source Map

Use these docs when a reference depends on Unity version, package version, or platform behavior. Prefer the official page before making claims about support windows, platform limits, or package APIs.

## How To Use This Map

- Pair topic-specific references with the matching official docs below when behavior is version-sensitive.
- Prefer Manual pages for workflows and constraints; prefer Scripting API pages for exact API behavior.
- Package pages matter for Addressables, Burst, Collections, and the Test Framework because package versions vary by editor version.
- Match the docs version to the local editor before making hard version claims.

## Core Runtime And Serialization

- Script serialization manual:
  `https://docs.unity3d.com/cn/2023.1/Manual/script-Serialization.html`
- MonoBehaviour API:
  `https://docs.unity3d.com/2023.1/Documentation/ScriptReference/MonoBehaviour.html`
- SerializeField API:
  `https://docs.unity3d.com/kr/530/ScriptReference/SerializeField.html`

Use these for:
- Serialized field rules and inspector behavior
- `destroyCancellationToken`, `didAwake`, and destroyed-object null semantics
- Confirming that inspector editing targets serialized backing fields, not property accessors

## Async And Concurrency

- Awaitable manual:
  `https://docs.unity3d.com/cn/current/Manual/async-await-support.html`
- Awaitable API:
  `https://docs.unity3d.com/ja/6000.0/ScriptReference/Awaitable.html`
- C# Job System overview:
  `https://docs.unity3d.com/cn/2022.3/Manual/JobSystemOverview.html`
- Burst package docs:
  `https://docs.unity3d.com/cn/2023.2/Manual/com.unity.burst.html`
- Collections package docs:
  `https://docs.unity3d.com/cn/2023.2/Manual/com.unity.collections.html`

Use these for:
- `Awaitable` availability and semantics
- The fact that `Awaitable` instances are pooled and must not be awaited multiple times
- Job scheduling, dependencies, NativeContainer safety, and Burst package support

## UI Toolkit

- Runtime UI setup:
  `https://docs.unity3d.com/cn/2023.2/Manual/UIE-render-runtime-ui.html`
- Panel Settings reference:
  `https://docs.unity3d.com/cn/2022.1/Manual/UIE-Runtime-Panel-Settings.html`
- UI Document component:
  `https://docs.unity3d.com/jp/current/Manual/UIE-create-ui-document-component.html`
- Runtime and editor data binding:
  `https://docs.unity3d.com/ja/2023.2/Manual/UIE-data-binding.html`

Use these for:
- `UIDocument`, `PanelSettings`, sort order, and runtime rendering
- Runtime UI data binding support and current limitations

## Performance, Pooling, And Asset Loading

- ObjectPool API:
  `https://docs.unity3d.com/kr/current/ScriptReference/Pool.ObjectPool_1.html`
- IObjectPool API:
  `https://docs.unity3d.com/kr/2022.2/ScriptReference/Pool.IObjectPool_1.html`
- Addressables package docs:
  `https://docs.unity3d.com/cn/2023.2/Manual/com.unity.addressables.html`

Use these for:
- Built-in object pooling support windows and API semantics
- Addressables package version compatibility with the current editor

## Web Platform

- Web technical limitations:
  `https://docs.unity3d.com/cn/2023.2/Manual/webgl-technical-overview.html`
- Unity 6 system requirements:
  `https://docs.unity3d.com/6000.0/Documentation/Manual/system-requirements.html`

Use these for:
- Current Web platform limitations, including filesystem and threading constraints
- Whether a target browser or device class is officially supported

## Testing

- Automated testing manual:
  `https://docs.unity3d.com/cn/current/Manual/testing-editortestsrunner.html`
- Test Framework package docs:
  `https://docs.unity3d.com/cn/2023.2/Manual/com.unity.test-framework.html`

Use these for:
- Edit Mode vs Play Mode guidance
- Package-version-specific Test Framework capabilities

## Notes For AI Output

- Do not state exact Unity version cutoffs unless they are confirmed against the official docs above.
- Treat package-backed systems as package-version-dependent even when the editor version is known.
- If a local project uses older APIs or older docs conventions, preserve project consistency and call out the version assumption explicitly.
