---
name: unity-project-init
description: >
  Use this skill to scaffold a Unity project's folder structure — creates Assets/_Project/ with
  feature-based organization, assembly definitions, .gitignore, and namespace-aligned directories.
  Use when the user says "set up my project," "create folder structure," "initialize project,"
  "scaffold my Unity project," or wants a clean starting layout for a new game or prototype.
  Also use when they mention "project organization," "folder layout," or "project template."
  Do not use for adding individual features to an existing project — use unity-code-deep for that.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-project-init

Generate a production-ready Unity project folder tree with assembly definitions, .gitignore, and namespace alignment.

## Scope

**Use when:** Starting a new Unity project, reorganizing a messy project, or setting up a clean folder structure from scratch.

**Switch out if:** Project already has an established structure and the user wants to add features (`unity-code-deep`) or write code (`unity-code-quick`).

## Workflow

1. **Gather** — Ask or infer these inputs:
   - **Company name** (namespace root, e.g., `Studio`)
   - **Project name** (e.g., `RPG`, `Platformer`)
   - **Initial features** (e.g., `Player`, `Combat`, `Inventory`) — default: `Player` only
   - **Render pipeline** (`URP`, `HDRP`, `Built-in`) — default: `URP`
   - **Include .gitignore?** — default: yes

   If the user gives a game description instead of explicit params, extract company/project/features from context.

2. **Generate** — Run the scaffold script:
   ```
   run_skill_script("unity-project-init", "scripts/generate_structure.py",
     arguments=["--company", "Studio", "--project", "RPG",
                "--features", "Player,Combat,Inventory",
                "--pipeline", "URP", "--gitignore"])
   ```
   The script outputs a JSON manifest of all paths and file contents.

3. **Apply** — Use the script output to create the structure in the Unity project:
   - Create directories via `bash mkdir -p`
   - Write `.asmdef` JSON files with correct references
   - Write `.gitignore` at project root if requested
   - Write `.asmdef` for Core, Infrastructure, each feature, and test assemblies

4. **Verify** — Confirm all directories and files exist. Report the generated tree to the user.

## What Gets Generated

```
Assets/
├── _Project/
│   ├── Core/Scripts/          + .asmdef (no deps)
│   ├── Features/{Name}/
│   │   ├── Scripts/           + .asmdef (refs Core)
│   │   ├── Prefabs/
│   │   ├── Art/
│   │   ├── Animations/
│   │   └── Tests/             + .asmdef (test assembly)
│   ├── Infrastructure/Scripts/ + .asmdef (refs Core + features)
│   ├── UI/
│   ├── Settings/
│   ├── Art/
│   ├── Audio/
│   └── Scenes/
├── Plugins/
.gitignore                     (Unity-optimized, at project root)
```

## Rules

- **Feature-based layout.** Every feature is self-contained with Scripts/, Prefabs/, Art/.
- **Assembly per feature.** Each Scripts/ folder gets a `.asmdef` — prevents monolithic recompilation.
- **Namespace = folder path.** `Company.Project.Feature` maps to `Features/Feature/Scripts/`.
- **Core has no deps.** Core assembly defines interfaces and data — everything else depends on it.
- **No `Resources/` folder.** Use Addressables instead — `Resources/` bloats builds.
- **`_Project/` prefix.** Sorts above Unity-generated folders in the Project window.

## Standards

Load the shared project structure reference for detailed rules:
```
read_skill_file("unity-standards", "references/code-standards/project-structure.md")
```

For naming conventions: `read_skill_file("unity-standards", "references/code-standards/naming.md")`
For assembly boundaries: `read_skill_file("unity-standards", "references/code-standards/dependencies.md")`
