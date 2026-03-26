# Code Standards — Consolidation Map

33 reference files consolidated into 4 comprehensive files for faster AI agent loading.

## New Files

| File | Sections | Lines |
|------|----------|-------|
| `core-conventions.md` | Naming, formatting, comments, access modifiers, null safety, unity attributes, code patterns | ~750 |
| `lifecycle-async-errors.md` | Lifecycle, async patterns, error handling, security/validation | ~700 |
| `performance-data.md` | Collections, LINQ, object pooling, serialization | ~720 |
| `architecture-systems.md` | Project structure, dependencies, events, architecture patterns, refactoring, workflows, editor patterns, gizmos, WebGL | ~1050 |

## Old → New Mapping

| Old File | New Location |
|----------|-------------|
| `naming.md` | `core-conventions.md` § Naming Conventions |
| `formatting.md` | `core-conventions.md` § Formatting |
| `comments.md` | `core-conventions.md` § Comments |
| `access-modifiers.md` | `core-conventions.md` § Access Modifiers |
| `null-safety.md` | `core-conventions.md` § Null Safety |
| `null-safety-advanced.md` | `core-conventions.md` § Null Safety (Debug.Assert, #nullable) |
| `unity-attributes.md` | `core-conventions.md` § Unity Attributes |
| `unity-attributes-advanced.md` | `core-conventions.md` § Unity Attributes (Conditional, Preserve, Obsolete) |
| `code-patterns.md` | `core-conventions.md` § Code Patterns |
| `lifecycle.md` | `lifecycle-async-errors.md` § Unity Lifecycle |
| `lifecycle-advanced.md` | `lifecycle-async-errors.md` § Unity Lifecycle (DefaultExecutionOrder, App callbacks) |
| `async.md` | `lifecycle-async-errors.md` § Async Patterns |
| `async-advanced.md` | `lifecycle-async-errors.md` § Async Patterns (Awaitable vs UniTask vs Task) |
| `error-handling.md` | `lifecycle-async-errors.md` § Error Handling |
| `error-handling-advanced.md` | `lifecycle-async-errors.md` § Error Handling (Fail-fast, Security) |
| `collections.md` | `performance-data.md` § Collections |
| `collections-advanced.md` | `performance-data.md` § Advanced Collections |
| `linq.md` | `performance-data.md` § LINQ Usage |
| `object-pooling.md` | `performance-data.md` § Object Pooling |
| `object-pooling-advanced.md` | `performance-data.md` § Object Pooling (Generic, Pre-2021) |
| `serialization.md` | `performance-data.md` § Serialization |
| `architecture-patterns.md` | `architecture-systems.md` § Architecture Patterns |
| `architecture-patterns-advanced.md` | `architecture-systems.md` § Architecture Patterns (Strategy, Mediator) |
| `project-structure.md` | `architecture-systems.md` § Project Folder Structure |
| `dependencies.md` | `architecture-systems.md` § Dependency Management |
| `dependencies-advanced.md` | `architecture-systems.md` § Dependency Management (Zenject) |
| `events.md` | `architecture-systems.md` § Events |
| `refactoring-patterns.md` | `architecture-systems.md` § Refactoring Patterns |
| `multi-file-workflow.md` | `architecture-systems.md` § Workflow Guides (Multi-File) |
| `single-file-runtime-workflow.md` | `architecture-systems.md` § Workflow Guides (Single-File) |
| `editor-patterns.md` | `architecture-systems.md` § Editor Patterns |
| `gizmos-handles.md` | `architecture-systems.md` § Editor Patterns (Gizmos, Handles) |
| `webgl-restrictions.md` | `architecture-systems.md` § Web Platform Restrictions |
