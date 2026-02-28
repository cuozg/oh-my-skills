---
description: Write Unity Editor C# code and tools
agent: prometheus
subtask: true
---
Use skill unity-code-editor to implement $ARGUMENTS (ulw)

# unity-code-editor — Workflow & Best Practices

## Workflow

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
