---
name: unity-profiler
description: Analyze Unity Profiler data — identify CPU spikes, GC pressure, rendering bottlenecks, and generate a short highlight report with severity-ranked findings and actionable fixes. Triggers — 'profiler report', 'performance analysis', 'profiler review', 'analyze profiler', 'performance report'.
---
# unity-profiler

Analyze Unity Profiler data read-only, identify performance issues across CPU, memory, and rendering, and generate a short highlight report with ranked findings.

## When to Use

- After a profiling session to interpret captured data
- Performance regression investigation
- Pre-release performance gate check
- Recurring frame spikes or GC hitches need root-cause analysis

## Workflow

1. **Collect data** — call `get_worst_cpu_frames` and `get_worst_gc_frames` to pull profiler snapshots
2. **Scan codebase** — grep for known anti-patterns: per-frame allocations, `FindObjectOfType`, `Camera.main`, LINQ in Update, string concat in hot paths
3. **Classify findings** — assign severity using frame budget and thresholds from `unity-standards/references/quality/performance-audit.md`
4. **Rank by impact** — sort findings by frame-time percentage; group into CPU, Memory, Rendering
5. **Cross-reference** — use `lsp_find_references` and `grep` to trace hotspot call chains back to root causes
6. **Generate report** — write highlight report using `references/report-template.md`

## Rules

- Read-only — never modify project code or assets
- Determine target fps from project settings or user input; default 60 fps (16.67 ms budget)
- Every finding must cite a source: profiler marker name, file:line, or tool output
- Severity levels: CRITICAL (blocks release), WARNING (investigate), INFO (acceptable)
- CRITICAL requires frame time > budget sustained 5+ frames OR GC > 10 KB/frame
- WARNING requires frame time 80-100% budget OR GC 1-10 KB/frame
- Include max 10 findings — prioritize by impact, not count
- Each finding: one line summary + source + recommended fix
- Mobile analysis must apply 0.65 thermal factor to frame budget
- Save report to `Documents/Profiler/PERF_{TOPIC}_{YYYYMMDD}.md`

## Output Format

Short markdown report at `Documents/Profiler/PERF_{TOPIC}_{YYYYMMDD}.md` — budget status, ranked findings (max 10), subsystem breakdown, top 3 recommended fixes.

## Reference Files

- `references/report-template.md` — markdown template for the highlight report

Load via `read_skill_file("unity-profiler", "references/report-template.md")`.

## Standards

Load `unity-standards` for performance thresholds and anti-pattern lists:

- `quality/performance-audit.md` — frame budgets, GC hotspots, draw call targets, ProfilerMarker patterns
- `review/performance-checklist.md` — hot-path allocation patterns, Update complexity

Load via `read_skill_file("unity-standards", "references/<path>")`.
