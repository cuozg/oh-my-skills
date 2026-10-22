---
name: writing-prompt
description: Use when the user asks to write, draft, build, create, or refine a prompt, system prompt, or agent instructions for an LLM, or asks to change or update an existing prompt doc under Docs/Prompts.
---

# writing-prompt

Grill the user until the prompt's intent is fully settled, then build the prompt with prompt-engineering structure and write it to `<git root>/Docs/Prompts/<kebab-title>.md`.

## Mode

- Request for a new prompt → Steps 1-4.
- Request to change or update a prompt that already exists under `Docs/Prompts/` → Update mode (bottom).

## Step 1. Grill

**REQUIRED SUB-SKILL:** Use `grilling`. **Q1 of the first round is always Consumer.**

The grill is finished only when every row below is settled by an answer or by an explicit "not needed":

| # | Dimension | What it decides |
|---|-----------|-----------------|
| 1 | Consumer | Claude Code agent session, API system prompt, or other LLM. Picks the template variant |
| 2 | Goal | One sentence: what the output must achieve |
| 3 | Inputs | What is injected at run time, and how it arrives |
| 4 | Constraints | Rules, limits, forbidden actions |
| 5 | Process | Steps the model follows |
| 6 | Output format | Exact shape, length, fields |
| 7 | Examples | How many, which case |
| 8 | Success criteria | How the user judges a good output |
| 9 | Out of scope | What the prompt must not attempt |
| 10 | Title | Say in round 1 that Title comes last; propose a kebab-case slug in the final round; user confirms |

Add a question outside the table when a row cannot be settled without it (e.g. owner source when the repo has no CODEOWNERS). When the user says "go with recommended", adopt the ➡️ answer and record it under Design Notes → Assumptions.

Facts about the codebase (paths, class names, existing docs, conventions) are your job: dispatch an Explore subagent in parallel with the first round. If no subagent tool is available, explore directly with Grep/Glob/Read and say so in one line. Ask the user for decisions only.

## Step 2. Build the prompt

Sections in this fixed order. A section is dropped only when its checklist row was settled as "not needed"; never leave a placeholder.

`Role → Context → Task → Inputs → Constraints → Process → Output Format → Examples → Success Criteria → Out of Scope`

Prompt-engineering conventions:
- Direct, imperative instructions. State what to do; prohibitions only for real safety or scope rules.
- Runtime-injected content is wrapped in XML tags (`<crash_report>…</crash_report>`), and the prompt refers to those tag names. An empty tag pair in Inputs showing where content lands is allowed; `TBD` or `<fill in>` text is not.
- Each example sits in `<example>` tags and matches Output Format exactly.
- Success Criteria are checkable by the model itself before it answers.
- Consumer = Claude Code agent: Process names the tools to use and ends with a verification step. Every path cited, including inside examples, comes from the explorer; when no matching file exists, write "not found in repo" instead of inventing a path.
- Consumer = API system prompt: Role comes first, no tool talk, Output Format strict enough to parse.

## Step 3. Write the doc

Path: `<git root of cwd>/Docs/Prompts/<kebab-title>.md`. Create the folder if missing. Write directly; no approval gate. If the file exists, switch to Update mode.

Doc layout (all slots REQUIRED). The prompt fence uses four backticks so that three-backtick blocks inside the prompt do not break it.

`````markdown
---
title: <Title Case>
date: <YYYY-MM-DD from `date`>
consumer: <claude-code-agent | api-system-prompt | other-llm>
version: 1
intent: <one line, the Goal row>
---

# <Title Case>

## Prompt

````markdown
<the full prompt, sections from Step 2>
````

## Design Notes

- **Decisions (v1, YYYY-MM-DD)**: one bullet per grill answer that shaped the prompt.
- **Assumptions**: anything you filled in without an explicit answer.
- **Open questions**: what the user deferred, or "none".
`````

## Step 4. Self-review

Run these 5 checks on the written file, fix in place:

1. Every checklist row is reflected in the prompt or listed as dropped in Design Notes.
2. Sections appear in the Step 2 order.
3. Each example matches Output Format exactly.
4. Injected inputs use XML tags; the prompt refers to them by tag name.
5. No placeholder text, no TBD.

Reply with the file path and one line: `Self-review: <n>/5 checks passed, fixed <what or none>.` Do not paste the prompt into chat.

## Update mode

Trigger: the user asks to change, update, or fix an existing `Docs/Prompts/*.md`.

1. Read the existing doc first.
2. Grill only the rows the change touches; skip the full round. Skip the explorer when the change needs no new codebase facts.
3. Edit the prompt in place, keeping the section order. Also update any Process step, Example, or Success Criteria bullet that refers to the changed section; touch nothing else.
4. Bump `version`, update `date`, append one bullet `**Decisions (vN, YYYY-MM-DD)**: <change>` to Design Notes; keep earlier bullets as they are.
5. Run Step 4.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| First question is about data plumbing | Q1 is Consumer; it drives the whole template |
| Interview covers inputs, output, and save path, then stops | Rows 7-10 (examples, success criteria, out of scope, title) must be settled too |
| Asking the user where to save or which docs exist | Those are facts; the explorer finds them |
| File is the raw prompt | Frontmatter + fenced prompt + Design Notes, always |
| Role is an unlabeled opening paragraph | `## Role` is the first section |
| Out of scope folded into Constraints | Separate `## Out of Scope` section |
| Example cites a path that is not in the repo | Use explorer facts or write "not found in repo" |
| Three-backtick block inside a three-backtick prompt fence | Prompt fence is four backticks |
| Pasting the whole prompt back into chat | Path + self-review line only |
