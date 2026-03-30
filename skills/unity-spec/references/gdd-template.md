# Game Design Specification: {Game_Title}

## Metadata

- **Title**: {Game_Title}
- **Version**: {version}
- **Date**: {date}
- **Status**: {Draft|Review|Approved}
- **Author**: {author}
- **Target Platforms**: {platforms}

---

## Game Overview

**Elevator Pitch**: {2-3 sentence pitch describing the core experience}

- **Genre**: {genre}
- **Target Audience**: {audience}
- **Core Fantasy**: {what the player feels}
- **Unique Selling Points**:
  - {usp_1}
  - {usp_2}
  - {usp_3}

---

## Feature Map

Each feature has its own spec file in `Docs/Specs/`. Status tracks spec completeness, not implementation.

| Feature | File | Status | Priority |
|---------|------|--------|----------|
| {feature_name} | [{Feature_Name}.md]({Feature_Name}.md) | {Draft/Review/Approved} | {P0/P1/P2} |
| {feature_name} | [{Feature_Name}.md]({Feature_Name}.md) | {Draft/Review/Approved} | {P0/P1/P2} |

---

## Primary Gameplay Loop

```mermaid
flowchart TD
    A[{loop_start}] --> B[{action_1}]
    B --> C[{action_2}]
    C --> D{"{decision}"}
    D -->|{outcome_a}| E[{reward}]
    D -->|{outcome_b}| F[{consequence}]
    E --> A
    F --> A
```

---

## Art Direction

- **Visual Style**: {style}
- **Color Palette**: {colors}
- **Reference / Mood**: {references}
- **Animation Style**: {approach}
- **Camera**: {type and behavior}

---

## Audio

- **Music Style**: {genre and mood}
- **SFX Categories**:
  - {category_1}: {description}
  - {category_2}: {description}
- **Voice Acting**: {needs}
- **Audio Middleware**: {middleware}

---

## Global Technical Constraints

| Constraint | Target |
|-----------|--------|
| Target FPS | {fps} |
| Memory Budget | {memory} MB |
| Load Time | {seconds}s max |
| Min Spec | {hardware} |
| Max Draw Calls | {count} |

---

## Platform Targets

| Platform | Priority | Notes |
|----------|----------|-------|
| {platform} | {P0/P1/P2} | {notes} |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {risk} | {Low/Medium/High} | {Low/Medium/High} | {strategy} |

---

## Milestones (Optional)

| Milestone | Target Date | Deliverables |
|-----------|-------------|--------------|
| {name} | {date} | {deliverables} |

---

## Validation Checklist

- [ ] Game Overview filled with pitch, genre, audience
- [ ] Feature Map lists all features with file links
- [ ] All referenced feature files exist in Docs/Specs/
- [ ] Primary gameplay loop diagram present
- [ ] At least 3 features have specs
- [ ] Platform targets defined with priorities
- [ ] Risk table has at least 3 entries
- [ ] No TODO/TBD/FIXME text
- [ ] No unfilled `{placeholder}` text
