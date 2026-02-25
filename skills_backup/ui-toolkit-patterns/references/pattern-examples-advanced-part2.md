## 7. Async Task Animation (Non-MonoBehaviour)

UIView classes (plain C#) use `async Task`. Fire-and-forget: `_ = MethodAsync()` — wrap in `try/catch`.

```csharp
// Typewriter — Task.Delay ignores timeScale
async Task TypewriterRoutine(Label label, string text) {
    label.text = ""; foreach (char c in text) { label.text += c; await Task.Delay(20); }
}
// Progress bar — Stopwatch + Yield
async Task UpdateLevelAsync(float target, float lerpTime) {
    float start = m_LevelProgress; var sw = System.Diagnostics.Stopwatch.StartNew();
    while (sw.Elapsed.TotalSeconds < lerpTime) {
        float t = (float)(sw.Elapsed.TotalSeconds / lerpTime);
        m_ProgressBar.style.width = new Length(Mathf.Lerp(start, target, t) * 100f, LengthUnit.Percent);
        await Task.Yield();
    }
}
```

## 8. Experimental Animation API

```csharp
// Position — slide marker (requires coordinate conversion)
void AnimateMarkerToTarget(VisualElement target, int ms = 200) {
    Vector2 world = target.parent.LocalToWorld(target.layout.position);
    Vector3 local = m_MenuMarker.parent.WorldToLocal(world);
    m_MenuMarker.experimental.animation.Position(local - new Vector3(m_MenuMarker.resolvedStyle.width / 2f, 0, 0), ms);
}
// Scale — pop-in: element.transform.scale = Vector3(0.1f,0.1f,1f); element.experimental.animation.Scale(1f, 200);
```

See [pattern-examples-layout.md](pattern-examples-layout.md) for patterns 9–10.
