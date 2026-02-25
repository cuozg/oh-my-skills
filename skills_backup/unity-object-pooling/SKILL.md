---
name: unity-object-pooling
description: "(opencode-project - Skill) Object pooling patterns for Unity. Covers generic ObjectPool, Unity's built-in ObjectPool API, particle system pooling, UI element pooling, projectile pools, and pool warming strategies. Use when: (1) Reducing GC allocations from frequent Instantiate/Destroy, (2) Building bullet/projectile systems, (3) Pooling UI elements for lists, (4) Managing particle system lifecycles, (5) Optimizing spawn-heavy gameplay. Triggers: 'object pool', 'pooling', 'reduce GC', 'spawn optimization', 'bullet pool', 'projectile pool', 'pool manager'."
---

# unity-object-pooling — Object Pooling Patterns

**Input**: Objects to pool (prefab type, spawn frequency, lifetime pattern), pool size constraints, warming needs

## Output

Production-ready C# object pooling code following the patterns above.

## Workflow

1. **Identify pool candidates** — Find objects with frequent Instantiate/Destroy (Profiler GC.Alloc markers)
2. **Choose implementation** — Unity `ObjectPool<T>` for simple cases, custom pool for complex lifecycle
3. **Implement IPoolable** — Define OnSpawn/OnDespawn contracts for clean reset
4. **Build pool manager** — Centralized registry with configurable initial size, max capacity, auto-expand
5. **Add warming** — Pre-instantiate during loading screens to avoid runtime hitches
6. **Profile to verify** — Compare GC allocations before/after via Unity Profiler

## Pool Implementation Selection

| Approach | Best For | Complexity |
|:---------|:---------|:-----------|
| `UnityEngine.Pool.ObjectPool<T>` | Single-type pooling, quick setup | Low |
| `UnityEngine.Pool.CollectionPool<T,V>` | Pooling Lists, HashSets, Dictionaries | Low |
| Custom `MonoBehaviourPool<T>` | GameObject pooling with lifecycle hooks | Medium |
| Multi-type `PoolManager` | Many prefab types, centralized management | High |

## Key Patterns

Refer to [code-examples.md](references/code-examples.md) for:
 Unity Built-in ObjectPool (Simplest)
 IPoolable Interface + Projectile
 Pool Warming (Async)
 Collection Pooling

## Best Practices

### Do
- Use Unity's built-in `ObjectPool<T>` — covers most cases
- Reset ALL state in OnDespawn (trails, particles, timers, subscriptions)
- Warm pools during loading, not gameplay
- Set reasonable max sizes to prevent unbounded growth
- Use `collectionCheck: false` in production (overhead)
- Profile before and after with Unity Profiler GC.Alloc

### Do Not
- Pool rarely-instantiated objects — complexity not worth it
- Forget to return objects (use auto-return timers as safety nets)
- Access pooled objects after Release() — treat as Destroy()
- Pool objects with unique persistent state across lifetimes
- Over-allocate initial sizes — profile actual usage first

## When to Pool

| Scenario | Pool? | Reason |
|:---------|:------|:-------|
| Bullets fired 60/sec | Yes | High-freq Instantiate/Destroy = GC spikes |
| Enemies every 5 sec | Maybe | Only if GC measurable in Profiler |
| Player character (1) | No | Single instance, never recycled |
| Particle effects on hit | Yes | Frequent spawn/despawn, recyclable |
| Audio sources for SFX | Yes | Many short-lived sources |

## Handoff & Boundaries

- **Delegates to**: `unity-optimize-performance` (profiling, memory analysis), `unity-code-deep` (general C# beyond pooling)
- **Does NOT handle**: Memory layout/cache-line optimization, ECS/DOTS pooling, Asset Bundle memory management
