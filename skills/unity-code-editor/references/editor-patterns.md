# editor-patterns.md

## EditorWindow

```csharp
// Editor/MyToolWindow.cs
using UnityEditor;
using UnityEngine;

public class MyToolWindow : EditorWindow
{
    [MenuItem("Tools/My Tool")]
    public static void Open() => GetWindow<MyToolWindow>("My Tool");

    private void OnGUI()
    {
        EditorGUILayout.LabelField("Settings", EditorStyles.boldLabel);
        // add controls here
    }
}
```

## CustomEditor

```csharp
// Editor/MyComponentEditor.cs
using UnityEditor;

[CustomEditor(typeof(MyComponent))]
public class MyComponentEditor : Editor
{
    SerializedProperty _speed;

    private void OnEnable() => _speed = serializedObject.FindProperty("speed");

    public override void OnInspectorGUI()
    {
        serializedObject.Update();
        base.OnInspectorGUI();
        EditorGUILayout.PropertyField(_speed);
        if (GUILayout.Button("Apply")) ((MyComponent)target).Apply();
        serializedObject.ApplyModifiedProperties();
    }
}
```

## PropertyDrawer

```csharp
// Editor/RangeDrawer.cs
using UnityEditor;
using UnityEngine;

[CustomPropertyDrawer(typeof(RangedFloat))]
public class RangedFloatDrawer : PropertyDrawer
{
    public override void OnGUI(Rect pos, SerializedProperty prop, GUIContent label)
    {
        EditorGUI.BeginProperty(pos, label, prop);
        var min = prop.FindPropertyRelative("min");
        var max = prop.FindPropertyRelative("max");
        float lo = min.floatValue, hi = max.floatValue;
        EditorGUI.MinMaxSlider(pos, label, ref lo, ref hi, 0f, 100f);
        min.floatValue = lo; max.floatValue = hi;
        EditorGUI.EndProperty();
    }
}
```

## Notes

- Always place under an `Editor/` folder (any depth)
- `SerializedProperty` path uses field name (camelCase), not display name
- Call `Undo.RecordObject(target, "label")` before direct field mutations
- Use `EditorUtility.SetDirty(target)` after direct mutations to mark scene dirty
