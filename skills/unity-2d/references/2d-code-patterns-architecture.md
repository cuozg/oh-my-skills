# 2D Physics & Advanced Patterns

## ContactFilter2D Pattern

```csharp
[RequireComponent(typeof(Rigidbody2D))]
public class ContactChecker : MonoBehaviour
{
    private Rigidbody2D _rb;
    private ContactFilter2D _filter;
    
    private void Start()
    {
        _rb = GetComponent<Rigidbody2D>();
        _filter.useTriggers = false;
        _filter.useLayerMask = true;
        _filter.layerMask = LayerMask.GetMask("Enemy");
    }
    
    public void CheckCollisions()
    {
        Collider2D[] results = new Collider2D[10];
        _rb.OverlapCollider(_filter, results);
        foreach (var col in results)
        {
            if (col != null) Debug.Log($"Hit: {col.name}");
        }
    }
}
```

## Sprite Animation Controller

```csharp
public class SpriteAnimationController : MonoBehaviour
{
    [SerializeField] private SpriteRenderer _spriteRenderer;
    [SerializeField] private Sprite[] _idleFrames;
    [SerializeField] private Sprite[] _runFrames;
    [SerializeField] private float _frameDuration = 0.1f;
    
    private int _currentFrame;
    private float _frameTimer;
    private Sprite[] _currentAnimation;
    
    private void Update()
    {
        _frameTimer -= Time.deltaTime;
        if (_frameTimer <= 0)
        {
            _frameTimer = _frameDuration;
            _currentFrame = (_currentFrame + 1) % _currentAnimation.Length;
            _spriteRenderer.sprite = _currentAnimation[_currentFrame];
        }
    }
    
    public void PlayAnimation(Sprite[] frames) => _currentAnimation = frames;
}
```

## Pixel Perfect Camera Setup

```csharp
public class PixelPerfectCameraSetup : MonoBehaviour
{
    [SerializeField] private Camera _camera;
    [SerializeField] private int _pixelsPerUnit = 16;
    
    private void Start()
    {
        _camera.orthographicSize = Screen.height / (2f * _pixelsPerUnit);
    }
}
```

## Tilemap Architecture Pattern

Use ScriptableObject to define tilemap layers and properties:

```csharp
[CreateAssetMenu]
public class TilemapConfig : ScriptableObject
{
    public string layerName;
    public int renderingOrder;
    public TileBase[] allowedTiles;
}
```

Assign configs to Tilemaps for modular level design and easy prefab reuse.
