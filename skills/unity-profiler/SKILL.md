---
name: unity-profiler
description: >
  Analyze Unity Profiler data and generate severity-ranked performance reports. Covers CPU frame
  analysis, memory/GC pressure, rendering bottlenecks, and custom profiling instrumentation.
  Use when the user says "analyze the profiler data," "performance report," "why is my game
  lagging," "check for GC spikes," "frame drops," "draw call issues," "memory leak," or has
  completed a profiling session and needs interpretation. Also use when the user wants to add
  custom ProfilerMarkers, measure specific code sections, or instrument their code for profiling.
  Read-only analysis — suggests fixes but does not modify code (except Custom mode which generates
  profiling snippets).
metadata:
  author: kuozg
  version: "2.1"
---

# unity-profiler

Analyze Unity Profiler data, identify performance issues across CPU, memory, and rendering, and generate a ranked findings report with actionable fixes.

## Auto-Triage

Detect the mode from the user's request:

| Signal | Mode | Action |
|--------|------|--------|
| Frame spikes, slow Update, scripting overhead, function timings | **CPU** | Load `references/cpu-mode.md` |
| GC spikes, memory leaks, allocation tracking, heap growth | **Memory** | Load `references/memory-mode.md` |
| Draw calls, overdraw, shader compilation, batching, GPU bound | **Rendering** | Load `references/rendering-mode.md` |
| "Add profiler markers," "instrument this," "measure this code" | **Custom** | Load `references/custom-mode.md` |

If unclear, ask: "Are you investigating CPU/scripting timing, memory/GC pressure, rendering performance, or do you need profiling instrumentation?"

## MCP Profiler Tools

When Unity MCP is available, use these tools to pull live profiler data instead of asking for screenshots. Pick tools based on analysis scope — don't use single-frame tools for multi-frame analysis or vice versa.

**Start broad, then drill down:**

| Step | Goal | Tool |
|------|------|------|
| 1. Overall picture | GC summary across all captured frames | `Unity.Profiler_GetOverallGcAlloca` |
| 2. Find slow range | Time summary across a frame range | `Unity.Profiler_GetFrameRangeTopTimeSummary` (needs `targetFrameTime`) |
| 3. Find GC range | GC allocations across a frame range | `Unity.Profiler_GetFrameRangeGcAll` |
| 4. Worst frame — time | Top samples by total or self time in one frame | `Unity.Profiler_GetFrameTopTimeSam` or `Unity.Profiler_GetFrameSelfTimeSa` |
| 5. Worst frame — GC | GC allocations in one frame | `Unity.Profiler_GetFrameGcAllocati` |
| 6. Drill into sample | Time or GC for a specific sample (by index or marker path) | `Unity.Profiler_GetSampleTimeSummary` / `Unity.Profiler_GetSampleGcAllocat` |
| 7. Cross-thread | Related samples on other threads | `Unity.Profiler_GetRelatedSamplesT` |
| 8. Bottom-up | Bottom-up analysis of a sample | `Unity.Profiler_GetBottomUpSampleT` |

**Tool selection guard clauses:**
- Use `markerIdPath` variants when you know the marker name — more stable than index-based lookups
- Use `FrameRange*` tools for multi-frame analysis — never loop single-frame tools across frames
- Profiler tools are read-only analysis — they identify problems but don't fix them

For the full decision tree with all parameters, load `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")` — see the **Profiling Branch** section.

## Workflow (All Analysis Modes)

1. **Gather data** — if MCP is available, use profiler tools above (start with overall GC summary → narrow to frame range → drill into worst frame). Otherwise, ask user for Profiler screenshots or describe symptoms. Identify target platform and fps target.
2. **Scan codebase** — grep for known anti-patterns in hot paths (mode-specific scan targets in reference files, general patterns in `unity-standards`)
3. **Classify findings** — assign severity using thresholds below
4. **Rank by impact** — sort by frame-time cost or allocation size; group into CPU, Memory, Rendering
5. **Cross-reference** — use `lsp_find_references` and `grep` to trace hotspot call chains to root causes
6. **Generate report** — write report using `references/report-template.md`

## Severity Thresholds

| Level | Frame Time | GC / Memory | Description |
|-------|-----------|-------------|-------------|
| CRITICAL | > budget sustained 5+ frames | > 10 KB/frame alloc or confirmed leak | Blocks release |
| WARNING | 80-100% of budget | 1-10 KB/frame or growing heap trend | Investigate before release |
| INFO | < 80% of budget | Minor inefficiency, stable heap | Acceptable, optimize later |

Frame budget: **60 fps = 16.67ms** (default), **30 fps = 33.33ms** (mobile), **90 fps = 11.11ms** (VR). Determine from user input or project settings. Mobile analysis: apply **0.65x thermal throttling factor** to budget.

## Rules

- **Read-only** — never modify project code or assets (except Custom mode generates snippets)
- Every finding must cite a source: profiler marker, file:line, or tool output
- Max 10 findings per report — prioritize impact over count
- Each finding: one-line summary + source + recommended fix
- Save report to `Documents/Profiler/PERF_{TOPIC}_{YYYYMMDD}.md`

## Output Format

Markdown report at `Documents/Profiler/PERF_{TOPIC}_{YYYYMMDD}.md` — budget status table, ranked findings (max 10), subsystem breakdown, top 3 recommended fixes.

Load template: `read_skill_file("unity-profiler", "references/report-template.md")`

## Reference Files

| File | When to Load |
|------|-------------|
| `references/cpu-mode.md` | CPU frame analysis, scripting bottlenecks, Update overhead |
| `references/memory-mode.md` | GC pressure, heap analysis, memory leak detection |
| `references/rendering-mode.md` | Draw calls, batching, overdraw, shader compilation, GPU profiling |
| `references/custom-mode.md` | ProfilerMarker instrumentation, ProfilerRecorder, measurement snippets |
| `references/report-template.md` | Always — report output template |

Load via `read_skill_file("unity-profiler", "references/<filename>")`.

## Standards

Load `unity-standards` for performance thresholds and anti-pattern checklists:

- `quality/performance-audit.md` — frame budgets, GC hotspots, draw call targets, ProfilerMarker patterns
- `review/checklist.md` — section `## 4. Performance`: hot-path allocations, component lookup, physics, Burst/Jobs
- `other/unity-mcp-routing-matrix.md` — full MCP profiler tool decision tree with parameters, guard clauses, and 12 profiler tools

Load via `read_skill_file("unity-standards", "references/<path>")`.
