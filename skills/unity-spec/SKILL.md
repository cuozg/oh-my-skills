---
name: unity-spec
description: >
  Generate detailed Game Design Specification (GDD) documents for Unity game projects.
  Covers game overview, core mechanics, systems design, progression, content, UX/UI flows,
  art direction, audio, technical constraints, platform targets, and risks. Investigates
  the existing codebase to align the spec with current architecture. Use when the user says
  "write a game spec," "create a GDD," "game design document," "spec out this game,"
  "feature specification," or describes a game concept needing a structured specification.
  Do not use for technical design docs (unity-document TDD mode) or planning (unity-plan).
metadata:
  author: kuozg
  version: "1.0"
---

# unity-spec

Generate codebase-aware Game Design Specifications. Auto-triage into Full GDD or Feature Spec.

## Triage

Classify the request before starting:

| Signal | Behavior |
|--------|----------|
| User describes a new game concept | **Full GDD** — all 12 sections |
| User describes a feature for an existing game | **Feature Spec** — relevant sections only |
| User provides partial spec, wants completion | **Fill** — complete remaining sections |

When ambiguous, ask: "Is this a full game spec or a feature-scoped spec?"

---

## Workflow

Every spec session follows 5 steps. Step 4 is BLOCKING — do not proceed without user approval.

### Step 1: Investigate

If a Unity project exists, scan the codebase (max 5 tool calls) to understand existing architecture, naming conventions, and systems. Note what already exists vs what is new.

### Step 2: Present Template

Load the GDD template: `read_skill_file("unity-spec", "references/gdd-template.md")`. Present ALL section headers with brief descriptions. Ask the user to fill what they know — the skill completes the rest.

### Step 3: Draft Spec

Fill every section of the template. For sections the user did not provide:
- Use codebase evidence if available, citing `file:line`
- Make reasonable design decisions and mark with `[ASSUMED]`
- Include mandatory Mermaid diagrams: architecture flowchart, at least 1 state diagram, data model class diagram (minimum 3 total for Full GDD, 1 for Feature Spec)

### Step 4: Review ⛔ BLOCK

**STOP. Present the completed spec to the user. Wait for user to approve, request changes, or discard.** Do NOT save until user approves.

### Step 5: Save & Validate

Save to `Documents/Specs/SPEC_{Name}.md`. Run validation:
`run_skill_script("unity-spec", "scripts/validate_spec.py", arguments=[<path>])`

---

## Shared Rules

- Investigate actual codebase before writing — no speculation about existing systems
- Every reference to existing code must cite `file:line`
- Mark assumptions with `[ASSUMED]` tag so user can verify
- No TODO/TBD/FIXME in the output document
- Use imperative language; avoid "we should" or "you could"
- Full GDD requires at least 3 Mermaid diagrams; Feature Spec requires at least 1
- No C# code stubs — architecture-level descriptions only

## Standards

Load `unity-standards` for architecture context. Key references:

- `code-standards/architecture-systems.md` — architecture patterns, dependencies, events, project structure

Load via `read_skill_file("unity-standards", "references/<path>")`.
