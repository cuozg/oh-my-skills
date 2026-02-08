# Unity Skill Catalog

Complete catalog of specialized skills in `.claude/skills/`.

## Core Skills

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `unity-orchestrator` | ALL Unity requests - routes to specialists | Any Unity question |
| `unity-code` | C# systems, MonoBehaviours, gameplay features | "implement", "create script", "add feature" |
| `unity-investigate-code` | Trace execution, understand existing code | "how does X work", "trace the flow", "explain this code" |

## Error & Debug Skills

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `unity-fix-errors` | Console errors, compiler errors, build failures | "fix error", "build failed", "NullReference" |
| `unity-debug` | Unexpected behavior requiring strategic investigation | "debug", "why is this happening", "investigate crash" |

## Performance & Optimization

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `unity-optimize-performance` | FPS issues, memory leaks, slow loads | "slow", "laggy", "memory leak", "optimize" |

## Platform Skills

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `unity-mobile-deploy` | iOS/Android: touch, native features, optimization | "mobile", "iOS", "Android", "touch input" |
| `unity-web-deploy` | WebGL: browser interop, memory limits, PWA | "WebGL", "browser", "JS interop" |

## Art & Tools

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `unity-tech-art` | Shaders, asset pipelines, procedural generation | "shader", "postprocessor", "rendering" |
| `unity-editor-tools` | Custom windows, inspectors, editor automation | "editor window", "inspector", "editor tool" |
| `unity-mcp` | unityMCP automation for Editor tasks | "automate", "batch", "find GameObject" |

## Planning & Documentation

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `unity-plan` | Requirements → roadmap with epics/tasks | "plan", "implement feature", "how should I build" |
| `unity-plan-brainstorm` | Critique and refine plans | After `unity-plan` |
| `unity-plan-tasks` | Create task skeletons in Documents/Tasks/ | After `unity-plan-brainstorm` |
| `unity-task-brainstorm` | Technical deep-dive with code-level details | After `unity-plan-tasks` |
| `unity-task-executor` | Execute detailed task instructions | After `unity-task-brainstorm` |
| `unity-write-tdd` | Formal Technical Design Documents | "TDD", "technical spec", "design document" |
| `unity-write-docs` | README, architecture docs, API references | "document", "README", "onboarding guide" |

## Testing & Quality

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `unity-test` | Edit/Play Mode tests, test assemblies | "test", "unit test", "test coverage" |
| `unity-review-pr` | GitHub PR code reviews | "review PR", "code review" |

## Data & Serialization

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `flatbuffers-coder` | FlatBuffers schemas, C# generation, binary data | "schema", "flatbuffers", "serialize", "data table" |

## Visualization

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `mermaid` | Flowcharts, sequence diagrams, architecture maps | "diagram", "flowchart", "visualize" |

## Meta

| Skill | When to Use | Triggers |
|:------|:------------|:---------|
| `skill-creator` | Create or improve agent skills | "create skill", "update skill" |

## Routing Decision Guide

### Error Handling

1. **Has error message/stack trace?** → `unity-fix-errors`
2. **No error but wrong behavior?** → `unity-debug`
3. **Performance degradation?** → `unity-optimize-performance`

### Feature Implementation

1. **Quick fix (1-2 files)?** → `unity-code`
2. **Medium scope (known requirements)?** → `unity-task-brainstorm` → `unity-task-executor`
3. **Large scope (needs planning)?** → Full pipeline starting with `unity-plan`

### Documentation

1. **Architecture/flow explanation?** → `unity-write-docs` + `mermaid`
2. **Formal specification?** → `unity-write-tdd`
3. **Code understanding?** → `unity-investigate-code`
