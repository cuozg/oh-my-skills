# API Routes — Next.js App Router Route Handlers

Write route handlers in `app/api/` using the Web Request/Response API extended by NextRequest/NextResponse.

## File Convention

```
app/api/<resource>/route.ts          # Collection: GET (list), POST (create)
app/api/<resource>/[id]/route.ts     # Item: GET (read), PUT (update), DELETE (remove)
```

Export named functions matching HTTP methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.

## Standard Route Handler

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const createSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().optional(),
});

const listQuerySchema = z.object({
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const query = listQuerySchema.safeParse({
    cursor: searchParams.get('cursor') ?? undefined,
    limit: searchParams.get('limit') ?? undefined,
  });
  if (!query.success) {
    return NextResponse.json(
      { error: 'Invalid query parameters', details: query.error.flatten().fieldErrors },
      { status: 400 },
    );
  }
  const { cursor, limit } = query.data;

  const items = await db.item.findMany({
    take: limit + 1,
    ...(cursor ? { cursor: { id: cursor }, skip: 1 } : {}),
    orderBy: { createdAt: 'desc' },
  });

  const hasMore = items.length > limit;
  if (hasMore) items.pop();

  return NextResponse.json({
    data: items,
    nextCursor: hasMore ? items[items.length - 1].id : null,
  });
}

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => null);
  if (!body) return NextResponse.json({ error: 'Invalid JSON' }, { status: 400 });

  const result = createSchema.safeParse(body);
  if (!result.success) {
    return NextResponse.json(
      { error: 'Validation failed', details: result.error.flatten().fieldErrors },
      { status: 400 },
    );
  }

  const item = await db.item.create({ data: result.data });
  return NextResponse.json({ data: item }, { status: 201 });
}
```

## Dynamic Route Params

```typescript
// app/api/posts/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const post = await db.post.findUnique({ where: { id } });
  if (!post) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json({ data: post });
}
```

## Runtime & Caching

```typescript
export const runtime = 'nodejs';       // Default. Use 'edge' for low-latency global distribution
export const dynamic = 'force-dynamic'; // Disable response caching for mutable endpoints
```

Edge runtime cannot use Node.js APIs (fs, net, crypto.createHash). Use `jose` instead of `jsonwebtoken`, `@upstash/redis` instead of `ioredis`.

## CORS Helper

```typescript
const corsHeaders = {
  'Access-Control-Allow-Origin': process.env.ALLOWED_ORIGIN ?? '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export async function OPTIONS() {
  return new Response(null, { status: 204, headers: corsHeaders });
}

export async function GET(request: NextRequest) {
  // ... your logic
  return NextResponse.json(data, { headers: corsHeaders });
}
```

## Streaming Response

```typescript
export async function GET() {
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      for (const chunk of data) {
        controller.enqueue(encoder.encode(JSON.stringify(chunk) + '\n'));
        await new Promise((r) => setTimeout(r, 100));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: { 'Content-Type': 'application/x-ndjson' },
  });
}
```

## Rules

- Always validate input with Zod before processing — both request bodies AND query parameters
- Return standardized error shape: `{ error: string, details?: unknown }`
- Wrap response data in `{ data: ... }` envelope for consistency
- Use cursor-based pagination for lists (never OFFSET for large datasets)
- Set `dynamic = 'force-dynamic'` on mutable endpoints
- Catch `request.json()` parse failures — don't let them throw 500
