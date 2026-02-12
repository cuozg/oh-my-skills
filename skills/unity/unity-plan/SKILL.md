---
name: unity-plan
description: "High-level planning for Unity features with multi-file output and patch generation. Use when: (1) Analyzing requirements and specs, (2) Investigating existing codebase/systems, (3) Breaking work into epics and tasks, (4) Estimating effort and identifying risks, (5) Generating implementation patches with 100% code changes. Outputs a folder of HTML files (overview, tasks, estimates, dependencies, timeline) plus a unified diff patch file."
---

# Unity Planning Skill

Create implementation plans for Unity features with architecture, task breakdown, estimates, dependencies, timeline, and complete code patches.

## Purpose

High-level planning for Unity features with multi-file output and patch generation — providing a structured, repeatable workflow that produces consistent results.

## Input

- **Required**: A clear description of the task or problem to address.
- **Optional**: Relevant file paths, constraints, or context that narrows the scope.

## Output

A folder of 6 HTML files + 1 patch file at `documents/plans/{plan-name}/`:
- `overview.html` — Architecture, summary cards, technical approach
- `tasks.html` — Epic/task breakdown with full walkthroughs
- `estimates.html` — Per-epic effort estimates and resource allocation
- `dependencies.html` — Dependency graph, risk matrix, blockers
- `timeline.html` — Phased implementation schedule with milestones
- `patch.html` — Visual diff viewer for all code changes
- `changes.patch` — Raw unified diff containing 100% of code changes

## Examples

| Trigger | What Happens |
|---------|-------------|
| "Run unity-plan" | Executes the primary workflow end-to-end |
| "Apply unity-plan to <target>" | Scopes execution to a specific file or module |
| "Check unity-plan output" | Reviews and validates previous results |


**IMPORTANT**: This skill is for **planning only**. Do NOT implement or execute any work — but DO generate complete code patches showing all changes.

---

## Architecture: Templates vs Generated Files

This skill uses a **template-to-output** architecture. Understanding the distinction prevents `ERR_FILE_NOT_FOUND` errors.

**Templates** (`assets/templates/`) are **internal boilerplate** containing HTML structure, CSS, `[PLACEHOLDER]` values, and `<!-- INSTRUCTION: ... -->` comments. They exist solely as input to the generation process. **NEVER** access template files directly — opening them in a browser shows placeholder text and navigation links break because sibling files don't exist at that path.

**Generated files** (`documents/plans/{plan-name}/`) are the **actual user-facing output** created by processing templates with real plan data. Users open these files in their browser.

| Template (internal — do not access) | Generated Output (user-facing) |
|---|---|
| `assets/templates/PLAN_OVERVIEW.html` | `documents/plans/{plan-name}/overview.html` |
| `assets/templates/PLAN_TASKS.html` | `documents/plans/{plan-name}/tasks.html` |
| `assets/templates/PLAN_ESTIMATES.html` | `documents/plans/{plan-name}/estimates.html` |
| `assets/templates/PLAN_DEPENDENCIES.html` | `documents/plans/{plan-name}/dependencies.html` |
| `assets/templates/PLAN_TIMELINE.html` | `documents/plans/{plan-name}/timeline.html` |
| `assets/templates/PLAN_PATCH.html` | `documents/plans/{plan-name}/patch.html` |
| `assets/templates/PLAN_PATCH_TEMPLATE.patch` | `documents/plans/{plan-name}/changes.patch` |

`{plan-name}` = kebab-case feature name (e.g. `multi-event-daily-boss`).

---

## Generation Process

When generating output from a template:

1. Read the template from `assets/templates/` to understand structure
2. Replace all `[PLACEHOLDER]` values with actual plan content
3. Keep the sticky `<nav class="plan-nav-bar">` — it is the first element in `<body>`, before `.container`. All navigation href paths use the `PLAN_` prefix format (e.g. `./PLAN_OVERVIEW.html`, `./PLAN_TASKS.html`) matching the actual template file names
4. Mark the correct tab with `class="nav-tab nav-tab-active"` for each output file (only one tab is active per file)
5. Remove all `<!-- INSTRUCTION: ... -->` comments from final output
6. Write the completed HTML to `documents/plans/{plan-name}/`
7. **Do NOT add any `<script>` tags or JavaScript** — navigation relies on pure HTML `<a href>` links with browser-default behavior
8. **Do NOT add `addEventListener`, `console.log`, `preventDefault`, or any event handlers** — these break navigation

---

## Workflow

### 1. Read All Templates

Read every template file in `assets/templates/`. Note the `<!-- INSTRUCTION: ... -->` comments — they describe what content goes where. The sticky navigation bar (`<nav class="plan-nav-bar">`) is the first element in `<body>`, uses relative paths with `PLAN_` prefix (e.g. `./PLAN_OVERVIEW.html`, `./PLAN_TASKS.html`), and has the current page's tab marked with `class="nav-tab-active"`. It stays fixed at the top while users scroll.

### 2. Analyze Requirements

- Read the provided spec/requirements
- Identify goals, constraints, and acceptance criteria
- Note ambiguities — **ask clarifying questions** if specs are unclear

### 3. Investigate Codebase

Use the **`unity-investigate`** skill:

```
Read and follow: .claude/skills/unity-investigate/SKILL.md
```

Focus on: existing systems affected, files needing modification, technical debt, reusable components, entry points and execution flows.

### 4. Create Output Folder

```bash
mkdir -p documents/plans/{plan-name}
```

### 5. Generate overview.html

Read `assets/templates/PLAN_OVERVIEW.html`. Replace placeholders and write to `documents/plans/{plan-name}/overview.html`. Populate:
- Feature title and generation date
- Summary cards: duration, risk, task count, epic count
- Architecture overview: old vs new ASCII diagrams + key benefits
- Technical approach: numbered implementation steps with `<code>` references

### 6. Generate tasks.html

Read `assets/templates/PLAN_TASKS.html`. Replace placeholders and write to `documents/plans/{plan-name}/tasks.html`. Populate:
- Task table grouped by epic (columns: #, Epic, Task, Description, Type, Cost)
- **Full walkthrough for EVERY task** — each task gets:
  - Detailed description of what to implement
  - Step-by-step implementation instructions
  - List of every file to modify/create
  - Task-specific acceptance criteria

Valid Types: `Logic`, `UI`, `Data`, `API`, `Asset`, `Test`, `Config`

Cost badges: `badge-s` S (<2h), `badge-m` M (2-4h), `badge-l` L (4-8h), `badge-xl` XL (1-2d)

Task numbering: `[Epic#].[Task#]` (e.g. 1.1, 1.2, 2.1)

### 7. Generate estimates.html

Read `assets/templates/PLAN_ESTIMATES.html`. Replace placeholders and write to `documents/plans/{plan-name}/estimates.html`. Populate:
- Aggregate totals: total hours range, total days range, complexity
- Per-epic estimation table with cost distribution (S/M/L/XL counts)
- Resource allocation cards: role, hours, assigned tasks, required skills
- Estimation assumptions

### 8. Generate dependencies.html

Read `assets/templates/PLAN_DEPENDENCIES.html`. Replace placeholders and write to `documents/plans/{plan-name}/dependencies.html`. Populate:
- ASCII dependency graph showing task flow with arrows
- Dependency matrix: each task's depends-on and blocks relationships
- Risk cards with level (high/medium/low), description, mitigation
- Blocker list with severity icons

### 9. Generate timeline.html

Read `assets/templates/PLAN_TIMELINE.html`. Replace placeholders and write to `documents/plans/{plan-name}/timeline.html`. Populate:
- Implementation phases with tasks per phase and duration
- Milestone checkpoints with success criteria
- Recommended implementation order with rationale

### 10. Generate changes.patch

Read `assets/templates/PLAN_PATCH_TEMPLATE.patch` as format reference. Generate a unified diff at `documents/plans/{plan-name}/changes.patch` containing **100% of all code changes** for the entire plan.

**Patch generation rules:**
1. Include every file that any task modifies, creates, or deletes
2. Use unified diff format: `--- a/path` / `+++ b/path` / `@@ hunks @@`
3. New files: `--- /dev/null` / `+++ b/path`
4. Deleted files: `--- a/path` / `+++ /dev/null`
5. Include 3 lines of context around each change
6. Order: new files, then modified files, then deleted files
7. Every task in the plan MUST have corresponding code in the patch
8. The patch must apply cleanly: `patch -p1 --dry-run < changes.patch`

### 11. Generate patch.html

Read `assets/templates/PLAN_PATCH.html`. Replace placeholders and write to `documents/plans/{plan-name}/patch.html`. Populate:
- Patch stats: file count, total additions, total deletions
- File list: each file with status (added/modified/deleted) and per-file stats
- Diff viewer: GitHub-style diff rendering with line numbers, additions (green), deletions (red), context lines
- Download link to raw `changes.patch` file

### 12. Verbal Summary

After generating all files, provide:
- Location of generated files: `documents/plans/{plan-name}/`
- Instruction to open `overview.html` in a browser
- Total estimated effort
- Key risks or blockers
- Critical path through dependencies
- Recommended implementation order
- Patch file statistics (files changed, insertions, deletions)

---

## How to Access Generated Plans

After generation, files are in `documents/plans/{plan-name}/`:

```
documents/plans/{plan-name}/
├── overview.html       ← Start here
├── tasks.html
├── estimates.html
├── dependencies.html
├── timeline.html
├── patch.html          ← Visual diff viewer
└── changes.patch       ← Raw patch file
```

1. Open `documents/plans/{plan-name}/overview.html` in a browser
2. Use the sticky navigation bar at the top to switch between sections (Overview, Tasks, Estimates, Dependencies, Timeline, View Patch)
3. The current section's tab is highlighted in blue — click any other tab to navigate
4. All navigation uses relative paths with `PLAN_` prefix matching template file names (`./PLAN_OVERVIEW.html`, `./PLAN_TASKS.html`, `./PLAN_ESTIMATES.html`, `./PLAN_DEPENDENCIES.html`, `./PLAN_TIMELINE.html`, `./PLAN_PATCH.html`)
5. The "View Patch" tab opens `patch.html` which shows a visual diff viewer with download link to raw `changes.patch`

**WARNING**: Do NOT open files from `.claude/skills/unity-plan/assets/templates/`. Those are internal templates with placeholder text. Clicking navigation tabs will cause `ERR_FILE_NOT_FOUND` because sibling files don't exist at that location.

### Navigation: Pure HTML Only

Navigation between plan pages uses **pure HTML anchor tags** (`<a href="./page.html">`). This is intentional.

**DO NOT** add any of the following to generated output:
- `<script>` tags
- `addEventListener` calls
- `console.log` statements
- `preventDefault()` or `stopPropagation()` calls
- `onclick` attributes or inline event handlers
- Any JavaScript that intercepts or modifies link behavior

The browser's default `<a href>` behavior handles navigation. Adding JavaScript click handlers can intercept clicks and prevent navigation — this is the most common cause of "tabs don't work" bugs.

### Content Security Policy (CSP)

All templates include a CSP meta tag in `<head>` that controls what resources the browser allows. This prevents CSP violation errors (e.g., `default-src 'none'` blocking navigation, connections, and inline styles).

**Current CSP configuration:**
```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self' 'unsafe-inline';
               style-src 'self' 'unsafe-inline'; img-src 'self' data:;
               font-src 'self' data:; connect-src 'self'; frame-src 'self';
               object-src 'none'; base-uri 'self'; form-action 'self';">
```

**Directive breakdown:**
| Directive | Value | Purpose |
|---|---|---|
| `default-src` | `'self'` | Allow same-origin resources by default |
| `script-src` | `'self' 'unsafe-inline'` | Allow inline scripts (unused but safe fallback) |
| `style-src` | `'self' 'unsafe-inline'` | Allow inline `<style>` blocks (required — all CSS is inline) |
| `img-src` | `'self' data:` | Allow images and data URIs |
| `font-src` | `'self' data:` | Allow fonts and data URIs |
| `connect-src` | `'self'` | Allow XHR/fetch/WebSocket to same origin (prevents DevTools CSP errors) |
| `frame-src` | `'self'` | Allow iframes from same origin |
| `object-src` | `'none'` | Block plugins (Flash, Java applets) |
| `base-uri` | `'self'` | Restrict `<base>` tag to same origin |
| `form-action` | `'self'` | Restrict form submissions to same origin |

**Why `'self'` instead of `'none'`:**
These are local HTML files opened via `file://` or a local dev server (`http://127.0.0.1:5504/`). Using `default-src 'none'` blocks all connections — including DevTools, inline styles, and same-origin navigation — causing console errors and broken functionality.

**Security considerations:**
- Generated plans are local files, not deployed to public web servers
- No external resources are loaded (all CSS is inline, no external JS)
- `object-src 'none'` prevents plugin-based attacks
- If deploying to a web server, consider tightening `script-src` by removing `'unsafe-inline'` and using nonces or hashes instead

**IMPORTANT:** When generating output files, the CSP meta tag from the template must be preserved exactly as-is. Do not modify, remove, or replace it with a more restrictive policy.

---

## Output Checklist

Before completing, verify:

- [ ] All 7 templates read from `assets/templates/` before generating output
- [ ] Output folder created at `documents/plans/{plan-name}/`
- [ ] All 6 HTML files written to output folder (NOT to `assets/templates/`)
- [ ] overview.html: CSS copied exactly, all placeholders replaced, architecture has old/new diagrams
- [ ] tasks.html: Every task has a walkthrough section, files listed, criteria defined
- [ ] estimates.html: Per-epic totals, resource allocation cards, assumptions listed
- [ ] dependencies.html: Dependency graph, matrix, risks with mitigations, blockers
- [ ] timeline.html: Phases with tasks, milestones with criteria, recommended order
- [ ] changes.patch: Unified diff format, all tasks have code changes, applies cleanly
- [ ] patch.html: Visual diff viewer with stats, file list, diff rendering, download link
- [ ] Navigation tabs present in all 6 HTML files with `PLAN_` prefix paths (e.g. `./PLAN_OVERVIEW.html`)
- [ ] Sticky navbar is FIRST element in `<body>`, before `.container`
- [ ] Correct tab marked `class="nav-tab-active"` in each file
- [ ] Patch tab links to `./PLAN_PATCH.html` with `class="nav-tab-patch"` in all HTML files
- [ ] **No `<script>` tags, JavaScript, or event handlers in any generated HTML file**
- [ ] All `<!-- INSTRUCTION: ... -->` comments removed from final output
- [ ] Summary includes path to generated files for user to open

---

## What This Skill Does NOT Do

- Execute implementations from the plan
- Modify actual project files (except creating the plan output folder)
- Run the generated patch file
- Skip any task in the walkthrough or patch
- Serve files from `assets/templates/` to users

---

## MCP Tools Integration

Use `unityMCP_*` tools during the **Investigate Codebase** phase (Step 3) to gather project context.

| Operation | MCP Tool |
|-----------|----------|
| Project state | `unityMCP_get_unity_editor_state` |
| Scene hierarchy | `unityMCP_list_game_objects_in_hierarchy()` |
| Object details | `unityMCP_get_game_object_info(gameObjectPath="...")` |
| Installed packages | `unityMCP_list_packages` |

### Codebase Assessment Flow

```
1. unityMCP_get_unity_editor_state           → Unity version, active scene, build target
2. unityMCP_list_game_objects_in_hierarchy()  → Understand existing scene structure
3. unityMCP_list_packages                     → Identify available packages/dependencies
4. [Proceed with plan generation]
```
