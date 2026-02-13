# Common Bugs & Fixes — UI Toolkit

Frequently encountered issues when working with UI Toolkit, with tested solutions. Items marked **[DC]** were observed or are relevant to the Dragon Crashers project patterns.

---

## 1. Q() Returns Null

**Symptom**: `NullReferenceException` when calling `root.Q<Label>("my-label")`.

**Causes & Fixes**:

| Cause | Fix |
|-------|-----|
| Element name mismatch (case-sensitive) | Check UXML — names are case-sensitive: `"gold-label"` ≠ `"Gold-Label"` |
| Querying before UXML is loaded | Query in `OnEnable()` after `m_Document.rootVisualElement` is available |
| Querying child of `VisualTreeAsset.Instantiate()` before adding to tree | Add to parent first, then query |
| **[DC]** Querying in constructor but UXML uses `VisualTreeAsset.CloneTree()` | Ensure `CloneTree()` is called before any `Q()` calls |

```csharp
// WRONG — querying before clone
public MyView(VisualElement root)
{
    m_Label = root.Q<Label>("title"); // May be null!
    m_Template.CloneTree(root);       // Too late
}

// RIGHT
public MyView(VisualElement root)
{
    m_Template.CloneTree(root);       // Clone first
    m_Label = root.Q<Label>("title"); // Now it exists
}
```

---

## 2. CSS Transitions Not Working

**Symptom**: Adding/removing a USS class doesn't animate — snaps instantly.

**Causes & Fixes**:

| Cause | Fix |
|-------|-----|
| Missing `transition-property` in USS | Add `transition-property: translate, opacity;` |
| Transitioning layout properties | Use `translate`/`scale`/`opacity` only — `width`/`height`/`margin` don't animate smoothly |
| **[DC]** Adding class too quickly after `display: flex` | Insert `await Task.Delay(10)` between showing element and adding transition class |
| Element not in visual tree yet | Wait for `GeometryChangedEvent` before applying transition class |

```csharp
// [DC] Pattern from OptionsBarView.cs — delay between display and class
async Task ShowOptionsBarTask()
{
    m_Element.style.display = DisplayStyle.Flex;
    await Task.Delay(10); // Let layout resolve
    m_Element.AddToClassList("options-bar--active"); // NOW transition works
}
```

---

## 3. Event Subscription Leaks

**Symptom**: Events fire multiple times or target destroyed objects. Memory grows over time.

**Causes & Fixes**:

| Cause | Fix |
|-------|-----|
| **[DC]** Missing `-=` for static Action delegates | Every `+=` must have matching `-=` in `Dispose()`/`OnDisable()` |
| Subscribing in `Awake()` but only unsubscribing in `OnDestroy()` | Use `OnEnable()`/`OnDisable()` pair instead |
| **[DC]** View constructor subscribes but `Dispose()` is never called | Controller MUST call `view.Dispose()` in `OnDisable()` |
| Lambda subscriptions can't be unsubscribed | Use method references: `CharEvents.GoldUpdated += OnGoldUpdated` |

```csharp
// [DC] Correct pattern from Dragon Crashers
// Controller
void OnEnable()
{
    m_HomeView = new HomeView(m_Document.rootVisualElement);
    HomeEvents.HomeScreenShown?.Invoke();
}
void OnDisable()
{
    m_HomeView.Dispose(); // MUST dispose view
}

// View
public HomeView(VisualElement root)
{
    CharEvents.GoldUpdated += OnGoldUpdated; // Subscribe
}
public void Dispose()
{
    CharEvents.GoldUpdated -= OnGoldUpdated; // Unsubscribe
}
```

---

## 4. ScrollView Swallows Child Click/Drag Events

**Symptom**: Buttons or interactive elements inside `ScrollView` don't respond, or dragging a child drags the scroll instead.

**Fix**:

```csharp
// [DC] Pattern from ShopItemComponent.cs
m_InteractiveChild.RegisterCallback<PointerDownEvent>(evt =>
{
    evt.StopImmediatePropagation(); // Prevent ScrollView from capturing
    HandleChildInteraction();
}, TrickleDown.TrickleDown); // TrickleDown phase is important!
```

**Note**: Use `StopImmediatePropagation()`, not `StopPropagation()`. The latter still allows other handlers on the same element.

---

## 5. Safe Area Not Updating on Rotation

**Symptom**: Notch insets are correct initially but wrong after device rotation.

**Causes & Fixes**:

| Cause | Fix |
|-------|-----|
| Only applying safe area once | Subscribe to `GeometryChangedEvent` on root for reapplication |
| **[DC]** Using `padding` for safe area | Use `borderWidth` — padding affects child layout calculations |
| Not recalculating when `Screen.safeArea` changes | Check in `Update()` or use `MediaQueryEvents.AspectRatioChanged` |

```csharp
// [DC] SafeAreaBorder.cs approach
void OnGeometryChanged(GeometryChangedEvent evt)
{
    ApplySafeArea(); // Recalculate on any geometry change
}

void ApplySafeArea()
{
    Rect safeArea = Screen.safeArea;
    // Use borderWidth, NOT padding
    m_Root.style.borderLeftWidth = CalculateInset(safeArea.x, Screen.width);
    m_Root.style.borderRightWidth = CalculateInset(Screen.width - safeArea.xMax, Screen.width);
}
```

---

## 6. Theme Switch Causes Flash/Flicker

**Symptom**: Brief visual glitch when switching themes at runtime.

**Causes & Fixes**:

| Cause | Fix |
|-------|-----|
| Swapping TSS without swapping PanelSettings | **[DC]** Swap BOTH `panelSettings` and `themeStyleSheet` together |
| Intermediate state visible for one frame | Apply both changes in same frame, before next repaint |
| Old theme USS classes still applied | Ensure USS files properly hide/show decorations per theme |

```csharp
// [DC] ThemeManager.cs — swap both atomically
public void SetTheme(string themeName)
{
    var settings = m_ThemeSettings.Find(x => x.theme == themeName);
    m_Document.panelSettings = settings.panelSettings;           // Swap PanelSettings
    m_Document.panelSettings.themeStyleSheet = settings.tss;     // Swap TSS
    // Both applied in same frame — no flicker
}
```

---

## 7. Layout Values Read as Zero

**Symptom**: `resolvedStyle.width` or `resolvedStyle.height` returns 0 even though element is visible.

**Fix**: Layout values aren't available until after the first layout pass. Use `GeometryChangedEvent`:

```csharp
// [DC] Pattern from HomeView.cs
m_Element.RegisterCallback<GeometryChangedEvent>(evt =>
{
    m_Element.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    float width = m_Element.resolvedStyle.width;  // Now valid
    float height = m_Element.resolvedStyle.height; // Now valid
    InitializeLayout(width, height);
});
```

**Common mistake**: Querying layout in the same frame as `Add()` or `style.display = Flex`.

---

## 8. World-to-Panel Position Jitters or Lags

**Symptom**: UI element tracking a 3D object appears to lag one frame behind.

**Causes & Fixes**:

| Cause | Fix |
|-------|-----|
| Updating position in `Update()` | **[DC]** Use `LateUpdate()` — runs after camera movement |
| Using `Camera.main` (accessor overhead + potential null) | Cache camera reference in `OnEnable()` |
| **[DC]** Not updating on orientation change | Listen for `ThemeEvents.CameraUpdated` to recalculate |

```csharp
// [DC] PositionToVisualElement.cs — correct timing
void LateUpdate()
{
    if (m_Camera == null || m_Panel == null) return;
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(
        m_Panel, m_WorldTransform.position, m_WorldSize, m_Camera);
    m_TargetElement.style.left = rect.x;
    m_TargetElement.style.top = rect.y;
}
```

---

## 9. Async Task Exception Silently Swallowed

**Symptom**: UI animation fails silently — no error in console.

**Cause**: Fire-and-forget `_ = AsyncMethod()` discards exceptions from the `Task`.

**Fix**:

```csharp
// Problem: exception disappears
_ = ShowAnimationAsync(); // If this throws, you'll never know

// Fix 1: Add try/catch inside the async method
async Task ShowAnimationAsync()
{
    try
    {
        await Task.Delay(300);
        m_Element.AddToClassList("active");
    }
    catch (Exception ex)
    {
        Debug.LogException(ex);
    }
}

// Fix 2: Use ContinueWith for logging
ShowAnimationAsync().ContinueWith(t =>
{
    if (t.IsFaulted) Debug.LogException(t.Exception);
}, TaskScheduler.FromCurrentSynchronizationContext());
```

---

## 10. VisualTreeAsset.Instantiate() Children Not Styled

**Symptom**: Dynamically instantiated elements appear unstyled or have default layout.

**Causes & Fixes**:

| Cause | Fix |
|-------|-----|
| USS not loaded in the UXML template | Add `<Style src="...">` in the template UXML |
| Parent USS classes don't cascade to instantiated children | Apply USS classes directly to instantiated root |
| **[DC]** Template expects USS from parent UIDocument | Ensure parent's TSS includes the component's USS |

```csharp
// [DC] Pattern from ShopView.cs
VisualElement item = m_ItemTemplate.Instantiate();
item.AddToClassList("shop-item"); // Apply expected class
container.Add(item); // Add to tree — styles now cascade
```

---

## 11. Button.userData Lost After Rebuild

**Symptom**: `button.userData` returns null after rebuilding a dynamic list.

**Cause**: `container.Clear()` destroys old elements. New elements from `Instantiate()` don't have `userData`.

**Fix**: Re-assign `userData` after every rebuild:

```csharp
// [DC] Pattern from ShopView.cs
void RebuildList(List<ShopItemSO> items)
{
    m_Container.Clear();
    foreach (var item in items)
    {
        var button = m_Template.Instantiate().Q<Button>("item-button");
        button.userData = item;  // Assign EVERY time
        button.RegisterCallback<ClickEvent>(OnItemClicked);
        m_Container.Add(button);
    }
}
```

---

## 12. UxmlFactory/UxmlTraits Not Showing in UI Builder

**Symptom**: Custom control doesn't appear in the UI Builder library panel.

**Causes & Fixes**:

| Cause | Fix |
|-------|-----|
| Missing `UxmlFactory` inner class | Add `public new class UxmlFactory : UxmlFactory<MyControl, UxmlTraits> { }` |
| Class not in correct namespace | UI Builder scans all assemblies — ensure class compiles |
| Assembly definition excluded from editor | Custom controls must be in a runtime assembly (not editor-only) |
| **[DC]** Using `new` keyword without base class having same nested type | `new` is correct for `BaseField<T>` subclasses (e.g., `SlideToggle`) |

```csharp
// [DC] SlideToggle.cs — correct pattern
public class SlideToggle : BaseField<bool>
{
    public new class UxmlFactory : UxmlFactory<SlideToggle, UxmlTraits> { }
    public new class UxmlTraits : BaseFieldTraits<bool, UxmlBoolAttributeDescription>
    {
        // Custom attribute declarations here
    }
}
```

---

## Quick Diagnostic Flowchart

```
Element not visible?
├── Check display: none → style.display = DisplayStyle.Flex
├── Check opacity: 0 → style.opacity = 1
├── Check visibility: hidden → style.visibility = Visibility.Visible
├── Check parent display/visibility
└── Check element is in visual tree → parent.Contains(element)

Element visible but not interactive?
├── Check pickingMode → PickingMode.Position (not Ignore)
├── Check if parent catches events → StopImmediatePropagation
├── Check if element is behind another → Check z-order / visual tree order
└── Check if in ScrollView → TrickleDown phase for child events

Event fires multiple times?
├── Check duplicate subscriptions → Use OnEnable/OnDisable pair
├── Check lambda subscriptions → Can't unsubscribe lambdas
├── Check event bubbling → Use StopPropagation if needed
└── Check view Dispose() is called → Controller must call it
```

---

## Related Skills

- **[ui-toolkit-debugging](../ui-toolkit-debugging/SKILL.md)** — Full debugging workflow and tools
- **[ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md)** — Correct implementation patterns
- **[ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md)** — Event bus, MVC, custom controls
- **[project-patterns.md](project-patterns.md)** — All 16 architecture patterns reference
