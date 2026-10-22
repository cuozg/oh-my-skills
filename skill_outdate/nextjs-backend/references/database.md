# Database — PostgreSQL with Prisma & Drizzle

Patterns for database integration in serverless Next.js. For comprehensive schema design, migrations, indexing, multi-tenancy, connection pooling, and seed data patterns, use the **database-design** skill (`read_skill_file("database-design", "references/<file>")`).

This file covers Next.js-specific database patterns only.

## Connection Singleton

Never instantiate the database client inside a request handler. Use a global singleton to reuse connections across warm lambda invocations.

### Prisma

```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const db = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
```

### Drizzle

```typescript
// lib/db.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const client = postgres(process.env.DATABASE_URL!, { prepare: false });
export const db = drizzle(client, { schema });
```

## Connection Pooling for Serverless

Use two connection strings — pooled for runtime, direct for migrations:

```env
DATABASE_URL="postgresql://user:pass@pooler.host:6543/db?pgbouncer=true"
DIRECT_URL="postgresql://user:pass@direct.host:5432/db"
```

For comprehensive pooling config (PgBouncer, Neon, Supabase, pool sizing): see `database-design/references/connection-pooling.md`.

## Cursor-Based Pagination

```typescript
// Prisma
async function listPosts(cursor?: string, limit = 20) {
  const items = await db.post.findMany({
    take: limit + 1,
    ...(cursor ? { cursor: { id: cursor }, skip: 1 } : {}),
    orderBy: { createdAt: 'desc' },
  });

  const hasMore = items.length > limit;
  if (hasMore) items.pop();

  return {
    data: items,
    nextCursor: hasMore ? items[items.length - 1].id : null,
  };
}
```

## Transactions

```typescript
// Prisma — sequential
const [order, payment] = await db.$transaction([
  db.order.create({ data: orderData }),
  db.payment.create({ data: paymentData }),
]);

// Prisma — interactive
await db.$transaction(async (tx) => {
  const account = await tx.account.findUniqueOrThrow({ where: { id: accountId } });
  if (account.balance < amount) throw new Error('Insufficient balance');
  await tx.account.update({ where: { id: accountId }, data: { balance: { decrement: amount } } });
});
```

## Full-Text Search

```typescript
// Prisma (raw query)
const results = await db.$queryRaw`
  SELECT * FROM posts
  WHERE to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('english', ${query})
  ORDER BY ts_rank(to_tsvector('english', title || ' ' || content), plainto_tsquery('english', ${query})) DESC
  LIMIT ${limit}
`;
```

## Cross-References to database-design

For deeper patterns, load the relevant database-design reference:

| Topic | Reference |
|-------|-----------|
| Schema design, naming, data types | `database-design/references/schema-design.md` |
| Prisma schema, relations, extensions | `database-design/references/prisma.md` |
| Drizzle schema, relations, queries | `database-design/references/drizzle.md` |
| Zero-downtime migrations | `database-design/references/migrations.md` |
| Indexing strategies | `database-design/references/indexing.md` |
| Multi-tenant RLS | `database-design/references/multi-tenancy.md` |
| Connection pooling | `database-design/references/connection-pooling.md` |
| Seed data & factories | `database-design/references/seed-data.md` |
