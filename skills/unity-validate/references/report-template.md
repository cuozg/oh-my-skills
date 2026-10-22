# Validation Report Template

**With a task file** (`Docs/Tasks/<task-name>.md`):
- Fill the Status and Evidence cells of its Test cases table.
- Write the **Validation** block below in place of the task file's `## Validation` section.
- Images go in `Docs/Tasks/assets/<task-name>/`.

**Standalone** (bug repro, fix check, image check, ad-hoc request): create
`Docs/Validations/<name>.md` with the full template. Images go in `Docs/Validations/assets/<name>/`.

`Docs/` lives at the Unity project root (next to `Assets/`), so project-relative tool output paths
and the Markdown image links agree.

Verdicts: `✅ Validated` · `❌ Failed` · `🟠 Not validated` · `🔴 Reproduced` · `⚪ Not reproduced` · `🟢 Fixed` · `❌ Still reproduces`
Case icons: `✅` pass with evidence · `❌` fail · `⚠️` cannot validate (reason + manual steps)
Methods: `Unit` · `PlayMode test` · `PlayMode run` · `Tree` · `Prefab shot` · `Game shot` · `Texture` · `Visual` · `Manual`

````markdown
# Validation: <title>

**Target:** <Docs/Tasks/x.md | bug: one line | image: path>

## Requirements (as checked)
- <R1: one checkable requirement>

## Cases
| ID | Case | Expected | Method | Status | Evidence |
|----|------|----------|--------|--------|----------|
| T1 | <case> | <observable result> | <Game shot> | ✅ | ![T1](assets/<name>/T1.png) |

## Validation

**Verdict:** <verdict>
**Validated:** YYYY-MM-DD · commit <short sha> + <clean | N uncommitted files> · Unity <version> · <live Editor | batch>

### Build health
- Compile: <clean | errors>
- Console: <nothing beyond baseline (<where the baseline came from>) | new lines pasted below>

### Tests
- <N passed / M failed – classes> · bite check: <T1_… went red when <change>, restored (checksum match)>
- Repro test kept: <path – bugs only | N/A>
- <N/A – no logic change>

### Evidence
<per case, as needed: tree, probe output, console excerpt, texture facts, before/after values>
```
<output>
```

### UI vs design
| State | Design | Implemented |
|-------|--------|-------------|
| <normal> | ![design](assets/<name>/design.png) | ![impl](assets/<name>/impl-normal.png) |

- <mismatch: what | none | N/A – no design provided>

### Not validated
- <case: reason + manual steps | none>
````

In the task-file case, copy only from `## Validation` down (it carries the verdict). The task
file already holds the title, requirements, and cases.
