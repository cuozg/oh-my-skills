# MCP Operation Log

**Date**: {YYYY-MM-DD}
**Scene**: {Scene name}
**Instance**: {ProjectName@hash or "default"}
**Operations**: {N total}

---

## 1. Pre-check

| Check | Result |
|-------|--------|
| `editor/state.ready_for_tools` | {true/false} |
| `editor/state.is_compiling` | {true/false} |
| Active scene | {scene name} |

---

## 2. Operations Performed

| # | Tool | Action | Target | Result |
|---|------|--------|--------|--------|
| 1 | `{tool_name}` | {action} | {GameObject/Component/Asset} | {Success/Failed} |
| 2 | `{tool_name}` | {action} | {GameObject/Component/Asset} | {Success/Failed} |

---

## 3. Verification

| Check | Method | Result |
|-------|--------|--------|
| Visual | `manage_scene(action="screenshot")` | {Confirmed/Issue found} |
| Console | `read_console(types=["error"])` | {Clean/Errors found} |
| Hierarchy | `manage_scene(action="get_hierarchy")` | {Expected/Unexpected} |
| Compilation | `refresh_unity` | {Clean/Errors} |

---

## 4. Summary

**Successful**: {N} operations
**Failed**: {N} operations
**Scripts created/edited**: {list or "None"}
**Warnings**: {Any issues to note}
