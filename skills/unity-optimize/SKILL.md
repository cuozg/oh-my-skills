---
name: unity-optimize
description: >
  Optimize Unity project performance — code hot paths, build settings, rendering, memory,
  physics, and platform-specific tuning. Auto-triages: Code (GC elimination, allocation-free
  patterns, Jobs/Burst migration in specific scripts), Settings (Player Settings, Quality
  Settings, Physics Settings, platform config for target hardware), Audit (full project
  performance sweep with ranked findings and applied fixes). MUST use for ANY Unity
  optimization request — "make this faster," "reduce GC," "optimize for mobile," "reduce
  build size," "too many draw calls," "memory issues," "frame drops during gameplay,"
  "performance pass," "optimize my project," "why is my game slow," even when the user
  doesn't say "optimize" explicitly but describes performance symptoms. Do not use for
  profiler data analysis (unity-profiler), code refactoring without perf focus (unity-code),
  or general code writing (unity-code).
metadata:
  author: kuozg
  version: "2.0"
---

# unity-optimize

Analyze performance bottlenecks, apply targeted fixes, verify improvement. Always measure before and after.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| Specific script(s) with perf issues, "optimize this Update," "reduce allocations," "GC spikes in this code" | **Code** |
| Build size, Player Settings, Quality Settings, platform config, "optimize for mobile," "reduce draw calls" | **Settings** |
| "Performance audit," "optimize everything," "full sweep," general "why is my game slow" | **Audit** |

State triage: "This is [mode] — [reason]."

## Step 2 — Execute

### Code Mode

Optimize specific scripts for runtime performance.

1. **Read** — load target file(s); understand current behavior completely before changing anything
2. **Scan** — load `references/code-scan-patterns.md` for systematic pattern detection:
   - GC allocations in Update/FixedUpdate/LateUpdate (LINQ, string concat, lambdas, boxing, `new`)
   - Uncached component lookups (`GetComponent`, `Find`, `FindObjectOfType` per frame)
   - Inefficient data access (wrong collection type, linear search where hash lookup fits)
   - Missing `sealed` on leaf MonoBehaviours (blocks devirtualization)
   - Candidates for Jobs/Burst migration (100+ entity loops on value-type data)
   - Load `review/performance-checklist.md` from unity-standards for comprehensive scan
3. **Rank** — prioritize by estimated frame-time impact: Critical (> frame budget) > Warning (measurable) > Info (minor)
4. **Fix** — apply optimizations using `references/gc-allocation-patterns.md` and `references/allocation-free-cookbook.md`:
   - Cache lookups in `Awake`/`Start` → replace per-frame calls
   - Replace LINQ in hot paths with manual loops (load `code-standards/linq.md`)
   - Eliminate allocations: reuse lists with `.Clear()`, `StringBuilder`, `NonAlloc` physics queries
   - Pool frequently spawned objects (load `code-standards/object-pooling.md`)
   - Add `sealed` to non-inherited MonoBehaviours
   - For 100+ entity loops: propose Jobs/Burst migration (load `optimization/jobs-burst-migration.md`)
5. **Instrument** — add ProfilerMarkers to optimized sections (load `references/profiling-instrumentation.md`)
6. **Verify** — `lsp_diagnostics` on every changed file
7. **Report** — list each change, pattern it fixes, estimated impact using `references/benchmark-template.md`

### Settings Mode

Optimize Unity project settings for target platform.

1. **Gather** — ask for: target platform(s), fps target, current pain points, Unity version
2. **Load targets** — read `references/platform-targets.md` for frame budgets and draw call targets
3. **Load guide** — read relevant platform reference from unity-standards:
   - Mobile: `optimization/mobile-settings.md`
   - Build size: `optimization/build-settings.md`
   - Rendering/Draw calls: `optimization/rendering-settings.md` + `references/draw-call-reduction.md`
   - Memory: `optimization/memory-settings.md`
   - Physics: `optimization/physics-settings.md`
   - Startup: `optimization/startup-settings.md`
   - Assets: `references/asset-optimization.md`
4. **Scan** — examine `ProjectSettings/` files if accessible; otherwise ask user about current settings
5. **Recommend** — generate ranked recommendations: setting name, current value, recommended value, expected impact
6. **Report** — organized by category (rendering, physics, build, memory), priority-ordered

Settings mode provides recommendations and exact paths/values — the user applies them in Unity Editor since ProjectSettings files shouldn't be edited directly.

### Audit Mode

Full project performance sweep.

1. **Scope** — ask for: target platform, fps target, known bottlenecks, project size
2. **Load targets** — read `references/platform-targets.md` for platform-specific budgets
3. **Code scan** — using `references/code-scan-patterns.md`, grep all runtime `.cs` files for hot-path anti-patterns:
   - `GetComponent` / `Find` / `FindObjectOfType` in Update-family methods
   - LINQ operations in Update/FixedUpdate/LateUpdate
   - String concatenation in hot paths
   - Lambda captures in per-frame callbacks
   - `new List` / `new Dictionary` in hot paths
   - Unsealed MonoBehaviours (check for missing `sealed` keyword)
4. **Settings review** — check ProjectSettings/ against platform best practices
5. **Asset review** — using `references/asset-optimization.md`, check for:
   - Oversized textures, uncompressed audio, Read/Write enabled meshes
   - Missing mip maps on 3D textures, over-qualified audio settings
6. **Rank** — classify all findings (Critical/Warning/Info), sort by estimated impact
7. **Report** — generate report using `references/audit-report-template.md`:
   - Summary: overall health, estimated frame budget usage, top 3 issues
   - Findings table: severity, category, file/setting, description, fix
   - Quick wins: changes that can be applied immediately
8. **Fix** — offer to apply code fixes for top findings

## Rules

- **Measure before optimizing** — establish baseline awareness, don't guess at bottlenecks
- **One optimization at a time** — verify each change preserves behavior
- **`lsp_diagnostics`** after every code change
- **Never sacrifice correctness** for performance without explicit user approval
- **Ask target platform** before recommending platform-specific settings
- **Cite references** for each recommendation — link to specific unity-standards file
- **Boundary**: This skill optimizes for performance. For structural cleanup without perf focus, use unity-code Optimize mode. For profiler data analysis, use unity-profiler.

## Escalation

| From | To | When |
|------|----|------|
| Code | Settings | Bottleneck is in Unity settings, not code |
| Code | unity-profiler | User needs profiler data analysis before optimization |
| Settings | Code | Settings are fine but code has hot-path issues |
| Any | unity-code | User wants structural refactoring, not perf optimization |
| Any | Audit | User wants comprehensive sweep instead of targeted fix |

## Standards

Load shared references from unity-standards via `read_skill_file("unity-standards", "references/<path>")`:

**Performance patterns:**
- `review/performance-checklist.md` — hot-path allocation patterns, component lookup costs, physics
- `review/performance-checklist-advanced.md` — Burst compiler, ProfilerMarker, Jobs
- `quality/performance-audit.md` — frame budgets, GC hotspots, draw call/texture budgets
- `code-standards/object-pooling.md` · `object-pooling-advanced.md` — pooling patterns
- `code-standards/collections.md` · `collections-advanced.md` — collection choice, NativeContainers
- `code-standards/linq.md` — LINQ hot-path rules

**Optimization settings:**
- `optimization/build-settings.md` — stripping, IL2CPP, compression, texture/audio/mesh
- `optimization/rendering-settings.md` — SRP Batcher, instancing, batching, shaders, LOD, culling
- `optimization/memory-settings.md` — texture streaming, audio memory, asset lifecycle, Addressables
- `optimization/physics-settings.md` — layer matrix, timestep, collision shapes, queries
- `optimization/mobile-settings.md` — frame rate, thermal throttling, resolution scaling, battery
- `optimization/startup-settings.md` — Enter Play Mode, domain reload, preloading
- `optimization/jobs-burst-migration.md` — Jobs, Burst, data layout, migration checklist

**Skill-specific references** via `read_skill_file("unity-optimize", "references/<path>")`:
- `references/gc-allocation-patterns.md` — GC anti-patterns with allocation-free replacements
- `references/allocation-free-cookbook.md` — ready-to-use zero-alloc code snippets
- `references/code-scan-patterns.md` — grep patterns for finding hot-path issues systematically
- `references/draw-call-reduction.md` — rendering optimization: SRP Batcher, instancing, LOD, culling
- `references/asset-optimization.md` — texture, audio, mesh, shader import optimization
- `references/benchmark-template.md` — before/after measurement report format
- `references/platform-targets.md` — frame budgets, draw call limits, memory budgets per platform
- `references/profiling-instrumentation.md` — ProfilerMarker, ProfilerCounter, GC measurement snippets
- `references/audit-report-template.md` — output template for Audit mode reports
