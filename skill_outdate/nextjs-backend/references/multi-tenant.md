# Multi-Tenant — Architecture & Implementation

Patterns for building multi-tenant Next.js applications with PostgreSQL data isolation.

## Strategy Selection

| Strategy | Isolation | Complexity | Best For |
|----------|-----------|------------|----------|
| Shared schema + `tenant_id` | Low (app-enforced) | Low | Early-stage SaaS, < 100 tenants |
| Shared schema + RLS | High (DB-enforced) | Medium | Production SaaS (Notion, Slack) |
| Schema-per-tenant | High | High | Enterprise, compliance-heavy |
| Database-per-tenant | Maximum | Very High | Healthcare, finance, government |

**Default recommendation**: Shared schema with PostgreSQL Row-Level Security (RLS). It prevents "forgotten WHERE clause" bugs at the database level.

## Tenant Resolution (Middleware)

### Subdomain-Based (`tenant.app.com`)

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

export function middleware(req: NextRequest) {
  const hostname = req.headers.get('host') ?? '';
  const subdomain = hostname.split('.')[0];

  // Skip for main app domain, localhost, or API routes
  if (subdomain === 'www' || subdomain === 'app' || hostname.startsWith('localhost')) {
    return NextResponse.next();
  }

  // Rewrite to tenant-scoped route group
  const url = req.nextUrl.clone();
  url.pathname = `/tenant/${subdomain}${url.pathname}`;
  return NextResponse.rewrite(url);
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Path-Based (`app.com/[tenant]/dashboard`)

Use a route group with a dynamic `[tenant]` segment:

```
app/
  (tenant)/
    [tenant]/
      dashboard/page.tsx
      settings/page.tsx
```

### From JWT Claims

```typescript
// lib/tenant.ts
import { auth } from '@/auth';

export async function getCurrentTenantId(): Promise<string> {
  const session = await auth();
  if (!session?.user?.tenantId) throw new Error('No tenant context');
  return session.user.tenantId;
}
```

## PostgreSQL Row-Level Security (RLS)

```sql
-- 1. Enable RLS on tenant-scoped tables
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- 2. Create isolation policy using a session variable
CREATE POLICY tenant_isolation ON projects
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- 3. Force RLS even for table owners
ALTER TABLE projects FORCE ROW LEVEL SECURITY;
```

## Prisma Tenant Extension

Wraps every query in a transaction that sets the PostgreSQL session variable for RLS.

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
            // Use parameterized query — never interpolate tenantId into SQL
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

export type TenantPrismaClient = ReturnType<typeof getTenantDb>;
```

### Tenant Context Helper

Reads the tenant ID from server-set headers. Always pair with the middleware above.

```typescript
// lib/tenant.ts
import { headers } from 'next/headers';

export async function getCurrentTenantId(): Promise<string> {
  const headersList = await headers();
  const tenantId = headersList.get('x-tenant-id');
  if (!tenantId) throw new Error('No tenant context — is middleware configured?');
  return tenantId;
}

export async function getTenantSlug(): Promise<string | null> {
  const headersList = await headers();
  return headersList.get('x-tenant-slug');
}
```

Usage in server component or action:

```typescript
const tenantId = await getCurrentTenantId();
const tenantDb = getTenantDb(tenantId);
const projects = await tenantDb.project.findMany(); // RLS filters automatically
```

## Tenant Provisioning Flow

```typescript
'use server';

export async function createTenant(formData: FormData) {
  const session = await auth();
  if (!session?.user) throw new Error('Unauthorized');

  const name = formData.get('name') as string;

  await db.$transaction(async (tx) => {
    // 1. Create tenant
    const tenant = await tx.tenant.create({
      data: { name, slug: slugify(name) },
    });

    // 2. Create membership (owner role)
    await tx.membership.create({
      data: {
        userId: session.user.id,
        tenantId: tenant.id,
        role: 'owner',
      },
    });

    // 3. Set up RLS session variable for initial data
    await tx.$queryRawUnsafe(
      `SELECT set_config('app.current_tenant_id', $1, true)`,
      tenant.id,
    );

    // 4. Seed default data (optional)
    await tx.project.create({
      data: { name: 'My First Project', tenantId: tenant.id },
    });
  });

  revalidatePath('/');
  redirect('/dashboard');
}
```

## Stripe Billing per Tenant

```typescript
// Webhook handler: app/api/webhooks/stripe/route.ts
import Stripe from 'stripe';

export async function POST(req: Request) {
  const body = await req.text();
  const sig = req.headers.get('stripe-signature')!;
  const event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);

  if (event.type === 'customer.subscription.updated') {
    const subscription = event.data.object as Stripe.Subscription;
    const tenantId = subscription.metadata.tenantId;

    await db.tenant.update({
      where: { id: tenantId },
      data: {
        plan: subscription.items.data[0].price.lookup_key,
        subscriptionStatus: subscription.status,
      },
    });
  }

  return new Response('OK', { status: 200 });
}
```

## Rules

- Always resolve tenant context before any database query
- Use `SET LOCAL` (not `SET`) for RLS session vars — scoped to transaction, not connection
- Use parameterized queries (`$1` placeholder) when setting RLS vars — never interpolate tenant IDs into SQL strings
- Never trust client-provided tenant IDs — derive from session/JWT
- Use the `globalThis` singleton pattern for the base Prisma client
- Test cross-tenant isolation: verify tenant A cannot read tenant B's data
