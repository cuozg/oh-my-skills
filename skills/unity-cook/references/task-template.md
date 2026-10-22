# Task File Template

Copy to `Docs/Tasks/<task-name>.md`. Write the **Spec** half in step 2 and the **Result** half
in step 6. `unity-validate` owns the Status/Evidence cells of the Test cases table and the
`## Validation` section (layout in `../unity-validate/references/report-template.md`). Keep
bullets to one line each.
Write `N/A – <reason>` for a section that does not apply. Never delete the section.

Status icons: `🟡 Awaiting approval` → `🔵 In progress` → `✅ Done` | `🟠 Not validated` | `❌ Blocked`
Case icons: `⬜` not run, `✅` passed with evidence, `❌` failed, `⚠️` cannot validate (reason + manual steps required)
Method values: `Unit` · `PlayMode test` · `PlayMode run` · `Tree` · `Prefab shot` · `Game shot` · `Texture` · `Visual` · `Manual` (see `../unity-validate/references/recipes.md`)

````markdown
# <Task Title>

**Status:** 🟡 Awaiting approval
**Type:** <ui-prefab | logic | mixed>
**Console baseline:** <N errors / M warnings before the change; key lines – written in step 3>
**Created:** YYYY-MM-DD · **Updated:** YYYY-MM-DD

---

## Spec

### Request (as understood)
- <one bullet per requirement, in the agent's words>

### Out of scope
- <what this task will not touch>

### Assumptions
- <assumption> — <why it is reasonable>

### Design source
- <image path | Figma link | N/A – no UI change | N/A – no design provided>

### Test cases
| ID | Case | Expected | Method | Status | Evidence |
|----|------|----------|--------|--------|----------|
| T1 | <happy path> | <observable result> | <Unit> | ⬜ | |
| T2 | <edge / empty / error> | <observable result> | <Prefab shot> | ⬜ | |
| R1 | <regression: existing flow X still works> | <observable result> | <Unit> | ⬜ | |

---

## Result

### What was done
- <one bullet per change, why-first>

### Changed files
| File | Change |
|------|--------|
| [Path/File.cs](../../Path/File.cs#L10-L42) | <one line> |

`git diff --stat`:
```
<output>
```

### Review & impact
| # | Severity | Finding | Resolution |
|---|----------|---------|------------|
| 1 | Major | <finding with file:line> | fixed / kept: <reason> |

- Impact: <changed public symbols / prefabs / scenes → who references them → checked how>

---

## Validation
<written by unity-validate: verdict + validated commit, build health, tests, evidence, UI vs design, not validated>
````
