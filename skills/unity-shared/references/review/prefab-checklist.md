# Prefab Review Checklist

## Missing Scripts

- [ ] No `Missing (Mono Script)` components (yellow warning icon)
- [ ] No broken references after assembly/namespace changes
- [ ] `[AddComponentMenu("")]` to hide internal components from menu

## Variant Overrides

- [ ] Variant overrides intentional — review each modified property
- [ ] No "override all" on variants (resets parent changes)
- [ ] Removed components in variants don't break base prefab logic
- [ ] Nested prefab overrides tracked (check Overrides dropdown)

## Hierarchy Depth

- [ ] Nesting ≤ 3 levels deep (Root > Group > Object)
- [ ] Flat hierarchy preferred for performance (Transform changes propagate down)
- [ ] Empty parent GameObjects justified (grouping, pivot, pooling)
- [ ] No orphan transforms (empty objects with only Transform)

## UI-Specific

- [ ] `Raycast Target` disabled on non-interactive elements (Text, Image, Background)
- [ ] Canvas `Render Mode` correct (Overlay vs Camera vs World)
- [ ] Canvas Scaler configured: Scale With Screen Size, reference resolution set
- [ ] Graphic Raycaster present only on Canvases needing input
- [ ] Layout Groups have `Content Size Fitter` if dynamic sizing needed

```csharp
// Common waste: raycast on every UI element
// Fix: Disable on decorative elements
[RequireComponent(typeof(CanvasRenderer))]
// Check in editor: Image > Raycast Target = false for non-interactive
```

## Transform State

- [ ] Root transform: position (0,0,0), rotation (0,0,0), scale (1,1,1)
- [ ] Child transforms have intentional local offsets
- [ ] No negative scale (causes inverted normals, physics issues)
- [ ] Rect Transform anchors set properly for responsive UI

## Inactive Objects

- [ ] Inactive GameObjects with coroutines won't resume on re-enable
- [ ] Inactive objects still serialize and load — remove if unused
- [ ] `SetActive(false)` in Awake still runs Awake but not Start

## Component Setup

- [ ] Colliders match visual mesh (not default unit cube on custom mesh)
- [ ] Rigidbody present if collider should respond to physics
- [ ] `isTrigger` set correctly (trigger vs collision)
- [ ] Audio Sources: spatial blend set (0=2D, 1=3D)
- [ ] Particle Systems: Play On Awake intentional, max particles capped

## Prefab Best Practices

| Pattern | Risk | Fix |
|---------|------|-----|
| Direct scene references in prefab | Null in other scenes | Use SO or event |
| Singleton prefab without guard | Duplicates on reload | Instance check in Awake |
| Large prefab (>50 objects) | Slow instantiate | Split or use pooling |
| Prefab with `HideFlags` | Invisible in hierarchy | Remove or document |

## Validation Script

```csharp
// Editor: Find missing scripts across all prefabs
[MenuItem("Tools/Find Missing Scripts")]
static void FindMissing()
{
    foreach (var go in Resources.FindObjectsOfTypeAll<GameObject>())
        foreach (var c in go.GetComponents<Component>())
            if (c == null) Debug.LogError($"Missing script: {go.name}", go);
}
```
