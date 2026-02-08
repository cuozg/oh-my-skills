# Unity-MCP Workflow Patterns

Extended workflow patterns for common Unity development scenarios.

## Table of Contents

- [Scene Creation](#scene-creation)
- [Script Development](#script-development)
- [Asset Management](#asset-management)
- [Testing](#testing)
- [Debugging](#debugging)
- [Batch Operations](#batch-operations)
- [Error Recovery](#error-recovery)

---

## Scene Creation

### Complete Scene from Scratch

```python
manage_scene(action="create", name="GameLevel", path="Assets/Scenes/")

batch_execute(commands=[
    {"tool": "manage_gameobject", "params": {"action": "create", "name": "Ground", "primitive_type": "Plane", "position": [0,0,0], "scale": [10,1,10]}},
    {"tool": "manage_gameobject", "params": {"action": "create", "name": "Player", "primitive_type": "Capsule", "position": [0,1,0]}},
    {"tool": "manage_gameobject", "params": {"action": "create", "name": "DirectionalLight"}}
])

# Add light component
manage_components(action="add", target="DirectionalLight", component_type="Light")
manage_components(action="set_property", target="DirectionalLight", component_type="Light", property="type", value="Directional")

manage_gameobject(action="modify", target="Main Camera", position=[0,5,-10], rotation=[30,0,0])
manage_scene(action="screenshot")
manage_scene(action="save")
```

### Grid of Objects

```python
commands = []
for x in range(5):
    for z in range(5):
        commands.append({"tool": "manage_gameobject", "params": {
            "action": "create", "name": f"Cube_{x}_{z}", "primitive_type": "Cube", "position": [x*2, 0, z*2]
        }})
batch_execute(commands=commands[:25], parallel=True)
```

### Clone and Arrange

```python
result = find_gameobjects(search_term="Template", search_method="by_name")
for i in range(10):
    manage_gameobject(action="duplicate", target=result["ids"][0], new_name=f"Instance_{i}", offset=[i*2, 0, 0])
```

---

## Script Development

### Create and Attach Script

```python
create_script(path="Assets/Scripts/EnemyAI.cs", contents='''using UnityEngine;

public class EnemyAI : MonoBehaviour
{
    public float speed = 5f;
    public Transform target;

    void Update()
    {
        if (target != null)
        {
            Vector3 dir = (target.position - transform.position).normalized;
            transform.position += dir * speed * Time.deltaTime;
        }
    }
}''')

refresh_unity(mode="force", scope="scripts", compile="request", wait_for_ready=True)
errors = read_console(types=["error"], count=10)
# Only attach if no errors
manage_gameobject(action="modify", target="Enemy", components_to_add=["EnemyAI"])
manage_components(action="set_property", target="Enemy", component_type="EnemyAI", properties={"speed": 10.0})
```

### Safe Script Edit

```python
sha_info = get_sha(uri="mcpforunity://path/Assets/Scripts/PlayerController.cs")

script_apply_edits(name="PlayerController", path="Assets/Scripts", edits=[
    {"op": "replace_method", "methodName": "Update", "replacement": '''void Update()
    {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        transform.Translate(new Vector3(h, 0, v) * speed * Time.deltaTime);
    }'''}
])

validate_script(uri="mcpforunity://path/Assets/Scripts/PlayerController.cs", level="standard")
refresh_unity(mode="force", scope="scripts", compile="request", wait_for_ready=True)
read_console(types=["error"], count=10)
```

### Add Using + Method

```python
script_apply_edits(name="GameManager", path="Assets/Scripts", edits=[
    {"op": "anchor_insert", "anchor": "using UnityEngine;", "position": "after", "text": "\nusing UnityEngine.SceneManagement;"},
    {"op": "insert_method", "afterMethod": "Start", "code": '''
    public void ResetGame()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }'''}
])
```

---

## Asset Management

### Create and Apply Material

```python
manage_material(action="create", material_path="Assets/Materials/PlayerMat.mat",
    shader="Standard", properties={"_Color": [0.2,0.5,1.0,1.0], "_Metallic": 0.5, "_Glossiness": 0.8})

manage_material(action="assign_material_to_renderer", target="Player",
    material_path="Assets/Materials/PlayerMat.mat", slot=0)

manage_scene(action="screenshot")
```

### Procedural Texture Pipeline

```python
manage_texture(action="create", path="Assets/Textures/Checker.png", width=256, height=256, fill_color=[255,255,255,255])
manage_texture(action="apply_pattern", path="Assets/Textures/Checker.png",
    pattern="checkerboard", palette=[[0,0,0,255], [255,255,255,255]], pattern_size=32)
manage_material(action="create", material_path="Assets/Materials/CheckerMat.mat", shader="Standard")
```

### Organize Assets

```python
batch_execute(commands=[
    {"tool": "manage_asset", "params": {"action": "create_folder", "path": "Assets/Prefabs"}},
    {"tool": "manage_asset", "params": {"action": "create_folder", "path": "Assets/Materials"}},
    {"tool": "manage_asset", "params": {"action": "create_folder", "path": "Assets/Scripts"}},
    {"tool": "manage_asset", "params": {"action": "create_folder", "path": "Assets/Textures"}}
])

manage_asset(action="move", path="Assets/MyMaterial.mat", destination="Assets/Materials/MyMaterial.mat")
```

### Search and Process Assets

```python
result = manage_asset(action="search", path="Assets", search_pattern="*.prefab", page_size=50, generate_preview=False)
for asset in result["assets"]:
    info = manage_prefabs(action="get_info", prefab_path=asset["path"])
```

---

## Testing

### Run Specific Tests

```python
# List: mcpforunity://tests/EditMode
result = run_tests(mode="EditMode", test_names=["MyTests.TestPlayerMovement"], include_failed_tests=True)
final = get_test_job(job_id=result["job_id"], wait_timeout=60, include_failed_tests=True)

for test in final.get("failed_tests", []):
    print(f"FAILED: {test['name']}: {test['message']}")
```

### Run by Category

```python
result = run_tests(mode="EditMode", category_names=["Unit"], include_failed_tests=True)
status = get_test_job(job_id=result["job_id"], wait_timeout=60)
```

### TDD Pattern

```python
# 1. Write test
create_script(path="Assets/Tests/Editor/PlayerTests.cs", contents='''using NUnit.Framework;
using UnityEngine;

public class PlayerTests
{
    [Test]
    public void TestPlayerStartsAtOrigin()
    {
        var player = new GameObject("TestPlayer");
        Assert.AreEqual(Vector3.zero, player.transform.position);
        Object.DestroyImmediate(player);
    }
}''')

# 2. Compile
refresh_unity(mode="force", scope="scripts", compile="request", wait_for_ready=True)

# 3. Run
result = run_tests(mode="EditMode", test_names=["PlayerTests.TestPlayerStartsAtOrigin"])
get_test_job(job_id=result["job_id"], wait_timeout=30)
```

---

## Debugging

### Diagnose Compilation Errors

```python
errors = read_console(types=["error"], count=20, include_stacktrace=True, format="detailed")
# Fix scripts...
refresh_unity(mode="force", scope="scripts", compile="request", wait_for_ready=True)
read_console(types=["error"], count=10)
```

### Investigate Missing References

```python
result = find_gameobjects(search_term="Player", search_method="by_name")
# Read: mcpforunity://scene/gameobject/{id}/components
# Check for null fields
target = find_gameobjects(search_term="Target", search_method="by_name")
manage_components(action="set_property", target="Player", component_type="PlayerController",
    property="target", value={"instanceID": target["ids"][0]})
```

### Check Scene State

```python
hierarchy = manage_scene(action="get_hierarchy", page_size=100, include_transform=True)
manage_scene(action="screenshot")
```

---

## Batch Operations

### Mass Property Update

```python
enemies = find_gameobjects(search_term="Enemy", search_method="by_tag")
commands = [{"tool": "manage_components", "params": {
    "action": "set_property", "target": id, "component_type": "EnemyHealth",
    "property": "maxHealth", "value": 100
}} for id in enemies["ids"]]

for i in range(0, len(commands), 25):
    batch_execute(commands=commands[i:i+25], parallel=True)
```

### Cleanup

```python
temps = find_gameobjects(search_term="Temp_", search_method="by_name")
commands = [{"tool": "manage_gameobject", "params": {"action": "delete", "target": id}} for id in temps["ids"]]
batch_execute(commands=commands, fail_fast=False)
```

---

## Error Recovery

### Stale File Recovery

```python
# On stale_file error: re-fetch SHA and retry
new_sha = get_sha(uri=script_uri)
apply_text_edits(uri=script_uri, edits=[...], precondition_sha256=new_sha["sha256"])
```

### Domain Reload Recovery

Wait and retry with exponential backoff. Check `mcpforunity://editor/state` for `ready_for_tools`.

### Compilation Block Recovery

```python
errors = read_console(types=["error"], count=20)
# Fix the script errors...
refresh_unity(mode="force", scope="scripts", compile="request", wait_for_ready=True)
read_console(types=["error"], count=5)  # Verify clean
```
