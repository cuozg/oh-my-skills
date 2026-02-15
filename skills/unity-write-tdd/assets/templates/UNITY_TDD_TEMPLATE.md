# [Feature Name] - Technical Design Document

## Review Status

| Reviewer | Approved | Last Reviewed | Re-review Ready |
|:---:|:---|:---:|---|
| | | Date | |

## Important Links

| Design 1-pager: | [Link] |
|:---|:---|
| Design brief/spec: | [Link] |
| Miro: | [Link] |
| Task Breakdown: | [Link to Documents/Plans] |

## Feature Summary

[Brief summary]

- **Existing Tech As-is**: [Description]
- **Existing Tech Changed**: [Description]
- **New Tech**: [Description]
- **External Integrations**: [List + documentation]
- **Time-Offset Compatibility**: [Compatible / Risks]

## Key Architectural Decisions

**Assumptions**: [Constraints and assumptions]

**Performance Risks**: Data storage, stress testing, backward compatibility, API overload, memory/FPS/CPU

## Feature Components

### [Component Name]

**Client**: Data population, refresh logic, static vs dynamic UI, asset loading, prefab details, client-server interactions, error/offline handling, kill-switch behavior

**Server**: Configuration, player progress data, storage/editability, API payload details

### WebGL Considerations
[Risks to WebGL performance]

### Launch & Monitoring
[Readiness and dashboards]

### Analytics
[Data hooks and verification]

### API Reference

**New APIs**: [Endpoint]: [Description]
**Modified APIs**: [Endpoint]: [Modification]

```json
// Request/Response example
```

### Data Architecture
- [Update/New] [blueprint_name.json]: [Description]
