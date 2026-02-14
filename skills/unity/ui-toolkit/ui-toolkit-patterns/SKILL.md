---
name: ui-toolkit-patterns
description: "Common UI patterns implemented in Unity UI Toolkit with complete UXML/USS/C# examples. Covers tabbed navigation, inventory grids, modal dialogs, stateful buttons, message lists, and scroll snapping. Use when: (1) Building tabbed interfaces, (2) Creating inventory or card grid layouts, (3) Implementing modal popups with backdrop, (4) Adding button states and loading spinners, (5) Building chat or mail list views, (6) Implementing horizontal scroll with page snap. Triggers: 'tab bar', 'inventory grid', 'modal popup', 'dialog overlay', 'button states', 'message list', 'scroll snap', 'UI pattern'."
---

# UI Toolkit Common Patterns

<!-- OWNERSHIP: Screen implementations (tabs, inventory, modals, mail, scroll snap), async Task animation, composite view pattern, ListView usage, CSS class toggling for state, Button.userData. -->

> **Based on**: Unity 6 (6000.0), [Dragon Crashers](../references/dragon-crashers-insights.md) official sample. Production-ready patterns with complete UXML, USS, and C#. Follows [architecture](../ui-toolkit-architecture/SKILL.md) principles: UXML=structure, USS=style, C#=behavior.

---

## 1. Tabbed Navigation

Tab bar with content switching and sliding indicator. Based on the [Dragon Crashers](../references/dragon-crashers-insights.md) pattern.

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement class="tab-view">
    <ui:VisualElement class="tab-bar">
      <ui:Button class="tab-bar__tab tab-bar__tab--active" name="tab-inventory" text="Inventory"/>
      <ui:Button class="tab-bar__tab" name="tab-skills" text="Skills"/>
      <ui:Button class="tab-bar__tab" name="tab-stats" text="Stats"/>
      <ui:VisualElement class="tab-bar__indicator"/>
    </ui:VisualElement>
    <ui:VisualElement class="tab-view__content">
      <ui:VisualElement name="content-inventory" class="tab-view__page"/>
      <ui:VisualElement name="content-skills" class="tab-view__page" style="display:none;"/>
      <ui:VisualElement name="content-stats" class="tab-view__page" style="display:none;"/>
    </ui:VisualElement>
  </ui:VisualElement>
</ui:UXML>
```

```css
:root { --tab-active: #4FC3F7; --tab-idle: #90A4AE; }
.tab-bar { flex-direction: row; border-bottom-width: 2px; border-bottom-color: rgba(255,255,255,0.1); }
.tab-bar__tab { flex-grow: 1; padding: 12px 0; background-color: rgba(0,0,0,0); border-width: 0; color: var(--tab-idle); font-size: 14px; -unity-font-style: bold; transition: color 0.2s; }
.tab-bar__tab:hover { color: #fff; }
.tab-bar__tab--active { color: var(--tab-active); }
.tab-bar__indicator { position: absolute; bottom: 0; height: 3px; width: 33.33%; background-color: var(--tab-active); transition: translate 0.25s ease-out; }
```

```csharp
public class TabViewController
{
    readonly List<Button> _tabs;
    readonly List<VisualElement> _pages;
    readonly VisualElement _indicator;
    int _activeIndex;

    public TabViewController(VisualElement root)
    {
        _tabs = root.Query<Button>(className: "tab-bar__tab").ToList();
        _pages = root.Query<VisualElement>(className: "tab-view__page").ToList();
        _indicator = root.Q(className: "tab-bar__indicator");
        for (int i = 0; i < _tabs.Count; i++)
        {
            int idx = i;
            _tabs[i].clicked += () => SelectTab(idx);
        }
        SelectTab(0);
    }

    public void SelectTab(int index)
    {
        _tabs[_activeIndex].RemoveFromClassList("tab-bar__tab--active");
        _pages[_activeIndex].style.display = DisplayStyle.None;
        _activeIndex = index;
        _tabs[_activeIndex].AddToClassList("tab-bar__tab--active");
        _pages[_activeIndex].style.display = DisplayStyle.Flex;
        _indicator.style.translate = new Translate(new Length(100f * index, LengthUnit.Percent), 0);
    }
}
```

### Dragon Crashers: Two Tab Approaches

DC uses two contrasting implementations — **Approach A** (reusable `TabbedMenuController` via naming convention) and **Approach B** (manual per-screen with domain events like `ShopView`). See [architecture skill](../ui-toolkit-architecture/SKILL.md#tabbedmenucontroller--convention-based-tab-switching) for full implementation. Use reusable for generic screens (Mail, Settings); use manual when tabs fire domain-specific events (Shop filters).

---

## 2. Inventory Grid

ListView-backed grid with item cards, selection state, and detail panel. See [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) for large-list virtualization.

UXML: `<ListView name="inventory-grid" fixed-item-height="90" selection-type="Single"/>` + detail panel with icon/name/desc labels.

```css
.inventory { flex-direction: row; flex-grow: 1; }
.inventory__grid { width: 65%; }
.item-card { width: 80px; height: 80px; margin: 4px; border-radius: 8px; background-color: rgba(255,255,255,0.06); align-items: center; justify-content: center; transition: scale 0.15s, background-color 0.15s; }
.item-card:hover { scale: 1.05; background-color: rgba(255,255,255,0.12); }
.item-card--selected { border-width: 2px; border-color: #4FC3F7; background-color: rgba(79,195,247,0.15); }
.item-card__icon { width: 48px; height: 48px; }
.item-card__qty { position: absolute; bottom: 4px; right: 6px; font-size: 11px; color: #ccc; }
.inventory__detail { width: 35%; padding: 16px; background-color: rgba(0,0,0,0.3); }
```

```csharp
public class InventoryGridController
{
    readonly ListView _grid;
    readonly VisualElement _detail;
    List<ItemData> _items;

    public InventoryGridController(VisualElement root, List<ItemData> items)
    {
        _items = items;
        _grid = root.Q<ListView>("inventory-grid");
        _detail = root.Q("detail-panel");
        _grid.makeItem = () => {
            var card = new VisualElement(); card.AddToClassList("item-card");
            var icon = new VisualElement(); icon.AddToClassList("item-card__icon");
            var qty = new Label(); qty.AddToClassList("item-card__qty");
            card.Add(icon); card.Add(qty);
            return card;
        };
        _grid.bindItem = (el, i) => {
            el.Q("icon").style.backgroundImage = new StyleBackground(_items[i].Icon);
            el.Q<Label>("qty").text = _items[i].Quantity > 1 ? $"x{_items[i].Quantity}" : "";
        };
        _grid.itemsSource = _items;
        _grid.selectionChanged += sel => {
            if (sel.FirstOrDefault() is not ItemData item) return;
            _detail.Q<Label>(className: "detail__name").text = item.Name;
            _detail.Q<Label>(className: "detail__desc").text = item.Description;
        };
    }
}
```

### Dragon Crashers: ScrollView + VisualTreeAsset (Not ListView)

DC uses `ScrollView` with manual `VisualTreeAsset.Instantiate()` loops instead of `ListView` — no virtualization, simpler for small fixed sets. See [dragon-crashers-insights.md](../references/dragon-crashers-insights.md).

> **Decision**: Use `ListView` for 100+ items (virtualization). Use `ScrollView` + `Instantiate()` for smaller fixed sets where you need full item lifecycle control.

---

## 3. Modal / Popup Dialog

Overlay with backdrop click-to-close and animated show/hide via `translate` + `opacity`.

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement name="modal-overlay" class="modal-overlay" style="display:none;">
    <ui:VisualElement class="modal-backdrop"/>
    <ui:VisualElement class="modal-dialog">
      <ui:Label class="modal__title" text="Confirm"/>
      <ui:Label class="modal__body" text="Are you sure?"/>
      <ui:VisualElement class="modal__actions">
        <ui:Button name="btn-cancel" class="modal__btn--secondary" text="Cancel"/>
        <ui:Button name="btn-confirm" class="modal__btn--primary" text="OK"/>
      </ui:VisualElement>
    </ui:VisualElement>
  </ui:VisualElement>
</ui:UXML>
```

```css
.modal-overlay { position: absolute; left: 0; top: 0; right: 0; bottom: 0; align-items: center; justify-content: center; }
.modal-backdrop { position: absolute; left: 0; top: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.5); opacity: 0; transition: opacity 0.2s; }
.modal-backdrop--visible { opacity: 1; }
.modal-dialog { width: 360px; padding: 24px; border-radius: 12px; background-color: #263238; translate: 0 30px; opacity: 0; transition: translate 0.25s ease-out, opacity 0.2s; }
.modal-dialog--visible { translate: 0 0; opacity: 1; }
.modal__actions { flex-direction: row; justify-content: flex-end; }
.modal__btn--secondary { padding: 8px 20px; border-radius: 6px; background-color: #455A64; color: #CFD8DC; margin-left: 8px; }
.modal__btn--primary { padding: 8px 20px; border-radius: 6px; background-color: #4FC3F7; color: #0D1B2A; margin-left: 8px; }
```

```csharp
public class ModalController
{
    readonly VisualElement _overlay, _backdrop, _dialog;
    Action _onConfirm;

    public ModalController(VisualElement root)
    {
        _overlay = root.Q("modal-overlay");
        _backdrop = root.Q(className: "modal-backdrop");
        _dialog = root.Q(className: "modal-dialog");
        _backdrop.RegisterCallback<ClickEvent>(_ => Hide());
        root.Q<Button>("btn-cancel").clicked += Hide;
        root.Q<Button>("btn-confirm").clicked += () => { _onConfirm?.Invoke(); Hide(); };
    }

    public void Show(string title, string body, Action onConfirm)
    {
        _overlay.Q<Label>(className: "modal__title").text = title;
        _overlay.Q<Label>(className: "modal__body").text = body;
        _onConfirm = onConfirm;
        _overlay.style.display = DisplayStyle.Flex;
        _overlay.schedule.Execute(() =>
        {
            _backdrop.AddToClassList("modal-backdrop--visible");
            _dialog.AddToClassList("modal-dialog--visible");
        });
    }

    public void Hide()
    {
        _backdrop.RemoveFromClassList("modal-backdrop--visible");
        _dialog.RemoveFromClassList("modal-dialog--visible");
        _dialog.schedule.Execute(() => _overlay.style.display = DisplayStyle.None).ExecuteLater(300);
    }
}
```

### Dragon Crashers: Modal vs Overlay Navigation

DC implements two navigation modes in `UIManager`: **modal** (replaces view) and **overlay** (shows on top, restores previous). See [architecture skill](../ui-toolkit-architecture/SKILL.md#uimanager--centralized-view-orchestration).

DC also uses `experimental.animation.Scale(1f, 200)` for pop-in on show — prefer USS transitions for easing control.

---

## 4. Stateful Buttons

USS pseudo-classes for normal/hover/active/disabled + loading spinner via class toggle.

```css
.btn-primary { padding: 10px 24px; border-radius: 8px; border-width: 0; background-color: #4FC3F7; color: #0D1B2A; font-size: 14px; -unity-font-style: bold; transition: background-color 0.15s, scale 0.1s; }
.btn-primary:hover { background-color: #29B6F6; scale: 1.03; }
.btn-primary:active { background-color: #0288D1; scale: 0.97; }
.btn-primary:disabled { background-color: #37474F; color: #607D8B; }
.btn-primary.btn--loading { background-color: #37474F; }
.btn-primary.btn--loading .btn__label { visibility: hidden; }
.btn-primary.btn--loading .btn__spinner { display: flex; }
.btn__spinner { display: none; position: absolute; width: 20px; height: 20px; border-width: 3px; border-color: rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; }
```

```csharp
public class StatefulButton
{
    readonly Button _button;
    readonly VisualElement _spinner;
    IVisualElementScheduledItem _spinAnim;

    public StatefulButton(Button button)
    {
        _button = button;
        _button.AddToClassList("btn-primary");
        _button.Q<Label>()?.AddToClassList("btn__label");
        _spinner = new VisualElement();
        _spinner.AddToClassList("btn__spinner");
        _button.Add(_spinner);
    }

    public void SetLoading(bool loading)
    {
        _button.SetEnabled(!loading);
        _button.EnableInClassList("btn--loading", loading);
        if (loading)
        {
            float angle = 0f;
            _spinAnim = _button.schedule.Execute(() =>
            {
                angle = (angle + 15f) % 360f;
                _spinner.style.rotate = new Rotate(angle);
            }).Every(16);
        }
        else { _spinAnim?.Pause(); _spinAnim = null; }
    }
}
```

### Dragon Crashers: Button State via CSS Class Toggle

DC manages button state through CSS class toggling (`AddToClassList`/`RemoveFromClassList`) + centralized `AudioManager.PlayDefaultButtonSound()`. See [dragon-crashers-insights.md](../references/dragon-crashers-insights.md).

---

## 5. Message List (Mail/Chat)

ListView with read/unread states, swipe gesture, and badge counter.

UXML: Header with title + badge `<Label name="badge-count"/>`, `<ListView name="message-list" fixed-item-height="72"/>`.

```css
.msg-row { flex-direction: row; padding: 12px 16px; align-items: center; border-bottom-width: 1px; border-bottom-color: rgba(255,255,255,0.06); transition: translate 0.2s, opacity 0.2s; }
.msg-row--unread { background-color: rgba(79,195,247,0.08); }
.msg-row--swiped { translate: -100% 0; opacity: 0; }
.msg__dot { width: 8px; height: 8px; border-radius: 4px; background-color: #4FC3F7; margin-right: 12px; }
.msg__dot--read { opacity: 0; }
.mail-header__badge { width: 24px; height: 24px; border-radius: 12px; background-color: #EF5350; align-items: center; justify-content: center; }
```

```csharp
public class MessageListController
{
    readonly ListView _list;
    readonly Label _badge;
    List<MessageData> _messages;

    public MessageListController(VisualElement root, List<MessageData> messages)
    {
        _messages = messages;
        _list = root.Q<ListView>("message-list");
        _badge = root.Q<Label>("badge-count");
        _list.makeItem = () => {
            var row = new VisualElement(); row.AddToClassList("msg-row");
            row.Add(new VisualElement { classList = { "msg__dot" } });
            var content = new VisualElement();
            content.Add(new Label { name = "sender" });
            content.Add(new Label { name = "preview" });
            row.Add(content);
            row.Add(new Label { name = "time" });
            // Swipe-to-dismiss
            float startX = 0;
            row.RegisterCallback<PointerDownEvent>(e => startX = e.position.x);
            row.RegisterCallback<PointerUpEvent>(e => {
                if (startX - e.position.x > 80) row.AddToClassList("msg-row--swiped");
            });
            return row;
        };
        _list.bindItem = (el, i) => {
            var msg = _messages[i];
            el.Q<Label>("sender").text = msg.Sender;
            el.Q<Label>("preview").text = msg.Preview;
            el.Q<Label>("time").text = msg.TimeAgo;
            el.EnableInClassList("msg-row--unread", !msg.IsRead);
            el.Q(className: "msg__dot").EnableInClassList("msg__dot--read", msg.IsRead);
        };
        _list.itemsSource = _messages;
        _badge.text = _messages.Count(m => !m.IsRead).ToString();
    }
}
```

### Dragon Crashers: Composite Mail System

DC's mail uses a **composite view** (`MailView` → 3 children), `MailScreenController` with LINQ sort, and `MailEvents` bus (11 delegates). See [architecture skill](../ui-toolkit-architecture/SKILL.md#composite-view-pattern) and [dragon-crashers-insights.md](../references/dragon-crashers-insights.md).

---

## 6. Scroll View with Snap

Horizontal carousel with page snapping and indicator dots.

UXML: `<ScrollView name="carousel-scroll" mode="Horizontal" horizontal-scroller-visibility="Hidden"/>` + `<VisualElement name="carousel-dots"/>`.

```css
.carousel__scroll #unity-content-container { flex-direction: row; flex-wrap: nowrap; }
.carousel__page { width: 100%; flex-shrink: 0; padding: 24px; }
.dot { width: 8px; height: 8px; border-radius: 4px; background-color: rgba(255,255,255,0.3); margin: 0 4px; transition: background-color 0.2s, scale 0.15s; }
.dot--active { background-color: #4FC3F7; scale: 1.3; }
```

```csharp
public class SnapCarouselController
{
    readonly ScrollView _scroll;
    readonly List<VisualElement> _dots = new();
    int _pageCount, _currentPage;

    public SnapCarouselController(VisualElement root, int pageCount)
    {
        _pageCount = pageCount;
        _scroll = root.Q<ScrollView>("carousel-scroll");
        var dotsContainer = root.Q("carousel-dots");
        for (int i = 0; i < pageCount; i++)
        {
            var page = new VisualElement(); page.AddToClassList("carousel__page");
            _scroll.contentContainer.Add(page);
            var dot = new VisualElement(); dot.AddToClassList("dot");
            int idx = i; dot.RegisterCallback<ClickEvent>(_ => SnapToPage(idx));
            dotsContainer.Add(dot); _dots.Add(dot);
        }
        _scroll.RegisterCallback<GeometryChangedEvent>(_ => SnapToPage(0));
        _scroll.horizontalScroller.valueChanged += v => {
            float pw = _scroll.contentContainer.resolvedStyle.width / _pageCount;
            if (pw > 0) { int n = Mathf.Clamp(Mathf.RoundToInt(v / pw), 0, _pageCount - 1); if (n != _currentPage) UpdateDots(n); }
        };
        UpdateDots(0);
    }

    public void SnapToPage(int i) { _scroll.scrollOffset = new Vector2(_scroll.contentContainer.resolvedStyle.width / _pageCount * i, 0); UpdateDots(i); }
    void UpdateDots(int a) { _dots[_currentPage].RemoveFromClassList("dot--active"); _currentPage = a; _dots[a].AddToClassList("dot--active"); }
}
```

---

## 7. Async Task Animation (Non-MonoBehaviour)

DC's `UIView` classes are plain C# (not MonoBehaviour), so they use `async Task`. Fire-and-forget (`_ = MethodAsync()`) — ⚠️ wrap in `try/catch`.

```csharp
// Typewriter — fixed-interval (ChatView). Task.Delay ignores timeScale.
async Task TypewriterRoutine(Label label, string text) {
    label.text = ""; foreach (char c in text) { label.text += c; await Task.Delay(20); }
}
// Counter lerp — frame-synced (OptionsBarView). Respects timeScale via deltaTime.
async Task LerpCounterAsync(Label label, int start, int end, float dur) {
    float elapsed = 0f;
    while (elapsed < dur) { elapsed += Time.deltaTime; label.text = ((int)Mathf.Lerp(start, end, Mathf.Clamp01(elapsed / dur))).ToString(); await Task.Delay(TimeSpan.FromSeconds(Time.deltaTime)); }
    label.text = end.ToString();
}
// Progress bar — Stopwatch + Yield for frame-independent timing (LevelMeterView)
async Task UpdateLevelAsync(float target, float lerpTime) {
    float start = m_LevelProgress; var sw = System.Diagnostics.Stopwatch.StartNew();
    while (sw.Elapsed.TotalSeconds < lerpTime) { float t = (float)(sw.Elapsed.TotalSeconds / lerpTime); m_ProgressBar.style.width = new Length(Mathf.Lerp(start, target, t) * 100f, LengthUnit.Percent); await Task.Yield(); }
}
```

| Strategy | `timeScale` | Best For |
|---|---|---|
| `Task.Delay(ms)` | Ignores | Typewriter, fixed-rate |
| `Task.Delay(deltaTime)` | Respects | Counter lerps |
| `Stopwatch` + `Yield()` | Ignores | Progress bars, precise |

---

## 8. Experimental Animation API

```csharp
// Position — slide marker to target (MenuBarView.cs). Requires coordinate conversion.
void AnimateMarkerToTarget(VisualElement target, int ms = 200) {
    Vector2 world = target.parent.LocalToWorld(target.layout.position);
    Vector3 local = m_MenuMarker.parent.WorldToLocal(world);
    m_MenuMarker.experimental.animation.Position(local - new Vector3(m_MenuMarker.resolvedStyle.width / 2f, 0, 0), ms);
}
// Scale — pop-in effect
element.transform.scale = new Vector3(0.1f, 0.1f, 1f);
element.experimental.animation.Scale(1f, 200);
```

**Click Cooldown Guard**: Prevent rapid re-triggers during animation:
```csharp
float m_NextClick = 0f;
void OnClicked(ClickEvent evt) { if (Time.time < m_NextClick) return; m_NextClick = Time.time + 0.2f; /* animate */ }
```

---

## 9. GeometryChangedEvent & Composite View

**GeometryChangedEvent**: `layout.position`/`resolvedStyle` return zero until layout. Register → fire once → unregister. See [architecture skill](../ui-toolkit-architecture/SKILL.md#geometrychangedevent--deferred-layout-initialization).
**Composite View**: Split complex screens into parent + child `UIView`s. Parent injects containers via `Q()`, delegates lifecycle. 2 levels max. See [architecture skill](../ui-toolkit-architecture/SKILL.md#composite-view-pattern).

---

## 10. World-to-Panel Positioning

```csharp
void UpdateHealthBarPosition(VisualElement element, Vector3 worldPos, Vector2 worldSize) {
    if (element.panel == null) return;
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(
        element.panel, worldPos, worldSize, Camera.main);
    element.transform.position = rect.position;
    element.style.width = rect.width;
    element.style.height = rect.height;
}
```

> Call every frame via `Update()` or `schedule.Execute().Every(16)`. Check `element.panel != null` — null when detached.

---

## Animation Decision Matrix

| Technique | Easing | Cancel | Best For |
|---|---|---|---|
| **USS `transition`** | ✅ `ease-*` | Remove class | State changes (hover, show/hide) |
| **USS class toggle** | ✅ via transition | `RemoveFromClassList` | Binary states, theme-aware |
| **`experimental.animation`** | ❌ linear | `.Stop()` | Position/scale slides |
| **`async Task`** | Manual Lerp | `CancellationToken` | Non-MonoBehaviour multi-step |
| **`IVisualElementScheduledItem`** | Manual | `.Pause()` | Repeating timers, delayed callbacks |

> Only animate **transform properties** (`translate`, `scale`, `opacity`, `rotate`). Set `usageHints = DynamicTransform` on animated elements. See [performance skill](../ui-toolkit-performance/SKILL.md).

```css
/* USS transition example */
.panel { translate: 0 30px; opacity: 0; transition: translate 0.25s ease-out, opacity 0.2s; }
.panel--visible { translate: 0 0; opacity: 1; }
```

## Quick Reference

| Pattern | Key API | DC Example |
|---------|---------|------------|
| Tabs | `tab-bar__tab--active`, indicator translate | `TabbedMenuController` |
| Inventory | ListView `makeItem`/`bindItem` | `InventoryView` ScrollView |
| Modal | `--visible` class toggle, backdrop | `UIManager.ShowModalView()` |
| Buttons | `:hover/:active/:disabled`, `.btn--loading` | CSS class toggle |
| Messages | `msg-row--unread/--swiped`, ListView | `MailView` composite |
| Carousel | `dot--active`, scrollOffset snap | — (generic) |
| Async Anims | `_ = MethodAsync()`, `Task.Delay` | `ChatView`, `LevelMeterView` |
| Experimental | `.Position()`, `.Scale()` | `MenuBarView` marker |
| Composite View | Parent injects containers to children | `MailView` → 3 children |

## Related Skills & Resources

- [Architecture](../ui-toolkit-architecture/SKILL.md) — UIView base class, event bus, view lifecycle
- [Performance](../ui-toolkit-performance/SKILL.md) — animation cost, virtualization
- [Mobile](../ui-toolkit-mobile/SKILL.md) — touch patterns, safe area
- [Code Templates](../references/code-templates.md) | [Dragon Crashers](../references/dragon-crashers-insights.md) | [QuizU Patterns](../references/quizu-patterns.md)

---

**← Previous**: [Data Binding](../ui-toolkit-databinding/SKILL.md) | **Next →**: [Performance](../ui-toolkit-performance/SKILL.md)
