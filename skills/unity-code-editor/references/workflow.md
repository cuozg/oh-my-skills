# unity-code-editor — Workflow

## Steps

1. **Assess**: Identify pain point, choose Window vs Inspector
2. **Architect**: UI Toolkit (modern) vs IMGUI (legacy), data persistence
3. **Implement**: Use templates, patterns from references
4. **Verify**: Test domain reloads, scene changes, profile if handling large data

## Best Practices

- **Undo Mandatory**: Always use `SerializedObject` or `Undo.RecordObject`
- **Match Engine**: Use USS themes for Dark/Light mode
- **Progress Bars**: `EditorUtility.DisplayProgressBar` for batch tasks
- **Batch Safety**: Wrap in `StartAssetEditing`/`StopAssetEditing`
- **No Polling**: Use `TrackPropertyValue` or events, not OnGUI checks

## Tool Types

| Type | Use Case | Template |
|------|----------|----------|
| EditorWindow | Global utility tools | EDITOR_WINDOW_TEMPLATE.md |
| CustomEditor | Component-specific inspectors | CUSTOM_INSPECTOR_TEMPLATE.md |
| AssetPostprocessor | Import automation | (custom pattern) |
| MenuItem/Shortcut | Quick actions | (attribute-based) |

## EditorWindow Checklist

- [ ] `[MenuItem]` path registered
- [ ] Inherits `EditorWindow`
- [ ] `ShowWindow()` static method
- [ ] Handles `OnEnable`/`OnDisable` for lifecycle
- [ ] `SerializedObject` for undo support
- [ ] USS theming applied (if UI Toolkit)

## CustomEditor Checklist

- [ ] `[CustomEditor(typeof(Target))]` attribute
- [ ] `OnInspectorGUI` override with `SerializedObject` workflow
- [ ] `serializedObject.Update()` at start
- [ ] `serializedObject.ApplyModifiedProperties()` at end
- [ ] Handles multi-object editing
