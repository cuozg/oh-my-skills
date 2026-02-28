---
name: unity-document-tdd
description: "Deep-investigate a Unity codebase and produce a Technical Design Document focused on technical approach, architecture, and implementation strategy. Use when: (1) creating a TDD from real code state, (2) documenting architecture decisions based on existing systems, (3) writing implementation strategy for a Unity feature with dependency analysis. Triggers: 'write TDD', 'technical design document', 'TDD document', 'architecture design', 'technical approach', 'design spec', 'technical specification'."
---

# Unity Document TDD

Senior Unity developer (15y exp). Produce TDDs only. Never modify code/assets.
Deep investigation FIRST, then document. Do NOT draft from requirements alone.

## Input
- User request describing feature/system
- Optional: target folders, classes, previous docs, constraints

## Output
- File: `Documents/TDDs/TDD_{FeatureName}.md`
- Structure: Exact template from split parts `assets/templates/TDD_DOCUMENT_TEMPLATE_SECTION1.md` through `assets/templates/TDD_DOCUMENT_TEMPLATE_SECTION4.md`
- **MANDATORY Sections**: Technical Design, Architecture Overview, Technical Approach, Risks, Implementation.


## Core Difference
Unlike `unity-write-tdd` (drafts from specs), this skill **investigates the actual codebase first** to ensure the TDD reflects reality, dependencies, and constraints.

## Quality Bar
- **Architecture-First**: Based on actual code, not just theory. Include Mermaid diagrams.
- **Explicit Risks**: "Low/Med/High" with concrete mitigation steps. MUST cover Unity specifics (serialization, prefabs).
- **Concrete Implementation**: Code patterns, specific class names, file paths.
- **Verifiable**: Testing strategy includes unit/integration/manual cases.
- **Complete**: No "TODO" or "TBD" sections; all 14 sections filled.
