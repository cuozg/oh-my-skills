---
name: unity-init
description: >
  Use this skill to initialize a Unity project structure based on user requests — scaffolding
  folder layout with feature-based organization, assembly definitions (.asmdef), .gitignore,
  and namespace-aligned directories under Assets/_Project/.
  Use whenever a user wants to start a new Unity project, set up folder structure, initialize or
  scaffold a project, create a project template, or organize their Unity project from scratch — even
  if they just say "I'm starting a new Unity game" or describe a game concept and ask for the
  project setup. Also triggers on "folder layout," "project organization," "directory structure,"
  "project template," "asmdef setup," or "best folder structure for Unity." Always use this skill
  when the user provides a company name, project name, and feature list for a new Unity project.
  Do not use for adding features to an existing project — use unity-code for that.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-init

Generate a production-ready Unity project folder tree with assembly definitions, .gitignore, and namespace alignment.

## Scope

**Use when:** Starting a new Unity project, reorganizing a messy project, or setting up a clean folder structure from scratch.

**Switch out if:** Project already has an established structure and the user wants to add features (`unity-code`).

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
   run_skill_script("unity-init", "scripts/generate_structure.py",
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
