# UI Toolkit Debugging — Diagnostic Utilities

## Debug Utility Class

```csharp
public static class UIDebugUtils
{
    public static void DumpTree(VisualElement root, int maxDepth = 10)
    {
        var sb = new StringBuilder(2048);
        Dump(sb, root, 0, maxDepth);
        Debug.Log(sb.ToString());
    }
    static void Dump(StringBuilder sb, VisualElement el, int d, int max)
    {
        if (d > max) return;
        var indent = new string(' ', d * 2);
        sb.AppendLine($"{indent}[{el.GetType().Name}] #{el.name} layout:{el.layout.width:F0}x{el.layout.height:F0} display:{el.resolvedStyle.display}");
        foreach (var c in el.Children()) Dump(sb, c, d + 1, max);
    }
    public static void FindZeroSize(VisualElement root) =>
        root.Query().ForEach(el => { if (el.resolvedStyle.display == DisplayStyle.Flex && (el.layout.width <= 0 || el.layout.height <= 0)) Debug.Log($"Zero-size: {el.name} {el.layout.width:F0}x{el.layout.height:F0}"); });
    public static void HighlightElement(VisualElement el, Color c, float w = 2f)
    { el.style.borderTopColor = el.style.borderBottomColor = el.style.borderLeftColor = el.style.borderRightColor = c; el.style.borderTopWidth = el.style.borderBottomWidth = el.style.borderLeftWidth = el.style.borderRightWidth = w; }
}
```

## Debug USS Styles

Add to `debug.uss` and remove before release:

```css
.debug-outline * { border-width:1px; border-color:rgba(255,0,0,0.3); }
.debug-highlight { border-width:2px; border-color:red; }
.debug-min-size { min-width:20px; min-height:20px; background-color:rgba(255,0,0,0.3); }
```

Activate in C#:

```csharp
#if UNITY_EDITOR || DEVELOPMENT_BUILD
root.ToggleInClassList("debug-outline");
root.Query().Where(e => e.layout.width <= 0).ForEach(e => e.AddToClassList("debug-min-size"));
#endif
```
