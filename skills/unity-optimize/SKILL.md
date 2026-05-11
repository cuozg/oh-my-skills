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
  version: "2.1"
---

# unity-optimize

Analyze performance bottlenecks, apply targeted fixes, verify improvement. Always measure before and after.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| Specific script(s), "optimize this Update," "reduce GC in this code" | **Code** |
| Build size, Player/Quality Settings, platform config, "optimize for mobile" | **Settings** |
| "Performance audit," "full sweep," general "why is my game slow" | **Audit** |

State triage: "This is [mode] — [reason]."

## Step 2 — Execute

### Code Mode
1. **Read** target files fully before changing anything
2. **Scan** `references/code-scan-patterns.md` + `unity-standards/review/performance-checklist.md`:
   - GC in Update (LINQ, string concat, lambdas, boxing, `new`)
   - Per-frame `GetComponent`/`Find`/`FindObjectOfType`
   - Wrong collection type, linear search in hot path
   - Missing `sealed` on leaf MonoBehaviours
3. **Rank** by frame-time impact: Critical → Warning → Info
4. **Fix** using `references/gc-allocation-patterns.md` + `references/allocation-free-cookbook.md`:
   - Cache in `Awake`/`Start` · Replace LINQ with loops · Use `NonAlloc` physics · Pool objects
5. **Instrument** `ProfilerMarkers` via `references/profiling-instrumentation.md`
6. **Verify** `lsp_diagnostics` on every changed file
7. **Report** each change, pattern fixed, estimated impact

### Settings Mode
1. Ask: target platform(s), fps target, current pain points, Unity version
2. Load relevant guide from unity-standards `optimization/<topic>.md`
3. Examine `ProjectSettings/` if accessible; else ask user about current settings
4. Output ranked recommendations: setting name · current value · recommended value · expected impact

Settings mode provides recommendations only — user applies in Unity Editor.

### Audit Mode
1. Scope: target platform, fps target, known bottlenecks, project size
2. Grep all runtime `.cs` for hot-path anti-patterns (see `references/code-scan-patterns.md`)
3. Check `ProjectSettings/` against platform best practices
4. Review assets via `references/asset-optimization.md`
5. Rank findings (Critical/Warning/Info) by estimated impact
6. Generate report via `references/audit-report-template.md`
7. Offer to apply code fixes for top findings

## Rules

- Measure before optimizing — establish baseline, don't guess
- `lsp_diagnostics` after every code change
- Never sacrifice correctness without explicit user approval
- Ask target platform before recommending platform-specific settings
- For structural cleanup without perf focus → `unity-code` · For profiler analysis → `unity-profiler`

## MCP Profiler Tools

| Purpose | Tool |
|---------|------|
| Baseline GC (all frames) | `Unity.Profiler_GetOverallGcAlloca` |
| Baseline frame time | `Unity.Profiler_GetFrameRangeTopTimeSummary` |
| Verify GC reduction | `Unity.Profiler_GetFrameGcAllocati` |
| Verify time improvement | `Unity.Profiler_GetFrameTopTimeSam` |

Full tool decision tree: `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")` → Profiling Branch.

## Standards

Via `read_skill_file("unity-standards", "references/<path>")`:
- `review/checklist.md` §4 · `quality/performance-audit.md` · `code-standards/performance-data.md`
- `optimization/build-settings.md` · `optimization/rendering-settings.md` · `optimization/memory-settings.md`
- `optimization/physics-settings.md` · `optimization/mobile-settings.md` · `optimization/jobs-burst-migration.md`

Via `read_skill_file("unity-optimize", "references/<path>")`:
- `gc-allocation-patterns.md` · `allocation-free-cookbook.md` · `code-scan-patterns.md`
- `draw-call-reduction.md` · `asset-optimization.md` · `platform-targets.md`
- `profiling-instrumentation.md` · `benchmark-template.md` · `audit-report-template.md`
