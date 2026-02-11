---
description: Find and fix Unity performance bottlenecks (FPS, memory, load times)
agent: build
---

Load the `unity/unity-optimize-performance` skill and optimize the specified area.

## Task

$ARGUMENTS

## Optimization Areas

1. **CPU** - Reduce frame time, optimize Update/FixedUpdate, cache expensive operations
2. **Memory** - Fix leaks, reduce GC allocations, pool objects, optimize textures
3. **Loading** - Reduce scene/asset load times, implement async loading
4. **Rendering** - Reduce draw calls, optimize shaders, LOD, occlusion culling
5. **Mobile** - Battery, thermal, memory budget considerations

## Workflow

1. **Profile** - Identify the worst offenders using profiling data
2. **Analyze** - Understand why each bottleneck occurs
3. **Fix** - Apply targeted optimizations with measurable impact
4. **Verify** - Ensure fixes don't break functionality, check with `lsp_diagnostics`
