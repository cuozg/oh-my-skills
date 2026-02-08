# Unity-MCP Tools Reference

Complete reference for all MCP tools with full parameters.

## Table of Contents

- [Infrastructure Tools](#infrastructure-tools)
- [Scene Tools](#scene-tools)
- [GameObject Tools](#gameobject-tools)
- [Script Tools](#script-tools)
- [Asset Tools](#asset-tools)
- [Material & Shader Tools](#material--shader-tools)
- [Editor Control Tools](#editor-control-tools)
- [Testing Tools](#testing-tools)
- [Search Tools](#search-tools)

---

## Infrastructure Tools

### batch_execute

Execute multiple MCP commands in a single batch (10-100x faster).

```python
batch_execute(
    commands=[                    # list[dict], required, max 25
        {"tool": "tool_name", "params": {...}},
    ],
    parallel=False,              # bool - run read-only ops in parallel
    fail_fast=False,             # bool - stop on first failure
    max_parallelism=None         # int - max parallel workers
)
```

### set_active_instance

Route commands to a specific Unity instance.

```python
set_active_instance(instance="ProjectName@abc123")  # Name@hash or hash prefix
```

### refresh_unity

Refresh asset database and trigger script compilation.

```python
refresh_unity(
    mode="if_dirty",             # "if_dirty" | "force"
    scope="all",                 # "assets" | "scripts" | "all"
    compile="none",              # "none" | "request"
    wait_for_ready=True          # bool - wait until editor ready
)
```

---

## Scene Tools

### manage_scene

```python
# Hierarchy (paginated)
manage_scene(action="get_hierarchy", page_size=50, cursor=0, parent=None, include_transform=False)

# Screenshot
manage_scene(action="screenshot")  # Returns base64 PNG

# Scene info
manage_scene(action="get_active")
manage_scene(action="get_build_settings")

# Scene CRUD
manage_scene(action="create", name="NewScene", path="Assets/Scenes/")
manage_scene(action="load", path="Assets/Scenes/Main.unity")
manage_scene(action="save")
```

### find_gameobjects

```python
find_gameobjects(
    search_term="Player",
    search_method="by_name",     # by_name|by_tag|by_layer|by_component|by_path|by_id
    include_inactive=False,
    page_size=50, cursor=0       # max 500
)
# Returns: {"ids": [12345, 67890], "next_cursor": 50}
```

---

## GameObject Tools

### manage_gameobject

```python
# Create
manage_gameobject(action="create", name="MyCube", primitive_type="Cube",  # Cube|Sphere|Capsule|Cylinder|Plane|Quad
    position=[0,1,0], rotation=[0,45,0], scale=[1,1,1],
    components_to_add=["Rigidbody", "BoxCollider"],
    save_as_prefab=False, prefab_path="Assets/Prefabs/MyCube.prefab")

# Modify
manage_gameobject(action="modify", target="Player", search_method="by_name",
    position=[10,0,0], rotation=[0,90,0], scale=[2,2,2],
    set_active=True, layer="Player",
    components_to_add=["AudioSource"], components_to_remove=["OldComponent"],
    component_properties={"Rigidbody": {"mass": 10.0, "useGravity": True}})

# Delete
manage_gameobject(action="delete", target="OldObject")

# Duplicate
manage_gameobject(action="duplicate", target="Player", new_name="Player2", offset=[5,0,0])

# Move relative
manage_gameobject(action="move_relative", target="Player",
    reference_object="Enemy",  # optional
    direction="left",          # left|right|up|down|forward|back
    distance=5.0, world_space=True)
```

### manage_components

```python
# Add
manage_components(action="add", target=12345, component_type="Rigidbody", search_method="by_id")

# Remove
manage_components(action="remove", target="Player", component_type="OldScript")

# Set single property
manage_components(action="set_property", target=12345, component_type="Rigidbody",
    property="mass", value=5.0)

# Set multiple properties
manage_components(action="set_property", target=12345, component_type="Transform",
    properties={"position": [1,2,3], "localScale": [2,2,2]})
```

---

## Script Tools

### create_script

```python
create_script(path="Assets/Scripts/MyScript.cs",
    contents="using UnityEngine;\n\npublic class MyScript : MonoBehaviour { }",
    script_type="MonoBehaviour", namespace="MyGame")
```

### script_apply_edits

Structured edits (safer than raw text):

```python
script_apply_edits(name="MyScript", path="Assets/Scripts", edits=[
    {"op": "replace_method", "methodName": "Update", "replacement": "void Update() { }"},
    {"op": "insert_method", "afterMethod": "Start", "code": "void OnEnable() { }"},
    {"op": "delete_method", "methodName": "OldMethod"},
    {"op": "anchor_insert", "anchor": "void Start()", "position": "before", "text": "// comment\n"},
    {"op": "regex_replace", "pattern": "Debug\\.Log\\(", "text": "Debug.LogWarning("},
    {"op": "prepend", "text": "// Header\n"},
    {"op": "append", "text": "\n// Footer"}
])
```

### apply_text_edits

Precise character-position edits (1-indexed):

```python
apply_text_edits(uri="mcpforunity://path/Assets/Scripts/MyScript.cs",
    edits=[{"startLine": 10, "startCol": 5, "endLine": 10, "endCol": 20, "newText": "new text"}],
    precondition_sha256="abc123...", strict=True)
```

### validate_script

```python
validate_script(uri="mcpforunity://path/Assets/Scripts/MyScript.cs",
    level="standard", include_diagnostics=True)  # "basic"|"standard"
```

### get_sha

```python
get_sha(uri="mcpforunity://path/Assets/Scripts/MyScript.cs")
# Returns: {"sha256": "...", "lengthBytes": 1234, "lastModifiedUtc": "..."}
```

### delete_script

```python
delete_script(uri="mcpforunity://path/Assets/Scripts/OldScript.cs")
```

---

## Asset Tools

### manage_asset

```python
# Search (paginated)
manage_asset(action="search", path="Assets", search_pattern="*.prefab",
    filter_type="Prefab", page_size=25, page_number=1, generate_preview=False)

# Info
manage_asset(action="get_info", path="Assets/Prefabs/Player.prefab")

# Create
manage_asset(action="create", path="Assets/Materials/New.mat",
    asset_type="Material", properties={"color": [1,0,0,1]})

# File ops
manage_asset(action="duplicate", path="Assets/A.prefab", destination="Assets/B.prefab")
manage_asset(action="move", path="Assets/A.prefab", destination="Assets/Prefabs/A.prefab")
manage_asset(action="rename", path="Assets/A.prefab", destination="Assets/B.prefab")
manage_asset(action="create_folder", path="Assets/NewFolder")
manage_asset(action="delete", path="Assets/OldAsset.asset")
```

### manage_prefabs

```python
manage_prefabs(action="get_info", prefab_path="Assets/Prefabs/Player.prefab")
manage_prefabs(action="get_hierarchy", prefab_path="Assets/Prefabs/Player.prefab")
manage_prefabs(action="create_from_gameobject", target="Player",
    prefab_path="Assets/Prefabs/Player.prefab", allow_overwrite=False)
manage_prefabs(action="modify_contents", prefab_path="Assets/Prefabs/Player.prefab",
    target="ChildObject", position=[0,1,0], components_to_add=["AudioSource"])
```

---

## Material & Shader Tools

### manage_material

```python
# Create
manage_material(action="create", material_path="Assets/Materials/Red.mat",
    shader="Standard", properties={"_Color": [1,0,0,1]})

# Info
manage_material(action="get_material_info", material_path="Assets/Materials/Red.mat")

# Set shader property
manage_material(action="set_material_shader_property",
    material_path="Assets/Materials/Red.mat", property="_Metallic", value=0.8)

# Set color
manage_material(action="set_material_color",
    material_path="Assets/Materials/Red.mat", property="_BaseColor", color=[0,1,0,1])

# Assign to renderer
manage_material(action="assign_material_to_renderer",
    target="MyCube", material_path="Assets/Materials/Red.mat", slot=0)

# Set renderer color directly
manage_material(action="set_renderer_color", target="MyCube",
    color=[1,0,0,1], mode="instance")  # shared|instance|property_block
```

### manage_texture

```python
# Create
manage_texture(action="create", path="Assets/Textures/Checker.png",
    width=64, height=64, fill_color=[255,255,255,255])

# Pattern
manage_texture(action="apply_pattern", path="Assets/Textures/Checker.png",
    pattern="checkerboard",  # checkerboard|stripes|dots|grid|brick
    palette=[[0,0,0,255], [255,255,255,255]], pattern_size=8)

# Gradient
manage_texture(action="apply_gradient", path="Assets/Textures/Gradient.png",
    gradient_type="linear", gradient_angle=45,  # linear|radial
    palette=[[255,0,0,255], [0,0,255,255]])
```

### manage_shader / manage_vfx

Manage shaders and VFX graphs. Refer to tool schema for available actions.

### manage_scriptable_object

Create and modify ScriptableObject assets. Refer to tool schema for available actions.

---

## Editor Control Tools

### manage_editor

```python
manage_editor(action="play")
manage_editor(action="pause")
manage_editor(action="stop")
manage_editor(action="set_active_tool", tool_name="Move")  # Move/Rotate/Scale
manage_editor(action="add_tag", tag_name="Enemy")
manage_editor(action="remove_tag", tag_name="OldTag")
manage_editor(action="add_layer", layer_name="Projectiles")
manage_editor(action="remove_layer", layer_name="OldLayer")
```

### execute_menu_item

```python
execute_menu_item(menu_path="File/Save Project")
execute_menu_item(menu_path="GameObject/3D Object/Cube")
```

### read_console

```python
# Get messages
read_console(action="get", types=["error", "warning"], count=10,
    filter_text="NullReference", page_size=50, cursor=0,
    format="detailed", include_stacktrace=True)

# Clear
read_console(action="clear")
```

---

## Testing Tools

### run_tests

```python
result = run_tests(mode="EditMode",  # EditMode|PlayMode
    test_names=["MyTests.TestA"],
    group_names=["Integration*"],
    category_names=["Unit"],
    assembly_names=["Tests"],
    include_failed_tests=True)
# Returns: {"job_id": "abc123"}
```

### get_test_job

```python
result = get_test_job(job_id="abc123", wait_timeout=60,
    include_failed_tests=True, include_details=False)
# Returns: {"status": "complete"|"running"|"failed", "results": {...}}
```

---

## Search Tools

### find_in_file

```python
find_in_file(uri="mcpforunity://path/Assets/Scripts/MyScript.cs",
    pattern="public void \\w+", max_results=200, ignore_case=True)
```
