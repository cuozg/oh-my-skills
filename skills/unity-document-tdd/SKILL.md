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

## Workflow
1. **Scope**: Parse request, identify feature boundary, define success criteria.
2. **Investigate**:
   - Map architecture: `scripts/trace_architecture.py`, `glob`, `read`.
   - Trace symbols: `lsp_symbols`, `lsp_find_references`, `lsp_goto_definition`.
   - Analyze risk: `impact-analyzer`, `grep` (events, serialization, managers).
3. **Analyze**: Convert discoveries into decisions, patterns, and approach options.
4. **Generate**: Fill `TDD_DOCUMENT_TEMPLATE_SECTION1.md` through `TDD_DOCUMENT_TEMPLATE_SECTION4.md` completely with concrete details.
5. **Validate**: Check all sections filled, diagrams valid, references correct.

## Focus Area Mapping
| User Focus | Template Section | Content Requirement |
|:---|:---|:---|
| **Technical Design** | 3.2 (ADRs) & 4 (Approach) | Key decisions, rationale, alternatives considered. |
| **Architecture** | 3 (Architecture Overview) | System context (3.1), Module Dependencies, Class diagrams (3.3). |
| **Technical Approach**| 4 (Technical Approach) | Components, data models, logic/state diagrams, API surface. |
| **Risks** | 7 (Risk Assessment) | Tech/Unity-Specific/Perf/Compat risks with prob/impact/mitigation. |
| **Implementation** | 6 (Implementation) | Step-by-step plan, migration steps, feature flags. |

## Core Difference
Unlike `unity-write-tdd` (drafts from specs), this skill **investigates the actual codebase first** to ensure the TDD reflects reality, dependencies, and constraints.

## Investigation Checklist
- [ ] Interfaces/contracts & Abstract base classes
- [ ] ScriptableObject data pipelines & configuration
- [ ] MonoBehaviour lifecycle & orchestration
- [ ] Event flow (C# events, UnityEvent, MessageBus)
- [ ] External dependencies (Packages, Services)

## Quality Bar
- **Architecture-First**: Based on actual code, not just theory. Include Mermaid diagrams.
- **Explicit Risks**: "Low/Med/High" with concrete mitigation steps. MUST cover Unity specifics (serialization, prefabs).
- **Concrete Implementation**: Code patterns, specific class names, file paths.
- **Verifiable**: Testing strategy includes unit/integration/manual cases.
- **Complete**: No "TODO" or "TBD" sections; all 14 sections filled.
