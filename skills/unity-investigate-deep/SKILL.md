---
name: unity-investigate-deep
description: "Deep investigation of Unity projects with full report output. Produces comprehensive markdown investigation documents with architecture diagrams, execution flows, risk tables, and improvement recommendations. Use when: (1) Need a thorough written report of how a system works, (2) Documenting complex system behavior for team review, (3) Deep-diving into architecture with Mermaid diagrams, (4) Producing investigation artifacts for future reference, (5) Tracing complete execution flows with side effects, (6) Auditing system health with risk assessment. Triggers: 'deep investigate', 'investigation report', 'document how X works', 'full analysis', 'write investigation', 'deep dive report', 'system analysis report', 'trace and document'."
---

# Unity Deep Investigator

**Input**: Question or system to investigate + optional starting file/class

## Output

Comprehensive investigation report (markdown) with architecture diagrams, execution flows, and risk tables. Save to `Documents/Investigations/`.

## Workflow

Follow the 5-step workflow: Scope → Discover → Analyze → Report → Summary.

## Shared References

Load shared investigation resources from `unity-shared`:

```python
read_skill_file("unity-shared", "references/investigation-analysis-rules.md")
```

## Reference Files
- [output-template.md](references/output-template.md) — Investigation report template
- workflow.md — 5-step investigation workflow
