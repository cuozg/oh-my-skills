# General Review Checklists

Technology-agnostic checklists. Apply alongside Unity-specific references (LOGIC_REVIEW, PREFAB_REVIEW, ASSET_REVIEW).

## PR Size → Checklist Focus

| Changed Lines | Focus |
|:--------------|:------|
| < 50 | Security + Correctness + Testing only |
| 50–300 | All 6 checklists |
| > 300 | Request split. If not possible, prioritize Security + Correctness. Note scope risk in summary. |

## Checklists

### 🔒 Security
- [ ] No hardcoded secrets, API keys, tokens, passwords
- [ ] User input validated and sanitized before use
- [ ] No SQL/command/path injection vectors
- [ ] Auth checks present on protected operations
- [ ] Sensitive data not logged or exposed in error messages
- [ ] Deserialization uses safe patterns (no `BinaryFormatter`)
- [ ] Auth/session tokens are not stored in insecure `PlayerPrefs`
- [ ] Save files with sensitive/user-owned data are encrypted or tamper-protected
- [ ] Debug/admin/test endpoints are gated or removed from production builds

### ✅ Correctness
- [ ] Logic matches stated intent (PR title/body/ticket)
- [ ] State transitions are valid — no impossible states
- [ ] Data integrity maintained (no partial writes, no orphaned refs)
- [ ] API contracts honored (parameters, return types, nullability)
- [ ] Error paths handled — no swallowed exceptions, no silent failures
- [ ] Concurrency safe — no race conditions in async/threaded code
- [ ] Scene/prefab references are valid (no missing scripts/components)
- [ ] Addressable labels/keys referenced in code exist in groups
- [ ] Assembly definition references are complete for moved/new types

### 🧪 Testing
- [ ] New public API has corresponding tests
- [ ] Modified logic has updated tests
- [ ] Edge cases covered (null, empty, boundary values, overflow)
- [ ] No test code in production paths
- [ ] Tests are deterministic — no flaky timing or order dependencies
- [ ] Play Mode tests cover async/coroutine and scene lifecycle flows
- [ ] Edit Mode tests cover serialization/deserialization compatibility
- [ ] Tests do not leave `Debug.Log`/warning/error spam in normal pass flow

### 🧹 Code Quality
- [ ] Single Responsibility — each method/class does one thing
- [ ] Methods < 30 lines, nesting < 4 levels
- [ ] No copy-paste duplication across files
- [ ] Magic numbers extracted to named constants
- [ ] Naming is clear and consistent with codebase conventions
- [ ] Dead code removed (unused variables, unreachable branches)

### ⚡ Performance
- [ ] No allocations in hot paths (Update, FixedUpdate, tight loops)
- [ ] No N+1 query patterns or repeated expensive operations
- [ ] Memory lifecycle clear — no leaks from event subscriptions or references
- [ ] Appropriate data structures (Dictionary vs List for lookups, etc.)
- [ ] Async operations don't block the main thread
- [ ] Shader variant stripping configured for target build platforms
- [ ] Texture streaming enabled/tuned for large texture sets
- [ ] Audio clip load type/compression strategy matches playback usage

### 🔄 Lifecycle
- [ ] `OnEnable`/`OnDisable` subscription pairs are symmetric
- [ ] Awake initialization does not depend on other components being ready
- [ ] Scene transition cleanup exists (unsubscribe, stop coroutines, kill tweens)
- [ ] Singleton/service access guarded for null during teardown
- [ ] Quit flow handles `OnApplicationQuit` vs `OnDestroy` ordering safely

### 📚 Documentation
- [ ] Public API has XML doc comments
- [ ] Complex logic has inline comments explaining "why"
- [ ] Breaking changes documented in PR description
- [ ] Removed/deprecated API has migration guidance
