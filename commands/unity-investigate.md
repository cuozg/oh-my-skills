---
description: Deep investigation of Unity projects — logic, data, assets, animation, VFX, audio, physics, UI, networking, performance, and all technical systems.
---

# Workflow: Unity Investigation

Use this workflow to investigate any Unity system, trace execution flows, or analyze technical implementations.

1.  **Define Scope**: 
    - Identify the target class, system, or feature.
    - Determine investigation type (logic, data, resources, animation, VFX, audio, physics, UI, networking, performance).
    - Ask the user for specific entry points if the scope is broad.
2.  **Discovery**:
    // turbo
    - Run `.claude/skills/unity-investigate/scripts/trace_logic.sh [Target]` to map definitions and usages.
    - Use LSP tools (`lsp_find_references`, `lsp_goto_definition`) to trace the call graph.
    - Use `grep` and `glob` to find related assets, prefabs, and configurations.
3.  **Analyze**:
    - Follow the logic from entry points through dependencies.
    - Document state changes, conditional branches, and side effects.
    - Apply system-specific analysis per the investigation type.
4.  **Generate Report**:
    - Use the `INVESTIGATION_REPORT.md` template from `.claude/skills/unity-investigate/assets/templates/`.
    - Save the final document in `Documents/Investigations/INVESTIGATION_[Subject]_[YYYYMMDD].md`.
    - Include **Mermaid diagrams** for complex flows, state machines, and architecture.
5.  **Summary**:
    - Provide a high-level summary to the user, highlighting risks, technical debt, and improvement opportunities.
