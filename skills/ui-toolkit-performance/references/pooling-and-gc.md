# Element Pooling & GC-Free Patterns

Reduce memory allocations and improve performance by reusing UI elements and caching values.

## Element Pooling

Generic pool for VisualElement subclasses.

```csharp
public class VisualElementPool<T> where T : VisualElement, new() {
    readonly Stack<T> _pool = new();
    readonly Action<T> _onGet, _onRelease;
    
    public VisualElementPool(Action<T> onGet = null, Action<T> onRelease = null, int prewarm = 0) {
        _onGet = onGet; _onRelease = onRelease;
        for (int i = 0; i < prewarm; i++) _pool.Push(new T());
    }
    
    public T Get() {
        var el = _pool.Count > 0 ? _pool.Pop() : new T();
        el.style.display = DisplayStyle.Flex;
        _onGet?.Invoke(el);
        return el;
    }
    
    public void Release(T el) {
        el.style.display = DisplayStyle.None;
        _onRelease?.Invoke(el);
        _pool.Push(el);
    }
}
```

**Usage:** Instantiate once in constructor, call `Get()` to lease, `Release()` to return.

## GC-Free Patterns

### Cache Q() Calls

```csharp
Label _scoreLabel;
void OnEnable() { _scoreLabel = root.Q<Label>("score"); }
void UpdateScore(int score) { _scoreLabel.text = score.ToString(); }
```

Call Q<T>() once in OnEnable or Awake; store reference; reuse.

### Avoid Boxing

```csharp
// WRONG: boxing
element.style.width = 100;

// RIGHT: explicit type
element.style.width = new Length(100, LengthUnit.Pixel);
```

### Cache Style Values

```csharp
static readonly StyleLength _width100 = new Length(100, LengthUnit.Percent);
static readonly StyleColor _colorRed = new StyleColor(Color.red);

void ApplyStyles() {
    element.style.width = _width100;
    element.style.backgroundColor = _colorRed;
}
```

### Method References Over Lambdas

```csharp
// WRONG: closure allocation per callback
button.RegisterCallback<ClickEvent>(evt => OnClick(evt));

// RIGHT: method reference, no closure
button.RegisterCallback<ClickEvent>(OnClick);
```

## Zero-Allocation String Updates

Cache ToString results; update only on change:

```csharp
int _cachedScore = -1;
void UpdateScoreLabel(int newScore) {
    if (_cachedScore == newScore) return;
    _cachedScore = newScore;
    _scoreLabel.text = newScore.ToString();
}
```
