# Analysis Rules by Type

## Logic Flow
 Trace from entry points: `Awake`, `Start`, `OnEnable`, `Update`, event handlers, coroutines
 Map complete call chain trigger→outcome, conditional branches, state transitions
 Identify async operations (coroutines, `Awaitable`, `UniTask`), execution order dependencies

## Data Structures & Serialization
 Map serialization format (JSON, FlatBuffers, Binary, ScriptableObject)
 Trace data source→transformations→destination
 Check `[Serializable]`, `[SerializeField]`, PlayerPrefs, schema versioning

## Resource Management
 Map loading strategies (Resources.Load, AssetBundle, Addressables), lifecycle, memory impact
 Document ScriptableObject configs, prefab instantiation, pooling

## Animation Systems
 Document Animator Controllers (states, transitions, parameters), Animation Events, Blend Trees
 Map state machine flow with Mermaid `stateDiagram-v2`

## VFX & Particle Systems
 Document hierarchies, emission, custom shaders, VFX Graph
 Assess performance: particle counts, overdraw, LOD culling

## Audio Systems
 Map AudioSource placement, AudioMixer routing, sound triggers, pooling/streaming

## Physics & Collision
 Document Collider types/layers, Rigidbody configs, OnCollision/OnTrigger handlers
 Identify raycast usage, FixedUpdate vs Update for physics

## UI/UX Implementation
 Document Canvas setup, layout system, screen navigation, input handling
 Check localization, accessibility, responsive scaling

## Networking & Multiplayer
 Identify protocol, message format, request→response lifecycle, state sync
 Check auth, encryption, data validation

## Performance Profiling
 Identify hot paths, memory allocation patterns, Update costs
 Check draw call batching, object pooling coverage