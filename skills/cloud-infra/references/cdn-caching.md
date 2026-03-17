# CDN Caching Patterns

## Cache-Control Recipes

### Static Assets (Content-Hashed)
```
Cache-Control: public, max-age=31536000, immutable
```
Use for: JS bundles, CSS, images with hash in filename (`main.a1b2c3.js`).
Next.js `/_next/static/` uses this automatically.

### Static HTML / SSG Pages
```
Cache-Control: public, max-age=0, must-revalidate
```
Use for: Pre-rendered pages that should revalidate on every request but can be cached at CDN.

### Dynamic API with CDN Cache
```
Cache-Control: public, s-maxage=60, stale-while-revalidate=300
```
Use for: API responses safe to cache at edge. `s-maxage` = CDN TTL, `stale-while-revalidate` = serve stale while refreshing.

### User-Specific / Private Data
```
Cache-Control: private, no-store
```
Use for: Auth responses, user profiles, cart data. NEVER cache at CDN.

### File Downloads
```
Cache-Control: public, max-age=86400
Content-Disposition: attachment; filename="report.pdf"
```

## Next.js Response Headers

```typescript
// app/api/products/route.ts
export async function GET() {
  const products = await db.product.findMany();

  return Response.json(products, {
    headers: {
      "Cache-Control": "public, s-maxage=60, stale-while-revalidate=300",
    },
  });
}
```

## Vercel ISR (Incremental Static Regeneration)

```typescript
// app/products/[id]/page.tsx
export const revalidate = 60; // Revalidate every 60 seconds

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);
  return <ProductView product={product} />;
}
```

### On-Demand Revalidation

```typescript
// app/api/revalidate/route.ts
import { revalidateTag, revalidatePath } from "next/cache";

export async function POST(request: Request) {
  const { tag, path, secret } = await request.json();

  if (secret !== process.env.REVALIDATION_SECRET) {
    return Response.json({ error: "Invalid secret" }, { status: 401 });
  }

  if (tag) {
    revalidateTag(tag);
    return Response.json({ revalidated: true, tag });
  }

  if (path) {
    revalidatePath(path);
    return Response.json({ revalidated: true, path });
  }

  return Response.json({ error: "Missing tag or path" }, { status: 400 });
}
```

```typescript
// Usage in data fetching
const products = await fetch("https://api.example.com/products", {
  next: { tags: ["products"], revalidate: 60 },
});
```

## Cloudflare Cache Rules

Replace deprecated Page Rules with Cache Rules (Dashboard → Caching → Cache Rules):

```
// Rule: Cache API responses at edge
When: hostname eq "api.example.com" AND URI path starts with "/api/public/"
Then: Cache eligible → Edge TTL: 60s, Browser TTL: 0s

// Rule: Bypass cache for authenticated requests
When: Cookie contains "session_token"
Then: Bypass cache

// Rule: Cache static assets aggressively
When: URI path starts with "/static/" OR URI path starts with "/_next/static/"
Then: Edge TTL: 365 days, Browser TTL: 365 days
```

## Workers Cache API

```typescript
// Workers: programmatic cache control
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const cache = caches.default;
    const cacheKey = new Request(request.url, request);

    // Check cache first
    let response = await cache.match(cacheKey);
    if (response) return response;

    // Generate response
    const data = await fetchFromOrigin(request);
    response = new Response(JSON.stringify(data), {
      headers: {
        "content-type": "application/json",
        "cache-control": "public, s-maxage=60",
      },
    });

    // Store in cache (non-blocking)
    const ctx = { waitUntil: (p: Promise<unknown>) => p };
    ctx.waitUntil(cache.put(cacheKey, response.clone()));

    return response;
  },
};
```

## CDN-Specific Headers

```typescript
// Target specific CDN layers independently
const headers = new Headers();

// Browser cache: 0s (always revalidate)
headers.set("Cache-Control", "public, max-age=0, must-revalidate");

// CDN cache: 60s (Cloudflare, Vercel, any standards-compliant CDN)
headers.set("CDN-Cache-Control", "max-age=60");

// Cloudflare-only: override all other CDN headers
headers.set("Cloudflare-CDN-Cache-Control", "max-age=120");
```

Priority: `Cloudflare-CDN-Cache-Control` > `CDN-Cache-Control` > `Cache-Control` (s-maxage) > `Cache-Control` (max-age)

## Image Optimization

```typescript
// Cloudflare Image Resizing (via Workers or URL convention)
// https://example.com/cdn-cgi/image/width=400,quality=80,format=auto/original-image.jpg

// Next.js Image Optimization (built-in on Vercel)
import Image from "next/image";
<Image src="/photo.jpg" width={400} height={300} alt="Photo" />
// Vercel automatically serves WebP/AVIF, resizes, and caches at edge
```

## Common Mistakes

- **Caching HTML too long** — Users see stale content, no way to force refresh
- **Missing `Vary` header** — Same URL serves different content (e.g., `Accept: webp`) without `Vary: Accept`
- **Caching `Set-Cookie`** — CDN serves one user's session cookie to another user
- **No `stale-while-revalidate`** — Cold cache hits are slow; always pair with `s-maxage`
- **Forgetting `immutable`** — Browser re-checks hashed assets on every navigation without it
- **`s-maxage` too high without purge** — Content updates not visible; pair with on-demand revalidation

## Uncacheable Routes

```typescript
// app/api/webhooks/stripe/route.ts
export const dynamic = "force-dynamic"; // NEVER cache this route

export async function POST(request: Request) {
  // Webhook handlers, auth endpoints, and mutation routes
  // must always be force-dynamic to bypass ISR/caching
}
```

Use `export const dynamic = "force-dynamic"` for routes that must never be cached: webhook handlers, auth callbacks, payment endpoints, and any route with side effects.

## Resilience with stale-if-error

```
Cache-Control: public, s-maxage=60, stale-while-revalidate=300, stale-if-error=86400
```

`stale-if-error` serves stale content when the origin returns 5xx errors — keeps your app available during outages. Set it high (e.g., 86400 = 24h) for non-critical content.

## Tag-Based Caching with next/cache

```typescript
import { unstable_cache } from "next/cache";

const getCachedProducts = unstable_cache(
  async () => db.product.findMany(),
  ["products"], // cache key
  { tags: ["products"], revalidate: 60 }
);

// Invalidate via: revalidateTag("products")
```

Use `unstable_cache` for fine-grained caching of database queries and expensive computations with tag-based invalidation.

## Purge Cache On-Demand (Cloudflare API)

Use the Cloudflare API to programmatically purge cached assets at the edge after content updates.

```typescript
// lib/cloudflare-purge.ts
import { z } from "zod";

const purgeResultSchema = z.object({
  success: z.boolean(),
  errors: z.array(z.object({ code: z.number(), message: z.string() })),
});

/**
 * Purge specific URLs from Cloudflare CDN cache.
 * Requires CF_API_TOKEN and CF_ZONE_ID env vars.
 * API docs: https://developers.cloudflare.com/api/operations/zone-purge
 */
export async function purgeCloudflareCache(urls: string[]): Promise<{ success: boolean; errors: string[] }> {
  const zoneId = process.env.CF_ZONE_ID;
  const apiToken = process.env.CF_API_TOKEN;

  if (!zoneId || !apiToken) {
    throw new Error("Missing CF_ZONE_ID or CF_API_TOKEN environment variables");
  }

  const response = await fetch(
    `https://api.cloudflare.com/client/v4/zones/${zoneId}/purge_cache`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ files: urls }),
    }
  );

  const data = await response.json();
  const parsed = purgeResultSchema.safeParse(data);

  if (!parsed.success) {
    return { success: false, errors: ["Unexpected API response format"] };
  }

  return {
    success: parsed.data.success,
    errors: parsed.data.errors.map((e) => e.message),
  };
}

/**
 * Purge everything in the zone. Use sparingly — affects all cached content.
 */
export async function purgeAllCloudflareCache(): Promise<{ success: boolean; errors: string[] }> {
  const zoneId = process.env.CF_ZONE_ID;
  const apiToken = process.env.CF_API_TOKEN;

  if (!zoneId || !apiToken) {
    throw new Error("Missing CF_ZONE_ID or CF_API_TOKEN environment variables");
  }

  const response = await fetch(
    `https://api.cloudflare.com/client/v4/zones/${zoneId}/purge_cache`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ purge_everything: true }),
    }
  );

  const data = await response.json();
  const parsed = purgeResultSchema.safeParse(data);

  if (!parsed.success) {
    return { success: false, errors: ["Unexpected API response format"] };
  }

  return {
    success: parsed.data.success,
    errors: parsed.data.errors.map((e) => e.message),
  };
}
```

### Usage: Purge After Form Submission

```typescript
// app/api/content/update/route.ts
import { revalidatePath, revalidateTag } from "next/cache";
import { purgeCloudflareCache } from "@/lib/cloudflare-purge";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  const { slug, secret } = await request.json();

  if (secret !== process.env.REVALIDATION_SECRET) {
    return Response.json({ error: "Unauthorized" }, { status: 401 });
  }

  // 1. Purge Next.js / Vercel cache
  revalidatePath(`/products/${slug}`);
  revalidateTag("products");

  // 2. Purge Cloudflare CDN cache
  const cdnResult = await purgeCloudflareCache([
    `https://example.com/products/${slug}`,
    `https://example.com/api/products/${slug}`,
  ]);

  return Response.json({
    revalidated: true,
    cdnPurged: cdnResult.success,
  });
}
```

**Key notes:**
- `purge_cache` endpoint: `POST /client/v4/zones/{zone_id}/purge_cache`
- Auth: `Authorization: Bearer <API_TOKEN>` (API token with Zone → Cache Purge → Edit permission)
- Purge by URL: `{ "files": ["https://example.com/page"] }` (max 30 URLs per call)
- Purge everything: `{ "purge_everything": true }` — use sparingly
- Purge propagation: ~30 seconds globally

### Usage in Webhook Handler

```typescript
// app/api/webhooks/product-update/route.ts
import { purgeCloudflareCache } from "@/lib/cloudflare-purge"
import crypto from "crypto"

export async function POST(req: Request) {
  const rawBody = await req.text()

  // Validate webhook signature
  const signature = req.headers.get("x-webhook-signature")
  const expected = crypto
    .createHmac("sha256", process.env.WEBHOOK_SECRET!)
    .update(rawBody)
    .digest("hex")

  if (!crypto.timingSafeEqual(Buffer.from(signature!), Buffer.from(expected))) {
    return new Response("Unauthorized", { status: 401 })
  }

  const body = JSON.parse(rawBody)

  // Purge affected paths
  await purgeCloudflareCache([
    `https://example.com/products/${body.productId}`,
    "https://example.com/products",
  ])

  return Response.json({ success: true })
}

export const dynamic = "force-dynamic"
```

**Common Purge Patterns:**

| Use Case | Payload |
|----------|---------|
| Purge single URL | `{ "files": ["https://example.com/page"] }` |
| Purge everything | `{ "purge_everything": true }` |
| Purge by cache tag | `{ "tags": ["products", "homepage"] }` (Enterprise only) |
