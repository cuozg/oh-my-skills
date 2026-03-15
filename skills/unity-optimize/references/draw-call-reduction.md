# Draw Call & Rendering Optimization

## Draw Call Reduction Strategy (Priority Order)

### 1. Enable SRP Batcher (URP/HDRP)

Biggest single win for CPU draw call overhead.

**Requirements:**
- URP or HDRP rendering pipeline
- Shaders declare `CBUFFER_START(UnityPerMaterial)` for all properties
- Verify in Frame Debugger: look for "SRP Batch" entries

**Common breakers:**
- Custom shaders without CBUFFER declaration
- MaterialPropertyBlock usage (breaks SRP batching)
- Mixed shader variants on same pass

### 2. Reduce Material Count

Each unique material = potential draw call break.

**Techniques:**
- Texture atlasing: combine multiple textures into atlas
- Material sharing: same material on multiple objects
- Uber-shaders: one shader with keyword toggles (vs many specialized shaders)
- Color/property via vertex color or UV2 (avoids material variants)

### 3. GPU Instancing for Repeated Objects

```
Best for: trees, grass, rocks, props, particles
Setup: Material Inspector → Enable GPU Instancing
Requirement: Same mesh + same material instance
```

**Limitations:**
- Doesn't work with SkinnedMeshRenderer
- MaterialPropertyBlock can break instancing in some cases
- Use `Graphics.DrawMeshInstanced` for manual control (1000+ objects)

### 4. Static Batching

For immovable environment geometry.

```
Setup: Inspector → Static checkbox → Batching Static
Tradeoff: Increased memory (vertices duplicated) vs zero CPU overhead
Best for: buildings, terrain props, fences, decorations
```

### 5. LOD Groups

```
LOD0: Full detail (> 50% screen)
LOD1: 50% triangles (25-50% screen)
LOD2: 25% triangles (10-25% screen)
Cull: Hidden (< 5-10% screen)
```

Mobile LOD Bias: 0.5-0.7 (more aggressive switching).

### 6. Occlusion Culling

```
Best for: indoor scenes, dense urban, many walls
Setup: Mark occluders (walls, floors) + occludees → Bake
Not useful: open landscapes, simple scenes (< 100 objects)
```

### 7. Camera Culling

```csharp
// Reduce far clip plane to actual needed distance
camera.farClipPlane = 200f; // not default 1000

// Per-layer culling distances
float[] distances = new float[32];
distances[LayerMask.NameToLayer("SmallProps")] = 50f;
distances[LayerMask.NameToLayer("VFX")] = 100f;
camera.layerCullDistances = distances;
```

## Particle System Optimization

- [ ] Max Particles: set realistic limit (not default 1000)
- [ ] Simulation Space: Local when possible (cheaper than World)
- [ ] Collision: reduce quality, use simplified collision module
- [ ] Renderer: GPU instancing for particle meshes
- [ ] Disable sub-emitters when not visible

## UI-Specific Rendering

- [ ] Split static and dynamic UI into separate Canvases
- [ ] Disable Raycast Target on non-interactive elements
- [ ] Reduce Canvas rebuilds: batch text changes, avoid layout recalculation
- [ ] Atlas UI sprites into shared sprite atlas
