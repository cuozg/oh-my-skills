# Canvas UI, Draw Calls, And Batching

Use this for uGUI Canvas performance: rebuilds, draw calls, batching, overdraw,
and atlas usage. UX baseline, prefab/layout standards, and pool reset contracts
live in `references/asset-management/canvas-ui-work.md`. For UI Toolkit, load
`references/ui-toolkit/performance.md` or the `unity:ui-uitk` skill. Deeper
coverage: `unity:ui-ugui`, `unity:manage-sprite-atlas` (atlas setup),
`unity:optimize-text-mesh-pro` (TMP fonts and text cost).

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
- For screens toggled often, disable the `Canvas` component instead of
  `SetActive(false)` on the root: the Canvas keeps its geometry and skips a full
  rebuild when re-enabled.

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

For non-UI renderers (SRP Batcher, GPU Resident Drawer, instancing, static
batching), see the Batching Choice Matrix in `rendering-settings.md`.

## Verification

- Use the Profiler UI and UI Details modules for Canvas rebuilds, layout
  rebuilds, and UI batch counts.
- Use Frame Debugger to prove why a batch broke: texture, material, shader pass,
  clipping, stencil, or Canvas boundary.
- Capture before/after draw calls, batches, SetPass calls, Canvas rebuild time,
  or frame time for optimization claims.
- For UI prefab edits, inspect raycast targets, active states, masks, materials,
  atlases, and Canvas boundaries in the actual prefab or scene.
- For production UI, also verify target device or representative low-end
  behavior: screen open time, scroll smoothness, draw calls, overdraw, and
  loading/error states for server-backed content.
