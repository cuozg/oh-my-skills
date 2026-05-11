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

Analyze Unity Profiler data, identify performance issues, generate severity-ranked report.

## Auto-Triage

| Signal | Mode | Load |
|--------|------|------|
| Frame spikes, slow Update, scripting overhead | **CPU** | `references/cpu-mode.md` |
| GC spikes, memory leaks, heap growth | **Memory** | `references/memory-mode.md` |
| Draw calls, overdraw, batching, GPU bound | **Rendering** | `references/rendering-mode.md` |
| "Add profiler markers," "instrument this" | **Custom** | `references/custom-mode.md` |

If unclear, ask: "CPU/scripting timing, memory/GC, rendering, or profiling instrumentation?"

## MCP Profiler Tools (Broad → Narrow → Drill)

| Step | Tool |
|------|------|
| Overall GC summary | `Unity.Profiler_GetOverallGcAlloca` |
| Slow frame range | `Unity.Profiler_GetFrameRangeTopTimeSummary` |
| GC frame range | `Unity.Profiler_GetFrameRangeGcAll` |
| Worst frame time | `Unity.Profiler_GetFrameTopTimeSam` |
| Worst frame GC | `Unity.Profiler_GetFrameGcAllocati` |
| Drill sample | `Unity.Profiler_GetSampleTimeSummary` / `Unity.Profiler_GetSampleGcAllocat` |
| Cross-thread | `Unity.Profiler_GetRelatedSamplesT` |
| Bottom-up | `Unity.Profiler_GetBottomUpSampleT` |

Use `markerIdPath` when marker name is known. Use `FrameRange*` for multi-frame (never loop single-frame tools).
Full decision tree: `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")` → Profiling Branch.

## Workflow

1. **Gather** — MCP profiler tools (broad→drill) or ask for Profiler screenshots. Identify platform + fps target.
2. **Scan** — grep for anti-patterns in hot paths (see mode reference file)
3. **Classify** — severity per thresholds below
4. **Rank** — by frame-time cost or allocation size; group CPU/Memory/Rendering
5. **Cross-reference** — trace hotspot call chains via `lsp_find_references` + grep
6. **Report** — use `references/report-template.md`, save to `Documents/Profiler/PERF_{TOPIC}_{YYYYMMDD}.md`

## Severity Thresholds

| Level | Frame Time | GC/Memory |
|-------|-----------|-----------|
| CRITICAL | >budget sustained 5+ frames | >10 KB/frame or confirmed leak |
| WARNING | 80–100% of budget | 1–10 KB/frame or growing heap |
| INFO | <80% of budget | Minor, stable heap |

Budget: **60 fps = 16.67ms** · **30 fps = 33.33ms** · **90 fps = 11.11ms**. Mobile: ×0.65 thermal throttling factor.

## Rules

- **Read-only** — never modify code/assets (Custom mode generates snippets only)
- Every finding must cite: profiler marker, file:line, or tool output
- Max 10 findings per report — prioritize impact
- Each finding: 1-line summary + source + recommended fix

## References

`read_skill_file("unity-profiler", "references/<file>")`:
- `cpu-mode.md` · `memory-mode.md` · `rendering-mode.md` · `custom-mode.md` · `report-template.md`

`read_skill_file("unity-standards", "references/<path>")`:
- `quality/performance-audit.md` · `review/checklist.md` §4 · `other/unity-mcp-routing-matrix.md`
