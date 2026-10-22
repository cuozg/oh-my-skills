# Physics Optimization Settings

Collider/Rigidbody setup and collision-event debugging: `unity:physics-3d-collision`.

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

Each disabled pair removes candidate pairs before narrowphase and contact work. Disable every pair that never interacts.

**Access:** Edit -> Project Settings -> Physics -> Layer Collision Matrix

## Fixed Timestep

| Setting | Value | Effect |
|---------|-------|--------|
| Default | 0.02 (50 Hz) | Standard for most games |
| Lower | 0.033 (30 Hz) | Less CPU, less accurate physics |
| Higher | 0.01 (100 Hz) | More CPU, more accurate (racing, physics puzzles) |

**Rule:** Match physics rate to visual requirement. Don't run at 50Hz if your game targets 30fps - set to 0.033.

Enable Rigidbody **Interpolate** on player-visible bodies when the physics rate is below the render rate.

**Maximum Allowed Timestep:** Default 0.333s - prevents spiral-of-death. Reduce to 0.1s for mobile to cap physics catchup.

## Simulation Mode

`Physics.simulationMode` (Project Settings > Physics) replaces the obsolete
`Physics.autoSimulation`:

| Mode | Use |
|------|-----|
| `FixedUpdate` (default) | Standard games |
| `Update` | Simulate once per frame with frame delta |
| `Script` | Manual `Physics.Simulate(step)` - lockstep, replays, prediction, idle scenes |

`Physics2D.simulationMode` works the same way for 2D.

## Auto Sync Transforms

**Default:** OFF in new projects (upgraded projects may still have it ON)
**Recommended:** OFF

When ON, every physics query first flushes pending Transform changes into the physics world - expensive with many moved colliders. When OFF, changes sync automatically before the simulation step.

**If OFF and you raycast against a collider moved this frame:** call `Physics.SyncTransforms()` once before the queries instead of re-enabling the setting.

## Collision Shape Performance

| Shape | Cost | Use For |
|-------|------|---------|
| Sphere | Cheapest | Characters, projectiles, pickups |
| Capsule | Cheap | Characters, limbs |
| Box | Cheap | Crates, walls, triggers |
| Convex Mesh | Medium | Simple vehicles, props (hull capped at 255 triangles) |
| Non-Convex Mesh | Expensive | Static environment only |

**Rules:**
- Non-convex mesh colliders: ONLY on static or kinematic bodies (non-kinematic Rigidbody requires convex)
- Compound colliders (multiple primitives) beat complex mesh colliders
- `isTrigger` is cheaper than collision response - use when physical response not needed

## Physics Query Optimization

```csharp
// GOOD: use NonAlloc variants
private readonly RaycastHit[] _hitBuffer = new RaycastHit[16];
void QueryTargets()
{
    int count = Physics.RaycastNonAlloc(ray, _hitBuffer, maxDist, layerMask);
    for (int i = 0; i < count; i++) ProcessHit(_hitBuffer[i]);
}

// GOOD: always specify layerMask - serialize it instead of calling GetMask per query
[SerializeField] private LayerMask _enemyMask;
Physics.Raycast(origin, dir, out hit, distance, _enemyMask);

// BAD: allocating variants
var hits = Physics.RaycastAll(ray); // allocates array each call
```

For hundreds of queries per frame, batch them with `RaycastCommand` jobs (see `jobs-burst-migration.md`).

## 2D Physics

- Use Physics2D layer matrix (separate from 3D)
- `Rigidbody2D.bodyType = RigidbodyType2D.Static` for immovable platforms (not just removing Rigidbody2D)
- Reuse a results array/`List<Collider2D>` with the `Physics2D.OverlapCircle(point, radius, contactFilter, results)` overloads; the 2D `*NonAlloc` methods are obsolete and `*All` allocates
- Composite Collider 2D: merges tilemap colliders into single shape

## Physics Settings Checklist

- [ ] Layer Collision Matrix: disabled all non-interacting pairs
- [ ] Auto Sync Transforms: OFF
- [ ] Fixed Timestep: matches game requirements (not over-resolved)
- [ ] Maximum Allowed Timestep: 0.1s on mobile
- [ ] Queries Hit Triggers: OFF unless triggers need to be raycast targets
- [ ] Reuse Collision Callbacks: ON (reduces GC from collision events)
- [ ] Default Contact Offset: 0.01 (default) - reduce to 0.005 if precision needed
- [ ] Non-convex mesh colliders on kinematic/static bodies only
- [ ] Simulation Mode set intentionally (`Script` only when the project drives `Physics.Simulate`)
