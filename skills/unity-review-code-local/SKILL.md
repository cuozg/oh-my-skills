---
name: unity-review-code-local
description: "Deep logic review for Unity C# code in the local project. Reviews code changes with surgical focus on logic correctness, edge cases, state management, data flow, and concurrency — then adds review comments directly into the code as inline comments. No report document. No GitHub interaction. Input: commit hash, commit range, branch diff, or a feature/logic description to review. Use when: reviewing logic before commit, validating a feature implementation, auditing business logic, tracing data flow for correctness, reviewing a specific commit. Triggers: 'review code', 'review logic', 'check this logic', 'review commit', 'review my changes', 'logic review', 'code review', 'review this feature'."
---

# Unity Logic Reviewer (Local)

Deep logic review for the local project. Comments go directly into the code as inline comments — no report document, no GitHub interaction.

## Input → Diff Command

| Input | Command |
|:------|:--------|
| None (default) | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Commit range | `git diff <base>..<head>` |
| Branch | `git diff <branch>...HEAD` |
| Feature/logic request | User describes what to review → find relevant files via grep/LSP |

## Severity

| Severity | Meaning | Action |
|:---------|:--------|:-------|
| 🔴 Critical | Crash, data loss, security, logic that produces wrong results | Must fix |
| 🟡 Major | Logic bugs, missing edge cases, state corruption risk | Should fix |
| 🔵 Minor | Simplification, clearer intent, defensive coding | Fix or acknowledge |

## Load References

Always load:
- [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md) — how to write and place inline review comments
- [VERIFICATION_GATES.md](references/VERIFICATION_GATES.md) — evidence requirements

## Code Standards Enforcement (MANDATORY)

**ALWAYS** load the `unity-code-standards` skill (`use_skill("unity-code-standards")`) before any review. This is the **sole source** for all logic review patterns, C# quality gates, and architecture standards. Non-negotiable.

The `unity-code-standards` skill provides:
- **Logic review patterns** — control flow, state management, data flow, concurrency, Unity-specific gotchas, edge cases (`references/review/logic-review-patterns.md`)
- **Architecture review** — dependency management, event architecture, data flow patterns (`references/review/architecture-review.md`)
- **C# quality gates** — nullable, access modifiers, logging, exceptions, modern C# (`references/review/csharp-quality.md`)
- **Performance review** — allocations, hot paths, component caching (`references/review/performance-review.md`)
- **Unity specifics** — lifecycle, serialization, async patterns (`references/review/unity-specifics.md`)

Apply all findings as inline review comments using the same format from [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md).

## Workflow

1. **Fetch** — Get the diff (see Input table). For feature/logic requests, identify files first via grep/LSP.

2. **Read full context** — For each changed file, read the **entire file** (not just the diff). Logic bugs hide in what surrounds the change.

3. **Deep investigate** (parallel, `run_in_background=true`) — spawn agents to gather evidence.

   **`@explore` agents (2-3):**

   | Agent | Task |
   |:------|:-----|
   | Call-site analysis | For each modified public method/property: find ALL callers, count call sites, identify which pass null/edge values. |
   | State flow | Trace state transitions: what sets each field, what reads it, can it be in an invalid state between set and read? |
   | Data contract | Check serialization, API boundaries, event payloads — does the data shape match all consumers? |

4. **Logic review** — Apply review references against evidence. Focus areas:

   **Control flow:**
   - Every `if` branch: what happens in the else? Is the else path even possible?
   - Every loop: can it infinite-loop? Off-by-one? Empty collection?
   - Every early return: does it skip cleanup that should happen?
   - Every switch: missing cases? Fall-through intentional?

   **State management:**
   - Field mutations: who else reads this field? Will they see a consistent state?
   - Init order: can this be called before initialization completes?
   - Lifetime: can this reference outlive the object it points to?

   **Data flow:**
   - Input validation: what values can arrive? Are all handled?
   - Null propagation: if A is null, does the chain handle it or crash 3 calls deep?
   - Type safety: any unsafe casts, enum-to-int conversions, implicit narrowing?

   **Edge cases:**
   - Zero, null, empty, max, negative, duplicate, concurrent
   - First call vs subsequent calls
   - Normal path vs error recovery path

   **Unity Lifecycle Verification:**
   - For EVERY `MonoBehaviour` in the diff, verify full lifecycle coverage
   - What is initialized in `Awake` vs `Start`? Any cross-component access in `Awake`?
   - Are `OnEnable`/`OnDisable` balanced? (subscribe/unsubscribe, register/deregister)
   - Are coroutines stopped in `OnDisable`?
   - Are DOTween animations killed in `OnDisable`/`OnDestroy`?
   - Is there cleanup in `OnDestroy` for native resources?
   - If `DontDestroyOnLoad`: is there a duplicate guard?
   - If `[ExecuteAlways]`: are Editor and Play mode paths properly split?

   **Serialization Safety Check:**
   - For any changed `[SerializeField]`, `[Serializable]`, or public field, verify migration safety
   - Was the field renamed? -> add `[FormerlySerializedAs]`
   - Was the type changed? -> require migration path or explicit data reset strategy
   - Was a field added to a ScriptableObject? -> validate safe defaults
   - Was a field removed? -> verify prefabs/SOs do not still depend on serialized data
   - Is the field interface/abstract? -> Unity default serializer needs `[SerializeReference]` or concrete type

   **Memory Safety Audit:**
   - Any `new` inside `Update`/`LateUpdate`/`FixedUpdate`? (per-frame allocation)
   - Any event `+=` without corresponding `-=`?
   - Any `Addressables.LoadAssetAsync` without `Release` ownership?
   - Any `UnityWebRequest` without `using`/`Dispose`?
   - Any texture/mesh created at runtime without `Destroy`?
   - Any static collections that grow without clear/reset?
   - Any delegate/lambda capturing `this` in long-lived context?

5. **Add inline comments** — Per [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md):
   - Use `edit` to insert pro-format review comments directly into source files
   - **Full box format** for 🔴 Critical and 🟡 Major issues:
     ```
     // ╔══════════════════════════════════════════════════════════════
     // ║ REVIEW [SEVERITY]: Problem Title
     // ╟──────────────────────────────────────────────────────────────
     // ║ WHY:  [root cause]
     // ║ WHERE: [evidence — callers, files, data flow]
     // ║ FIX:  [concrete code fix]
     // ╚══════════════════════════════════════════════════════════════
     ```
   - **Quick format** for 🔵 Minor or self-evident issues:
     ```
     // ⚠ REVIEW [🔵 MINOR]: Problem → fix suggestion.
     ```
   - Every comment MUST have: problem name, WHY, and FIX
   - Batch pattern: full box on first, `// ⚠ REVIEW` back-ref on rest

6. **Summarize** — After all comments are placed, give a short verdict to the user:
   - Count of findings by severity
   - List of files modified with comments
   - Top 3 most important issues

## Comment Placement Rules

- **Add** review comments into actual source files using `edit`
- **Never** create a separate report document
- **Never** modify the actual logic — only add review comments
- One issue = one comment. Don't combine.
- Same issue in N places → full box on first, `// ⚠ REVIEW` back-ref on rest
- 🔴 and 🟡 → full box format (╔/╟/╚ borders)
- 🔵 → quick single-line format (⚠ prefix)

## Evidence Rules

- 🔴 needs: caller count + affected files + reproduction scenario
- 🟡 needs: trigger conditions + what state leads to the bug
- 🔵 needs: brief explanation of why current code is suboptimal
- **Never flag without evidence. Investigate before commenting.**

## Rules

- ✅ Read the full file, not just the diff. Logic bugs need context.
- ✅ Trace data flow end-to-end. Follow the value from source to sink.
- ✅ Check what happens when assumptions are violated (null, empty, concurrent, out-of-order).
- ✅ Verify event subscribe/unsubscribe pairs. Check lifecycle ordering.
- ✅ For each branch/path: "Can this state actually occur? What happens if it does?"
- ✅ When reviewing MonoBehaviour lifecycle, check the FULL lifecycle (`Awake -> OnEnable -> Start -> Update -> OnDisable -> OnDestroy`), not just the changed method.
- ✅ Check dependency injection approach and consistency — injection patterns differ from manual singleton access.
- ✅ For async code, verify the project's async convention: UniTask vs Awaitable vs raw Task.
- ✅ For each allocation in changed code, ask: "How often is this called per frame?"
- ❌ Never flag style-only issues (naming, formatting) as 🔴 or 🟡.
- ❌ Never suggest behavioral changes beyond the flagged issue.
- ❌ Never skip the investigation step. No comment without evidence.
- ❌ Never downgrade severity because the fix is complex. Severity reflects impact, not fix difficulty.
