---
name: unity-debug-log
description: "Generate targeted Debug.Log statements wrapped in #if UNITY_EDITOR to help understand code flow, logic, and state. Produces color-coded, structured log snippets — never modifies or adds code to the project. Use when: (1) Need to trace execution flow through methods, (2) Want to inspect variable state at runtime, (3) Debugging null references or unexpected values, (4) Understanding Unity lifecycle ordering, (5) Tracking event subscriptions and callbacks, (6) Monitoring state machine transitions. Triggers: 'add debug logs', 'trace this flow', 'log this method', 'debug log', 'add logging', 'trace execution', 'monitor state', 'log variables', 'show me the flow', 'instrument this code'."
---

# Unity Debug Log Generator

**Input**: User request describing what they want to understand — a method, flow, state, or behavior

## Hard Constraints

- **READ-ONLY**: Never edit, add, or modify any project file. Output log snippets as text only.
- **Never commit**: No git operations.
- **#if UNITY_EDITOR**: Every Debug.Log MUST be wrapped in `#if UNITY_EDITOR` / `#endif`.
- **[DBG] prefix**: Every log message starts with `[DBG]` for easy filtering.
- **Color-coded**: Every log uses `<color=X>` tags per the color guide below.
- **ALWAYS use template**: Follow `references/log-format.md` exactly.

## Workflow

1. **Understand** — Read the user's request. What do they want to see? (flow, state, null check, lifecycle, event)
2. **Read Code** — Open the target file(s). Understand the method signatures, parameters, fields, and call chain.
3. **Classify** — Determine log types needed (see Log Types below).
4. **Generate** — Produce log snippets per `references/log-format.md`. One code block per insertion point.
5. **Present** — Output using the Response Template below. Show WHERE each snippet goes (file:line, before/after which statement).

## Log Types & Colors

| Type | Color | When |
|:---|:---|:---|
| **Flow** | `yellow` | Method entry/exit, branch taken |
| **State** | `orange` | Variable values, field inspection, state transitions |
| **Null Check** | `cyan` | Null guards, reference validation |
| **Lifecycle** | `magenta` | Awake, OnEnable, Start, OnDestroy, OnDisable |
| **Collection** | `lime` | List/array counts, element inspection |
| **Error** | `red` | Unexpected conditions, fallthrough cases |
| **Event** | `green` | Event subscribe/unsubscribe/invoke |
| **Timing** | `white` | Frame count, deltaTime, timestamps |

## Log Format Examples

```csharp
// Flow — method entry with parameters
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DBG] ClassName.MethodName ENTER | param1={param1}, param2={param2}</color>");
#endif

// Flow — method exit with return value
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DBG] ClassName.MethodName EXIT | result={result}</color>");
#endif

// Flow — branch taken
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DBG] ClassName.MethodName | Taking path: {(condition ? "A" : "B")}</color>");
#endif

// State — variable inspection
#if UNITY_EDITOR
Debug.Log($"<color=orange>[DBG] ClassName.MethodName | _health={_health}, _shield={_shield}, _isDead={_isDead}</color>");
#endif

// State — transition
#if UNITY_EDITOR
Debug.Log($"<color=orange>[DBG] ClassName | State: {_previousState} -> {_currentState}</color>");
#endif

// Null Check
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DBG] ClassName.MethodName | _target={(_target != null ? _target.name : "NULL")}, _rb={(_rb != null ? "valid" : "NULL")}</color>");
#endif

// Lifecycle
#if UNITY_EDITOR
Debug.Log($"<color=magenta>[DBG] {GetType().Name}.Awake | gameObject={gameObject.name}, instanceId={GetInstanceID()}</color>");
#endif

// Collection
#if UNITY_EDITOR
Debug.Log($"<color=lime>[DBG] ClassName.MethodName | _items.Count={_items?.Count ?? -1}, firstItem={(_items?.Count > 0 ? _items[0].ToString() : "empty")}</color>");
#endif

// Error — unexpected condition
#if UNITY_EDITOR
Debug.LogWarning($"<color=red>[DBG] ClassName.MethodName | UNEXPECTED: condition={condition}, expected={expected}</color>");
#endif

// Event
#if UNITY_EDITOR
Debug.Log($"<color=green>[DBG] ClassName.OnEnable | Subscribing to EventName</color>");
#endif

// Timing
#if UNITY_EDITOR
Debug.Log($"<color=white>[DBG] ClassName.MethodName | frame={Time.frameCount}, time={Time.time:F3}, dt={Time.deltaTime:F4}</color>");
#endif
```

## Output

Debug.Log code snippets per the Response Template below. Never modifies project files.

## Response Template

ALWAYS use this exact structure:

```
## Debug Logs for `{ClassName}.{MethodName}` [{purpose}]

{1-2 sentences: what these logs will reveal}

### {FileNameA}.cs

**Insert at line {N}** (before `{statement}`):
​```csharp
#if UNITY_EDITOR
Debug.Log($"<color={color}>[DBG] ...</color>");
#endif
​```

**Insert at line {M}** (after `{statement}`):
​```csharp
#if UNITY_EDITOR
Debug.Log($"<color={color}>[DBG] ...</color>");
#endif
​```

### {FileNameB}.cs (if multi-file)

...same pattern...

---
**Log summary**: {N} logs across {M} files — filter by `[DBG]` in Console
**What to look for**: {specific patterns or values the user should watch for}
```

## Tool Selection

| Need | Tool |
|:---|:---|
| Read target code | `read` |
| Find method definition | `lsp_goto_definition` |
| Find callers | `lsp_find_references` |
| Find by pattern | `grep` / `ast_grep_search` |
| Locate file | `glob` |

## Rules

- Output log snippets only. NEVER edit files.
- Each log must have: `#if UNITY_EDITOR` wrapper, `<color=X>` tag, `[DBG]` prefix, `ClassName.MethodName` context.
- Use string interpolation `$"..."` always. Never `string.Format` or concatenation.
- For null-safe inspection: use ternary `(x != null ? x.name : "NULL")` or `x?.ToString() ?? "NULL"`.
- Include exact file path and line number for each insertion point.
- Group logs by file. Order by execution flow (top to bottom).
- Keep log messages concise — show the value, not a novel.
