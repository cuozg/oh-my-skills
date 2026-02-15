# UI Toolkit Code Templates

> DC patterns → [project-patterns.md](project-patterns.md). QuizU patterns → [quizu-patterns.md](quizu-patterns.md). Theme tokens → `ui-toolkit-theming/SKILL.md`.

## 1. Base Screen (UXML + USS)

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement name="screen-root" class="screen">
    <ui:VisualElement name="header" class="header">
      <ui:Button name="btn-back" class="btn-icon btn-back"/>
      <ui:Label name="title" class="header-title" text="Title"/>
      <ui:VisualElement class="header-spacer"/>
    </ui:VisualElement>
    <ui:ScrollView name="content" class="content" mode="Vertical" horizontal-scroller-visibility="Hidden"/>
    <ui:VisualElement name="footer" class="footer"/>
  </ui:VisualElement>
</ui:UXML>
```

```css
.screen { flex-grow:1; flex-direction:column; }
.header { flex-direction:row; align-items:center; height:56px; padding:0 16px; flex-shrink:0; }
.content { flex-grow:1; }
.footer { flex-direction:row; height:64px; flex-shrink:0; }
```

## 2. UIScreen (QuizU Stack Nav)

```csharp
public abstract class UIScreen
{
    protected VisualElement m_RootElement, m_Screen;
    public UIScreen(VisualElement root) { m_RootElement = root; Initialize(); }
    protected abstract void Initialize();
    public virtual void Show() { m_Screen.RemoveFromClassList("screen-hidden"); m_Screen.AddToClassList("screen-visible"); }
    public virtual void Hide() { m_Screen.RemoveFromClassList("screen-visible"); m_Screen.AddToClassList("screen-hidden"); }
}
```

## 3. Custom Control (`[UxmlElement]`, Unity 6+)

> DC uses legacy `UxmlFactory`/`UxmlTraits` — see [project-patterns.md](project-patterns.md).

```csharp
[UxmlElement]
public partial class CustomCard : VisualElement
{
    [UxmlAttribute] public string Title { get => _title?.text ?? ""; set { if (_title != null) _title.text = value; } }
    Label _title;
    public CustomCard()
    {
        AddToClassList("custom-card");
        _title = new Label { name = "title" }; Add(_title);
        RegisterCallback<PointerDownEvent>(e => { ToggleInClassList("custom-card--selected"); e.StopPropagation(); });
    }
}
```

## 4. ListView + Virtualization

```csharp
_listView.itemsSource = _items;
_listView.fixedItemHeight = 72;
_listView.virtualizationMethod = CollectionVirtualizationMethod.FixedHeight;
_listView.makeItem = () => {
    var item = new VisualElement(); item.AddToClassList("list-item");
    item.Add(new Label { name = "title" }); item.Add(new Label { name = "subtitle" });
    return item;
};
_listView.bindItem = (el, i) => {
    el.Q<Label>("title").text = _items[i].Name;
    el.Q<Label>("subtitle").text = _items[i].Description;
};
_listView.unbindItem = (el, _) => el.RemoveFromClassList("list-item--highlighted");
```

## 5. Data Binding (Unity 6 Runtime)

```csharp
public class PlayerDataSource : ScriptableObject, IDataSource
{
    [SerializeField] int _health = 100, _maxHealth = 100;
    [CreateProperty] public int Health { get => _health; set { if (_health == value) return; _health = Mathf.Clamp(value, 0, _maxHealth); NotifyPropertyChanged(nameof(Health)); } }
    [CreateProperty] public float HealthPct => _maxHealth > 0 ? (float)_health / _maxHealth : 0f;
    public event System.EventHandler<BindablePropertyChangedEventArgs> propertyChanged;
    void NotifyPropertyChanged(string p) => propertyChanged?.Invoke(this, new BindablePropertyChangedEventArgs(p));
}

// Bind: root.dataSource = data;
// root.Q<ProgressBar>("hp").SetBinding("value", new DataBinding { dataSourcePath = new PropertyPath("HealthPct") });
```

## 6. SafeArea Handler

> DC uses `borderWidth` approach — see [project-patterns.md](project-patterns.md).

```csharp
[RequireComponent(typeof(UIDocument))]
public class SafeAreaHandler : MonoBehaviour
{
    void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement.Q("safe-area") ?? GetComponent<UIDocument>().rootVisualElement;
        root.RegisterCallback<GeometryChangedEvent>(_ => Apply(root));
        Apply(root);
    }
    void Apply(VisualElement r)
    {
        var sa = Screen.safeArea; float w = Screen.width, h = Screen.height;
        if (w <= 0 || h <= 0) return;
        r.style.paddingLeft = new Length(sa.x / w * 100f, LengthUnit.Percent);
        r.style.paddingRight = new Length((1f - sa.xMax / w) * 100f, LengthUnit.Percent);
        r.style.paddingTop = new Length((1f - sa.yMax / h) * 100f, LengthUnit.Percent);
        r.style.paddingBottom = new Length(sa.y / h * 100f, LengthUnit.Percent);
    }
}
```

## 7. Screen Manager (Stack Nav)

```csharp
public class UIScreenManager : MonoBehaviour
{
    [SerializeField] UIDocument _document;
    [SerializeField] List<VisualTreeAsset> _templates;
    readonly Stack<string> _stack = new();
    readonly Dictionary<string, VisualElement> _screens = new();
    VisualElement _container;
    void OnEnable() => _container = _document.rootVisualElement.Q("screen-container");
    public void Push(string name) { HideCurrent(); Show(name); _stack.Push(name); }
    public void Pop() { if (_stack.Count <= 1) return; Hide(_stack.Pop()); Show(_stack.Peek()); }
    void HideCurrent() { if (_stack.Count > 0) Hide(_stack.Peek()); }
    void Hide(string n) { if (_screens.TryGetValue(n, out var s)) s.style.display = DisplayStyle.None; }
    void Show(string name)
    {
        if (!_screens.TryGetValue(name, out var screen))
        {
            var tmpl = _templates.Find(t => t.name == name);
            if (tmpl == null) return;
            screen = tmpl.Instantiate(); screen.name = name; _container.Add(screen); _screens[name] = screen;
        }
        screen.style.display = DisplayStyle.Flex;
    }
}
```

## 8. EventRegistry (Disposable Cleanup)

```csharp
public class EventRegistry : IDisposable
{
    readonly List<Action> _unsubs = new();
    public void RegisterCallback<T>(VisualElement el, EventCallback<T> cb) where T : EventBase<T>, new()
    { el.RegisterCallback(cb); _unsubs.Add(() => el.UnregisterCallback(cb)); }
    public void Dispose() { foreach (var u in _unsubs) u?.Invoke(); _unsubs.Clear(); }
}
```

## 9. Element Pool

```csharp
public class VisualElementPool<T> where T : VisualElement, new()
{
    readonly Stack<T> _pool = new();
    public T Get() { var el = _pool.Count > 0 ? _pool.Pop() : new T(); el.style.display = DisplayStyle.Flex; return el; }
    public void Release(T el) { el.style.display = DisplayStyle.None; _pool.Push(el); }
}
```