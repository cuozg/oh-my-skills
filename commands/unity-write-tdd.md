---
description: Workflow for generating a Technical Design Document (TDD) based on the project template, using the output from the unity-plan skill.
---

# Workflow: Write TDD

Generate professional Technical Design Documents (TDD) based on implementation plans.

1.  **Locate Source**:
    - Find the latest plan in `Documents/Plans/IMPLEMENTATION_PLAN_[Feature].md`.
    - If missing, run `/unity-plan` first.
2.  **Define Architecture**:
    - Document foundational assumptions and performance constraints (FPS/Memory/CPU).
    - Map feature epics into logical TDD Components.
3.  **Detail Logic**:
    - Define UI lifecycles, asset loading schemes, and client-server interactions.
    - Specify API references and data blueprint changes.
4.  **Generate Document**:
    - Use the `UNITY_TDD_TEMPLATE.md` from `.claude/skills/unity-write-tdd/assets/templates/`.
    - Save the TDD in `Documents/TDDs/TDD_[Feature].md`.
5.  **Validation**:
    - Ensure all mandatory sections (Architecture, Components, API, Analytics) are addressed.
    - Present the final TDD to the user for technical review.
