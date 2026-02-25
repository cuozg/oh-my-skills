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

See [code-templates-advanced.md](code-templates-advanced.md) for Screen Manager, EventRegistry, and Element Pool patterns.
