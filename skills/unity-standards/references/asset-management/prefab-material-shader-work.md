# Prefab, Material, And Shader Asset Work

This is a compatibility map for older prompts that mention prefab, material, and
shader work together. Prefer the focused references below for new tasks so the
agent only loads the standard it needs.

## Load The Smallest Surface

| Surface | Load |
| --- | --- |
| Prefabs, variants, nested prefabs, runtime-spawned assets | `prefab-work.md` |
| uGUI Canvas screens, popups, HUDs, layout prefabs | `canvas-ui-work.md` |
| Material assets, assignments, property changes | `material-work.md` |
| ShaderLab, HLSL, Shader Graph, keywords, passes | `shader-work.md` |
| Draw calls, batching, overdraw, Canvas rebuilds | `../optimization/canvas-ui-drawcalls-batching.md` |

## Efficient Mixed-Asset Workflow

1. Start from the user's named asset, prefab, material, shader, scene, or visual
   symptom.
2. Identify the touched surface before loading references. For example, a button
   color bug may be Canvas UI, prefab override, material assignment, or shader
   clipping; do not assume all four.
3. Load one focused reference first. Add another only when the evidence crosses
   that boundary.
4. Verify through the real Unity surface: prefab inspection, Play Mode UI flow,
   Frame Debugger, profiler, screenshot, shader compile, or platform check.

## Shared Rules

- Preserve GUIDs and `.meta` files.
- Avoid unrelated YAML churn from opening and resaving assets casually.
- Keep asset ownership clear: base prefab vs variant, shared material vs
  instance, shader property vs material override, static UI vs dynamic UI.
- Use project-local naming, folder, Addressables, and render-pipeline patterns.
- Prove visual and performance claims with Unity evidence when possible.
