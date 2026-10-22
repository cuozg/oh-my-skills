# Feature Spec: {Feature_Name}

## 1. Overview

- **Feature**: {Feature_Name}
- **Version**: {version}
- **Date**: {date}
- **Status**: {Draft|Review|Approved}
- **Parent GDD**: {link to _INDEX.md or "Standalone"}
- **Owner**: {author}

**Summary**: {2-3 sentence description of what this feature does and why it exists}

**Goals**:
- {goal_1}
- {goal_2}

**Non-Goals** (explicitly out of scope):
- {non_goal_1}
- {non_goal_2}

---

## 2. Core Mechanics

### Player Experience

{What the player sees, feels, and does when interacting with this feature}

### Rules & Behavior

| Rule | Description |
|------|-------------|
| {rule_name} | {what_happens} |

### Player Actions

| Action | Input | Result | Feedback |
|--------|-------|--------|----------|
| {action} | {input_binding} | {what_happens} | {visual/audio/haptic} |

### Gameplay Loop

```mermaid
flowchart TD
    A[{entry_point}] --> B[{action}]
    B --> C{"{decision}"}
    C -->|{outcome_a}| D[{result_a}]
    C -->|{outcome_b}| E[{result_b}]
    D --> A
    E --> A
```

---

## 3. Systems Design

### Architecture

```mermaid
classDiagram
    class {MainClass} {
        +{property}
        +{method}()
    }
    class {SupportClass} {
        +{property}
        +{method}()
    }
    {MainClass} --> {SupportClass} : {relationship}
```

### Components

| Component | Responsibility | Key Methods |
|-----------|---------------|-------------|
| {class_name} | {what_it_does} | {public_api} |

### State Machine (if applicable)

```mermaid
stateDiagram-v2
    [*] --> {initial_state}
    {initial_state} --> {state_2} : {trigger}
    {state_2} --> {state_3} : {trigger}
    {state_3} --> [*]
```

### Events

| Event | Publisher | Subscriber(s) | Payload |
|-------|----------|---------------|---------|
| {event_name} | {who_raises} | {who_listens} | {data_type} |

---

## 4. Data Model

### Runtime Data

| Field | Type | Purpose | Default |
|-------|------|---------|---------|
| {field_name} | {type} | {what_it_stores} | {default_value} |

### Configuration (ScriptableObjects)

| Config | Fields | Purpose |
|--------|--------|---------|
| {config_name} | {key_fields} | {what_it_configures} |

### Persistence (if applicable)

| Data | Storage | Format | When Saved |
|------|---------|--------|------------|
| {data_name} | {PlayerPrefs/JSON/Binary} | {format} | {trigger} |

---

## 5. UX/UI Flows

### Screen Flow

```mermaid
flowchart TD
    A[{entry_screen}] --> B[{interaction}]
    B --> C{"{outcome}"}
    C -->|{option_a}| D[{screen_a}]
    C -->|{option_b}| E[{screen_b}]
```

### UI Elements

| Element | Type | Purpose | Interaction |
|---------|------|---------|-------------|
| {element_name} | {Button/Slider/Panel} | {what_it_shows} | {how_user_interacts} |

### Feedback & Juice

| Event | Visual | Audio | Haptic |
|-------|--------|-------|--------|
| {trigger} | {vfx/animation} | {sfx} | {vibration} |

---

## 6. Dependencies & Integration

### Depends On

| System | How Used | Coupling |
|--------|----------|----------|
| {system_name} | {interface/event/direct} | {Loose/Tight} |

### Depended By

| Consumer | What It Needs | Impact if Changed |
|----------|--------------|-------------------|
| {system_name} | {api/event/data} | {Low/Medium/High} |

### Integration Points

- {How this feature connects to other features — event channels, shared interfaces, inspector references}

---

## 7. Content (if applicable)

### Items / Entities

| Name | Category | Properties | Rarity/Tier |
|------|----------|------------|-------------|
| {name} | {category} | {key_properties} | {rarity} |

### Balancing Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| {param_name} | {value} | {why_this_value} |

### Progression

| Gate | Requirement | Unlocks |
|------|------------|---------|
| {gate_name} | {condition} | {what_unlocks} |

---

## 8. Technical Constraints

| Constraint | Target | Rationale |
|-----------|--------|-----------|
| {constraint_name} | {value} | {why_this_limit} |

### Platform Considerations

- {platform_specific_note_1}
- {platform_specific_note_2}

---

## 9. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {risk_description} | {Low/Medium/High} | {Low/Medium/High} | {strategy} |

---

## 10. Open Questions

- {question_1}
- {question_2}

---

## Validation Checklist

- [ ] Sections 1-6 fully filled — no placeholders remain
- [ ] At least 1 Mermaid diagram present (architecture, state, or flow)
- [ ] No TODO/TBD/FIXME text
- [ ] All `[ASSUMED]` tags reviewed
- [ ] Dependencies mapped with coupling level
- [ ] Events documented with publisher/subscriber
- [ ] Risks have mitigations
