---
name: unity-fix-errors
description: "Diagnose and fix Unity errors. Use when: (1) Console shows compiler errors/exceptions, (2) Play Mode behavior is broken, (3) Build fails, (4) Need structured debug report."
---

# Unity Debugger

Systematically identify and resolve Unity technical issues.

## Purpose

Diagnose and fix Unity errors — compiler errors, runtime exceptions, broken Play Mode behavior, and failed builds — using a structured triage-to-fix workflow.

## Input

- **Required**: Error message, stack trace, or description of broken behavior
- **Optional**: Console logs, affected scripts, repro steps, build target

## Output

A debug report saved to `Documents/Debugs/DEBUG_[ErrorName]_[Timestamp].md` (per `DEBUG_REPORT_TEMPLATE.md`) documenting: error classification, root cause, fix applied, and verification result.

## Examples

| User Request | Skill Action |
|:---|:---|
| "NullReferenceException in PlayerController.cs line 42" | Trace the null ref, identify missing assignment, apply fix, verify with compile check |
| "Build fails on Android with 'shader not supported'" | Check shader compatibility, replace with URP fallback, rebuild |
| "Game freezes when opening inventory" | Check for infinite loops / deadlocks in inventory code, add guard, verify in Play Mode |

## Output Requirement (MANDATORY)

**Every debug report MUST follow the template**: [DEBUG_REPORT_TEMPLATE.md](.claude/skills/unity-fix-errors/assets/templates/DEBUG_REPORT_TEMPLATE.md)

Save output to: `Documents/Debugs/DEBUG_[ErrorName]_[Timestamp].md`

Read the template first, then populate all sections.

## Debugging Workflow

1. **Gather Intel**
   - `unityMCP_get_unity_logs(show_errors=true)` → Get error message, stack trace, frequency
   - Identify: script, line number, error type (NullRef, IndexOutOfRange, etc.)
   - `unityMCP_capture_scene_object()` for visual/UI issues

2. **Investigate**
   - `view_file` → Code around error line
   - `grep_search` → Find all references to failing variable/object
   - Check component properties via `unityMCP_get_game_object_info(gameObjectPath="...")`

3. **Fix**
   - Draft fix (null guard, race condition, logic correction)
   - Apply via code edit tools

4. **Verify**
   - `unityMCP_check_compile_errors` → Confirm no compile errors
   - `unityMCP_get_unity_logs(show_errors=true)` → If errors persist, repeat Step 1

5. **Runtime Validate**
   - `unityMCP_play_game` → Verify fix in action
   - Ensure no regressions
   - `unityMCP_stop_game` → Stop after validation

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
- **Clean Slate**: `unityMCP_check_compile_errors` to rule out transient state
- **Isolate**: Reproduce in empty test scene if systemic
- **Evidence-Based**: Only declare fixed if console clear after repro steps

---

## MCP Tools Integration

Prefer `unityMCP_*` tools over manual file/shell operations for Unity Editor interaction.

| Operation | MCP Tool | Replaces |
|-----------|----------|----------|
| Read console errors | `unityMCP_get_unity_logs(show_errors=true)` | `read_console` |
| Check compilation | `unityMCP_check_compile_errors` | `refresh_unity(compile="request")` |
| Play game | `unityMCP_play_game` | `manage_editor(action="play")` |
| Stop game | `unityMCP_stop_game` | `manage_editor(action="stop")` |
| Inspect object | `unityMCP_get_game_object_info(gameObjectPath="...")` | `mcpforunity://scene/gameobject` |
| Scene screenshot | `unityMCP_capture_scene_object()` | `manage_scene` screenshot |
| List hierarchy | `unityMCP_list_game_objects_in_hierarchy(nameFilter="...")` | Manual scene browsing |
| Editor state | `unityMCP_get_unity_editor_state` | Manual editor checks |

### Debug-Fix-Verify Flow

```
1. unityMCP_get_unity_logs(show_errors=true)       → Capture errors and stack traces
2. unityMCP_get_game_object_info(gameObjectPath=..) → Inspect failing object's components
3. [Apply code fix via editor tools]
4. unityMCP_check_compile_errors                    → Confirm compilation success
5. unityMCP_play_game                               → Runtime validation
6. unityMCP_get_unity_logs(show_errors=true)        → Verify no new errors
7. unityMCP_stop_game                               → Clean stop
```
