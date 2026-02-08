---
name: unity-debug
description: "Deep investigation and debugging of Unity errors. Use when: (1) User provides a stack trace or error message, (2) User describes unexpected behavior, (3) Need to understand WHY an error occurs (not just fix it), (4) Creating detailed debug reports with root cause analysis. Triggers: 'debug this error', 'why is this happening', 'investigate this crash', 'trace this exception', 'explain this stack trace'."
---

# Unity Debug

Investigate Unity errors deeply, add strategic Debug.Log statements, identify root causes, and produce detailed debug reports.

## Output Requirement (MANDATORY)

**Every debug report MUST follow the template**: [DEBUG_REPORT_TEMPLATE.md](.claude/skills/unity-debug/assets/DEBUG_REPORT_TEMPLATE.md)

Save output to: `Documents/Debugs/DEBUG_{ErrorName}_{YYYYMMDD}.md`

Read the template first, then populate all sections.

## ⚠️ CRITICAL CONSTRAINT: READ-ONLY DEBUGGING

**This skill is STRICTLY for investigation and diagnosis, NOT for fixing code.**

### What You CAN Do:
- ✅ Add `Debug.Log` statements to capture runtime state
- ✅ Read and analyze code to understand execution flow
- ✅ Investigate root causes and document findings
- ✅ Provide fix recommendations **in the report file ONLY**

### What You CANNOT Do:
- ❌ **NEVER** modify logic code, fix bugs, or refactor
- ❌ **NEVER** apply quick fixes or proper fixes directly to code
- ❌ **NEVER** change any code except adding `Debug.Log` statements
- ❌ **NEVER** delete, rename, or restructure existing code

### Why This Matters:
The user must decide whether to apply fixes. Your role is to:
1. Diagnose the problem thoroughly
2. Add debug logging to capture evidence
3. Document all findings and proposed solutions in `Documents/Debugs/DEBUG_*.md`
4. **Let the user review and apply fixes themselves**

## Workflow

```
Input (Stack trace / Error description)
          │
          ▼
┌─────────────────────────┐
│ 1. GATHER INTEL         │
│    Parse error, locate  │
│    files, understand    │
│    context              │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 2. INVESTIGATE LOGIC    │
│    Use unity-investigate│
│    -code skill to trace │
│    execution flow       │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 3. ADD DEBUG.LOG        │
│    Strategic logging at │
│    entry/exit points,   │
│    state transitions    │
│    ✅ ONLY code change  │
│       allowed!          │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 4. ROOT CAUSE ANALYSIS  │
│    Identify WHY error   │
│    happens, not just    │
│    what triggers it     │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 5. DOCUMENT SOLUTIONS   │
│    Write fixes to       │
│    report file ONLY     │
│    ❌ NO code changes!  │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 6. GENERATE REPORT      │
│    Save to Documents/   │
│    Debugs/DEBUG_*.md    │
│    User decides to      │
│    apply fixes          │
└─────────────────────────┘
```

## Step 1: Gather Intel

Parse error input to extract:

| Field | Source | Example |
|-------|--------|---------|
| Error Type | Exception name | `NullReferenceException` |
| Message | Error description | `Object reference not set` |
| File | Stack trace | `PlayerController.cs` |
| Line | Stack trace | `line 42` |
| Call Stack | Full trace | Method chain |
| Frequency | User/console | `Every frame` / `On button click` |

**From stack trace:**
```
NullReferenceException: Object reference not set to an instance of an object
  at PlayerController.UpdateHealth () [0x00012] in Assets/Scripts/Player/PlayerController.cs:42
  at GameManager.OnPlayerDamaged () [0x00008] in Assets/Scripts/Managers/GameManager.cs:156
```

Extract: `PlayerController.cs:42`, called from `GameManager.cs:156`

**From user description:**
- Reproduce steps
- When it occurs (startup, specific action, random)
- Related recent changes

## Step 2: Investigate Logic

Load `unity-investigate` skill for deep analysis:

1. **Read error file** - Code around error line with context (±50 lines)
2. **Trace callers** - Use `grep_search` or `lsp_find_references` for call sites
3. **Map data flow** - Track variables involved in error from source to crash point
4. **Check lifecycle** - Identify Unity lifecycle timing issues (Awake vs Start vs Enable)
5. **Find side effects** - Singletons, static state, event subscriptions

**Key questions:**
- What state must exist for this code to work?
- What could make that state null/invalid?
- When is this state supposed to be initialized?
- What other code modifies this state?

## Step 3: Add Debug.Log Statements (ONLY ALLOWED CODE CHANGE)

⚠️ **This is the ONLY step where you modify code files.**

Add strategic logging to capture runtime state. Follow these patterns:

### Entry/Exit Logging
```csharp
public void ProcessDamage(int damage, DamageType type)
{
    Debug.Log($"[DEBUG] ProcessDamage ENTER: damage={damage}, type={type}, currentHealth={_health}");
    
    // ... existing code ...
    
    Debug.Log($"[DEBUG] ProcessDamage EXIT: newHealth={_health}, isDead={IsDead}");
}
```

### Null Check Logging
```csharp
Debug.Log($"[DEBUG] _player is {(_player != null ? "valid" : "NULL")}");
Debug.Log($"[DEBUG] _targetEnemy is {(_targetEnemy != null ? _targetEnemy.name : "NULL")}");
```

### State Transition Logging
```csharp
Debug.Log($"[DEBUG] State change: {_previousState} -> {_currentState}");
Debug.Log($"[DEBUG] Before assignment: field={_field?.ToString() ?? "null"}");
_field = newValue;
Debug.Log($"[DEBUG] After assignment: field={_field?.ToString() ?? "null"}");
```

### Collection Logging
```csharp
Debug.Log($"[DEBUG] items count={items?.Count ?? -1}");
Debug.Log($"[DEBUG] array length={array?.Length ?? -1}, accessing index={index}");
```

### Lifecycle Logging
```csharp
void Awake() => Debug.Log($"[DEBUG] {GetType().Name}.Awake() called, gameObject={gameObject.name}");
void Start() => Debug.Log($"[DEBUG] {GetType().Name}.Start() called");
void OnEnable() => Debug.Log($"[DEBUG] {GetType().Name}.OnEnable() called");
void OnDisable() => Debug.Log($"[DEBUG] {GetType().Name}.OnDisable() called");
void OnDestroy() => Debug.Log($"[DEBUG] {GetType().Name}.OnDestroy() called");
```

### Conditional Debug (Unity 2022+)
```csharp
[System.Diagnostics.Conditional("UNITY_EDITOR")]
private void DebugLog(string message) => Debug.Log($"[DEBUG] {message}");
```

**Logging Guidelines:**
- Prefix with `[DEBUG]` for easy filtering/removal later
- Include method name and relevant variable values
- Log BEFORE and AFTER critical operations
- Log collection counts before index access
- Log object validity before method calls

## Step 4: Root Cause Analysis

Identify the underlying cause, not just the symptom:

| Symptom | Typical Root Causes |
|---------|---------------------|
| NullReferenceException | Uninitialized field, destroyed object, missing reference, race condition |
| IndexOutOfRangeException | Off-by-one error, collection modified during iteration, stale index |
| MissingReferenceException | Object destroyed but reference held, async operation completed after destroy |
| InvalidOperationException | State machine in wrong state, collection modified during enumeration |
| StackOverflowException | Recursive call without exit condition, circular dependencies |

**Analysis Framework:**
1. **Immediate cause** - What null/invalid value triggered it?
2. **Proximate cause** - Why was that value null/invalid at that moment?
3. **Root cause** - What design/logic flaw allowed this state?
4. **Contributing factors** - Timing, concurrency, external dependencies?

## Step 5: Document Solutions (IN REPORT ONLY)

⚠️ **CRITICAL: Do NOT modify any code in this step. All solutions go in the report file.**

For each identified cause, **document** in the report:

1. **Quick Fix** - Minimal change to prevent crash (guard clause, null check)
2. **Proper Fix** - Address root cause with proper architecture
3. **Preventive Measures** - How to avoid similar issues in future

**Example documentation in report:**
```markdown
### Problem
`_playerData` is null when `UpdateUI()` is called because `Start()` runs before 
`GameManager.Initialize()` completes the async data load.

### Quick Fix (Prevent crash)
**File:** `Assets/Scripts/UI/PlayerUI.cs`
**Line:** 42

```csharp
// BEFORE:
public void UpdateUI()
{
    _healthBar.SetValue(_playerData.Health);
    // ... rest of method
}

// AFTER:
public void UpdateUI()
{
    if (_playerData == null)
    {
        Debug.LogWarning("[UpdateUI] _playerData not yet loaded, skipping update");
        return;
    }
    _healthBar.SetValue(_playerData.Health);
    // ... rest of method
}
```

**Trade-offs:** Silently skips update if data not ready; UI may show stale values.

### Proper Fix (Address root cause)
**File:** `Assets/Scripts/UI/PlayerUI.cs`

```csharp
// Subscribe to initialization event instead of polling
private void OnEnable()
{
    GameManager.OnDataLoaded += HandleDataLoaded;
}

private void OnDisable()
{
    GameManager.OnDataLoaded -= HandleDataLoaded;
}

private void HandleDataLoaded(PlayerData data)
{
    _playerData = data;
    UpdateUI();
}
```

**Why this is better:** Event-driven approach ensures UI updates only when data is actually available.

### Preventive Measures
- [ ] Use dependency injection or event-driven initialization
- [ ] Document initialization order requirements
- [ ] Add runtime assertions in debug builds
```

**Remember:** The user will review these recommendations and decide which fixes to apply. Your job is to provide clear, actionable documentation.

## Step 6: Generate Debug Report

Save report to `Documents/Debugs/DEBUG_{ErrorName}_{YYYYMMDD}.md`

Use template: [DEBUG_REPORT_TEMPLATE.md](.claude/skills/unity-debug/assets/DEBUG_REPORT_TEMPLATE.md)

```bash
mkdir -p Documents/Debugs
```

Report structure:
1. Error Summary (type, file, line, frequency)
2. Stack Trace (formatted)
3. Investigation Findings (data flow, lifecycle, side effects)
4. Debug.Log Additions (files modified, logs added)
5. Root Cause Analysis (immediate, proximate, root)
6. Solutions (quick fix, proper fix, prevention)
7. References (related code, documentation)

## Common Unity Error Patterns

See [.claude/skills/unity-debug/references/common_errors.md](.claude/skills/unity-debug/references/common_errors.md) for detailed patterns and solutions for:
- NullReferenceException patterns
- Async/await pitfalls
- Unity lifecycle issues
- Serialization problems
- Event subscription leaks

## Best Practices

- **Never guess** - Always trace to source with evidence
- **Log strategically** - Too many logs obscure the problem
- **Preserve context** - Include variable values, not just "here"
- **Clean up** - Remove debug logs after issue resolved (or use `[Conditional]`)
- **Document** - Debug reports help with future similar issues
- **READ-ONLY** - Never modify code except for Debug.Log statements
- **User decides** - All fixes documented in report; user applies them

---

## MCP Tools Integration

Use `coplay-mcp_*` tools for Unity Editor interaction during investigation.

| Operation | MCP Tool |
|-----------|----------|
| Read console errors | `coplay-mcp_get_unity_logs(show_errors=true)` |
| Filter specific logs | `coplay-mcp_get_unity_logs(search_term="[DEBUG]")` |
| Inspect object state | `coplay-mcp_get_game_object_info(gameObjectPath="...")` |
| Browse hierarchy | `coplay-mcp_list_game_objects_in_hierarchy(nameFilter="...")` |
| Scene screenshot | `coplay-mcp_capture_scene_object(gameObjectPath="...")` |
| Editor state | `coplay-mcp_get_unity_editor_state` |
| Check compilation | `coplay-mcp_check_compile_errors` |
| Play to reproduce | `coplay-mcp_play_game` |
| Stop after repro | `coplay-mcp_stop_game` |

### Investigation Flow

```
1. coplay-mcp_get_unity_logs(show_errors=true)             → Capture error + stack trace
2. coplay-mcp_list_game_objects_in_hierarchy(nameFilter=..) → Locate relevant objects
3. coplay-mcp_get_game_object_info(gameObjectPath=..)      → Inspect component state
4. [Add Debug.Log statements]
5. coplay-mcp_check_compile_errors                         → Verify logs compile
6. coplay-mcp_play_game                                    → Reproduce issue
7. coplay-mcp_get_unity_logs(search_term="[DEBUG]")        → Capture debug output
8. coplay-mcp_stop_game                                    → Stop and analyze
```
