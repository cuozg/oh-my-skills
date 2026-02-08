---
name: unity-plan-detail
description: "Generate 100% complete code changes for each task in a plan. Use when: (1) A plan HTML file from unity-plan exists and needs per-task code, (2) Need fully implementable code for individual tasks, (3) Preparing executable task specs for unity-task-executor. Input: plan HTML from Documents/Plans/. Output: HTML with complete code per task in Documents/Tasks/."
---

# Unity Plan Detail

Walk through every task in a plan file and generate **100% complete code changes**.

**CRITICAL**: This skill produces **per-task code only**. It does NOT:
- Repeat the high-level plan (architecture, epics, acceptance criteria)
- Generate summaries or explanations beyond task scope
- Skip any code — every line must be shown

---

## Input

A plan HTML file from `unity-plan`, typically at `Documents/Plans/[FeatureName]_PLAN.html`.

---

## Output

HTML file at `Documents/Tasks/[FeatureName]_DETAIL.html` following template exactly:

**Template**: `.claude/skills/unity-plan-detail/assets/templates/DETAIL_OUTPUT.html`

Read template first. Copy exact HTML/CSS. Replace only placeholders.

---

## Workflow

### 1. Parse Plan File

Read input HTML and extract:
- Feature metadata (title, duration)
- **Task table**: all rows with task number, epic, title, description, type, cost
- Technical approach (for context only)

### 2. For Each Task

Walk through EVERY task in the task table and produce:

#### 2.1 Title
Format: `[TASK_NUMBER] — [TASK_TITLE]`

#### 2.2 Description
Write comprehensive description:
- **Purpose**: what this task accomplishes
- **Approach**: how implementation works
- **Dependencies**: which tasks must complete first
- **Files affected**: list with change summary
- **Edge cases**: special handling needed

#### 2.3 Code Changes (CRITICAL — 100% COMPLETE)

**MANDATORY**: For each file in the task, show **ALL code changes**.

**How to generate code:**

1. **Read actual source files** using `unity-investigate-code` skill:
   ```
   Read and follow: .claude/skills/unity-investigate-code/SKILL.md
   ```

2. **For existing files**:
   - Read current file content
   - Identify exact lines to change
   - Show complete before/after with context
   - Include accurate line numbers

3. **For new files**:
   - Show full file content as additions
   - Left side all empty, right side all green

**Rules:**
- Show 100% of code changes — no omissions
- Complete method implementations, not snippets
- Full class definitions when creating new classes
- Complete `[Obsolete]` wrappers with forwarding logic
- Accurate line numbers from actual source
- Correct hunk headers `@@ -old,count +new,count @@`

**NEVER:**
- Use `...` or `// remaining code`
- Skip files because they are "similar"
- Summarize instead of showing code
- Omit any method or property
- Reuse diffs without verifying source

### 3. Assemble Output

Using DETAIL_OUTPUT.html template:
1. Fill header with feature metadata
2. Build table of contents from tasks
3. Create one `task-section` per task
4. Each task has: title, description, file diffs
5. Remove all `<!-- INSTRUCTION: -->` comments

### 4. Save

Save to `Documents/Tasks/[FeatureName]_DETAIL.html`.

Provide summary:
- Total tasks detailed
- Files per task
- Recommended implementation order

---

## Diff Structure Reference

All diff formats defined in template. Key patterns:

```html
<!-- Context line (unchanged) -->
<tr class="diff-line-context">
  <td class="diff-line-num">42</td>
  <td class="diff-line-sign"></td>
  <td class="diff-line-code">    unchanged line</td>
</tr>

<!-- Deletion (left side, red) -->
<tr class="diff-line-deletion">
  <td class="diff-line-num">43</td>
  <td class="diff-line-sign">-</td>
  <td class="diff-line-code">    <y>removed</y> code</td>
</tr>

<!-- Addition (right side, green) -->
<tr class="diff-line-addition">
  <td class="diff-line-num">43</td>
  <td class="diff-line-sign">+</td>
  <td class="diff-line-code">    <x>added</x> code</td>
</tr>

<!-- Empty placeholder -->
<tr class="diff-line-empty">
  <td class="diff-line-num"></td>
  <td class="diff-line-sign"></td>
  <td class="diff-line-code"></td>
</tr>
```

Word highlights:
- `<x>text</x>` — new/changed text (green)
- `<y>text</y>` — removed/changed text (red)

HTML escape: `& → &amp;` `< → &lt;` `> → &gt;`

---

## Output Checklist

- [ ] Read DETAIL_OUTPUT.html template first
- [ ] Copied exact CSS
- [ ] Header placeholders filled
- [ ] Table of contents lists all tasks
- [ ] Each task has section block
- [ ] Each task has title + description + code
- [ ] ALL files for each task shown
- [ ] 100% code shown — no `...` or summaries
- [ ] Line numbers verified against source
- [ ] HTML characters escaped
- [ ] Saved to Documents/Tasks/
