---
name: database-design
description: >
  Unified PostgreSQL database design skill — schema creation, migrations, indexing,
  multi-tenancy, connection pooling, seed data, and ORM integration (Prisma/Drizzle).
  Auto-triages: Quick (single table, add column, create index, simple migration) or
  Deep (multi-table schema, multi-tenant setup, migration strategy, full data model).
  MUST use for ANY PostgreSQL schema or database design request. Triggers: "design a
  schema," "create a table," "Prisma model," "Drizzle schema," "add an index,"
  "migration strategy," "multi-tenant database," "normalize this," "PostgreSQL schema,"
  "foreign key," "RLS policy," "JSONB vs relational," "cursor pagination," "soft deletes,"
  "audit columns," "seed data," "connection pooling," "PgBouncer," "pool sizing,"
  "factory pattern." Do not use for application-layer query optimization (nextjs-backend)
  or database administration (backups, replication).
metadata:
  author: cuongnp
  version: "1.1"
---
# database-design

Design PostgreSQL schemas, write safe migrations, choose indexes, and define ORM models. Detect which ORM the project uses (Prisma vs Drizzle), match local conventions, and deliver production-quality database code.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| One table/model, add column, single index, simple migration | **Quick** |
| Multi-table schema, relationships, multi-tenant, migration strategy, full data model | **Deep** |

State triage: "This is [mode] — [reason]."

## Step 2 — Detect ORM

Check the project for ORM signals before writing any code:

| Signal | ORM |
|--------|-----|
| `prisma/schema.prisma`, `@prisma/client` in package.json | **Prisma** |
| `drizzle.config.ts`, `drizzle-orm` in package.json | **Drizzle** |
| Raw SQL files, no ORM detected | **Raw SQL** |

If both are present, ask which to use. If neither is present, ask the user's preference.

## Step 3 — Execute

### Quick Mode

Load the relevant reference for the task:
- Schema design → `read_skill_file("database-design", "references/schema-design.md")`
- Index decision → `read_skill_file("database-design", "references/indexing.md")`
- Migration → `read_skill_file("database-design", "references/migrations.md")`
- Prisma model → `read_skill_file("database-design", "references/prisma.md")`
- Drizzle table → `read_skill_file("database-design", "references/drizzle.md")`
- Seed data → `read_skill_file("database-design", "references/seed-data.md")`
- Connection pooling → `read_skill_file("database-design", "references/connection-pooling.md")`

1. **Discover** — read existing schema files, migration history, and 1-2 nearby models for naming conventions and patterns
2. **Implement** — write the schema change matching local conventions (naming, ID strategy, timestamp columns, constraint style)
3. **Migration** — generate migration file if applicable (`prisma migrate dev`, `drizzle-kit generate`, or raw SQL)
4. **Verify** — `lsp_diagnostics` on changed files; confirm migration SQL is safe (no locks on large tables, no data loss)

### Deep Mode

Load all references relevant to the feature scope.

1. **Discover** — read project structure, existing schema, migration history, ORM config, and related domain models
2. **Design** — define entity relationships, choose data types per the schema-design reference, identify which tables need indexes
3. **Plan** — list every table/model change, migration order, index additions, and RLS policies if multi-tenant
4. **Implement** — schema definitions first → migration files → seed data if needed
5. **Verify** — `lsp_diagnostics` on all changed files, review migration SQL for safety
6. **Handoff** — list changed files, migration commands to run, any manual steps (backfill, RLS setup)

## Rules

- **snake_case everywhere** — table names, column names, index names, constraint names
- **TIMESTAMPTZ** for all temporal columns, never `TIMESTAMP` without timezone
- **BIGINT or UUID v7** for primary keys — never `SERIAL`/`INTEGER` (wraps on large tables)
- **TEXT over VARCHAR(n)** unless the length limit is a strict business rule
- **JSONB over JSON** — JSON has no indexing support and stores as text
- **NOT NULL by default** — make columns nullable only when null has a specific business meaning
- **Foreign keys always** — skip only with explicit justification (e.g., cross-database references)
- **Audit columns on every table** — `created_at TIMESTAMPTZ DEFAULT now()`, `updated_at` via trigger or ORM
- **Soft deletes need partial unique indexes** — `CREATE UNIQUE INDEX ... WHERE deleted_at IS NULL`
- Never add a `NOT NULL` column without `DEFAULT` on large tables (causes full table rewrite pre-PG11)
- Always use `CREATE INDEX CONCURRENTLY` for non-blocking index creation on production tables
- Use `SET lock_timeout = '5s'` before DDL in production migrations to avoid lock queue buildup
- Local style wins — if project uses specific naming, ID strategy, or patterns, match them exactly
- `lsp_diagnostics` after every code change

## Escalation

| From | To | When |
|------|----|------|
| Quick | Deep | Schema change touches 2+ tables or requires relationship design |
| Deep | Quick | Analysis reveals single-table scope |

Carry forward context; tell user why.

## Reference Catalog

Load on demand via `read_skill_file("database-design", "references/<file>")`:

- `schema-design.md` — Naming conventions, data types, constraints, relationships, normalization, JSONB patterns, audit columns, soft deletes
- `migrations.md` — Versioned migrations, zero-downtime DDL, expand-contract, idempotent scripts, data migrations, rollback strategies
- `multi-tenancy.md` — Shared schema + RLS, schema-per-tenant, tenant resolution, connection pooling, RLS policies with Prisma/Drizzle
- `indexing.md` — B-tree, GIN, GiST, partial indexes, expression indexes, covering indexes (INCLUDE), when NOT to index, composite index column order
- `prisma.md` — Schema definition (@map/@db), migrations (dev/deploy), relations, client extensions, cursor pagination, transactions, raw SQL
- `drizzle.md` — pgTable definition, column types, drizzle-kit migrations, relations, query patterns, JSONB/array/full-text search, transactions
- `seed-data.md` — Prisma/Drizzle seed setup, factory pattern with faker.js, idempotent upserts, environment-aware seeding, batch inserts, dependency ordering
- `connection-pooling.md` — Singleton pattern, PgBouncer (transaction/session mode), Neon/Supabase/Vercel serverless drivers, pool sizing, dual connection strings, retry patterns
