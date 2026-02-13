# Unity UI Toolkit Mastery Series

A comprehensive 9-skill learning path for building production-quality UI with Unity's UI Toolkit (Unity 6+).

> **Based on**: Unity 6 (6000.0), Dragon Crashers official sample, and production mobile game patterns.
> **Enhanced with**: Project-specific code examples, 16 architecture patterns, mobile optimization checklists, and common bug fixes from the Dragon Crashers UIToolkit demo.

## Prerequisites

- Unity 6.0+ (LTS recommended)
- `com.unity.ui` package (included by default)
- Basic C# proficiency
- Familiarity with Unity Editor

## Decision Tree — Which Skill Do I Need?

Use this to jump directly to the right skill for your task:

```
What are you trying to do?
│
├── Setting up a new UI project?
│   └── Start with: ui-toolkit-master → ui-toolkit-architecture
│
├── Building a screen or view?
│   ├── Simple screen → ui-toolkit-patterns (tabs, modals, lists)
│   ├── Complex layout → ui-toolkit-responsive (flexbox, safe area)
│   └── Data-driven → ui-toolkit-databinding (event bus, controllers)
│
├── Styling or theming?
│   ├── Design tokens / colors → ui-toolkit-theming
│   ├── Dark/light or seasonal themes → ui-toolkit-theming (compound themes)
│   └── Responsive styles → ui-toolkit-responsive + ui-toolkit-theming
│
├── Targeting mobile?
│   ├── Touch input / gestures → ui-toolkit-mobile
│   ├── Safe area / orientation → ui-toolkit-mobile + ui-toolkit-responsive
│   └── Performance budgets → ui-toolkit-performance + ui-toolkit-mobile
│
├── Optimizing performance?
│   └── ui-toolkit-performance (profiling, draw calls, virtualization)
│
├── Debugging a UI issue?
│   ├── Visual issues → ui-toolkit-debugging (UI Debugger, style cascade)
│   ├── Event issues → ui-toolkit-debugging (event bus, async debugging)
│   └── Performance issues → ui-toolkit-performance + ui-toolkit-debugging
│
└── Need a quick reference?
    ├── Code templates → references/code-templates.md
    ├── Architecture patterns → references/project-patterns.md
    ├── Mobile checklist → references/mobile-optimization-checklist.md
    └── Common bugs → references/common-bugs-and-fixes.md
```

## Learning Path (~15 hours)

Progress through three levels — each builds on the previous.

### Level 1 — Foundations (~4.5 hrs)

Start here. Learn the mental model, component architecture, and layout system.

| # | Skill | What You'll Learn | Est. Time |
|---|-------|-------------------|-----------|
| 1 | [Master](ui-toolkit-master/SKILL.md) | UXML/USS/C# triad, UIDocument, PanelSettings, project setup | 1 hr |
| 2 | [Architecture](ui-toolkit-architecture/SKILL.md) | Custom controls, MVC pattern, event bus, template composition | 2 hrs |
| 3 | [Responsive](ui-toolkit-responsive/SKILL.md) | Flexbox layout, length units, safe area, orientation handling | 1.5 hrs |

### Level 2 — Core Skills (~5.5 hrs)

Design tokens, data flow, and common UI patterns used in production.

| # | Skill | What You'll Learn | Est. Time |
|---|-------|-------------------|-----------|
| 4 | [Theming](ui-toolkit-theming/SKILL.md) | TSS/USS cascade, design tokens, compound theme switching | 1.5 hrs |
| 5 | [Data Binding](ui-toolkit-databinding/SKILL.md) | Event-driven binding, controller→view flow, manual sync patterns | 2 hrs |
| 6 | [Patterns](ui-toolkit-patterns/SKILL.md) | Tabs, inventory grid, modals, async animation, scroll snap | 2 hrs |

### Level 3 — Production (~5 hrs)

Optimization, platform-specific concerns, and troubleshooting.

| # | Skill | What You'll Learn | Est. Time |
|---|-------|-------------------|-----------|
| 7 | [Performance](ui-toolkit-performance/SKILL.md) | Profiling, draw calls, `UsageHints`, virtualization, GC-free patterns | 1.5 hrs |
| 8 | [Mobile](ui-toolkit-mobile/SKILL.md) | Touch input, safe area (borderWidth), world-to-UI, frame rate control | 2 hrs |
| 9 | [Debugging](ui-toolkit-debugging/SKILL.md) | UI Debugger, event bus debugging, async task diagnostics | 1.5 hrs |

### Visual Navigation

```
Level 1                    Level 2                    Level 3
┌─────────────┐           ┌─────────────┐           ┌─────────────┐
│ 1. Master   │──────────▶│ 4. Theming  │──────────▶│ 7. Perform. │
└──────┬──────┘           ├─────────────┤           ├─────────────┤
       │                  │ 5. Binding  │           │ 8. Mobile   │
┌──────▼──────┐           ├─────────────┤           ├─────────────┤
│ 2. Arch.    │──────────▶│ 6. Patterns │──────────▶│ 9. Debug    │
└──────┬──────┘           └─────────────┘           └─────────────┘
       │
┌──────▼──────┐
│ 3. Respons. │
└─────────────┘
```

## Reference Documents

These reference files are shared across all 9 skills:

### Core References

| Reference | Description |
|-----------|-------------|
| [Dragon Crashers Insights](references/dragon-crashers-insights.md) | Patterns extracted from Unity's official UI Toolkit demo project |
| [Official Docs Links](references/official-docs-links.md) | Curated Unity 6 documentation links organized by topic |
| [Code Templates](references/code-templates.md) | 8 production-ready templates (screens, controls, ListView, binding, theming) |
| [Performance Benchmarks](references/performance-benchmarks.md) | Draw call targets, layout vs transform costs, memory profiles |

### Project-Specific References (New)

| Reference | Description |
|-----------|-------------|
| [Project Patterns](references/project-patterns.md) | 16 architecture patterns discovered in Dragon Crashers with code examples and selection guide |
| [Mobile Optimization Checklist](references/mobile-optimization-checklist.md) | Actionable mobile checklist with `[DC]` markers for Dragon Crashers-specific patterns |
| [Common Bugs & Fixes](references/common-bugs-and-fixes.md) | 12 common UI Toolkit bugs with causes, fixes, and diagnostic flowchart |

## Quick Start

Load any skill by name:

```
Load skill: unity/ui-toolkit/ui-toolkit-master
```

Combine skills for complex tasks:

```
Load skills: unity/ui-toolkit/ui-toolkit-architecture, unity/ui-toolkit/ui-toolkit-performance
```

### Quick-Start Workflow

1. **New project?** → Load `ui-toolkit-master`, follow the project setup section
2. **Adding a screen?** → Load `ui-toolkit-architecture` + `ui-toolkit-patterns`
3. **Styling?** → Load `ui-toolkit-theming`, check compound theme section
4. **Going mobile?** → Load `ui-toolkit-mobile` + `ui-toolkit-responsive`
5. **Something broken?** → Load `ui-toolkit-debugging`, check project-specific scenarios
6. **Need a template?** → Check `references/code-templates.md` first

### Recommended Combinations

| Task | Skills to Load |
|------|---------------|
| New UI project setup | `ui-toolkit-master` + `ui-toolkit-architecture` |
| Building a complex screen | `ui-toolkit-patterns` + `ui-toolkit-responsive` |
| Adding dark/light theme | `ui-toolkit-theming` + `ui-toolkit-architecture` |
| Connecting data models | `ui-toolkit-databinding` + `ui-toolkit-patterns` |
| Mobile game UI | `ui-toolkit-mobile` + `ui-toolkit-responsive` + `ui-toolkit-performance` |
| Fixing UI issues | `ui-toolkit-debugging` + `ui-toolkit-performance` |
| World-to-UI (3D + UI) | `ui-toolkit-mobile` + `ui-toolkit-patterns` |
| Seasonal/event themes | `ui-toolkit-theming` (compound themes section) |

## What Each Skill Includes

Every enhanced skill in this series provides:

- **Dragon Crashers examples** — real code patterns from Unity's official sample
- **Project-specific patterns** — code extracted from the actual DC codebase
- **Practical exercise** — hands-on mini-project with checklist
- **Common pitfalls** — table of mistakes and solutions
- **Cross-references** — links to related skills for deeper coverage
- **Official documentation** — curated Unity 6 doc links
- **Navigation footer** — prev/next/up links for series flow

## Key Project Patterns (Summary)

The Dragon Crashers project uses these patterns extensively across all skills:

| Pattern | Used In | Key Skill |
|---------|---------|-----------|
| Static `Action` event bus | All controllers/views | Architecture, Debugging |
| MVC-like (Controller→View) | Screen management | Architecture, Data Binding |
| Two UIDocument architecture | Main + overlay screens | Architecture, Patterns |
| Compound themes (`"Landscape--Christmas"`) | ThemeManager | Theming |
| Async/await fire-and-forget (`_ = Task()`) | View animations | Patterns, Debugging |
| SafeAreaBorder (borderWidth) | Safe area handling | Mobile, Responsive |
| PositionToVisualElement | 3D health bars | Mobile, Patterns |
| MediaQuery orientation detection | Responsive layout | Responsive, Mobile |
| CSS class toggling | State management | Patterns, Theming |
| `experimental.animation` | Smooth transitions | Patterns, Performance |

## Series Structure

```
ui-toolkit/
├── README.md                                  # This file — overview, decision tree, quick start
├── references/                                # Shared reference materials (all skills)
│   ├── dragon-crashers-insights.md            #   DC patterns & code examples
│   ├── official-docs-links.md                 #   Unity 6 documentation links
│   ├── code-templates.md                      #   8 production-ready templates
│   ├── performance-benchmarks.md              #   Metrics, budgets, benchmarks
│   ├── project-patterns.md                    #   16 architecture patterns (NEW)
│   ├── mobile-optimization-checklist.md       #   Mobile checklist with [DC] markers (NEW)
│   └── common-bugs-and-fixes.md               #   12 common bugs & diagnostic flowchart (NEW)
├── scripts/                                   # Shared utility scripts
├── ui-toolkit-master/SKILL.md                 # 1. Foundations & mental model
├── ui-toolkit-architecture/SKILL.md           # 2. Component design & composition
├── ui-toolkit-responsive/SKILL.md             # 3. Adaptive layouts & flexbox
├── ui-toolkit-theming/SKILL.md                # 4. Design tokens & style architecture
├── ui-toolkit-databinding/SKILL.md            # 5. Event-driven data flow
├── ui-toolkit-patterns/SKILL.md               # 6. Common UI implementations
├── ui-toolkit-performance/SKILL.md            # 7. Optimization techniques
├── ui-toolkit-mobile/SKILL.md                 # 8. Touch & platform optimization
└── ui-toolkit-debugging/SKILL.md              # 9. Troubleshooting & diagnostics
```