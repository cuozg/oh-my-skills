# Unity Editor Patterns

Common patterns and utilities for engineering-focused editor tools.

## 1. Accessing the Editor

- **MenuItem**: Define menu entries with `[MenuItem("Window/Tool")]`. Use validation methods to dynamically enable/disable them.
- **Shortcuts**: Use `[Shortcut("Name", KeyCode)]` for high-frequency engineer tools.
- **Selection**: Query `Selection.objects` or `Selection.activeGameObject` to act on user focus context.
- **Lifecycle**: `EditorWindow` uses `CreateGUI` (once for UI Toolkit setup), `OnEnable`/`OnDisable` (events and data loading), and `OnFocus`/`OnLostFocus`.

## 2. Managing Objects & Data

- **SerializedObject**: Always use the Serialized system to modify data, ensuring **Undo** support and **Prefab** overrides are handled correctly.
- **Multi-object Editing**: Add `[CanEditMultipleObjects]` to `CustomEditor` classes to support array-like selection.
- **System APIs**: Use `AssetDatabase` for file manipulation and `EditorSceneManager` for scene lifecycle.

```csharp
// SerializedObject Modification Pattern
serializedObject.Update();
EditorGUI.BeginChangeCheck();

EditorGUILayout.PropertyField(myProperty); // Draw the property UI

if (EditorGUI.EndChangeCheck()) {
    // Execute custom logic immediately when the user changes a value
    Debug.Log($"Value changed!");
}

serializedObject.ApplyModifiedProperties(); // Save changes and register Undo
```

## 3. Scene View Interaction

- **Handles**: Draw lines, shapes, and interactable controls (`Handles.PositionHandle`) in the 3D scene view.
- **Gizmos**: Override `OnDrawGizmos` for always-visible debug rendering or custom component icons.
- **Custom Editor**: Override `OnSceneGUI` to provide scene-view editing tools specific to a selected component.

## 4. Automation Contexts

- **AssetPostprocessor**: Run logic after asset import (e.g., auto-configure textures, models, or audio).
- **IPreprocessBuildWithReport**: Execute project validation or setup logic right before a build starts.
- **InitializeOnLoad**: Run static constructors as soon as Unity compiles scripts or opens the editor.
- **Batch Processing**: Use `AssetDatabase.StartAssetEditing()` to safely and quickly modify thousands of assets.

## 5. UI Toolkit

Best practices for modern Unity Editor interfaces (UXML/USS/C#). Use for complex windows and custom inspectors.

### Core Concepts & Best Practices
- **Layout & Styling**: Use Flexbox for responsive layouts. Avoid absolute positioning. Leverage `--unity-colors-*` variables to automatically support Light and Dark themes.
- **Data Binding**: Use `element.Bind(serializedObject)` to auto-sync UI and data without writing boilerplate.
- **Performance**: Cache UXML. Use `ListView` or `TreeView` for virtualized data sets. Track changes with `TrackPropertyValue`.
- **IMGUI Fallback**: Host legacy IMGUI code inside an `IMGUIContainer` when absolutely necessary.

### EditorWindow Example
```csharp
public class MyToolWindow : EditorWindow {
    [SerializeField] private VisualTreeAsset uxml;
    [SerializeField] private StyleSheet uss;

    [MenuItem("Tools/My Tool")]
    public static void ShowWindow() => GetWindow<MyToolWindow>("My Tool");

    public void CreateGUI() {
        // CreateGUI runs once. Construct the visual tree here.
        VisualElement root = rootVisualElement;
        uxml.CloneTree(root);
        root.styleSheets.Add(uss);

        var saveBtn = root.Q<Button>("save-btn");
        saveBtn.clicked += () => Debug.Log("Saved!");
    }
    
    private void OnEnable() { /* Subscribe to global events */ }
    private void OnDisable() { /* Cleanup and unsubscribe */ }
    private void OnFocus() { /* Handle gaining focus */ }
    private void OnLostFocus() { /* Handle losing focus */ }
}
```

### PropertyDrawer Example
```csharp
[CustomPropertyDrawer(typeof(MyData))]
public class MyDataDrawer : PropertyDrawer {
    public override VisualElement CreatePropertyGUI(SerializedProperty property) {
        var root = new VisualElement();
        
        // Create and bind property fields automatically
        var nameField = new PropertyField(property.FindPropertyRelative("name"));
        var valueField = new PropertyField(property.FindPropertyRelative("value"));
        
        root.Add(nameField);
        root.Add(valueField);
        
        return root;
    }
}
```