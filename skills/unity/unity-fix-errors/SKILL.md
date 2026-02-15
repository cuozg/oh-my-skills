---
name: unity-fix-errors
description: "(opencode-project - Skill) Diagnose and fix Unity errors. Use when: (1) Console shows compiler errors/exceptions, (2) Play Mode behavior is broken, (3) Build fails, (4) Need structured debug report, (5) Assembly definition conflicts, (6) Package import errors. Triggers: 'fix error', 'compiler error', 'CS0', 'NullReferenceException', 'MissingReferenceException', 'build failed', 'play mode broken', 'stack trace', 'exception', 'runtime error', 'console error', 'red error', 'script error', 'assembly error', 'serialization error', 'missing script', 'broken prefab', 'fix this', 'not compiling', 'won\\'t compile', 'error in console', 'asmdef error', 'package error', 'type not found', 'namespace missing'."
---

# Unity Debugger

**Input**: Error message, stack trace, or broken behavior description + optional console logs, affected scripts, repro steps
**Output**: Debug report at `Documents/Debugs/DEBUG_[ErrorName]_[Timestamp].md` per [DEBUG_REPORT_TEMPLATE.md](.opencode/skills/unity/unity-fix-errors/assets/templates/DEBUG_REPORT_TEMPLATE.md)

## Workflow

1. **Gather** — `unityMCP_get_unity_logs(show_errors=true)` → error message, stack trace, frequency; `unityMCP_capture_scene_object()` for visual issues
2. **Investigate** — read code around error line, grep references to failing variable, `unityMCP_get_game_object_info()` for component state
3. **Fix** — draft fix (null guard, race condition, logic correction), apply via edit tools
4. **Verify** — `unityMCP_check_compile_errors`, then `unityMCP_get_unity_logs(show_errors=true)` — repeat if errors persist
5. **Runtime Validate** — `unityMCP_play_game` → verify fix → `unityMCP_stop_game`
6. **Document** (optional) — save report, run `/unity-test` for stability

## Safety Constraints

- Always backup before destructive fixes; user confirmation for scene/prefab mods and multi-system changes
- ALWAYS run `unityMCP_check_compile_errors` after changes; NEVER skip runtime validation for gameplay errors
- If fix introduces new errors: revert immediately; if validation fails: document and propose alternative
- Fix ONLY the reported error — don't refactor surrounding code
- User confirmation required for: deleting/renaming public methods, changing execution order, modifying build/project settings, third-party package changes

## Common Fixes

| Error | Typical Fix |
|-------|-------------|
| NullReferenceException | Add null guard, verify serialized reference |
| IndexOutOfRangeException | Validate array bounds before access |
| MissingReferenceException | Check if destroyed, use `this == null` after await |
| Race Condition | Verify async/await order, add synchronization |

## Best Practices

- **Stack Trace First**: Top of trace = immediate trigger
- **Clean Slate**: `unityMCP_check_compile_errors` to rule out transient state
- **Isolate**: Reproduce in empty test scene if systemic
- **Evidence-Based**: Only declare fixed if console clear after repro steps
