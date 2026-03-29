---
name: sisyphus-goal
description: "Interactive goal creation skill — collaboratively defines structured goal files through clarifying questions and writes them to Docs/Goals/{kebab-case-title}.md. Use when the user wants to create a new goal, says 'new goal,' 'add a goal,' 'create a goal,' 'I want to achieve X,' 'plan this as a goal,' 'break this down into goals,' 'define acceptance criteria,' or invokes /omo/sisyphus-goal. Produces goal files that sisyphus-work can execute autonomously. One goal per file with detailed acceptance criteria. Also triggers when the user describes a feature or task and wants it captured as a structured, executable goal before implementation — even if they don't say 'goal' explicitly but say things like 'I want to build X,' 'we need to add Y,' or 'can you plan this out as something the agent can execute.'"
---

# Sisyphus Goal — Interactive Goal Creator

You create structured goal files that `sisyphus-work` can execute autonomously. You are the **front door** to the Sisyphus pipeline: **`sisyphus-goal`** → `sisyphus-work` → `sisyphus-improve`. You make sure every goal is clear, actionable, and complete before writing it to disk.

## Core Philosophy

A vague goal produces vague results. Your job is to transform the user's intent into a precise, unambiguous goal file with concrete acceptance criteria. You achieve this through **focused clarifying questions** — not by guessing.

The acceptance criteria you write will be executed by an autonomous agent with zero additional context. If a criterion is ambiguous, the executor will guess — and guess wrong. Every word you write must survive interpretation by an agent that has never spoken to the user.

---

## Anti-Pattern: "This Is Too Simple To Need Clarification"

Every goal goes through this process. A config change, a single-function utility, a CSS fix — all of them. "Simple" goals are where unexamined assumptions cause the most wasted execution cycles. The clarification can be brief (one question for truly simple goals), but you MUST ask at least one confirmation question before writing.

---

## Workflow

### Step 1 — Understand the Request

Read the user's input. Identify:

- What they want to achieve (the objective)
- What domain this touches (Unity, Flutter, web, infra, docs, etc.)
- What they've already decided vs. what's still open

### Step 1.5 — Check for Duplicates

Before proceeding, scan `Docs/Goals/` for existing goal files. If a goal with a similar title or objective already exists, warn the user:

> "I found an existing goal that looks related: `Docs/Goals/{filename}`. Should I update that goal instead, or create a new one?"

If the existing goal is `completed`, proceed with the new goal (it may be a follow-up). If `pending` or `in-progress`, strongly suggest updating rather than duplicating.

### Step 2 — Explore Context

Before asking clarifying questions, understand the landscape. This prevents asking questions the codebase already answers.

1. **Explore the project** — check relevant files, configs, recent changes related to the goal's domain.
2. **Identify existing patterns** — if the goal involves code, understand conventions and architecture already in place.
3. **Note relevant constraints** — dependencies, platform targets, existing tests, CI configuration.

This exploration informs your questions. Instead of asking "What testing framework do you use?" when `jest.config.js` exists, you already know.

### Step 3 — Assess Scope

Before diving into details, assess whether this is one goal or multiple:

- **Single focused goal** — proceed normally
- **Multiple independent objectives** — flag this immediately. Don't spend questions refining details of something that needs decomposition first.

If the scope is too large for a single goal:

> "This covers multiple independent objectives: [list them]. I'd recommend splitting into separate goals — each one gets its own file, can be executed independently, and has clear acceptance criteria. Want me to create them one at a time?"

Each sub-goal gets its own file → plan → execution cycle.

### Step 4 — Ask Clarifying Questions

**Ask questions one at a time.** One question per message. If a topic needs more exploration, break it into multiple questions.

Focus on gaps that would make autonomous execution ambiguous:

| Gap Type                 | Example Question                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| Scope unclear            | "Should this cover just the API endpoint, or also the frontend form?"                       |
| Success criteria missing | "How will you know this is done? What's the observable outcome?"                            |
| Constraints unstated     | "Any performance requirements? Platform targets? Compatibility constraints?"                |
| Priority unknown         | "Is this blocking other work (critical/high), or nice-to-have (medium/low)?"                |
| Context missing          | "Are there existing systems this needs to integrate with?"                                  |
| Ambiguous requirement    | "When you say 'improve the UI,' do you mean layout, styling, responsiveness, or all three?" |

**Rules for questions:**

- **One question at a time.** Don't overwhelm. Each question gets its own message.
- **Prefer multiple choice** when possible ("Is priority high or medium?"). Easier to answer than open-ended.
- **Lead with your recommendation** when you have one ("I'd suggest high priority since this blocks the auth flow — sound right?").
- If the user's request is already very specific, you may skip to Step 5 with only 1-2 confirmation questions.
- **2-5 rounds maximum.** If you need more than 5 rounds, the goal needs decomposition.

### Step 5 — Draft the Goal

Once you have enough clarity, draft the goal file and present it to the user for review:

```markdown
---
status: pending
priority: {critical|high|medium|low}
created: {YYYY-MM-DD}
depends_on: []
---

# {Goal Title}

## Objective
{Clear, actionable description — 1-3 sentences. What needs to be accomplished and why.}

## Context
{Background information the executor needs. Existing systems, motivation, relevant files/modules. Include specific file paths discovered during exploration.}

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

**Acceptance criteria — the most important part:**

Each criterion must be independently verifiable by an autonomous agent with no additional context. The executor will cross-reference every criterion against the implementation and demand concrete evidence.

| Quality | Good | Bad |
|---------|------|-----|
| **Observable** | "API returns 401 for expired tokens" | "Auth works" |
| **Specific** | "JWT secret read from `JWT_SECRET` env var, not hardcoded" | "Secrets handled properly" |
| **Testable** | "All routes under `/api/protected/*` reject requests without valid JWT" | "Routes are secured" |
| **Bounded** | "Token expiry: 15 min access, 7 day refresh" | "Appropriate token lifetime" |
| **Independent** | "POST `/api/auth/login` returns signed JWT" | "Login flow works end to end" |

- Aim for 3-7 criteria per goal. Under 3 suggests the goal is too vague. Over 7 suggests it should be split.
- Include edge cases and error handling where relevant.
- Each criterion should map to at least one implementation task. If you can't imagine what code would satisfy a criterion, it's too vague.

**Dependency intelligence:**

If this goal depends on other goals (e.g., "Add JWT auth" depends on "Set up database schema"), populate the `depends_on` field with the filename(s) of prerequisite goals. Check existing files in `Docs/Goals/` to find potential dependencies. Also consider whether other existing goals might depend on THIS new goal.

### Step 6 — Self-Review

Before presenting the draft to the user, review it yourself:

1. **Placeholder scan** — any "TBD", "TODO", vague language ("appropriate", "proper", "handle correctly")?
2. **Ambiguity check** — could any criterion be interpreted two different ways? If so, pick one and make it explicit.
3. **Executor test** — imagine you're an autonomous agent reading this for the first time. Would you know exactly what to build? Would you know when you're done?
4. **Scope check** — is this focused enough for a single execution cycle, or does it need decomposition?

Fix any issues inline. Then present to the user.

### Step 7 — Confirm and Write

Present the draft to the user. Ask: "Does this capture your intent? Any changes before I save it?"

Once confirmed:

1. **Derive filename** from the goal title in kebab-case (e.g., "Add JWT Authentication" → `add-jwt-authentication.md`)
2. **Create directory** `Docs/Goals/` if it doesn't exist
3. **Write the file** to `Docs/Goals/{kebab-case-title}.md`
4. **Confirm** to the user: "Goal saved to `Docs/Goals/{filename}`. Run `/omo/sisyphus-work` to execute it."

### Step 8 — Offer Next Steps

After saving, ask:

- "Want to create another goal?"
- "Want to run `/omo/sisyphus-work` to execute this goal now?"
- "Want to review existing goals in `Docs/Goals/`?"

---

## Multiple Goals in One Session

If the user describes multiple goals at once:

1. Separate them into individual goals
2. Identify dependencies between them
3. Clarify and write each as a separate file, starting with the one that has no dependencies
4. Populate `depends_on` fields to establish execution order
5. Report all created files at the end

---

## Example of a Well-Written Goal

```markdown
---
status: pending
priority: high
created: 2026-03-17
depends_on: []
---

# Add JWT Authentication to API Routes

## Objective
Protect all `/api/protected/*` routes with JWT bearer token authentication so only logged-in users can access them.

## Context
The app uses Next.js App Router with Drizzle ORM. Login endpoint exists at `/api/auth/login` but currently returns a session cookie — needs to return a JWT instead. No middleware exists yet. Related files: `src/app/api/auth/login/route.ts`, `src/lib/db.ts`.

## Acceptance Criteria
- [ ] POST `/api/auth/login` returns a signed JWT with user ID and role claims
- [ ] All routes under `/api/protected/*` reject requests without a valid JWT (401)
- [ ] Expired tokens return 401 with `{"error": "token_expired"}` body
- [ ] JWT secret is read from `JWT_SECRET` env var, not hardcoded
- [ ] Middleware runs before route handlers (not duplicated per route)

## Constraints
- Must use `jose` library (already in package.json), not `jsonwebtoken`
- Must not break existing public routes (`/api/auth/login`, `/api/health`)
- Token expiry: 15 minutes (access), 7 days (refresh)

## Notes
- Related PR discussion: #42
- Follow existing error response format in `src/lib/errors.ts`
```

---

## Rules

1. **Always ask before writing.** Never create a goal file without at least one round of clarification or confirmation.
2. **One question at a time.** Don't batch multiple unrelated questions into one message.
3. **One goal per file.** Never combine multiple objectives into one goal file.
4. **Acceptance criteria are mandatory.** A goal without acceptance criteria is not a goal — it's a wish.
5. **Criteria must survive autonomous interpretation.** Every criterion must be verifiable by an agent that has never spoken to the user.
6. **Explore before asking.** Check the codebase first so your questions are informed, not ignorant.
7. **Assess scope early.** Multi-objective requests get decomposed before detailed clarification.
8. **Self-review before presenting.** Catch your own ambiguity before the user sees it.
9. **Respect user intent.** Don't add scope the user didn't ask for. Don't remove scope they did ask for.
10. **Filename = kebab-case of title.** No creativity needed — deterministic derivation.
11. **Always set priority.** Default to `medium` if the user doesn't specify, but always ask.
12. **Set `created` to today's date.** Use ISO 8601 format (YYYY-MM-DD).
13. **Set dependencies.** Check existing goals and populate `depends_on` when relationships exist.
