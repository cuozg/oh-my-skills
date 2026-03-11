---
name: unity-document-system
description: >
  Use this skill to write system documentation for a Unity system — architecture diagrams, data flows,
  public API references, and extension guides. Use when the user says "document this system," "write docs
  for X," "I need architecture documentation," or wants a comprehensive technical reference for a codebase
  module. Produces a structured markdown document with Mermaid diagrams and cited evidence. Do not use for
  design decisions before implementation — use unity-document-tdd for that.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-document-system

**CRITICAL MANDATE: Output ALWAYS uses the exact template structure below. No exceptions.**

## Workflow

1. **Identify**: Locate the core entry points, data models, and managers for the target system.
2. **Trace**: Follow the data flow from input to output, noting all dependencies and events.
3. **Map**: Identify the architectural pattern (e.g., Event Bus, Singleton, ECS).
4. **Diagram**: Formulate Mermaid sequence and architecture diagrams based on code relationships.
5. **Write** → **MUST follow template structure exactly** (see below). Do not rename, reorder, or skip sections.
6. **Validate** → Check all sections are present, all claims cited, and metadata filled out.

## Template Rules

The final output must precisely match the structure of `references/system-doc-template.md`. 

### MANDATORY OUTPUT STRUCTURE

You must include these exact sections in order:

- [ ] **Metadata**: Owner, Last Updated, Next Review Due (max 90 days out), Status.
- [ ] **1. Overview**: 1-2 sentences of purpose and a clear scope definition.
- [ ] **2. Architecture**: Mermaid diagram (Class/Component/Data Flow) + min 3 components shown.
- [ ] **3. Public API**: Table of methods, properties, and events with `(file:line)` citations.
- [ ] **4. Decision Drivers**: Table of architectural rationale with `(file:line)` evidence.
- [ ] **5. Data Flow**: Mermaid sequence diagram representing execution flow.
- [ ] **6. Extension Guide**: Bulleted list on how to override/extend with `(file:line)` citations.
- [ ] **7. Dependencies**: Table of external dependencies and versions with `(file:line)` evidence.
- [ ] **8. Known Limitations**: Table of limitations, workarounds, and issue IDs.
- [ ] **Validation Checklist**: Unmodified checklist at the end.

### Citation Enforcement

**EVERY** technical claim, API reference, architectural choice, and dependency statement **MUST** be cited inline using the format `(filename.ext:line)`. 

### Reference Resources
- Template: `references/system-doc-template.md`
- Validation Script: `scripts/validate_system_doc.py <path-to-doc.md>`

> *Note: Before submitting the final documentation, you must verify it would pass the validation script.*