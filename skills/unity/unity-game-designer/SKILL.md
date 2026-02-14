---
name: unity-game-designer
description: "(opencode-project - Skill) Game design documentation and brainstorming for Unity projects. Generate Game Design Documents (GDD), brainstorm core loops, progression systems, economy models, and social features. Use when: (1) Conceptualizing a new game or feature from scratch, (2) Brainstorming core loops, progression, or economy systems, (3) Writing or updating a Game Design Document, (4) Evaluating monetization or engagement strategies, (5) Documenting game mechanics for a development team, (6) Comparing design patterns (F2P, premium, battle pass, etc.). Triggers: 'game concept', 'game design', 'brainstorm mechanics', 'write GDD', 'game design document', 'core loop', 'progression system', 'economy design', 'monetization', 'game pitch', 'feature spec', 'mechanic design', 'game idea'."
---

# Unity Game Designer

Game design documentation and mechanic brainstorming for Unity projects. Transform game concepts into structured, production-ready Game Design Documents with validated mechanics, economy models, and implementation roadmaps.

## Input

- **Required**: Game concept, feature idea, or design problem to solve
- **Optional**: Target platform, audience, genre, existing project constraints

## Output

| Output Type | File Location |
|:---|:---|
| Full GDD | `Documents/GDD/GDD_[GameName].md` |
| Feature spec | `Documents/GDD/Feature_[FeatureName].md` |
| Brainstorm notes | Inline response (no file) |

## Workflow

Execute one of three phases based on user intent. Phases may run independently or sequentially.

### Phase 1: Requirements Intake

Gather foundational information before designing. Ask clarifying questions when information is missing.

**Required inputs** (ask if not provided):
1. **Concept**: One-sentence game pitch
2. **Genre**: Primary and secondary genre tags
3. **Platform**: Mobile, PC, Console, Cross-platform
4. **Audience**: Age range, player archetype (casual, mid-core, hardcore)
5. **Monetization**: F2P, premium, hybrid, subscription

**Optional inputs** (use defaults if omitted):
- Session length target (default: 5-15 min mobile, 30-60 min PC)
- Retention goals (D1, D7, D30 benchmarks)
- Art style preference
- Competitive references (up to 3 games)

**Output**: Structured requirements summary used by Phase 2 and Phase 3.

### Phase 2: Mechanic Brainstorming

Ideate and evaluate game systems. Load [mechanics-patterns.md](references/mechanics-patterns.md) for reusable design patterns.

**Process**:
1. Identify 2-3 candidate **core loops** matching genre and audience
2. Propose **progression systems** (see patterns reference for options)
3. Draft **economy model** aligned with monetization strategy
4. Suggest **social/multiplayer hooks** if applicable
5. Evaluate each mechanic against constraints (platform, session length, audience)

**Evaluation criteria** per mechanic:
- Depth vs. complexity ratio
- Implementation cost estimate (Low/Medium/High)
- Retention impact (engagement driver vs. nice-to-have)
- Monetization compatibility

**Output**: Ranked list of recommended mechanics with rationale.

### Phase 3: GDD Generation

Produce a structured Game Design Document. Load [gdd-template.md](references/gdd-template.md) and populate all sections.

**Process**:
1. Read the GDD template reference for full section structure
2. Populate each section using Phase 1 requirements and Phase 2 mechanics
3. Add implementation notes relevant to Unity (scenes, prefabs, systems)
4. Include platform-specific considerations
5. Save to `Documents/GDD/GDD_[GameName].md`

**Validation checklist** before delivering:
- [ ] Executive summary is one paragraph, no jargon
- [ ] Core loop diagram described (text-based flowchart)
- [ ] Economy has sink/source balance documented
- [ ] Progression has clear milestones with unlock schedule
- [ ] UX flow covers first-time user experience (FTUE)
- [ ] Technical constraints section addresses target platforms
- [ ] Implementation roadmap has prioritized phases

## Decision Tree

```
User says...
├── "I have a game idea" / "new game concept"
│   └── Phase 1 → Phase 2 → Phase 3 (full pipeline)
├── "brainstorm mechanics" / "core loop ideas"
│   └── Phase 1 (quick) → Phase 2 only
├── "write a GDD" / "document this design"
│   └── Phase 1 → Phase 3 (skip brainstorming)
├── "evaluate this mechanic" / "compare approaches"
│   └── Phase 2 only (focused evaluation)
├── "update the GDD" / "add feature to GDD"
│   └── Read existing GDD → Phase 3 (incremental update)
└── "game pitch" / "elevator pitch"
    └── Phase 1 → Executive Summary only
```

## Unity-Specific Guidance

When generating GDD sections, consider these Unity implementation details:

- **Scenes**: Map major game states to Unity scenes (Main Menu, Gameplay, Results)
- **Prefabs**: Identify reusable entities (enemies, items, UI panels)
- **ScriptableObjects**: Use for game config data (level definitions, item stats, economy tables)
- **Addressables**: Flag assets that need dynamic loading (levels, cosmetics)
- **UI Toolkit vs uGUI**: Recommend UI approach based on complexity

## References

| File | When to Load | Content |
|:---|:---|:---|
| [gdd-template.md](references/gdd-template.md) | Phase 3 — GDD generation | Full GDD section structure with guidance per section |
| [mechanics-patterns.md](references/mechanics-patterns.md) | Phase 2 — brainstorming | Reusable design patterns: progression, economy, social, monetization |

## Examples

| User Request | Workflow | Output |
|:---|:---|:---|
| "Design a mobile idle RPG" | Phase 1 → 2 → 3 | Full GDD at `Documents/GDD/GDD_IdleRPG.md` |
| "Brainstorm progression for our puzzle game" | Phase 2 | Ranked mechanic recommendations |
| "Write a GDD for the tower defense we discussed" | Phase 1 → 3 | GDD from existing context |
| "What monetization fits a casual match-3?" | Phase 2 (focused) | Economy pattern comparison |
| "Add a guild system to our GDD" | Phase 3 (update) | Updated GDD with guild feature |
