# Specialist Execution Mapping

Guide for choosing the right specialized skill for a task based on the domain.

| Task Domain | Specialist Skill to Load |
| :--- | :--- |
| **C# Logic, MonoBehaviours, Managers** | `unity-implement-logic` |
| **Shaders, VFX, Materials, AssetPostprocessors** | `unity-tech-art` |
| **Editor Windows, Custom Inspectors, Tools** | `unity-editor-tools` |
| **FlatBuffer Schema (.fbs), JSON Data, Binary** | `flatbuffers-coder` |
| **Mobile Interop, Android/iOS Features** | `unity-mobile-deploy` |
| **WebGL, JS Interop, Browser Optimization** | `unity-web-deploy` |
| **Profiling, FPS Fixes, Memory Leaks** | `unity-optimize-performance` |
| **Automated Tests (Edit/Play Mode)** | `unity-test` |
| **Code Structure, API Documentation** | `unity-write-docs` |

## Composite Tasks

If a task detail file (`.md`) includes multiple domains:
1.  **Phase 1**: Load `unity-implement-logic` to set up the logic backbone.
2.  **Phase 2**: Load specialists for specific assets (e.g., `flatbuffers-coder` for data or `unity-tech-art` for shaders).
3.  **Phase 3**: Load `unity-test` to verify implementation.
