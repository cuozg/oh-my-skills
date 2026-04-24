---
name: flutter-init
description: >
  Initialize Flutter project structure from user requests: feature-first folders,
  pubspec.yaml with Riverpod/GoRouter/Dio/Freezed, analysis_options.yaml, .gitignore,
  and boilerplate Dart files under lib/. Use when starting a new Flutter project,
  setting up folder structure, creating a template, organizing a project from scratch,
  or when the user gives an org name, project name, and feature list. Triggers include
  "folder layout," "project organization," "directory structure," "project template,"
  "pubspec setup," "best folder structure for Flutter," "flutter create with
  architecture," and "set up a Flutter project with Riverpod." Do not use for adding
  features to an existing project; use flutter-code for that.
metadata:
  author: kuozg
  version: "1.0"
---

# flutter-init

Generate a production-ready Flutter project folder tree with feature-first architecture, Riverpod state management, GoRouter routing, and standard tooling.

## Scope

**Use when:** Starting a new Flutter project, reorganizing a project from scratch, or setting up a clean feature-first structure.

**Switch out if:** Project already has an established structure and the user wants to add features (`flutter-code`), build UI (`flutter-ui`), or debug issues (`flutter-debug`).

## Workflow

1. **Gather** — Ask or infer these inputs:
   - **Org** (reverse domain, e.g., `com.example`)
   - **Project name** (snake_case, e.g., `my_app`)
   - **Initial features** (e.g., `auth`, `home`, `profile`) — default: `home` only
   - **State management** (`riverpod`) — default: `riverpod`
   - **Include test scaffolding?** — default: no
   - **Include .gitignore?** — default: yes

   If the user gives an app description instead of explicit params, extract org/project/features from context.

2. **Generate** — Run the scaffold script:
   ```
   run_skill_script("flutter-init", "scripts/generate_structure.py",
     arguments=["--org", "com.example", "--project", "my_app",
                "--features", "auth,home,profile",
                "--state-management", "riverpod",
                "--include-tests"])
   ```
   The script outputs a JSON manifest of all paths and file contents.

3. **Apply** — Use the script output to create the structure:
   - Create directories via `bash mkdir -p`
   - Write all Dart files, pubspec.yaml, analysis_options.yaml
   - Write .gitignore at project root if requested
   - Write README.md with setup instructions

4. **Verify** — Confirm all directories and files exist. Report the generated tree to the user.

## What Gets Generated

```
{project_name}/
├── lib/
│   ├── main.dart                    # ProviderScope + App entry
│   ├── app/
│   │   ├── app.dart                 # MaterialApp.router (ConsumerWidget)
│   │   ├── router.dart              # GoRouter route definitions
│   │   └── theme.dart               # ThemeData, ColorScheme, useMaterial3
│   ├── core/
│   │   ├── constants.dart           # App-wide constants
│   │   ├── exceptions.dart          # AppException base class
│   │   └── network/
│   │       └── dio_client.dart      # Dio HTTP client setup
│   ├── features/
│   │   └── {feature_name}/
│   │       ├── data/
│   │       │   └── {feature}_repository.dart
│   │       ├── presentation/
│   │       │   └── {feature}_screen.dart
│   │       └── providers/
│   │           └── {feature}_provider.dart
│   ├── shared/
│   │   ├── widgets/                 # Reusable UI components
│   │   └── models/                  # Shared data models
│   └── l10n/
│       └── app_en.arb               # English localization starter
├── test/                            # (when --include-tests)
│   └── features/{feature}/
│       └── {feature}_repository_test.dart
├── pubspec.yaml                     # Riverpod + GoRouter + Dio + Freezed
├── analysis_options.yaml            # flutter_lints + strict rules
├── .gitignore                       # Flutter-optimized
└── README.md                        # Setup instructions + architecture
```

## Rules

- **Feature-first layout.** Every feature is self-contained with data/, presentation/, providers/.
- **Three layers per feature.** Data (repositories, models) → State (Riverpod providers) → UI (screens, widgets). Dependency flows downward only.
- **One class per file.** File name matches class name in snake_case.
- **No cross-feature data imports.** Features share code only through `core/` (pure Dart) or `shared/` (Flutter widgets).
- **ConsumerWidget only.** No StatefulWidget in generated code — Riverpod handles all state.
- **Minimal main.dart.** Only `ProviderScope` wrapper and `App()` — everything else delegates to `app/`.
- **Riverpod codegen ready.** Generated providers use `@riverpod` annotation pattern.
- **Freezed ready.** pubspec includes freezed for immutable data classes.

## Standards

Load the shared Flutter reference for detailed rules:
```
read_skill_file("flutter-standards", "references/code-organization.md")
```

For architecture patterns: `read_skill_file("flutter-standards", "references/architecture-patterns.md")`
For naming conventions: `read_skill_file("flutter-standards", "references/dart-style-guide.md")`
For state management: `read_skill_file("flutter-standards", "references/state-management-guide.md")`
