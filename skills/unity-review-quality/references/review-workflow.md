# Review Workflow Details

## Step 2: Architecture Scan (parallel explore agents)

Spawn 3-5 explore agents in parallel:

| Agent | Focus |
|:------|:------|
| Architecture patterns | Find Singleton patterns, Manager classes, DI, service locators, event systems, SO channels. Map class hierarchy depth. |
| Assembly structure | Read all .asmdef files. Map assembly graph. Find circular references, missing refs, overly broad assemblies. |
| Cross-cutting concerns | Find logging patterns, error handling, analytics/telemetry, configuration management. |
| Coupling analysis | Find tight coupling: direct component refs vs interfaces, concrete vs abstract deps, static access. |
| Data flow | Trace data persistence: save/load, serialization format, PlayerPrefs, SO data containers. |

## Step 3: Code Quality Deep-Dive (parallel explore agents)

Spawn 3-5 explore agents in parallel:

| Agent | Focus |
|:------|:------|
| Hot path analysis | Find all Update/FixedUpdate/LateUpdate. Check for allocations, GetComponent, Find, LINQ, string ops. |
| Lifecycle audit | Find all MonoBehaviours. Check Awake/Start/OnEnable/OnDisable/OnDestroy balance. Check coroutine lifecycle. |
| Memory patterns | Find event subscriptions (+= without -=), Addressable loads without Release, UnityWebRequest without Dispose, static collections. |
| Async patterns | Find all async methods, coroutines, UniTask. Check cancellation tokens, error handling, fire-and-forget. |
| Anti-pattern scan | Find God classes (>500 lines), deep nesting (>4), magic numbers, copy-paste duplication, empty catch blocks. |

## Step 4: Unity-Specific Review (parallel explore agents)

Spawn 2-4 explore agents in parallel:

| Agent | Focus |
|:------|:------|
| Serialization safety | Find [SerializeField], [Serializable], [SerializeReference]. Check FormerlySerializedAs, SO mutation, interface serialization. |
| Asset management | Check texture import settings (max size, compression), audio import (load type), mesh import (read/write). |
| Scene/Prefab health | Sample 3-5 scenes and 5-10 prefabs. Check missing scripts, Canvas setup, nested layouts, raycast targets. |
| Physics & rendering | Check layer setup, collision matrix, Rigidbody configs, shader complexity, draw calls, batching. |

## Step 5: Project Health Check

Direct tool reads (no agents needed):
- `ProjectSettings/ProjectSettings.asset` — scripting backend, API compat, stripping level
- `ProjectSettings/QualitySettings.asset` — quality levels, shadows, vsync, LOD bias
- `ProjectSettings/TagManager.asset` — layer/tag organization
- `ProjectSettings/Physics2DSettings.asset` or `DynamicsManager.asset` — physics config
- `ProjectSettings/EditorBuildSettings.asset` — scene list
- Check `.gitignore` covers Library/, Temp/, Logs/, UserSettings/
- Check for `.editorconfig` or code style configuration
