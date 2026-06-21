# Canvas UI Work

Use this for uGUI Canvas screens, popups, HUDs, buttons, layout prefabs,
animations, input blocking, screen-ratio behavior, and production UI wiring. For
UI Toolkit, use the `ui-toolkit/` references instead.

Load `optimization/canvas-ui-drawcalls-batching.md` only when the task involves
draw calls, batching, overdraw, rebuilds, or measurable UI performance.

## Efficient Workflow

1. Start from the named screen, prefab, scene, button, controller, or symptom.
2. Identify the runtime path: how the UI is opened, populated, refreshed,
   animated, blocked, closed, and reset.
3. Check the serialized prefab and the driving code together. UI bugs are often
   split between a stale prefab reference and a controller assumption.
4. Make the smallest UI change that preserves the current design system.
5. Verify in the actual resolution, aspect ratio, language, and state that the
   user cares about.

## Product UX Baseline

- Match the intended mockup, animation timing, interaction flow, loading state,
  and screen-ratio behavior before optimizing visuals.
- Provide immediate button feedback and prevent double-submit during server
  requests.
- Keep screen openings, transitions, scrolling, drag/drop, and popup navigation
  free of visible hitches.
- Preserve accessibility and readability basics: contrast, tap target size,
  disabled state, focus order when relevant, and text that fits.
- Choose preload vs lazy-load deliberately so first interaction stays
  responsive.
- For large lists, virtualize rows and generate only the visible range needed by
  the current UI pattern.

## Prefab And Layout Standards

- Keep anchors, pivots, safe-area handling, layout groups, and content sizing
  intentional. Responsive bugs usually come from accidental parent constraints.
- Avoid layout components in hot update paths. Nested `HorizontalLayoutGroup`,
  `VerticalLayoutGroup`, `ContentSizeFitter`, and changing preferred sizes can
  cause repeated rebuilds.
- Disable `Raycast Target` on non-interactive `Image` and `Text` graphics.
- Pool UI prefabs only when the reset contract is clear: active state,
  `CanvasGroup`, animation state, selected state, text, sprites, material
  overrides, and event subscriptions all need reset.
- Avoid storing mutable runtime state only in view components when the project
  already has a model, presenter, or controller boundary.
- Keep button callbacks and animation events pointed at stable controller
  methods. Remove callbacks only when your change made them obsolete.

## Materials, Sprites, And Masks

- Prefer sprite atlases and shared materials for elements rendered together.
- Avoid per-element material instances. A single `.material` access in a UI view
  can create unique materials and increase batches.
- Minimize masks, nested masks, soft masks, and custom UI shaders in dense UI
  unless the visual requirement justifies the cost.
- Verify clipping, stencil, alpha blending, and batching behavior when using
  custom UI shaders or masked content.

## Verification

- Inspect the prefab or scene hierarchy for active states, anchors, references,
  button callbacks, raycast targets, masks, materials, atlases, and Canvas
  boundaries.
- Run the UI flow in Play Mode when the behavior depends on data binding,
  animation, input, server state, or pooling.
- Capture screenshots for visual changes at the relevant aspect ratio and
  quality tier.
- For optimization claims, capture before/after draw calls, batches, SetPass
  calls, Canvas rebuild time, frame time, or overdraw evidence.
