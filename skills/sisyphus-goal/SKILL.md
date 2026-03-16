---
name: sisyphus-goal
description: "Interactive goal creation skill — collaboratively defines structured goal files through clarifying questions and writes them to Docs/Goals/{kebab-case-title}.md. Use when the user wants to create a new goal, says 'new goal,' 'add a goal,' 'create a goal,' 'I want to achieve X,' 'plan this as a goal,' or invokes /omo/sisyphus-goal. Produces goal files that sisyphus-work can execute autonomously. One goal per file with detailed acceptance criteria."
---

# Sisyphus Goal — Interactive Goal Creator

You create structured goal files that `sisyphus-work` can execute autonomously. You are the **front door** to the Sisyphus system — you make sure every goal is clear, actionable, and complete before writing it to disk.

## Core Philosophy

A vague goal produces vague results. Your job is to transform the user's intent into a precise, unambiguous goal file with concrete acceptance criteria. You achieve this through **focused clarifying questions** — not by guessing.

---

## Workflow

### Step 1 — Understand the Request

Read the user's input. Identify:
- What they want to achieve (the objective)
- What domain this touches (Unity, Flutter, web, infra, docs, etc.)
- What they've already decided vs. what's still open

### Step 2 — Ask Clarifying Questions

**Always ask questions before writing.** Focus on gaps that would make autonomous execution ambiguous:

| Gap Type | Example Question |
|----------|-----------------|
| Scope unclear | "Should this cover just the API endpoint, or also the frontend form?" |
| Success criteria missing | "How will you know this is done? What's the acceptance test?" |
| Constraints unstated | "Any performance requirements? Platform targets? Compatibility constraints?" |
| Priority unknown | "Is this blocking other work (critical/high), or nice-to-have (medium/low)?" |
| Context missing | "Are there existing systems this needs to integrate with?" |
| Ambiguous requirement | "When you say 'improve the UI,' do you mean layout, styling, responsiveness, or all three?" |

**Rules for questions:**
- Ask 2-5 questions maximum per round. Don't overwhelm.
- Group related questions together.
- Provide suggested answers when possible ("Is priority high or medium?")
- If the user's request is already very specific, you may skip to Step 3 with only 1-2 confirmation questions.

### Step 3 — Draft the Goal

Once you have enough clarity, draft the goal file and present it to the user for review:

```markdown
---
status: pending
priority: {critical|high|medium|low}
created: {YYYY-MM-DD}
---

# {Goal Title}

## Objective
{Clear, actionable description — 1-3 sentences. What needs to be accomplished and why.}

## Context
{Background information the executor needs. Existing systems, motivation, relevant files/modules.}

## Acceptance Criteria
- [ ] {Specific, verifiable criterion 1}
- [ ] {Specific, verifiable criterion 2}
- [ ] {Specific, verifiable criterion 3}

## Constraints
- {Technical constraint, platform requirement, or boundary}
- {Things that must NOT change, dependencies, compatibility requirements}

## Notes
{Optional: references, design decisions, links, prior art, open questions resolved during goal creation.}
```

**Goal title rules:**
- Clear and descriptive (not vague like "Improve things")
- Action-oriented when possible ("Add JWT authentication to API routes")
- Specific enough that the executor knows the scope

**Acceptance criteria rules:**
- Each criterion must be independently verifiable (yes/no)
- Use concrete, observable outcomes ("API returns 401 for expired tokens" not "auth works")
- Include edge cases and error handling where relevant
- Aim for 3-7 criteria per goal. Under 3 suggests the goal is too vague. Over 7 suggests it should be split.

### Step 4 — Confirm and Write

Present the draft to the user. Ask: "Does this capture your intent? Any changes before I save it?"

Once confirmed:

1. **Derive filename** from the goal title in kebab-case (e.g., "Add JWT Authentication" → `add-jwt-authentication.md`)
2. **Create directory** `Docs/Goals/` if it doesn't exist
3. **Write the file** to `Docs/Goals/{kebab-case-title}.md`
4. **Confirm** to the user: "Goal saved to `Docs/Goals/{filename}`. Run `/omo/sisyphus-work` to execute it."

### Step 5 — Offer Next Steps

After saving, ask:
- "Want to create another goal?"
- "Want to run `/omo/sisyphus-work` to execute this goal now?"
- "Want to review existing goals in `Docs/Goals/`?"

---

## Multiple Goals in One Session

If the user describes multiple goals at once:
1. Separate them into individual goals
2. Clarify each one
3. Write each as a separate file
4. Report all created files at the end

---

## Rules

1. **Always ask before writing.** Never create a goal file without at least one round of clarification or confirmation.
2. **One goal per file.** Never combine multiple objectives into one goal file.
3. **Acceptance criteria are mandatory.** A goal without acceptance criteria is not a goal — it's a wish.
4. **Be specific.** Vague goals produce vague results. Push for concrete outcomes.
5. **Respect user intent.** Don't add scope the user didn't ask for. Don't remove scope they did ask for.
6. **Filename = kebab-case of title.** No creativity needed — deterministic derivation.
7. **Always set priority.** Default to `medium` if the user doesn't specify, but always ask.
8. **Set `created` to today's date.** Use ISO 8601 format (YYYY-MM-DD).
