# 2D Code Patterns & Project Setup

## Project Setup

### Sorting Layers (Back to Front)

```
Sorting Layers (Project Settings > Tags and Layers):
  - Background      (parallax sky, mountains)
  - Midground       (decorative trees, bushes)
  - Default         (player, enemies, items, ground tiles)
  - Foreground      (foreground foliage, rain, overlay effects)
  - UI              (HUD elements rendered in world space)

Rendering priority (evaluated in order):
  1. Sorting Layer   — highest priority (Background < Foreground)
  2. Order in Layer  — integer, higher = rendered on top
  3. Z position      — tiebreaker for same layer/order (closer to camera wins)
```

### Sprite Import Settings

| Art Style | Filter Mode | Compression | PPU | Max Size |
|:----------|:-----------|:------------|:----|:---------|
| Pixel art (16x16 tiles) | Point (no filter) | None | 16 | 256–512 |
| Pixel art (32x32 tiles) | Point (no filter) | None | 32 | 512–1024 |
| HD hand-drawn | Bilinear | ASTC 6x6 (mobile) / BC7 (desktop) | 100 | 2048–4096 |
| Vector-style | Bilinear | ASTC 4x4 / BC7 | 100 | 2048 |

### Sprite Sheet Import Checklist

| Setting | Pixel Art | HD Art |
|:--------|:---------|:-------|
| Sprite Mode | Multiple | Multiple |
| Pixels Per Unit | Match tile size (16, 32) | 100 |
| Filter Mode | Point (no filter) | Bilinear |
| Compression | None | Platform-specific |
| Pivot | Center or Bottom | Center |
| Mesh Type | Full Rect | Tight |
| Generate Physics Shape | Yes (for colliders) | Yes |

---

## Key Patterns

### 2D Character Controller (Platformer)

```csharp
/// <summary>
/// Physics-based 2D platformer controller using Rigidbody2D.
/// Features: coyote time, jump buffering, variable jump height, better-jump gravity.
/// </summary>
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
        _rb.freezeRotation = true; // Prevent tumbling
        _rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
    }

    private void Update()
    {
        // Input polling in Update for responsiveness
        _moveInput = Input.GetAxisRaw("Horizontal");

        if (Input.GetButtonDown("Jump"))
        {
            _lastJumpPressedTime = _jumpBufferTime;
        }

        // Tick timers
        _lastJumpPressedTime -= Time.deltaTime;
        _lastGroundedTime -= Time.deltaTime;
    }

    private void FixedUpdate()
    {
        // Ground detection via overlap circle
        _isGrounded = Physics2D.OverlapCircle(
            _groundCheck.position, _groundCheckRadius, _groundLayer);

        if (_isGrounded)
        {
            _lastGroundedTime = _coyoteTime;
        }

        ApplyMovement();
        ApplyJump();
        ApplyBetterJumpGravity();
    }

    private void ApplyMovement()
    {
        float targetSpeed = _moveInput * _moveSpeed;
        float speedDiff = targetSpeed - _rb.linearVelocity.x;
        float accelRate = Mathf.Abs(targetSpeed) > 0.01f ? _acceleration : _deceleration;
        float force = speedDiff * accelRate;

        _rb.AddForce(Vector2.right * force);
    }

    private void ApplyJump()
    {
        // Coyote time + jump buffer — forgiving input window
        if (_lastJumpPressedTime > 0 && _lastGroundedTime > 0)
        {
            _rb.linearVelocity = new Vector2(_rb.linearVelocity.x, _jumpForce);
            _lastJumpPressedTime = 0;
            _lastGroundedTime = 0;
        }
    }

    private void ApplyBetterJumpGravity()
    {
        // Faster falling for snappier game feel
        if (_rb.linearVelocity.y < 0)
        {
            _rb.linearVelocity += Vector2.up * (Physics2D.gravity.y * (_fallMultiplier - 1) * Time.fixedDeltaTime);
        }
        // Short hop when jump released early (variable jump height)
        else if (_rb.linearVelocity.y > 0 && !Input.GetButton("Jump"))
        {
            _rb.linearVelocity += Vector2.up * (Physics2D.gravity.y * (_lowJumpMultiplier - 1) * Time.fixedDeltaTime);
        }
    }

    /// <summary>Visual debug for ground check radius.</summary>
    private void OnDrawGizmosSelected()
    {
        if (_groundCheck == null) return;
        Gizmos.color = _isGrounded ? Color.green : Color.red;
        Gizmos.DrawWireSphere(_groundCheck.position, _groundCheckRadius);
    }
}
```

### Tilemap Scripting (SetTile / GetTile)

```csharp
using UnityEngine;
using UnityEngine.Tilemaps;

/// <summary>
/// Runtime tilemap manipulation — place, remove, and query tiles via code.
/// Useful for destructible terrain, procedural generation, and level editors.
/// </summary>
public class TilemapController : MonoBehaviour
{
    [SerializeField] private Tilemap _tilemap;
    [SerializeField] private TileBase _groundTile;
    [SerializeField] private TileBase _wallTile;

    /// <summary>
    /// Place a tile at a world position.
    /// </summary>
    public void PlaceTile(Vector3 worldPosition, TileBase tile)
    {
        Vector3Int cellPos = _tilemap.WorldToCell(worldPosition);
        _tilemap.SetTile(cellPos, tile);
    }

    /// <summary>
    /// Remove a tile at a world position.
    /// </summary>
    public void RemoveTile(Vector3 worldPosition)
    {
        Vector3Int cellPos = _tilemap.WorldToCell(worldPosition);
        _tilemap.SetTile(cellPos, null);
    }

    /// <summary>
    /// Query what tile exists at a world position.
    /// </summary>
    public TileBase GetTileAt(Vector3 worldPosition)
    {
        Vector3Int cellPos = _tilemap.WorldToCell(worldPosition);
        return _tilemap.GetTile(cellPos);
    }

    /// <summary>
    /// Check if a cell is empty (no tile placed).
    /// </summary>
    public bool IsCellEmpty(Vector3 worldPosition)
    {
        return GetTileAt(worldPosition) == null;
    }

    /// <summary>
    /// Fill a rectangular region with a tile.
    /// Uses BoundsInt for efficient batch operations.
    /// </summary>
    public void FillRegion(Vector3Int start, Vector3Int size, TileBase tile)
    {
        BoundsInt bounds = new BoundsInt(start, size);
        TileBase[] tiles = new TileBase[size.x * size.y * size.z];

        for (int i = 0; i < tiles.Length; i++)
        {
            tiles[i] = tile;
        }

        _tilemap.SetTilesBlock(bounds, tiles);
    }

    /// <summary>
    /// Procedurally generate a simple platform level.
    /// </summary>
    public void GenerateSimpleLevel(int width, int height)
    {
        // Ground floor
        for (int x = 0; x < width; x++)
        {
            _tilemap.SetTile(new Vector3Int(x, 0, 0), _groundTile);
        }

        // Walls on edges
        for (int y = 0; y < height; y++)
        {
            _tilemap.SetTile(new Vector3Int(0, y, 0), _wallTile);
            _tilemap.SetTile(new Vector3Int(width - 1, y, 0), _wallTile);
        }

        // Random platforms
        for (int i = 0; i < width / 4; i++)
        {
            int x = Random.Range(2, width - 3);
            int y = Random.Range(2, height - 1);
            int platformWidth = Random.Range(2, 5);

            for (int px = 0; px < platformWidth; px++)
            {
                _tilemap.SetTile(new Vector3Int(x + px, y, 0), _groundTile);
            }
        }
    }
}
```

### Custom RuleTile

```csharp
using UnityEngine;
using UnityEngine.Tilemaps;

/// <summary>
/// Custom RuleTile that auto-selects sprite based on neighboring tiles.
/// Create via Assets > Create > 2D > Tiles > Rule Tile.
/// For code-driven rule tiles, extend RuleTile.
/// </summary>
[CreateAssetMenu(fileName = "NewTerrainRuleTile", menuName = "2D/Tiles/Terrain Rule Tile")]
public class TerrainRuleTile : RuleTile<TerrainRuleTile.Neighbor>
{
    /// <summary>
    /// Custom neighbor rules beyond the built-in This/NotThis.
    /// </summary>
    public class Neighbor : RuleTile.TilingRule.Neighbor
    {
        // Built-in: This = 1, NotThis = 2
        public const int SameTileType = 3;
        public const int DifferentTileType = 4;
    }

    /// <summary>
    /// Override neighbor matching to support custom rules.
    /// </summary>
    public override bool RuleMatch(int neighbor, TileBase tile)
    {
        switch (neighbor)
        {
            case Neighbor.SameTileType:
                return tile is TerrainRuleTile;
            case Neighbor.DifferentTileType:
                return !(tile is TerrainRuleTile);
            default:
                return base.RuleMatch(neighbor, tile);
        }
    }
}

/// <summary>
/// Animated tile that cycles through sprites at a given speed.
/// Create instances via Assets > Create > 2D > Tiles > Animated Tile.
/// </summary>
[CreateAssetMenu(fileName = "NewAnimatedTile", menuName = "2D/Tiles/Animated Tile")]
public class SimpleAnimatedTile : TileBase
{
    [SerializeField] private Sprite[] _frames;
    [SerializeField] private float _animationSpeed = 2f;

    public override void GetTileData(Vector3Int position, ITilemap tilemap, ref TileData tileData)
    {
        if (_frames == null || _frames.Length == 0) return;
        tileData.sprite = _frames[0];
    }

    public override bool GetTileAnimationData(
        Vector3Int position, ITilemap tilemap, ref TileAnimationData tileAnimationData)
    {
        if (_frames == null || _frames.Length <= 1) return false;

        tileAnimationData.animatedSprites = _frames;
        tileAnimationData.animationSpeed = _animationSpeed;
        tileAnimationData.animationStartTime = 0f;
        return true;
    }
}
```

### ContactFilter2D Usage

```csharp
using UnityEngine;
using System.Collections.Generic;

/// <summary>
/// Advanced 2D physics queries using ContactFilter2D.
/// ContactFilter2D allows filtering by layer, trigger, normal angle —
/// more efficient and flexible than multiple OverlapCircle calls.
/// </summary>
public class PhysicsQuery2D : MonoBehaviour
{
    [SerializeField] private LayerMask _enemyLayer;
    [SerializeField] private float _detectionRadius = 5f;

    // Reusable buffers to avoid GC allocation
    private readonly List<Collider2D> _overlapResults = new(16);
    private readonly List<RaycastHit2D> _raycastResults = new(16);
    private readonly ContactFilter2D _enemyFilter = new();
    private readonly ContactFilter2D _groundFilter = new();

    private void Awake()
    {
        // Configure enemy detection filter
        _enemyFilter.SetLayerMask(_enemyLayer);
        _enemyFilter.useLayerMask = true;
        _enemyFilter.useTriggers = false; // Ignore trigger colliders

        // Configure ground detection filter — only surfaces facing up
        _groundFilter.SetLayerMask(LayerMask.GetMask("Ground"));
        _groundFilter.useLayerMask = true;
        _groundFilter.useNormalAngle = true;
        _groundFilter.minNormalAngle = 45f;   // Minimum angle from horizontal
        _groundFilter.maxNormalAngle = 135f;  // Maximum angle from horizontal
    }

    /// <summary>
    /// Find all enemies within detection radius. Zero-allocation with reusable list.
    /// </summary>
    public int FindNearbyEnemies(out List<Collider2D> results)
    {
        _overlapResults.Clear();
        int count = Physics2D.OverlapCircle(
            transform.position,
            _detectionRadius,
            _enemyFilter,
            _overlapResults);

        results = _overlapResults;
        return count;
    }

    /// <summary>
    /// Raycast downward with ground filter — only hits surfaces facing up.
    /// </summary>
    public bool CheckGroundBelow(float maxDistance)
    {
        _raycastResults.Clear();
        int count = Physics2D.Raycast(
            transform.position,
            Vector2.down,
            _groundFilter,
            _raycastResults,
            maxDistance);

        return count > 0;
    }

    /// <summary>
    /// Cast the attached collider in a direction (for movement prediction).
    /// </summary>
    public bool WillCollide(Vector2 direction, float distance)
    {
        var collider = GetComponent<Collider2D>();
        if (collider == null) return false;

        _raycastResults.Clear();
        int count = collider.Cast(direction, _groundFilter, _raycastResults, distance);
        return count > 0;
    }

    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, _detectionRadius);
    }
}
```

### Sprite Animation State Machine

```csharp
/// <summary>
/// Sprite animation controller driving Animator parameters.
/// Caches parameter hashes for zero-allocation updates.
/// Handles sprite flipping based on movement direction.
/// </summary>
public class SpriteAnimationController : MonoBehaviour
{
    private Animator _animator;
    private SpriteRenderer _spriteRenderer;

    // Cached parameter hashes — avoid string allocation on every SetFloat/SetBool
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

    /// <summary>
    /// Update animation state from character controller data.
    /// Call every frame after input processing.
    /// </summary>
    public void UpdateAnimation(float moveX, float velocityY, bool isGrounded)
    {
        _animator.SetFloat(SpeedHash, Mathf.Abs(moveX));
        _animator.SetFloat(VelocityYHash, velocityY);
        _animator.SetBool(IsGroundedHash, isGrounded);

        // Flip sprite based on movement direction (preserves scale)
        if (Mathf.Abs(moveX) > 0.01f)
        {
            _spriteRenderer.flipX = moveX < 0;
        }
    }

    /// <summary>Trigger attack animation.</summary>
    public void PlayAttack() => _animator.SetTrigger(AttackTrigger);

    /// <summary>Trigger hurt animation.</summary>
    public void PlayHurt() => _animator.SetTrigger(HurtTrigger);
}
```

### 2D Lighting Setup (URP)

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;

/// <summary>
/// Dynamic 2D light controller — flicker effect for torches, campfires, etc.
/// Requires URP 2D Renderer and Light2D component.
/// </summary>
[RequireComponent(typeof(Light2D))]
public class FlickerLight2D : MonoBehaviour
{
    [SerializeField] private float _baseIntensity = 1f;
    [SerializeField] private float _flickerAmount = 0.2f;
    [SerializeField] private float _flickerSpeed = 8f;

    [SerializeField] private float _baseOuterRadius = 5f;
    [SerializeField] private float _radiusFlicker = 0.3f;

    private Light2D _light;
    private float _noiseOffset;

    private void Awake()
    {
        _light = GetComponent<Light2D>();
        _noiseOffset = Random.Range(0f, 100f); // Unique per instance
    }

    private void Update()
    {
        float noise = Mathf.PerlinNoise(Time.time * _flickerSpeed + _noiseOffset, 0f);

        // Intensity flicker
        _light.intensity = _baseIntensity + (noise - 0.5f) * 2f * _flickerAmount;

        // Radius flicker (subtle)
        _light.pointLightOuterRadius = _baseOuterRadius + (noise - 0.5f) * 2f * _radiusFlicker;
    }
}
```

### Pixel Perfect Camera Setup

```
Pixel Perfect Camera (com.unity.2d.pixel-perfect):

  Configuration:
    Assets Pixels Per Unit: match sprite PPU (e.g., 16 for 16x16 tiles)
    Reference Resolution:  target viewport in pixels (e.g., 320x180 for 16:9)
    Upscale Render Texture: ON — renders at reference res, upscales to screen
    Pixel Snapping:         ON — snaps sprites to pixel grid, prevents sub-pixel jitter
    Crop Frame:             X and Y — handles non-integer scaling ratios

  When to use:
    - Pixel art games where crisp edges are critical
    - Retro-style games with fixed-resolution feel
    - Any 2D game where bilinear filtering causes blur
```

---

## Tilemap Architecture

### Recommended Hierarchy

```
Grid
  ├── Background    (Tilemap, Sorting Layer: Background, no collider)
  ├── Midground     (Tilemap, Sorting Layer: Midground, no collider)
  ├── Ground        (Tilemap + TilemapCollider2D + CompositeCollider2D)
  ├── OneWayPlatform(Tilemap + PlatformEffector2D)
  └── Foreground    (Tilemap, Sorting Layer: Foreground, no collider)
```

### Collider Optimization

```
Tilemap Collider Optimization:
  1. Add TilemapCollider2D to the Ground tilemap
  2. Set "Used by Composite" = true on TilemapCollider2D
  3. Add CompositeCollider2D to the same GameObject
  4. Set Rigidbody2D (auto-added) body type to Static
  Result: One merged collider instead of per-tile colliders (massive perf gain)
```
