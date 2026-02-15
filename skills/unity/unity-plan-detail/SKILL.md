---
name: unity-plan-detail
description: "Generate 100% complete code changes for each task in a plan. Use when: (1) A plan HTML file from unity-plan exists and needs per-task code, (2) Need fully implementable code for individual tasks, (3) Preparing executable task specs for unity-plan-executor. Input: plan HTML from Documents/Plans/. Output: HTML with complete code per task in Documents/Tasks/."
---

# Unity Plan Detail

**Input**: Plan HTML from `Documents/Plans/[FeatureName]_PLAN.html`
**Output**: HTML at `Documents/Tasks/[FeatureName]_DETAIL.html` using template at `.opencode/skills/unity/unity-plan-detail/assets/templates/DETAIL_OUTPUT.html`

**CRITICAL**: Produces per-task code ONLY. No plan summaries, no explanations beyond task scope, no omitted code.

## Workflow

1. **Parse plan** — read input HTML, extract task table (number, epic, title, description, type, cost) and technical approach
2. **For each task**:
   - **Title**: `[TASK_NUMBER] — [TASK_TITLE]`
   - **Description**: purpose, approach, dependencies, files affected, edge cases
   - **Code changes** (100% complete):
     - Read actual source via `unity-investigate` skill
     - Existing files: show complete before/after with accurate line numbers
     - New files: full content as additions
     - Correct hunk headers `@@ -old,count +new,count @@`
3. **Assemble** — read DETAIL_OUTPUT.html template, fill header, build TOC, one `task-section` per task, remove `<!-- INSTRUCTION: -->` comments
4. **Save** to `Documents/Tasks/[FeatureName]_DETAIL.html` with summary (total tasks, files per task, implementation order)

## Code Change Rules

**MANDATORY**:
- 100% of code changes — no omissions
- Complete method/class implementations, not snippets
- Accurate line numbers from actual source

**NEVER**:
- Use `...` or `// remaining code`
- Skip files because they are "similar"
- Summarize instead of showing code

## Diff Structure Reference

```html
<!-- Context (unchanged) -->
<tr class="diff-line-context"><td class="diff-line-num">42</td><td class="diff-line-sign"></td><td class="diff-line-code">    unchanged</td></tr>
<!-- Deletion (red) -->
<tr class="diff-line-deletion"><td class="diff-line-num">43</td><td class="diff-line-sign">-</td><td class="diff-line-code">    <y>removed</y></td></tr>
<!-- Addition (green) -->
<tr class="diff-line-addition"><td class="diff-line-num">43</td><td class="diff-line-sign">+</td><td class="diff-line-code">    <x>added</x></td></tr>
```

Word highlights: `<x>text</x>` (green/new), `<y>text</y>` (red/removed). HTML escape: `& → &amp;` `< → &lt;` `> → &gt;`

## Output Checklist

- [ ] Read DETAIL_OUTPUT.html template first
- [ ] Header placeholders filled, TOC lists all tasks
- [ ] Each task has title + description + code
- [ ] 100% code shown — no `...` or summaries
- [ ] Line numbers verified against source
- [ ] HTML characters escaped
- [ ] Saved to Documents/Tasks/
