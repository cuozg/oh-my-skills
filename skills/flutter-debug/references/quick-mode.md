# Quick Mode — Interactive Runtime Diagnosis

Interactive diagnosis for runtime bugs: reproduce → investigate → propose → user picks → fix → verify.

## When to Use

- Runtime crash, exception, or unexpected widget behavior
- Null assertion error, `LateInitializationError`, `StateError`
- Widget build errors (`setState() during build`, overflow, missing keys)
- First encounter with a bug — no prior investigation

## Workflow

1. **Parse** — extract symptom, affected widget/provider/service, stack trace, reproduction steps
2. **Investigate** — read affected files, trace call chain, grep related patterns. Check >=3 angles:
   - **State management** — provider scope, notifier lifecycle, stale refs
   - **Widget lifecycle** — initState/dispose/didChangeDependencies ordering
   - **Async** — unawaited futures, stream subscriptions, race conditions
   - **Widget tree** — key management, build context scope, overflow
3. **Propose** — present 2-3 numbered solutions with risk and effort:
   ```
   1. [Safest] Add mounted check before setState — Low risk, 5 min
   2. [Proper] Move subscription to ref.listen with autoDispose — Med risk, 15 min
   3. [Architectural] Restructure with AsyncNotifier — High risk, 1 hr
   ```
4. **Await** — user picks (never auto-apply)
5. **Fix** — apply minimally; run `dart analyze` on changed files
6. **Verify** — if symptom persists, loop back to step 1

## Common Runtime Bugs

| Bug Pattern | Typical Root Cause |
|-------------|-------------------|
| `Null check operator used on a null value` | Late/uninitialized field, wrong provider scope |
| `setState() called after dispose` | Missing `mounted` check, uncancelled async |
| `markNeedsBuild() called during build` | Synchronous state mutation in build method |
| `RenderFlex overflowed` | Missing `Expanded`/`Flexible`, unbounded constraints |
| `LateInitializationError` | Field read before assignment, wrong lifecycle hook |
| `Stream has already been listened to` | Broadcast stream needed, or duplicate listener |

## Rules

- Read the affected file before proposing fixes
- Run `dart analyze` after every code change
- Never apply a fix without user consent
- If 3 loops pass without resolution, escalate to Deep Mode
- Cite `file:line` for every finding

## Output

Diagnostic tree + interactive choice. Loops until resolved or escalated.
