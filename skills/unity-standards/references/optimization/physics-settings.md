# Physics Optimization Settings

## Layer Collision Matrix

Disable collisions between layer pairs that never need to interact.

**Common optimization:**
```
             Player  Enemy  Bullet  Pickup  Environment  UI  Trigger
Player        -       X      -       X       X           -    X
Enemy         X       -      X       -       X           -    X
Bullet        -       X      -       -       X           -    -
Pickup        X       -      -       -       X           -    -
Environment   X       X      X       X       -           -    -
UI            -       -      -       -       -           -    -
Trigger       X       X      -       -       -           -    -
```

Each disabled pair saves a broadphase check per frame. With 10 layers, maximum 45 pairs — disable all but needed.

**Access:** Edit → Project Settings → Physics → Layer Collision Matrix

## Fixed Timestep

| Setting | Value | Effect |
|---------|-------|--------|
| Default | 0.02 (50 Hz) | Standard for most games |
| Lower | 0.033 (30 Hz) | Less CPU, less accurate physics |
| Higher | 0.01 (100 Hz) | More CPU, more accurate (racing, physics puzzles) |

**Rule:** Match physics rate to visual requirement. Don't run at 50Hz if your game targets 30fps — set to 0.033.

**Maximum Allowed Timestep:** Default 0.333s — prevents spiral-of-death. Reduce to 0.1s for mobile to cap physics catchup.

## Auto Sync Transforms

**Default:** ON (legacy behavior)
**Recommended:** OFF

When ON, `transform.position = X` immediately updates physics world — expensive. When OFF, physics world syncs once before `FixedUpdate`.

**Turn OFF unless:** You read `transform.position` immediately after setting it and expect physics-updated values in the same frame.

## Collision Shape Performance

| Shape | Cost | Use For |
|-------|------|---------|
| Sphere | Cheapest | Characters, projectiles, pickups |
| Capsule | Cheap | Characters, limbs |
| Box | Cheap | Crates, walls, triggers |
| Convex Mesh | Medium | Simple vehicles, props (< 255 verts) |
| Non-Convex Mesh | Expensive | Static environment only |

**Rules:**
- Non-convex mesh colliders: ONLY on static objects (Rigidbody requires convex)
- Compound colliders (multiple primitives) beat complex mesh colliders
- `isTrigger` is cheaper than collision response — use when physical response not needed

## Physics Query Optimization

```csharp
// ✅ Use NonAlloc variants
private readonly RaycastHit[] _hitBuffer = new RaycastHit[16];
void QueryTargets()
{
    int count = Physics.RaycastNonAlloc(ray, _hitBuffer, maxDist, layerMask);
    for (int i = 0; i < count; i++) ProcessHit(_hitBuffer[i]);
}

// ✅ Always specify layerMask
Physics.Raycast(origin, dir, out hit, distance, LayerMask.GetMask("Enemy"));

// ❌ Avoid: allocating variants
var hits = Physics.RaycastAll(ray); // allocates array each call
```

## 2D Physics

- Use Physics2D layer matrix (separate from 3D)
- `Rigidbody2D.bodyType = RigidbodyType2D.Static` for immovable platforms (not just removing Rigidbody2D)
- `Physics2D.OverlapCircleNonAlloc` over `OverlapCircleAll`
- Composite Collider 2D: merges tilemap colliders into single shape

## Physics Settings Checklist

- [ ] Layer Collision Matrix: disabled all non-interacting pairs
- [ ] Auto Sync Transforms: OFF
- [ ] Fixed Timestep: matches game requirements (not over-resolved)
- [ ] Maximum Allowed Timestep: 0.1s on mobile
- [ ] Queries Hit Triggers: OFF unless triggers need to be raycast targets
- [ ] Reuse Collision Callbacks: ON (reduces GC from collision events)
- [ ] Default Contact Offset: 0.01 (default) — reduce to 0.005 if precision needed
- [ ] All mesh colliders on kinematic/static bodies only
