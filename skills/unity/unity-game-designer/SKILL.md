---
name: unity-game-designer
description: "(opencode-project - Skill) Game design documentation and brainstorming for Unity projects. Generate Game Design Documents (GDD), brainstorm core loops, progression systems, economy models, and social features. Use when: (1) Conceptualizing a new game or feature from scratch, (2) Brainstorming core loops, progression, or economy systems, (3) Writing or updating a Game Design Document, (4) Evaluating monetization or engagement strategies, (5) Documenting game mechanics for a development team, (6) Comparing design patterns (F2P, premium, battle pass, etc.). Triggers: 'game concept', 'game design', 'brainstorm mechanics', 'write GDD', 'game design document', 'core loop', 'progression system', 'economy design', 'monetization', 'game pitch', 'feature spec', 'mechanic design', 'game idea'."
---

# Unity Game Designer

**Input**: Game concept, feature idea, or design problem + optional platform, audience, genre, constraints
**Output**: GDD at `Documents/GDD/GDD_[GameName].md`, feature spec at `Documents/GDD/Feature_[FeatureName].md`, or inline brainstorm

## Workflow

### Phase 1: Requirements Intake
Gather before designing (ask if missing):
1. **Concept**: One-sentence pitch
2. **Genre**: Primary + secondary tags
3. **Platform**: Mobile, PC, Console, Cross-platform
4. **Audience**: Age range, player archetype (casual/mid-core/hardcore)
5. **Monetization**: F2P, premium, hybrid, subscription

Optional: session length, retention goals, art style, competitive refs (up to 3)

### Phase 2: Mechanic Brainstorming
Load [mechanics-patterns.md](references/mechanics-patterns.md) for reusable patterns.
1. Identify 2-3 candidate core loops matching genre/audience
2. Propose progression systems from patterns reference
3. Draft economy model aligned with monetization
4. Suggest social/multiplayer hooks if applicable
5. Evaluate each: depth/complexity ratio, implementation cost, retention impact, monetization fit

### Phase 3: GDD Generation
Load [gdd-template.md](references/gdd-template.md) and populate all sections.
1. Read template, populate using Phase 1+2 outputs
2. Add Unity implementation notes (scenes, prefabs, systems)
3. Include platform-specific considerations
4. Save to `Documents/GDD/GDD_[GameName].md`

**Validation**: executive summary is jargon-free, core loop diagram included, economy has sink/source balance, progression has milestones, FTUE covered, implementation roadmap prioritized

## Decision Tree

```
"game idea" / "new concept"     → Phase 1 → 2 → 3 (full pipeline)
"brainstorm mechanics"          → Phase 1 (quick) → Phase 2 only
"write a GDD"                   → Phase 1 → Phase 3
"evaluate this mechanic"        → Phase 2 only
"update the GDD"                → Read existing → Phase 3 (incremental)
"game pitch"                    → Phase 1 → Executive Summary only
```

## Unity-Specific Guidance

- **Scenes**: Map game states to scenes (Main Menu, Gameplay, Results)
- **ScriptableObjects**: Use for config data (level defs, item stats, economy tables)
- **Addressables**: Flag assets needing dynamic loading
- **UI approach**: Recommend UI Toolkit vs uGUI based on complexity

## References

| File | When | Content |
|:---|:---|:---|
| [gdd-template.md](references/gdd-template.md) | Phase 3 | Full GDD section structure |
| [mechanics-patterns.md](references/mechanics-patterns.md) | Phase 2 | Progression, economy, social, monetization patterns |
