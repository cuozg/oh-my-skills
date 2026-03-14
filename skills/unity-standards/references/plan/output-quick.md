# Quick Plan Output Format

## Template

```
▲ {Feature Name}
{size} · {hours} · {risk} risk

{1-sentence summary with evidence}

┌ Tasks
├─ {subject}
│  {description}
│  → skill:{skill-name}
├─ {subject}
│  {description}
│  → skill:{skill-name}
└─ {subject}
   {description}
   → skill:{skill-name}
```

## Example

```
▲ Add Player Health System
S · 2-4h · Low risk

Add health component with damage/heal API and death event, based on existing IDamageable pattern in Assets/Scripts/Interfaces/.

┌ Tasks
├─ Implement HealthComponent MonoBehaviour
│  Track current/max HP, expose TakeDamage/Heal, fire OnDeath event.
│  Serialized fields for maxHealth, invincibility duration.
│  → skill:unity-code
├─ Create HealthBar UI prefab
│  Slider-based bar, subscribe to HealthComponent events.
│  Follow existing UI pattern in Assets/Prefabs/UI/.
│  → skill:unity-code
└─ Write HealthComponent unit tests
   Cover: damage clamp, heal cap, death trigger, negative input.
   → skill:unity-test-unit
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

## Metadata Line

Single line: `{size} · {hours} · {risk} risk`
