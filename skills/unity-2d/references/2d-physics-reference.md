# 2D Physics Reference

## 2D Physics Reference

| Scenario | Rigidbody2D Type | Collider | Notes |
|:---------|:----------------|:---------|:------|
| Player character | Dynamic | CapsuleCollider2D | Freeze Z rotation |
| Moving platform | Kinematic | BoxCollider2D | Move via `MovePosition` |
| Static terrain | Static (via Composite) | CompositeCollider2D | Merge tile colliders |
| Trigger zone | Static or Kinematic | BoxCollider2D (Is Trigger) | Use `OnTriggerEnter2D` |
| One-way platform | Static | PlatformEffector2D | Enable "Use One Way" |
| Conveyor belt | Static | SurfaceEffector2D | Set speed and force |
| Bouncy surface | Static | BoxCollider2D + Physics Material 2D | Set bounciness on material |

### Physics 2D Project Settings

```
Edit > Project Settings > Physics 2D:
  Gravity:                (0, -9.81) for platformers, (0, 0) for top-down
  Default Contact Offset: 0.01
  Velocity Iterations:    8
  Position Iterations:    3
  Queries Hit Triggers:   OFF (unless you need trigger detection in raycasts)
```
