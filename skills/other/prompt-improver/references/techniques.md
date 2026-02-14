# Prompt Engineering Techniques for Coding Agents

Comprehensive catalog of techniques to transform raw prompts into high-quality, actionable prompts for AI coding agents.

## Table of Contents

1. [Specificity](#1-specificity)
2. [Structure](#2-structure)
3. [Context Injection](#3-context-injection)
4. [Constraint Definition](#4-constraint-definition)
5. [Role Framing](#5-role-framing)
6. [Chain-of-Thought Decomposition](#6-chain-of-thought-decomposition)
7. [Example Seeding](#7-example-seeding)
8. [Scope Bounding](#8-scope-bounding)
9. [Verification Criteria](#9-verification-criteria)
10. [Anti-Patterns to Fix](#10-anti-patterns-to-fix)

---

## 1. Specificity

Replace vague language with concrete details. Vague prompts produce vague results.

**Techniques:**

- **Name the thing**: Replace "the file" with `src/auth/login.ts`, "the component" with `UserProfileCard`
- **Quantify**: Replace "improve performance" with "reduce initial load time from 3.2s to under 1.5s"
- **Name the technology**: Replace "add a database" with "add a PostgreSQL table with Prisma ORM"
- **Specify the behavior**: Replace "fix the bug" with "fix: clicking Submit twice creates duplicate orders"
- **Reference the pattern**: Replace "make it like the others" with "follow the repository pattern used in `OrderService.cs`"

**Signal words that need replacing:**

| Vague | Ask for / Replace with |
|---|---|
| "it", "the thing", "this" | Exact name, path, or identifier |
| "better", "improve", "optimize" | Measurable target or comparison baseline |
| "handle", "deal with" | Specific behavior (validate, reject, retry, log) |
| "some", "a few", "various" | Exact count or enumerated list |
| "like before", "the usual way" | Reference to specific file, pattern, or convention |
| "clean up" | Specific actions (extract method, rename, remove dead code) |

---

## 2. Structure

Transform walls of text into organized sections. Structure helps agents parse intent quickly and reduces ambiguity.

**Standard sections for coding prompts:**

```
## Goal
[One sentence: what to achieve]

## Context
[Relevant background, current state, why this is needed]

## Scope
[Files, modules, or systems to touch]
[What is explicitly OUT of scope]

## Requirements
[Numbered list of specific behaviors or deliverables]

## Constraints
[Technical limitations, patterns to follow, things to avoid]

## Success Criteria
[How to verify the work is done correctly]
```

**When to use which sections:**

- **Simple tasks** (single file, clear action): Goal + Requirements only
- **Feature implementation**: Goal + Context + Scope + Requirements + Constraints
- **Bug fixes**: Goal + Context (reproduction steps) + Requirements + Success Criteria
- **Refactoring**: Goal + Scope + Constraints + Success Criteria
- **Complex multi-step**: All sections + MUST DO / MUST NOT DO lists

---

## 3. Context Injection

Add information the agent needs but doesn't have. Agents work best when they understand the "why" and "where."

**Types of context to inject:**

- **File paths**: "The auth logic lives in `src/services/auth/` with entry point `AuthService.ts`"
- **Existing patterns**: "Other services in this project use the Repository pattern — see `OrderRepository.cs` for reference"
- **Data shapes**: "The API returns `{ user: { id: string, email: string, roles: string[] } }`"
- **Business rules**: "Users with role 'admin' bypass rate limiting; free-tier users are limited to 100 requests/hour"
- **Historical context**: "We migrated from REST to GraphQL last sprint; some endpoints still use the old pattern"
- **Architecture decisions**: "We use event-driven architecture — changes to Order trigger events consumed by Inventory and Billing"
- **Environment**: "This runs on Unity 6, targeting mobile (iOS/Android) with IL2CPP backend"

**Context injection checklist:**

1. What files/systems are involved?
2. What patterns should be followed?
3. What has been tried or decided already?
4. What are the data shapes/types?
5. What domain rules apply?

---

## 4. Constraint Definition

Explicit boundaries prevent the agent from making assumptions or going off-track.

**MUST DO / MUST NOT DO format:**

```
## MUST DO
1. Follow existing naming conventions in the codebase
2. Add XML documentation comments to all public methods
3. Write unit tests for new logic
4. Use dependency injection for new services

## MUST NOT DO
1. Do NOT modify the database schema
2. Do NOT change the public API contract
3. Do NOT add new NuGet/npm packages without listing them
4. Do NOT use async void (use async Task instead)
```

**Common constraint categories:**

- **Style**: naming conventions, code formatting, comment requirements
- **Architecture**: patterns to follow, layers to respect, coupling rules
- **Performance**: allocation limits, complexity bounds, render budget
- **Compatibility**: target platforms, minimum versions, backward compatibility
- **Safety**: no destructive operations, no force pushes, no data deletion without confirmation
- **Scope**: files to touch, files to leave alone, systems that are off-limits

---

## 5. Role Framing

Set the right persona or expertise level for the task. Role framing activates relevant knowledge.

**Effective role frames for coding agents:**

- "Act as a senior Unity developer with expertise in UI Toolkit and mobile optimization"
- "Act as a security-focused code reviewer looking for OWASP Top 10 vulnerabilities"
- "Act as a performance engineer profiling a Node.js application with high p99 latency"
- "Act as a database architect designing for 10M+ daily active users"

**When to use role framing:**

- Domain-specific tasks requiring specialized knowledge
- Code reviews needing a specific lens (security, performance, accessibility)
- Architecture decisions requiring experience-based judgment
- Debugging sessions requiring deep system knowledge

**When NOT needed:**

- Simple file edits or renames
- Straightforward CRUD operations
- Tasks where the skill already sets the role

---

## 6. Chain-of-Thought Decomposition

Break complex tasks into ordered steps. This prevents the agent from skipping steps or making assumptions about execution order.

**Decomposition patterns:**

**Sequential** (each step depends on the previous):
```
1. Read and understand the current PlayerHealth.cs implementation
2. Add a `RegenerationRate` field with [SerializeField] attribute
3. Implement `StartRegeneration()` method using coroutine
4. Add unit tests for regeneration logic
5. Update the Inspector to show regeneration controls
```

**Parallel** (independent steps that can be done in any order):
```
These changes are independent and can be made in any order:
- [ ] Update the model class to add the new field
- [ ] Update the API endpoint to accept the new parameter
- [ ] Update the frontend form to include the new input
- [ ] Add validation for the new field
```

**Conditional** (branching based on discovery):
```
1. Check if `UserService` already has a caching layer
   - If yes → extend the existing cache with TTL support
   - If no → add Redis caching with 5-minute TTL
2. Verify cache invalidation triggers exist for user updates
```

---

## 7. Example Seeding

Provide input/output examples when the desired format or transformation isn't obvious.

**When to seed examples:**

- Code generation where style matters
- Data transformation where format is critical
- Naming conventions that can't be easily described
- Output format that must match an existing pattern

**Example format:**

```
Generate API endpoints following this pattern:

Input: "Get user by ID"
Output:
[HttpGet("{id}")]
public async Task<ActionResult<UserDto>> GetById(int id)
{
    var user = await _userService.GetByIdAsync(id);
    if (user == null) return NotFound();
    return Ok(user);
}

Now generate endpoints for:
- "Create a new order"
- "Update order status"
- "Delete order by ID"
```

---

## 8. Scope Bounding

Define what's in and out of scope to prevent scope creep and unnecessary changes.

**Explicit scope template:**

```
## In Scope
- Modify: `src/services/OrderService.ts`
- Modify: `src/controllers/OrderController.ts`  
- Create: `src/services/__tests__/OrderService.test.ts`
- Create: `src/models/OrderStatus.ts`

## Out of Scope
- Do NOT modify the database migration files
- Do NOT change the existing API routes
- Do NOT refactor unrelated services
- Leave `PaymentService.ts` untouched even if you see improvement opportunities
```

**Scope bounding signals:**

- "Only touch files in the `src/auth/` directory"
- "This change should be limited to the frontend — no backend changes"
- "Focus on the `ProcessOrder` method; don't refactor the entire class"
- "Add the feature but don't optimize existing code in the same PR"

---

## 9. Verification Criteria

Define measurable conditions for "done." This allows the agent to self-verify.

**Types of verification:**

- **Compilation**: "Code compiles with zero errors and zero warnings"
- **Tests**: "All existing tests pass; new tests cover the added logic with >80% branch coverage"
- **Behavior**: "Clicking 'Submit' with an empty form shows validation errors for all required fields"
- **Performance**: "The list renders 1000 items with <16ms frame time"
- **Diagnostics**: "Run `lsp_diagnostics` on all changed files — zero errors"
- **Manual check**: "Read all modified files to verify correctness"

**Good verification criteria pattern:**

```
## Success Criteria
1. `dotnet build` passes with zero errors
2. `dotnet test` passes — all existing + new tests green
3. API returns 200 for valid input, 422 for invalid input with error details
4. No N+1 query patterns (verify with SQL logging)
5. Run lsp_diagnostics on all changed files — clean
```

---

## 10. Anti-Patterns to Fix

Common prompt mistakes and their corrections.

### Too Vague
**Bad**: "Fix the login"
**Good**: "Fix: users with special characters in email (e.g., `user+test@example.com`) get a 500 error on POST `/api/auth/login`. The error is in `AuthService.validateEmail()` — it rejects the `+` character."

### Too Verbose / Noisy
**Bad**: (3 paragraphs of background, history of the project, team dynamics, and then the actual request buried in paragraph 4)
**Good**: Move background to a `## Context` section; put the actionable request in `## Goal` at the top.

### Missing Context
**Bad**: "Add caching to the API"
**Good**: "Add Redis caching (we already have a Redis instance at `redis://cache:6379`) to the `GET /api/products` endpoint in `ProductController.ts`. Cache for 5 minutes. Invalidate on `POST/PUT/DELETE` to products."

### Ambiguous Scope
**Bad**: "Refactor the user module"
**Good**: "Extract the validation logic from `UserService.createUser()` into a separate `UserValidator` class. Only modify `UserService.ts` and create `UserValidator.ts`. Don't change tests yet."

### No Success Criteria
**Bad**: "Make the dashboard faster"
**Good**: "Reduce the dashboard's initial load time from 4.2s to under 2s. Key targets: (1) lazy-load the chart components, (2) paginate the activity feed to 20 items, (3) cache the summary stats for 60s. Measure with Lighthouse Performance score — target 85+."

### Asking Multiple Unrelated Things
**Bad**: "Fix the login bug, also add dark mode, and can you review the PR?"
**Good**: Split into three separate prompts, each with its own goal, scope, and constraints.

### Prescribing Implementation Instead of Outcome
**Bad**: "Create a `HashMap<String, List<Integer>>`, iterate through it with a for loop, and..."
**Good**: "Group the order items by category, returning a mapping of category name to list of order IDs. Use whatever data structure and approach is most idiomatic."
