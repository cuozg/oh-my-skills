---
name: prompt-improver
description: "AI Prompt Engineer for coding agents. Auto-rewrites vague, incomplete, or poorly structured user prompts into optimized, actionable prompts that maximize agent success. Scores prompts on 5 dimensions (Specificity, Context, Constraints, Success Criteria, Actionability), then produces an improved version with structured sections. Use when: (1) User prompt is vague or underspecified, (2) Task requires multiple steps but prompt lacks structure, (3) Prompt missing success criteria or constraints, (4) Delegating complex work to sub-agents, (5) Prompt lacks technical context needed for implementation, (6) User wants to maximize first-attempt success rate. Triggers: 'improve prompt', 'rewrite prompt', 'optimize prompt', 'prompt engineer', 'make this prompt better', 'refine this request', 'structure this task', 'enhance prompt', 'prompt quality', 'prompt score'."
---

# Prompt Improver

AI Prompt Engineer that transforms raw user requests into structured, high-quality prompts optimized for coding agent execution. Works for ANY coding agent — not limited to a specific framework or domain.

## Input

The skill accepts a single input: the **raw user prompt** to be improved. This can be:
- A vague one-liner ("fix the auth")
- A multi-paragraph but unstructured request
- A partially structured prompt that needs refinement
- A prompt being prepared for delegation to a sub-agent

## Output

The skill produces:
1. **Score Card** — 5-dimension rating of the original prompt
2. **Improved Prompt** — Restructured, enriched version ready for agent consumption
3. **Changes Summary** — What was added/changed and why

## Workflow

### Step 1: Score the Original Prompt

Rate the incoming prompt on 5 dimensions using a 1-3 scale:

| Dimension | 1 (Weak) | 2 (Adequate) | 3 (Strong) |
|---|---|---|---|
| **Specificity** | Vague intent, no details | Some details, gaps remain | Precise scope, named targets |
| **Context** | No background info | Partial context | Full tech stack, file paths, constraints |
| **Constraints** | No boundaries stated | Some limits mentioned | Clear boundaries, edge cases noted |
| **Success Criteria** | No definition of done | Implicit criteria | Explicit, verifiable outcomes |
| **Actionability** | Cannot start without questions | Can start with assumptions | Can execute immediately |

**Total score**: Sum of all 5 dimensions (range: 5-15)
- **5-8**: Critical rewrite needed — prompt will likely fail or produce wrong output
- **9-11**: Improvement recommended — agent can work but will make assumptions
- **12-15**: Minor polish only — prompt is already well-structured

### Step 2: Auto-Rewrite

**IMPORTANT**: Rewrite FIRST, present SECOND. Do NOT ask clarifying questions before producing the first improved version. The rewrite itself surfaces what's missing.

Apply these techniques in order:

1. **Extract Intent** — Identify what the user actually wants to achieve (not just what they said)
2. **Add Structure** — Organize into Goal / Context / Requirements / Constraints / Success Criteria sections
3. **Fill Gaps** — Infer reasonable defaults for missing information; mark assumptions with `[ASSUMED: ...]`
4. **Add Specificity** — Replace vague words ("improve", "fix", "update") with concrete actions
5. **Define Done** — Add explicit success criteria if missing
6. **Scope Boundaries** — Add what's NOT in scope to prevent scope creep

Use the improved prompt template:

```
## Goal
[1-2 sentences: what needs to be accomplished and why]

## Context
[Technical context: language, framework, file paths, current state]
[ASSUMED: any inferred context marked clearly]

## Requirements
1. [Specific, actionable requirement]
2. [Each requirement independently verifiable]
...

## Constraints
- [What NOT to change]
- [Performance/compatibility requirements]
- [Style/convention requirements]

## Success Criteria
- [ ] [Verifiable outcome 1]
- [ ] [Verifiable outcome 2]
...

## Out of Scope
- [Explicitly excluded items to prevent scope creep]
```

### Step 3: Present the Improved Prompt

Present the output in this format:

```
### Score Card (Original)
| Dimension | Score | Notes |
|---|---|---|
| Specificity | X/3 | [brief note] |
| Context | X/3 | [brief note] |
| Constraints | X/3 | [brief note] |
| Success Criteria | X/3 | [brief note] |
| Actionability | X/3 | [brief note] |
| **Total** | **X/15** | |

### Improved Prompt
[The rewritten prompt using the template above]

### Changes Made
- [What was added/changed and why, as bullet points]

### Assumptions Made
- [List any [ASSUMED: ...] items that the user should verify]
```

### Step 4: Refine (Optional)

If the user provides feedback or corrections:
1. Incorporate their feedback
2. Remove or update any incorrect `[ASSUMED: ...]` markers
3. Re-score if significant changes were made
4. Present the updated version

Repeat until the user is satisfied or explicitly accepts the prompt.

## Quick Reference: Techniques

| Technique | When to Use | Example Transform |
|---|---|---|
| Intent Extraction | Prompt says HOW not WHAT | "refactor the code" → "reduce coupling between AuthService and UserRepo to enable independent testing" |
| Gap Filling | Missing obvious context | "fix the bug" → "fix the null reference in UserController.GetProfile (line 42) when user has no avatar" |
| Constraint Injection | No boundaries stated | "update the API" → "update the API response format; maintain backward compatibility with v2 clients" |
| Success Criteria | No definition of done | "improve performance" → "reduce P95 latency from 800ms to <200ms on the /search endpoint" |
| Scope Bounding | Risk of scope creep | "clean up the codebase" → "remove dead code in src/utils/; do NOT refactor working implementations" |
| Assumption Marking | Must infer context | Mark with `[ASSUMED: using React 18]` so user can correct |

> **Full techniques catalog**: See `references/techniques.md` for 10 detailed technique categories with examples.

## Inline Examples

### Example 1: Vague Bug Fix

**Original** (Score: 6/15):
> "Fix the login bug"

**Improved**:
> ## Goal
> Fix the authentication failure that prevents users from logging in.
>
> ## Context
> [ASSUMED: Web application with form-based login]
> [ASSUMED: Bug is a recent regression — login worked previously]
>
> ## Requirements
> 1. Identify the root cause of login failures
> 2. Implement a fix that resolves the issue
> 3. Add or update tests covering the login flow
>
> ## Constraints
> - Do not change the login UI/UX
> - Maintain existing session management behavior
> - [ASSUMED: Do not modify database schema]
>
> ## Success Criteria
> - [ ] Users can log in with valid credentials
> - [ ] Invalid credentials show appropriate error message
> - [ ] Existing tests pass; new test covers the bug scenario
>
> ## Out of Scope
> - Registration flow changes
> - Password reset flow
> - OAuth/SSO integration

### Example 2: Feature Request

**Original** (Score: 7/15):
> "Add dark mode to the settings page"

**Improved**:
> ## Goal
> Add a dark mode toggle to the application settings that persists user preference and applies theme globally.
>
> ## Context
> [ASSUMED: Web application with CSS-based theming]
> [ASSUMED: Settings page already exists at a known route]
> [ASSUMED: No existing theme system — building from scratch]
>
> ## Requirements
> 1. Add a toggle switch in the Settings page under "Appearance" section
> 2. Implement dark theme CSS variables (background, text, borders, accents)
> 3. Apply theme globally across all pages when toggled
> 4. Persist preference in localStorage (or user profile if authenticated)
> 5. Respect OS-level prefers-color-scheme on first visit
>
> ## Constraints
> - Use CSS custom properties (variables) — no CSS-in-JS
> - Transition between themes must be smooth (no flash)
> - All existing components must remain readable in both themes
>
> ## Success Criteria
> - [ ] Toggle in Settings switches between light and dark themes
> - [ ] Preference persists across page reloads
> - [ ] All pages/components render correctly in both themes
> - [ ] First visit respects OS preference
> - [ ] No FOUC (flash of unstyled content) on page load
>
> ## Out of Scope
> - Custom theme builder / color picker
> - Per-page theme overrides
> - Theme scheduling (auto-switch by time of day)

> **More examples**: See `references/examples.md` for 8 before/after pairs covering APIs, refactoring, testing, deployment, and more.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | What to Do Instead |
|---|---|---|
| Asking questions before rewriting | Delays value; the rewrite itself reveals gaps | Rewrite first with `[ASSUMED]` markers, then let user correct |
| Over-specifying implementation | Constrains the agent's solution space | Specify WHAT and WHY, not HOW (unless implementation is critical) |
| Ignoring scope boundaries | Agent does too much or too little | Always include "Out of Scope" section |
| Generic success criteria | "It works" is not verifiable | Use specific, testable criteria: "P95 < 200ms", "all tests pass" |
| Removing user's original intent | Rewrite changes what they wanted | Preserve core intent; ADD structure and clarity around it |
| One-size-fits-all structure | Not every prompt needs all sections | Scale structure to prompt complexity — simple tasks need simple prompts |

## Adaptation by Target

Adjust emphasis based on what will consume the prompt:

| Target | Emphasize | De-emphasize |
|---|---|---|
| **Coding agent (general)** | File paths, success criteria, constraints | Background motivation |
| **Code review agent** | What to look for, severity levels, standards | Implementation details |
| **Planning agent** | Goals, dependencies, timeline | Code-level specifics |
| **Sub-agent delegation** | Complete context (no shared state), explicit skill loading | Conversational tone |
| **Human developer** | Motivation, acceptance criteria | Mechanical details they'd know |

## References

- `references/techniques.md` — Full catalog of 10 prompt engineering technique categories
- `references/examples.md` — 8 complete before/after prompt improvement examples
