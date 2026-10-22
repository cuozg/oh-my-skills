---
name: nextjs-backend
description: >
  Unified Next.js backend coding skill — write API routes, server actions, database queries,
  authentication, and multi-tenant logic using the App Router. Auto-triages: Quick (single
  route handler, one server action, simple CRUD endpoint, auth check) or Deep (multi-file
  features: full auth system, multi-tenant setup, CRUD with pagination + validation, webhook
  integrations). MUST use for ANY Next.js backend request — API routes, route handlers,
  server actions, database queries (Prisma/Drizzle), JWT auth, middleware, multi-tenant
  architecture, webhook processing, or server-side data mutations. Triggers: "create an API
  route," "add a server action," "connect to PostgreSQL," "add authentication," "protect
  this route," "multi-tenant," "webhook handler," "database query," "Prisma schema,"
  "Drizzle query," "JWT," "middleware auth." Do not use for frontend React components,
  styling, or client-side state management.
metadata:
  author: cuongnp
  version: "1.1"
---
# nextjs-backend

Detect scope, pick mode, implement. Match local patterns (Prisma vs Drizzle, Auth.js vs custom JWT), verify with TypeScript, deliver complete backend code.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| One file: single route handler, one server action, add auth check, simple query | **Quick** |
| 2+ files: auth system, multi-tenant setup, full CRUD resource, webhook + DB integration | **Deep** |

State triage: "This is [mode] — [reason]."

## Step 2 — Execute

### Quick Mode

Load the relevant reference for the task domain:
- API route → `read_skill_file("nextjs-backend", "references/api-routes.md")`
- Server action → `read_skill_file("nextjs-backend", "references/server-actions.md")`
- Database query → `read_skill_file("nextjs-backend", "references/database.md")`
- Auth check → `read_skill_file("nextjs-backend", "references/auth.md")`

1. **Qualify** — confirm one file suffices; escalate to Deep if scope grows
2. **Discover** — read target + 1-2 nearby files for project conventions (which ORM, auth library, error format, naming)
3. **Implement** — smallest complete change matching local patterns. Use Zod for input validation, proper HTTP status codes, TypeScript types throughout
4. **Verify** — `lsp_diagnostics` on changed file
5. **Handoff** — file path, what changed, usage example (curl/fetch), any env vars needed

### Deep Mode

Load all relevant references for the feature scope.

1. **Qualify** — confirm 2+ files needed; switch to Quick if single-file
2. **Discover** — read project structure, existing auth setup, database config, middleware, env vars. Identify which ORM (Prisma/Drizzle), auth library (Auth.js/custom), and patterns are already in use
3. **Plan** — list every file, layer (schema/models → lib/services → API routes/actions → middleware), dependency order
4. **Implement** — data layer first (Prisma schema, Drizzle tables, migrations) → service/lib layer (queries, auth utils) → API routes/server actions → middleware
5. **Verify** — `lsp_diagnostics` per layer, then all files
6. **Handoff** — changed paths, env vars needed, migration commands (`npx prisma migrate dev`), testing guidance (curl examples)

## Rules

- Local style wins — if project uses Drizzle, don't suggest Prisma; if custom JWT, don't add Auth.js
- Zod validation on every user input (request body, form data, search params)
- Proper HTTP status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error
- Standardized error response: `{ error: string, details?: unknown }`
- Never expose internal errors to clients — log full error server-side, return generic message
- Never leave `TODO`, stubs, or placeholder logic
- Auth checks at the start of every protected handler/action — fail fast
- Connection singleton for database clients — never instantiate inside a request handler
- `lsp_diagnostics` after every code change
- Ambiguity → ask which ORM/auth approach to use if project has no existing convention

## Escalation

| From | To | When |
|------|----|------|
| Quick | Deep | Work requires a second file or new data layer |
| Deep | Quick | Plan reveals single-file scope |

Carry forward context; tell user why.

## Reference Catalog

Load on demand via `read_skill_file("nextjs-backend", "references/<file>")`:

- `api-routes.md` — Route handlers (GET/POST/PUT/DELETE), NextRequest/NextResponse, dynamic routes, streaming, CORS, runtime selection
- `server-actions.md` — `'use server'` patterns, useActionState, form validation, revalidation, optimistic updates, security
- `database.md` — PostgreSQL with Prisma/Drizzle, connection pooling, transactions, cursor pagination, full-text search, migrations
- `auth.md` — Auth.js v5 JWT strategy, custom JWT with jose, middleware protection, RBAC, password hashing, refresh tokens
- `multi-tenant.md` — Tenant resolution (subdomain/path/domain), PostgreSQL RLS, Prisma tenant extensions, provisioning flow, Stripe billing
- `validation-errors.md` — Zod schemas, error response standardization, pagination params, file upload validation, webhook signature verification
