# Quick Plan Output Format

## Template

```markdown
## {Feature Name}
{size} | {hours} | {risk} risk

{1-sentence summary with evidence}

Product / release surface: {None, or KPI/analytics/LiveOps/API/release risk}

### Tasks
- [ ] {subject}
  - {description}
  - Skill: `{skill-name}`
- [ ] {subject}
  - {description}
  - Skill: `{skill-name}`
- [ ] {subject}
  - {description}
  - Skill: `{skill-name}`
```

## Example

```markdown
## Add Player Health System
S | 2-4h | Low risk

Add health component with damage/heal API and death event, based on existing IDamageable pattern in Assets/Scripts/Interfaces/.

### Tasks
- [ ] Implement HealthComponent MonoBehaviour
  - Track current/max HP, expose TakeDamage/Heal, fire OnDeath event.
  - Serialized fields for maxHealth and invincibility duration.
  - Skill: `unity-standards`
- [ ] Create HealthBar UI prefab
  - Slider-based bar, subscribe to HealthComponent events.
  - Follow existing UI pattern in Assets/Prefabs/UI/.
  - Skill: `unity-standards`
- [ ] Write HealthComponent unit tests
  - Cover damage clamp, heal cap, death trigger, and negative input.
  - Skill: `unity-test-unit`
```

## Field Rules

| Field       | Format                                      |
|-------------|---------------------------------------------|
| Size        | XS/S/M/L                                    |
| Hours       | Range (e.g., 2-4h)                          |
| Risk        | Low / Medium / High / Critical              |
| Summary     | 1 sentence, reference existing code/patterns|
| Subject     | Imperative verb + target                    |
| Description | What + why + constraints (2-3 lines max)    |
| Skill       | Exact skill name from skill registry        |
| Product / release surface | Mention analytics, LiveOps, server, IAP, release, or monitoring only when touched |

## Metadata Line

Single line: `{size} | {hours} | {risk} risk`
