# Beads Workflow Examples

This document provides complete, end-to-end workflow walkthroughs for the beads skill in Unity projects. Each example demonstrates a different complexity level and pattern.

---

## Example 1: Simple Feature - Health Regeneration System

**Scenario**: Add passive health regeneration to the Hero class (LOW risk, linear workflow)

### 1.1 Discovery & Risk Assessment

**Discovery Report**:
```
Feature: Passive Health Regeneration
Files to modify: 
  - Assets/_Project/Scripts/Hero/HeroStats.cs (add regen logic)
  - Assets/_Project/ScriptableObjects/HeroDataSO.cs (add regenPerSecond field)

Dependencies: None (uses existing Update loop)
Risk: LOW (familiar pattern, 2 files, isolated change)
```

**Risk Decision**: Proceed directly (no spike needed)

### 1.2 Bead Creation

```bash
# Create epic bead
bd add "Add passive health regeneration to heroes" \
  --priority 2 \
  --epic

# Output: Created bead bd-10

# Add task bead
bd add "Implement health regen in HeroStats + add SO field" \
  --parent bd-10 \
  --priority 2
  
# Output: Created bead bd-11
```

**Bead Tree**:
```
bd-10 (epic): Add passive health regeneration to heroes
  └── bd-11: Implement health regen in HeroStats + add SO field
```

### 1.3 Worker Execution (bd-11)

**Worker Prompt** (spawned for bd-11):
```
You are Worker1, assigned to bd-11.

BEAD: Implement health regen in HeroStats + add SO field
EPIC: bd-10 (Add passive health regeneration to heroes)
THREAD: track:Worker1:bd-10

TASK:
1. Add `regenPerSecond` float field to HeroDataSO
2. Add regen logic to HeroStats.Update():
   - if (currentHealth < maxHealth)
       currentHealth += dataSO.regenPerSecond * Time.deltaTime
3. Clamp currentHealth to maxHealth

FILES:
- Assets/_Project/Scripts/Hero/HeroStats.cs
- Assets/_Project/ScriptableObjects/HeroDataSO.cs

Reserve files, implement, test in Play Mode, commit, close bead.
```

**Worker Actions**:

```bash
# 1. Reserve files
file_reservation_paths(
  project_key="/path/to/project",
  agent_name="Worker1",
  paths=["Assets/_Project/Scripts/Hero/HeroStats.cs", 
         "Assets/_Project/ScriptableObjects/HeroDataSO.cs"],
  exclusive=true,
  ttl_seconds=7200
)

# 2. Implement changes
# (code implementation happens here)

# 3. Self-message context preservation
send_message(
  project_key="/path/to/project",
  sender_name="Worker1",
  to=["Worker1"],
  thread_id="track:Worker1:bd-10",
  subject="[bd-11] Context for Next Bead",
  body_md="Completed health regen implementation. Files modified: HeroStats.cs, HeroDataSO.cs. Next: Testing phase."
)

# 4. Test in Play Mode (manual verification)

# 5. Commit
git add Assets/_Project/Scripts/Hero/HeroStats.cs Assets/_Project/ScriptableObjects/HeroDataSO.cs
git commit -m "feat(hero): add passive health regeneration

- Add regenPerSecond field to HeroDataSO
- Implement regen logic in HeroStats.Update()
- Clamp health to max value

Closes bd-11
Part of bd-10"

# 6. Release files
release_file_reservations(
  project_key="/path/to/project",
  agent_name="Worker1"
)

# 7. Close bead
bd close bd-11
```

**Completion Message**:
```bash
send_message(
  project_key="/path/to/project",
  sender_name="Worker1",
  to=["Orchestrator"],
  thread_id="bd-10",
  subject="[bd-11] COMPLETE",
  body_md="✅ Health regeneration implemented and tested.

**Changes**:
- HeroDataSO: Added `regenPerSecond` float field
- HeroStats: Added regen logic in Update() with clamping

**Testing**: Verified in Play Mode - hero health regenerates correctly.
**Commit**: feat(hero): add passive health regeneration"
)
```

### 1.4 Epic Closure

```bash
# Orchestrator closes epic
bd close bd-10

# Completion message
send_message(
  to=["ProjectLead"],
  thread_id="bd-10",
  subject="[Track 1] COMPLETE",
  body_md="✅ Health regeneration feature complete. All beads closed, tests passing."
)
```

**Quick Reference**:
- **Pattern**: Simple linear workflow (1 epic → 1 task)
- **Risk**: LOW (2 files, familiar pattern)
- **Duration**: ~30 minutes
- **Commits**: 1 (feature commit)

---

## Example 2: Complex Feature - Enemy Object Pooling

**Scenario**: Implement object pooling for enemies with NavMeshAgent support (HIGH risk, requires spikes)

### 2.1 Discovery & Risk Assessment

**Discovery Report**:
```
Feature: Enemy Object Pooling System
Files to create/modify:
  - Assets/_Project/Scripts/Utils/ObjectPool.cs (new generic pool)
  - Assets/_Project/Scripts/Combat/EnemySpawner.cs (modify to use pool)
  - Assets/_Project/Scripts/AI/EnemyAI.cs (add Reset() method)
  - Assets/_Project/Scripts/Combat/EnemyHealth.cs (modify OnDeath to return to pool)
  - Prefabs: Enemy prefabs need PooledObject component

Dependencies: 
  - NavMeshAgent behavior on pooled objects (UNKNOWN - needs validation)
  - Unity's object pooling API (new dependency)

Risk: HIGH
  - Novel pattern (pooling with NavMesh)
  - 6+ files
  - New dependency (Unity.Pool)
  - Performance-critical system
```

**Risk Decision**: Spike required for NavMeshAgent pooling validation

### 2.2 Spike Bead Creation

```bash
# Create spike bead
bd add "SPIKE: Validate NavMeshAgent pooling behavior" \
  --priority 0 \
  --parent bd-12

# Output: Created bead bd-13
```

### 2.3 Spike Execution (bd-13)

**Spike Prompt**:
```
SPIKE BEAD: bd-13
TIME-BOX: 30 minutes
GOAL: Validate NavMeshAgent behavior when pooling enemies

QUESTIONS:
1. Can NavMeshAgent be disabled/re-enabled without issues?
2. Does NavMesh.SamplePosition work on pooled agents?
3. What's the correct reset sequence?

OUTPUT: .spikes/enemy-pooling/bd-13/FINDINGS.md
```

**Spike Findings** (`.spikes/enemy-pooling/bd-13/FINDINGS.md`):
```markdown
# Spike bd-13: NavMeshAgent Pooling Validation

**Time-box**: 30 minutes
**Status**: PROCEED

## Findings

✅ **NavMeshAgent CAN be pooled safely** with correct reset sequence:

```csharp
void ResetPooledEnemy(GameObject enemy) {
    var agent = enemy.GetComponent<NavMeshAgent>();
    
    // Critical: disable BEFORE moving
    agent.enabled = false;
    enemy.transform.position = spawnPoint;
    enemy.transform.rotation = Quaternion.identity;
    
    // Re-enable and warp to position
    agent.enabled = true;
    agent.Warp(spawnPoint);
    agent.ResetPath();
}
```

## Performance
- No NavMesh.SamplePosition needed (Warp handles it)
- No memory leaks observed in 100-object pool stress test
- ~0.2ms per reset (acceptable)

## Recommendation
**PROCEED** with pooling implementation. Use above reset sequence in EnemyAI.Reset().

## References
- Unity Docs: https://docs.unity3d.com/ScriptReference/AI.NavMeshAgent.Warp.html
- Test scene: `.spikes/enemy-pooling/bd-13/PoolingTest.unity`
```

**Spike Closure**:
```bash
bd close bd-13

send_message(
  to=["Orchestrator"],
  thread_id="bd-12",
  subject="[Spike bd-13] FINDINGS: PROCEED",
  body_md="✅ NavMeshAgent pooling validated. Safe to proceed with implementation.

**Key finding**: Must disable agent BEFORE repositioning, then Warp() after re-enabling.

See full findings: `.spikes/enemy-pooling/bd-13/FINDINGS.md`"
)
```

### 2.4 Feature Decomposition (Post-Spike)

```bash
# Epic already created
# bd-12 (epic): Implement enemy object pooling

# Now add task beads based on spike findings
bd add "Create generic ObjectPool<T> utility class" \
  --parent bd-12 \
  --priority 1

# Output: bd-14

bd add "Add Reset() methods to Enemy components (AI, Health, etc.)" \
  --parent bd-12 \
  --priority 1

# Output: bd-15

bd add "Modify EnemySpawner to use ObjectPool" \
  --parent bd-12 \
  --priority 1

# Output: bd-16

bd add "Update enemy prefabs with PooledObject component" \
  --parent bd-12 \
  --priority 2

# Output: bd-17
```

**Bead Tree**:
```
bd-12 (epic): Implement enemy object pooling
  ├── bd-13 (spike): Validate NavMeshAgent pooling behavior [CLOSED]
  ├── bd-14: Create generic ObjectPool<T> utility class
  ├── bd-15: Add Reset() methods to Enemy components
  ├── bd-16: Modify EnemySpawner to use ObjectPool
  └── bd-17: Update enemy prefabs with PooledObject component
```

### 2.5 Track Planning

```bash
# Generate parallel tracks
bv --robot-plan --bead bd-12

# Output suggests 2 parallel tracks:
# Track 1 (Worker1): bd-14 → bd-16 (pool impl + spawner)
# Track 2 (Worker2): bd-15 → bd-17 (components + prefabs)
```

**Track Threads Created**:
- `track:Worker1:bd-12` (Worker1's context thread)
- `track:Worker2:bd-12` (Worker2's context thread)

### 2.6 Parallel Execution

**Worker1 (bd-14 → bd-16)**:

```bash
# bd-14: Create ObjectPool<T>
file_reservation_paths(paths=["Assets/_Project/Scripts/Utils/ObjectPool.cs"], ...)
# Implement generic pool class...
git commit -m "feat(utils): add generic ObjectPool<T>"
bd close bd-14

# bd-16: Modify EnemySpawner
file_reservation_paths(paths=["Assets/_Project/Scripts/Combat/EnemySpawner.cs"], ...)
# Integrate pool into spawner...
git commit -m "feat(combat): integrate ObjectPool into EnemySpawner"
bd close bd-16

# Track complete
send_message(
  to=["Orchestrator"],
  thread_id="bd-12",
  subject="[Track 1] COMPLETE",
  body_md="✅ Pool implementation and spawner integration complete."
)
```

**Worker2 (bd-15 → bd-17)**:

```bash
# bd-15: Add Reset() methods
file_reservation_paths(paths=[
  "Assets/_Project/Scripts/AI/EnemyAI.cs",
  "Assets/_Project/Scripts/Combat/EnemyHealth.cs"
], ...)
# Add Reset() methods using spike findings...
git commit -m "feat(ai): add Reset() methods for pooling"
bd close bd-15

# bd-17: Update prefabs
file_reservation_paths(paths=["Assets/_Project/Prefabs/Enemy/*.prefab"], ...)
# Add PooledObject components...
git commit -m "feat(prefabs): add PooledObject to enemy prefabs"
bd close bd-17

# Track complete
send_message(
  to=["Orchestrator"],
  thread_id="bd-12",
  subject="[Track 2] COMPLETE",
  body_md="✅ Component reset methods and prefab updates complete."
)
```

### 2.7 Epic Closure

**Integration Checklist** (Orchestrator validates):
```markdown
- [x] All beads closed (bd-13, bd-14, bd-15, bd-16, bd-17)
- [x] Spike findings documented (.spikes/enemy-pooling/bd-13/FINDINGS.md)
- [x] All commits follow conventions
- [x] No compilation errors
- [x] Play Mode test: 50 enemies spawn/despawn correctly
- [x] Performance: <1ms per spawn/return to pool
- [x] NavMeshAgent navigation works after pooling
```

```bash
bd close bd-12

send_message(
  to=["ProjectLead"],
  thread_id="bd-12",
  subject="[Epic bd-12] COMPLETE",
  body_md="✅ Enemy object pooling fully implemented and tested.

**Deliverables**:
- Generic ObjectPool<T> utility
- NavMeshAgent pooling with validated reset sequence
- 2 parallel tracks completed successfully
- Spike findings documented

**Performance**: <1ms per spawn/despawn, 50-enemy stress test passed."
)
```

**Quick Reference**:
- **Pattern**: Spike → parallel tracks with file conflicts managed
- **Risk**: HIGH → spike validated → MEDIUM (post-spike)
- **Duration**: ~4 hours (30min spike + 3.5h implementation)
- **Tracks**: 2 parallel (Worker1 + Worker2)
- **Commits**: 5 (spike prototype + 4 feature commits)

---

## Example 3: Spike Workflow - Addressables Async Loading

**Scenario**: Validate Addressables for async scene loading before implementing dungeon streaming

### 3.1 Spike Bead Creation

```bash
bd add "SPIKE: Validate Addressables async loading for dungeon scenes" \
  --priority 0

# Output: bd-18
```

### 3.2 Spike Execution

**Spike Prompt**:
```
SPIKE BEAD: bd-18
TIME-BOX: 30 minutes
GOAL: Validate Addressables for async scene loading with loading screen

QUESTIONS:
1. Can Addressables load 3D scenes async without blocking main thread?
2. Is progress reporting accurate for loading screens?
3. What's memory overhead vs. Resources.LoadAsync?
4. Compatible with Unity 6 (6000.3.8f1)?

OUTPUT: .spikes/addressables-loading/bd-18/FINDINGS.md
```

**Spike Findings** (`.spikes/addressables-loading/bd-18/FINDINGS.md`):
```markdown
# Spike bd-18: Addressables Async Scene Loading

**Time-box**: 30 minutes
**Status**: PROCEED (with caveat)

## Findings

✅ **Addressables async loading works** with accurate progress:

```csharp
async Task LoadDungeonSceneAsync(string sceneKey) {
    var handle = Addressables.LoadSceneAsync(sceneKey, LoadSceneMode.Additive);
    
    while (!handle.IsDone) {
        float progress = handle.PercentComplete; // Accurate 0-1
        UpdateLoadingBar(progress);
        await Task.Yield();
    }
    
    var scene = handle.Result;
    // Scene loaded, can activate/unload
}
```

## Performance Comparison

| Method | Load Time (DungeonRoom.unity) | Memory Overhead | Progress Accuracy |
|--------|-------------------------------|-----------------|-------------------|
| Resources.LoadAsync | 1.2s | Baseline | Poor (jumps to 0.9 instantly) |
| Addressables | 1.1s | +2MB (catalog) | Excellent (smooth 0→1) |

## Caveat
⚠️ **Initial catalog load**: First Addressables call adds ~150ms one-time overhead. Pre-warm catalog in Boot scene.

## Recommendation
**PROCEED** with Addressables. Implement catalog pre-warming in BootScene.

## Prototype Code
- Test scene: `.spikes/addressables-loading/bd-18/LoadingTest.unity`
- Script: `.spikes/addressables-loading/bd-18/AddressablesLoadingTest.cs`

## References
- Unity Addressables Docs: https://docs.unity3d.com/Packages/com.unity.addressables@1.21/manual/
- Confirmed compatible with Unity 6.0.3
```

### 3.3 Spike Closure & Decision

```bash
bd close bd-18

send_message(
  to=["Orchestrator"],
  thread_id="bd-18",
  subject="[Spike bd-18] FINDINGS: PROCEED",
  body_md="✅ Addressables validated for async scene loading.

**Decision**: PROCEED with implementation.

**Action item**: Add catalog pre-warming to BootScene (150ms one-time cost).

**Next steps**: Convert spike findings into implementation beads for dungeon streaming feature.

See full findings: `.spikes/addressables-loading/bd-18/FINDINGS.md`"
)
```

### 3.4 Follow-Up Epic Creation

```bash
# Based on spike success, create implementation epic
bd add "Implement async dungeon scene loading with Addressables" \
  --priority 1 \
  --epic

# Output: bd-19

# Add tasks based on spike findings
bd add "Pre-warm Addressables catalog in BootScene" \
  --parent bd-19 \
  --priority 1

# Output: bd-20

bd add "Implement SceneLoader.LoadDungeonAsync() using Addressables" \
  --parent bd-19 \
  --priority 1

# Output: bd-21
```

**Quick Reference**:
- **Pattern**: Spike → decision → feature conversion
- **Time-box**: 30 minutes
- **Output**: Findings document + prototype code
- **Decision**: PROCEED (with pre-warming caveat)
- **Follow-up**: 1 epic + 2 tasks created

---

## Example 4: Blocked Resolution - Missing Dependency

**Scenario**: Worker encounters missing event definition mid-execution and requests orchestrator intervention

### 4.1 Initial Bead Execution (bd-22)

**Worker2 executing bd-22**: "Implement CombatManager.OnHeroAttack event"

**Worker Actions**:
```bash
# Worker2 starts implementation
file_reservation_paths(paths=["Assets/_Project/Scripts/Combat/CombatManager.cs"], ...)

# Mid-implementation, discovers missing dependency
# HeroController needs to raise OnHeroAttacked event, but event doesn't exist
```

**Blocked Message**:
```bash
send_message(
  project_key="/path/to/project",
  sender_name="Worker2",
  to=["Orchestrator"],
  thread_id="bd-20", # Epic thread
  subject="[bd-22] BLOCKED: Missing OnHeroAttacked event definition",
  body_md="🚫 Cannot proceed with bd-22.

**Issue**: HeroController.cs is missing the OnHeroAttacked event definition that CombatManager needs to listen to.

**Required**:
- Define event in HeroController: `public UnityEvent<int> OnHeroAttacked;`
- Raise event in TakeDamage() method

**Files needed**:
- Assets/_Project/Scripts/Hero/HeroController.cs (currently reserved by Worker1 on bd-21)

**Blocker**: Worker1 has HeroController.cs reserved. Need hotfix bead to add event definition.

**Current state**: CombatManager event listener code written but commented out. Awaiting HeroController update."
)
```

### 4.2 Orchestrator Intervention

**Orchestrator checks file reservations**:
```bash
# Query active reservations
fetch_inbox(agent_name="Orchestrator", since_ts="2026-02-14T00:00:00Z")

# Discovers: Worker1 reserved HeroController.cs for bd-21 (different feature)
```

**Orchestrator Decision**: Create hotfix bead, assign to Worker1 (already has file reserved)

```bash
# Create hotfix bead
bd add "HOTFIX: Add OnHeroAttacked event to HeroController" \
  --parent bd-20 \
  --priority 1 \
  --depends-on bd-21 # Wait for Worker1's current task

# Output: bd-23
```

**Orchestrator Message to Worker1**:
```bash
send_message(
  sender_name="Orchestrator",
  to=["Worker1"],
  thread_id="track:Worker1:bd-20",
  subject="[HOTFIX] bd-23 - Unblock Worker2",
  body_md="🔧 Hotfix bead assigned: bd-23

**Task**: Add OnHeroAttacked event to HeroController
**Blocker**: Worker2 is blocked on bd-22 awaiting this event

**Changes needed**:
```csharp
// In HeroController.cs
public UnityEvent<int> OnHeroAttacked;

void TakeDamage(int damage) {
    currentHealth -= damage;
    OnHeroAttacked?.Invoke(damage); // Add this line
}
```

**Priority**: Complete after bd-21 (you already have HeroController.cs reserved).

**Notify**: Message Worker2 when bd-23 is closed so they can resume bd-22."
)
```

### 4.3 Hotfix Execution (bd-23)

**Worker1 Actions**:
```bash
# Worker1 completes bd-21 first
git commit -m "feat(hero): implement skill cooldown UI"
bd close bd-21

# Then immediately addresses bd-23 (file still reserved)
# Add OnHeroAttacked event definition...
git commit -m "fix(hero): add OnHeroAttacked event for combat integration

- Define UnityEvent<int> OnHeroAttacked
- Raise event in TakeDamage()

Unblocks bd-22"

bd close bd-23

# Release file reservation
release_file_reservations(agent_name="Worker1")
```

**Unblock Notification**:
```bash
send_message(
  sender_name="Worker1",
  to=["Worker2"],
  thread_id="track:Worker2:bd-20",
  subject="[bd-23] COMPLETE - Unblocked",
  body_md="✅ HeroController.OnHeroAttacked event added.

**Changes**:
- Event definition added: `public UnityEvent<int> OnHeroAttacked;`
- Event raised in TakeDamage(int damage)

**Worker2**: You can now resume bd-22. HeroController.cs is released."
)
```

### 4.4 Resume Original Bead (bd-22)

**Worker2 Actions**:
```bash
# Resume bd-22 implementation
# Uncomment CombatManager event listener code...
# Test integration...

git commit -m "feat(combat): implement OnHeroAttack event listener

- Listen to HeroController.OnHeroAttacked
- Trigger combat response logic

Closes bd-22 (was blocked by bd-23)"

bd close bd-22

send_message(
  to=["Orchestrator"],
  thread_id="bd-20",
  subject="[bd-22] COMPLETE",
  body_md="✅ CombatManager event integration complete.

**Resolution**: Hotfix bd-23 resolved blocker. Event listener now functional."
)
```

**Quick Reference**:
- **Pattern**: Worker blocked → orchestrator hotfix → resume
- **Message**: `[bd-X] BLOCKED: <reason>` triggers intervention
- **Hotfix priority**: 1 (high) to minimize blocked time
- **Notification**: Explicit unblock message from hotfix worker to blocked worker
- **File discipline**: Hotfix assigned to worker who already has file reserved

---

## Example 5: Interface Change Propagation - Item System Refactor

**Scenario**: Epic bd-30 refactors item system from `int itemId` to `ScriptableObject Item`. Multiple workers need notification to update their code.

### 5.1 Interface Change Detection

**Worker3 executing bd-31**: "Refactor ItemManager to use ScriptableObject-based items"

**Mid-implementation, Worker3 realizes**: This breaks public API used by 4 other beads currently in progress.

**Interface Change Broadcast**:
```bash
send_message(
  sender_name="Worker3",
  to=["Worker1", "Worker2", "Worker4", "Worker5"],
  cc=["Orchestrator"],
  thread_id="bd-30", # Epic thread (NOT individual worker threads)
  subject="[Interface Change] ItemManager API: int itemId → ScriptableObject Item",
  importance="high",
  body_md="⚠️ **Breaking API Change in bd-31**

## What Changed

**Old API** (deprecated):
```csharp
ItemManager.GetItem(int itemId)
ItemManager.AddToInventory(int itemId, int count)
```

**New API** (use this):
```csharp
ItemManager.GetItem(Item itemSO)
ItemManager.AddToInventory(Item itemSO, int count)
```

## Migration Guide

### Before:
```csharp
int swordId = 101;
itemManager.AddToInventory(swordId, 1);
```

### After:
```csharp
[SerializeField] Item swordItemSO; // Assign in Inspector
itemManager.AddToInventory(swordItemSO, 1);
```

## Affected Beads

If your bead uses ItemManager, update your code:
- bd-32 (Worker1): LootDropper uses GetItem(int) → update to Item SO reference
- bd-33 (Worker2): ShopUI displays items by ID → update to Item SO array
- bd-34 (Worker4): QuestRewards gives items by ID → update to Item SO rewards
- bd-35 (Worker5): SaveSystem serializes item IDs → update to GUID-based serialization

## Timeline

- **bd-31 merge**: Expected today (2026-02-15)
- **Your deadline**: Update your code before merging to avoid conflicts

## Need Help?

Reply to this thread if you need clarification on migration.

**Orchestrator**: Please track this change across affected beads."
)
```

### 5.2 Orchestrator Tracking

**Orchestrator Actions**:

1. **Acknowledge broadcast**:
```bash
send_message(
  to=["Worker1", "Worker2", "Worker4", "Worker5"],
  thread_id="bd-30",
  subject="[Interface Change] Acknowledged - Tracking Updates",
  body_md="📋 Tracking API migration across 4 affected beads.

**Action required** by each worker:
- Update code to use ScriptableObject Item instead of int itemId
- Reply to this thread when your bead's migration is complete

**Deadline**: Before merging your bead (to prevent merge conflicts)

I'll validate all migrations before closing epic bd-30."
)
```

2. **Update bead dependencies**:
```bash
# Mark bd-31 as dependency for affected beads
bd update bd-32 --depends-on bd-31
bd update bd-33 --depends-on bd-31
bd update bd-34 --depends-on bd-31
bd update bd-35 --depends-on bd-31
```

### 5.3 Worker Responses

**Worker1 (bd-32)**:
```bash
send_message(
  to=["Orchestrator"],
  thread_id="bd-30",
  subject="[bd-32] Migration Complete",
  body_md="✅ LootDropper updated to use Item ScriptableObject.

**Changes**:
- Replaced `int lootTableItemIds[]` with `Item[] lootTableItems`
- Updated GetItem(int) calls to direct SO references
- Tested: Loot drops work correctly

**Commit**: refactor(loot): migrate to ScriptableObject Item system"
)
```

**Worker2 (bd-33)**:
```bash
send_message(
  to=["Orchestrator"],
  thread_id="bd-30",
  subject="[bd-33] Migration Complete",
  body_md="✅ ShopUI updated to use Item ScriptableObject array.

**Changes**:
- Shop data now references `Item[] shopInventory` instead of int IDs
- UI displays item name/icon directly from SO fields
- Removed ID→Item lookup code (cleaner now)

**Commit**: refactor(ui): migrate ShopUI to Item ScriptableObject"
)
```

*(Worker4 and Worker5 respond similarly)*

### 5.4 Orchestrator Validation

**After all migrations complete**:

```bash
# Orchestrator validates all affected beads updated
# Checks commits contain "refactor" keyword and Item SO references
# Confirms no compilation errors

send_message(
  to=["Worker1", "Worker2", "Worker4", "Worker5"],
  thread_id="bd-30",
  subject="[Interface Change] All Migrations Verified ✅",
  body_md="✅ All 4 affected beads successfully migrated to Item ScriptableObject API.

**Status**:
- bd-32 (LootDropper): ✅ Migrated
- bd-33 (ShopUI): ✅ Migrated
- bd-34 (QuestRewards): ✅ Migrated
- bd-35 (SaveSystem): ✅ Migrated

**Compilation**: No errors
**Integration test**: Item system works across all features

Proceeding with epic bd-30 closure."
)
```

### 5.5 Epic Closure

```bash
bd close bd-30

send_message(
  to=["ProjectLead"],
  thread_id="bd-30",
  subject="[Epic bd-30] COMPLETE - Item System Refactored",
  body_md="✅ Item system successfully refactored to ScriptableObject architecture.

**Scope**:
- Core refactor: bd-31 (ItemManager API change)
- Propagated to 4 dependent systems (Loot, Shop, Quests, Save)
- All migrations validated, no integration issues

**Impact**:
- Cleaner code (removed ID→Item lookups)
- Type-safe item references
- Easier data authoring (Inspector-friendly)

**Commits**: 5 (1 core refactor + 4 migrations)"
)
```

**Quick Reference**:
- **Pattern**: Breaking change → broadcast → track migrations → validate
- **Subject**: `[Interface Change] <summary>` for high visibility
- **Broadcast to**: All affected workers + Orchestrator
- **Thread**: Epic thread (NOT worker threads)
- **Dependencies**: Update `bd update --depends-on` to enforce merge order
- **Validation**: Orchestrator confirms all migrations before epic closure

---

## Quick Reference: Common Patterns

### Pattern: Linear Workflow (Example 1)
```
Discovery → Risk (LOW) → Epic → Task → Complete
No spike, no parallelism, single worker.
```

### Pattern: Spike-Gated Workflow (Example 2)
```
Discovery → Risk (HIGH) → Spike → Decision (PROCEED) → 
  Decompose → Parallel Tracks → Complete
Spike validates unknowns before feature work.
```

### Pattern: Spike-Only Workflow (Example 3)
```
Spike → Decision → (Convert to epic OR abort)
Validation-only, no immediate implementation.
```

### Pattern: Blocked → Hotfix (Example 4)
```
Worker1: Task A → BLOCKED (missing X)
Orchestrator: Create Hotfix B → Assign Worker2
Worker2: Hotfix B → Complete
Worker1: Resume Task A → Complete
```

### Pattern: Interface Change (Example 5)
```
Worker3: Refactor (breaking API change detected)
Worker3: Broadcast [Interface Change] to affected workers
Orchestrator: Track migrations, update dependencies
Workers 1,2,4,5: Migrate code → Report complete
Orchestrator: Validate all migrations → Close epic
```

---

## Template Selection Guide

| Scenario | Use Template | Example Reference |
|----------|--------------|-------------------|
| Starting new feature | Discovery Report → Risk Assessment | Example 1, 2 |
| HIGH risk feature | Spike Bead | Example 2, 3 |
| Creating task breakdown | Epic Bead → Task Bead (×N) | Example 1, 2 |
| Spawning worker | Worker Prompt | Example 1, 2 |
| Bead finished | Message: COMPLETE | Example 1, 2 |
| Bead stuck | Message: BLOCKED | Example 4 |
| API changes | Message: Interface Change | Example 5 |
| Track finished | Message: Track Complete | Example 2 |
| Spike results | Spike Findings Document | Example 2, 3 |
| Epic finished | Integration Checklist | Example 2 |

---

## Common Command Sequences

### Simple Feature (1 epic, 1 task)
```bash
bd add "Feature description" --epic
bd add "Implementation task" --parent bd-X --priority 2
# Execute task...
bd close bd-Y
bd close bd-X
```

### Spike → Feature Conversion
```bash
bd add "SPIKE: Validation question" --priority 0
# Execute spike, document findings...
bd close bd-X
# If PROCEED:
bd add "Implement feature (validated by bd-X)" --epic
bd add "Task 1" --parent bd-Y --priority 1
```

### Hotfix for Blocked Worker
```bash
# Blocked worker sends [bd-N] BLOCKED message
# Orchestrator:
bd add "HOTFIX: Unblock bd-N" --priority 1 --parent bd-epic
# Assign to worker with reserved files...
# After hotfix:
bd close bd-hotfix
# Blocked worker resumes bd-N
```

### Parallel Tracks
```bash
bd add "Epic" --epic
bd add "Task 1" --parent bd-X --priority 1
bd add "Task 2" --parent bd-X --priority 1
bd add "Task 3" --parent bd-X --priority 1
# Plan tracks:
bv --robot-plan --bead bd-X
# Spawn Worker1 for Track 1, Worker2 for Track 2...
```

---

**End of Examples Document**
