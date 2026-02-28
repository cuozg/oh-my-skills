## Workflow

1. **Scope**: Parse request, identify feature boundary, define success criteria.
2. **Investigate**:
   - Map architecture: `../../unity-shared/scripts/investigate/trace_unified.py architecture`, `glob`, `read`.
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

## Investigation Checklist

- [ ] Interfaces/contracts & Abstract base classes
- [ ] ScriptableObject data pipelines & configuration
- [ ] MonoBehaviour lifecycle & orchestration
- [ ] Event flow (C# events, UnityEvent, MessageBus)
- [ ] External dependencies (Packages, Services)
