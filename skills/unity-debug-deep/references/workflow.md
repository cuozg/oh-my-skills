## Workflow

1. **Scope** — Define the issue precisely. What is the subject? What is expected vs actual behavior? What are the investigation boundaries?

2. **Survey** — Broad sweep: identify all files, classes, and systems involved. Use `glob`, `grep`, `lsp_symbols` to map the landscape.

3. **Trace Forward** — Start from the trigger/entry point. Follow execution flow step by step. Document every branch, state change, and side effect.

4. **Trace Backward** — Start from the failure/symptom. Work backwards: who set this value? Who called this method? What state was required?

5. **Cross-Cut** — Investigate orthogonal angles (minimum 3):
   - **Lifecycle**: Is ordering (Awake/OnEnable/Start) a factor?
   - **Threading**: Any async/coroutine/callback boundaries?
   - **State**: Who else mutates the relevant state?
   - **Timing**: Frame-dependent? Scene-load-dependent? First-run-only?
   - **Edge Cases**: Empty collections? Null inputs? Destroyed objects?
   - **External**: Scriptable Objects? Inspector values? Prefab overrides?

6. **Determine Root Cause** — Synthesize findings into a clear explanation of WHY the issue happens. Build an evidence chain from origin to symptom. Identify reproduction steps.

7. **Assess Impact** — What does this issue break downstream? What systems are affected? Rate severity.

8. **Formulate Solutions** — Generate 2-4 solution approaches with different trade-offs (quick fix vs proper fix vs architectural). Also identify any temporary workaround. Do NOT write implementation code — describe the approach and location.

9. **Write Report** — Fill the analysis template. Save to `Documents/Debug/`.

## Tool Selection

| Need | Tool |
|:---|:---|
| Read code | `read` |
| Find definition | `lsp_goto_definition` |
| Find all usages | `lsp_find_references` |
| Search symbols | `lsp_symbols` (workspace) |
| Pattern search | `grep` / `ast_grep_search` |
| Blast radius | `impact-analyzer` |
| File discovery | `glob` |
| Cross-reference | `lsp_find_references` chained |
| Check diagnostics | `lsp_diagnostics` |

Use ALL relevant tools. This is a deep investigation — thoroughness over speed.
