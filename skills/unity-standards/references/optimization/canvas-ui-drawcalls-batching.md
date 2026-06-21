# Canvas UI, Draw Calls, And Batching

Use this for uGUI Canvas performance, UI draw calls, batching, overdraw, atlas
usage, and UI prefab changes. For UI Toolkit, load the `ui-toolkit/` references
instead.

## Product UX Baseline

UI quality is runtime engineering work. Match the intended mockup, animation
timing, interaction flow, loading state, and screen-ratio behavior before
optimizing visuals. Players perceive quality through responsiveness and
smoothness.

- Provide immediate button feedback and prevent double-submit during server
  requests.
- Keep screen openings, transitions, scrolling, drag/drop, and popup navigation
  free of visible hitches.
- Choose preload vs lazy-load deliberately so first interaction stays responsive.
- For large lists, virtualize rows and generate only the needed visible range.

## Canvas Rebuilds

- Split dynamic and static UI into separate Canvases when frequent changes force
  expensive rebuilds. A changing timer, progress bar, or animated reward should
  not rebuild a large static screen.
- Keep Canvas count intentional. More Canvases reduce rebuild scope but add
  batches and management overhead.
- Avoid layout components in hot update paths. Nested `HorizontalLayoutGroup`,
  `VerticalLayoutGroup`, `ContentSizeFitter`, and constantly changing preferred
  sizes can cause repeated rebuilds.
- Disable `Raycast Target` on non-interactive `Image` and `Text` graphics so
  input raycasts do less work.
- Pool UI prefabs only when their reset contract is clear: active state,
  `CanvasGroup`, animation state, selected state, text, sprites, material
  overrides, and event subscriptions all need reset.

## Draw Calls And Batching

- UI batches break when material, texture, clipping/masking, shader pass, render
  queue, stencil state, or Canvas changes.
- Prefer sprite atlases and shared materials for elements rendered together.
- Minimize masks, nested masks, soft masks, and custom UI shaders in dense UI.
  They can add stencil work, extra passes, or break batching.
- Avoid per-element material instances. A single `.material` access in a UI view
  can create unique materials and increase batches.
- Use `Canvas.additionalShaderChannels` only for data the shaders actually need.

## Overdraw

- Large transparent full-screen images, layered panels, blurred backgrounds, and
  stacked alpha effects can cost more than their draw-call count suggests.
- Crop sprites tightly and avoid invisible transparent padding in atlases.
- Prefer disabling hidden UI roots over leaving transparent graphics active.
- Test on the target aspect ratio and quality tier; UI overdraw often changes
  with responsive layouts.

## Batching Choice Matrix

| Surface | Prefer | Watch For |
| --- | --- | --- |
| uGUI Canvas | Sprite atlases, shared materials, split static/dynamic Canvases | Masks, unique materials, frequent layout rebuilds |
| URP/HDRP renderers | SRP Batcher, shared shader variants | Non-compatible shaders or material CBUFFER layout |
| Repeated meshes | GPU instancing | Unique materials, unsupported shaders, SkinnedMeshRenderer limits |
| Static environment | Static batching | Memory growth and immovable objects |
| Small dynamic meshes | Usually SRP Batcher or instancing first | Dynamic batching CPU cost |

## Verification

- Use Unity Profiler UI modules for Canvas rebuilds, layout rebuilds, and UI
  batch counts.
- Use Frame Debugger to prove why a batch broke: texture, material, shader pass,
  clipping, stencil, or Canvas boundary.
- Capture before/after draw calls, batches, SetPass calls, Canvas rebuild time,
  or frame time for optimization claims.
- For UI prefab edits, inspect raycast targets, active states, masks, materials,
  atlases, and Canvas boundaries in the actual prefab or scene.
- For production UI, also verify target device or representative low-end
  behavior: screen open time, scroll smoothness, draw calls, overdraw, and
  loading/error states for server-backed content.
