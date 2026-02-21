---
name: unity-log-analyzer
description: "Parse and analyze Unity Editor console logs to classify errors, group duplicates, and suggest fixes. Use when: (1) Console has many errors/warnings to triage, (2) Need to prioritize which errors to fix first, (3) Identifying recurring error patterns across play sessions, (4) Generating error summary reports for team review, (5) Mapping errors to likely source files. Triggers: 'analyze logs', 'log analysis', 'triage errors', 'parse console', 'error summary', 'what errors are happening'."
---

# Unity Log Analyzer

**Input**: Unity console log text (pasted or from `coplay-mcp_get_unity_logs`). Optional: filter (`errors-only`/`warnings-only`/`all`), format (`summary`/`detailed`/`json`).

## Output

Structured log analysis: error classification, duplicate grouping, priority ranking, and suggested fixes.

## Workflow

1. **Collect**: Fetch logs via `coplay-mcp_get_unity_logs(show_errors=true, show_warnings=true, limit=500)` or `python3 .opencode/tools/unity-log-analyzer.py --input <log>`
2. **Classify**: Categorize each entry (NullRef, MissingComponent, MissingAsset, Serialization, Network, AssetBundle, UI, Performance, Shader, Script)
3. **Deduplicate**: Normalize messages (strip timestamps/addresses), group by content, count occurrences, sort by frequency
4. **Suggest Fixes**: Pattern-match known errors to fixes (see table below)
5. **Report**: Generate markdown — summary counts, critical errors first, prioritized recommendations

## Category Patterns

| Category | Pattern Indicators |
|:---|:---|
| NullReference | `NullReferenceException`, `Object reference not set` |
| MissingComponent | `MissingComponentException`, `GetComponent.*null` |
| MissingAsset | `Failed to load`, `Asset not found`, `Missing sprite` |
| Serialization | `SerializationException`, `Could not deserialize` |
| Network | `WebException`, `SocketException`, `HTTP error` |
| Shader | `Shader error`, `compilation failed`, `fallback` |
| Script | `CompilerError`, `TypeLoadException`, `assembly` |

## Fix Suggestions

| Error Pattern | Suggested Fix |
|:---|:---|
| `NullReferenceException` | Add null-check, verify object lifecycle, check `HasInstance` |
| `MissingComponentException` | Verify component on prefab, add `RequireComponent` |
| `Failed to load AssetBundle` | Check bundle URL, verify CDN, clear cache |
| `SerializationException` | Check data format version, validate schema |
| `SocketException` | Check connectivity, verify server URL, check timeout |

## Handoff

- **Delegates to**: `unity-fix-errors` (apply fixes), `unity-debug` (deep single-error investigation)
- **Does NOT**: Fix errors directly or perform deep root cause analysis
