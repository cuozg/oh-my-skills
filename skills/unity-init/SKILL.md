# unity-init

Generate a production-ready Unity project folder tree following the **ZenoGames Ten Crush pattern**: tiered assembly definitions, event-bus-first feature isolation, MVVM view controllers, optional shared SDK scaffold, asset-first docs.

## Scope

**Use when:** Starting a new Unity project, reorganizing a messy project, or scaffolding the canonical structure for a ZenoGames title.

**Switch out if:** Project already has an established structure and the user wants to add features (`unity-code`).

## Quick Start

```bash
python3 scripts/generate_structure.py \
  --company ZenoGames --project TenCrush \
  --sdk ZenoSDK \
  --features "Board,Match,Score,Goal,Audio,Input,Tile,VFX" \
  --ui-controllers "HUD,Popups" \
  --pipeline URP \
  --gitignore \
  --output-dir /path/to/UnityProject
```

Generates the full folder tree + every `.asmdef` + feature `README.md` + `AGENTS.md`. The project's own `CLAUDE.md` and the resulting tree should match — see "Verify Against CLAUDE.md" below.

## Workflow

1. **Gather** — collect or infer these inputs:
   - `--company` (namespace root, e.g. `ZenoGames`)
   - `--project` (game name, e.g. `TenCrush`)
   - `--features` (csv; default `Board,Match,Score,Goal,Audio,Input,Tile,VFX`)
   - `--ui-controllers` (csv; default `HUD,Popups`)
   - `--sdk` (optional, e.g. `ZenoSDK` → generates `Assets/_ZenoSDK/` scaffold)
   - `--pipeline` (`URP` | `URP2D` | `HDRP` | `Built-in`; default `URP`)
   - `--gitignore` (default off)
2. **Generate** — run the scaffold script (above).
3. **Apply** — creates directories, writes `.asmdef` files with correct references, optional `.gitignore`, `README.md` and `AGENTS.md` per feature.
4. **Verify** — confirm tree, check every `<X>.asmdef` compiles in Unity, then update the project's `CLAUDE.md` folder-structure table.

## What Gets Generated

```
Assets/
├── Scenes/                                # project-level (non-game)
├── Settings/
│   ├── Build Profiles/                    # per-platform build profiles
│   └── Scenes/                            # scene templates
├── Tests/
│   ├── EditMode/                          # Editor-only test asmdef
│   └── PlayMode/                          # PlayMode test asmdef
├── _<Project>/                            # game-specific (e.g. _TenCrush)
│   ├── Audio/  Fonts/  Shaders/  Sprites/  VFXs/
│   ├── Datas/{Events,Levels}/             # ScriptableObject data assets
│   ├── Editor/                            # editor-only scripts
│   ├── Prefabs/{GamePlay,Services,UI}/    # categorized prefabs
│   ├── Scenes/                            # game scenes
│   ├── Scripts/
│   │   ├── Bootstrap/                     # composition root
│   │   ├── Core/                          # foundation (no deps)
│   │   ├── Events/                        # foundation (no deps) — event bus
│   │   ├── Models/                        # data layer (refs Core)
│   │   ├── Systems/                       # cross-cutting services
│   │   ├── ViewModels/                    # MVVM (refs Core + Events)
│   │   ├── Features/<Name>/               # self-contained features
│   │   │   ├── Scripts/<X>.asmdef
│   │   │   ├── Tests/                     # per-feature test folder
│   │   │   ├── README.md
│   │   │   └── AGENTS.md
│   │   └── ViewControllers/<Name>/        # UI controllers (HUD, Popups)
│   ├── README.md  AGENTS.md
└── _<SDK>/                                # optional shared SDK (e.g. _ZenoSDK)
    ├── Scripts/{Core,Events}/
    └── Editor/
```

## Assembly Topology

All runtime asmdefs default to `autoReferenced: true`; tests to `autoReferenced: false` + `UNITY_INCLUDE_TESTS`.

```
Foundation (zero deps)
├─ ZenoGames.<Project>.Core
└─ ZenoGames.<Project>.Events            ← event bus; ONLY cross-feature channel

Data layer
└─ ZenoGames.<Project>.Models            → Core

Cross-cutting
└─ ZenoGames.<Project>.Systems           → Core, Events, Models

MVVM
└─ ZenoGames.<Project>.ViewModels        → Core, Events

Features (each isolated)
├─ ZenoGames.<Project>.Features.Audio    → Core, Events
├─ ZenoGames.<Project>.Features.Board    → Core, Events
├─ ...

UI ViewControllers
├─ ZenoGames.<Project>.ViewControllers.HUD    → Core, Events, ViewModels
├─ ZenoGames.<Project>.ViewControllers.Popups → Core, Events, ViewModels
└─ ZenoGames.<Project>.ViewControllers        → Core, Events, ViewModels, .HUD, .Popups

Composition root
└─ ZenoGames.<Project>.Bootstrap         → Core, Events, +features

Editor (includePlatforms: ["Editor"])
└─ ZenoGames.<Project>.Editor            → Core, Events, ViewModels, Models, *features

Tests
├─ ZenoGames.<Project>.EditMode.Tests    → Core, Events, ViewModels, *features (Editor)
└─ ZenoGames.<Project>.PlayMode.Tests    → Core, Events, ViewModels, Bootstrap, *features
```

**Hard rules baked into the generator:**
- `Core` and `Events` have zero internal deps.
- Every `Features.*` depends only on `Core` + `Events` — never on another feature.
- `ViewControllers.*` depend on `Core` + `Events` + `ViewModels`.
- `Bootstrap` is the only assembly that wires features together.
- `Editor` references everything (Editor-only build).

## Optional SDK Layer

Pass `--sdk ZenoSDK` to generate a parallel `Assets/_ZenoSDK/` skeleton with:
- `ZenoGames.ZenoSDK.Core` (zero deps)
- `ZenoGames.ZenoSDK.Events` (zero deps)
- `ZenoGames.ZenoSDK.Editor` (Editor-only, refs Core + Events)

Use this when the studio plans to share libraries across multiple titles.

## Project Rules

The skill assumes the project follows the Ten Crush `CLAUDE.md` rules:

- **NEVER use worktree** — work in place.
- **Asset-first:** create ScriptableObject data assets and prefabs before logic. Generator only emits the folder + asmdef skeleton; data assets are added by `unity-data`/`unity-prefab` later.
- **Per-feature docs:** every feature folder must include `README.md` (what + how) and `AGENTS.md` (gotchas). Generator creates both as stubs — replace before shipping.
- **Event-bus communication:** features never reference each other directly. Use `TenCrush.Events`.
- **No Resources/ Plugins/ folders** in the generated tree — Addressables and explicit imports only.

## Documentation Maintenance

After running this skill, update the project's `CLAUDE.md`:
- Add rows to the **Project Structure** table for any new `Datas/`, `Prefabs/`, or `Scripts/` subfolders.
- Update the **Assembly Definitions** diagram when adding/removing asmdefs.

## Verify Against CLAUDE.md

Before declaring done:
- [ ] Tree matches the project's `CLAUDE.md` structure table.
- [ ] Every `<X>.asmdef` has the expected `references[]` (no feature-to-feature links).
- [ ] Unity recompiles cleanly (`read_console` via MCP).
- [ ] Project opens without missing-assembly errors.

## Standards

For naming/convention specifics: load `unity-standards` skill.
For MCP asset tooling (creating actual prefabs/SOs): `unity-asset-generation` + `manage_asset action=create_folder`.
