---
name: unity-investigate-code
description: "Analyze C# logic and trace execution flows. Use when: (1) Understanding how a feature works, (2) Tracing execution from trigger to outcome, (3) Extracting business rules, (4) Identifying dependencies and side effects. Triggers: 'how does X work', 'trace the flow', 'explain this code', 'what calls this'."
---

# Unity Code Investigator

Analyze and explain C# logic, execution flows, and feature implementations.

## Output Requirement (MANDATORY)

**Every investigation report MUST follow the template**: [INVESTIGATION_REPORT.md](assets/templates/INVESTIGATION_REPORT.md)

Save output to: `Documents/Investigations/INVESTIGATION_[FeatureName]_[YYYYMMDD].md`

Read the template first, then populate all sections.

## Investigation Workflow

1. **Define Scope**: Target class/method/feature, ask for entry points if complex
2. **Discover**: Run `.claude/skills/unity-investigate-code/scripts/trace_logic.sh [Target]`
3. **Trace Flow**: Follow from entry (Update, OnClick, OnTrigger) through call stack
4. **Analyze Side Effects**: Singletons, static managers, events, network calls
5. **Generate Report**: Use `INVESTIGATION_REPORT.md` template, save to `Documents/Investigations/`
6. **Visualize**: Use `mermaid` skill for sequence diagrams of complex flows

## Key Analysis Points

- **Entry Points**: `Update`, `Start`, `OnEnable`, event handlers, UI callbacks
- **State Changes**: Conditionals, async sequences, data mutations
- **Side Effects**: Singleton access, static state, event dispatch
- **Dependencies**: External systems, third-party plugins, engine APIs

## Best Practices

- **Breadth-First**: High-level file overview before deep-dive
- **Unity Context**: Factor in Physics, Input, UI system interactions
- **Explain "Why"**: Recover original engineering intent
- **Highlight Risks**: Technical debt, threading issues, optimization opportunities
