# report-template.md

Use this template when writing the output report for unity-profiler.

---

```markdown
# Performance Report: {SHORT_TOPIC}

**Date**: YYYY-MM-DD
**Platform**: {target platform}
**Target**: {fps} fps ({budget} ms/frame)

---

## Budget Status

| Metric | Measured | Budget | Status |
|--------|----------|--------|--------|
| Frame time (avg) | {avg_ms} ms | {budget} ms | {OK/OVER} |
| Frame time (peak) | {peak_ms} ms | {budget} ms | {OK/OVER} |
| GC alloc/frame | {gc_kb} KB | < 1 KB | {OK/OVER} |
| Draw calls | {draws} | {draw_target} | {OK/OVER} |

---

## Findings

### {CRITICAL/WARNING/INFO} — {one-line summary}

**Source**: {profiler marker / file:line / tool output}
**Impact**: {X ms / X% of frame budget / X KB per frame}
**Fix**: {one-line actionable recommendation}

---

### {CRITICAL/WARNING/INFO} — {one-line summary}

**Source**: {source}
**Impact**: {impact}
**Fix**: {recommendation}

---

(Repeat for up to 10 findings, ranked by impact. CRITICAL first, then WARNING, then INFO.)

---

## Subsystem Breakdown

| Subsystem | Time (ms) | % Budget | Trend |
|-----------|-----------|----------|-------|
| Rendering | {ms} | {pct}% | {stable/rising/new} |
| Scripts | {ms} | {pct}% | {trend} |
| Physics | {ms} | {pct}% | {trend} |
| GC | {ms} | {pct}% | {trend} |
| Animation | {ms} | {pct}% | {trend} |
| Other | {ms} | {pct}% | {trend} |

---

## Top 3 Fixes

1. **{Fix title}** — {what to change} at `{file:line}` — est. {X ms} saved
2. **{Fix title}** — {what to change} at `{file:line}` — est. {X ms} saved
3. **{Fix title}** — {what to change} at `{file:line}` — est. {X ms} saved

---

**Data source**: {get_worst_cpu_frames / get_worst_gc_frames / manual capture}
**Build**: {IL2CPP/Mono, Development/Release}
```

---

## Notes

- Save to `Documents/Profiler/PERF_{TOPIC}_{YYYYMMDD}.md`
- Max 10 findings — prioritize impact over quantity
- Each finding: 3 lines only (Source, Impact, Fix)
- CRITICAL findings must include estimated ms or KB cost
- Omit subsystem rows that show 0 ms
- Mobile reports: apply 0.65 thermal factor to budget column
