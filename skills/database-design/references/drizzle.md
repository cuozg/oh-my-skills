# Drizzle — Schema, Migrations & Queries

Production patterns for Drizzle ORM with PostgreSQL. TypeScript-first, SQL-like syntax, lightweight runtime.

## Schema Definition

Drizzle schemas are plain TypeScript — the schema IS the source of truth.

```typescript
// db/schema.ts
import {
  pgTable, serial, bigint, text, varchar, integer, timestamp,
  jsonb, boolean, uuid, pgEnum, index, uniqueIndex, check,
  primaryKey,
} from 'drizzle-orm/pg-core';
import { sql } from 'drizzle-orm';

// Enum definition
export const statusEnum = pgEnum('status', ['active', 'archived', 'deleted']);

// Table definition
export const user = pgTable('user', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  role: text('role', { enum: ['admin', 'member'] }).notNull().default('member'),
  metadata: jsonb('metadata').$type<{ avatarUrl?: string }>().default({}),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
  deletedAt: timestamp('deleted_at', { withTimezone: true }),
}, (table) => [
  index('idx_user_email').on(table.email),
  check('chk_user_name_length', sql`length(${table.name}) > 0`),
]);

// Table with foreign key
export const post = pgTable('post', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: text('title').notNull(),
  content: text('content').notNull(),
  authorId: uuid('author_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index('idx_post_author').on(table.authorId),
]);

// Junction table (many-to-many)
export const postTag = pgTable('post_tag', {
  postId: uuid('post_id').notNull().references(() => post.id, { onDelete: 'cascade' }),
  tagId: uuid('tag_id').notNull().references(() => tag.id, { onDelete: 'cascade' }),
}, (table) => [
  primaryKey({ columns: [table.postId, table.tagId] }),
  index('idx_post_tag_tag').on(table.tagId),
]);
```

## Column Types Reference

| PostgreSQL Type | Drizzle Function | Example |
|----------------|-----------------|---------|
| `TEXT` | `text('col')` | `text('name').notNull()` |
| `VARCHAR(n)` | `varchar('col', { length: n })` | `varchar('code', { length: 3 })` |
| `INTEGER` | `integer('col')` | `integer('age')` |
| `BIGINT` | `bigint('col', { mode: 'number' })` | `bigint('amount', { mode: 'number' })` |
| `SERIAL` | `serial('col')` | `serial('id').primaryKey()` |
| `UUID` | `uuid('col')` | `uuid('id').defaultRandom()` |
| `BOOLEAN` | `boolean('col')` | `boolean('is_active').default(true)` |
| `TIMESTAMPTZ` | `timestamp('col', { withTimezone: true })` | `timestamp('created_at', { withTimezone: true })` |
| `JSONB` | `jsonb('col')` | `jsonb('data').$type<MyType>()` |
| `TEXT[]` | `text('col').array()` | `text('tags').array()` |
| Custom ENUM | `pgEnum('name', [...])` | See above |

## Connection Setup

```typescript
// db/index.ts
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool, { schema });
```

### Serverless (Neon)

```typescript
import { drizzle } from 'drizzle-orm/neon-http';
import { neon } from '@neondatabase/serverless';
import * as schema from './schema';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

## Relations

Define relations separately from tables to avoid circular imports:

```typescript
// db/relations.ts
import { relations } from 'drizzle-orm';
import { user, post, postTag, tag } from './schema';

export const userRelations = relations(user, ({ many }) => ({
  posts: many(post),
}));

export const postRelations = relations(post, ({ one, many }) => ({
  author: one(user, { fields: [post.authorId], references: [user.id] }),
  postTags: many(postTag),
}));

export const postTagRelations = relations(postTag, ({ one }) => ({
  post: one(post, { fields: [postTag.postId], references: [post.id] }),
  tag: one(tag, { fields: [postTag.tagId], references: [tag.id] }),
}));
```

## Query Patterns

### Select with Filters

```typescript
import { eq, and, gt, like, isNull, desc, sql } from 'drizzle-orm';

// Basic select
const users = await db.select().from(user).where(eq(user.role, 'admin'));

// Multiple conditions
const activePosts = await db.select()
  .from(post)
  .where(and(
    eq(post.authorId, userId),
    isNull(post.deletedAt),
    gt(post.createdAt, lastWeek),
  ))
  .orderBy(desc(post.createdAt))
  .limit(20);

// Select specific columns
const emails = await db.select({ email: user.email }).from(user);
```

### Joins

```typescript
// Left join
const userPosts = await db.select({
  userName: user.name,
  postTitle: post.title,
})
.from(user)
.leftJoin(post, eq(user.id, post.authorId));
```

### Insert / Update / Delete

```typescript
// Insert with returning
const [newUser] = await db.insert(user)
  .values({ email: 'test@example.com', name: 'Test' })
  .returning();

// Upsert (ON CONFLICT)
await db.insert(user)
  .values({ id: userId, email, name })
  .onConflictDoUpdate({
    target: user.id,
    set: { name, updatedAt: new Date() },
  });

// Update
await db.update(user)
  .set({ name: 'New Name', updatedAt: new Date() })
  .where(eq(user.id, userId));

// Soft delete
await db.update(user)
  .set({ deletedAt: new Date() })
  .where(eq(user.id, userId));
```

### Relational Queries (RQB)

```typescript
// Fetch user with posts (uses the relations defined above)
const userWithPosts = await db.query.user.findFirst({
  where: eq(user.id, userId),
  with: { posts: { limit: 10, orderBy: [desc(post.createdAt)] } },
});

// Nested relations
const data = await db.query.post.findMany({
  with: {
    author: true,
    postTags: { with: { tag: true } },
  },
});
```

### Cursor-Based Pagination

```typescript
async function listPosts(cursor?: string, limit = 20) {
  const items = await db.select()
    .from(post)
    .where(cursor
      ? and(isNull(post.deletedAt), lt(post.id, cursor))
      : isNull(post.deletedAt)
    )
    .orderBy(desc(post.createdAt))
    .limit(limit + 1);

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
await db.transaction(async (tx) => {
  const [order] = await tx.insert(orders).values(orderData).returning();
  await tx.insert(orderItems).values(
    items.map((item) => ({ ...item, orderId: order.id }))
  );
});
```

## Advanced PostgreSQL Features

### JSONB Queries

```typescript
// Containment operator (@>)
const redProducts = await db.select()
  .from(product)
  .where(sql`${product.metadata} @> '{"color": "red"}'::jsonb`);

// Extract JSON field
const names = await db.select({
  name: sql<string>`${user.metadata}->>'displayName'`,
}).from(user);
```

### Full-Text Search

```typescript
const results = await db.select()
  .from(post)
  .where(sql`to_tsvector('english', ${post.title} || ' ' || ${post.content})
    @@ plainto_tsquery('english', ${searchTerm})`)
  .orderBy(sql`ts_rank(
    to_tsvector('english', ${post.title} || ' ' || ${post.content}),
    plainto_tsquery('english', ${searchTerm})
  ) DESC`);
```

### Common Table Expressions (CTEs)

```typescript
const activePosts = db.$with('active_posts').as(
  db.select().from(post).where(isNull(post.deletedAt))
);

const result = await db.with(activePosts)
  .select()
  .from(activePosts)
  .where(eq(activePosts.authorId, userId));
```

### Prepared Statements

```typescript
// Prepare once, execute many times (reduces parsing overhead)
const findUserByEmail = db.select()
  .from(user)
  .where(eq(user.email, sql.placeholder('email')))
  .prepare('find_user_by_email');

const result = await findUserByEmail.execute({ email: 'test@example.com' });
```

## Migration Workflow

| Command | Purpose |
|---------|---------|
| `npx drizzle-kit generate` | Generate SQL migration files from schema diff |
| `npx drizzle-kit migrate` | Apply pending migrations |
| `npx drizzle-kit push` | Push schema directly (dev only, no migration files) |
| `npx drizzle-kit pull` | Introspect existing DB into Drizzle schema |
| `npx drizzle-kit studio` | Open Drizzle Studio (visual DB browser) |

### drizzle.config.ts

```typescript
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  dialect: 'postgresql',
  schema: './src/db/schema.ts',
  out: './drizzle',
  dbCredentials: { url: process.env.DATABASE_URL! },
});
```

## Drizzle vs Prisma

| Aspect | Drizzle | Prisma |
|--------|---------|--------|
| Schema language | TypeScript | `.prisma` DSL |
| Bundle size | ~7KB | ~2MB (includes engine) |
| Edge/serverless | Native support | Requires Accelerate or Data Proxy |
| SQL control | Full (SQL-like API) | Abstracted (escape to `$queryRaw`) |
| Type safety | Inferred from schema | Generated from `prisma generate` |
| Studio/GUI | `drizzle-kit studio` | Prisma Studio |
| Migrations | SQL files (editable) | SQL files (less editable) |
| Best for | Performance, SQL control, edge | Rapid development, complex relations |
