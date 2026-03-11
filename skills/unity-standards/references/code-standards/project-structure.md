# Project Folder Structure

## Layout Strategy

Use **feature-based** organization. Keep related assets together so features are self-contained and portable.

```
Assets/
├── _Project/                    # underscore prefix → sorts to top
│   ├── Core/                    # interfaces, base classes, shared data
│   │   ├── Scripts/             # Company.Project.Core.asmdef
│   │   └── Tests/               # Company.Project.Core.Tests.asmdef
│   ├── Features/
│   │   ├── Player/
│   │   │   ├── Scripts/         # Company.Project.Player.asmdef
│   │   │   ├── Prefabs/
│   │   │   ├── Animations/
│   │   │   ├── Art/
│   │   │   └── Tests/           # Company.Project.Player.Tests.asmdef
│   │   └── Combat/
│   │       ├── Scripts/         # Company.Project.Combat.asmdef → refs Core
│   │       └── Tests/
│   ├── Infrastructure/          # DI installers, bootstrapping, scene management
│   │   └── Scripts/             # Company.Project.Infrastructure.asmdef → refs Core + features
│   ├── UI/                      # shared UXML, USS, UI controllers
│   ├── Settings/                # ScriptableObject configs, InputActions, render pipeline
│   ├── Art/                     # shared materials, shaders, textures
│   ├── Audio/                   # shared SFX, music, mixer assets
│   └── Scenes/
├── Plugins/                     # 3rd-party (Odin, DoTween, etc.)
└── Resources/                   # AVOID — use Addressables instead
```

## Assembly Definitions

| Assembly | References | Purpose |
|----------|-----------|---------|
| `Company.Project.Core` | none | interfaces, enums, data, events |
| `Company.Project.{Feature}` | Core | feature runtime code |
| `Company.Project.Infrastructure` | Core + features | DI wiring, bootstrapping |
| `Company.Project.{Feature}.Editor` | feature + Core | editor tooling for feature |
| `Company.Project.{Feature}.Tests` | feature + NUnit | test assemblies |

- Name = namespace: `Company.Project.Feature` → folder `Features/Feature/Scripts/`
- Set `autoReferenced: false` on all except top-level game assembly
- No circular dependencies — route through Core interfaces
- Test assemblies: check "Test Assemblies" toggle, reference NUnit + target assembly

## Special Folders

| Folder | Behavior |
|--------|----------|
| `Editor/` | excluded from builds, `UnityEditor` API access |
| `Resources/` | included in build, loaded via `Resources.Load` — avoid, use Addressables |
| `StreamingAssets/` | copied raw to device — videos, databases, initial configs |
| `Plugins/` | native libs (.dll/.so), compiled before project scripts |
| `Gizmos/` | icons for `Gizmos.DrawIcon()` |

## Namespace Convention

```
Company.Project.Feature
```

Map 1:1 to folder path. If folder moves, namespace moves.

```csharp
// Assets/_Project/Features/Combat/Scripts/DamageCalculator.cs
namespace Company.Project.Combat
{
    public class DamageCalculator { }
}
```

## .gitignore Essentials

```gitignore
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
[Ll]ogs/
[Uu]tmp/
[Mm]emoryCaptures/
.vs/
.idea/
*.csproj
*.sln
.DS_Store
```

## Rules

- Feature-based over type-based — keeps features portable
- Every script folder gets an `.asmdef` — prevents monolithic recompilation
- `_Project/` prefix keeps project code above Unity-generated folders
- `Settings/` for all ScriptableObject configs — not buried in `Resources/`
- `Editor/` folders can exist at any depth — Unity detects them automatically
- Never put runtime code in `Editor/` or reference Editor assemblies from runtime
