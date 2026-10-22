---
name: unity-init
description: >
  Scaffold or reorganize a Unity 6 project — folder tree, tiered assembly definitions
  (Core/Events/Models/Systems/ViewModels/Features/ViewControllers/Bootstrap/Editor/Tests),
  per-feature README/AGENTS docs, optional shared SDK, and a root CLAUDE.md agent guide with
  mandatory unity-cli and unity-skill rules. Use when the user says "init Unity project",
  "set up project structure", "scaffold asmdefs", "add CLAUDE.md for this Unity project", or
  "reorganize folders". Do not use to add gameplay code to an established structure
  (unity-standards) or to create the Unity project itself (unity:new-unity-project).
metadata:
  author: kuozg
  version: "2.0"
---
# unity-init

Generate a production-ready folder tree + asmdef topology for any Unity 6 project, and write a
root `CLAUDE.md` that tells agents how to work in it. All names come from the project or user
input — nothing is game-specific.

## Workflow

### 1. Preflight
- No Unity project yet → create it first (`unity:new-unity-project`, or `unity projects create` via `unity:unity-cli`), then continue.
- Confirm the target root contains `ProjectSettings/` and `Assets/`.
- Run `unity status --format json` (see `../unity-standards/references/other/unity-cli-routing.md`) to learn whether an Editor has the project open — needed for Step 5.

### 2. Gather inputs
Auto-detected from the target when omitted — state what was detected:

| Flag | Default |
|---|---|
| `--company` | `ProjectSettings.asset` → `companyName` (sanitized to a C# identifier) |
| `--project` | `ProjectSettings.asset` → `productName` (sanitized) |
| `--pipeline` | `auto` → from `Packages/manifest.json` (`URP` / `URP2D` / `HDRP` / `Built-in`) |
| `--unity-version` | `ProjectSettings/ProjectVersion.txt` |
| `--features` | none — ask the user for the feature list (csv) |
| `--ui-controllers` | none — ask (csv, e.g. screens/HUD groups) |
| `--sdk` | none — only when the studio shares code across titles |
| `--gitignore` | off — skipped if a `.gitignore` exists |
| `--no-claude-md` | off — CLAUDE.md is written by default |

Ask only for what cannot be detected (features, controllers, SDK). Do not invent feature names.

### 3. Dry run → confirm
```bash
python3 scripts/generate_structure.py --output-dir <project-root> \
  --features "<csv>" --ui-controllers "<csv>" [--sdk <Name>] [--gitignore] --dry-run
```
(`scripts/` is relative to this skill's base directory.) Show the user the `detected` values and
the tree; wait for confirmation before writing.

### 4. Apply
Re-run without `--dry-run`. The script:
- creates missing directories and files only — existing files are reported in `skipped`, never overwritten;
- writes `CLAUDE.md` as a managed block between `<!-- unity-init:begin ... -->` and
  `<!-- unity-init:end -->`: creates the file, appends to an existing one, or replaces only the
  block on re-runs. User content outside the block is preserved.

### 5. Verify (BLOCKING)
- [ ] Tree matches the `CLAUDE.md` Project Structure table.
- [ ] Every `.asmdef` `references[]` points at a generated assembly; no feature→feature links.
- [ ] Unity compiles cleanly: live Editor → `unity command recompile` + console scan for `error CS`
      (pass `--caller plugin --skill unity-init`); no Editor → `unity open .`, wait for `ready`, then check.
      If the CLI cannot connect, check Safe Mode (`unity pipeline list`) before anything else.
- [ ] `CLAUDE.md` block present once; user content outside it unchanged.
- [ ] Report `created` / `updated` / `skipped` counts and anything not verified.

## What Gets Generated

```
CLAUDE.md                                  # managed agent-guide block (facts, MANDATORY rules, how-to)
Assets/
├── Scenes/                                # project-level (non-game)
├── Settings/
│   ├── Build Profiles/                    # per-platform build profiles (unity build --profile)
│   └── Scenes/                            # scene templates
├── Tests/
│   ├── EditMode/                          # Editor-only test asmdef
│   └── PlayMode/                          # PlayMode test asmdef
├── _<Project>/                            # game-specific root
│   ├── Audio/  Fonts/  Shaders/  Sprites/  VFXs/
│   ├── Datas/{Events,Levels}/             # ScriptableObject data assets
│   ├── Editor/                            # editor-only asmdef
│   ├── Prefabs/{GamePlay,Services,UI}/
│   ├── Scenes/
│   ├── Scripts/
│   │   ├── Bootstrap/  Core/  Events/  Models/  Systems/  ViewModels/
│   │   ├── Features/<Name>/{Scripts/<asmdef>, Tests/, README.md, AGENTS.md}
│   │   └── ViewControllers/<Name>/Scripts/<asmdef>
│   └── README.md  AGENTS.md
└── _<SDK>/                                # optional shared SDK (Core, Events, Editor)
```

## Assembly Topology

Namespace root `<Company>.<Project>`. Runtime asmdefs `autoReferenced: true`; tests
`autoReferenced: false` + `UNITY_INCLUDE_TESTS` + `nunit.framework.dll`.

```
Core, Events                 → (none)            ← Events = ONLY cross-feature channel
Models                       → Core
Systems                      → Core, Events, Models
ViewModels                   → Core, Events
Features.<Name>              → Core, Events
ViewControllers.<Name>       → Core, Events, ViewModels
ViewControllers              → Core, Events, ViewModels, every ViewControllers.<Name>
Bootstrap                    → Core, Events, every generated feature   (composition root)
Editor  [Editor only]        → Core, Events, ViewModels, Models, every feature
EditMode.Tests [Editor only] → Core, Events, ViewModels, every feature
PlayMode.Tests               → Core, Events, ViewModels, Bootstrap, every feature
```

## Generated CLAUDE.md

Built from the inputs, so it always matches the tree. Sections: Project Facts (Unity version,
pipeline, namespace, features) · **MANDATORY — Unity CLI** (preflight, no YAML edits while an
Editor is reachable, compile check per C# change, test evidence before "done", Safe Mode and
sandbox handling) · **MANDATORY — Unity Skills** (task → skill table; stop if a skill is
missing) · How to Work With This Project (`unity open/status/command/test/build` from the
project root) · Project Structure · Architecture Rules.

To change the rules for every project, edit `make_claude_md()` in `scripts/generate_structure.py`
and its tests; never hand-edit inside the managed block of a generated file.

## Rules

- Never overwrite existing project files; report skips instead.
- No `Resources/` or `Plugins/` folders in the generated tree.
- Feature `README.md` / `AGENTS.md` are stubs — tell the user to fill them before shipping.
- Adding a feature later: re-run with the full `--features` list. Existing asmdefs are skipped, so add
  the new feature's reference to Bootstrap, Editor, and test asmdefs manually (or through the Editor).

## Scripts

- `scripts/generate_structure.py` — generator (Python 3.7+).
- `scripts/test_generate_structure.py` — run `python3 -m pytest scripts/test_generate_structure.py` after any change.

## Standards

- Naming/conventions/asmdef boundaries: `../unity-standards/references/code-standards/architecture-systems.md`
- Test asmdef layout: `../unity-standards/references/test/naming-conventions.md`
- Editor access: `../unity-standards/references/other/unity-cli-routing.md`
