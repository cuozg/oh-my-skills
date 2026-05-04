---
name: unity-prefab
description: "Create, modify, duplicate, wire, inspect, and validate Unity prefabs through Unity MCP tools. MUST use for prefab creation, component setup, serialized field references, prefab variants or duplicates, asset path validation, and non-destructive prefab modification. Prefer explicit asset paths over ambiguous object names and preserve existing prefabs unless modification is requested."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-prefab

Standardize safe prefab creation and modification through GameObject and asset inspection.

## When to use

Use for:

- Creating new prefabs from GameObjects.
- Modifying existing prefab components or serialized fields.
- Duplicating prefabs or creating prefab variants where supported.
- Wiring component references, materials, meshes, scripts, and child objects.
- Validating prefab assets after changes.

## Required inputs

- Explicit prefab path such as `Assets/Prefabs/Enemy.prefab`.
- Component list and serialized field values to add or change.
- Asset references by path for materials, sprites, meshes, audio, or other prefab dependencies.
- Clear instruction when an existing prefab should be modified.

## MCP tool usage

- Use `ManageGameObject(create/modify/add_component/set_component_property/get_components)` for object setup and component wiring.
- Use `ManageGameObject` with `save_as_prefab` or `prefab_path` when creating prefabs.
- Use `ManageAsset(GetInfo/Search/Duplicate/Move/Rename)` for prefab existence, duplication, or asset management.
- Use `ReadConsole` or `GetConsoleLogs` after prefab or component changes.
- Use scene capture tools only when visual placement or layout matters.

## Safety rules

- Preserve existing prefab assets unless the user explicitly requests modification.
- Prefer explicit asset paths over ambiguous object names.
- Verify referenced assets exist before assigning them.
- Avoid broad component rewrites; change only requested components and fields.
- Do not save scene changes unless scene persistence was requested.
- Keep prefab paths under `Assets/` and use descriptive names.

## Validation

Verify:

- Prefab asset exists at the expected path.
- Required components are present.
- Serialized fields and object/asset references are assigned correctly.
- Child hierarchy and transforms match the requested structure.
- Referenced assets exist and are not missing.
- Unity console has no serialization, missing script, prefab, import, or compile errors.

## Boundaries

- Delegate runtime component implementation to `unity-code`.
- Delegate generated meshes/materials/sprites to `unity-asset-generation`.
- Delegate scene layout and object placement to `unity-scene-builder`.
- Delegate custom prefab editor tooling to `unity-editor`.

## Handoff

Report prefab path, components added or changed, references assigned, validation evidence, and any manual inspector review recommended.
