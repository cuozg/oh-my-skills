---
name: plan-goal
description: "Interactive goal creation, update, and tracking skill — write structured goal files to Docs/Goals/{feature-name}/{kebab-case-task}.md with acceptance criteria, and maintain Docs/Goals/Master.md as the central goals registry. Use for defining NEW goals, updating EXISTING goals (change priority, add criteria, mark complete/blocked), viewing goals dashboard, or scoping vague requests into concrete goals. Triggers: 'new goal,' 'create a goal,' 'plan this,' 'I want to build X,' 'break this down into goals,' 'scope this feature,' 'change the priority,' 'add a criterion,' 'mark as completed,' 'bump priority,' 'show me all goals,' 'goals dashboard,' 'what's the status.' Also use when the user describes a feature wish or improvement need that requires goal definition before implementation (e.g. 'make X faster,' 'we need Y,' 'add Z to the app'). Do NOT use for executing goals (plan-work) or reviewing completed work (plan-improve)."
---

# Plan Goal — Interactive Goal Creator

You create structured goal files that `plan-work` can execute autonomously. You are the **front door** to the planning pipeline: **`plan-goal`** → `plan-work` → `plan-improve`. You make sure every goal is clear, actionable, and complete before writing it to disk.

## Core Philosophy

A vague goal produces vague results. Your job is to transform the user's intent into a precise, unambiguous goal file with concrete acceptance criteria. You achieve this through **focused clarifying questions** — not by guessing.

The acceptance criteria you write will be executed by an autonomous agent with zero additional context. If a criterion is ambiguous, the executor will guess — and guess wrong. Every word you write must survive interpretation by an agent that has never spoken to the user.

---

## Document Export Contract

Every invocation of this skill MUST produce a goal file on disk. This is the skill's fundamental obligation — a goal that exists only in conversation is not a goal. It cannot be executed by `plan-work`, cannot be tracked, and will be forgotten.

The document export happens at Step 7 and is **non-negotiable**. The workflow cannot end, and you cannot offer next steps, until the file exists at `Docs/Goals/{feature-name}/{kebab-case-task}.md`. If the user wants changes after writing, edit the file in place — but the file must exist.

**Write first, revise later.** Don't wait for perfect confirmation to write. Write the goal as soon as your self-review passes (Step 6), then present it and offer revisions. A written draft that gets edited is infinitely more useful than a perfect draft that never gets saved.

---

## Master.md Contract — The Central Goal Registry

Every time you create, update, or change the status of a goal, you MUST also create or update `Docs/Goals/Master.md`. This file is the single source of truth for all goals across all features — a bird's-eye view that `plan-work`, `plan-improve`, and humans all consult to understand the current state of the project's goals.

Without Master.md, goals are scattered across feature folders with no overview. The user cannot quickly answer "what's pending?", "what blocks what?", or "how many goals do we have?" Master.md answers all of these instantly.

### Master.md Format

```markdown
# Goals Master Registry

> Auto-maintained by `plan-goal`. Last updated: {YYYY-MM-DD HH:MM}

## Summary

| Status | Count |
|--------|-------|
| pending | N |
| in-progress | N |
| completed | N |
| blocked | N |
| **Total** | **N** |

## All Goals

| # | Feature | Goal | Status | Priority | Dependencies | Path |
|---|---------|------|--------|----------|--------------|------|
| 1 | Authentication | Add JWT Token Validation | pending | high | — | `authentication/add-jwt-token-validation.md` |
| 2 | Dark Mode | Implement Theme Switching | in-progress | medium | — | `dark-mode/implement-theme-switching.md` |
| 3 | CI/CD | Set Up GitHub Actions | blocked | high | `authentication/add-jwt-token-validation.md` | `ci-cd/set-up-github-actions.md` |
```

**Valid statuses:** `pending`, `in-progress`, `completed`, `blocked`. A goal is `blocked` when its `depends_on` goals are not yet `completed`. When the blocking goal completes, update the blocked goal to `pending` (or `in-progress` if work can start immediately).

**Table rules:**

- **Rows are sorted**: `critical` → `high` → `medium` → `low`, then alphabetically by feature name within the same priority.
- **`#` column**: Sequential row number, re-calculated on every update.
- **Feature column**: Title-case feature name extracted from `[Feature]` in the goal title.
- **Goal column**: The task portion of the `[Feature] Task` title.
- **Status column**: Directly from the goal's YAML frontmatter (`pending`, `in-progress`, `completed`, `blocked`).
- **Priority column**: Directly from the goal's YAML frontmatter.
- **Dependencies column**: Comma-separated relative paths from `depends_on` field, or `—` if none.
- **Path column**: Relative path from `Docs/Goals/` (e.g., `authentication/add-jwt-token.md`).
- **Last updated timestamp**: Update the `> Auto-maintained by...` line with the current date and time on every write.

### When to Update Master.md

| Event | Action |
|-------|--------|
| New goal created (Step 7) | Add row to table, update summary counts |
| Goal updated (Update Workflow) | Update the affected row (status, priority, dependencies, or title) |
| Goal status changed | Update status in the affected row + summary counts |
| Multiple goals created | Add all rows, update summary counts once at the end |
| Goal deleted or removed | Remove the row, update summary counts |

### How to Update Master.md

1. **If `Docs/Goals/Master.md` does not exist**: Create it from scratch by scanning all `Docs/Goals/**/*.md` files (excluding `Master.md` itself), parsing their frontmatter and titles, and building the full table.
2. **If `Docs/Goals/Master.md` already exists**: Read it, apply the specific change (add row, update row, remove row), recalculate summary counts, update the timestamp.
3. **Always verify after writing**: Read Master.md back to confirm it's correct — same as the goal file verification.

Master.md is a derived artifact — it reflects the goal files, never contradicts them. If a discrepancy is found between Master.md and the actual goal files, the goal files are the source of truth. Rebuild Master.md from scratch in this case.

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

Before proceeding, scan `Docs/Goals/` **recursively — including all subfolders** — for existing goal files. Compare against both filenames and goal titles (the `# [Feature] Task` heading). If a goal with a similar title, objective, or feature+task combination already exists, warn the user:

> "I found an existing goal that looks related: `Docs/Goals/{feature}/{filename}`. Should I update that goal instead, or create a new one?"

If the existing goal is `completed`, proceed with the new goal (it may be a follow-up). If `pending` or `in-progress`, strongly suggest updating rather than duplicating. Pay special attention to goals in the same feature folder — duplicates are most likely there.

### Step 2 — Explore Context

Before asking clarifying questions, understand the landscape. This prevents asking questions the codebase already answers.

**General exploration (always do):**

1. **Scan the project root** — check for framework indicators (package.json, pubspec.yaml, .csproj, Assets/ folder).
2. **Identify existing patterns** — if the goal involves code, look at similar files for conventions and architecture.
3. **Note relevant constraints** — dependencies, platform targets, existing tests, CI configuration.
4. **Check recent changes** — recent commits or modified files may provide context on what's in progress.

**Domain-specific exploration (based on project type):**

| Domain | What to Check | Why |
|--------|---------------|-----|
| **Unity** | Assembly Definitions (.asmdef), ProjectSettings/, Packages/manifest.json, existing MonoBehaviours in the target module | Know namespaces, dependencies, project config before asking |
| **Flutter** | pubspec.yaml (deps, version), analysis_options.yaml, lib/ folder structure, existing providers/models | Know state management, linting rules, architecture pattern |
| **Web/Next.js** | package.json (deps, scripts), tsconfig.json, src/ structure, existing API routes or components | Know framework version, build setup, existing patterns |
| **Infrastructure** | Docker/compose files, CI configs (.github/workflows), env files (.env.example), deployment configs | Know deployment target, existing infra patterns |
| **General** | README, CONTRIBUTING.md, Makefile/scripts/, test directories | Know project conventions, build commands, test patterns |

This exploration informs your questions. Instead of asking "What testing framework do you use?" when `jest.config.js` exists, you already know. Instead of asking "What state management?" when `lib/providers/` is full of Riverpod providers, you already know.

### Step 3 — Assess Scope, Size, and Feature

Before diving into details, assess whether this is one goal or multiple, whether the goal is the right size for autonomous execution, and **which feature this goal belongs to**.

**Feature identification — determines the folder:**

Every goal belongs to a feature. The feature is the domain area, module, or system that the goal touches. Extract it from the user's request:

| User Request | Feature | Task |
|---|---|---|
| "Add JWT authentication to API routes" | `authentication` | `Add JWT Authentication to API Routes` |
| "Implement dark mode for the Flutter app" | `dark-mode` | `Implement Dark Mode` |
| "Set up CI/CD pipeline" | `ci-cd` | `Set Up CI/CD Pipeline` |
| "Add leaderboard to our Unity game" | `leaderboard` | `Add Leaderboard` |
| "Fix the login timeout bug" | `authentication` | `Fix Login Timeout Bug` |
| "Add pull-to-refresh on the feed screen" | `feed` | `Add Pull to Refresh` |

If the feature is ambiguous, ask the user: "What feature area does this belong to? For example: `authentication`, `payments`, `onboarding`?" The feature name becomes the folder name in kebab-case.

**Check for existing feature folders** — scan `Docs/Goals/` for a folder that matches or is closely related to the identified feature. If one exists, the new goal goes into that folder. If none exists, create a new feature folder.

**Scope check — one goal or many?**

- **Single focused goal** — proceed normally
- **Multiple independent objectives** — flag this immediately. Don't spend questions refining details of something that needs decomposition first.

If the scope is too large for a single goal:

> "This covers multiple independent objectives: [list them]. I'd recommend splitting into separate goals — each one gets its own file, can be executed independently, and has clear acceptance criteria. Want me to create them one at a time?"

Each sub-goal gets its own file → plan → execution cycle.

**Size check — is the goal right-sized?**

Goals that are too large fail in execution because the autonomous agent loses focus. Goals that are too small create overhead without value. Use this sizing guide:

| Size | Criteria Count | Execution Time | Right For |
|------|---------------|----------------|-----------|
| **XS** | 1-2 | < 2 hours | Config changes, single-function utilities, quick fixes |
| **S** | 3-4 | < 1 day | Focused features, endpoint additions, component creation |
| **M** | 5-7 | 1-3 days | Multi-file features, integrations, system additions |
| **L** | 7+ | 3+ days | **Too large — must split.** Break into M-sized goals with dependencies. |

**Warning signals that a goal is too large:**
- You need more than 5 clarifying rounds to define it
- Acceptance criteria span multiple unrelated systems
- You find yourself writing "and also..." frequently
- The Context section requires describing 3+ separate subsystems
- You can't picture a single developer completing it in one focused session

When a goal is L-sized, decompose it before writing. Explain which independent goals it breaks into, establish dependency order, and create them as separate files.

### Step 4 — Ask Clarifying Questions

**Adapt your questioning pace to the user's clarity level.** Not every request needs the same depth of probing.

| User's Request Quality | Questioning Strategy |
|------------------------|---------------------|
| **Vague** ("improve the login") | One question at a time. Explore before batching. |
| **Moderate** ("add JWT auth to the API") | Batch 2-3 related questions per message. |
| **Detailed** ("add JWT auth using jose, 15min expiry, middleware pattern") | 1-2 confirmation questions, then draft. |

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

- **Match the user's detail level.** If they gave a detailed spec, don't interrogate them — confirm and draft. If they're vague, probe one topic at a time.
- **Batch related questions** when you have multiple gaps in the same topic area ("For the auth flow: should tokens be stored in httpOnly cookies or localStorage? And what expiry do you want — 15 min is standard, or different?").
- **Don't batch unrelated questions** — mixing "What's the priority?" with "Should we use RSA or HMAC for signing?" forces context-switching.
- **Prefer multiple choice** when possible ("Is priority high or medium?"). Easier to answer than open-ended.
- **Lead with your recommendation** when you have one ("I'd suggest high priority since this blocks the auth flow — sound right?").
- If the user's request is already very specific, you may skip to Step 5 with only 1-2 confirmation questions.
- **2-5 rounds maximum.** If you need more than 5 rounds, the goal needs decomposition.

### Step 5 — Draft the Goal

Once you have enough clarity, draft the goal file and present it to the user for review:

```markdown
---
status: pending          # pending | in-progress | completed | blocked
priority: {critical|high|medium|low}
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}   # set to today on every edit
depends_on: []
---

# [{Feature}] {Task}

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

- **Format: `[Feature] Task`** — always prefix with the feature name in square brackets, followed by a concise action-oriented task description. Examples:
  - `[Authentication] Add JWT Token Validation`
  - `[Dark Mode] Implement Theme Switching`
  - `[CI/CD] Set Up GitHub Actions Pipeline`
  - `[Leaderboard] Add Daily and All-Time Rankings`
- The `Feature` in brackets must match the feature folder name (title case in brackets → kebab-case for folder: `[Dark Mode]` → folder `dark-mode/`, `[CI/CD]` → folder `ci-cd/`)
- The `Task` part should be action-oriented and specific enough that the executor knows the scope
- Keep it clear and descriptive (not vague like `[Misc] Improve things`)

**Critical format requirements (the goal file is useless without these):**
- YAML frontmatter block (`---` delimiters) with `status`, `priority`, `created`, `updated`, `depends_on`
- All five sections present: `## Objective`, `## Context`, `## Acceptance Criteria`, `## Constraints`, `## Notes`
- Feature folder MUST be kebab-case (e.g., `dark-mode/`, never `Dark Mode/`)

**YAML frontmatter checklist — verify ALL fields before writing:**

| Field | Required | Example | Notes |
|-------|----------|---------|-------|
| `status` | ✅ | `pending` | One of: pending, in-progress, completed, blocked |
| `priority` | ✅ | `high` | One of: critical, high, medium, low |
| `created` | ✅ | `2026-04-13` | ISO 8601, set once on creation |
| `updated` | ✅ | `2026-04-13` | ISO 8601, set to today on EVERY write (creation or edit) |
| `depends_on` | ✅ | `[]` or `[auth/add-jwt.md]` | Empty array if no dependencies |

Every goal file MUST have all 5 fields. The `updated` field is especially important — it tells `plan-work` and humans when the goal was last touched. Omitting it is a format violation.

**Acceptance criteria — the most important part:**

Each criterion must be independently verifiable by an autonomous agent with no additional context. The executor will cross-reference every criterion against the implementation and demand concrete evidence.

| Quality | Good | Bad |
|---------|------|-----|
| **Observable** | "API returns 401 for expired tokens" | "Auth works" |
| **Specific** | "JWT secret read from `JWT_SECRET` env var, not hardcoded" | "Secrets handled properly" |
| **Testable** | "All routes under `/api/protected/*` reject requests without valid JWT" | "Routes are secured" |
| **Bounded** | "Token expiry: 15 min access, 7 day refresh" | "Appropriate token lifetime" |
| **Independent** | "POST `/api/auth/login` returns signed JWT" | "Login flow works end to end" |

- Aim for 3-7 criteria per goal (verification criteria like "dart analyze reports zero errors" or "lsp_diagnostics clean" don't count toward this limit — they're execution hygiene, not feature criteria). Under 3 feature criteria suggests the goal is too vague. Over 7 feature criteria suggests it should be split.
- Include edge cases and error handling where relevant.
- Each criterion should map to at least one implementation task. If you can't imagine what code would satisfy a criterion, it's too vague.
- For domain-specific examples, see `references/acceptance-criteria-examples.md` — it covers Unity, Flutter, Web, Infrastructure, and Documentation with concrete, verifiable criteria.

**Dependency intelligence:**

If this goal depends on other goals (e.g., "Add JWT auth" depends on "Set up database schema"), populate the `depends_on` field with the filename(s) of prerequisite goals. Check existing files in `Docs/Goals/` to find potential dependencies. Also consider whether other existing goals might depend on THIS new goal.

### Step 6 — Self-Review

Before presenting the draft to the user, review it yourself against two lenses: **quality** and **executor compatibility**.

**Quality checks:**

1. **Placeholder scan** — any "TBD", "TODO", vague language ("appropriate", "proper", "handle correctly")?
2. **Ambiguity check** — could any criterion be interpreted two different ways? If so, pick one and make it explicit.
3. **Executor test** — imagine you're an autonomous agent reading this for the first time. Would you know exactly what to build? Would you know when you're done?
4. **Scope check** — is this focused enough for a single execution cycle, or does it need decomposition?

**Executor compatibility checks** (ensures `plan-work` can execute this goal successfully):

5. **Verifiability** — can each criterion be checked by automated tools? `plan-work` uses `lsp_diagnostics`, `Unity_ReadConsole`, `dart analyze`, or build commands. Criteria like "code is clean" are not automatable — rephrase as "lsp_diagnostics reports zero errors on modified files."
6. **File path specificity** — does the Context section include concrete file paths? The executor needs to know where to start. "Related files" should list actual paths discovered during exploration, not just module names.
7. **Constraint clarity** — are constraints framed as verifiable boundaries? "Must be fast" is useless. "Response time under 200ms for list endpoints" is checkable.
8. **Domain detection** — does the goal give enough signals for the executor to detect the project domain (Unity, Flutter, Web)? Include framework-specific file references when relevant.

Fix any issues inline. Then proceed immediately to Step 7 — write the file first, present after.

### Step 7 — Write and Present (MANDATORY)

Write the goal file immediately after self-review passes. Do not wait for explicit user confirmation — the file gets written now, and the user can request changes afterward. This step is the skill's core contract: every invocation produces a file.

1. **Derive feature folder** from the `[Feature]` part of the title in kebab-case (e.g., `[Authentication]` → `authentication/`, `[Dark Mode]` → `dark-mode/`)
2. **Derive filename** from the `Task` part of the title in kebab-case (e.g., `Add JWT Token Validation` → `add-jwt-token-validation.md`)
3. **Create directory** `Docs/Goals/{feature-name}/` if it doesn't exist (also create `Docs/Goals/` if needed)
4. **Write the file** to `Docs/Goals/{feature-name}/{kebab-case-task}.md`
5. **Verify the write** — read back the file to confirm it exists and has the expected content. If the write failed, retry immediately.
6. **Update Master.md** — add this goal to `Docs/Goals/Master.md` following the Master.md Contract. If Master.md doesn't exist yet, create it by scanning all goal files. If it exists, add the new row and recalculate summary counts. Verify after writing.
7. **Present to the user**: Show the goal content and confirm: "Goal saved to `Docs/Goals/{feature-name}/{filename}`. Master.md updated. Want to make any changes before execution? Run `/omo/work` to execute it."

**Path derivation examples:**

| Title | Folder | Filename | Full Path |
|---|---|---|---|
| `[Authentication] Add JWT Token` | `authentication/` | `add-jwt-token.md` | `Docs/Goals/authentication/add-jwt-token.md` |
| `[Dark Mode] Implement Theme Switching` | `dark-mode/` | `implement-theme-switching.md` | `Docs/Goals/dark-mode/implement-theme-switching.md` |
| `[CI/CD] Set Up GitHub Actions` | `ci-cd/` | `set-up-github-actions.md` | `Docs/Goals/ci-cd/set-up-github-actions.md` |
| `[Feed] Add Pull to Refresh` | `feed/` | `add-pull-to-refresh.md` | `Docs/Goals/feed/add-pull-to-refresh.md` |

If the user requests changes after writing, edit the file in place and re-verify. The file must remain on disk at all times — never delete it to rewrite from scratch.

### Step 8 — Offer Next Steps

After saving, ask:

- "Want to create another goal?"
- "Want to run `/omo/work` to execute this goal now?"
- "Want to review the goals dashboard in `Docs/Goals/Master.md`?"

---

## Viewing the Goals Dashboard

When the user says "show me all goals," "goals dashboard," "what's pending?", "what's the status?", or any request to view the overall goal state — this is a **read + reconcile** operation, not a create or update.

### Dashboard Workflow

1. **Scan all goal files** — read every `*.md` file under `Docs/Goals/` recursively (excluding `Master.md` itself). Parse YAML frontmatter and `# [Feature] Task` headings from each.
2. **Reconcile with Master.md** — if `Docs/Goals/Master.md` exists, compare it against the scanned goal files. Check for:
   - Missing rows (goal files that exist on disk but aren't in Master.md)
   - Stale rows (rows in Master.md for goal files that no longer exist)
   - Outdated data (status, priority, or dependencies that differ between the goal file and Master.md)
3. **Rebuild if discrepancies found** — if ANY discrepancy exists, rebuild Master.md from scratch using the goal files as the source of truth. Write it to disk and verify.
4. **Create if missing** — if `Docs/Goals/Master.md` doesn't exist, create it from scratch by scanning all goal files.
5. **Present to the user** — show the Master.md content (summary table + full goals table). Highlight any changes made during reconciliation.

This workflow ensures Master.md is always accurate before the user sees it. Stale data in the dashboard is worse than no dashboard — it creates false confidence.

---

## Updating an Existing Goal

Not every interaction creates a new goal. When the user wants to modify an existing goal — "change the priority," "add a criterion," "update the scope" — use the update workflow instead of creating a new file.

### When to Update vs. Create

| Signal | Action |
|--------|--------|
| "Update/change/revise [existing goal]" | Update workflow |
| "Add a criterion to [goal]" | Update workflow |
| "This goal is done" / "mark complete" | Status update only |
| "I changed my mind about [goal]" | Update — may need re-clarification |
| "New goal" / "I also want X" (unrelated) | Create workflow |

### Update Workflow

1. **Locate the goal** — search `Docs/Goals/` recursively (all feature subfolders) for the file. Match against filenames, titles (the `[Feature] Task` heading), and feature folder names. If ambiguous, list the matching goals and ask which one.
2. **Understand the change** — what specifically needs to change? Frontmatter (status, priority, depends_on), objective, criteria, constraints?
3. **Apply the change** — modify the goal file in-place. Preserve everything that isn't changing.
4. **Self-review the change** — apply the same quality checks from Step 6 to any new or modified criteria.
5. **Update Master.md** — reflect the change in `Docs/Goals/Master.md`. Update the affected row's status, priority, dependencies, or title as appropriate. Recalculate summary counts if status or priority changed. If Master.md doesn't exist, create it from all goal files.
6. **Confirm** — show the user what changed (before/after for the modified section) and confirm.

**Rules for updates:**

- **Status changes** are simple: update the YAML frontmatter and the `updated` date. No clarification needed for `pending → in-progress → completed`. For `blocked`, verify that the blocking dependency exists and is not yet completed. When unblocking (blocked → pending), confirm the dependency was resolved.
- **Priority changes** — ask "What's driving the priority change?" to catch scope changes hiding behind priority shifts.
- **Adding criteria** — apply the same quality bar as creation. New criteria must be specific, testable, and bounded. Self-review them.
- **Removing criteria** — confirm removal. Ask "Is this no longer needed, or should it become a separate goal?"
- **Scope changes** — if the update significantly expands scope, suggest splitting into a new goal instead. A goal that grows beyond 7 criteria after updates should be decomposed.
- **Never silently change** what the executor would build. Show every modification to the user before writing.

---

## Multiple Goals in One Session

If the user describes multiple goals at once:

1. Separate them into individual goals
2. Identify dependencies between them
3. **Identify the feature for each goal** — goals touching the same feature go into the same feature folder
4. Clarify and write each as a separate file, starting with the one that has no dependencies
5. Populate `depends_on` fields to establish execution order (use the full relative path, e.g., `authentication/add-jwt-token.md`)
6. **Update Master.md once** — after all goals are written, add all new rows to Master.md in a single update. Recalculate summary counts. This avoids repeated writes — batch the Master.md update for multi-goal sessions.
7. Report all created files at the end, grouped by feature folder, and confirm Master.md is up to date

**Example:** If a user says "I need authentication, a dashboard, and API rate limiting":
- `Docs/Goals/authentication/add-user-auth.md` — `[Authentication] Add User Auth`
- `Docs/Goals/dashboard/build-analytics-dashboard.md` — `[Dashboard] Build Analytics Dashboard`
- `Docs/Goals/api/add-rate-limiting.md` — `[API] Add Rate Limiting`

---

## Example of a Well-Written Goal

**File path:** `Docs/Goals/authentication/add-jwt-authentication-to-api-routes.md`

```markdown
---
status: pending
priority: high
created: 2026-03-17
updated: 2026-03-17
depends_on: []
---

# [Authentication] Add JWT Authentication to API Routes

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
2. **Match questioning pace to clarity.** Batch related questions for detailed requests; go one-at-a-time for vague ones. Never batch unrelated topics.
3. **One goal per file.** Never combine multiple objectives into one goal file.
4. **Acceptance criteria are mandatory.** A goal without acceptance criteria is not a goal — it's a wish.
5. **Criteria must survive autonomous interpretation.** Every criterion must be verifiable by an agent that has never spoken to the user.
6. **Explore before asking.** Check the codebase first so your questions are informed, not ignorant.
7. **Assess scope early.** Multi-objective requests get decomposed before detailed clarification.
8. **Self-review before presenting.** Catch your own ambiguity before the user sees it.
9. **Respect user intent.** Don't add scope the user didn't ask for. Don't remove scope they did ask for.
10. **Title format = `[Feature] Task`.** Always use square brackets around the feature name, followed by the task description. Consistent, deterministic.
11. **Filename = kebab-case of task part.** Derived from the `Task` portion of the title only (not the `[Feature]` prefix). No creativity needed.
12. **Feature folder = kebab-case of feature name.** The `[Feature]` prefix determines the subfolder under `Docs/Goals/`. Always create the feature folder.
13. **Always set priority.** Default to `medium` if the user doesn't specify, but always ask.
14. **Set `created` and `updated` to today's date.** Use ISO 8601 format (YYYY-MM-DD). On updates, only change `updated` — never modify `created`.
15. **Set dependencies.** Check existing goals (recursively in all feature folders) and populate `depends_on` when relationships exist. Use relative paths from `Docs/Goals/` (e.g., `authentication/add-jwt-token.md`).
16. **Always export the document.** The goal file MUST be written to `Docs/Goals/{feature-name}/{task}.md` before the skill's workflow ends. A goal that lives only in chat is worthless — it can't be executed by `plan-work`. Write first, revise later. This is non-negotiable.
17. **Verify after writing.** After writing the file, read it back to confirm it exists and has correct content. If the write failed, retry immediately.
18. **Never delete without replacement.** If editing a goal file, edit in place. Never delete the file and leave the user with no goal on disk.
19. **Scan recursively for duplicates.** Always check `Docs/Goals/` and ALL subfolders before creating a new goal. Match on title similarity, not just exact filenames.
20. **Always update Master.md.** Every goal creation, update, status change, or deletion MUST be reflected in `Docs/Goals/Master.md`. If Master.md doesn't exist, create it by scanning all goal files. If it exists, update the affected rows and recalculate summary counts. This is non-negotiable — Master.md is the central registry.
21. **Master.md reflects goal files, never contradicts them.** If a discrepancy is found, the individual goal files are the source of truth. Rebuild Master.md from scratch.
22. **Verify Master.md after writing.** Read it back after every update to confirm the table is correct, counts are accurate, and no rows are missing or duplicated.
23. **Use `blocked` status for dependency chains.** When a goal's `depends_on` references a non-completed goal, set its status to `blocked`. When the blocking goal completes, transition blocked goals to `pending`.
24. **Dashboard requests trigger reconciliation.** When the user asks to view goals ("show me all goals," "goals dashboard," "what's pending?"), always scan goal files and reconcile Master.md before presenting. Stale dashboards are worse than no dashboard.
