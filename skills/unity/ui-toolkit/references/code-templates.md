# UI Toolkit Code Templates

> **PURPOSE**: Production-ready, copy-paste templates using Unity 6+ APIs for your own projects.
> For **DC's actual implementation patterns** (what Dragon Crashers does), see [project-patterns.md](project-patterns.md).

Production-ready UXML, USS, and C# templates for common UI patterns.

## Table of Contents

1. [Base Screen Template](#base-screen-template)
2. [UIScreen Template (QuizU-style)](#uiscreen-template-quizu-style)
3. [Custom Control Template](#custom-control-template)
4. [ListView with Virtualization](#listview-with-virtualization)
5. [Data Binding Setup](#data-binding-setup)
6. [Theme Token System](#theme-token-system)
7. [SafeArea Handler](#safearea-handler)
8. [Screen Manager](#screen-manager)
9. [EventRegistry (Disposable Event Cleanup)](#eventregistry-disposable-event-cleanup)
10. [Element Pool](#element-pool)

---

## Base Screen Template

### UXML — `BaseScreen.uxml`

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements">
    <ui:VisualElement name="screen-root" class="screen">
        <!-- Header -->
        <ui:VisualElement name="header" class="header">
            <ui:Button name="btn-back" class="btn-icon btn-back" />
            <ui:Label name="title" class="header-title" text="Screen Title" />
            <ui:VisualElement class="header-spacer" />
        </ui:VisualElement>

        <!-- Content (scrollable) -->
        <ui:ScrollView name="content" class="content"
            mode="Vertical"
            horizontal-scroller-visibility="Hidden">
            <!-- Screen-specific content here -->
        </ui:ScrollView>

        <!-- Footer (optional) -->
        <ui:VisualElement name="footer" class="footer">
            <!-- Tab bar or action buttons -->
        </ui:VisualElement>
    </ui:VisualElement>
</ui:UXML>
```

### USS — `BaseScreen.uss`

```css
.screen {
    flex-grow: 1;
    flex-direction: column;
    background-color: var(--color-bg-primary);
}

.header {
    flex-direction: row;
    align-items: center;
    height: 56px;
    padding: 0 16px;
    background-color: var(--color-bg-header);
    flex-shrink: 0;
}

.header-title {
    flex-grow: 1;
    -unity-text-align: middle-center;
    font-size: var(--font-size-lg);
    color: var(--color-text-primary);
    -unity-font-style: bold;
}

.header-spacer {
    width: 40px; /* Balance back button */
}

.content {
    flex-grow: 1;
}

.footer {
    flex-direction: row;
    height: 64px;
    flex-shrink: 0;
    background-color: var(--color-bg-footer);
    border-top-width: 1px;
    border-top-color: var(--color-border);
}
```

---

## UIScreen Template (QuizU-style)

> **Pattern**: Single UIDocument with stack-based navigation. All screens are non-MonoBehaviour C# classes.
> See [quizu-patterns.md](quizu-patterns.md) for architecture details.

### C# — `UIScreen.cs` (Base Class)

```csharp
using UnityEngine.UIElements;

/// <summary>
/// Abstract screen base class (plain C#, not MonoBehaviour).
/// Show/Hide via USS class toggling for GPU-friendly transitions.
/// </summary>
public abstract class UIScreen
{
    protected VisualElement m_RootElement;
    protected VisualElement m_Screen;

    const string k_VisibleClass = "screen-visible";
    const string k_HiddenClass = "screen-hidden";

    public UIScreen(VisualElement rootElement)
    {
        m_RootElement = rootElement;
        Initialize();
    }

    protected abstract void Initialize();

    public virtual void Show()
    {
        m_Screen.RemoveFromClassList(k_HiddenClass);
        m_Screen.AddToClassList(k_VisibleClass);
    }

    public virtual void Hide()
    {
        m_Screen.RemoveFromClassList(k_VisibleClass);
        m_Screen.AddToClassList(k_HiddenClass);
    }
}
```

### C# — Concrete Screen Example

```csharp
public class MyGameScreen : UIScreen
{
    EventRegistry m_Events = new();

    public MyGameScreen(VisualElement rootElement) : base(rootElement) { }

    protected override void Initialize()
    {
        m_Screen = m_RootElement.Q("MyGameScreen");
        var startButton = m_Screen.Q<Button>("start-button");
        m_Events.RegisterCallback<ClickEvent>(startButton, OnStartClicked);
    }

    void OnStartClicked(ClickEvent evt) { /* handle click */ }

    public void Dispose() => m_Events.Dispose();
}
```

### USS — Screen Transitions

```css
.screen-visible {
    transition-property: all;
    transition-duration: 0.5s;
    transition-timing-function: ease-in-out;
    position: absolute;
}

.screen-hidden {
    transition-property: all;
    opacity: 0;
    transition-duration: 0.5s;
    transition-timing-function: ease;
    bottom: 100%;
    position: absolute;
}
```

---

## Custom Control Template

> **Unity 6+ API**: This template uses the `[UxmlElement]`/`[UxmlAttribute]` attribute-based API (recommended for Unity 6+).
> Dragon Crashers uses the older `UxmlFactory`/`UxmlTraits` pattern — see [project-patterns.md → Pattern #5](project-patterns.md#5-custom-controls-uxmlfactory--uxmltraits--legacy-pattern) for that approach.

### C# — `CustomCard.cs`

```csharp
using UnityEngine;
using UnityEngine.UIElements;

[UxmlElement]
public partial class CustomCard : VisualElement
{
    // Exposed UXML attributes
    [UxmlAttribute]
    public string Title
    {
        get => _titleLabel?.text ?? string.Empty;
        set { if (_titleLabel != null) _titleLabel.text = value; }
    }

    [UxmlAttribute]
    public string Description
    {
        get => _descLabel?.text ?? string.Empty;
        set { if (_descLabel != null) _descLabel.text = value; }
    }

    // USS class name convention
    public static readonly string ussClassName = "custom-card";
    public static readonly string ussSelectedClassName = "custom-card--selected";

    Label _titleLabel;
    Label _descLabel;
    VisualElement _icon;

    public CustomCard()
    {
        AddToClassList(ussClassName);

        // Build hierarchy
        _icon = new VisualElement { name = "icon" };
        _icon.AddToClassList($"{ussClassName}__icon");
        Add(_icon);

        var textContainer = new VisualElement();
        textContainer.AddToClassList($"{ussClassName}__text");
        Add(textContainer);

        _titleLabel = new Label { name = "title" };
        _titleLabel.AddToClassList($"{ussClassName}__title");
        textContainer.Add(_titleLabel);

        _descLabel = new Label { name = "description" };
        _descLabel.AddToClassList($"{ussClassName}__desc");
        textContainer.Add(_descLabel);

        // Register events
        RegisterCallback<PointerDownEvent>(OnPointerDown);
    }

    void OnPointerDown(PointerDownEvent evt)
    {
        ToggleInClassList(ussSelectedClassName);
        evt.StopPropagation();
    }
}
```

### USS — `CustomCard.uss`

```css
.custom-card {
    flex-direction: row;
    padding: 12px;
    margin: 4px 8px;
    border-radius: 8px;
    background-color: var(--color-bg-card);
    border-width: 1px;
    border-color: var(--color-border);
    transition-property: background-color, border-color;
    transition-duration: 150ms;
}

.custom-card:hover {
    background-color: var(--color-bg-card-hover);
    border-color: var(--color-primary);
}

.custom-card--selected {
    background-color: var(--color-bg-card-selected);
    border-color: var(--color-primary);
    border-width: 2px;
}

.custom-card__icon {
    width: 48px;
    height: 48px;
    margin-right: 12px;
    flex-shrink: 0;
    border-radius: 8px;
    background-color: var(--color-bg-icon);
}

.custom-card__text {
    flex-grow: 1;
    justify-content: center;
}

.custom-card__title {
    font-size: var(--font-size-md);
    color: var(--color-text-primary);
    -unity-font-style: bold;
}

.custom-card__desc {
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    margin-top: 4px;
}
```

---

## ListView with Virtualization

### C# — `VirtualizedListController.cs`

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UIElements;

public class VirtualizedListController
{
    readonly ListView _listView;
    List<ItemData> _items;

    public VirtualizedListController(VisualElement root, List<ItemData> items)
    {
        _items = items;
        _listView = root.Q<ListView>("item-list");
        SetupListView();
    }

    void SetupListView()
    {
        _listView.itemsSource = _items;
        _listView.fixedItemHeight = 72;          // Required for virtualization
        _listView.virtualizationMethod = CollectionVirtualizationMethod.FixedHeight;
        _listView.selectionType = SelectionType.Single;
        _listView.showAlternatingRowBackgrounds = AlternatingRowBackground.ContentOnly;

        _listView.makeItem = MakeItem;
        _listView.bindItem = BindItem;
        _listView.unbindItem = UnbindItem;

        _listView.selectedIndicesChanged += OnSelectionChanged;
    }

    VisualElement MakeItem()
    {
        var item = new VisualElement();
        item.AddToClassList("list-item");

        var icon = new VisualElement { name = "icon" };
        icon.AddToClassList("list-item__icon");
        item.Add(icon);

        var textContainer = new VisualElement();
        textContainer.AddToClassList("list-item__text");
        item.Add(textContainer);

        var title = new Label { name = "title" };
        title.AddToClassList("list-item__title");
        textContainer.Add(title);

        var subtitle = new Label { name = "subtitle" };
        subtitle.AddToClassList("list-item__subtitle");
        textContainer.Add(subtitle);

        return item;
    }

    void BindItem(VisualElement element, int index)
    {
        if (index < 0 || index >= _items.Count) return;

        var data = _items[index];
        element.Q<Label>("title").text = data.Name;
        element.Q<Label>("subtitle").text = data.Description;

        element.EnableInClassList("list-item--highlighted", data.IsHighlighted);
    }

    void UnbindItem(VisualElement element, int index)
    {
        // Clean up any event subscriptions or references
        element.RemoveFromClassList("list-item--highlighted");
    }

    void OnSelectionChanged(IEnumerable<int> indices)
    {
        foreach (var index in indices)
        {
            if (index >= 0 && index < _items.Count)
                Debug.Log($"Selected: {_items[index].Name}");
        }
    }

    // Refresh when data changes
    public void RefreshData(List<ItemData> newItems)
    {
        _items = newItems;
        _listView.itemsSource = _items;
        _listView.RefreshItems();
    }
}

[System.Serializable]
public class ItemData
{
    public string Name;
    public string Description;
    public Sprite Icon;
    public bool IsHighlighted;
}
```

---

## Data Binding Setup

### C# — `PlayerDataSource.cs` (Unity 6 Runtime Binding)

```csharp
using Unity.Properties;
using UnityEngine;
using UnityEngine.UIElements;

[CreateAssetMenu(fileName = "PlayerData", menuName = "Data/PlayerData")]
public class PlayerDataSource : ScriptableObject, IDataSource
{
    [SerializeField] string _playerName = "Hero";
    [SerializeField] int _level = 1;
    [SerializeField] int _health = 100;
    [SerializeField] int _maxHealth = 100;
    [SerializeField] float _experience = 0f;

    [CreateProperty]
    public string PlayerName
    {
        get => _playerName;
        set
        {
            if (_playerName == value) return;
            _playerName = value;
            NotifyPropertyChanged(nameof(PlayerName));
        }
    }

    [CreateProperty]
    public int Level
    {
        get => _level;
        set
        {
            if (_level == value) return;
            _level = value;
            NotifyPropertyChanged(nameof(Level));
        }
    }

    [CreateProperty]
    public int Health
    {
        get => _health;
        set
        {
            if (_health == value) return;
            _health = Mathf.Clamp(value, 0, _maxHealth);
            NotifyPropertyChanged(nameof(Health));
            NotifyPropertyChanged(nameof(HealthPercent));
        }
    }

    [CreateProperty]
    public int MaxHealth
    {
        get => _maxHealth;
        set
        {
            if (_maxHealth == value) return;
            _maxHealth = Mathf.Max(1, value);
            NotifyPropertyChanged(nameof(MaxHealth));
            NotifyPropertyChanged(nameof(HealthPercent));
        }
    }

    [CreateProperty]
    public float HealthPercent => _maxHealth > 0 ? (float)_health / _maxHealth : 0f;

    [CreateProperty]
    public float Experience
    {
        get => _experience;
        set
        {
            if (Mathf.Approximately(_experience, value)) return;
            _experience = Mathf.Clamp01(value);
            NotifyPropertyChanged(nameof(Experience));
        }
    }

    // IDataSource
    public event System.EventHandler<BindablePropertyChangedEventArgs> propertyChanged;

    void NotifyPropertyChanged(string propertyName)
    {
        propertyChanged?.Invoke(this, new BindablePropertyChangedEventArgs(propertyName));
    }
}
```

### C# — Binding in Controller

```csharp
void SetupBindings(VisualElement root, PlayerDataSource data)
{
    // Set data source on container — children inherit it
    root.dataSource = data;

    // Bind individual elements
    root.Q<Label>("player-name").SetBinding("text",
        new DataBinding { dataSourcePath = new PropertyPath("PlayerName") });

    root.Q<Label>("level-label").SetBinding("text",
        new DataBinding { dataSourcePath = new PropertyPath("Level") });

    root.Q<ProgressBar>("health-bar").SetBinding("value",
        new DataBinding { dataSourcePath = new PropertyPath("HealthPercent") });
}
```

---

## Theme Token System

### USS — `tokens.uss`

```css
:root {
    /* Colors — Primary Palette */
    --color-primary: #4A90D9;
    --color-primary-hover: #3A7BC8;
    --color-primary-active: #2A66B0;
    --color-secondary: #7B68EE;
    --color-accent: #FF6B6B;

    /* Colors — Background */
    --color-bg-primary: #1A1A2E;
    --color-bg-secondary: #16213E;
    --color-bg-card: #0F3460;
    --color-bg-card-hover: #154785;
    --color-bg-card-selected: #1A5AA0;
    --color-bg-header: #0D1B2A;
    --color-bg-footer: #0D1B2A;
    --color-bg-icon: rgba(255, 255, 255, 0.08);
    --color-bg-overlay: rgba(0, 0, 0, 0.6);

    /* Colors — Text */
    --color-text-primary: #FFFFFF;
    --color-text-secondary: #B0BEC5;
    --color-text-disabled: #546E7A;
    --color-text-accent: #FFD700;

    /* Colors — Border */
    --color-border: rgba(255, 255, 255, 0.1);
    --color-border-focus: var(--color-primary);

    /* Colors — Status */
    --color-success: #4CAF50;
    --color-warning: #FF9800;
    --color-error: #F44336;
    --color-info: #2196F3;

    /* Typography */
    --font-size-xs: 10px;
    --font-size-sm: 12px;
    --font-size-md: 14px;
    --font-size-lg: 18px;
    --font-size-xl: 24px;
    --font-size-xxl: 32px;

    /* Spacing */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 12px;
    --spacing-lg: 16px;
    --spacing-xl: 24px;
    --spacing-xxl: 32px;

    /* Border Radius */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-round: 999px;

    /* Shadows (via border or background layering) */
    --shadow-color: rgba(0, 0, 0, 0.3);

    /* Transitions */
    --transition-fast: 100ms;
    --transition-normal: 200ms;
    --transition-slow: 350ms;
}
```

---

## SafeArea Handler

> **Note**: This template uses a `padding`-based approach — a generic alternative suitable for most projects.
> Dragon Crashers uses a `borderWidth`-based approach (`SafeAreaBorder`) which avoids affecting child layout calculations.
> See [project-patterns.md → Pattern #15](project-patterns.md#15-safeareaborder-borderwidth-approach) for DC's approach,
> or [ui-toolkit-responsive SKILL](../ui-toolkit-responsive/SKILL.md) for a full comparison of both approaches.

### C# — `SafeAreaHandler.cs`

```csharp
using UnityEngine;
using UnityEngine.UIElements;

/// <summary>
/// Apply device safe area insets to a UI Toolkit root element (padding approach).
/// For borderWidth approach (Dragon Crashers pattern), see SafeAreaBorder.
/// Attach this to the same GameObject as UIDocument.
/// </summary>
[RequireComponent(typeof(UIDocument))]
public class SafeAreaHandler : MonoBehaviour
{
    VisualElement _root;

    void OnEnable()
    {
        var doc = GetComponent<UIDocument>();
        _root = doc.rootVisualElement.Q("safe-area") ?? doc.rootVisualElement;
        _root.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
        ApplySafeArea();
    }

    void OnDisable()
    {
        _root?.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    }

    void OnGeometryChanged(GeometryChangedEvent evt) => ApplySafeArea();

    void ApplySafeArea()
    {
        var safeArea = Screen.safeArea;
        var screenW = Screen.width;
        var screenH = Screen.height;

        if (screenW <= 0 || screenH <= 0) return;

        float left = safeArea.x / screenW * 100f;
        float right = (1f - (safeArea.xMax / screenW)) * 100f;
        float top = (1f - (safeArea.yMax / screenH)) * 100f;
        float bottom = safeArea.y / screenH * 100f;

        _root.style.paddingLeft = new Length(left, LengthUnit.Percent);
        _root.style.paddingRight = new Length(right, LengthUnit.Percent);
        _root.style.paddingTop = new Length(top, LengthUnit.Percent);
        _root.style.paddingBottom = new Length(bottom, LengthUnit.Percent);
    }
}
```

---

## Screen Manager

### C# — `UIScreenManager.cs`

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UIElements;

/// <summary>
/// Manages screen transitions with stack-based navigation.
/// </summary>
public class UIScreenManager : MonoBehaviour
{
    [SerializeField] UIDocument _document;
    [SerializeField] List<VisualTreeAsset> _screenTemplates;

    readonly Stack<string> _screenStack = new();
    readonly Dictionary<string, VisualElement> _screens = new();

    VisualElement _container;

    void OnEnable()
    {
        _container = _document.rootVisualElement.Q("screen-container");
    }

    /// <summary>Push a new screen onto the stack (hides current).</summary>
    public void Push(string screenName)
    {
        if (_screens.TryGetValue(_screenStack.Peek(), out var current))
            current.style.display = DisplayStyle.None;

        ShowScreen(screenName);
        _screenStack.Push(screenName);
    }

    /// <summary>Pop current screen, reveal previous.</summary>
    public void Pop()
    {
        if (_screenStack.Count <= 1) return; // Don't pop the root

        var top = _screenStack.Pop();
        if (_screens.TryGetValue(top, out var topElement))
            topElement.style.display = DisplayStyle.None;

        if (_screens.TryGetValue(_screenStack.Peek(), out var prev))
            prev.style.display = DisplayStyle.Flex;
    }

    /// <summary>Replace entire stack with a single screen.</summary>
    public void Replace(string screenName)
    {
        foreach (var s in _screens.Values)
            s.style.display = DisplayStyle.None;

        _screenStack.Clear();
        ShowScreen(screenName);
        _screenStack.Push(screenName);
    }

    void ShowScreen(string screenName)
    {
        if (!_screens.TryGetValue(screenName, out var screen))
        {
            // Instantiate from template
            var template = _screenTemplates.Find(t => t.name == screenName);
            if (template == null)
            {
                Debug.LogError($"[UIScreenManager] Template not found: {screenName}");
                return;
            }

            screen = template.Instantiate();
            screen.name = screenName;
            screen.AddToClassList("screen");
            _container.Add(screen);
            _screens[screenName] = screen;
        }

        screen.style.display = DisplayStyle.Flex;
    }
}
```

---

## EventRegistry (Disposable Event Cleanup)

> **Pattern from QuizU**: Tracks all event subscriptions for batch cleanup. Eliminates manual `+=`/`-=` tracking.
> See [quizu-patterns.md → Pattern #4](quizu-patterns.md#4-eventregistry-idisposable-event-cleanup).

### C# — `EventRegistry.cs`

```csharp
using System;
using System.Collections.Generic;
using UnityEngine.UIElements;

/// <summary>
/// IDisposable utility for safe event cleanup.
/// Register events via this class; Dispose() unsubscribes all at once.
/// </summary>
public class EventRegistry : IDisposable
{
    readonly List<Action> m_Unsubscribers = new();

    /// <summary>Register a static Action delegate handler.</summary>
    public void Register<T>(Action<T> handler, ref Action<T> eventDelegate)
    {
        eventDelegate += handler;
        var del = eventDelegate; // capture for unsubscribe
        m_Unsubscribers.Add(() => del -= handler);
    }

    /// <summary>Register a UI Toolkit event callback.</summary>
    public void RegisterCallback<TEvent>(VisualElement element,
        EventCallback<TEvent> callback) where TEvent : EventBase<TEvent>, new()
    {
        element.RegisterCallback(callback);
        m_Unsubscribers.Add(() => element.UnregisterCallback(callback));
    }

    public void Dispose()
    {
        foreach (var unsub in m_Unsubscribers)
            unsub?.Invoke();
        m_Unsubscribers.Clear();
    }
}
```

### Usage

```csharp
public class MyView : IDisposable
{
    readonly EventRegistry m_Events = new();

    public MyView(VisualElement root)
    {
        var btn = root.Q<Button>("my-button");
        m_Events.RegisterCallback<ClickEvent>(btn, OnClicked);
        // No need to manually track unsubscription
    }

    void OnClicked(ClickEvent evt) { /* handle */ }

    public void Dispose() => m_Events.Dispose(); // Cleans up everything
}
```

---

## Element Pool

### C# — `VisualElementPool.cs`

```csharp
using System;
using System.Collections.Generic;
using UnityEngine.UIElements;

/// <summary>
/// Object pool for VisualElements to reduce GC pressure.
/// Typical use: notification toasts, floating damage numbers, chat messages.
/// </summary>
public class VisualElementPool<T> where T : VisualElement, new()
{
    readonly Stack<T> _pool = new();
    readonly Action<T> _onGet;
    readonly Action<T> _onRelease;

    public int CountActive { get; private set; }
    public int CountInactive => _pool.Count;

    public VisualElementPool(Action<T> onGet = null, Action<T> onRelease = null, int prewarm = 0)
    {
        _onGet = onGet;
        _onRelease = onRelease;

        for (int i = 0; i < prewarm; i++)
            _pool.Push(new T());
    }

    public T Get()
    {
        var element = _pool.Count > 0 ? _pool.Pop() : new T();
        element.style.display = DisplayStyle.Flex;
        _onGet?.Invoke(element);
        CountActive++;
        return element;
    }

    public void Release(T element)
    {
        element.style.display = DisplayStyle.None;
        _onRelease?.Invoke(element);
        _pool.Push(element);
        CountActive--;
    }

    public void Clear()
    {
        _pool.Clear();
        CountActive = 0;
    }
}
```
