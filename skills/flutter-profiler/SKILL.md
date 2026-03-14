---
name: flutter-profiler
description: >
  Analyze Flutter performance data and generate severity-ranked reports. Covers CPU frame analysis,
  memory/GC pressure, frame rendering and jank, and custom profiling snippets. Use when the user says
  "analyze profiler data," "performance report," "why is my app slow," "check for jank," "memory leak,"
  "GC spikes," "frame drops," or has completed a DevTools profiling session and needs interpretation.
  Also use when the user wants to add custom performance markers, timeline events, or profiling
  instrumentation to their Flutter code. Read-only analysis — suggests fixes but does not modify code.
metadata:
  author: kuozg
  version: "1.0"
---

# flutter-profiler

Analyze Flutter DevTools performance data, identify bottlenecks across CPU, memory, and rendering, and generate a ranked findings report with actionable fixes.

## Auto-Triage

Detect the mode from the user's request:

| Signal | Mode | Action |
|--------|------|--------|
| Slow frames, CPU timeline, function timings | **CPU** | Load `references/cpu-mode.md` |
| GC spikes, memory leaks, heap growth | **Memory** | Load `references/memory-mode.md` |
| Jank, frame drops, GPU bottleneck, shader compilation | **Frame** | Load `references/frame-mode.md` |
| "Add profiling," "custom markers," "instrument this" | **Custom** | Load `references/custom-mode.md` |

If unclear, ask: "Are you investigating CPU timing, memory usage, frame rendering, or do you need profiling instrumentation?"

## Workflow (All Analysis Modes)

1. **Gather data** — ask user for DevTools screenshots, timeline exports, or profiler output; scan codebase for known anti-patterns
2. **Scan codebase** — grep for hot-path issues: `setState` in loops, missing `const`, `MediaQuery.of` in deep widgets, full-list builds, unclosed streams
3. **Classify findings** — assign severity using thresholds below
4. **Rank by impact** — sort by frame-time or allocation cost; group into CPU, Memory, Rendering
5. **Cross-reference** — trace hotspot call chains via `grep` and `lsp_find_references`
6. **Generate report** — write report using `references/report-template.md`

## Severity Thresholds

| Level | Frame Time | GC / Memory | Description |
|-------|-----------|-------------|-------------|
| CRITICAL | > budget sustained 5+ frames | > 10 MB retained or leak confirmed | Blocks release |
| WARNING | 80-100% of budget | Growing heap trend or > 1 MB/s alloc | Investigate |
| INFO | < 80% of budget | Stable, minor inefficiency | Acceptable |

Frame budget: **60 fps = 16.67ms** (default), **120 fps = 8.33ms** (high-refresh). Determine from user input or device target.

## Rules

- **Read-only** — never modify project code (except Custom mode which generates snippets)
- Every finding must cite a source: DevTools marker, file:line, profiler output, or tool evidence
- Max 10 findings per report — prioritize impact over count
- Each finding: one-line summary + source + recommended fix
- Mobile analysis: apply **0.7x thermal throttling factor** to frame budget
- Profile in **profile mode** (`flutter run --profile`), never debug mode — debug overhead skews all timings
- Save report to `Documents/Profiler/PERF_{TOPIC}_{YYYYMMDD}.md`

## Output Format

Markdown report at `Documents/Profiler/PERF_{TOPIC}_{YYYYMMDD}.md` — budget status table, ranked findings (max 10), subsystem breakdown, top 3 recommended fixes.

Load template: `read_skill_file("flutter-profiler", "references/report-template.md")`

## Reference Files

| File | When to Load |
|------|-------------|
| `references/cpu-mode.md` | CPU frame analysis, slow function identification |
| `references/memory-mode.md` | GC pressure, heap analysis, leak detection |
| `references/frame-mode.md` | Jank, frame drops, GPU vs CPU, shader compilation |
| `references/custom-mode.md` | Custom markers, Timeline API, instrumentation snippets |
| `references/report-template.md` | Always — report output template |

Load via `read_skill_file("flutter-profiler", "references/<filename>")`.

## Standards

Load `flutter-standards` for performance baselines and anti-pattern lists:

- `performance-optimization.md` — Frame budgets, rebuild profiling, RepaintBoundary, image optimization
- `debug-logging.md` — DevTools tabs, debug flags, structured logging
- `async-streams.md` — Stream/Future performance, cancellation patterns

Load via `read_skill_file("flutter-standards", "references/<filename>")`.
