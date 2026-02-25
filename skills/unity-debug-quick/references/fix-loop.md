# Fix Loop — Delegation & Iteration

After the tree output and interactive prompt, handle user's choice:

## User Picks a Solution Number

1. **Build delegation prompt** with:
   - Root cause summary (from investigation)
   - Chosen solution's approach, target file(s), and line(s)
   - BEFORE/AFTER code expectations
   - Verification steps from the `verify` section

2. **Delegate** via `task()`:
   ```
   task(
     category="quick",  // or "deep" for architectural fixes
     load_skills=["unity-code-quick"],
     description="Apply fix: {solution title}",
     prompt="
       1. TASK: Apply {solution title} to fix {issue}.
       2. EXPECTED OUTCOME: {describe the fixed behavior}.
       3. REQUIRED TOOLS: read, edit, lsp_diagnostics.
       4. MUST DO:
          - Modify ONLY the files listed: {file list}.
          - Apply the approach: {approach description}.
          - Run lsp_diagnostics on changed files after edit.
       5. MUST NOT DO:
          - Do NOT modify unrelated files.
          - Do NOT refactor beyond the fix scope.
          - Do NOT commit.
       6. CONTEXT: {root cause summary, file:line refs, relevant code context}.
     ",
     run_in_background=false
   )
   ```

3. **Verify** after delegation completes:
   - Run `lsp_diagnostics` on changed files
   - Confirm no new errors introduced
   - Report result to user

4. **Continue the loop** — ask:

   > ✅ Fix applied and verified. Any other issues to investigate? (or type `stop` to end)

## User Says `skip`

Ask: "Any other issues to investigate? (or type `stop` to end)"

## User Says `stop`

End the session. No further output.

## Category Selection Guide

| Fix Type | Category | Skills |
| :--- | :--- | :--- |
| Quick/small fix (1-2 files) | `quick` | `["unity-code-quick"]` |
| Moderate fix (logic change) | `unspecified-low` | `["unity-code-quick"]` |
| Architectural fix | `deep` | `["unity-code-quick", "unity-code-deep"]` |
| Performance fix | `deep` | `["unity-code-quick", "unity-optimize-performance"]` |

## Rules

- ALWAYS use `run_in_background=false` — wait for fix to complete before verifying.
- ALWAYS run `lsp_diagnostics` after fix delegation.
- ALWAYS report verification result to user.
- If fix delegation fails, report the failure and ask user how to proceed.
- Store `session_id` from delegation — if fix needs adjustment, continue the same session.
- Never apply fixes directly — always delegate via `task()`.