---
name: unity-uitoolkit-create
description: >
  Use this skill to build runtime UI with Unity UI Toolkit — UXML templates, USS styling, C# controller
  bindings, and custom controls. Accepts design docs, images, or verbal descriptions as input and asks
  clarifying questions for ambiguous requirements. Use when the user says "create a UI screen," "build a
  menu," "make a HUD," "UI from this mockup," or any request involving UXML, USS, or runtime UI panels.
  Do not use for editor-only UI — use unity-code-editor for that.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-uitoolkit-create

Build production runtime UI using UI Toolkit. Parse design input (document, image, description) → clarify unknowns → create UXML + USS + C# controller.

## When to Use

- Creating new UI screens, panels, modals, HUDs, or menus
- Translating a design mockup or wireframe into UXML/USS/C#
- Building reusable UI components with custom VisualElements
- Setting up UIDocument + PanelSettings for runtime UI
- Any runtime UI work using UI Toolkit (not uGUI, not Editor UI)

## Workflow

1. **Parse Input** — Identify UI elements, layout, interactions from design doc/image/description
2. **Clarify** — Ask user about unclear aspects: color palette, responsive behavior, data sources, navigation flow
3. **Discover** — Check existing project for UI conventions, shared USS variables, naming patterns (grep/glob, max 3 searches)
4. **Structure** — Plan file list: UXML templates, USS sheets, C# controllers. Define hierarchy and reusable components.
5. **Implement** — Write files in order: USS variables/theme → UXML templates → C# controllers
6. **Wire** — Set up UIDocument, PanelSettings, event bindings, data sources

## Rules

- Always create separate files: `.uxml` for structure, `.uss` for styling, `.cs` for logic. No inline styles.
- Use BEM naming for USS classes: `block`, `block__element`, `block--modifier`.
- Name UXML elements with `name="kebab-case"` for C# querying via `Q<T>("name")`.
- Cache all `Q<T>()` / `Query<T>()` results in fields — never query in Update/callbacks.
- Register callbacks in `OnEnable`, unregister in `OnDisable`. Always pair.
- Capture specific elements in closures, never capture `this`.
- Use `visibility: hidden` to hide elements (cheapest). Avoid `display: none` for frequently toggled UI.
- Use USS custom properties (`:root { --var: value; }`) for colors, spacing, fonts — enable theming.
- Set `ScaleWithScreenSize` on PanelSettings for responsive UI (reference: 1920×1080).
- One C# controller per UIDocument. Controller manages its own root element tree.
- For all C# coding standards — follow `unity-standards`.

## Handling Design Input

- **Image/mockup**: Describe observed layout, colors, typography. Ask user to confirm before implementing.
- **Document/spec**: Extract element hierarchy, interactions, states. Flag missing details.
- **Verbal request**: Map to concrete elements. Propose structure, ask for approval on ambiguous parts.
- Always ask about: responsive behavior, animation/transitions, data binding needs, navigation between screens.

## Output Format

Write all files directly. Report: file list with paths, element hierarchy, and compilation status.

## Reference Files

All UI Toolkit references live in `unity-standards`. Load on demand:

- `ui-toolkit/setup.md` — UIDocument, PanelSettings, scale modes, multi-panel, file org
- `ui-toolkit/performance.md` — pooling, visibility cost, selectors, UsageHints, profiler markers
- `ui-toolkit/uxml-patterns.md` — UXML structure, templates, BEM naming, reusable snippets
- `ui-toolkit/uss-styling.md` — USS selectors, variables, responsive patterns, theming
- `ui-toolkit/csharp-bindings.md` — UQuery, event callbacks, data binding, focus management
- `ui-toolkit/custom-controls.md` — UxmlElement, UxmlAttribute, custom VisualElement creation

Load via `read_skill_file("unity-standards", "references/ui-toolkit/<file>")`.
