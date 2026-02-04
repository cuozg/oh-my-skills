---
description: Workflow for identifying and resolving performance bottlenecks in Unity.
---

# Workflow: Performance Optimization

Use this workflow to improve frame rates, reduce memory usage, or optimize load times.

1.  **Baseline Check**:
    // turbo
    - Use `manage_scene` (action="get_hierarchy") to check for object counts and deep hierarchies.
    - Check the console for high-frequency logs using `read_console`.
2.  **Detection**:
    - Search for expensive calls (`GetComponent`, `Find`, `Instantiate`) inside `Update()` or hot loops.
    - Identify excessive string allocations or boxing in frequently called logic.
3.  **Graphic Audit**:
    - List large assets using `manage_asset` (search_pattern="*.mat" or "*.prefab").
    - Use `manage_material` to check for heavy shaders or missing optimizations.
4.  **Optimization**:
    - **Logic**: Implement object pooling, cache references in `Awake`, or use the `Awaitable` API for async tasks.
    - **Assets**: Combine materials, simplify meshes, and adjust texture compression settings.
5.  **Validation**:
    - Run the game in the Editor and monitor for improvements in the console or frame timing logs.
6.  **Update Docs**:
    - If architecture was changed for performance (e.g., adding a Manager), update the project documentation using `/unity-documentation`.
