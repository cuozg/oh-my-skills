# Performance Audit Report Template

Use this template for Audit mode output.

## Report Structure

```markdown
# Performance Audit Report
**Project:** [name] | **Platform:** [target] | **FPS Target:** [target fps] | **Date:** [date]

## Executive Summary

| Category | Health | Top Issue |
|----------|--------|-----------|
| Code | [Good/Warning/Critical] | [one-line summary] |
| Rendering | [Good/Warning/Critical] | [one-line summary] |
| Memory | [Good/Warning/Critical] | [one-line summary] |
| Physics | [Good/Warning/Critical] | [one-line summary] |
| Build | [Good/Warning/Critical] | [one-line summary] |

**Overall:** [Critical/Warning/Good] — [1-2 sentence summary]

## Findings

### Critical

| # | Category | File/Setting | Issue | Fix | Est. Impact |
|---|----------|-------------|-------|-----|-------------|
| 1 | Code | `path/file.cs:42` | GetComponent in Update | Cache in Awake | -0.5ms/frame |

### Warning

| # | Category | File/Setting | Issue | Fix | Est. Impact |
|---|----------|-------------|-------|-----|-------------|

### Info

| # | Category | File/Setting | Issue | Fix | Est. Impact |
|---|----------|-------------|-------|-----|-------------|

## Quick Wins

Top 3 changes with highest impact-to-effort ratio:

1. **[change]** — [1 line description] → [expected improvement]
2. **[change]** — [1 line description] → [expected improvement]
3. **[change]** — [1 line description] → [expected improvement]

## Detailed Recommendations

### Code Optimizations
[specific code changes with before/after snippets]

### Settings Recommendations
| Setting | Current | Recommended | Path |
|---------|---------|-------------|------|

### Asset Optimizations
[specific asset changes with sizes/formats]
```

## Health Rating Criteria

| Rating | Meaning |
|--------|---------|
| Good | No significant issues found, within budget |
| Warning | Some issues found, may cause problems under load |
| Critical | Issues that will cause visible frame drops or crashes |

## Impact Estimation Guide

| Change | Typical Savings |
|--------|----------------|
| Cache GetComponent | 0.01-0.1ms per call eliminated |
| Remove LINQ from Update | 0.05-0.5ms per LINQ chain |
| Object pooling vs Instantiate | 0.5-2ms per spawn avoided |
| Seal MonoBehaviours | ~5% improvement in virtual dispatch |
| Fix Physics layer matrix | 0.1-1ms depending on object count |
| Texture compression | 50-75% memory reduction |
| Enable SRP Batcher | 20-50% draw call CPU reduction |
