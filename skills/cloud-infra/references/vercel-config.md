# Vercel Configuration

## vercel.json Structure

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "regions": ["sfo1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" }
      ]
    },
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/proxy/:path*",
      "destination": "https://external-api.example.com/:path*"
    }
  ],
  "crons": [
    {
      "path": "/api/cron/cleanup",
      "schedule": "0 */6 * * *"
    }
  ]
}
```

## Environment Variables

**Types:**
- **Plain** — Visible in logs, build output. Use for non-secret config.
- **Secret** — Encrypted at rest, masked in logs. Use for API keys, tokens.
- **Sensitive** — Like Secret, also redacted from Vercel CLI output.

```bash
# Pull env vars to local .env.local
vercel env pull .env.local

# Add via CLI
vercel env add R2_ACCOUNT_ID production
vercel env add R2_SECRET_ACCESS_KEY production --sensitive
```

**Runtime access:**
```typescript
// Available in server components, route handlers, middleware
process.env.R2_ACCOUNT_ID    // Plain
process.env.R2_SECRET_ACCESS_KEY  // Secret — only available server-side

// Branch-based config
const isProd = process.env.VERCEL_ENV === "production";
const apiUrl = isProd ? "https://api.prod.com" : "https://api.staging.com";
```

**Never commit `.env.local`** — add to `.gitignore`.

## Functions Configuration

```json
{
  "functions": {
    "app/api/upload/route.ts": {
      "memory": 1024,
      "maxDuration": 60
    },
    "app/api/process/route.ts": {
      "memory": 3008,
      "maxDuration": 300
    }
  }
}
```

**Key limits (Pro plan):**
- `memory`: 128–3008 MB (default 1024)
- `maxDuration`: Up to 300s (Pro), 60s (Hobby)
- `regions`: Deploy to specific regions `["sfo1", "iad1"]`

## Edge Runtime

```typescript
// app/api/fast/route.ts
export const runtime = "edge";

export async function GET(request: Request) {
  // Runs on Cloudflare Workers-like edge network
  // No Node.js APIs — use Web APIs only
  return new Response(JSON.stringify({ fast: true }), {
    headers: { "content-type": "application/json" },
  });
}
```

## Monorepo Setup (Turborepo)

```json
// vercel.json (root)
{
  "buildCommand": "cd ../.. && npx turbo build --filter=web",
  "installCommand": "npm install --prefix ../..",
  "framework": "nextjs"
}
```

**Ignore builds** for unchanged apps:
```bash
# In project settings → Build & Development Settings → Ignored Build Step
npx turbo-ignore
```

## Domains

```typescript
// Apex redirect for SEO (vercel.json)
{
  "redirects": [
    {
      "source": "/:path((?!api/).*)",
      "has": [{ "type": "host", "value": "www.example.com" }],
      "destination": "https://example.com/:path",
      "permanent": true
    }
  ]
}
```

- Auto SSL provisioned on deploy
- `_vercel` TXT record for domain verification
- Wildcard domains supported on Pro plan

## Cron Jobs

```typescript
// app/api/cron/cleanup/route.ts
export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  // Verify cron secret to prevent unauthorized access
  const authHeader = request.headers.get("authorization");
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response("Unauthorized", { status: 401 });
  }

  // Cleanup logic
  await deleteExpiredUploads();

  return Response.json({ cleaned: true });
}
```

## Middleware Patterns

Next.js middleware runs **before** every matched request at the edge. Place `middleware.ts` at the project root (or `src/middleware.ts`).

**Key Rules:**
- Must return `NextResponse` for pass-through, redirect, rewrite, or custom response
- Use `matcher` config to limit to specific routes — avoids running on static assets
- Runs in Edge runtime: no `fs`, `Buffer`, or Node.js-only APIs
- `request.geo` provides country, city, region (Vercel only — unavailable in local dev)
- Keep middleware fast — no DB queries, no heavy computation
- Rate limiting with in-memory store resets on cold start; use Vercel KV or Redis for production

### Auth Redirect

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { jwtVerify } from "jose";

const PUBLIC_PATHS = ["/login", "/signup", "/api/auth"];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Skip public paths
  if (PUBLIC_PATHS.some((p) => pathname.startsWith(p))) {
    return NextResponse.next();
  }

  const token = request.cookies.get("session_token")?.value;
  if (!token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  try {
    const secret = new TextEncoder().encode(process.env.JWT_SECRET!);
    await jwtVerify(token, secret);
    return NextResponse.next();
  } catch {
    return NextResponse.redirect(new URL("/login", request.url));
  }
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
```

### Geo-Routing

```typescript
// middleware.ts — serve region-specific content
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const REGION_MAP: Record<string, string> = {
  US: "/en-us",
  GB: "/en-gb",
  DE: "/de",
  JP: "/ja",
};

export function middleware(request: NextRequest) {
  const country = request.geo?.country ?? "US";
  const { pathname } = request.nextUrl;

  // Only redirect root path
  if (pathname === "/") {
    const regionPath = REGION_MAP[country] ?? "/en-us";
    return NextResponse.redirect(new URL(regionPath, request.url));
  }

  // GDPR consent gate for EU users
  if (country === "EU" && !request.cookies.get("gdpr-consent")) {
    return NextResponse.rewrite(new URL("/gdpr-banner", request.url));
  }

  // Add country header for downstream use
  const response = NextResponse.next();
  response.headers.set("x-user-country", country);
  return response;
}
```

### Rate Limiting (Edge-Compatible)

```typescript
// middleware.ts — simple IP-based rate limiting
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// In-memory store (resets on cold start — use KV/Redis for production)
const rateLimitMap = new Map<string, { count: number; resetTime: number }>();

const RATE_LIMIT = 100; // requests per window
const WINDOW_MS = 60_000; // 1 minute

export function middleware(request: NextRequest) {
  if (!request.nextUrl.pathname.startsWith("/api/")) {
    return NextResponse.next();
  }

  const ip = request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ?? "unknown";
  const now = Date.now();
  const entry = rateLimitMap.get(ip);

  if (!entry || now > entry.resetTime) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + WINDOW_MS });
    return NextResponse.next();
  }

  entry.count++;
  if (entry.count > RATE_LIMIT) {
    return new NextResponse("Too Many Requests", {
      status: 429,
      headers: {
        "Retry-After": String(Math.ceil((entry.resetTime - now) / 1000)),
      },
    });
  }

  return NextResponse.next();
}
```

**Note:** In-memory rate limiting resets when the deployment restarts or scales to a new instance. For persistent, cross-instance rate limiting, use Vercel KV or Redis.

### i18n Detection + Auth (Combined)

```typescript
// middleware.ts — combined i18n + auth middleware
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { match } from "@formatjs/intl-localematcher";
import Negotiator from "negotiator";

const SUPPORTED_LOCALES = ["en", "de", "ja", "fr"];
const DEFAULT_LOCALE = "en";

function getLocale(request: NextRequest): string {
  const headers: Record<string, string> = {};
  request.headers.forEach((value, key) => {
    headers[key] = value;
  });
  const languages = new Negotiator({ headers }).languages();
  return match(languages, SUPPORTED_LOCALES, DEFAULT_LOCALE);
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check if locale is in the pathname
  const hasLocale = SUPPORTED_LOCALES.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  );

  if (!hasLocale) {
    const locale = getLocale(request);
    return NextResponse.redirect(new URL(`/${locale}${pathname}`, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api/).*)"],
};
```

## Pitfalls

- Overlapping rewrites/redirects → first match wins, order matters
- `maxDuration` on Hobby plan is 60s — large uploads need client-side direct-to-R2
- Edge runtime cannot use Node.js `fs`, `crypto` (node:), or `Buffer` — use Web APIs
- Committing `.env.local` exposes secrets — always gitignore
- `s-maxage` without `stale-while-revalidate` → cold cache hits are slow
- Middleware runs on **every matched request** — keep it fast (no DB queries)
- `matcher` config is required to avoid running middleware on static assets
- `request.geo` is only available on Vercel (not in local dev)

## Edge vs Serverless Comparison

| Aspect | Edge Runtime | Serverless (Node.js) |
|--------|-------------|---------------------|
| Cold start | ~0ms (instant) | 250ms–1s+ |
| Max duration | 30s (Hobby), 30s (Pro) | 60s (Hobby), 300s (Pro) |
| Memory | 128MB | 128–3008MB |
| APIs | Web APIs only | Full Node.js |
| `fs`, `crypto` (node:) | Not available | Available |
| `@aws-sdk/*` | Not available | Available |
| Best for | Auth checks, redirects, geolocation, simple transforms | R2 uploads, DB queries, heavy computation |

Use `export const runtime = "edge"` only for lightweight, latency-sensitive routes. R2/S3 SDK operations require Node.js runtime.

## System Environment Variables

```typescript
// Available automatically on Vercel — do NOT set manually
const deployUrl = process.env.VERCEL_URL; // e.g. "my-app-abc123.vercel.app" (no protocol)
const fullUrl = `https://${process.env.VERCEL_URL}`;
const env = process.env.VERCEL_ENV; // "production" | "preview" | "development"
const region = process.env.VERCEL_REGION; // e.g. "iad1"
```

Use `VERCEL_URL` for constructing absolute URLs in webhooks and callbacks. Note: it does NOT include the protocol prefix.
