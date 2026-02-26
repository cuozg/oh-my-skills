# Oh My Unity

A comprehensive skill pack and tooling configuration for AI agents working with Unity projects. Clone it into your OpenCode config directory and get 61+ specialized skills, 11 custom tools, 30 slash commands, and 4 agent personas — all tuned for Unity C# development.

## Installation

### 1. Clone

```bash
git clone https://github.com/cuozg/oh-my-unity.git ./.opencode
```

### 2. Install GitHub CLI (`gh`)

Several skills (PR reviews, PR descriptions, git workflows) use the [GitHub CLI](https://cli.github.com/) to interact with GitHub. Install it and authenticate:

**macOS**
```bash
brew install gh
```

Then authenticate:
```bash
gh auth login
```

> For other platforms, see the [official install docs](https://github.com/cli/cli#installation).

## Skills (61)

### Unity — Code
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-code-deep` | **Complex C#** implementation | **Write production C#**, MonoBehaviours, SO | **Skip** simple boilerplate | **Production-ready** `.cs` files | **Unity 6** features supported |
| `unity-code-standards` | **Code quality** gates | **Enforce 4-priority gates**, hygiene, perf | **Auto-fix** code | **Quality assessment** | **Review** guidelines only |
| `unity-code-quick` | **Fast C#** generation | **Generate production C#**, verify diagnostics | **Write** untested code | **Production-ready** `.cs` files | **Delegated** by other skills |
| `unity-refactor` | **Safe code** transformation | **Extract, rename, decouple**, remove dead code | **Break** existing logic | **Refactored** `.cs` files | **Orchestrates** verification |

### Unity — Debug
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-debug-quick` | **Interactive bug** investigation + **error fixing** | **Diagnose errors, propose solutions**, apply user choice | **Stop** after one try | **Fixed** bug | **Loops** until done |
| `unity-debug-deep` | **Exhaustive multi-angle** analysis | **Analyze lifecycle, state**, edge cases | **Modify** code | **Structured** document | **Team review** artifact |
| `unity-debug-fix` | **Error/stack trace** analysis | **Suggest ranked** fix options | **Modify** code | **Ranked** solutions | **Presents** trade-offs |
| `unity-debug-log` | **Tracing execution** flow | **Generate targeted logs**, color-coded | **Modify** project code | **Log** snippets | **Wrapped** in `#if UNITY_EDITOR` |

### Unity — Plan
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-plan-quick` | **Quick** costing | **Estimate size, time**, risks, blast radius | **Write** long documents | **Inline report**, tasks | **XS/S** tasks |
| `unity-plan-deep` | **Big feature** planning | **Investigate codebase**, breakdown work | **Write** verbose plans | **Short markdown**, tasks | **M/L** tasks |
| `unity-plan-detail` | **XL** planning | **Generate per-task patches**, full detail | **Create** tasks automatically | **3 HTML files**, `.patch` | **User registers** tasks |
| `unity-plan-shared` | **Shared plan** pipeline refs | **Provide investigation script**, costing standards | **Activate** directly | **Shared** references | **Used by** other plan skills |
| `unity-plan-executor` | **Execute HTML** plans | **Apply exact code changes**, zero interpretation | **Interpret** or guess | **Modified** project files | **100%** accuracy |

### Unity — Review
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-review-code-local` | **Local logic** review | **Check correctness, edge cases**, data flow | **Push** to GitHub | **Inline** comments | **Delegates** fixes |
| `unity-review-code-pr` | **PR C#** review | **Validate C# behavior**, lifecycle risks | **Modify** code | **GitHub API** comments | **Accepts** PR links |
| `unity-review-architecture` | **PR architecture** review | **Check dependencies, events**, coupling | **Modify** code | **GitHub API** comments | **Accepts** PR links |
| `unity-review-asset` | **PR asset** review | **Check shaders, textures**, models, animations | **Modify** assets | **GitHub API** comments | **Accepts** PR links |
| `unity-review-prefab` | **PR prefab/scene** review | **Check missing scripts**, broken variants | **Modify** prefabs | **GitHub API** comments | **Accepts** PR links |
| `unity-review-general` | **PR general** quality | **Check security, testing**, docs, correctness | **Modify** code | **GitHub API** comments | **Tech-agnostic** checks |
| `unity-review-quality` | **Full project** audit | **Review architecture, perf**, technical debt | **Modify** project files | **HTML report** document | **Read-only** |

### Unity — Investigate
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-investigate-quick` | **Quick** Q&A | **Summarize system**, provide 1-3 details | **Write** long reports | **Direct conversational** answer | **Speed** over ceremony |
| `unity-investigate-deep` | **Full** report | **Trace execution flows**, assess risks | **Skip** architecture diagrams | **Markdown** document | **For team** review |

### Unity — Test
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-test-unit` | **Test Framework** automation | **Create Edit/Play tests**, mock dependencies | **Ignore** coverage | **Test** suites | **Maximizes** coverage |
| `unity-test-case` | **QA test case** documents | **Deep investigate features**, generate test cases | **Miss** edge cases | **HTML** document | **For game** mechanics |

### Unity — Document & Write
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-document-system` | **System architecture** docs | **Document data flows**, extension guides | **Modify** code | **Comprehensive** document | **For** onboarding |
| `unity-document-tdd` | **TDD from real** code | **Document architecture decisions**, implementation | **Guess** implementation | **Technical Design** Document | **Dependency** analysis |
| `unity-write-tdd` | **Feature** specs | **Define game systems**, API specs, schemas | **Ignore** multiplayer/backend | **Technical Design** Document | **Formalizes** plans |
| `unity-write-docs` | **Project** documentation | **Write README, API refs**, code comments | **Ignore** XML docs | **Markdown/XML** docs | **Prefab/Scene** setups |

### Unity — Design
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-game-designer` | **Game design** brainstorming | **Generate GDD, core loops**, economy models | **Write** code | **Game Design** Document | **Compares** design patterns |
| `unity-ux-design` | **UX screen** specs | **Document UI layouts**, navigation flows | **Write** code | **Spec documents**, prefabs | **Mobile game** UI |
| `unity-ui` | **Implement UX** designs | **Translate HTML to prefabs**, map design specs | **Lose** design fidelity | **Unity UI** prefabs | **100%** fidelity |

### Unity — Systems & Editor
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-event-system` | **Event-driven** architecture | **Design communication**, decouple systems | **Skip** pattern selection | **Event** implementation | **C# events**, UnityEvent, SO |
| `unity-serialization` | **Data** persistence | **Build save/load**, serialize complex data | **Handle** encryption | **Serialization** implementation | **JSON, binary**, PlayerPrefs |
| `unity-object-pooling` | **Object pooling** patterns | **Reduce GC**, manage pool lifecycles | **Handle** non-poolable objects | **Pool** implementation | **Generic, UI**, particles |
| `unity-singleton-auditor` | **Audit singleton** usage | **Detect init order risks**, circular deps | **Modify** code | **Audit** report | **Finds** anti-patterns |
| `unity-editor-tools` | **Custom Editor** extensions | **Build Editor Windows**, inspectors, utilities | **Handle** runtime logic | **Editor** scripts | **UXML/USS**, Gizmos |

### Unity — Performance & Build
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-optimize-performance` | **Fix perf** issues | **Profile CPU/GPU**, optimize memory, FPS | **Restructure** architecture | **Optimized** project | **Audits** assets |
| `unity-build-pipeline` | **Build** automation | **Configure Addressables**, CI/CD, asset bundles | **Handle** runtime logic | **Build** scripts/configs | **Platform-specific** |

### Unity — Deploy
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-mobile-deploy` | **iOS/Android** development | **Optimize battery, memory**, handle touch/IAP | **Handle** gameplay logic | **Mobile** builds/configs | **Device** testing |
| `unity-web-deploy` | **WebGL** deployment | **Configure JS interop**, PWA, compression | **Handle** native plugins | **WebGL** builds/configs | **Hosting** setup |

### Unity — Art & 2D
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-tech-art` | **Bridge art** and code | **Optimize shaders, VFX**, procedural gen | **Handle** gameplay logic | **Shaders, tools**, assets | **HLSL**, Shader Graph |
| `unity-sprite-gen` | **AI-generated 2D** sprites | **Create game-ready sprites**, transparent BG | **Create** 3D models | **Sprite/icon** assets | **Auto-configures** import |
| `unity-2d` | **2D game** development | **Setup sprites, tilemaps**, 2D physics | **Handle** 3D systems | **2D** implementation | **Sprite Atlas**, 2D lighting |

### Unity — Other
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `unity-log-analyzer` | **Parse console** logs | **Classify errors, group duplicates**, suggest fixes | **Fix** the errors | **Error summary** report | **Maps errors** to files |
| `unity-fix-errors` | **Console errors** and **build failures** | **Diagnose and fix** compiler/runtime errors | **Ignore** root cause | **Fixed** project | **Assembly**, package errors |

### UI Toolkit
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `ui-toolkit-master` | **Starting** UI Toolkit | **Explain architecture**, UXML/USS/C# triad | **Cover** legacy uGUI | **Project structure** guide | **Unity 6+** |
| `ui-toolkit-architecture` | **Component-based** architecture | **Design UI hierarchies**, MVC/MVP patterns | **Write** runtime logic | **Custom controls** guide | **Scalable** structure |
| `ui-toolkit-databinding` | **Unity 6 runtime** binding | **Bind data models**, reactive UI updates | **Handle** legacy binding | **Data binding** setup | **Type** converters |
| `ui-toolkit-debugging` | **UI** troubleshooting | **Investigate draw calls**, memory leaks | **Fix** code directly | **Debugging** insights | **UI Toolkit** Debugger |
| `ui-toolkit-mobile` | **Mobile UI** optimization | **Handle touch, safe areas**, orientation | **Handle** gameplay input | **Mobile-friendly** UI | **Virtual** keyboard |
| `ui-toolkit-patterns` | **Common UI** patterns | **Implement tabs, grids**, modals, scroll snap | **Design** custom patterns | **UXML/USS/C#** examples | **Reusable** patterns |
| `ui-toolkit-performance` | **UI perf** optimization | **Optimize draw calls**, element pooling | **Restructure** architecture | **Optimized** UI | **Virtualization**, GC-free |
| `ui-toolkit-responsive` | **Responsive** design | **Implement flexbox**, safe area, breakpoints | **Handle** content logic | **Adaptive** UI | **Phone/tablet/desktop** |
| `ui-toolkit-theming` | **Theme** systems | **Build design tokens**, dark/light modes | **Handle** runtime logic | **TSS/USS** setup | **Runtime theme** switching |

### Git
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `git-commit` | **Clean commit** messages | **Generate concise bullets** from staged changes | **Include** AI metadata | **Local** commit | **No tool** attribution |
| `git-comment` | **Amend last** commit | **Generate short bullet-point message** | **Push** to remote | **Amended local** commit | **Reads** latest diff |
| `git-description` | **PR** descriptions | **Deep investigate changes**, structured template | **Ignore** architecture impact | **Edited GitHub** PR | **Uses** `gh pr edit` |
| `git-squash` | **Squash** commits | **Consolidate messy history**, organize commits | **Lose** commit context | **Clean commit** history | **Pre-merge** cleanup |

### Bash
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `bash-check` | **Validate** scripts | **Check syntax, formatting**, runtime issues | **Auto-fix** problems | **Validation** report | **Shell version** aware |
| `bash-optimize` | **Optimize** scripts | **Improve readability, performance**, modern syntax | **Change** functionality | **Refactored** script | **Best practices** applied |
| `bash-install` | **Install** software | **Auto-retry, fallback strategies**, verify | **Skip** verification | **Installed** packages | **CLI tools/dependencies** |

### Skill
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `skill-creator` | **Create/update** skills | **Guide skill creation**, scripts, references | **Auto-deploy** skills | **New/updated** skill | **Extends** capabilities |
| `skill-router` | **Find best skill** match | **Scan, score relevance**, return ranked list | **Execute** the skill | **Ranked** list | **Explains** choices |

### Other
| Skill | Use When | Do | Don't | Result | Notes |
|---|---|---|---|---|---|
| `mermaid` | **Create** diagrams | **Document logic flows**, architecture, state | **Execute** diagrams | **Mermaid** code | **Flowcharts**, sequence, state |
| `flatbuffers-coder` | **FlatBuffers** for Unity | **Create schemas, generate C#**, JSON-to-binary | **Handle** runtime logic | **`.fbs` and C#** files | **Binary** data pipeline |
| `beads` | **Git-backed issue** tracking | **Plan work, track tasks**, manage dependencies | **Write** code | **`bd` CLI** commands | **Multi-agent** coordination |
| `prompt-improver` | **Rewrite vague** prompts | **Score on 5 dimensions**, structure output | **Execute** the task | **Optimized** prompt | **Maximizes** agent success |

## Tools (11)

Custom MCP tools for Unity project analysis and skill management.

| Tool | Description |
|---|---|
| `blueprint-inspector` | Inspect Unity Blueprint data files (JSON) — schema, record count, validation |
| `change-summarizer` | Summarize uncommitted git changes — files changed, systems affected, risk level |
| `codebase-health` | Analyze Unity codebase health metrics — file counts, TODOs, Singletons, line distribution |
| `impact-analyzer` | Analyze blast radius of a C# class/file — traces references, reports risk level |
| `prefab-ref-finder` | Find prefab/scene/asset files that reference a C# script by GUID |
| `skill-deps` | Analyze skill dependencies — build dependency graph, detect missing references |
| `skill-finder` | Find the best matching skill for a task description — ranks by relevance |
| `skill-scaffold-generator` | Generate domain-aware skill scaffolds — tailored SKILL.md templates |
| `skill-scaffold` | Smart skill scaffolding — type-aware templates for unity/bash/git/other |
| `skill-validator` | Deep structural validation of a skill folder — frontmatter, body, references |
| `unity-log-analyzer` | Analyze Unity Editor console logs — classify errors, group duplicates, suggest fixes |

## Commands (30)

Slash commands for common workflows.

| Command | Description |
|---|---|
| `/git comment` | Generate and apply concise commit messages for the last commit |
| `/git description` | Generate structured PR descriptions from GitHub pull request links |
| `/git review` | Review a pull request on GitHub |
| `/git squash` | Squash and organize commits into clean, well-documented history |
| `/omo plan` | Delegation to @prometheus to plan |
| `/omo prompt` | Improve user's prompt |
| `/omo quick` | Delegation to @sisyphus-junior |
| `/omo ulw` | Delegation to @sisyphus (ultrawork) |
| `/skill deep` | Create or update a skill (ultrawork) |
| `/skill quick` | Create or update a skill (quick) |
| `/unity debug deep` | Deep investigation of complex Unity issues |
| `/unity debug fix` | Analyze errors and suggest fix solutions |
| `/unity debug log` | Generate targeted Debug.Log statements |
| `/unity debug quick` | Explain Unity issues, flows, or logic |
| `/unity document system` | Create a system architecture document |
| `/unity document tdd` | Create a Technical Design Document |
| `/unity investigate deep` | Deep investigation with full report output |
| `/unity investigate quick` | Quick investigation of how systems work |
| `/unity plan deep` | Create an implementation plan document |
| `/unity plan detail` | Create a detailed plan with patch generation |
| `/unity plan quick` | Quick costing and impact assessment |
| `/unity review architecture` | Review Unity project architecture in PRs |
| `/unity review asset` | Review Unity asset files in PRs |
| `/unity review code-pr` | Review C# code logic in GitHub PRs |
| `/unity review general` | Review PR against general quality checklists |
| `/unity review local` | Review local code changes with deep logic analysis |
| `/unity review prefab` | Review .prefab and .unity files in PRs |
| `/unity review quality` | Full project quality audit and review |
| `/unity test case` | Create QA test cases plan for a Unity feature |
| `/unity test unit` | Create unit tests for a Unity feature |

## Agents (4)

| Agent | Mode | Description |
|---|---|---|
| `omo` | Primary | Prompt-optimizing agent — rewrites vague prompts into structured, actionable format |
| `sisyphus-raw-proxy` | Primary | Zero-modification proxy — forwards exact user prompt to Sisyphus unchanged |
| `unity-code-reviewer` | Subagent | Expert Unity code reviewer for C# scripts, prefabs, scenes, materials, shaders |
| `unity-debugger` | Subagent | Investigate complex system issues, analyze performance bottlenecks, debug pipelines |

## Rules (3)

Shared rules applied across all agents.

| Rule | Purpose |
|---|---|
| `agent-behavior` | Core agent behavior guidelines and interaction patterns |
| `unity-asset-rules` | Unity asset handling conventions and best practices |
| `unity-csharp-conventions` | C# coding standards specific to Unity projects |

## License

MIT
