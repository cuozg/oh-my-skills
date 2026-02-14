# Unity Skills Index

**Last Updated**: February 2026  
**Total Skills**: 39

## Quick Navigation

- [🎯 Start Here](#-start-here) - Entry point for all Unity tasks
- [💻 Code & Implementation](#-code--implementation) - Writing and generating Unity C# code
- [🐛 Debugging & Fixing](#-debugging--fixing) - Error diagnosis and resolution
- [📋 Planning & Design](#-planning--design) - Feature planning and architecture
- [🎨 UI & UX](#-ui--ux) - UI Toolkit development (11 skills)
- [⚡ Performance & Optimization](#-performance--optimization)
- [🧪 Testing & Quality](#-testing--quality)
- [🔍 Analysis & Investigation](#-analysis--investigation)
- [📦 Deployment & Build](#-deployment--build)
- [🎮 2D Development](#-2d-development) - Sprites, tilemaps, 2D physics
- [📚 Documentation](#-documentation)
- [🔧 Editor Tools](#-editor-tools)

---

## 🎯 Start Here

### unity-orchestrator
**Master Unity technical lead** - Routes all Unity requests to specialized skills.

- **Use First**: For ANY Unity task or when unsure which skill to use
- **Triggers**: Any Unity request, "which skill?", "help with Unity"
- **Routes To**: All skills below based on intent analysis

---

## 💻 Code & Implementation

### unity-code
Expert Unity Developer implementing clean, performant C# code.

- **Use When**: Creating MonoBehaviours, ScriptableObjects, gameplay features
- **Best For**: New implementations following Unity 6 patterns
- **Avoids**: Anti-patterns caught by unity-review-pr

### unity-plan-executor
Execute implementation plans from HTML files with 100% accuracy.

- **Use When**: Applying exact code changes from Documents/Plans/*.html
- **Best For**: Scripted implementations with no interpretation
- **Input**: HTML plan with split diff views

### unity-refactor
Orchestrate safe code transformations for Unity C# codebases.

- **Use When**: Extracting methods, reducing coupling, replacing anti-patterns
- **Best For**: Systematic refactoring with verification
- **Safety**: Includes investigation + verification phases

### unity-serialization
Data persistence and serialization patterns.

- **Use When**: Building save/load systems, JSON/binary serialization
- **Covers**: JsonUtility, Newtonsoft.Json, ScriptableObject containers, PlayerPrefs
- **Best For**: Save systems, data migration, cross-platform persistence

### unity-event-system
Event-driven architecture and decoupling patterns.

- **Use When**: Implementing observer pattern, event channels, message buses
- **Covers**: C# events/delegates, UnityEvent, ScriptableObject event channels, generic event bus
- **Best For**: Decoupling systems, reducing dependencies between components

---

## 🐛 Debugging & Fixing

### unity-fix-errors
Diagnose and fix Unity compiler errors, runtime exceptions, and broken Play Mode.

- **Use When**: Console shows errors, build fails, game crashes
- **Output**: DEBUG_*.md report in Documents/Debugs/
- **Safety**: Includes rollback strategy and verification steps

### unity-debug
Deep investigation and root cause analysis of Unity errors.

- **Use When**: Need to understand WHY error occurs (not just fix it)
- **Output**: Detailed stack trace analysis and debug report
- **Complements**: unity-fix-errors (diagnose → fix workflow)

### unity-log-analyzer
Parse and analyze Unity console logs to classify errors and suggest fixes.

- **Use When**: Triaging many errors, identifying recurring patterns
- **Output**: Error summary with prioritization
- **Best For**: Post-playtest error analysis

---

## 📋 Planning & Design

### unity-plan
High-level planning with multi-file output and patch generation.

- **Use When**: Breaking features into epics/tasks, estimating effort
- **Output**: HTML files (overview, tasks, timeline) + unified diff patch
- **Next Step**: unity-plan-detail for per-task code

### unity-plan-detail
Generate 100% complete code changes for each task in a plan.

- **Input**: Plan HTML from unity-plan
- **Output**: Executable task specs in Documents/Tasks/
- **Next Step**: unity-plan-executor applies the changes

### unity-write-tdd
Generate Technical Design Documents for Unity projects.

- **Use When**: Formalizing architecture, documenting game systems
- **Output**: TDD following UNITY_TDD_TEMPLATE.md
- **Best For**: API specs, multiplayer design, system architecture

### unity-game-designer
Game design documentation and brainstorming.

- **Use When**: Conceptualizing features, writing GDDs, designing core loops
- **Output**: Game Design Documents with mechanics/progression/economy
- **Best For**: Feature specs before implementation

---

## 🎨 UI & UX

### ui-toolkit-master
Master guide for Unity UI Toolkit (Unity 6+).

- **Start Here**: For all UI Toolkit questions
- **Covers**: UXML/USS/C# triad, architecture, project structure
- **Links To**: All 8 specialized UI Toolkit skills below

### ui-toolkit-architecture
Component-based architecture with custom controls and MVC patterns.

- **Use When**: Designing UI hierarchies, creating reusable components
- **Covers**: [UxmlElement], templates, MVC/MVP patterns
- **Best For**: Inventory systems, character screens, menu architectures

### ui-toolkit-databinding
Unity 6 runtime data binding (IDataSource, [CreateProperty]).

- **Use When**: Binding data models to UI without manual callbacks
- **Covers**: INotifyBindablePropertyChanged, PropertyPath, type converters
- **Best For**: Reactive UI updates

### ui-toolkit-debugging
Debugging and troubleshooting UI Toolkit.

- **Use When**: Element not visible, events not firing, USS not applying
- **Tools**: UI Toolkit Debugger, Event Debugger, Memory Profiler
- **Best For**: Diagnosing layout/style/binding issues

### ui-toolkit-mobile
Mobile optimization and touch input.

- **Use When**: Building touch UI, handling safe areas, orientation changes
- **Covers**: Gesture detection, virtual keyboard, mobile performance
- **Best For**: Mobile game UI with proper hit targets

### ui-toolkit-patterns
Common UI patterns with UXML/USS/C# examples.

- **Use When**: Building tabs, inventory grids, modals, message lists
- **Includes**: Complete code for 6 common patterns
- **Best For**: Copy-paste starting points

### ui-toolkit-performance
Performance optimization for UI Toolkit.

- **Use When**: Low UI frame rate, high draw calls, layout thrashing
- **Covers**: Profiling, element pooling, ListView virtualization
- **Best For**: Optimizing complex UI with many elements

### ui-toolkit-responsive
Responsive design with flexbox and safe area handling.

- **Use When**: Adaptive UI across phone/tablet/desktop
- **Covers**: Flexbox layout, aspect ratios, breakpoints
- **Best For**: Multi-device support

### ui-toolkit-theming
Theme Style Sheets (TSS) and design tokens.

- **Use When**: Building dark/light themes, creating design systems
- **Covers**: TSS/USS cascade, semantic tokens, runtime theme switching
- **Best For**: Scalable theme architecture

### unity-ux-design
UX screen specifications and mobile game UI design.

- **Use When**: Creating UX specs, wireframing mobile game screens, defining interaction patterns
- **Covers**: Screen specifications, navigation flows, touch targets, responsive behavior
- **Best For**: Generating spec documents that feed into unity-ui for implementation

### unity-ui
Implement UX designs from HTML documents into Unity UI prefabs.

- **Use When**: Translating HTML/CSS design docs into Unity prefab hierarchies
- **Covers**: Design-to-prefab mapping, layout systems, multi-screen UI
- **Best For**: Pixel-perfect fidelity between design spec and Unity implementation

---

## ⚡ Performance & Optimization

### unity-optimize-performance
Fix low FPS, memory leaks, and slow load times.

- **Use When**: Performance issues affecting gameplay
- **Audits**: Scripts, assets, draw calls, memory allocation
- **Output**: Performance report with prioritized fixes

### unity-singleton-auditor
Audit Singleton usage for circular dependencies and initialization risks.

- **Use When**: Large projects with many Singletons (50+ classes)
- **Detects**: Circular deps, unsafe access, initialization order issues
- **Output**: Dependency graph and recommendations

### unity-object-pooling
Generic and specialized object pooling for Unity.

- **Use When**: Reducing GC pressure, pooling frequently spawned objects
- **Covers**: Generic pools, particle pools, UI pools, UnityEngine.Pool API
- **Best For**: Bullet/VFX/enemy spawning, UI element recycling

---

## 🧪 Testing & Quality

### unity-test
Unity Test Framework automation (Edit/Play Mode tests).

- **Use When**: Writing tests, generating test suites, mocking dependencies
- **Output**: NUnit tests with maximum coverage
- **Best For**: TDD workflows, regression prevention

### unity-test-case
Generate comprehensive test case documents (QA perspective).

- **Use When**: Creating test plans for game features
- **Output**: HTML test case documents
- **Best For**: Manual QA planning

### unity-review-pr
Expert code reviewer for Unity PRs.

- **Use When**: Reviewing PRs, commits, branches, uncommitted changes
- **Accepts**: GitHub PR links, commit hashes, branch names
- **Focus**: Unity patterns, performance, best practices

### unity-review-pr-local
Local PR reviews without GitHub posting.

- **Use When**: Offline reviews, draft reviews before posting
- **Output**: Markdown review file
- **Best For**: Pre-commit validation

---

## 🔍 Analysis & Investigation

### unity-investigate
Deep investigation of Unity projects (logic, data, systems).

- **Use When**: Understanding how a feature works, tracing execution flow
- **Covers**: All Unity systems (animation, VFX, audio, physics, networking)
- **Output**: Flow diagrams and system explanations

---

## 📦 Deployment & Build

### unity-mobile-deploy
iOS/Android development and mobile optimization.

- **Use When**: Touch controls, mobile builds, native features (IAP, notifications)
- **Covers**: Battery/heat/memory optimization
- **Best For**: Mobile-specific workflows

### unity-web-deploy
WebGL deployment and browser optimization.

- **Use When**: WebGL builds, C#/JavaScript interop
- **Covers**: Browser memory limits, audio/input handling
- **Best For**: Web game deployment

### unity-build-pipeline
Build automation, Addressables, and CI/CD for Unity.

- **Use When**: Automating builds, configuring Addressables, setting up CI/CD
- **Covers**: BuildPipeline API, build callbacks, define symbols, build reports
- **Best For**: Automated build pipelines, multi-platform builds

---

## 🎮 2D Development

### unity-2d
2D game development — sprites, tilemaps, 2D physics.

- **Use When**: Building 2D games, working with sprites/tilemaps
- **Covers**: SpriteRenderer, Tilemap, Rigidbody2D, 2D animation, sprite atlas, 2D lighting
- **Best For**: 2D platformers, top-down games, pixel-art projects

---

## 📚 Documentation

### unity-write-docs
Create Unity project documentation.

- **Use When**: Creating README, API docs, onboarding guides
- **Output**: Markdown documentation
- **Best For**: Project setup guides, architecture docs

---

## 🔧 Editor Tools

### unity-editor-tools
Create Unity Editor tools (Windows, Inspectors, utilities).

- **Use When**: Building custom Editor workflows
- **Covers**: UI Toolkit editor interfaces, asset validation
- **Best For**: Engineer productivity tools

### unity-tech-art
Bridge art and code (shaders, tools, pipelines).

- **Use When**: Shader authoring, procedural generation, asset pipelines
- **Covers**: HLSL/Shader Graph, artist tools
- **Best For**: Technical artist workflows

---

## Skill Relationships

### Common Workflows

```
Feature Implementation:
unity-plan → unity-plan-detail → unity-plan-executor → unity-test → unity-review-pr

Error Resolution:
unity-debug → unity-fix-errors → unity-test

UI Development:
ui-toolkit-master → [specialized UI skill] → ui-toolkit-debugging → ui-toolkit-performance

Code Quality:
unity-investigate → unity-refactor → unity-review-pr-local → unity-test

Data Persistence:
unity-serialization → unity-build-pipeline (for asset bundles)

Event Architecture:
unity-event-system → unity-code → unity-refactor (event-driven decoupling)

2D Game Development:
unity-2d → unity-optimize-performance → unity-build-pipeline
```

### Complementary Pairs

| If You Use... | Consider Also... |
|--------------|------------------|
| unity-fix-errors | unity-debug (for root cause) |
| unity-plan | unity-plan-detail (for implementation) |
| unity-code | unity-test (for test coverage) |
| unity-code | unity-event-system (for decoupling) |
| unity-review-pr | unity-singleton-auditor (for Singleton health) |
| ui-toolkit-master | ui-toolkit-debugging (when stuck) |
| unity-optimize-performance | unity-singleton-auditor (for init order) |
| unity-optimize-performance | unity-object-pooling (for GC reduction) |
| unity-mobile-deploy | unity-build-pipeline (for build automation) |
| unity-serialization | unity-code (for data models) |
| unity-2d | unity-tech-art (for 2D shaders/effects) |

---

## Validation

All skills validated with `.opencode/skills/validate_skill.py`:

```bash
python3 .opencode/skills/validate_skill.py .opencode/skills/unity
```

**Status**: ✅ 39/39 skills structurally valid (Feb 2026)

---

## Contributing

When creating new Unity skills:

1. Use template: `.opencode/skills/unity/_templates/basic-skill/SKILL.md`
2. Run validation: `python3 validate_skill.py <skill-path>`
3. Add to this INDEX.md under appropriate category
4. Include 5+ trigger keywords in description
5. Document safety constraints for destructive operations

---

**Need Help?** Start with `unity-orchestrator` - it will route you to the right skill.
