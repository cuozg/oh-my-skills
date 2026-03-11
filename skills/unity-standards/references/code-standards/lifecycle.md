# Unity Lifecycle

## Execution Order

```
Awake()           — first call, once per instance
OnEnable()        — each time object becomes active
Start()           — before first Update, after all Awake
  ┌─ FixedUpdate()   — physics tick (default 50Hz)
  │  Update()        — every frame
  │  LateUpdate()    — after all Updates (camera follow here)
  └─ repeat
OnDisable()       — each time object becomes inactive
OnDestroy()       — when destroyed or scene unloads
```

## Awake vs Start

```csharp
public sealed class Enemy : MonoBehaviour
{
    Rigidbody _rb;
    HealthBar _healthBar;

    void Awake() => _rb = GetComponent<Rigidbody>(); // self-init only

    void Start()
    {
        _healthBar = FindObjectOfType<HealthBar>(); // cross-object refs
        _healthBar.Bind(this);
    }
}
```

| Use | Awake | Start |
|-----|-------|-------|
| GetComponent | ✅ | ✅ |
| Cross-object refs | ❌ | ✅ |
| Called if disabled | ✅ | ❌ |
| Order guarantee | None | After all Awake |

## FixedUpdate for Physics

```csharp
// ✅ Physics in FixedUpdate — deterministic
void FixedUpdate()
{
    _rb.AddForce(Vector3.up * _thrust);
    _rb.MovePosition(_rb.position + _velocity * Time.fixedDeltaTime);
}

// ❌ Physics in Update — frame-rate dependent
void Update() { _rb.AddForce(Vector3.up * _thrust); }
```

## Subscribe Pattern — OnEnable/OnDisable

```csharp
void OnEnable()
{
    _health.OnDeath += HandleDeath;
    InputActions.Player.Jump.performed += OnJump;
}

void OnDisable()
{
    _health.OnDeath -= HandleDeath;
    InputActions.Player.Jump.performed -= OnJump;
}
```

## Coroutine Lifecycle

```csharp
Coroutine _moveRoutine;
void StartMoving()
{
    if (_moveRoutine != null) StopCoroutine(_moveRoutine);
    _moveRoutine = StartCoroutine(MoveRoutine());
}
IEnumerator MoveRoutine()
{
    while (Vector3.Distance(transform.position, _target) > 0.1f)
    {
        transform.position = Vector3.MoveTowards(transform.position, _target, _speed * Time.deltaTime);
        yield return null;
    }
}
// Stops when: object disabled, destroyed, or StopCoroutine
```

<!-- Advanced: lifecycle-advanced.md -->
