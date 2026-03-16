# Multi-Tenancy — PostgreSQL Data Isolation

Patterns for building multi-tenant applications with PostgreSQL. Covers strategy selection, Row-Level Security, schema isolation, and ORM integration.

## Strategy Selection

| Strategy | Isolation Level | Complexity | Best For |
|----------|----------------|------------|----------|
| Shared schema + `tenant_id` (app-enforced) | Low | Low | Prototyping, internal tools |
| Shared schema + RLS (DB-enforced) | High | Medium | Production SaaS (recommended default) |
| Schema-per-tenant | High | High | Enterprise, compliance-heavy |
| Database-per-tenant | Maximum | Very High | Healthcare, finance, government |

**Recommended default**: Shared schema with PostgreSQL Row-Level Security (RLS). It prevents "forgotten WHERE clause" data leaks at the database level, not just the application level.

## Shared Schema + RLS (Recommended)

### 1. Table Design

Every tenant-scoped table gets a `tenant_id` column:

```sql
CREATE TABLE project (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id UUID NOT NULL REFERENCES tenant(id),
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Composite index: tenant_id first (all queries are tenant-scoped)
CREATE INDEX idx_project_tenant ON project(tenant_id, created_at DESC);
```

### 2. Enable RLS

```sql
-- Enable RLS on every tenant-scoped table
ALTER TABLE project ENABLE ROW LEVEL SECURITY;

-- Force RLS even for table owners (prevents accidental bypass)
ALTER TABLE project FORCE ROW LEVEL SECURITY;

-- Isolation policy using a session variable
CREATE POLICY tenant_isolation ON project
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- If you need separate read/write policies:
CREATE POLICY tenant_read ON project
  FOR SELECT USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

CREATE POLICY tenant_write ON project
  FOR ALL USING (tenant_id = current_setting('app.current_tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

### 3. Setting Tenant Context

Set the session variable at the start of every request, scoped to the transaction:

```sql
-- SET LOCAL is transaction-scoped (safe for connection pooling)
-- SET (without LOCAL) is session-scoped (DANGEROUS with connection pooling — bleeds across requests)
BEGIN;
SELECT set_config('app.current_tenant_id', $1, true);  -- true = transaction-local
-- ... queries here are automatically filtered ...
COMMIT;
```

### 4. Prisma Integration

```typescript
// lib/tenant-db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
const basePrisma = globalForPrisma.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = basePrisma;

export function getTenantDb(tenantId: string) {
  return basePrisma.$extends({
    query: {
      $allModels: {
        async $allOperations({ args, query }) {
          return basePrisma.$transaction(async (tx) => {
            // Parameterized — never interpolate tenantId into SQL
            await tx.$queryRawUnsafe(
              `SELECT set_config('app.current_tenant_id', $1, true)`,
              tenantId,
            );
            return query(args);
          });
        },
      },
    },
  });
}
```

### 5. Drizzle Integration

```typescript
// lib/tenant-db.ts
import { db } from './db';
import { sql } from 'drizzle-orm';

export async function withTenant<T>(
  tenantId: string,
  fn: (tx: typeof db) => Promise<T>,
): Promise<T> {
  return db.transaction(async (tx) => {
    await tx.execute(
      sql`SELECT set_config('app.current_tenant_id', ${tenantId}, true)`
    );
    return fn(tx as unknown as typeof db);
  });
}

// Usage
const projects = await withTenant(tenantId, async (tx) => {
  return tx.select().from(project).orderBy(project.createdAt);
});
```

## Schema-Per-Tenant

Each tenant gets their own PostgreSQL schema. Stronger isolation but harder to manage.

### Setup

```sql
-- Create schema for new tenant
CREATE SCHEMA tenant_acme;

-- Create tables in tenant schema
CREATE TABLE tenant_acme.project (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL
);

-- Set search_path per request
SET search_path TO tenant_acme, public;
```

### Connection Pooling Considerations

Schema-per-tenant breaks connection pooling in `transaction` mode (PgBouncer) because `SET search_path` is session-level. Solutions:

1. Use `SET LOCAL search_path` within transactions (limits functionality)
2. Use PgBouncer in `session` mode (fewer pooled connections)
3. Use a connection pool per tenant (complex, resource-heavy)

### Migration Challenges

Every schema migration must be applied to ALL tenant schemas. Use a migration runner that iterates:

```typescript
async function migrateAllTenants(migrationSql: string) {
  const tenants = await db.query('SELECT schema_name FROM tenant');
  for (const tenant of tenants) {
    await db.query(`SET search_path TO ${tenant.schema_name}, public`);
    await db.query(migrationSql);
  }
}
```

## Tenant Resolution

Resolve the tenant ID server-side — never trust client-provided values.

| Method | Example | Notes |
|--------|---------|-------|
| Subdomain | `acme.app.com` → look up `acme` in DB | Most common for SaaS |
| Path prefix | `/org/acme/dashboard` | Works without DNS config |
| Custom domain | `acme.com` → look up domain mapping | For white-label products |
| JWT claim | `token.tenantId` | After authentication |
| API key header | `X-Tenant-ID: uuid` | For API-first products |

### Middleware Pattern (Framework-Agnostic)

```typescript
async function resolveTenant(request: Request): Promise<string> {
  // Option 1: From subdomain
  const hostname = request.headers.get('host') ?? '';
  const subdomain = hostname.split('.')[0];
  if (subdomain && subdomain !== 'www' && subdomain !== 'app') {
    const tenant = await db.query(
      'SELECT id FROM tenant WHERE slug = $1',
      [subdomain]
    );
    if (tenant) return tenant.id;
  }

  // Option 2: From JWT
  const token = await verifyToken(request);
  if (token?.tenantId) return token.tenantId;

  throw new Error('Unable to resolve tenant');
}
```

## Cross-Tenant Operations

Some operations need to bypass RLS (admin dashboards, analytics, billing):

```sql
-- Create a superuser role that bypasses RLS
CREATE ROLE app_admin BYPASSRLS;

-- Or use a separate connection without RLS set
-- In Prisma: use the base client (not the tenant-extended one)
```

```typescript
// Admin operations use the base client (no RLS)
const allTenants = await basePrisma.tenant.findMany();

// Tenant-scoped operations use the extended client
const tenantDb = getTenantDb(tenantId);
const projects = await tenantDb.project.findMany();
```

## Rules

- Always resolve tenant from server-side context (JWT, subdomain, session) — never from request body
- Use `SET LOCAL` or `set_config(..., true)` for RLS vars — scoped to transaction, not connection
- Use parameterized queries (`$1`) when setting RLS vars — never string interpolation
- Index `tenant_id` as the first column in composite indexes — every query is tenant-scoped
- Test cross-tenant isolation: verify tenant A cannot read tenant B's data
- For schema-per-tenant: plan migration strategy before you hit 50+ tenants
