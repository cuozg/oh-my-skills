# Naming Conventions — Unity C#

## Casing Rules

| Element          | Style          | Example                        |
|------------------|----------------|--------------------------------|
| Class/Struct     | PascalCase     | `PlayerController`             |
| Interface        | I + PascalCase | `IDamageable`                  |
| Method           | PascalCase     | `TakeDamage()`                 |
| Property         | PascalCase     | `CurrentHealth`                |
| Public field     | camelCase      | (avoid — use SerializeField)   |
| Private field    | _camelCase     | `_moveSpeed`                   |
| Parameter        | camelCase      | `hitPoint`                     |
| Constant         | PascalCase     | `MaxHealth`                    |
| Enum type        | PascalCase     | `WeaponType`                   |
| Enum value       | PascalCase     | `WeaponType.Melee`             |
| Event            | PascalCase     | `OnDeath`                      |
| Local var        | camelCase      | `elapsed`                      |
| Bool field/prop  | is/has/can     | `_isGrounded`, `HasAmmo`       |

## Namespace Convention

```
CompanyName.ProjectName.Feature
```

Match what exists in project. If nothing exists, use `Game.Feature`.

## Folder → Namespace Mapping

```
Assets/Scripts/Player/       → Game.Player
Assets/Scripts/UI/           → Game.UI
Assets/Scripts/Data/         → Game.Data
Assets/Scripts/Systems/      → Game.Systems
Assets/Scripts/Utilities/    → Game.Utilities
```

## File Naming

- One class per file (exceptions: nested private classes, related enums)
- File name = class name: `PlayerController.cs`
- Interface files: `IDamageable.cs`
- SO data: `ItemData.cs`
- SO events: `VoidEventChannel.cs`

## Field Order in Class

```
1. Constants / static readonly
2. [SerializeField] private fields
3. Private fields (non-serialized)
4. Public properties
5. Unity lifecycle (Awake → OnEnable → Start → Update → FixedUpdate → LateUpdate → OnDisable → OnDestroy)
6. Public methods
7. Private methods
```

## Common Abbreviations (acceptable)

```
rb   → Rigidbody         col  → Collider
sr   → SpriteRenderer    anim → Animator
cam  → Camera            nav  → NavMeshAgent
dir  → direction         pos  → position
vel  → velocity          btn  → Button
```
