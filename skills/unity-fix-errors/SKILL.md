---
name: unity-fix-errors
description: "Diagnose and fix Unity errors. Use when: (1) Console shows compiler errors/exceptions, (2) Play Mode behavior is broken, (3) Build fails, (4) Need structured debug report."
---

# Unity Debugger

Systematically identify and resolve Unity technical issues.

## Output Requirement (MANDATORY)

**Every debug report MUST follow the template**: [DEBUG_REPORT_TEMPLATE.md](assets/templates/DEBUG_REPORT_TEMPLATE.md)

Save output to: `Documents/Debugs/DEBUG_[ErrorName]_[Timestamp].md`

Read the template first, then populate all sections.

## Debugging Workflow

1. **Gather Intel**
   - `read_console` → Get error message, stack trace, frequency
   - Identify: script, line number, error type (NullRef, IndexOutOfRange, etc.)
   - `manage_scene` (screenshot) for visual/UI issues

2. **Investigate**
   - `view_file` → Code around error line
   - `grep_search` → Find all references to failing variable/object
   - Check component properties via `mcpforunity://scene/gameobject/{id}/components`

3. **Fix**
   - Draft fix (null guard, race condition, logic correction)
   - Apply: `script_apply_edits` (structural) or `apply_text_edits` (minor)

4. **Verify**
   - `refresh_unity(compile="request", wait_for_ready=true)`
   - `read_console` again - if errors persist, repeat Step 1

5. **Runtime Validate**
   - `manage_editor(action="play")` → Verify fix in action
   - Ensure no regressions

6. **Document** (Optional)
   - Save report to `Documents/Debugs/DEBUG_[ErrorName]_[Timestamp].md`
   - Run `/unity-test` for system stability

## Common Fixes

| Error | Typical Fix |
|-------|-------------|
| NullReferenceException | Add null guard, verify serialized reference |
| IndexOutOfRangeException | Validate array bounds before access |
| MissingReferenceException | Check if object was destroyed, use `this == null` after await |
| Race Condition | Verify async/await order, add synchronization |

## Best Practices

- **Stack Trace First**: Top of trace = immediate trigger
- **Clean Slate**: `refresh_unity` to rule out transient state
- **Isolate**: Reproduce in empty test scene if systemic
- **Evidence-Based**: Only declare fixed if console clear after repro steps
