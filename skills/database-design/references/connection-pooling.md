# Connection Pooling — PostgreSQL Performance

Strategies for managing PostgreSQL connections in serverless, edge, and traditional deployments. Covers pool sizing, PgBouncer, serverless drivers, and common gotchas.

## Why Pooling Matters

PostgreSQL forks a new process per connection (~10MB RAM each). Without pooling:
- 100 concurrent requests = 100 connections = ~1GB RAM on the DB server
- Serverless functions create/destroy connections rapidly, exhausting `max_connections`
- Connection establishment takes 20-100ms (TCP + TLS + auth)

## Connection Singleton (Application-Level)

Every application should use a single shared client instance. Never instantiate inside a request handler.

### Prisma

```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
export const db = globalForPrisma.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
```

### Drizzle (node-postgres)

```typescript
// lib/db.ts
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,               // max connections in pool
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

export const db = drizzle(pool, { schema });
```

### Drizzle (postgres.js — for serverless)

```typescript
// lib/db.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const client = postgres(process.env.DATABASE_URL!, {
  prepare: false,  // Required for PgBouncer transaction mode
  max: 10,
});

export const db = drizzle(client, { schema });
```

## Dual Connection Strings

Use two connection strings — pooled for runtime, direct for migrations:

```env
# Pooled connection for runtime queries (PgBouncer / Neon / Supabase pooler)
DATABASE_URL="postgresql://user:pass@pooler.host:6543/db?pgbouncer=true"

# Direct connection for migrations (schema changes need session features)
DIRECT_URL="postgresql://user:pass@direct.host:5432/db"
```

### Prisma Configuration

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")  // Used by prisma migrate
}
```

### Drizzle Configuration

```typescript
// drizzle.config.ts — always uses direct connection
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  dialect: 'postgresql',
  schema: './src/db/schema.ts',
  out: './drizzle',
  dbCredentials: {
    url: process.env.DIRECT_URL!,  // Direct connection for migrations
  },
});
```

## PgBouncer

External connection pooler that sits between your app and PostgreSQL.

### Transaction Mode (Recommended for Serverless)

Each query or transaction gets a connection, released immediately after. Most efficient for serverless.

```ini
# pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_port = 6543
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
server_idle_timeout = 30
```

### Transaction Mode Gotchas

| Feature | Works? | Workaround |
|---------|--------|------------|
| Prepared statements | No | Set `prepare: false` in postgres.js, `pgbouncer=true` in Prisma URL |
| `SET` variables (session-level) | No | Use `SET LOCAL` inside transactions |
| `LISTEN/NOTIFY` | No | Use session mode for these connections |
| Advisory locks | No | Use session mode or row-level locks |
| Temp tables | No | Use CTEs or regular tables |

### Session Mode

Connection is held for the entire client session. Higher resource usage but supports all PostgreSQL features.

```ini
pool_mode = session
default_pool_size = 50
```

Use session mode when you need: `LISTEN/NOTIFY`, advisory locks, temp tables, or connection-level `SET` commands.

## Serverless Providers

### Neon (HTTP Driver)

Zero-cold-start connections over HTTP — no TCP connection overhead:

```typescript
import { drizzle } from 'drizzle-orm/neon-http';
import { neon } from '@neondatabase/serverless';
import * as schema from './schema';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

For WebSocket connections (when you need transactions):

```typescript
import { drizzle } from 'drizzle-orm/neon-serverless';
import { Pool } from '@neondatabase/serverless';
import * as schema from './schema';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool, { schema });
```

### Supabase

Supabase provides a built-in PgBouncer pooler on port 6543:

```env
# Transaction mode pooler (port 6543)
DATABASE_URL="postgresql://postgres.ref:pass@aws-0-region.pooler.supabase.com:6543/postgres"

# Direct (port 5432)
DIRECT_URL="postgresql://postgres.ref:pass@aws-0-region.supabase.com:5432/postgres"
```

### Vercel Postgres / @vercel/postgres

Uses Neon under the hood with automatic pooling:

```typescript
import { sql } from '@vercel/postgres';
import { drizzle } from 'drizzle-orm/vercel-postgres';
import * as schema from './schema';

export const db = drizzle(sql, { schema });
```

## Pool Sizing

### Formula

```
max_connections = (num_physical_cores * 2) + effective_spindle_count
```

For most cloud databases:
- **Small** (1-2 vCPU): 25-50 connections
- **Medium** (4-8 vCPU): 50-100 connections
- **Large** (16+ vCPU): 100-200 connections

### Application-Side Pool Size

```
app_pool_size = max_connections / num_app_instances
```

Example: 100 DB connections, 4 app instances → `max: 25` per instance.

### Serverless Considerations

- Each cold-start creates a new pool
- Set `max: 1-5` per function instance
- Use external pooler (PgBouncer/Neon/Supabase) to multiplex
- Monitor `pg_stat_activity` for connection count:

```sql
SELECT count(*) FROM pg_stat_activity WHERE datname = 'mydb';
SELECT max_conn FROM pg_settings WHERE name = 'max_connections';
```

## Connection Health

### Timeout Configuration

```typescript
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  connectionTimeoutMillis: 5000,   // Fail fast if can't connect in 5s
  idleTimeoutMillis: 30000,        // Close idle connections after 30s
  allowExitOnIdle: true,           // Allow Node process to exit when pool is idle
});

// Health check
pool.on('error', (err) => {
  console.error('Unexpected pool error:', err);
});
```

### Retry Pattern

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 100,
): Promise<T> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error: any) {
      const isRetryable =
        error.code === 'ECONNREFUSED' ||
        error.code === '53300' ||  // too_many_connections
        error.code === '57P01';    // admin_shutdown

      if (!isRetryable || attempt === maxRetries) throw error;

      const delay = baseDelay * Math.pow(2, attempt - 1); // Exponential backoff
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw new Error('Unreachable');
}
```

## Deployment Strategy Summary

| Deployment | Driver | Pooler | Pool Size |
|------------|--------|--------|-----------|
| Vercel / Lambda | `@neondatabase/serverless` or `postgres` | Neon HTTP or PgBouncer | 1-5 per instance |
| Edge Runtime | `@neondatabase/serverless` (HTTP) | Neon HTTP | 1 (HTTP, no pool) |
| Docker / VPS | `pg` Pool | Internal pool or PgBouncer | 10-25 per instance |
| Kubernetes | `pg` Pool | PgBouncer sidecar | 5-10 per pod |

## Rules

- **Never instantiate** database clients inside request handlers — use a module-level singleton
- **Always use `prepare: false`** with PgBouncer transaction mode — prepared statements are connection-scoped
- **Use dual connection strings** — pooled for runtime, direct for migrations
- **Set `connectionTimeoutMillis`** — fail fast (5s) rather than queue indefinitely
- **Monitor `pg_stat_activity`** — alert when connection count approaches `max_connections`
- **Match pool size to deployment** — serverless (1-5), traditional (10-25), never exceed DB `max_connections / instance_count`
