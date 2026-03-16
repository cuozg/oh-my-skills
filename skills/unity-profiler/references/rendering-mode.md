# Rendering Mode — Draw Calls, Batching & GPU Analysis

Analyze rendering performance: draw calls, batching efficiency, overdraw, shader compilation, and GPU bottlenecks.

## Unity Profiler Rendering Analysis

1. Open **Profiler** → **Rendering** module for draw call counts and batch stats
2. Use **Frame Debugger** (Window → Analysis → Frame Debugger) to see each draw call
3. Check **GPU Profiler** module for GPU-side timings (requires development build)
4. Look at **Statistics** window in Game view for real-time triangle/vertex counts

## Draw Call & Batch Budgets

| Platform | Max Draw Calls | Max Batches | Max Triangles |
|----------|---------------|-------------|---------------|
| Mobile (low) | 100-200 | 50-100 | 100K-300K |
| Mobile (high) | 200-500 | 100-200 | 500K-1M |
| Console | 2000-3000 | 500-1000 | 2M-5M |
| PC | 2000-5000 | 500-2000 | 5M-10M |
| VR (per eye) | 100-150 | 50-75 | 500K-1M |

## Batching Analysis

Unity batches draw calls to reduce CPU-GPU communication. Check which batching methods are active:

| Batching Type | How It Works | When It Breaks |
|---------------|-------------|----------------|
| **SRP Batcher** | Batches by shader variant, not material | Incompatible shader, non-SRP pipeline |
| **Static Batching** | Combines static meshes at build time | Too many unique meshes, memory cost |
| **Dynamic Batching** | Combines small meshes at runtime | > 300 vertices, different materials/scales |
| **GPU Instancing** | Single draw call for identical meshes | Different material properties, non-instanced shader |

### Frame Debugger Workflow

1. Open Frame Debugger and click **Enable**
2. Step through draw calls — look for:
   - Many calls with same material that aren't batched (batching break)
   - Redundant state changes between draws
   - Unexpected full-screen passes (post-processing, shadows)
3. Check **"Why this draw call can't be batched"** message in details panel

## Common Rendering Anti-Patterns

| Pattern | Impact | Fix |
|---------|--------|-----|
| `Renderer.material` access | Creates material instance, breaks batching | Use `sharedMaterial` for reads, `MaterialPropertyBlock` for per-instance data |
| Runtime material creation | Each instance = separate draw call | Share materials, use GPU instancing |
| Unoptimized shadow casters | Extra pass per shadow-casting light | Reduce shadow distance, use shadow cascades, LOD groups |
| Overdraw from transparent objects | Fragments drawn multiple times | Reduce transparent layers, use cutout when possible |
| UI Canvas rebuilds | Mesh regeneration per change | Split static/dynamic into separate canvases |
| Full-screen post-processing on mobile | Fills entire screen per effect | Reduce effect count, lower resolution, use optimized variants |
| Missing LOD groups | Full detail at distance | Add LOD groups, use imposters for distant objects |
| Uncompressed textures | VRAM bloat, slower sampling | ASTC (mobile), BC7/DXT5 (PC), enable mipmaps for 3D |

## Codebase Scan Targets

Grep for rendering issues:

```
.material              — runtime material access (creates instance)
.material =            — assigning material at runtime
.materials             — accessing material array (allocates)
new Material(          — runtime material creation
Shader.Find(           — runtime shader lookup
Graphics.Blit(         — full-screen blit operations
RenderTexture.GetTemporary  — check for matching Release
SetPass(               — manual rendering passes
Camera.Render()        — manual camera render calls
```

## GPU Profiling

### Development Build GPU Markers

In development builds, the GPU Profiler module shows:
- **Opaque**: geometry rendering time
- **Transparent**: alpha-blended objects
- **Shadows**: shadow map rendering
- **Post-processing**: screen-space effects

### GPU Bound vs CPU Bound

| Symptom | Bottleneck | Action |
|---------|-----------|--------|
| GPU module shows time > budget, CPU is fine | GPU bound | Reduce triangles, overdraw, shader complexity |
| CPU rendering markers high, GPU is fine | CPU bound | Reduce draw calls via batching, culling |
| Both high | Combined | Fix the larger bottleneck first |
| Main thread waiting on render thread | CPU-side render bottleneck | Reduce draw call submission count |

## Shader Compilation

Shader variants compile on first use, causing frame spikes:
- **Shader Variant Collection**: pre-warm shaders at loading screen
- **ShaderVariantCollection.WarmUp()**: call during scene load
- Check **Shader Compilation** profiler marker for runtime compilation spikes
- Strip unused shader variants in **Graphics Settings → Shader Stripping**
