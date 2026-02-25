# EDITOR_WINDOW_TEMPLATE.cs

```csharp
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

namespace _Project.Editor.Windows
{
    public class NewEditorWindow : EditorWindow
    {
        [MenuItem("Tools/Engineers/New Window")]
        public static void ShowExample()
        {
            NewEditorWindow wnd = GetWindow<NewEditorWindow>();
            wnd.titleContent = new GUIContent("Engineering Tool");
        }

        public void CreateGUI()
        {
            // Each editor window contains a root VisualElement object
            VisualElement root = rootVisualElement;

            // VisualElements objects can contain other VisualElement following a tree hierarchy.
            VisualElement label = new Label("Welcome to the Engineering Tool!");
            root.Add(label);

            // Import UXML/USS if needed
            // var visualTree = AssetDatabase.LoadAssetAtPath<VisualTreeAsset>("path/to/uxml");
            // root.Add(visualTree.Instantiate());
        }
    }
}
```
