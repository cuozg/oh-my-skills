---
name: unity-debug
description: "Deep investigation and debugging of Unity errors. Use when: (1) User provides a stack trace or error message, (2) User describes unexpected behavior, (3) Need to understand WHY an error occurs (not just fix it), (4) Creating detailed debug reports with root cause analysis. Triggers: 'debug this error', 'why is this happening', 'investigate this crash', 'trace this exception', 'explain this stack trace'."
---

# Unity Debug

Investigate Unity errors deeply — understand the requirement, trace logic chains, build smart debug flows, and identify root causes to guide resolution.

## Purpose

Deeply investigate Unity errors and unexpected behaviors to understand WHY they occur — trace logic chains, build targeted debug flows, and produce root cause analysis that guides resolution.

## Input

- **Required**: Error description — stack trace, error message, or description of unexpected behavior
- **Optional**: Expected vs actual behavior, repro steps, affected scenes/prefabs, recent code changes

## Output

A root cause analysis with: requirement understanding, logic chain trace, debug flow design, evidence collected, and identified root cause. Output follows the skill's internal debug methodology (no separate template file).

## Examples

| User Request | Skill Action |
|:---|:---|
| "Why does the player teleport when jumping near walls?" | Trace physics + movement logic, add conditional logging, identify collision resolver conflict |
| "Explain this stack trace from matchmaking" | Walk through each frame, map to code, identify the race condition causing the crash |
| "Score doesn't update after killing enemies" | Trace event chain: kill event → score handler → UI binding, find broken subscription |

## Core Philosophy

This skill is about **understanding**, not reporting. The goal is to:
1. Deeply understand what the user expects vs. what actually happens
2. Systematically investigate the logic chain that produces the bug
3. Build targeted debug flows to capture evidence and isolate root causes
4. Arrive at a clear root cause with actionable fix recommendations

## Workflow

```
Input (Error / Unexpected behavior)
          │
          ▼
┌─────────────────────────────┐
│ 1. UNDERSTAND REQUIREMENT   │  What should happen vs. what does?
└───────────┬─────────────────┘
            ▼
┌─────────────────────────────┐
│ 2. INVESTIGATE LOGIC        │  Trace execution, map data flow
└───────────┬─────────────────┘
            ▼
┌─────────────────────────────┐
│ 3. BUILD DEBUG FLOW         │  Strategic logging + runtime checks
└───────────┬─────────────────┘
            ▼
┌─────────────────────────────┐
│ 4. ROOT CAUSE ANALYSIS      │  Why, not just what
└───────────┬─────────────────┘
            ▼
┌─────────────────────────────┐
│ 5. GUIDE RESOLUTION         │  Recommend fix + hand off
└─────────────────────────────┘
```

## Step 1: Understand the Requirement

Clarify the gap between expected and actual behavior before touching code.

**From a stack trace / error message — extract:**

| Field | Source | Example |
|-------|--------|---------|
| Error Type | Exception name | `NullReferenceException` |
| Message | Error text | `Object reference not set` |
| File:Line | Stack trace | `PlayerController.cs:42` |
| Call Stack | Full trace | Method chain |
| Frequency | User/console | `Every frame` / `On button click` |

**From a behavior description — clarify:**
- What does the user **expect** to happen?
- What **actually** happens instead?
- Reproduction steps (when, where, how often)
- Recent changes that might be related
- Is the behavior consistent or intermittent?

**Key questions to ask yourself (or the user if unclear):**
- What is the correct behavior for this code path?
- Under what conditions should this code execute?
- What state must exist for this to work correctly?

## Step 2: Investigate Logic

Trace the execution path from trigger to failure point.

**Tools to use:**
- `lsp_goto_definition` / `lsp_find_references` — trace call graph
- `grep` / `ast_grep_search` — find patterns, usages, related code
- `unity-investigate` skill — delegate when investigation spans multiple systems

**Investigation checklist:**

1. **Read the crash site** — code around the error line with ±50 lines of context
2. **Trace callers** — who calls this method? Under what conditions?
3. **Map data flow** — track the variable(s) involved from source to crash point
4. **Check lifecycle** — Unity lifecycle timing (Awake → OnEnable → Start order)
5. **Find state mutations** — what else modifies the involved state? Singletons, statics, events?
6. **Check async boundaries** — coroutines, async/await, callbacks that cross frame boundaries

**State questions to answer:**
- What state must exist for this code path to succeed?
- What could invalidate that state?
- When is the state initialized vs. when is it consumed?
- What other code paths modify this state?

## Step 3: Build a Smart Debug Flow

Add targeted instrumentation to capture evidence. This is the primary code modification step.

### Debug Flow Patterns

**Entry/Exit — bracket the problem:**
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DEBUG] ProcessDamage ENTER: damage={damage}, type={type}, health={_health}</color>");
#endif
// ... existing code ...
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DEBUG] ProcessDamage EXIT: health={_health}, isDead={IsDead}</color>");
#endif
```

**Null Guard — expose missing state:**
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DEBUG] _player={(_player != null ? "valid" : "NULL")}, _target={(_targetEnemy != null ? _targetEnemy.name : "NULL")}</color>");
#endif
```

**State Transition — catch mutations:**
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=orange>[DEBUG] State: {_prevState} → {_currentState}</color>");
Debug.Log($"<color=orange>[DEBUG] Before: field={_field?.ToString() ?? "null"}</color>");
#endif
_field = newValue;
#if UNITY_EDITOR
Debug.Log($"<color=orange>[DEBUG] After: field={_field?.ToString() ?? "null"}</color>");
#endif
```

**Collection Bounds — prevent index errors:**
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=lime>[DEBUG] items.Count={items?.Count ?? -1}, index={index}</color>");
#endif
```

**Lifecycle — catch ordering issues:**
```csharp
#if UNITY_EDITOR
void Awake() => Debug.Log($"<color=magenta>[DEBUG] {GetType().Name}.Awake on {gameObject.name}</color>");
void OnEnable() => Debug.Log($"<color=magenta>[DEBUG] {GetType().Name}.OnEnable</color>");
void Start() => Debug.Log($"<color=magenta>[DEBUG] {GetType().Name}.Start</color>");
#endif
```

**Conditional (strip from builds):**
```csharp
[System.Diagnostics.Conditional("UNITY_EDITOR")]
private void DebugLog(string msg) => Debug.Log($"<color=yellow>[DEBUG] {msg}</color>");
```

### Debug Flow Guidelines

- **MANDATORY**: Wrap ALL `Debug.Log` statements in `#if UNITY_EDITOR`...`#endif` preprocessor flags
- **MANDATORY**: Apply highlight color to ALL `Debug.Log` output using `<color=COLOR>...</color>` tags
- Color guide: `yellow` (general), `cyan` (null checks), `orange` (state changes), `lime` (collections), `magenta` (lifecycle), `red` (errors)
- Prefix ALL debug logs with `[DEBUG]` for easy filtering/removal
- Log BEFORE and AFTER critical operations
- Include method name + relevant variable values (not just "here")
- Log collection counts before index access
- Log object validity before method calls
- Place logs strategically — too many obscure the signal

### Runtime Verification via MCP

After adding debug logs, use MCP tools to run and capture output:

```
1. unityMCP_check_compile_errors         → Verify debug logs compile
2. unityMCP_play_game                    → Reproduce the issue
3. unityMCP_get_unity_logs(search_term="[DEBUG]") → Capture debug output
4. unityMCP_stop_game                    → Analyze results
```

## Step 4: Root Cause Analysis

Identify the underlying cause, not just the symptom.

**Analysis framework:**

| Level | Question |
|-------|----------|
| **Immediate** | What null/invalid value triggered the error? |
| **Proximate** | Why was that value null/invalid at that moment? |
| **Root** | What design/logic flaw allowed this state to exist? |
| **Contributing** | Timing, concurrency, external dependencies? |

**Common root cause categories:**

| Symptom | Typical Root Causes |
|---------|---------------------|
| NullReferenceException | Uninitialized field, destroyed object, race condition, missing reference |
| IndexOutOfRange | Off-by-one, stale index, collection modified during iteration |
| MissingReferenceException | Object destroyed during async op, held reference to destroyed object |
| InvalidOperationException | Wrong state machine state, collection modified during enumeration |
| StackOverflowException | Recursive call without base case, circular dependencies |

For detailed patterns and solutions, see [references/common_errors.md](references/common_errors.md).

## Step 5: Guide Resolution

Present findings and recommend fixes directly to the user. Do NOT generate report files.

**Output format** — communicate findings as structured inline text:

| Section | Content |
|---------|---------|
| **Root Cause** | One-sentence description of the underlying issue |
| **Evidence** | Debug log output or code path that confirms the cause |
| **Quick Fix** | Minimal change to stop the crash (guard clause, null check) |
| **Proper Fix** | Address the root cause architecturally |
| **Prevention** | How to avoid this class of bug going forward |

**For each identified cause, communicate:**

1. **What's happening** — the root cause in plain language
2. **Quick fix** — minimal change to prevent the crash (guard clause, null check)
3. **Proper fix** — address the root cause with correct architecture
4. **Prevention** — how to avoid this class of bug in the future

**When the fix is straightforward** — apply it directly (or delegate to `unity-code` / `unity-fix-errors`).

**When the fix is complex or architectural** — explain the root cause, propose options, let the user decide.

**Clean up** — after the issue is resolved, remove `[DEBUG]` log statements (or suggest the user does).

## Skill Integration

| Scenario | Delegate To |
|----------|-------------|
| Deep system tracing across multiple files/systems | `unity-investigate` |
| Implementing the actual fix | `unity-code` or `unity-fix-errors` |
| Performance-related bugs | `unity-optimize-performance` |

## MCP Tools for Investigation

| Operation | Tool |
|-----------|------|
| Read console errors | `unityMCP_get_unity_logs(show_errors=true)` |
| Filter debug output | `unityMCP_get_unity_logs(search_term="[DEBUG]")` |
| Inspect object state | `unityMCP_get_game_object_info(gameObjectPath="...")` |
| Browse hierarchy | `unityMCP_list_game_objects_in_hierarchy(nameFilter="...")` |
| Scene screenshot | `unityMCP_capture_scene_object(gameObjectPath="...")` |
| Editor state | `unityMCP_get_unity_editor_state` |
| Check compilation | `unityMCP_check_compile_errors` |
| Play to reproduce | `unityMCP_play_game` |
| Stop after repro | `unityMCP_stop_game` |

### Full Investigation Loop

```
1. unityMCP_get_unity_logs(show_errors=true)             → Capture error + stack trace
2. [Trace code: lsp_goto_definition, lsp_find_references]  → Map execution path
3. [Add Debug.Log statements]                              → Instrument code
4. unityMCP_check_compile_errors                         → Verify instrumentation compiles
5. unityMCP_play_game                                    → Reproduce issue
6. unityMCP_get_unity_logs(search_term="[DEBUG]")        → Capture evidence
7. unityMCP_stop_game                                    → Analyze and conclude
```
