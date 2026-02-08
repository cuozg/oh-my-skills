# Unity-MCP Resources Reference

Resources provide read-only access to Unity state. Use `mcpforunity://` URI scheme.

## Table of Contents

- [Editor State Resources](#editor-state-resources)
- [Scene & GameObject Resources](#scene--gameobject-resources)
- [Prefab Resources](#prefab-resources)
- [Project Resources](#project-resources)
- [Instance Resources](#instance-resources)
- [Test Resources](#test-resources)

---

## Editor State Resources

### mcpforunity://editor/state

Editor readiness snapshot — check before tool operations.

```json
{
  "unity_version": "2022.3.10f1",
  "is_compiling": false,
  "is_domain_reload_pending": false,
  "play_mode": {"is_playing": false, "is_paused": false},
  "active_scene": {"path": "Assets/Scenes/Main.unity", "name": "Main"},
  "ready_for_tools": true,
  "blocking_reasons": [],
  "recommended_retry_after_ms": null,
  "staleness": {"age_ms": 150, "is_stale": false}
}
```

Key: Only proceed when `ready_for_tools == true`.

### mcpforunity://editor/selection

Currently selected objects: `activeObject`, `activeInstanceID`, `count`, `gameObjects[]`, `assetGUIDs[]`.

### mcpforunity://editor/active-tool

Current tool state: `activeTool`, `pivotMode`, `pivotRotation`.

### mcpforunity://editor/windows

All open editor windows with title, type, focus state, and position.

### mcpforunity://editor/prefab-stage

Current prefab editing context: `isOpen`, `assetPath`, `prefabRootName`, `isDirty`.

---

## Scene & GameObject Resources

### mcpforunity://scene/gameobject-api

Documentation for GameObject resource schema. Read this first.

### mcpforunity://scene/gameobject/{instance_id}

Basic GameObject metadata (no component properties):

```json
{
  "instanceID": 12345, "name": "Player", "tag": "Player",
  "layer": 8, "layerName": "Player", "active": true,
  "transform": {"position": [0,1,0], "rotation": [0,0,0], "scale": [1,1,1]},
  "parent": {"instanceID": 0},
  "children": [{"instanceID": 67890}],
  "componentTypes": ["Transform", "Rigidbody", "PlayerController"],
  "path": "/Player"
}
```

### mcpforunity://scene/gameobject/{instance_id}/components

All components with serialized properties (paginated). Params: `page_size` (max 100), `cursor`, `include_properties` (default true).

### mcpforunity://scene/gameobject/{instance_id}/component/{component_name}

Single component with full properties. Example: `.../component/Rigidbody`.

---

## Prefab Resources

**IMPORTANT**: URL-encode path slashes. `Assets/Prefabs/Player.prefab` → `Assets%2FPrefabs%2FPlayer.prefab`

### mcpforunity://prefab-api

Documentation for prefab resource schema.

### mcpforunity://prefab/{encoded_path}

Prefab asset info: `assetPath`, `guid`, `prefabType`, `rootObjectName`, `rootComponentTypes[]`, `childCount`, `isVariant`, `parentPrefab`.

### mcpforunity://prefab/{encoded_path}/hierarchy

Full hierarchy with nested prefab detection: `items[]` with `name`, `path`, `componentTypes[]`, `isNestedPrefab`, `nestedPrefabPath`.

---

## Project Resources

### mcpforunity://project/info

Static config: `projectRoot`, `projectName`, `unityVersion`, `platform`, `assetsPath`.

### mcpforunity://project/tags

All tags: `["Untagged", "Player", "Enemy", ...]`

### mcpforunity://project/layers

Layers 0-31: `{"0": "Default", "5": "UI", "8": "Player", ...}`

### mcpforunity://menu-items

All menu items: `["File/Save", "GameObject/3D Object/Cube", ...]`

### mcpforunity://custom-tools

Custom tools in active project with name, description, and parameter schemas.

---

## Instance Resources

### mcpforunity://instances

All running Unity Editor instances for multi-instance workflows:

```json
{
  "instance_count": 2,
  "instances": [
    {"id": "MyProject@abc123", "name": "MyProject", "hash": "abc123", "unity_version": "2022.3.10f1"}
  ]
}
```

Use with `set_active_instance(instance="MyProject@abc123")`.

---

## Test Resources

### mcpforunity://tests

All tests: `[{"name": "TestA", "full_name": "MyTests.TestA", "mode": "EditMode"}]`

### mcpforunity://tests/{mode}

Filter by mode: `mcpforunity://tests/EditMode` or `mcpforunity://tests/PlayMode`.

---

## Best Practices

1. **Check editor state first** — `ready_for_tools` must be true
2. **Find then read** — `find_gameobjects` for IDs, then resource URI for full data
3. **Paginate large queries** — Start with `include_properties=false`, read specific components as needed
4. **URL-encode prefab paths** — `/` → `%2F`
5. **Multi-instance awareness** — Check `mcpforunity://instances` when commands fail unexpectedly
