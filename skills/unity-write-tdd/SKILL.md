---
description: 'Generate Technical Design Documents for Unity projects. Document game
  systems, architecture decisions, client/server logic, API specs, and data schemas.
  Use when: (1) Formalizing Unity feature plans into specs, (2) Documenting MonoBehaviour/ScriptableObject
  architectures, (3) Defining gameplay systems and data flow, (4) Specifying multiplayer
  or backend integration, (5) Creating onboarding docs for Unity developers. Triggers:
  ''write TDD'', ''technical design'', ''design document'', ''architecture spec'',
  ''Unity system design'', ''API documentation''.'
name: unity-write-tdd
---

# Unity TDD Writer

**Input**: Feature or system to document. Optional: file paths, constraints, existing plan.

## Output
Technical Design Document (TDD) in markdown covering architecture, data schemas, and implementation strategy.

## Workflow

1. **Find Plan**: `Documents/Plans/IMPLEMENTATION_PLAN_[FeatureName].md` (run `/unity-plan` if missing)
2. **Define Architecture**: Constraints (FPS, Memory, CPU), map Epics to TDD Components
3. **Detail Logic**: UI lifecycles, asset loading (Addressables, pooling), client-server interactions
4. **Generate**: Use template, address all sections
5. **Validate**: Verify Architecture, Components, API, Analytics, Performance covered

## Required Sections

- **Architecture**: Assumptions, constraints, dependencies
- **Components**: Feature modules mapped from plan
- **API Reference**: Endpoints, request/response formats
- **Data Schema**: Blueprint/FlatBuffer changes
- **Performance**: Mobile/low-end considerations
- **Analytics**: Events to track

## Best Practices

- **Explicit Assumptions**: Never leave constraints undocumented
- **Performance First**: Address mobile/low-end risks
- **UI Lifecycle**: When data populates and refreshes
- **Error Handling**: API failures, offline behavior
