# Unity Editor UI Toolkit Guide

Best practices for building modern Unity Editor interfaces using UI Toolkit (UIE).

## 1. Core Concepts

 UI Toolkit is based on web standards (HTML/CSS):
- **UXML**: The structure (XML-based).
- **USS**: The styling (CSS-like).
- **VisualElement**: The base building block.

## 2. Layout & Styling Best Practices

- **Flexbox**: Use Flexbox for all layout needs. Avoid absolute positioning unless necessary for overlays.
- **Custom Controls**: Inherit from `VisualElement` or existing controls (like `BindableElement`) to create reusable UI components.
- **Data Binding**: Use `Bind(serializedObject)` for automatic synchronization between UI and SerializedProperties.
- **Themes**: Leverage Unity's built-in variables (e.g., `--unity-colors-button-background`) to ensure your tool matches Light/Dark modes automatically.

## 3. Performance & Efficiency

- **UXML Caching**: Load UXML and USS assets once in `OnEnable` and cache them.
- **Batched Updates**: If updating many elements, consider using a `ListView` or `TreeView` for virtualization.
- **Property Watchers**: Use `TrackPropertyValue` to react to property changes without polling.

## 4. IMGUI vs UI Toolkit

- **UI Toolkit**: Use for windows, complex inspectors, and high-quality UI.
- **IMGUI**: Use for simple scene-view handles (`Handles.DrawWireCube`), small property drawers, or quick prototypes.
- **Integration**: You can host an `IMGUIContainer` inside a UI Toolkit element if you need to use legacy IMGUI features.
