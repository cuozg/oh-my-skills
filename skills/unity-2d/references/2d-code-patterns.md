# 2D Code Patterns & Project Setup

## Project Setup

### Sorting Layers (Back to Front)
```
Background → Midground → Default → Foreground → UI
Priority: Sorting Layer > Order in Layer > Z position
```

### Sprite Import Settings

| Art Style | Filter | Compression | PPU | Max Size |
|:--|:--|:--|:--|:--|
| Pixel 16x16 | Point | None | 16 | 256–512 |
| Pixel 32x32 | Point | None | 32 | 512–1024 |
| HD hand-drawn | Bilinear | ASTC 6x6 / BC7 | 100 | 2048–4096 |
| Vector-style | Bilinear | ASTC 4x4 / BC7 | 100 | 2048 |

Sprite sheet: Mode=Multiple, Mesh=FullRect (pixel) or Tight (HD), Generate Physics Shape=Yes.

## Key Patterns

### 2D Platformer Controller

```csharp
[RequireComponent(typeof(Rigidbody2D))]
[RequireComponent(typeof(CapsuleCollider2D))]
public class PlatformerController2D : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float _moveSpeed = 8f;
    [SerializeField] private float _acceleration = 60f;
    [SerializeField] private float _deceleration = 40f;

    [Header("Jump")]
    [SerializeField] private float _jumpForce = 14f;
    [SerializeField] private float _fallMultiplier = 2.5f;
    [SerializeField] private float _lowJumpMultiplier = 2f;
    [SerializeField] private float _coyoteTime = 0.1f;
    [SerializeField] private float _jumpBufferTime = 0.1f;

    [Header("Ground Check")]
    [SerializeField] private Transform _groundCheck;
    [SerializeField] private float _groundCheckRadius = 0.15f;
    [SerializeField] private LayerMask _groundLayer;

    private Rigidbody2D _rb;
    private float _moveInput;
    private bool _isGrounded;
    private float _lastGroundedTime;
    private float _lastJumpPressedTime;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody2D>();
        _rb.freezeRotation = true;
        _rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
    }

    private void Update()
    {
        _moveInput = Input.GetAxisRaw("Horizontal");
        if (Input.GetButtonDown("Jump"))
            _lastJumpPressedTime = _jumpBufferTime;
        _lastJumpPressedTime -= Time.deltaTime;
        _lastGroundedTime -= Time.deltaTime;
    }

    private void FixedUpdate()
    {
        _isGrounded = Physics2D.OverlapCircle(
            _groundCheck.position, _groundCheckRadius, _groundLayer);
        if (_isGrounded) _lastGroundedTime = _coyoteTime;
        ApplyMovement();
        ApplyJump();
        ApplyBetterJumpGravity();
    }

    private void ApplyMovement()
    {
        float targetSpeed = _moveInput * _moveSpeed;
        float speedDiff = targetSpeed - _rb.linearVelocity.x;
        float accelRate = Mathf.Abs(targetSpeed) > 0.01f ? _acceleration : _deceleration;
        _rb.AddForce(Vector2.right * speedDiff * accelRate);
    }

    private void ApplyJump()
    {
        if (_lastJumpPressedTime > 0 && _lastGroundedTime > 0)
        {
            _rb.linearVelocity = new Vector2(_rb.linearVelocity.x, _jumpForce);
            _lastJumpPressedTime = 0;
            _lastGroundedTime = 0;
        }
    }

    private void ApplyBetterJumpGravity()
    {
        if (_rb.linearVelocity.y < 0)
            _rb.linearVelocity += Vector2.up * (Physics2D.gravity.y * (_fallMultiplier - 1) * Time.fixedDeltaTime);
        else if (_rb.linearVelocity.y > 0 && !Input.GetButton("Jump"))
            _rb.linearVelocity += Vector2.up * (Physics2D.gravity.y * (_lowJumpMultiplier - 1) * Time.fixedDeltaTime);
    }
}
```

### Tilemap Scripting

```csharp
using UnityEngine.Tilemaps;

public class TilemapController : MonoBehaviour
{
    [SerializeField] private Tilemap _tilemap;
    [SerializeField] private TileBase _groundTile;
    [SerializeField] private TileBase _wallTile;

    public void PlaceTile(Vector3 worldPos, TileBase tile) =>
        _tilemap.SetTile(_tilemap.WorldToCell(worldPos), tile);

    public void RemoveTile(Vector3 worldPos) =>
        _tilemap.SetTile(_tilemap.WorldToCell(worldPos), null);

    public TileBase GetTileAt(Vector3 worldPos) =>
        _tilemap.GetTile(_tilemap.WorldToCell(worldPos));

    public bool IsCellEmpty(Vector3 worldPos) => GetTileAt(worldPos) == null;

    public void FillRegion(Vector3Int start, Vector3Int size, TileBase tile)
    {
        BoundsInt bounds = new BoundsInt(start, size);
        TileBase[] tiles = new TileBase[size.x * size.y * size.z];
        for (int i = 0; i < tiles.Length; i++) tiles[i] = tile;
        _tilemap.SetTilesBlock(bounds, tiles);
    }
}
```

### Custom RuleTile

```csharp
[CreateAssetMenu(fileName = "NewTerrainRuleTile", menuName = "2D/Tiles/Terrain Rule Tile")]
public class TerrainRuleTile : RuleTile<TerrainRuleTile.Neighbor>
{
    public class Neighbor : RuleTile.TilingRule.Neighbor
    {
        public const int SameTileType = 3;
        public const int DifferentTileType = 4;
    }

    public override bool RuleMatch(int neighbor, TileBase tile)
    {
        return neighbor switch
        {
            Neighbor.SameTileType => tile is TerrainRuleTile,
            Neighbor.DifferentTileType => !(tile is TerrainRuleTile),
            _ => base.RuleMatch(neighbor, tile)
        };
    }
}
```

### ContactFilter2D Usage

```csharp
public class PhysicsQuery2D : MonoBehaviour
{
    [SerializeField] private LayerMask _enemyLayer;
    [SerializeField] private float _detectionRadius = 5f;

    private readonly List<Collider2D> _overlapResults = new(16);
    private readonly List<RaycastHit2D> _raycastResults = new(16);
    private readonly ContactFilter2D _enemyFilter = new();
    private readonly ContactFilter2D _groundFilter = new();

    private void Awake()
    {
        _enemyFilter.SetLayerMask(_enemyLayer);
        _enemyFilter.useLayerMask = true;
        _enemyFilter.useTriggers = false;

        _groundFilter.SetLayerMask(LayerMask.GetMask("Ground"));
        _groundFilter.useLayerMask = true;
        _groundFilter.useNormalAngle = true;
        _groundFilter.minNormalAngle = 45f;
        _groundFilter.maxNormalAngle = 135f;
    }

    public int FindNearbyEnemies(out List<Collider2D> results)
    {
        _overlapResults.Clear();
        int count = Physics2D.OverlapCircle(
            transform.position, _detectionRadius, _enemyFilter, _overlapResults);
        results = _overlapResults;
        return count;
    }

    public bool CheckGroundBelow(float maxDistance)
    {
        _raycastResults.Clear();
        return Physics2D.Raycast(
            transform.position, Vector2.down, _groundFilter, _raycastResults, maxDistance) > 0;
    }
}
```

### Sprite Animation Controller

```csharp
public class SpriteAnimationController : MonoBehaviour
{
    private Animator _animator;
    private SpriteRenderer _spriteRenderer;
    private static readonly int SpeedHash = Animator.StringToHash("Speed");
    private static readonly int IsGroundedHash = Animator.StringToHash("IsGrounded");
    private static readonly int VelocityYHash = Animator.StringToHash("VelocityY");
    private static readonly int AttackTrigger = Animator.StringToHash("Attack");
    private static readonly int HurtTrigger = Animator.StringToHash("Hurt");

    private void Awake()
    {
        _animator = GetComponent<Animator>();
        _spriteRenderer = GetComponent<SpriteRenderer>();
    }

    public void UpdateAnimation(float moveX, float velocityY, bool isGrounded)
    {
        _animator.SetFloat(SpeedHash, Mathf.Abs(moveX));
        _animator.SetFloat(VelocityYHash, velocityY);
        _animator.SetBool(IsGroundedHash, isGrounded);
        if (Mathf.Abs(moveX) > 0.01f) _spriteRenderer.flipX = moveX < 0;
    }

    public void PlayAttack() => _animator.SetTrigger(AttackTrigger);
    public void PlayHurt() => _animator.SetTrigger(HurtTrigger);
}
```

### Pixel Perfect Camera
```
Assets Pixels Per Unit: match sprite PPU (e.g., 16)
Reference Resolution: target viewport (e.g., 320x180)
Upscale Render Texture: ON
Pixel Snapping: ON
Crop Frame: X and Y
```

## Tilemap Architecture

```
Grid
  ├── Background    (Tilemap, Sorting Layer: Background, no collider)
  ├── Midground     (Tilemap, Sorting Layer: Midground, no collider)
  ├── Ground        (Tilemap + TilemapCollider2D + CompositeCollider2D)
  ├── OneWayPlatform(Tilemap + PlatformEffector2D)
  └── Foreground    (Tilemap, Sorting Layer: Foreground, no collider)
```

**Collider optimization**: Add TilemapCollider2D → set "Used by Composite"=true → add CompositeCollider2D → set Rigidbody2D to Static. Result: one merged collider instead of per-tile.
