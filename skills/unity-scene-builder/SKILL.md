---
name: unity-scene-builder
description: "Build, modify, inspect, and validate Unity scenes using Unity MCP scene, GameObject, asset, and capture tools. MUST use for scene creation, loading, hierarchy setup, object placement, component wiring in scenes, camera/light/layout validation, and visual scene captures. Avoid destructive scene edits and save only when explicitly requested."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-scene-builder

Automate scene setup and validation with Unity MCP scene, GameObject, and capture tools.

## When to use

Use for:

- Scene creation and loading.
- Hierarchy setup and parent/child organization.
- Object placement, transforms, cameras, lights, and simple layout.
- Scene-level component wiring.
- Scene validation with hierarchy, console, and visual captures.

## MCP tool usage

- Use `ManageScene(Create/Load/Save/GetHierarchy/GetActive/GetBuildSettings)` for scene operations.
- Use `ManageGameObject(create/modify/delete/find/add_component/set_component_property/get_components)` for scene objects.
- Use `ManageAsset(Search/GetInfo)` for prefabs, materials, meshes, sprites, and scene assets.
- Use `Camera_Capture` for camera-specific validation.
- Use `SceneView_Capture2DScene` for 2D layouts and tilemap-style scenes.
- Use `SceneView_CaptureMultiAngleSceneView` for 3D scene structure validation.
- Use `ReadConsole` or `GetConsoleLogs` after scene or component changes.

## Safety rules

- Inspect active scene and hierarchy before editing.
- Preserve existing scenes unless the user explicitly requests modification.
- Save only when requested or when creating a new scene for the task.
- Avoid destructive scene edits unless the user explicitly asks.
- Prefer adding named parent containers for generated objects.
- Use explicit object paths or instance IDs when modifying existing objects.

## Execution guidance

1. Identify target scene and whether it should be created, loaded, or modified.
2. Inspect current hierarchy and relevant assets.
3. Create or modify objects in small groups.
4. Wire components and asset references explicitly.
5. Validate hierarchy and transforms.
6. Capture the scene when visual layout matters.
7. Check Unity console before reporting completion.

## Validation

Verify:

- Target scene is active or saved at the expected path.
- Required hierarchy objects exist with expected names, parents, active states, transforms, and components.
- Asset references are assigned correctly.
- Object placement is validated through hierarchy and, when relevant, captures.
- Unity console has no scene, missing script, serialization, import, or compile errors.

## Boundaries

- Delegate prefab asset creation to `unity-prefab`.
- Delegate generated meshes/materials/sprites/audio to `unity-asset-generation`.
- Delegate runtime gameplay logic to `unity-code`.
- Delegate UI Toolkit screens to `unity-uitoolkit`.

## Handoff

Report scene path, hierarchy changes, objects/components created or modified, save status, console status, and capture evidence when used.
