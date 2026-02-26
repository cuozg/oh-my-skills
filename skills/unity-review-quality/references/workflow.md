## Workflow

### Step 1: Project Discovery
Gather project metadata using tools — do NOT modify anything.
- Run parallel globs: `Assets/**/*.cs`, `*.unity`, `*.prefab`, `*.asmdef`, `*.shader`, `*.shadergraph`
- Run `codebase-health` tool for quick metrics
- Read `ProjectSettings/ProjectSettings.asset`, `Packages/manifest.json`

### Steps 2-5: Parallel Investigation
See `review-workflow.md` for detailed agent tables covering:
- **Step 2**: Architecture scan (patterns, assembly structure, coupling, data flow)
- **Step 3**: Code quality deep-dive (hot paths, lifecycle, memory, async, anti-patterns)
- **Step 4**: Unity-specific review (serialization, assets, scenes/prefabs, physics/rendering)
- **Step 5**: Project health check (settings, build config, gitignore)

### Step 6: Compile Report
Read template parts in order from `assets/templates/QUALITY_REVIEW_REPORT_SECTION1.md` through `assets/templates/QUALITY_REVIEW_REPORT_SECTION8.md`. Fill every section — mark empty ones "No issues found." Output to: `Documents/Reviews/QUALITY_REVIEW_[ProjectName]_[YYYYMMDD].html`

### Step 7: Present Summary
Use the template in `summary-template.md` to present findings to the user.

## Review Principles

1. **Breadth first** — scan the whole project structure before deep-diving into specific files
2. **Worst first** — prioritize findings by impact, not by file order
3. **Context matters** — a prototype has different standards than a shipping product. Note project maturity.
4. **Explain "why"** — every finding explains the real-world impact, not just the rule violation
5. **Be fair** — acknowledge good patterns alongside problems. Include a "What's Done Well" section.
6. **Quantify** — estimate memory impact, CPU cost, build size contribution where possible
