# Custom Controls

## UxmlElement Pattern (Unity 6+)

```csharp
using UnityEngine.UIElements;

[UxmlElement("stat-bar")]
public partial class StatBar : VisualElement
{
    [UxmlAttribute]
    public string label { get; set; } = "Health";

    [UxmlAttribute]
    public float value { get; set; } = 1f;

    [UxmlAttribute]
    public float maxValue { get; set; } = 1f;

    private Label _label;
    private VisualElement _fill;

    public StatBar()
    {
        AddToClassList("stat-bar");

        _label = new Label();
        _label.AddToClassList("stat-bar__label");
        Add(_label);

        var track = new VisualElement();
        track.AddToClassList("stat-bar__track");
        Add(track);

        _fill = new VisualElement();
        _fill.AddToClassList("stat-bar__fill");
        track.Add(_fill);
    }

    public void Refresh()
    {
        _label.text = label;
        float pct = maxValue > 0 ? value / maxValue : 0f;
        _fill.style.width = Length.Percent(pct * 100f);
    }
}
```

## Usage in UXML

```xml
<UXML xmlns="UnityEngine.UIElements">
  <stat-bar name="health-bar" label="HP" value="75" max-value="100" />
  <stat-bar name="mana-bar" label="MP" value="30" max-value="50" />
</UXML>
```

## USS for Custom Control

```css
.stat-bar {
  flex-direction: row;
  align-items: center;
  margin-bottom: var(--space-sm);
}

.stat-bar__label {
  width: 60px;
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.stat-bar__track {
  flex-grow: 1;
  height: 8px;
  background-color: var(--color-surface);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.stat-bar__fill {
  height: 100%;
  background-color: var(--color-primary);
  border-radius: var(--radius-sm);
}
```

## Guidelines

- Derive from `VisualElement` or built-in controls (`BaseField<T>`, `Button`)
- Add BEM classes in constructor: `AddToClassList("block")`, `AddToClassList("block__part")`
- Use `[UxmlAttribute]` for UXML-configurable properties (Unity 6+)
- Keep logic in the control; keep styling in USS
- Expose events for parent controllers: `public event Action<float> OnValueChanged`
- Call `Refresh()` or property setters to update visuals after data changes
- Pre-6.0 fallback: use `UxmlFactory`/`UxmlTraits` inner classes with attribute descriptions
