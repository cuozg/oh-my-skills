# CUSTOM_INSPECTOR_TEMPLATE.cs

```csharp
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;
using UnityEditor.UIElements;

namespace _Project.Editor.Inspectors
{
    [CustomEditor(typeof(TargetComponent))]
    public class TargetComponentEditor : UnityEditor.Editor
    {
        public override VisualElement CreateInspectorGUI()
        {
            // Create a new VisualElement to be the root of our inspector UI
            VisualElement myInspector = new VisualElement();

            // Add a simple label
            myInspector.Add(new Label("Engineering Debug Info"));

            // Draw the default inspector properties
            InspectorElement.FillDefaultInspector(myInspector, serializedObject, this);

            // Add custom button
            Button btn = new Button(() => { Debug.Log("Utility Action Triggered"); });
            btn.text = "Run Engineering Utility";
            myInspector.Add(btn);

            return myInspector;
        }
    }
}
```
