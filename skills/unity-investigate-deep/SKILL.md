---
name: unity-investigate-deep
description: "Deep investigation of Unity projects with full report output. Produces comprehensive markdown investigation documents with architecture diagrams, execution flows, risk tables, and improvement recommendations. Use when: (1) Need a thorough written report of how a system works, (2) Documenting complex system behavior for team review, (3) Deep-diving into architecture with Mermaid diagrams, (4) Producing investigation artifacts for future reference, (5) Tracing complete execution flows with side effects, (6) Auditing system health with risk assessment. Triggers: 'deep investigate', 'investigation report', 'document how X works', 'full analysis', 'write investigation', 'deep dive report', 'system analysis report', 'trace and document'."
---

# Unity Deep Investigator

**Input**: Question or system to investigate + optional starting file/class

## Output

Comprehensive investigation report (markdown) with architecture diagrams, execution flows, and risk tables. Save to `Documents/Investigations/`.

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
