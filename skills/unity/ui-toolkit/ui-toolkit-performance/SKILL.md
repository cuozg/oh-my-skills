---
name: ui-toolkit-performance
description: "Performance optimization for Unity UI Toolkit. Covers profiling, draw call optimization, transform vs layout animations, element pooling, ListView virtualization, memory management, and GC-free patterns. Use when: (1) UI frame rate is low, (2) Profiling UI draw calls or layout cost, (3) Optimizing list/grid rendering, (4) Reducing GC allocations in UI code, (5) Choosing animation strategies. Triggers: 'UI performance', 'draw calls', 'layout thrashing', 'UI profiling', 'element pool', 'UI memory', 'virtualization', 'UsageHints'."
---

# UI Toolkit Performance

> **Based on**: Unity 6 (6000.0), [Dragon Crashers](../references/dragon-crashers-insights.md) official sample

Optimize UI Toolkit rendering, layout, and memory for 60fps on all platforms. Dragon Crashers achieves 2-4 draw calls per simple screen and < 0.5ms layout cost by following these patterns.

## Performance Mental Model

```
 User Input → Event Processing → Data Update → Binding → Style Resolution
                                                              │
                                                              ▼
                               ┌─────────────────────────────────┐
                               │      LAYOUT (Yoga/Flexbox)      │  ← EXPENSIVE
                               │  Calculates position & size     │
                               │  Triggered by: width, height,   │
                               │  margin, padding, flex changes   │
                               └──────────────┬──────────────────┘
                                              ▼
                               ┌─────────────────────────────────┐
                               │    TRANSFORM (GPU-accelerated)  │  ← CHEAP
                               │  translate, rotate, scale       │
                               │  Does NOT trigger layout        │
                               └──────────────┬──────────────────┘
                                              ▼
                               ┌─────────────────────────────────┐
                               │      RENDER (Batched draws)     │
                               │  Uber shader batches similar    │
                               │  elements into single draw call │
                               └─────────────────────────────────┘
```

**Rule #1: Never trigger layout during animation. Use transforms only.**

## Transform vs Layout Animations

| Property | Type | Layout Recalc | Use For |
|----------|------|--------------|---------|
| `translate` | Transform | No | Slide, position |
| `rotate` | Transform | No | Spin, flip |
| `scale` | Transform | No | Pulse, grow |
| `opacity` | Transform | No | Fade |
| `width` | Layout | **Yes — full subtree** | Never animate |
| `height` | Layout | **Yes — full subtree** | Never animate |
| `margin-*` | Layout | **Yes — full subtree** | Never animate |
| `padding-*` | Layout | **Yes — full subtree** | Never animate |
| `flex-grow` | Layout | **Yes — full subtree** | Never animate |

### Correct: Slide animation via translate

```css
.panel-slide {
    translate: 100% 0;
    opacity: 0;
    transition-property: translate, opacity;
    transition-duration: 300ms;
    transition-timing-function: ease-out;
}

.panel-slide--active {
    translate: 0 0;
    opacity: 1;
}
```

```csharp
// Toggle with USS class — no layout cost
panel.ToggleInClassList("panel-slide--active");
```

### Wrong: Slide animation via width

```css
/* DON'T — triggers layout recalc every frame */
.panel-bad {
    width: 0;
    overflow: hidden;
    transition-property: width;
    transition-duration: 300ms;
}
.panel-bad--open { width: 300px; }
```

## UsageHints

Tell the renderer how elements will change:

```csharp
// Animated elements — enables separate batch for transform changes
panel.usageHints = UsageHints.DynamicTransform;

// Container of animated children
container.usageHints = UsageHints.GroupTransform;

// Elements with color/opacity transitions
button.usageHints = UsageHints.DynamicColor;
```

| Hint | When to Use |
|------|-------------|
| `DynamicTransform` | Element's translate/rotate/scale changes frequently |
| `GroupTransform` | Container that moves/transforms with all children |
| `DynamicColor` | Element's background-color or opacity changes frequently |
| `MaskContainer` | Container with `overflow: hidden` that clips children |

**Do not set on static elements** — adds overhead for elements that don't change.

## ListView Virtualization

For any list with 20+ items, use `ListView` instead of manual ScrollView:

```csharp
// CRITICAL: Set fixedItemHeight for best performance
listView.fixedItemHeight = 72;
listView.virtualizationMethod = CollectionVirtualizationMethod.FixedHeight;

// makeItem: called only for visible + buffer items (typically 8-15)
listView.makeItem = () => itemTemplate.Instantiate();

// bindItem: called when recycled element gets new data
listView.bindItem = (element, index) =>
{
    element.Q<Label>("name").text = items[index].Name;
};

// unbindItem: clean up subscriptions when element goes off-screen
listView.unbindItem = (element, index) =>
{
    // Remove any per-item event subscriptions
};
```

Performance comparison — see [Performance Benchmarks — ListView Virtualization](../references/performance-benchmarks.md) for detailed numbers.

## Draw Call Optimization

### What creates new draw calls

| Cause | Fix |
|-------|-----|
| Different textures | Use SpriteAtlas to batch |
| Different fonts | Limit to 2-3 fonts |
| Nested `overflow: hidden` | Minimize clipping containers |
| Opacity < 1 on containers | Apply opacity to leaf elements |
| Custom render textures | Use sparingly |

### Checking draw calls

1. **Window > Analysis > Frame Debugger** — step through draw calls
2. Look for `UIR.DrawChain` entries
3. Consecutive elements with same texture/font batch together
4. Breaks in sequence indicate new draw call

### SpriteAtlas for batching

```csharp
// All sprites in the same atlas batch into one draw call
// Create atlas: Assets > Create > 2D > Sprite Atlas
// Drag sprites into atlas, ensure "Include in Build" is checked
```

## Element Pooling

For frequently created/destroyed elements (notifications, damage numbers, chat messages):

```csharp
public class VisualElementPool<T> where T : VisualElement, new()
{
    readonly Stack<T> _pool = new();
    readonly Action<T> _onGet;
    readonly Action<T> _onRelease;

    public VisualElementPool(Action<T> onGet = null, Action<T> onRelease = null, int prewarm = 0)
    {
        _onGet = onGet;
        _onRelease = onRelease;
        for (int i = 0; i < prewarm; i++)
            _pool.Push(new T());
    }

    public T Get()
    {
        var el = _pool.Count > 0 ? _pool.Pop() : new T();
        el.style.display = DisplayStyle.Flex;
        _onGet?.Invoke(el);
        return el;
    }

    public void Release(T el)
    {
        el.style.display = DisplayStyle.None;
        _onRelease?.Invoke(el);
        _pool.Push(el);
    }
}
```

## GC-Free Patterns

### Cache Q() calls

```csharp
// BAD: Allocates every frame
void Update() {
    root.Q<Label>("score").text = score.ToString();
}

// GOOD: Cache once
Label _scoreLabel;
void OnEnable() { _scoreLabel = root.Q<Label>("score"); }
void UpdateScore(int score) { _scoreLabel.text = score.ToString(); }
```

### Avoid boxing in style setters

```csharp
// BAD: Boxing allocation
element.style.width = 100; // int boxed to StyleLength

// GOOD: Explicit struct
element.style.width = new Length(100, LengthUnit.Pixel);
```

### Cache Length/StyleColor values

```csharp
// Pre-compute style values used repeatedly
static readonly StyleLength _width100 = new Length(100, LengthUnit.Percent);
static readonly StyleColor _colorRed = new StyleColor(Color.red);
```

### Use method references over lambdas

```csharp
// BAD: Lambda allocates closure
button.RegisterCallback<ClickEvent>(evt => OnClick(evt));

// GOOD: Method reference — no allocation
button.RegisterCallback<ClickEvent>(OnClick);
void OnClick(ClickEvent evt) { /* ... */ }
```

## Profiling Workflow

1. Open **Window > Analysis > Profiler**
2. Select **UI Details** module
3. Play and interact with UI
4. Watch markers:

| Marker | Target | Action if exceeded |
|--------|--------|--------------------|
| `UIR.Layout` | < 0.5ms | Reduce layout changes, flatten hierarchy |
| `UIR.RenderChainUpdate` | < 0.3ms | Reduce dirty elements per frame |
| `UIR.TextRegen` | < 0.2ms | Reduce text changes, batch updates |
| `UIR.DrawChain` | < 0.2ms | Reduce draw calls (atlas, fewer fonts) |

5. Use **Frame Debugger** to count draw calls per screen
6. Compare against targets in [Performance Benchmarks — Draw Call Targets](../references/performance-benchmarks.md)

## Dragon Crashers: Project-Specific Performance Patterns

The following patterns are extracted from the Dragon Crashers UIToolkit demo project with performance annotations.

### FPS Counter with Ring Buffer Averaging

> **Source**: `Assets/Scripts/Utilities/FpsCounter.cs`

UIDocument-based FPS display using a circular buffer for smooth averaging:

```csharp
public class FpsCounter : MonoBehaviour
{
    public const int k_TargetFrameRate = 60;  // -1 for uncapped (PC)
    public const int k_BufferSize = 50;       // frames to average

    [SerializeField] UIDocument m_Document;

    float[] m_DeltaTimeBuffer;
    int m_CurrentIndex;
    Label m_FpsLabel;       // cached — never re-queried
    bool m_IsEnabled;

    void Awake()
    {
        m_DeltaTimeBuffer = new float[k_BufferSize];
        Application.targetFrameRate = k_TargetFrameRate;
    }

    void OnEnable()
    {
        SettingsEvents.FpsCounterToggled += OnFpsCounterToggled;
        m_FpsLabel = m_Document.rootVisualElement.Q<Label>("fps-counter");
    }

    void OnDisable()
    {
        SettingsEvents.FpsCounterToggled -= OnFpsCounterToggled;
    }

    void Update()
    {
        if (!m_IsEnabled) return;  // skip work when hidden

        m_DeltaTimeBuffer[m_CurrentIndex] = Time.deltaTime;
        m_CurrentIndex = (m_CurrentIndex + 1) % m_DeltaTimeBuffer.Length;

        // ⚠ Per-frame string allocation from interpolation
        m_FpsLabel.text = $"FPS: {Mathf.RoundToInt(CalculateFps())}";
    }
}
```

**Performance notes**:
- **Ring buffer** avoids List resizing and gives smooth averaging over `k_BufferSize` frames
- **`m_IsEnabled` guard** skips all Update work when counter is hidden — zero cost when off
- **`Application.targetFrameRate = 60`** is critical for mobile battery/thermal management
- **Cached `m_FpsLabel`** — queried once in OnEnable, never per-frame
- ⚠ **Per-frame `$"FPS: {value}"`** allocates a string every frame (~40 bytes). For zero-GC, use a `char[]` buffer or update only when value changes

### World-to-Panel Positioning (LateUpdate Cost)

> **Source**: `Assets/Scripts/UI/Controllers/HealthBarController.cs`

Per-frame world-to-panel projection for health bars anchored to 3D characters:

```csharp
// Called EVERY frame in LateUpdate — expensive per-instance
void MoveToWorldPosition(VisualElement element, Vector3 worldPosition, Vector2 worldSize)
{
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(
        element.panel, worldPosition, worldSize, Camera.main);
    element.transform.position = rect.position;  // transform, not layout — good
}

private void LateUpdate()
{
    // ShowNameAndStats calls Q<> every frame — should be cached
    ShowNameAndStats(m_ShowNameplate, m_ShowStat);
    MoveToWorldPosition(m_HealthBar, transformToFollow.position, m_WorldSize);
}
```

**Performance notes**:
- **`Camera.main`** calls `FindWithTag("MainCamera")` internally — cache it: `Camera _cam; void Start() { _cam = Camera.main; }`
- **`element.transform.position`** uses transform (not layout) — no layout rebuild, good for per-frame updates
- **`ShowNameAndStats` calls `Q<>` every frame** — these should be cached in `OnEnable` or setup
- **Per-instance cost**: Each health bar runs its own LateUpdate + camera projection. With 10+ entities, consider batching all projections in a single manager
- **`RuntimePanelUtils.CameraTransformWorldToPanelRect`** does matrix multiplication per call — unavoidable but limit the number of elements using it

### Async/Await vs Coroutine Tradeoffs for UI Animations

> **Sources**: `Assets/Scripts/UI/UIViews/OptionsBarView.cs`, `Assets/Scripts/UI/UIViews/ChatView.cs`

Dragon Crashers uses `async Task` for UI animations because views are plain C# classes (not MonoBehaviours), so coroutines are unavailable:

```csharp
// Fire-and-forget pattern — each call allocates a Task object
void OnFundsUpdated(GameData gameData)
{
    _ = HandleFundsUpdatedAsync(gameData);  // Task discarded
}

// Animated counter lerp — GC pressure from Task.Delay per frame
async Task LerpRoutine(Label label, uint startValue, uint endValue, float duration)
{
    float lerpValue = (float)startValue;
    float t = 0f;

    while (Mathf.Abs((float)endValue - lerpValue) > 0.05f)
    {
        t += Time.deltaTime / duration;
        lerpValue = Mathf.Lerp(startValue, endValue, t);
        label.text = lerpValue.ToString("0");           // string alloc per frame
        await Task.Delay(TimeSpan.FromSeconds(Time.deltaTime));  // Timer + TCS alloc
    }
    label.text = endValue.ToString();
}
```

```csharp
// Infinite typewriter loop — no cancellation token
async Task ChatRoutine(List<ChatSO> chatData)
{
    while (true)
    {
        foreach (ChatSO chat in chatData)
        {
            // String concat per character: m_ChatText.text += c
            await AnimateMessageAsync(chat.chatname, chat.message);
            await Task.Delay(k_DelayBetweenLines);     // 1000ms
        }
    }
}
```

**GC cost comparison**:

| Pattern | Allocation per iteration | Notes |
|---------|------------------------|-------|
| `await Task.Delay(ms)` | Timer + TaskCompletionSource (~120 bytes) | Adds up in per-frame loops |
| `_ = SomeAsync()` | Task object (~72 bytes) | One-time per fire-and-forget call |
| `label.text += c` | New string per character | Use `StringBuilder` instead |
| `value.ToString("0")` | String allocation (~24 bytes) | Update only when display value changes |

**Recommendations**:
- For non-MonoBehaviour classes, `async Task` is the only option — accept the GC cost for infrequent animations
- For per-frame loops, prefer USS transitions or `IVisualElementScheduledItem` (schedule.Execute) over `await Task.Delay`
- Add `CancellationToken` to infinite loops to prevent leaks when views are disposed
- Use `UniTask` (if available) for allocation-free async in hot paths

### Dynamic List Generation: Instantiate vs ListView

> **Sources**: `Assets/Scripts/UI/UIViews/InventoryView.cs`, `Assets/Scripts/UI/UIViews/ShopView.cs`

Dragon Crashers uses `VisualTreeAsset.Instantiate()` in a loop for all dynamic lists:

```csharp
// InventoryView: Clear + re-instantiate all items on every update
void ShowGearItems(List<EquipmentSO> gearToShow)
{
    VisualElement contentContainer = m_ScrollViewParent.Q<VisualElement>("unity-content-container");
    contentContainer.Clear();  // destroys all previous elements

    for (int i = 0; i < gearToShow.Count; i++)
    {
        // Each call: clones UXML tree, creates VisualElements, triggers layout
        TemplateContainer gearUIElement = m_GearItemAsset.Instantiate();
        container.Add(gearUIElement);
    }
}

// ShopView: Same pattern — Instantiate per item
void CreateShopItemElement(ShopItemSO shopItemData, VisualElement parentElement)
{
    TemplateContainer shopItemElem = m_ShopItemAsset.Instantiate();
    // ... setup component, add to parent
    parentElement.Add(shopItemElem);
}
```

**When this is acceptable**: Small lists (< 30 items) updated infrequently (tab switch, screen open). Dragon Crashers' shop has ~5-10 items per tab — no performance issue.

**When to switch to ListView**:

| Item Count | Approach | Why |
|-----------|----------|-----|
| < 20 | `Instantiate()` in loop | Simpler code, negligible cost |
| 20–50 | Consider `ListView` | Layout cost grows linearly |
| 50+ | **Must use `ListView`** | Only creates ~8-15 visible elements regardless of data size |

```csharp
// Preferred for large lists — only visible items are instantiated
listView.fixedItemHeight = 72;
listView.virtualizationMethod = CollectionVirtualizationMethod.FixedHeight;
listView.makeItem = () => m_GearItemAsset.Instantiate();
listView.bindItem = (element, index) => {
    var component = new GearItemComponent(gearList[index]);
    component.SetVisualElements(element as TemplateContainer);
    component.SetGameData(element as TemplateContainer);
};
listView.itemsSource = gearList;
```

### Event Propagation: StopImmediatePropagation Impact

> **Source**: `Assets/Scripts/UI/Components/ShopItemComponent.cs`

```csharp
// Prevents ScrollView drag when pointer moves over buy button
m_BuyButton.RegisterCallback<PointerMoveEvent>(MovePointerEventHandler);

void MovePointerEventHandler(PointerMoveEvent evt)
{
    evt.StopImmediatePropagation();  // aggressive — stops ALL further processing
}
```

**Propagation methods compared**:

| Method | Effect | Use Case |
|--------|--------|----------|
| `StopPropagation()` | Stops bubbling up, remaining listeners on current target still fire | Most cases |
| `StopImmediatePropagation()` | Stops bubbling AND remaining listeners on current target | When you need to block ScrollView drag |
| `PreventDefault()` | Prevents default behavior but event still propagates | Rarely needed in UI Toolkit |

**Performance impact**: `StopImmediatePropagation()` is a micro-optimization — it prevents the event system from walking up the visual tree. In ScrollViews with many interactive children, this avoids unnecessary propagation work. However, it can silently break other listeners on the same element — use with awareness.

### Event Subscription Lifecycle: Preventing Leaks

Dragon Crashers uses two subscription patterns depending on class type:

**MonoBehaviour controllers** — OnEnable/OnDisable:
```csharp
// HealthBarController, FpsCounter
void OnEnable()  { MediaQueryEvents.CameraResized += OnCameraResized; }
void OnDisable() { MediaQueryEvents.CameraResized -= OnCameraResized; }
```

**Plain C# view classes** — Constructor/Dispose:
```csharp
// OptionsBarView, ChatView, InventoryView, ShopView
public OptionsBarView(VisualElement topElement) : base(topElement)
{
    ShopEvents.FundsUpdated += OnFundsUpdated;
}

public override void Dispose()
{
    base.Dispose();
    ShopEvents.FundsUpdated -= OnFundsUpdated;
    UnregisterButtonCallbacks();  // also clean up UI event callbacks
}
```

**Leak prevention rules**:
1. **Every `+=` must have a matching `-=`** in the symmetrical lifecycle method
2. **MonoBehaviour**: subscribe in `OnEnable`, unsubscribe in `OnDisable` (handles re-enable correctly)
3. **Plain C# classes**: subscribe in constructor, unsubscribe in `Dispose()` — caller must call Dispose
4. **UI callbacks** (`RegisterCallback`): unregister in Dispose/OnDisable if the element outlives the handler
5. **Static events** (like `ShopEvents.FundsUpdated`) are the most dangerous — they root the subscriber in memory indefinitely if not unsubscribed

### Project-Specific Recommendations

| Recommendation | Source | Impact |
|---------------|--------|--------|
| Set `Application.targetFrameRate = 60` for mobile | `FpsCounter.cs` | Reduces battery drain, thermal throttling |
| Cache `Camera.main` — don't call per-frame | `HealthBarController.cs` | Avoids `FindWithTag` allocation per frame |
| Cache all `Q<T>()` results — never re-query in Update/LateUpdate | `HealthBarController.cs` | Eliminates per-frame string + traversal cost |
| Use transform (not layout) for positioning | `HealthBarController.cs` | `element.transform.position` skips layout recalc |
| Prefer USS transitions over `async Task.Delay` loops | `OptionsBarView.cs`, `ChatView.cs` | Eliminates Timer + TaskCompletionSource allocations |
| Add `CancellationToken` to infinite async loops | `ChatView.cs` | Prevents memory leak when view is disposed |
| Use `StringBuilder` for character-by-character text | `ChatView.cs` | Avoids O(n²) string concat |
| `VisualTreeAsset.Instantiate()` is fine for < 30 items | `InventoryView.cs`, `ShopView.cs` | Switch to ListView for 50+ items |
| `StopImmediatePropagation()` for ScrollView children | `ShopItemComponent.cs` | Prevents drag conflicts, micro-optimization |
| Match subscribe/unsubscribe lifecycle symmetrically | All views/controllers | Prevents memory leaks from static event refs |

## Optimization Checklist

- [ ] Lists 20+ items → ListView with fixedItemHeight
- [ ] All animations use translate/rotate/scale/opacity only
- [ ] Animated elements have `UsageHints.DynamicTransform`
- [ ] Q() calls cached in OnEnable, not called per-frame
- [ ] No string concat in per-frame updates
- [ ] Sprites in SpriteAtlas for batching
- [ ] Max 2-3 fonts per screen
- [ ] Minimal nested overflow:hidden
- [ ] Opacity on leaf elements, not containers
- [ ] Element pooling for transient UI (notifications, popups)

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Animating `width`/`height` | Full subtree layout recalc every frame | Use `translate`, `scale`, `rotate`, `opacity` |
| Q() in Update() | GC allocation every frame from string queries | Cache references in `OnEnable` |
| No `fixedItemHeight` on ListView | Falls back to variable height — slower virtualization | Always set `fixedItemHeight` |
| `UsageHints` on static elements | Adds per-frame overhead for elements that don't change | Only set on animated elements |
| String concatenation per frame | GC allocation from `$"Score: {val}"` every update | Use `StringBuilder` or update only on change |
| Opacity on containers | Breaks draw call batching for all children | Apply opacity to leaf elements only |
| Nested `overflow: hidden` | Each clip layer adds a draw call | Minimize clip nesting, flatten hierarchy |
| Creating elements in hot paths | GC pressure from `new VisualElement()` in loops | Use element pooling |

## Exercise: Optimize a Leaderboard Screen

Profile and optimize a 100-row leaderboard with player avatars:

1. **Baseline**: Create a `ScrollView` with 100 manually created row elements, each with an avatar image + name label + score label
2. **Profile**: Open **Profiler > UI Details**, measure `UIR.Layout` and draw call count
3. **Optimize Step 1**: Replace ScrollView with `ListView` + `fixedItemHeight: 56` — measure improvement
4. **Optimize Step 2**: Pack all avatar sprites into a `SpriteAtlas` — measure draw call reduction
5. **Optimize Step 3**: Add `UsageHints.DynamicTransform` to row highlight animation — verify `UIR.TransformUpdate` replaces `UIR.Layout`
6. **Optimize Step 4**: Cache all `Q()` calls, remove per-frame allocations — verify zero GC in Profiler

**Checklist**: ✅ Before/after profiler screenshots captured · ✅ ListView virtualization active (verify: only 8-15 `makeItem` calls, not 100) · ✅ Draw calls ≤ 5 for the screen · ✅ Zero GC allocations during scroll · ✅ `UIR.Layout` < 0.5ms

## Shared Resources

- [Performance Benchmarks](../references/performance-benchmarks.md) — metrics, targets, zero-alloc patterns
- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — production performance patterns
- [Code Templates](../references/code-templates.md) — Element Pool, Base Screen templates
- [Official Docs Links](../references/official-docs-links.md) — Unity 6 documentation index

## Official Documentation

- [Performance Considerations](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-performance-considerations.html)
- [ListView](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-ListView.html)
- [USS Transitions](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-Transitions.html)
- [Profiler](https://docs.unity3d.com/6000.0/Documentation/Manual/Profiler.html)

## Cross-References

- **[UI Toolkit Patterns](../ui-toolkit-patterns/SKILL.md)** — Animation patterns (USS transitions, async animations, typewriter effects) referenced by performance tradeoffs above
- **[UI Toolkit Mobile](../ui-toolkit-mobile/SKILL.md)** — Mobile-specific performance: `Application.targetFrameRate`, safe area, touch targets
- **[UI Toolkit Debugging](../ui-toolkit-debugging/SKILL.md)** — UI Toolkit Debugger, profiler workflow, draw call inspection
- **[Dragon Crashers Insights](../references/dragon-crashers-insights.md)** — Full architectural analysis of patterns used above

---

**← Previous**: [Patterns](../ui-toolkit-patterns/SKILL.md) | **Next →**: [Mobile](../ui-toolkit-mobile/SKILL.md)
