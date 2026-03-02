# gizmos-handles.md

## OnDrawGizmos / OnDrawGizmosSelected

```csharp
// In a MonoBehaviour (Runtime file — use #if guard if referencing Handles)
private void OnDrawGizmos()
{
    Gizmos.color = Color.yellow;
    Gizmos.DrawWireSphere(transform.position, detectionRadius);
}

private void OnDrawGizmosSelected()
{
    Gizmos.color = Color.red;
    Gizmos.DrawLine(transform.position, targetPoint);
}
```

## Handles in CustomEditor (OnSceneGUI)

```csharp
// Editor/PatrolEditor.cs
using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(PatrolPath))]
public class PatrolPathEditor : Editor
{
    private void OnSceneGUI()
    {
        var path = (PatrolPath)target;
        Handles.color = Color.cyan;

        for (int i = 0; i < path.points.Length; i++)
        {
            EditorGUI.BeginChangeCheck();
            Vector3 newPos = Handles.PositionHandle(path.points[i], Quaternion.identity);
            if (EditorGUI.EndChangeCheck())
            {
                Undo.RecordObject(path, "Move Patrol Point");
                path.points[i] = newPos;
            }
        }

        for (int i = 0; i + 1 < path.points.Length; i++)
            Handles.DrawLine(path.points[i], path.points[i + 1]);
    }
}
```

## SceneView Repaint

```csharp
// Force scene repaint while tool is active
private void OnEnable()  => SceneView.duringSceneGui += OnSceneGUI;
private void OnDisable() => SceneView.duringSceneGui -= OnSceneGUI;
private void OnSceneGUI(SceneView sv) { /* draw here */ sv.Repaint(); }
```

## Notes

- `OnDrawGizmos` runs always; `OnDrawGizmosSelected` only when object is selected
- Wrap `using UnityEditor` in `#if UNITY_EDITOR` inside Runtime assemblies
- `Handles.PositionHandle` returns world-space position; always check `EndChangeCheck`
- Use `Handles.Label` for text overlays at a world position
