---
name: unity-document-system
description: "Documentation-only deep investigation skill. Produces comprehensive system documents covering architecture, data flows, usage, and extension guides. Use when: (1) Documenting a Unity system's architecture and data flow, (2) Creating onboarding docs for a complex system, (3) Generating extension/implementation guides for a system, (4) Producing integration and dependency maps. Triggers: 'document system', 'explain system', 'system overview', 'system document', 'architecture document'."
---

# Unity System Documenter

Read-only. Investigate and document — never modify project code.

**Input**: System/feature/class to document + optional scope boundaries.
**Output**: System document saved to `Documents/Systems/{SystemName}.md`.

Load [workflow.md](references/workflow.md) for step-by-step workflow and tool selection.

## Rules

- Every claim backed by code evidence (`File.cs:L##`)
- Mermaid diagrams mandatory for init flow + execution flow + system context
- Fill every template section; use "N/A — {reason}" only when truly not applicable
- Explain **why + how**, not just what exists
- Extension guides must be step-by-step and copy-paste ready
- Bullet points over prose walls
