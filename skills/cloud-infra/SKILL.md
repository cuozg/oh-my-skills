---
name: cloud-infra
description: >
  Unified cloud infrastructure skill — Cloudflare R2 storage, Vercel deployment,
  signed URLs, CDN caching, and file upload patterns for Next.js applications.
  Auto-triages: Quick (single config, one upload endpoint, cache header fix) or
  Deep (full upload pipeline, multi-zone CDN strategy, R2+Workers integration).
  MUST use for ANY cloud infrastructure request — R2 bucket setup, presigned URLs,
  Vercel configuration, CDN caching strategy, file uploads, image optimization,
  edge caching, cache invalidation, or storage integration.
  Triggers: "R2 bucket," "presigned URL," "signed URL," "Vercel config," "vercel.json,"
  "CDN caching," "cache headers," "file upload," "multipart upload," "image CDN,"
  "edge caching," "cache invalidation," "Cloudflare Workers," "S3 compatible,"
  "upload to R2," "serve files from CDN," "Cache-Control," "ISR revalidation,"
  "stale-while-revalidate," "wrangler," "R2 binding."
  Do not use for database design (database-design), API routes (nextjs-backend),
  or frontend components (visual-engineering).
metadata:
  author: cuongnp
  version: "1.1"
---

# cloud-infra

Cloud infrastructure patterns for Next.js apps — R2 storage, Vercel config, signed URLs, CDN caching, and upload pipelines.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| Single R2 bucket setup, one presigned URL endpoint, cache header fix, env var config | **Quick** |
| Full upload pipeline with validation, R2 + Workers + CDN integration, multi-zone caching strategy, complete Vercel deployment setup | **Deep** |

## Step 2 — Execute

### Quick Mode

1. **Load reference** — Read the single most relevant reference file for the task
2. **Discover** — Check existing project config (`vercel.json`, `wrangler.toml`, `.env*`, route handlers)
3. **Implement** — Write the minimal code/config following reference patterns exactly
4. **Verify** — Confirm env vars referenced exist, imports resolve, types are correct
5. **Handoff** — State what was created and what the user must configure (API keys, bucket names)

### Deep Mode

1. **Load references** — Read ALL relevant reference files for the task scope
2. **Discover** — Scan project structure: existing routes, middleware, storage config, caching headers
3. **Plan** — List files to create/modify with brief rationale for each
4. **Implement** — Write all code following reference patterns; use TypeScript throughout
5. **Verify** — Run `lsp_diagnostics` on all changed files; confirm no missing env vars
6. **Handoff** — Provide setup checklist: env vars to set, Cloudflare dashboard steps, deployment notes

## Rules

- ALWAYS use `@aws-sdk/client-s3` + `@aws-sdk/s3-request-presigner` for R2 (NOT full AWS SDK)
- ALWAYS set `region: "auto"` for R2 S3 client — R2 does not use AWS regions
- ALWAYS use `forcePathStyle: true` in S3 client config for R2
- NEVER hardcode R2 account IDs, API tokens, or bucket names — use env vars
- NEVER use `as any` or `@ts-ignore` — type everything properly
- ALWAYS set `Content-Type` constraints on presigned upload URLs to prevent type spoofing
- ALWAYS use short expiry for upload URLs (300s default) and longer for download URLs (3600s default)
- ALWAYS include `Cache-Control` headers on responses — never rely on CDN defaults
- PREFER `s-maxage` + `stale-while-revalidate` for CDN-cached API responses
- PREFER `public, max-age=31536000, immutable` for content-hashed static assets
- NEVER cache responses containing `Set-Cookie` headers
- ALWAYS validate file size and MIME type server-side before generating upload URLs
- Use Zod for request validation in upload endpoints
- For Workers-based R2 access, use native `env.BUCKET` API — not S3 SDK
- R2 does NOT support S3 ACLs — never include `ACL` parameters in PutObject or CreateBucket commands
- ALWAYS use `export const dynamic = "force-dynamic"` for API routes that must never be cached (webhooks, auth callbacks, mutations)
- NEVER use Edge Runtime for routes requiring `@aws-sdk/*` — R2 SDK needs Node.js runtime
- ALWAYS use minimum 5MB per part for R2 multipart uploads except the last part
- ALWAYS implement retry logic with exponential backoff for transient failures (503, 429, socket timeout)
- NEVER retry after `AbortController.abort()` — let the abort propagate and clean up server-side

## Escalation

- Complex Workers + R2 streaming with range requests → Consult oracle
- Multi-region replication or failover strategies → Consult oracle
- Custom CDN cache key logic with Cloudflare Transform Rules → Consult oracle

## Reference Catalog

| File | Covers |
|------|--------|
| `cloudflare-r2.md` | R2 bucket setup, S3 SDK config, Workers binding, native API, cost patterns |
| `vercel-config.md` | vercel.json, env vars, functions config, monorepo, storage, domains, crons |
| `signed-urls.md` | Presigned upload/download URLs, HMAC signing, security constraints, multipart |
| `cdn-caching.md` | Cache-Control recipes, Cloudflare Cache Rules, Vercel ISR, on-demand revalidation |
| `upload-patterns.md` | Direct upload flow, multipart uploads, progress tracking, validation, Next.js integration |
