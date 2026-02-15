# Unity Editor Scripting Patterns

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
