# Prefab Work

Use this when creating, editing, reviewing, or debugging Unity prefabs and
prefab variants. Load `canvas-ui-work.md` as well when the prefab is a uGUI
screen, popup, HUD item, or reusable UI component.

## Efficient Workflow

1. Identify the real prefab owner: root prefab, nested prefab, variant, scene
   instance, or runtime-spawned asset.
2. Inspect overrides before editing. Decide which values belong on the base
   prefab, variant, or scene instance.
3. Make the smallest serialized change that solves the task. Avoid normalizing
   unrelated components, transforms, or inactive children.
4. Validate the prefab in Unity when possible. Raw YAML is useful for diff
   review, but it does not prove missing references, active states, or runtime
   reset behavior.
5. Capture evidence: prefab inspection, scene smoke, Play Mode path, screenshot,
   or focused test according to the prefab's runtime use.

## Standards

- Preserve prefab GUIDs and `.meta` files when moving or renaming assets.
  Broken GUIDs break scene and prefab references even when filenames look right.
- Prefer prefab variants for intentional theme, platform, or feature
  differences. Avoid duplicating whole prefabs when only visuals, data, or a few
  serialized values differ.
- Keep overrides intentional. Unintended overrides commonly hide inactive
  children, wrong anchors, stale references, raycast targets, disabled scripts,
  or temporary debug values.
- Do not bind reusable prefabs to scene objects. Use prefab-local serialized
  references, ScriptableObjects, events, or runtime injection according to the
  project pattern.
- For runtime-instantiated prefabs, validate root transform, required
  components, default active state, pooled reset state, and safe behavior when
  instantiated multiple times.
- For nested prefabs, edit the owner that should carry the change. Do not push a
  nested override up to the parent unless that parent is the real product
  variant.
- Keep naming, folder placement, Addressables labels, and bundle grouping aligned
  with nearby assets.

## Common Checks

- Missing scripts or missing object references
- Unexpected scene references
- Disabled required components
- Root scale or anchor values changed by accident
- Event subscriptions, button callbacks, animation bindings, and timeline tracks
- Pool reset state: active flags, visual selection, timers, text, sprites,
  materials, particles, sounds, and subscriptions
- Addressables key, label, group, and load/release ownership when applicable

## Verification

- Inspect the affected prefab or scene hierarchy in Unity when available.
- Run the user flow that instantiates or opens the prefab when the behavior is
  runtime-visible.
- For UI prefabs, also verify target aspect ratios, safe areas, input blocking,
  active states, and screenshots.
- For performance-sensitive prefabs, use Profiler or Frame Debugger evidence
  instead of assuming the serialized diff improved performance.
