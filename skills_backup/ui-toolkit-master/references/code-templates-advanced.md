# UI Toolkit Code Templates — Advanced

> See [code-templates.md](code-templates.md) for base templates (Base Screen, UIScreen, Custom Control, ListView, Data Binding, SafeArea).

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
