---
name: unity-investigate
description: "Deep investigation of Unity projects as an expert Unity developer. Covers: logic flow, data structures, serialization, resource management, animation systems, VFX/particles, audio, physics/collision, UI/UX, networking/multiplayer, performance profiling, and all other Unity-related technical aspects. Use when: (1) Understanding how a feature or system works, (2) Tracing execution from trigger to outcome, (3) Analyzing data flow and serialization, (4) Investigating resource/asset management, (5) Examining animation state machines, (6) Debugging VFX or particle setups, (7) Analyzing audio routing, (8) Understanding physics/collision configurations, (9) Reviewing UI/UX implementation patterns, (10) Tracing network request flows, (11) Profiling performance bottlenecks, (12) Extracting business rules and side effects. Triggers: 'how does X work', 'trace the flow', 'explain this code', 'what calls this', 'investigate', 'analyze this system', 'how is X loaded', 'what triggers X', 'where is X serialized'."
---

# Unity Investigator

Deep investigation of Unity projects — logic, data, assets, animation, VFX, audio, physics, UI, networking, performance, and all technical systems.

## Purpose

Deeply analyze how Unity project systems work — trace execution flows, map data pipelines, extract business rules, and document findings so developers understand the codebase.

## Input

- **Required**: Question or system to investigate (e.g., "How does matchmaking work?", "What triggers the daily reward popup?")
- **Optional**: Starting file/class, specific aspect to focus on (data flow, lifecycle, serialization)

## Output

An investigation report saved to `Documents/Investigations/` (per `INVESTIGATION_REPORT.md` template) documenting: system overview, execution flow, data structures, side effects, and key findings.

## Examples

| User Request | Skill Action |
|:---|:---|
| "How does the matchmaking system work?" | Trace from UI button → API call → server response → match start, document full flow |
| "What triggers the daily reward popup?" | Find all callers, trace conditions (login time, cooldown, server flag), map decision tree |
| "Where is player data serialized?" | Map save/load paths, identify serialization format, document schema and migration logic |

## Output Requirement (MANDATORY)

**Every investigation MUST follow the template**: `assets/templates/INVESTIGATION_REPORT.md`

1. Read the template at `.claude/skills/unity-investigate/assets/templates/INVESTIGATION_REPORT.md`
2. Populate ALL applicable sections (delete sections that don't apply)
3. Save output to: `Documents/Investigations/INVESTIGATION_[SubjectName]_[YYYYMMDD].md`

## Investigation Workflow

### Phase 1: Scope Definition
1. Identify the investigation **type** (logic, data, resources, animation, VFX, audio, physics, UI, networking, performance, or general)
2. Define the **primary subject** (class, system, feature, asset)
3. Clarify **entry points** — ask the user if ambiguous
4. Define **boundaries** — what's included vs excluded

### Phase 2: Discovery
1. Run `.claude/skills/unity-investigate/scripts/trace_logic.sh [Target]` to map references
2. Use LSP tools (`lsp_find_references`, `lsp_goto_definition`, `lsp_symbols`) to trace the call graph
3. Use `grep` and `glob` to find related assets, prefabs, ScriptableObjects, and configurations
4. Use `ast_grep_search` for structural code patterns

### Phase 3: Analysis
Apply the analysis rules for the relevant investigation type(s) below. Most investigations span multiple types — analyze all that apply.

### Phase 4: Report Generation
1. Read the `INVESTIGATION_REPORT.md` template
2. Fill the **Investigation Type** field in the header
3. Populate all relevant sections — **delete unused System-Specific sections** (§8.x)
4. Include **Mermaid diagrams** for flows, state machines, and architecture
5. Save to `Documents/Investigations/`

### Phase 5: Summary
Present key findings to the user. Highlight risks, technical debt, and improvement opportunities.

## Analysis Rules by Investigation Type

### Logic Flow
- Trace from **entry points**: `Awake`, `Start`, `OnEnable`, `Update`, `FixedUpdate`, event handlers, UI callbacks, coroutines
- Map the **complete call chain** from trigger to outcome
- Document **conditional branches** and state transitions
- Identify **async operations**: coroutines, `Awaitable`, `UniTask`, callbacks
- Note **execution order** dependencies (Script Execution Order, `[DefaultExecutionOrder]`)

### Data Structures & Serialization
- Identify data models and their **serialization format** (JSON, FlatBuffers, Binary, ScriptableObject)
- Trace data from **source → transformations → destination**
- Check `[Serializable]`, `[SerializeField]`, `[NonSerialized]` attributes
- Analyze **PlayerPrefs**, file I/O, and server data persistence
- Document **schema versioning** and migration strategies

### Resource Management
- Map **asset loading strategies**: Resources.Load, AssetBundle, Addressables
- Analyze **lifecycle**: when loaded, cached, unloaded
- Identify **memory impact** and potential leaks (missing unload, circular refs)
- Document **ScriptableObject** configurations and their consumers
- Check **prefab instantiation** patterns and pooling

### Animation Systems
- Document **Animator Controllers**: states, transitions, parameters, conditions
- Map **state machine flow** with Mermaid `stateDiagram-v2`
- Identify **Animation Events** and their callback methods
- Analyze **Blend Trees** and **IK/Rigging** configurations
- Check **animation clip references** and asset dependencies

### VFX & Particle Systems
- Document **Particle System** hierarchies, emission, lifetime, and rendering
- Identify **custom shaders** and their properties/keywords
- Analyze **Visual Effect Graph** assets if used
- Assess **performance**: particle counts, overdraw, fill rate
- Check **LOD** and distance-based culling

### Audio Systems
- Map **AudioSource** placement and configuration
- Document **AudioMixer** routing and groups
- Trace **sound triggers** — what plays when and why
- Identify **pooling** and **streaming** strategies
- Check spatial audio settings (3D sound, rolloff curves)

### Physics & Collision
- Document **Collider** types, layers, and Layer Collision Matrix
- Analyze **Rigidbody** configurations (mass, drag, constraints, interpolation)
- Trace **OnCollision/OnTrigger** handler chains
- Identify **raycast** usage and optimization (LayerMask, maxDistance)
- Check **FixedUpdate** vs **Update** usage for physics operations

### UI/UX Implementation
- Document **Canvas** setup (render mode, scaler, sorting order)
- Analyze **layout system** (Layout Groups, Content Size Fitters, anchoring)
- Trace **screen navigation** flow and transition systems
- Map **input handling** (touch, click, keyboard, new Input System)
- Check **localization**, **accessibility**, and **responsive scaling**

### Networking & Multiplayer
- Identify **protocol** (HTTP, WebSocket, custom TCP/UDP)
- Document **message format** (JSON, Protobuf, FlatBuffers)
- Trace **request → response** lifecycle including retries and timeouts
- Analyze **state synchronization** mechanisms
- Check **authentication**, **encryption**, and **data validation**

### Performance Profiling
- Identify **hot paths** (per-frame code, tight loops, LINQ in Update)
- Analyze **memory allocation** patterns (GC pressure, boxing, string concat)
- Document **Update/LateUpdate/FixedUpdate** costs
- Check **draw call batching**, **mesh combining**, **texture atlasing**
- Evaluate **object pooling** implementation and coverage

## Best Practices

- **Breadth-First**: Scan file structure and class hierarchy before deep-diving into methods
- **Unity Context**: Factor in engine systems (Physics timing, UI event systems, Animator callbacks)
- **Explain "Why"**: Recover original engineering intent, not just describe what code does
- **Highlight Risks**: Flag technical debt, threading issues, memory leaks, race conditions
- **Use Diagrams**: Mermaid sequence diagrams for flows, state diagrams for state machines, graph diagrams for architecture
- **Cross-Reference**: Connect findings across systems (e.g., animation events triggering audio, UI driving network calls)
- **Quantify Impact**: Estimate memory, CPU, or draw call costs where possible

---

## MCP Tools Integration

Use `unityMCP_*` tools for runtime inspection during investigation.

| Operation | MCP Tool |
|-----------|----------|
| Scene hierarchy | `unityMCP_list_game_objects_in_hierarchy(nameFilter="...")` |
| Object details | `unityMCP_get_game_object_info(gameObjectPath="...")` |
| Component filter | `unityMCP_list_game_objects_in_hierarchy(componentFilter="...")` |
| Console logs | `unityMCP_get_unity_logs()` |
| Editor state | `unityMCP_get_unity_editor_state` |
| Scene screenshot | `unityMCP_capture_scene_object(gameObjectPath="...")` |
| UI screenshot | `unityMCP_capture_ui_canvas()` |
| Play to test | `unityMCP_play_game` / `unityMCP_stop_game` |
| Installed packages | `unityMCP_list_packages` |

### Investigation Discovery Flow

```
1. unityMCP_get_unity_editor_state                           → Project context
2. unityMCP_list_game_objects_in_hierarchy(nameFilter="...")  → Find target objects
3. unityMCP_get_game_object_info(gameObjectPath="...")       → Inspect components/state
4. unityMCP_capture_scene_object(gameObjectPath="...")       → Visual reference
5. [Trace code via LSP tools + grep]
```
