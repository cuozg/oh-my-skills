---
name: unity-review-pr
description: "Expert Unity Developer code reviewer. Reviews PRs, commits, branches, or uncommitted changes with focus on Unity-specific patterns, performance, and best practices. Accepts Pull Request links as input. Use when: reviewing PRs, checking changes, comparing branches. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity Code Reviewer

Review code changes as an **expert Unity Developer**. Each issue → separate inline comment the author must resolve before merge.

## Output Requirement (MANDATORY)

> [!CAUTION]
> **MUST follow [REVIEW_TEMPLATE.md](.claude/skills/unity-review-pr/references/REVIEW_TEMPLATE.md) for output format — no variations.**
> All review logic, criteria, and decision rules live HERE — the template is output format only.

Submit using: `.claude/skills/unity-review-pr/scripts/post_review.sh <pr_number> /tmp/review.json`

## Input

| Input Type | Detection | Commands |
|:-----------|:----------|:---------|
| **No arguments** | Default | `git diff`, `git diff --cached`, `git status --short` |
| **Commit hash** | SHA or short hash | `git show <hash>` |
| **Branch name** | Branch identifier | `git diff <branch>...HEAD` |
| **PR URL/number** | Contains "github.com", "pull", or PR number | `gh pr view`, `gh pr diff` |

## Severity Guide

- **🔴 Critical**: Crash, data loss, memory leak, severe perf regression → blocks merge
- **🟡 Major**: Conditional failure, encapsulation break, subtle bugs → should fix before merge
- **🔵 Minor**: Style, conventions, minor improvements → nice to fix, not blocking

**Approval logic:** Any 🔴 → `REQUEST_CHANGES` · Only 🟡/🔵 → `COMMENT` · Clean → `APPROVE`

---

## Anti-Pattern Catalog

Every issue below: **Issue** | **Evidence** (what to grep for) | **Why** (impact) | **Fix** (concrete action).

### 🔴 Critical — Unity Performance

| Issue | Evidence | Why | Fix |
|:------|:---------|:----|:----|
| **GetComponent in hot path** | `GetComponent<T>()` inside `Update`/`FixedUpdate`/`LateUpdate` | Reflection-based lookup every frame; O(n) component search | Cache in `Awake`/`Start`: `private T _cached;` |
| **Camera.main in loop** | `Camera.main` in `Update`/`FixedUpdate` | Calls `FindGameObjectWithTag("MainCamera")` every access | Cache: `private Camera _cam; void Awake() => _cam = Camera.main;` |
| **Find in runtime** | `Find()`, `FindObjectOfType()`, `FindObjectsOfType()` in gameplay code | O(n) scene traversal per call; freezes on large scenes | Inject via `[SerializeField]` or service locator |
| **Instantiate/Destroy spam** | Frequent `Instantiate`/`Destroy` in gameplay loops (bullets, VFX, UI) | GC spikes from allocation + finalization; frame hitches | Object pooling: `ObjectPool<T>` or custom pool |
| **String concat in Update** | `string + string` or `$""` interpolation in hot paths | New `string` allocation every frame → GC pressure | `StringBuilder` or cache; avoid per-frame string ops |
| **Allocating in hot path** | `new List<>()`, `.ToList()`, `.ToArray()`, LINQ `.Where()`/`.Select()` in Update | Heap allocation every frame; GC spikes | Pre-allocate collections; use `NonAlloc` variants |

### 🔴 Critical — Async & Lifecycle

| Issue | Evidence | Why | Fix |
|:------|:---------|:----|:----|
| **Null after await** | `await` then use `this`/`gameObject`/any `UnityEngine.Object` without null check | Object may be destroyed during await → `MissingReferenceException` | Add `if (this == null) return;` after every `await` |
| **Coroutine orphan** | `StartCoroutine` without storing handle or stopping in `OnDisable` | Coroutine runs after disable/destroy → null refs, logic bugs | Store `Coroutine _cr;` → `StopCoroutine(_cr)` in `OnDisable` |
| **Event leak** | `+=` subscription without matching `-=` in `OnDisable`/`OnDestroy` | Memory leak; callbacks fire on destroyed objects → crashes | Subscribe in `OnEnable`, unsubscribe in `OnDisable` |
| **async void** | `async void` on non-Unity-event methods | Exceptions silently swallowed; can't await; crashes hard to diagnose | Use `async Task` or `async UniTask`; `async void` only for Unity events |

### 🔴 Critical — General

| Issue | Evidence | Why | Fix |
|:------|:---------|:----|:----|
| **Breaking API change** | Method/property signature changed (params added/removed/retyped) | All callers break at compile or runtime | Investigate callers first; add overload for backward compat |
| **NullReferenceException** | No null check on common code paths (deserialization, external data, collections) | Crash in production; hard to diagnose | Defensive null checks; `?.` and `??` operators |
| **Memory leak** | Resources, streams, native arrays, events not disposed/unsubscribed | Unbounded memory growth over session | `IDisposable`; `using` statements; clean up in `OnDestroy` |
| **Data corruption** | Serialization format change without migration; field type change | Existing saves/prefabs lose data silently | `[FormerlySerializedAs]`; migration code |
| **Race condition** | Shared mutable state from multiple threads/async paths | Non-deterministic behavior; intermittent crashes | Lock critical sections; thread-safe collections; single-writer |
| **Security vulnerability** | Unsanitized input, hardcoded secrets, API keys in source | Exploitable in production builds | Sanitize input; use env vars or encrypted config |

### 🟡 Major — Unity Specific

| Issue | Evidence | Why | Fix |
|:------|:---------|:----|:----|
| **SerializedField visibility flip** | `private` → `public` on `[SerializeField]` fields | Can break prefab serialization; exposes internals | Keep `[SerializeField] private`; add property if needed |
| **Missing FormerlySerializedAs** | Field renamed without `[FormerlySerializedAs("oldName")]` | Loses serialized data on existing prefabs/SOs | Add attribute before renaming |
| **DOTween not killed** | `DOTween.To()` / `.DOMove()` without `.Kill()` in `OnDisable`/`OnDestroy` | Tween runs after destroy → null ref, visual artifacts | `_tween?.Kill();` in `OnDisable` |
| **Lifecycle order violation** | Accessing sibling components in `Awake()` | `Awake` execution order not guaranteed across objects | Use `Start` for cross-component access; or Script Execution Order |
| **ScriptableObject mutation** | Modifying SO fields at runtime without `.Instantiate()` clone | Changes persist in Editor; affects all references | Clone: `var local = Instantiate(configSO);` |
| **Physics in Update** | `Physics.Raycast`, `OverlapSphere` in `Update` instead of `FixedUpdate` | Inconsistent results; physics on fixed timestep | Move to `FixedUpdate`; or use `Time.fixedDeltaTime` |

### 🟡 Major — General

| Issue | Evidence | Why | Fix |
|:------|:---------|:----|:----|
| **Potential NullReference** | Null possible under edge conditions (first frame, missing prefab, network timeout) | Crash in edge cases that pass basic testing | Null guards with meaningful error logging |
| **Visibility escalation** | `private` → `public` without justification | Breaks encapsulation; increases coupling surface | Keep private; expose via interface or read-only property |
| **Tight coupling** | Direct `GetComponent<OtherController>()` cross-system; concrete dependencies | Untestable; refactor cascades across systems | Events, interfaces, or ScriptableObject channels |
| **Missing error handling** | No try/catch around I/O, network, file, deserialization | Silent failures in production; data loss | Wrap in try/catch with logging; fallback behavior |
| **Incorrect conditional** | Off-by-one, wrong operator (`<` vs `<=`), inverted logic, missing `break` | Logic bugs that pass basic testing, fail edge cases | Review boundaries; add unit tests |
| **Resource not disposed** | `IDisposable` created without `using` or explicit `Dispose()` | Native resource leak (file handles, connections) | `using var x = ...;` or dispose in `finally` |

### 🔵 Minor

| Issue | Evidence | Why | Fix |
|:------|:---------|:----|:----|
| **Magic numbers** | Hardcoded `0.5f`, `100`, `"some_key"` without context | Intent unclear; hard to tune; scattered constants | `const`, `static readonly`, or `[SerializeField]` |
| **Debug.Log in production** | `Debug.Log/Warn/Error` not in `#if UNITY_EDITOR` or conditional | Perf cost in release builds; log spam | `#if UNITY_EDITOR` or logging framework |
| **Empty Unity callback** | Empty `Update()`, `Start()`, `OnGUI()` body | Unity still calls them → overhead | Delete empty callbacks |
| **Dead code** | Unreachable branches, unused variables, commented-out blocks | Maintenance burden; confusion | Remove or document |
| **Naming convention** | Breaks project PascalCase/camelCase/underscore rules | Inconsistent codebase; harder to navigate | Follow project conventions |
| **Excessive nesting** | 4+ levels of `if`/`for`/`while` | Hard to read, reason about, test | Early returns; extract methods; guard clauses |
| **Missing XML docs** | Public API without `/// <summary>` | Consumers can't understand intent | Add XML doc comments |
| **Implicit vector ops** | `transform.position.x = 5f;` (no-op; position is value type) | Silently does nothing; common Unity trap | `var pos = transform.position; pos.x = 5f; transform.position = pos;` |

---

## Investigation Patterns

**Never flag an issue without investigating callers/impact first.** Every 🔴 must include evidence (caller count, affected files). Every 🟡 must explain conditions under which the issue manifests.

### Method Signature Changes

Find all callers that will break:

```bash
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs"
grep -rn "\"MethodName\"" Assets/Scripts/ --include="*.cs"        # reflection
grep -rn "nameof(.*MethodName)" Assets/Scripts/ --include="*.cs"  # nameof
grep -rn "IInterfaceName" Assets/Scripts/ --include="*.cs"        # interface impls
```

**Report:**
```markdown
🔴 **Breaking Change**: `ClassName.MethodName` signature changed.
**Before**: `void MethodName(int x)` → **After**: `void MethodName(Vector3 position)`
**Callers requiring update** (N found):
| File | Line | Current Call |
|:-----|:-----|:-------------|
| Foo.cs | 42 | `MethodName(1)` |
```

### Event/Delegate Changes

```bash
grep -rn "EventName\s*+=" Assets/Scripts/ --include="*.cs"  # subscribers
grep -rn "EventName\s*-=" Assets/Scripts/ --include="*.cs"  # unsubscribers
grep -rn "EventName\s*+=\s*(" Assets/Scripts/ --include="*.cs"  # lambda (can't unsub)
```

**Report:**
```markdown
🔴 **Breaking Change**: Event `ClassName.EventName` signature changed.
**Subscribers affected** (N found):
| File | Line | Subscription |
|:-----|:-----|:-------------|
| Bar.cs | 15 | `EventName += OnEvent` |
**Unsubscribe check**: [All have matching `-=` | Missing in N files]
```

### Serialization Changes

```bash
grep -rn "TypeName" Assets/ --include="*.asset"    # SO references
grep -rn "TypeName" Assets/ --include="*.prefab"   # prefab references
grep -rn "\[SerializeField\]" Assets/Scripts/ChangedFile.cs
grep -rn "\[SerializeReference\]" Assets/Scripts/ChangedFile.cs
```

**Report:**
```markdown
🟡 **Serialization Risk**: Field `score` renamed to `playerScore` without migration.
\`\`\`suggestion
[FormerlySerializedAs("score")]
public int playerScore;
\`\`\`
```

### Inheritance/Interface Changes

```bash
grep -rn ":\s*BaseClassName" Assets/Scripts/ --include="*.cs"
grep -rn ":\s*.*IInterfaceName" Assets/Scripts/ --include="*.cs"
```

### Prefab/Scene References

```bash
grep -rn "m_Script:.*ComponentGUID" Assets/ --include="*.prefab"
grep -rn "m_Script:.*ComponentGUID" Assets/ --include="*.unity"
```

---

## Workflow

### Phase 1: Fetch Changes

```bash
# PR
gh pr diff <number> --patch
gh pr view <number> --json title,body,files

# Uncommitted
git diff && git diff --cached && git status --short
```

### Phase 2: Investigate Codebase

**Delegate to subagent** — understand patterns, not just diffs.

Use `@explore` or `@librarian` to:
- Read full files for context around changed lines
- Find callers of changed methods (Investigation Patterns above)
- Trace event subscribers; verify unsubscribe pairs
- Check for similar patterns elsewhere needing the same fix
- Identify breaking change impact (signatures, serialization, interfaces)
- Verify Unity lifecycle correctness (Awake → OnEnable → Start order)

**Priority investigation order:**
1. Method signature changes → find all callers
2. Event/delegate changes → find all subscribers
3. Serialized field changes → check prefabs/assets
4. Inheritance changes → check all derived types
5. Public API changes → check cross-assembly impact

### Phase 3: Generate Acceptance Criteria

Analyze PR changes → create testable acceptance criteria by category:

- **UI Verification**: Layout, rendering, animation, responsive behavior
- **Functional Verification**: Feature logic, edge cases, error handling
- **Performance Verification**: Frame drops, memory, GC spikes, load times
- **Data Verification**: Save migration, serialization, config values, no breaking changes

Each criterion must reference actual classes, methods, and scenarios from the PR.

### Phase 4: Create Review JSON

Build `/tmp/review.json` per **[REVIEW_TEMPLATE.md](.claude/skills/unity-review-pr/references/REVIEW_TEMPLATE.md)**.

1. Write summary body with PR number, scope, assessment, acceptance criteria
2. Count issues by severity: 🔴 Breaking · 🟡 Potential · 🔵 Quality
3. One `comments` entry per issue — never combine
4. Each comment: `path`, `line` (right side of diff), `side: "RIGHT"`, `body` (formatted per template)
5. Include `suggestion` code blocks for actionable fixes
6. Add Impact Analysis (files investigated, breaking call sites found)

**Line number rules:** Use right-side line number. For deleted lines, use last line of surrounding context. `side` always `"RIGHT"`.

### Phase 5: Submit

```bash
.claude/skills/unity-review-pr/scripts/post_review.sh <pr_number> /tmp/review.json
```

Verify submission succeeds. If it fails, check: valid JSON, correct PR number, line numbers exist in diff.

**Fallback for merged/closed PRs:**
```bash
gh pr comment <number> --body "## Post-Merge Review\n\n<body>"
```

**Fallback for API errors:**
```bash
gh api -X POST -H "Accept: application/vnd.github+json" \
  repos/{owner}/{repo}/pulls/{pr_number}/reviews \
  -f body="[REVIEW BODY]" -f event="COMMENT"
```

---

## Critical Rules

### ✅ Always

1. Follow [REVIEW_TEMPLATE.md](.claude/skills/unity-review-pr/references/REVIEW_TEMPLATE.md) for output format
2. Apply ALL review criteria from Anti-Pattern Catalog — Unity patterns first
3. Generate Acceptance Criteria based on PR changes
4. Submit using `post_review.sh` — verify posted successfully
5. Each issue = separate `comments` entry
6. Submit even if PR is merged/closed

### ❌ Never

1. Deviate from REVIEW_TEMPLATE.md output format
2. Skip Acceptance Criteria section
3. Combine multiple issues into one comment
4. Skip GitHub submission
5. Flag issues without investigating callers/impact
6. Miss Unity-specific patterns (Update allocations, async safety, lifecycle)

**Review is incomplete until each issue is a resolvable comment on GitHub.**

---

## MCP Tools Integration

Optionally verify compilation and runtime behavior after reviewing code changes.

| Operation | MCP Tool | Use Case |
| --------- | -------- | -------- |
| Check compilation | `coplay-mcp_check_compile_errors` | Verify PR changes compile cleanly |
| Read console | `coplay-mcp_get_unity_logs(show_errors=true)` | Check for runtime errors post-merge |
| Play/stop game | `coplay-mcp_play_game` / `coplay-mcp_stop_game` | Smoke-test PR changes in Editor |
| Inspect hierarchy | `coplay-mcp_list_game_objects_in_hierarchy()` | Verify scene structure changes |
| Get object details | `coplay-mcp_get_game_object_info(gameObjectPath="...")` | Validate component/property changes |

### Post-Review Verification (Optional)

```
1. coplay-mcp_check_compile_errors         → confirm PR compiles
2. coplay-mcp_get_unity_logs(show_errors=true) → check for warnings/errors
3. coplay-mcp_play_game                    → smoke-test if needed
4. coplay-mcp_stop_game                    → end test session
```
