# Validation & Errors — Zod Schemas & Response Standards

Standardized patterns for input validation, error responses, and common parameter parsing.

## Zod Validation Helper

Reusable wrapper for API route handlers:

```typescript
// lib/validate.ts
import { NextResponse } from 'next/server';
import { z, type ZodSchema } from 'zod';

export async function validateBody<T>(
  request: Request,
  schema: ZodSchema<T>,
): Promise<{ data: T } | { error: NextResponse }> {
  const body = await request.json().catch(() => null);
  if (!body) {
    return { error: NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 }) };
  }

  const result = schema.safeParse(body);
  if (!result.success) {
    return {
      error: NextResponse.json(
        { error: 'Validation failed', details: result.error.flatten().fieldErrors },
        { status: 400 },
      ),
    };
  }

  return { data: result.data };
}
```

Usage:

```typescript
export async function POST(request: NextRequest) {
  const validation = await validateBody(request, createUserSchema);
  if ('error' in validation) return validation.error;

  const user = await db.user.create({ data: validation.data });
  return NextResponse.json({ data: user }, { status: 201 });
}
```

## Pagination Params

```typescript
// lib/pagination.ts
import { z } from 'zod';

export const paginationSchema = z.object({
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

export function parsePagination(searchParams: URLSearchParams) {
  return paginationSchema.parse({
    cursor: searchParams.get('cursor') ?? undefined,
    limit: searchParams.get('limit') ?? undefined,
  });
}
```

## Common Zod Patterns

```typescript
// IDs
const idSchema = z.string().uuid();
const cuidSchema = z.string().cuid();

// Enums
const roleSchema = z.enum(['admin', 'member', 'viewer']);

// Date ranges
const dateRangeSchema = z.object({
  from: z.coerce.date(),
  to: z.coerce.date(),
}).refine((d) => d.to > d.from, { message: 'End date must be after start date' });

// Pagination + filters
const listQuerySchema = z.object({
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  search: z.string().max(200).optional(),
  sortBy: z.enum(['createdAt', 'updatedAt', 'name']).default('createdAt'),
  sortOrder: z.enum(['asc', 'desc']).default('desc'),
  status: z.enum(['active', 'archived', 'draft']).optional(),
});

// File upload metadata
const uploadSchema = z.object({
  filename: z.string().min(1).max(255),
  contentType: z.string().refine(
    (t) => ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'].includes(t),
    { message: 'Unsupported file type' },
  ),
  size: z.number().max(10 * 1024 * 1024, 'File must be under 10MB'),
});
```

## Standardized Error Response

Every error response should follow this shape:

```typescript
type ErrorResponse = {
  error: string;                          // Human-readable message
  details?: Record<string, string[]>;     // Field-level validation errors
  code?: string;                          // Machine-readable error code
};
```

```typescript
// lib/errors.ts
import { NextResponse } from 'next/server';

export function badRequest(message: string, details?: Record<string, string[]>) {
  return NextResponse.json({ error: message, details }, { status: 400 });
}

export function unauthorized(message = 'Authentication required') {
  return NextResponse.json({ error: message }, { status: 401 });
}

export function forbidden(message = 'Insufficient permissions') {
  return NextResponse.json({ error: message }, { status: 403 });
}

export function notFound(resource = 'Resource') {
  return NextResponse.json({ error: `${resource} not found` }, { status: 404 });
}

export function conflict(message: string) {
  return NextResponse.json({ error: message }, { status: 409 });
}

export function internalError(error: unknown) {
  console.error('Internal error:', error);
  return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
}
```

## Webhook Signature Verification

```typescript
import { createHmac, timingSafeEqual } from 'crypto';

export function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string,
): boolean {
  const expected = createHmac('sha256', secret).update(payload).digest('hex');
  const sig = signature.replace('sha256=', '');

  return timingSafeEqual(
    Buffer.from(expected, 'hex'),
    Buffer.from(sig, 'hex'),
  );
}

// Usage in route handler
export async function POST(request: NextRequest) {
  const body = await request.text();
  const sig = request.headers.get('x-signature') ?? '';

  if (!verifyWebhookSignature(body, sig, process.env.WEBHOOK_SECRET!)) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  const data = JSON.parse(body);
  // Process webhook...
  return NextResponse.json({ received: true });
}
```

## Rules

- Every route handler: validate all input (body, params, query) with Zod
- Never trust `request.json()` — always wrap in `.catch(() => null)`
- Use `z.coerce.number()` for query params (they arrive as strings)
- Log full errors server-side, return generic messages to clients
- Use `timingSafeEqual` for any signature/token comparison (prevents timing attacks)
