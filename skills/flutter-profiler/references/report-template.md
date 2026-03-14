# report-template.md

Use this template when writing the output report for flutter-profiler.

---

```markdown
# Performance Report: {SHORT_TOPIC}

**Date**: YYYY-MM-DD
**Platform**: {iOS / Android / Web / Desktop}
**Target**: {fps} fps ({budget} ms/frame)
**Mode**: {Profile / Debug — always profile for accurate data}

---

## Budget Status

| Metric | Measured | Budget | Status |
|--------|----------|--------|--------|
| Frame time (avg) | {avg_ms} ms | {budget} ms | {OK/OVER} |
| Frame time (peak) | {peak_ms} ms | {budget} ms | {OK/OVER} |
| UI thread (avg) | {ui_ms} ms | {budget} ms | {OK/OVER} |
| Raster thread (avg) | {raster_ms} ms | {budget} ms | {OK/OVER} |
| Heap usage | {heap_mb} MB | {limit} MB | {OK/OVER} |

---

## Findings

### {CRITICAL/WARNING/INFO} — {one-line summary}

**Source**: {DevTools marker / file:line / profiler output}
**Impact**: {X ms / X% of frame budget / X MB retained}
**Fix**: {one-line actionable recommendation}

---

(Repeat for up to 10 findings, ranked by impact. CRITICAL first, then WARNING, then INFO.)

---

## Subsystem Breakdown

| Subsystem | Time (ms) | % Budget | Notes |
|-----------|-----------|----------|-------|
| Build (widgets) | {ms} | {pct}% | {rebuild count if known} |
| Layout | {ms} | {pct}% | {intrinsic issues} |
| Paint | {ms} | {pct}% | {overdraw notes} |
| Raster | {ms} | {pct}% | {shader compilation} |
| GC | {ms} | {pct}% | {frequency} |
| Platform channel | {ms} | {pct}% | {method channel calls} |

---

## Top 3 Fixes

1. **{Fix title}** — {what to change} at `{file:line}` — est. {X ms} saved
2. **{Fix title}** — {what to change} at `{file:line}` — est. {X ms} saved
3. **{Fix title}** — {what to change} at `{file:line}` — est. {X ms} saved

---

**Data source**: {DevTools / timeline export / manual measurement}
**Build mode**: {Profile / Release}
**Renderer**: {Skia / Impeller}
```

---

## Notes

- Save to `Documents/Profiler/PERF_{TOPIC}_{YYYYMMDD}.md`
- Max 10 findings — prioritize impact over quantity
- Each finding: 3 lines only (Source, Impact, Fix)
- CRITICAL findings must include estimated ms or MB cost
- Omit subsystem rows that show 0 ms
- Mobile reports: apply 0.7x thermal factor to budget column
- Always note renderer (Skia vs Impeller) — performance profiles differ significantly
