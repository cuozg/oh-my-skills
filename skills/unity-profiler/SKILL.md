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
  version: "2.0"
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

## Workflow (All Analysis Modes)

1. **Gather data** — ask user for Profiler screenshots, profiler captures, or describe the symptoms; identify target platform and fps target
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
- `review/performance-checklist.md` — hot-path allocation patterns, component lookup costs, physics checks
- `review/performance-checklist-advanced.md` — Burst compiler, ProfilerMarker best practices, Jobs system

Load via `read_skill_file("unity-standards", "references/<path>")`.
