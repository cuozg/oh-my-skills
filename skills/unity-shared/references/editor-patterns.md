# Unity Editor Patterns

Common patterns and utilities for engineering-focused editor tools.

## 1. Accessing the Editor

- **MenuItem**: Define menu entries with priorities and validation methods.
- **Shortcuts**: Use `[Shortcut("Name", KeyCode)]` for high-frequency engineer tools.
- **Selection**: Query `Selection.objects` or `Selection.activeGameObject` to act on user focus.

## 2. Managing Objects & Data

- **SerializedObject/Property**: Always use the Serialized system to modify data to ensure **Undo** support and **Prefab** overrides are handled correctly.
- **EditorSceneManager**: Use for opening, closing, and marking scenes as dirty.
- **AssetDatabase**: Critical for asset manipulation (Create, Rename, Delete, DeleteFolder, SaveAssets).

## 3. Scene View Interaction

- **Handles**: Draw lines, shapes, and interactable controls in the 3D scene view.
- **Gizmos**: Use for always-visible debug info or icons.
- **Custom Editor**: Override `OnSceneGUI` to provide scene-view tools specific to a component.

## 4. Automation Contexts

- **AssetPostprocessor**: Automate stuff when files are saved.
- **IPreprocessBuild**: Run logic before a build starts.
- **InitializeOnLoad**: Run code as soon as Unity opens.

## 5. Engineer-Specific Features

- **Project Validation**: Tools that scan the project for missing references, large textures, or invalid naming.
- **Object Finders**: Advanced search tools (e.g., "Find all objects with missing scripts").
- **Batch Processing**: Tools that modify thousands of assets safely (use `AssetDatabase.StartAssetEditing()`).

## UI Toolkit

Best practices for building modern Unity Editor interfaces using UI Toolkit (UIE).

### 1. Core Concepts

UI Toolkit is based on web standards (HTML/CSS):
- **UXML**: The structure (XML-based).
- **USS**: The styling (CSS-like).
- **VisualElement**: The base building block.

### 2. Layout & Styling Best Practices

- **Flexbox**: Use Flexbox for all layout needs. Avoid absolute positioning unless necessary for overlays.
- **Custom Controls**: Inherit from `VisualElement` or existing controls (like `BindableElement`) to create reusable UI components.
- **Data Binding**: Use `Bind(serializedObject)` for automatic synchronization between UI and SerializedProperties.
- **Themes**: Leverage Unity's built-in variables (e.g., `--unity-colors-button-background`) to ensure your tool matches Light/Dark modes automatically.

### 3. Performance & Efficiency

- **UXML Caching**: Load UXML and USS assets once in `OnEnable` and cache them.
- **Batched Updates**: If updating many elements, consider using a `ListView` or `TreeView` for virtualization.
- **Property Watchers**: Use `TrackPropertyValue` to react to property changes without polling.

### 4. IMGUI vs UI Toolkit

- **UI Toolkit**: Use for windows, complex inspectors, and high-quality UI.
- **IMGUI**: Use for simple scene-view handles (`Handles.DrawWireCube`), small property drawers, or quick prototypes.
- **Integration**: You can host an `IMGUIContainer` inside a UI Toolkit element if you need to use legacy IMGUI features.
