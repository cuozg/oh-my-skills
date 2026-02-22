# Anti-Patterns

**NEVER do these:**

| Anti-Pattern                   | Required Pattern                                         |
| ------------------------------ | -------------------------------------------------------- |
| `Debug.Log` in runtime code      | `ILogger` injected via constructor                         |
| `static Instance` singleton      | Dependency injection                                     |
| `async void`                     | `async UniTask` or `async UniTaskVoid`                       |
| `async Task`                     | `async UniTask` (allocation-free)                          |
| `StartCoroutine` for new code    | `async UniTask` with CancellationToken                     |
| Field injection on POCO classes  | Constructor injection                                    |
| `FindObjectOfType` / `Find`        | `[SerializeField]` or dependency injection                 |
| `GetComponent` in Update         | Cache in Awake                                           |
| `new List<>()` / LINQ in Update  | Pre-allocate; manual loops in hot paths                  |
| Logging in constructors        | Move to `Initialize()` or first use                        |
| `this.logger?.Method()`          | `this.logger.Method()` (DI guarantees non-null)            |
| `catch (Exception) { }`          | Catch specific; let `OperationCanceledException` propagate |
| Mutable event arg structs      | `readonly record struct`                                   |
| Lambda event subscribers       | Named method (so you can unsubscribe)                    |

## When Singletons Are Acceptable

Only as **last resort** when dependency injection is not available (e.g., bootstrapping before DI container exists). Document WHY.
