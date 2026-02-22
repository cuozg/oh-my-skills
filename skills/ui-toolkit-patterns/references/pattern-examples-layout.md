# UI Toolkit Pattern Examples (Part 3)

> Code patterns for patterns 9–10. See [SKILL.md](../SKILL.md) for overview and [pattern-examples-advanced.md](pattern-examples-advanced.md) for patterns 4–8.

## 9. GeometryChangedEvent & Composite View

- **GeometryChangedEvent**: `resolvedStyle` returns zero until layout. Register → fire once → unregister. See [responsive](../../ui-toolkit-responsive/SKILL.md).
- **Composite View**: Split complex screens into parent + child UIViews. Parent injects containers via `Q()`. 2 levels max. See [architecture](../../ui-toolkit-architecture/SKILL.md).

## 10. World-to-Panel Positioning

```csharp
void UpdateHealthBarPosition(VisualElement element, Vector3 worldPos, Vector2 worldSize) {
    if (element.panel == null) return;
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(element.panel, worldPos, worldSize, Camera.main);
    element.transform.position = rect.position;
    element.style.width = rect.width; element.style.height = rect.height;
}
// Call every frame via Update() or schedule.Execute().Every(16). Check element.panel != null.
```
