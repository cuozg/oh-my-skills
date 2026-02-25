---
name: unity-optimize-performance
description: "(opencode-project - Skill) Fix Unity performance issues and optimize runtime efficiency. Use when: (1) Low/inconsistent FPS, (2) High memory usage or leaks, (3) Slow load times, (4) Need to audit assets for performance risks, (5) Reducing build size, (6) Profiling CPU/GPU bottlenecks. Triggers: 'performance', 'FPS drop', 'frame rate', 'lag', 'stutter', 'GC spike', 'garbage collection', 'memory leak', 'profiler', 'CPU bound', 'GPU bound', 'draw calls', 'batching', 'object pooling', 'async loading', 'Addressables', 'load time', 'optimization', 'overdraw', 'fill rate', 'texture memory', 'mesh optimization', 'optimize', 'slow', 'too many draw calls', 'build size', 'reduce memory', 'frame budget', 'spike', 'jank'."
---

# Unity Performance Optimizer

**Input**: Performance complaint or metric target (e.g., "drops to 15 FPS in combat"). Optional: target platform, profiler captures, specific scenes/systems.

## Output

Performance audit report with identified bottlenecks, measurements, and optimized code.

## Workflow

1. **Baseline**: Object counts via hierarchy listing, high-freq logs check
2. **Detect**: `grep` for expensive patterns in scripts (see Red Flags below)
3. **Audit Graphics**: Find high-poly objects, check draw calls
4. **Implement**: Object pooling, cache refs, optimize algorithms, combine materials
5. **Validate**: Play game, check frame timing via worst CPU frames, ensure no visual regressions
6. **Document**: Update docs if architecture changed

## Red Flags to Find

```bash
grep -r "GetComponent" --include="*.cs" | grep "Update"    # GetComponent in Update
grep -r "Camera\.main" --include="*.cs"                     # Camera.main usage
grep -r '"\ \+ ' --include="*.cs"                           # String concat in loops
grep -r "new " --include="*.cs" | grep "Update"             # Allocations in Update
```

## Common Fixes

| Problem | Solution |
|---------|----------|
| GetComponent in Update | Cache in Awake/Start |
| Camera.main in loops | Cache reference |
| String concatenation | StringBuilder |
| Frequent Instantiate | Object pooling |
| Too many draw calls | Combine materials, GPU instancing |
| Large textures | Reduce size, ASTC compression |

## Best Practices

- **Avoid Update**: Use event-based or reactive patterns
- **Cache Everything**: Never lookup in loops
- **Pool Objects**: Projectiles, VFX, UI elements
- **Mobile First**: Optimize for lowest-spec target device
