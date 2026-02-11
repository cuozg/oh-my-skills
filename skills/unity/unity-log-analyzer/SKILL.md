---
name: unity-log-analyzer
description: "Parse and analyze Unity Editor console logs to classify errors, group duplicates, and suggest fixes. Use when: (1) Console has many errors/warnings to triage, (2) Need to prioritize which errors to fix first, (3) Identifying recurring error patterns across play sessions, (4) Generating error summary reports for team review, (5) Mapping errors to likely source files. Triggers: 'analyze logs', 'log analysis', 'triage errors', 'parse console', 'error summary', 'what errors are happening'."
---

# Unity Log Analyzer

Parse, classify, and prioritize Unity Editor console logs — group duplicates, suggest probable causes, and generate actionable error triage reports.

## Purpose

Unity projects generate hundreds of console messages during play mode. This skill systematically parses those logs, classifies by severity and category, deduplicates repeated messages, and produces a prioritized report with suggested fix strategies.

## Input

- **Required**: Unity console log text (pasted or from `coplay-mcp_get_unity_logs`)
- **Optional**: Filter — `errors-only`, `warnings-only`, or `all` (default: `all`)
- **Optional**: Output format — `summary`, `detailed`, or `json` (default: `summary`)

## Output

An analysis report with:
1. **Summary** — total counts by severity (Error, Warning, Info)
2. **Grouped Errors** — deduplicated with occurrence count
3. **Category Classification** — NullRef, MissingComponent, AssetBundle, Serialization, Network, etc.
4. **Fix Suggestions** — pattern-matched recommendations per error type
5. **Priority Ranking** — Critical → High → Medium → Low

## Examples

| User Request | Skill Action |
|:---|:---|
| "Analyze the Unity console logs" | Fetch logs via MCP, parse, classify, group, suggest fixes |
| "What errors keep happening?" | Focus on recurring errors with high duplicate count |
| "Triage the build errors" | Filter to errors only, prioritize by severity |
| "Summarize today's console output" | Generate high-level summary with counts and categories |

## Workflow

### Phase 1: Log Collection

1. If logs not provided, fetch via:
   ```
   coplay-mcp_get_unity_logs(show_errors=true, show_warnings=true, limit=500)
   ```
2. Alternatively, run the Python analyzer on a log file:
   ```bash
   python3 .opencode/tools/unity-log-analyzer.py --input <log_text_or_file>
   ```

### Phase 2: Classification

Each log entry is classified into categories:

| Category | Pattern Indicators |
|:---|:---|
| NullReference | `NullReferenceException`, `Object reference not set` |
| MissingComponent | `MissingComponentException`, `GetComponent.*null` |
| MissingAsset | `Failed to load`, `Asset not found`, `Missing sprite` |
| Serialization | `SerializationException`, `Could not deserialize` |
| Network | `WebException`, `SocketException`, `HTTP error` |
| AssetBundle | `AssetBundle`, `bundle.*failed`, `download.*error` |
| UI | `Canvas`, `RectTransform`, `Layout`, `EventSystem` |
| Performance | `Frame budget`, `GC.Alloc`, `spike detected` |
| Shader | `Shader error`, `compilation failed`, `fallback` |
| Script | `CompilerError`, `TypeLoadException`, `assembly` |

### Phase 3: Deduplication & Grouping

1. Normalize log messages (strip line numbers, timestamps, memory addresses)
2. Group by normalized message
3. Count occurrences
4. Keep first and last timestamp for each group
5. Sort by occurrence count (most frequent first)

### Phase 4: Fix Suggestion

Pattern-match known error types to suggest fixes:

| Error Pattern | Suggested Fix |
|:---|:---|
| `NullReferenceException` at runtime | Add null-check, verify object lifecycle, check `HasInstance` |
| `MissingComponentException` | Verify component exists on prefab, check `RequireComponent` attribute |
| `Failed to load AssetBundle` | Check bundle URL, verify CDN availability, clear cache |
| `SerializationException` | Check data format version, validate JSON/FlatBuffer schema |
| `SocketException` | Check network connectivity, verify server URL, check timeout settings |

### Phase 5: Report Generation

Generate a markdown report:

```markdown
# Unity Console Log Analysis
## Date: YYYY-MM-DD

### Summary
- Errors: N | Warnings: N | Info: N
- Unique error patterns: N
- Most frequent: [error message] (Nx)

### Critical Errors (fix immediately)
1. [Error] — N occurrences — [suggested fix]

### Warnings (review when possible)
1. [Warning] — N occurrences — [suggested fix]

### Recommendations
1. [Prioritized action items]
```

## Integration with Other Skills

- **unity-fix-errors**: After analysis, delegate fixing to this skill
- **unity-debug**: For deep-dive on specific error root causes
- **unity-investigate**: To trace error sources through the codebase

## MCP Tools

- `coplay-mcp_get_unity_logs` — fetch logs directly from Unity Editor
- `coplay-mcp_check_compile_errors` — verify compile state
- `grep` — search codebase for error source patterns
- `lsp_diagnostics` — cross-reference with LSP errors
