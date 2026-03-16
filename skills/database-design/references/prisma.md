# Prisma — Schema, Migrations & Queries

Production patterns for Prisma ORM with PostgreSQL. Covers schema definition, naming conventions, migrations, queries, relations, and performance.

## Schema Definition

### Naming Convention: PascalCase Models → snake_case Tables

Prisma uses PascalCase for models and camelCase for fields. Map to PostgreSQL's snake_case convention with `@@map` and `@map`:

```prisma
model UserProfile {
  id          String   @id @default(uuid()) @map("id")
  firstName   String   @map("first_name")
  lastName    String   @map("last_name")
  email       String   @unique
  role        UserRole @default(MEMBER)
  tenantId    String   @map("tenant_id")
  metadata    Json?    @default("{}")    // Maps to JSONB in PostgreSQL
  createdAt   DateTime @default(now())   @map("created_at") @db.Timestamptz
  updatedAt   DateTime @updatedAt        @map("updated_at") @db.Timestamptz
  deletedAt   DateTime?                  @map("deleted_at") @db.Timestamptz

  tenant      Tenant   @relation(fields: [tenantId], references: [id])
  posts       Post[]

  @@map("user_profile")
  @@index([tenantId])
  @@unique([email], map: "uniq_user_profile_email")
}

enum UserRole {
  ADMIN
  MEMBER
}
```

### Key Annotations

| Annotation | Purpose | Example |
|-----------|---------|---------|
| `@map("snake_case")` | Map field to PG column name | `firstName @map("first_name")` |
| `@@map("snake_case")` | Map model to PG table name | `@@map("user_profile")` |
| `@db.Timestamptz` | Use `TIMESTAMPTZ` instead of `TIMESTAMP` | `createdAt @db.Timestamptz` |
| `@db.Text` | Use `TEXT` instead of `VARCHAR(191)` | `content @db.Text` |
| `@db.BigInt` | Use `BIGINT` for large numbers | `amount @db.BigInt` |
| `@default(uuid())` | UUID v4 primary key | `id String @id @default(uuid())` |
| `@default(dbgenerated("gen_random_uuid()"))` | DB-generated UUID | PostgreSQL-native UUID generation |
| `@updatedAt` | Auto-set on update | `updatedAt DateTime @updatedAt` |
| `Json` | Maps to JSONB in PostgreSQL | `metadata Json?` |

## Connection Singleton

Never instantiate PrismaClient in a request handler. Use a global singleton:

```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
export const db = globalForPrisma.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
```

### Connection Pooling (Serverless)

Use two connection strings in `.env`:

```env
# Pooled connection for runtime queries (PgBouncer / Neon pooler)
DATABASE_URL="postgresql://user:pass@pooler.host:6543/db?pgbouncer=true"
# Direct connection for migrations only
DIRECT_URL="postgresql://user:pass@direct.host:5432/db"
```

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}
```

## Relations

### One-to-Many

```prisma
model User {
  id    String @id @default(uuid())
  posts Post[]
  @@map("user")
}

model Post {
  id       String @id @default(uuid())
  authorId String @map("author_id")
  author   User   @relation(fields: [authorId], references: [id], onDelete: Cascade)
  @@map("post")
  @@index([authorId])
}
```

### Many-to-Many (Explicit Junction)

Use explicit junction tables when the relationship has its own data:

```prisma
model PostTag {
  postId    String   @map("post_id")
  tagId     String   @map("tag_id")
  createdAt DateTime @default(now()) @map("created_at")

  post Post @relation(fields: [postId], references: [id], onDelete: Cascade)
  tag  Tag  @relation(fields: [tagId], references: [id], onDelete: Cascade)

  @@id([postId, tagId])
  @@map("post_tag")
}
```

### Self-Relation

```prisma
model User {
  id         String  @id @default(uuid())
  mentorId   String? @map("mentor_id")
  mentor     User?   @relation("Mentorship", fields: [mentorId], references: [id])
  mentees    User[]  @relation("Mentorship")
  @@map("user")
}
```

## Queries

### Cursor-Based Pagination

```typescript
async function listPosts(cursor?: string, limit = 20) {
  const items = await db.post.findMany({
    take: limit + 1,
    ...(cursor ? { cursor: { id: cursor }, skip: 1 } : {}),
    orderBy: { createdAt: 'desc' },
    select: { id: true, title: true, createdAt: true },
  });

  const hasMore = items.length > limit;
  if (hasMore) items.pop();

  return {
    data: items,
    nextCursor: hasMore ? items[items.length - 1].id : null,
  };
}
```

### Select vs Include

```typescript
// GOOD: Select only needed fields (smaller payload, faster query)
const users = await db.user.findMany({
  select: { id: true, email: true, role: true },
});

// AVOID: Include fetches entire related models (over-fetching)
const users = await db.user.findMany({
  include: { posts: { include: { comments: true } } }, // 3-level deep join
});
```

### Transactions

```typescript
// Sequential (array of operations)
const [order, payment] = await db.$transaction([
  db.order.create({ data: orderData }),
  db.payment.create({ data: paymentData }),
]);

// Interactive (when queries depend on each other)
await db.$transaction(async (tx) => {
  const account = await tx.account.findUniqueOrThrow({
    where: { id: accountId },
  });
  if (account.balance < amount) throw new Error('Insufficient balance');
  await tx.account.update({
    where: { id: accountId },
    data: { balance: { decrement: amount } },
  });
});
```

### Raw SQL (Parameterized)

```typescript
// $queryRaw with tagged template — auto-parameterized, SQL-injection safe
const results = await db.$queryRaw`
  SELECT * FROM post
  WHERE to_tsvector('english', title || ' ' || content)
    @@ plainto_tsquery('english', ${searchTerm})
  ORDER BY ts_rank(
    to_tsvector('english', title || ' ' || content),
    plainto_tsquery('english', ${searchTerm})
  ) DESC
  LIMIT ${limit}
`;
```

## Client Extensions

### Soft Delete Extension

```typescript
import { Prisma } from '@prisma/client';

export const softDeleteExtension = Prisma.defineExtension({
  query: {
    $allModels: {
      async delete({ model, args, query }) {
        return (db as any)[model].update({
          ...args,
          data: { deletedAt: new Date() },
        });
      },
      async findMany({ model, args, query }) {
        args.where = { ...args.where, deletedAt: null };
        return query(args);
      },
    },
  },
});

// Usage
const db = new PrismaClient().$extends(softDeleteExtension);
```

## Migration Workflow

| Command | Environment | Purpose |
|---------|------------|---------|
| `npx prisma migrate dev --name add_posts` | Development | Generate + apply migration |
| `npx prisma migrate deploy` | Production/CI | Apply pending migrations (no generation) |
| `npx prisma migrate dev --create-only` | Development | Generate migration SQL without applying (for custom SQL edits) |
| `npx prisma migrate reset` | Development | Drop + recreate + seed |
| `npx prisma db seed` | Development | Run seed script |

### Custom SQL in Migrations

For triggers, RLS, functions — use `--create-only` then edit:

```bash
npx prisma migrate dev --create-only --name add_rls_policies
# Edit the generated SQL file to add custom DDL
npx prisma migrate dev  # Apply
```

## Common Gotchas

| Gotcha | Problem | Solution |
|--------|---------|----------|
| `updateMany` returns count, not records | Can't chain operations | Use `update` for single records or raw SQL |
| `Json` field isn't type-safe | Runtime type errors | Validate with Zod on input/output |
| Case sensitivity | `findFirst({ where: { email }})` is case-sensitive | Use `mode: 'insensitive'` filter |
| `@updatedAt` precision | Prisma sets in app, not DB | Add DB trigger for accuracy |
| Implicit M:N can't have extra fields | No `createdAt` on junction | Use explicit junction model |
| `include` N+1 | Deeply nested includes = massive queries | Use `select` and limit depth |
