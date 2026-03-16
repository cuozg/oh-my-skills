# Seed Data — Patterns for PostgreSQL

Strategies for seeding PostgreSQL databases with realistic, reproducible data. Covers Prisma and Drizzle workflows, factory patterns, and environment-aware seeding.

## Prisma Seed Setup

### Configuration

```json
// package.json
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

```bash
# Run seed
npx prisma db seed

# Reset + seed (drops DB, applies migrations, runs seed)
npx prisma migrate reset
```

### Basic Seed Script

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const db = new PrismaClient();

async function main() {
  // Upsert for idempotency — safe to re-run
  const admin = await db.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      name: 'Admin User',
      role: 'ADMIN',
    },
  });

  const org = await db.organization.upsert({
    where: { slug: 'acme' },
    update: {},
    create: {
      name: 'Acme Corp',
      slug: 'acme',
    },
  });

  // Create dependent records
  await db.membership.upsert({
    where: {
      userId_organizationId: { userId: admin.id, organizationId: org.id },
    },
    update: {},
    create: {
      userId: admin.id,
      organizationId: org.id,
      role: 'OWNER',
    },
  });

  console.log('Seed complete:', { admin: admin.id, org: org.id });
}

main()
  .catch((e) => {
    console.error('Seed failed:', e);
    process.exit(1);
  })
  .finally(() => db.$disconnect());
```

## Drizzle Seed Setup

### Option A: Custom Script (Full Control)

```json
// package.json
{
  "scripts": {
    "db:seed": "tsx src/db/seed.ts"
  }
}
```

```typescript
// src/db/seed.ts
import { db } from './index';
import { user, organization, membership } from './schema';

async function main() {
  console.log('Seeding database...');

  // Upsert pattern with ON CONFLICT
  const [admin] = await db.insert(user)
    .values({
      email: 'admin@example.com',
      name: 'Admin User',
      role: 'admin',
    })
    .onConflictDoUpdate({
      target: user.email,
      set: { name: 'Admin User' },
    })
    .returning();

  const [org] = await db.insert(organization)
    .values({
      name: 'Acme Corp',
      slug: 'acme',
    })
    .onConflictDoUpdate({
      target: organization.slug,
      set: { name: 'Acme Corp' },
    })
    .returning();

  await db.insert(membership)
    .values({
      userId: admin.id,
      organizationId: org.id,
      role: 'owner',
    })
    .onConflictDoNothing();

  console.log('Seed complete:', { admin: admin.id, org: org.id });
}

main()
  .catch((e) => {
    console.error('Seed failed:', e);
    process.exit(1);
  })
  .finally(() => process.exit(0));
```

### Option B: drizzle-seed (Schema-Aware Auto-Generation)

The `drizzle-seed` package generates realistic data based on column types and constraints automatically:

```bash
npm install drizzle-seed
```

```typescript
import { seed } from 'drizzle-seed';
import * as schema from './schema';
import { db } from './db';

async function main() {
  // Deterministic seed — same number = same data every time
  await seed(db, schema, { seed: 42 }).refine((f) => ({
    user: {
      count: 50,
      columns: {
        email: f.email(),
        name: f.firstName(),
      },
    },
    project: {
      count: 200,
      // Automatically resolves FK relationships from schema
    },
  }));
}

main().catch(console.error);
```

`drizzle-seed` reads your schema's column types, foreign keys, and constraints to generate appropriate data without manual factory definitions. Use it for dev environments; use Option A for reference/system data that must be exact.

## Factory Pattern

Factory functions generate realistic data with sensible defaults. Override only what matters for each test case.

```typescript
// prisma/factories.ts (or src/db/factories.ts for Drizzle)
import { faker } from '@faker-js/faker';

// Deterministic seed for reproducible tests
faker.seed(42);

export function buildUser(overrides: Partial<UserCreateInput> = {}) {
  return {
    email: faker.internet.email().toLowerCase(),
    name: faker.person.fullName(),
    role: 'member' as const,
    ...overrides,
  };
}

export function buildOrganization(overrides: Partial<OrgCreateInput> = {}) {
  return {
    name: faker.company.name(),
    slug: faker.helpers.slugify(faker.company.name()).toLowerCase(),
    plan: 'free' as const,
    ...overrides,
  };
}

export function buildProject(overrides: Partial<ProjectCreateInput> = {}) {
  return {
    name: faker.commerce.productName(),
    description: faker.lorem.sentence(),
    status: 'active' as const,
    ...overrides,
  };
}

// Usage in seed script:
// const users = Array.from({ length: 50 }, () => buildUser());
// await db.insert(user).values(users);
```

### Factory with Relations (Prisma)

```typescript
export async function createUserWithOrg(
  db: PrismaClient,
  userOverrides: Partial<UserCreateInput> = {},
  orgOverrides: Partial<OrgCreateInput> = {},
) {
  const org = await db.organization.create({
    data: buildOrganization(orgOverrides),
  });

  const user = await db.user.create({
    data: {
      ...buildUser(userOverrides),
      memberships: {
        create: { organizationId: org.id, role: 'OWNER' },
      },
    },
    include: { memberships: true },
  });

  return { user, org };
}
```

## Environment-Aware Seeding

Different environments need different seed data:

```typescript
// prisma/seed.ts
type SeedEnv = 'development' | 'staging' | 'test';

const SEED_ENV = (process.env.SEED_ENV ?? 'development') as SeedEnv;

async function main() {
  // Always seed: system-required reference data
  await seedReferenceData();

  if (SEED_ENV === 'development') {
    // Rich dataset for local development
    await seedDemoData({ userCount: 50, projectCount: 200 });
  }

  if (SEED_ENV === 'staging') {
    // Minimal realistic data for QA
    await seedDemoData({ userCount: 10, projectCount: 20 });
  }

  if (SEED_ENV === 'test') {
    // Bare minimum for test isolation
    await seedTestFixtures();
  }
}
```

### Reference Data (Always Seeded)

Lookup tables, system config, and default values that the app requires:

```typescript
async function seedReferenceData() {
  const categories = [
    { slug: 'engineering', name: 'Engineering', sortOrder: 1 },
    { slug: 'design', name: 'Design', sortOrder: 2 },
    { slug: 'marketing', name: 'Marketing', sortOrder: 3 },
  ];

  for (const cat of categories) {
    await db.category.upsert({
      where: { slug: cat.slug },
      update: { name: cat.name, sortOrder: cat.sortOrder },
      create: cat,
    });
  }
}
```

## Batch Seeding (Large Datasets)

For development environments that need thousands of rows:

```typescript
// Batch insert for performance (Drizzle)
async function seedDemoData({ userCount = 100, projectCount = 500 }) {
  const BATCH_SIZE = 100;
  const users = Array.from({ length: userCount }, () => buildUser());

  // Insert in batches to avoid parameter limit (~65,535 in PG)
  for (let i = 0; i < users.length; i += BATCH_SIZE) {
    const batch = users.slice(i, i + BATCH_SIZE);
    await db.insert(user).values(batch).onConflictDoNothing();
  }

  // Fetch inserted users for FK references
  const insertedUsers = await db.select({ id: user.id }).from(user);

  const projects = Array.from({ length: projectCount }, () => ({
    ...buildProject(),
    ownerId: faker.helpers.arrayElement(insertedUsers).id,
  }));

  for (let i = 0; i < projects.length; i += BATCH_SIZE) {
    const batch = projects.slice(i, i + BATCH_SIZE);
    await db.insert(project).values(batch).onConflictDoNothing();
  }

  console.log(`Seeded ${userCount} users, ${projectCount} projects`);
}
```

## Seed Ordering

Tables with foreign keys must be seeded in dependency order. Tear down in reverse order.

```typescript
// Correct order: parents first, children last
async function seedAll() {
  // 1. Independent tables (no FKs)
  await seedCategories();
  await seedPlans();

  // 2. Root entities
  await seedOrganizations();
  await seedUsers();

  // 3. Junction / dependent tables
  await seedMemberships();    // depends on users + orgs
  await seedProjects();       // depends on orgs
  await seedTasks();          // depends on projects

  // 4. Leaf entities
  await seedComments();       // depends on tasks + users
}

// For test cleanup, reverse the order:
async function cleanAll() {
  await db.delete(comment);
  await db.delete(task);
  await db.delete(project);
  await db.delete(membership);
  await db.delete(user);
  await db.delete(organization);
  await db.delete(category);
  await db.delete(plan);
}
```

## Rules

- **Always use upserts** — seeds must be idempotent (safe to re-run)
- **Set `faker.seed()`** for deterministic data — same seed = same data across machines
- **Batch inserts** for large datasets — don't insert row-by-row
- **Separate reference data from demo data** — reference data runs in all environments, demo data only in dev/staging
- **Never seed production** with fake data — use a flag or environment check to prevent accidents
- **Match FK dependency order** — seed parents before children, clean children before parents
- **Use `onConflictDoNothing()` / `onConflictDoUpdate()`** — not raw `INSERT` that fails on duplicates
