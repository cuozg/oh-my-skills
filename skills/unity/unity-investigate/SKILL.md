---
name: unity-investigate
description: "Deep investigation of Unity projects as an expert Unity developer. Covers: logic flow, data structures, serialization, resource management, animation systems, VFX/particles, audio, physics/collision, UI/UX, networking/multiplayer, performance profiling, and all other Unity-related technical aspects. Use when: (1) Understanding how a feature or system works, (2) Tracing execution from trigger to outcome, (3) Analyzing data flow and serialization, (4) Investigating resource/asset management, (5) Examining animation state machines, (6) Debugging VFX or particle setups, (7) Analyzing audio routing, (8) Understanding physics/collision configurations, (9) Reviewing UI/UX implementation patterns, (10) Tracing network request flows, (11) Profiling performance bottlenecks, (12) Extracting business rules and side effects. Triggers: 'how does X work', 'trace the flow', 'explain this code', 'what calls this', 'investigate', 'analyze this system', 'how is X loaded', 'what triggers X', 'where is X serialized'."
---

# Unity Investigator

**Input**: Question or system to investigate + optional starting file/class
**Output**: Report at `Documents/Investigations/INVESTIGATION_[SubjectName]_[YYYYMMDD].md` per `assets/templates/INVESTIGATION_REPORT.md`

## Workflow

1. **Scope** — identify investigation type (logic/data/resources/animation/VFX/audio/physics/UI/networking/performance), primary subject, entry points, boundaries
2. **Discover** — run `scripts/trace_logic.sh [Target]`, use LSP tools (`lsp_find_references`, `lsp_goto_definition`, `lsp_symbols`), grep/glob for assets, `ast_grep_search` for patterns
3. **Analyze** — apply analysis rules for relevant type(s) below
4. **Report** — read INVESTIGATION_REPORT.md template, fill type field, populate sections, delete unused §8.x sections, include Mermaid diagrams, save
5. **Summary** — present key findings, highlight risks/debt/improvements

## Analysis Rules by Type

### Logic Flow
- Trace from entry points: `Awake`, `Start`, `OnEnable`, `Update`, event handlers, coroutines
- Map complete call chain trigger→outcome, conditional branches, state transitions
- Identify async operations (coroutines, `Awaitable`, `UniTask`), execution order dependencies

### Data Structures & Serialization
- Map serialization format (JSON, FlatBuffers, Binary, ScriptableObject)
- Trace data source→transformations→destination
- Check `[Serializable]`, `[SerializeField]`, PlayerPrefs, schema versioning

### Resource Management
- Map loading strategies (Resources.Load, AssetBundle, Addressables), lifecycle, memory impact
- Document ScriptableObject configs, prefab instantiation, pooling

### Animation Systems
- Document Animator Controllers (states, transitions, parameters), Animation Events, Blend Trees
- Map state machine flow with Mermaid `stateDiagram-v2`

### VFX & Particle Systems
- Document hierarchies, emission, custom shaders, VFX Graph
- Assess performance: particle counts, overdraw, LOD culling

### Audio Systems
- Map AudioSource placement, AudioMixer routing, sound triggers, pooling/streaming

### Physics & Collision
- Document Collider types/layers, Rigidbody configs, OnCollision/OnTrigger handlers
- Identify raycast usage, FixedUpdate vs Update for physics

### UI/UX Implementation
- Document Canvas setup, layout system, screen navigation, input handling
- Check localization, accessibility, responsive scaling

### Networking & Multiplayer
- Identify protocol, message format, request→response lifecycle, state sync
- Check auth, encryption, data validation

### Performance Profiling
- Identify hot paths, memory allocation patterns, Update costs
- Check draw call batching, object pooling coverage

## Best Practices

- **Breadth-First**: Scan structure before deep-diving methods
- **Explain "Why"**: Recover engineering intent, not just describe code
- **Highlight Risks**: Flag debt, threading issues, memory leaks, race conditions
- **Use Diagrams**: Mermaid sequence/state/graph diagrams
- **Quantify Impact**: Estimate memory, CPU, draw call costs
