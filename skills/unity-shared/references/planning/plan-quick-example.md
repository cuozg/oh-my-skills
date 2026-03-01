# Example Assessment

**Input**: "Add daily login reward system"

**Assessment Output**:

```
▲ Daily Login Reward System
  M · 12-20 hours · Med risk
  New system (6-8 files) with data persistence and UI; extends RewardManager with timezone-sensitive streak tracking.

  ┌ Tasks
  ├─ Core logic + data model
  │  DailyLoginModel, streak tracker, reward config SO → skill:unity-code-deep
  ├─ UI screen + animations
  │  Daily reward popup, claim flow, streak display → skill:unity-ui
  ├─ Save/load + timezone handling
  │  Persistent timestamps, server-time sync, exploit prevention → skill:unity-serialization
  └─ Testing + polish
     Unit tests for streak logic, timezone edge cases → skill:unity-test-unit
```

**Task System Recording** (Step 5):

```
// Parent task
task_create(
  subject: "▲ Daily Login Reward System",
  description: "<full assessment tree text above>",
  metadata: { cost: "M", costHours: "12-20h", risk: "Med",
              skillSource: "unity-plan-quick" }
)
// → Returns T-abc123

// Child tasks — one per ┌ Tasks entry
task_create(
  subject: "Core logic + data model",
  description: "DailyLoginModel, streak tracker, reward config SO",
  parentID: "T-abc123",
  metadata: { cost: "S", costHours: "3-5h", risk: "Low",
              skill: "unity-code-deep", skillSource: "unity-plan-quick" }
)

task_create(
  subject: "UI screen + animations",
  description: "Daily reward popup, claim flow, streak display",
  parentID: "T-abc123",
  metadata: { cost: "S", costHours: "4-6h", risk: "Low",
              skill: "unity-ui", skillSource: "unity-plan-quick" }
)

task_create(
  subject: "Save/load + timezone handling",
  description: "Persistent timestamps, server-time sync, exploit prevention",
  parentID: "T-abc123",
  metadata: { cost: "S", costHours: "3-5h", risk: "High",
              skill: "unity-serialization", skillSource: "unity-plan-quick" }
)

task_create(
  subject: "Testing + polish",
  description: "Unit tests for streak logic, timezone edge cases",
  parentID: "T-abc123",
  metadata: { cost: "XS", costHours: "2-4h", risk: "Low",
              skill: "unity-test-unit", skillSource: "unity-plan-quick" }
)
```

> Child tasks map 1:1 to `┌ Tasks` entries. Skip children for single-task assessments.
