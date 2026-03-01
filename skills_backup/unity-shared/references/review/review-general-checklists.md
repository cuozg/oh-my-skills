# General Review — PR Checklist

> Catch-all for cross-cutting concerns not covered by specialized review files.
> Cross-ref: `review-csharp.md` (code quality), `review-architecture-patterns.md` (coupling, SOLID), `review-asset-patterns.md` (performance), `code/security.md` (security deep-dive)

---

## PR Size Guide

| Size | Files | Risk | Review Strategy |
|------|-------|------|----------------|
| XS | 1–3 | Low | Single-pass review |
| S | 4–10 | Low–Med | File-by-file, check dependencies |
| M | 11–25 | Medium | Split by concern, verify integration points |
| L | 26–50 | High | Multi-reviewer, staged review, test plan required |
| XL | 50+ | Very High | Request split into smaller PRs |

---

## 🔴 Critical — Security

| Name | Issue | Fix |
|------|-------|-----|
| Secrets in Code | API keys, tokens, passwords hardcoded in source | Use environment variables, encrypted config, or Unity's `CloudProjectSettings` |
| SQL/Command Injection | User input passed directly to queries or `Process.Start` | Parameterize queries; validate/sanitize all external input |
| Insecure Deserialization | `BinaryFormatter` or unvalidated JSON from untrusted source | Use safe serializer (Newtonsoft with TypeNameHandling.None); validate schema |
| Debug Code in Build | `Debug.Log` floods, test cheats, god-mode flags in release | Guard with `#if UNITY_EDITOR` or `[Conditional("DEBUG")]`; strip in build |
| PlayerPrefs for Sensitive Data | Storing tokens/passwords in `PlayerPrefs` (plaintext on disk) | Use OS keychain, encrypted file, or server-side session |

> **Deep dive:** See `code/security.md` for full security implementation checklist.

## 🔴 Critical — Correctness

| Name | Issue | Fix |
|------|-------|-----|
| Race Condition | Shared state accessed from multiple threads/callbacks without sync | Use `lock`, `Interlocked`, `ConcurrentDictionary`, or confine to main thread |
| Off-by-One Error | Loop bounds, array index, or count calculation off by 1 | Verify boundary: `< length` not `<= length`; test empty and single-element cases |
| Uninitialized State | Field used before assignment — default value causes silent bug | Initialize in constructor/`Awake`; use `[field: SerializeField]` for required refs |
| Missing Null Check on External Data | Deserialized/loaded data assumed non-null | Validate after load: null-check, schema validation, fallback defaults |

## 🟡 Major — Testing

| Name | Issue | Fix |
|------|-------|-----|
| No Tests for New Logic | New feature has zero test coverage | Add unit tests for business logic; integration tests for system boundaries |
| Test Depends on Execution Order | Tests pass in isolation but fail when run together | Each test sets up and tears down its own state; no shared mutable state |
| Test Asserts on Implementation | Test checks internal method calls instead of behavior | Assert on outputs and observable side effects, not internal wiring |
| Flaky Test | Test passes 90% of the time — timing, randomness, or external dependency | Remove timing dependencies; mock externals; use deterministic seed |
| Missing Edge Case Tests | Only happy path tested — no empty, null, overflow, boundary cases | Add tests for: empty input, null, max/min values, concurrent access |

## 🟡 Major — Performance

| Name | Issue | Fix |
|------|-------|-----|
| Allocation in Update | `new`, `string concat`, LINQ, or `ToString()` in `Update()` | Pre-allocate, cache, use `StringBuilder`, or `NonAlloc` variants |
| Missing Object Pooling | `Instantiate`/`Destroy` called frequently (projectiles, particles, VFX) | Use object pool; return to pool instead of `Destroy` |
| Unbounded Collection Growth | `List<T>` grows forever without cleanup | Cap size, use ring buffer, or clear periodically |
| Physics Every Frame | `Raycast` or overlap query in `Update` instead of `FixedUpdate` | Move physics queries to `FixedUpdate`; cache results; use layer masks |
| Unoptimized LINQ in Hot Path | `.Where().Select().ToList()` in per-frame code — allocations per call | Use `for` loop with pre-allocated list; reserve LINQ for init/editor |

> **Deep dive:** See `quality-performance-checklist.md` for advanced CPU, memory, GPU, and physics optimization.

## 🔵 Medium — Lifecycle & Unity

| Name | Issue | Fix |
|------|-------|-----|
| Work in `Awake` Depending on Other Objects | `Awake` references another object that isn't initialized yet | Use `Start` for cross-object setup; `Awake` for self-init only |
| Missing `OnDisable`/`OnDestroy` Cleanup | Coroutines, events, or timers not cleaned up | Stop coroutines, unsubscribe events, cancel tokens in `OnDisable`/`OnDestroy` |
| `DontDestroyOnLoad` Leak | Object persists across scenes but accumulates duplicates | Check for existing instance in `Awake`; destroy duplicate |
| Coroutine Without Stop | `StartCoroutine` without `StopCoroutine` or `StopAllCoroutines` on disable | Track coroutine handle; stop in `OnDisable` |
| `[SerializeField]` on Wrong Type | Serializing `Dictionary`, interface, or abstract class (won't serialize) | Use `List<KeyValuePair>` for dicts; use concrete type or SO reference |

## 🔵 Medium — Documentation & Process

| Name | Issue | Fix |
|------|-------|-----|
| PR Missing Description | No context for reviewer — what changed and why | Add summary, motivation, testing steps, and screenshots if UI |
| Breaking Change Without Migration | API change breaks existing callers with no upgrade guide | Add `[Obsolete("Use X instead")]`, migration notes, or adapter |
| Missing Changelog Entry | User-facing change not documented | Add entry to CHANGELOG.md with version, change type, and description |

## 🟢 Minor

| Name | Issue | Fix |
|------|-------|-----|
| Inconsistent Code Style | Mixed brace style, spacing, or naming in same file | Run formatter (`dotnet format`); follow `.editorconfig` |
| Large Commit | Single commit with 20+ files changed across concerns | Split into atomic commits: one per logical change |
| Missing `.meta` File | New asset added without Unity `.meta` file in version control | Always commit `.meta` files alongside assets |
