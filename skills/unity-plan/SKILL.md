---
name: unity-plan
description: "High-level planning for Unity features. Use when: (1) Analyzing requirements and specs, (2) Investigating existing codebase/systems, (3) Breaking work into epics and tasks, (4) Estimating effort and identifying risks. Outputs an HTML file with architecture overview, technical approach, task breakdown, and acceptance criteria."
---

# Unity Planning Skill

Create implementation plans for Unity features with clear architecture, task breakdown, and acceptance criteria.

**IMPORTANT**: This skill is for **planning only**. Do NOT implement or execute any work.

---

## Mandatory Output Requirement

**The output MUST follow the template EXACTLY — 100% identical structure, no exceptions.**

- **Template**: `.claude/skills/unity-plan/assets/templates/PLAN_OUTPUT.html`
- **Output path**: `Documents/Plans/[FeatureName]_PLAN.html`

1. **Read the template file FIRST** before generating any output
2. **Copy the exact HTML structure** — all CSS, all classes, all elements
3. **Replace only the placeholder values** — do not modify structure
4. **Use the exact CSS** from the template verbatim
5. All placeholder names, class names, and section structures are defined **exclusively in the template** — refer to the inline `<!-- INSTRUCTION: ... -->` comments

---

## Workflow

### 1. Read the Template

Before any analysis, read the template file and understand all `<!-- INSTRUCTION: ... -->` comments within it. These comments are the authoritative reference for all output structures.

### 2. Analyze Requirements

- Read the provided spec/requirements carefully
- Identify goals, constraints, and acceptance criteria
- Note ambiguities or missing information
- **Ask clarifying questions** before proceeding if specs are unclear

### 3. Investigate Codebase

Use the **`unity-investigate-code`** skill:

```
Read and follow: .claude/skills/unity-investigate-code/SKILL.md
```

Focus on:
- Existing systems that will be affected
- Files that need modification
- Technical debt or constraints
- Reusable components
- Entry points and execution flows

### 4. Architecture Overview

Show the architectural change using simple before/after ASCII diagrams.

Rules:
- Keep diagrams simple and scannable (max 10-15 lines each)
- Use ASCII tree structure (`├──`, `└──`, `│`)
- Show data flow and object relationships
- Highlight the core structural change
- Include **OLD ARCHITECTURE**, **NEW ARCHITECTURE**, and **Key Benefits**

### 5. Technical Approach

Create a numbered list of implementation steps with `<code>` references. Structure defined in template.

### 6. Task Table

Break work into tasks grouped by epic. Structure and valid values defined in template.

### 7. Acceptance Criteria

Group criteria into categories (Functional, UI/UX, Edge Cases, Debug Verification). Structure defined in template.

### 8. Summary

After generating the HTML file, provide a verbal summary:
- Total estimated effort
- Key risks or blockers
- Dependencies between tasks
- Recommended implementation order

---

## Output Checklist

Before saving the file, verify:

- [ ] Read PLAN_OUTPUT.html template first
- [ ] Copied exact CSS from template
- [ ] All placeholders replaced with actual values
- [ ] Architecture overview has old/new diagrams + benefits
- [ ] Technical approach is numbered list with `<code>` tags
- [ ] Task table uses correct badge classes
- [ ] Acceptance criteria grouped correctly
- [ ] File saved to `Documents/Plans/[FeatureName]_PLAN.html`

---

## What This Skill Does NOT Do

- Write or modify actual code files
- Create or edit Unity assets
- Run implementations
- Execute tasks from the plan
- Generate code diffs or proposed code changes

This skill produces a **planning document** with architecture, tasks, and acceptance criteria only.
