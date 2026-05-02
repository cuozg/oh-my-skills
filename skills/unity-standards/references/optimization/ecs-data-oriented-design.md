# Unity ECS (Entity Component System)

Data-oriented design framework for high-performance Unity games.

## Core Concepts

### Entities
- Lightweight IDs, not GameObjects
- No methods, no data — just a collection of components
- Created via `EntityManager.CreateEntity()`
- Can be created from archetypes for batch creation

### Components
- **IComponentData**: Unmanaged components stored in chunks (Burst-compatible)
- **IBufferElementData**: Dynamic buffers attached to entities
- **ISharedComponentData**: Shared data across entities (stored once, referenced many)
- **Managed components**: Rarely used, not Burst-compatible

### Systems
- Logic that processes entities with specific components
- Runs on main thread or via Job System
- System groups control update order

## Basic ECS Structure

```csharp
using Unity.Entities;
using Unity.Mathematics;
using Unity.Transforms;

// Component - pure data
public struct Velocity : IComponentData
{
    public float3 Value;
}

// System - logic
public partial struct VelocitySystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        // Query entities with LocalTransform and Velocity
        foreach (var (transform, velocity) in 
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>>())
        {
            transform.ValueRW.Position += velocity.ValueRO.Value * deltaTime;
        }
    }
}
```

## System Types

| System Type | Use Case | Threading |
|-------------|----------|-----------|
| `ISystem` | Modern ECS, Burst-compatible | Main thread or jobified |
| `SystemBase` | Legacy ECS, more features | Main thread or jobified |
| `EntityCommandBufferSystem` | Deferred entity operations | Always at end of group |

## Entity Queries

```csharp
// Simple query - all entities with Position
EntityQuery query = SystemAPI.QueryBuilder()
    .WithAll<Position>()
    .Build();

// Complex query
EntityQuery query = SystemAPI.QueryBuilder()
    .WithAll<LocalTransform, Velocity>()      // Must have these
    .WithAny<EnemyTag, BossTag>()              // Must have at least one
    .WithNone<DeadTag>()                       // Must NOT have these
    .Build();

// Using in system update
foreach (var (transform, velocity) in 
    SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>>())
{
    // Process entities
}
```

## Jobified Systems

```csharp
[BurstCompile]
public partial struct MoveJob : IJobEntity
{
    public float DeltaTime;
    
    // IJobEntity automatically queries matching entities
    void Execute(ref LocalTransform transform, in Velocity velocity)
    {
        transform.Position += velocity.Value * DeltaTime;
    }
}

public partial struct VelocitySystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        new MoveJob { DeltaTime = SystemAPI.Time.DeltaTime }
            .ScheduleParallel();
    }
}
```

## Entity Command Buffers (ECB)

Use ECB for structural changes (creating/destroying entities, adding/removing components) inside jobs:

```csharp
public partial struct SpawnSystem : ISystem
{
    [BurstCompile]
    public void OnCreate(ref SystemState state)
    {
        // Require ECB system
        state.RequireForUpdate<BeginSimulationEntityCommandBufferSystem.Singleton>();
    }
    
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        var ecb = SystemAPI.GetSingleton<BeginSimulationEntityCommandBufferSystem.Singleton>()
            .CreateCommandBuffer(state.WorldUnmanaged);
        
        foreach (var (spawner, entity) in 
            SystemAPI.Query<RefRO<Spawner>>().WithEntityAccess())
        {
            if (spawner.ValueRO.SpawnTimer <= 0)
            {
                Entity newEntity = ecb.Instantiate(spawner.ValueRO.Prefab);
                ecb.SetComponent(newEntity, LocalTransform.FromPosition(spawner.ValueRO.SpawnPosition));
            }
        }
    }
}
```

## Archetypes & Chunks

```csharp
// Create archetype for efficient batch entity creation
EntityArchetype archetype = state.EntityManager.CreateArchetype(
    typeof(LocalTransform),
    typeof(Velocity),
    typeof(Health)
);

// Create 100 entities with this archetype
NativeArray<Entity> entities = state.EntityManager.CreateEntity(archetype, 100, Allocator.Temp);
```

## Best Practices

### Data Layout
- **Struct of Arrays (SoA)**: Better cache locality
- Keep component sizes small (< 128 bytes)
- Group frequently accessed components together
- Use `ChunkBaseIndex` for chunk-level operations

### System Organization
```
Systems/
├── InitializationSystemGroup/     (Scene loading, setup)
├── SimulationSystemGroup/         (Gameplay logic)
│   ├── FixedStepSimulationSystemGroup/  (Physics)
│   └── VariableRateSimulationSystemGroup/
├── PresentationSystemGroup/       (Rendering, VFX)
└── CleanupSystemGroup/             (Destruction)
```

### Update Order Attributes
```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateBefore(typeof(TransformSystemGroup))]
[UpdateAfter(typeof(FixedStepSimulationSystemGroup))]
public partial struct MySystem : ISystem { }
```

### Component Best Practices

```csharp
// ✅ Small, focused components
public struct Health : IComponentData
{
    public float Current;
    public float Max;
}

// ❌ Avoid large combined components
public struct CharacterStats : IComponentData  // Too big!
{
    public float Health;
    public float MaxHealth;
    public float Mana;
    public float MaxMana;
    public float Stamina;
    // ... 20 more fields
}

// ✅ Use separate components for different concerns
public struct Health : IComponentData { public float Value; }
public struct Mana : IComponentData { public float Value; }
public struct Stamina : IComponentData { public float Value; }
```

### Memory Management

| Allocator | Use Case | Lifetime |
|-----------|----------|----------|
| `Temp` | Immediate calculations | 1 frame |
| `TempJob` | Job data | 4 frames |
| `Persistent` | Long-lived data | Manual disposal |

```csharp
// Frame-scoped data
NativeArray<float3> positions = new NativeArray<float3>(100, Allocator.Temp);

// Job data
NativeArray<float3> velocities = new NativeArray<float3>(100, Allocator.TempJob);

// Long-lived data
NativeArray<Entity> persistentEntities = new NativeArray<Entity>(100, Allocator.Persistent);
// Must call persistentEntities.Dispose() when done
```

## Common Patterns

### Tag Components
```csharp
// Zero-size component for tagging entities
public struct PlayerTag : IComponentData { }
public struct EnemyTag : IComponentData { }
public struct DestroyNextFrame : IComponentData { }

// Query for player only
foreach (var transform in SystemAPI.Query<RefRO<LocalTransform>>()
    .WithAll<PlayerTag>())
{
    // Process player
}
```

### Singleton Pattern
```csharp
// Component to hold global game state
public struct GameState : IComponentData
{
    public float GameTime;
    public int Score;
    public bool IsPaused;
}

// Access in system
GameState gameState = SystemAPI.GetSingleton<GameState>();
```

### Prefab Instantiation
```csharp
public struct Spawner : IComponentData
{
    public Entity Prefab;  // Entity reference to prefab
    public float3 SpawnPosition;
    public float SpawnInterval;
}

// Spawn from prefab
Entity newEntity = ecb.Instantiate(spawner.Prefab);
```

## Hybrid ECS (GameObject + ECS)

```csharp
// Convert GameObject to entity at runtime
public class ConvertToEntity : MonoBehaviour
{
    void Start()
    {
        var world = World.DefaultGameObjectInjectionWorld;
        var entityManager = world.EntityManager;
        
        // Create entity from GameObject
        Entity entity = GameObjectConversionUtility.ConvertGameObjectHierarchy(
            gameObject, 
            world
        );
    }
}

// Or use Baking for subscenes
public class MyAuthoring : MonoBehaviour
{
    public float Speed = 10f;
}

public class MyBaker : Baker<MyAuthoring>
{
    public override void Bake(MyAuthoring authoring)
    {
        AddComponent(new Velocity { Value = new float3(authoring.Speed, 0, 0) });
    }
}
```

## Performance Guidelines

### DO
- Use `IJobEntity` for parallel processing
- Cache queries in `OnCreate`
- Use `[BurstCompile]` on job structs and methods
- Keep components small and cache-friendly
- Use `RefRO<T>` for read-only, `RefRW<T>` for read-write
- Schedule jobs early, complete results late
- Use ECB for structural changes

### DON'T
- Query inside loops
- Access managed objects (GameObject, Transform) in jobs
- Create/destroy entities in tight loops
- Use `EntityManager` directly inside jobs
- Forget to dispose `NativeArray` and `NativeList`
- Use `TempJob` allocator without completing within 4 frames

## Debugging

```csharp
// Entity debugger
EntityManager entityManager = World.DefaultGameObjectInjectionWorld.EntityManager;
EntityQuery query = SystemAPI.QueryBuilder().WithAll<Velocity>().Build();

// In Inspector: Window > Entities > Entity Debugger
// Shows all entities, their components, and chunk layout

// System performance
// Window > Entities > System Performance
// Shows per-system execution time
```

## Migration Checklist (MonoBehaviour → ECS)

1. **Identify hot paths**: Profile to find CPU bottlenecks
2. **Extract data**: Convert MonoBehaviour fields to IComponentData
3. **Create systems**: Move Update() logic to ISystem
4. **Jobify**: Add BurstCompile, convert to IJobEntity
5. **Optimize queries**: Use WithAll/WithAny/WithNone efficiently
6. **Handle lifecycle**: Use ECB for spawn/destroy
7. **Profile again**: Verify performance gains

## Resources

- Unity ECS Samples: https://github.com/Unity-Technologies/EntityComponentSystemSamples
- DOTS Documentation: https://docs.unity3d.com/Packages/com.unity.entities@latest
- Performance by default: https://docs.unity3d.com/Manual/DOTS.html
