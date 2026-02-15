---
name: unity-debug
description: "Deep investigation and debugging of Unity errors. Use when: (1) User provides a stack trace or error message, (2) User describes unexpected behavior, (3) Need to understand WHY an error occurs (not just fix it), (4) Creating detailed debug reports with root cause analysis. Triggers: 'debug this error', 'why is this happening', 'investigate this crash', 'trace this exception', 'explain this stack trace'."
---

# Unity Debug

**Input**: Error description — stack trace, error message, or unexpected behavior description
**Output**: Root cause analysis with logic trace, debug flow, evidence, and fix recommendations

## Core Philosophy

This skill is about **understanding**, not reporting:
1. Deeply understand expected vs actual behavior
2. Systematically investigate the logic chain
3. Build targeted debug flows to isolate root causes
4. Arrive at clear root cause with actionable fixes

## Workflow

1. **Understand Requirement** — What should happen vs. what does?
2. **Investigate Logic** — Trace execution, map data flow
3. **Build Debug Flow** — Strategic logging + runtime checks
4. **Root Cause Analysis** — Why, not just what
5. **Guide Resolution** — Recommend fix + hand off

## Step 1: Understand the Requirement

**From stack trace / error message — extract:**
- Error Type, Message, File:Line, Call Stack, Frequency

**From behavior description — clarify:**
- Expected vs actual behavior
- Reproduction steps (when, where, how often)
- Recent changes, consistent or intermittent?

**Key questions:** What is correct behavior? What conditions trigger it? What state is required?

## Step 2: Investigate Logic

Trace execution from trigger to failure:
1. **Read crash site** — code ±50 lines of context
2. **Trace callers** — `lsp_find_references` / `lsp_goto_definition`
3. **Map data flow** — track variables from source to crash
4. **Check lifecycle** — Awake → OnEnable → Start ordering
5. **Find state mutations** — other modifiers (singletons, statics, events)
6. **Check async boundaries** — coroutines, async/await, callbacks

Delegate to `unity-investigate` when spanning multiple systems.

## Step 3: Build Debug Flow

Add targeted instrumentation. **MANDATORY**: wrap ALL `Debug.Log` in `#if UNITY_EDITOR`, apply color tags.

```csharp
// Entry/Exit
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DEBUG] ProcessDamage ENTER: damage={damage}, health={_health}</color>");
#endif

// Null Guard
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DEBUG] _player={(_player != null ? "valid" : "NULL")}</color>");
#endif

// State Transition
#if UNITY_EDITOR
Debug.Log($"<color=orange>[DEBUG] State: {_prevState} → {_currentState}</color>");
#endif

// Lifecycle
#if UNITY_EDITOR
void Awake() => Debug.Log($"<color=magenta>[DEBUG] {GetType().Name}.Awake on {gameObject.name}</color>");
#endif
```

Color guide: `yellow` (general), `cyan` (null checks), `orange` (state), `lime` (collections), `magenta` (lifecycle), `red` (errors)

All logs prefixed with `[DEBUG]` for easy filtering/removal.

## Step 4: Root Cause Analysis

| Level | Question |
|-------|----------|
| **Immediate** | What null/invalid value triggered the error? |
| **Proximate** | Why was that value null/invalid? |
| **Root** | What design/logic flaw allowed this state? |
| **Contributing** | Timing, concurrency, external dependencies? |

### Common Root Causes

| Symptom | Typical Causes |
|---------|----------------|
| NullReferenceException | Uninitialized field, destroyed object, race condition |
| IndexOutOfRange | Off-by-one, stale index, modified collection |
| MissingReferenceException | Destroyed during async op, held reference |
| StackOverflowException | Recursive call without base case |

See [common_errors.md](references/common_errors.md) for detailed patterns.

## Step 5: Guide Resolution

Communicate findings as structured text:
- **Root Cause**: one-sentence description
- **Evidence**: debug output or code path confirming cause
- **Quick Fix**: minimal change to stop the crash
- **Proper Fix**: address root cause architecturally
- **Prevention**: avoid this class of bug going forward

When fix is straightforward → apply directly or delegate to `unity-code` / `unity-fix-errors`.
When complex → explain root cause, propose options, let user decide.
**Clean up** `[DEBUG]` logs after resolution.

## Skill Integration

| Scenario | Delegate To |
|----------|-------------|
| Deep system tracing across files | `unity-investigate` |
| Implementing the fix | `unity-code` or `unity-fix-errors` |
| Performance-related bugs | `unity-optimize-performance` |
