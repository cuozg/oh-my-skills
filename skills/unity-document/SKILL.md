---
name: unity-document
description: >
  Unity documentation skill for investigating a feature in a Unity codebase and writing an
  evidence-based system document to Docs/Systems/<feature-name>.md.
metadata:
  author: kuozg
  version: "3.0"
---

# unity-document

Create a Unity system document grounded in the real codebase, then verify the result.

## When to Use

Use this skill when the user wants a document for a Unity project feature, subsystem, flow,
manager, integration, or gameplay system.

## Workflow

### 1. **Understand the requirement**
   - Identify the feature name, scope, audience, and expected output file name.
   - Clarify only if the request is ambiguous enough that a reasonable file name or scope cannot
     be inferred.
### 2. **Investigate the codebase**
   - Spawn at least one `explorer` subagent to inspect the relevant code paths, assets, scenes,
     tests, and config.
   - Spawn a second `explorer` when a separate pass is useful for dependencies, events, or setup
     paths.
   - Use the subagent findings as evidence, not as a substitute for reading the source.
### 3. **Build the document**
   - Write the document in this exact section order:
     1. `Overview`
     2. `System Architecture`
     3. `Core Components`
     4. `Lifecycle & Initialization`
     5. `Data Models`
     6. `How to Setup an Event`
     7. `How to Fake Data for Testing`
     8. `Validation`
     9. `Debugging`
     10. `API Reference`
   - Put the file at `Docs/Systems/<feature-name>.md`.
   - Use concise, evidence-backed prose. Cite claims with `file:line` references from the codebase.
   - Include Mermaid diagrams where they clarify the architecture or event flow.
### 4. **Verify the document**
   - Confirm the target path is correct.
   - Confirm every required section exists and is in the correct order.
   - Confirm the document has no placeholder text such as `TODO`, `TBD`, or `FIXME`.
   - Confirm the document includes source citations and any required Mermaid diagrams.
   - Run the bundled validator when available.

## Writing Rules

- Investigate the actual codebase before writing. Do not speculate.
- Prefer the concrete runtime path over abstract design language.
- Document real setup steps, not idealized ones.
- If a capability is not present in the codebase, state that clearly.
- Keep the document focused on one Unity feature or system.

## Minimum Content Expectations

- `Overview`: what the system does and why it exists.
- `System Architecture`: major runtime pieces and how they connect.
- `Core Components`: the key classes, ScriptableObjects, scenes, prefabs, or services.
- `Lifecycle & Initialization`: startup order, bootstrap, registration, and teardown.
- `Data Models`: runtime data, serialized data, event payloads, and config.
- `How to Setup an Event`: the concrete wiring required to emit and receive the event.
- `How to Fake Data for Testing`: test doubles, mock data, editor setup, or harnesses.
- `Validation`: how to confirm the feature works.
- `Debugging`: likely failure points and where to inspect them.
- `API Reference`: public methods, events, properties, and entry points.