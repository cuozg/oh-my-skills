# Cloudflare R2 Storage

## S3 Client Configuration

```typescript
// lib/r2.ts
import { S3Client } from "@aws-sdk/client-s3";

export const r2Client = new S3Client({
  region: "auto", // R2 does not use AWS regions
  endpoint: `https://${process.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: process.env.R2_ACCESS_KEY_ID!,
    secretAccessKey: process.env.R2_SECRET_ACCESS_KEY!,
  },
  forcePathStyle: true, // Required for R2
});

export const R2_BUCKET = process.env.R2_BUCKET_NAME!;
```

**Required env vars:**
- `R2_ACCOUNT_ID` — Cloudflare account ID (Dashboard → Overview → right sidebar)
- `R2_ACCESS_KEY_ID` — R2 API token access key (R2 → Manage R2 API Tokens)
- `R2_SECRET_ACCESS_KEY` — R2 API token secret key
- `R2_BUCKET_NAME` — Bucket name

## Wrangler Configuration (Workers)

```toml
# wrangler.toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket-name"
preview_bucket_name = "my-bucket-dev"
```

## Workers Native R2 API

Faster than S3 SDK inside Workers. Use this when your code runs on Cloudflare Workers.

```typescript
// Workers: env.BUCKET is the R2 binding
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    switch (request.method) {
      case "PUT": {
        await env.MY_BUCKET.put(key, request.body, {
          httpMetadata: {
            contentType: request.headers.get("content-type") ?? "application/octet-stream",
          },
        });
        return new Response(`Put ${key} successfully`);
      }

      case "GET": {
        const object = await env.MY_BUCKET.get(key);
        if (!object) return new Response("Not Found", { status: 404 });

        const headers = new Headers();
        object.writeHttpMetadata(headers);
        headers.set("etag", object.httpEtag);
        headers.set("cache-control", "public, max-age=86400");

        return new Response(object.body, { headers });
      }

      case "DELETE": {
        await env.MY_BUCKET.delete(key);
        return new Response("Deleted");
      }

      default:
        return new Response("Method Not Allowed", { status: 405 });
    }
  },
};
```

## CORS Configuration

Apply via Cloudflare Dashboard → R2 → Bucket → Settings → CORS Policy:

```json
[
  {
    "AllowedOrigins": ["https://yourdomain.com"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedHeaders": ["Content-Type", "Authorization"],
    "ExposeHeaders": ["ETag", "Content-Length"],
    "MaxAgeSeconds": 3600
  }
]
```

## Common Operations (S3 SDK)

```typescript
import { PutObjectCommand, GetObjectCommand, DeleteObjectCommand, ListObjectsV2Command } from "@aws-sdk/client-s3";
import { r2Client, R2_BUCKET } from "@/lib/r2";

// Upload
await r2Client.send(new PutObjectCommand({
  Bucket: R2_BUCKET,
  Key: `uploads/${userId}/${filename}`,
  Body: buffer,
  ContentType: mimeType,
}));

// Download
const response = await r2Client.send(new GetObjectCommand({
  Bucket: R2_BUCKET,
  Key: "uploads/file.pdf",
}));
const body = await response.Body?.transformToByteArray();

// Delete
await r2Client.send(new DeleteObjectCommand({
  Bucket: R2_BUCKET,
  Key: "uploads/file.pdf",
}));

// List with prefix
const listed = await r2Client.send(new ListObjectsV2Command({
  Bucket: R2_BUCKET,
  Prefix: `uploads/${userId}/`,
  MaxKeys: 100,
}));
```

## Cost Optimization

- **$0 egress** — R2 has zero egress fees (vs S3 $0.09/GB)
- **Lifecycle rules** — Auto-delete temp uploads after 24h (Dashboard → Bucket → Settings → Object lifecycle)
- **Infrequent Access** — Use `storageClass: "INFREQUENT_ACCESS"` for rarely-read files (lower storage cost)
- **Custom domain** — Attach custom domain for edge caching without Workers (Dashboard → R2 → Bucket → Public access)

## S3 Compatibility Notes

- R2 does **NOT** support S3 ACLs (e.g. `ACL: "public-read"`) — access is managed via API tokens or public bucket settings
- `region` must always be `"auto"` — R2 does not use AWS regions
- Storage classes: `Standard` (default, zero retrieval fees) and `InfrequentAccess` (lower storage cost, retrieval fees apply, 30-day minimum retention)
- Lifecycle rules: Configure via Dashboard (Bucket → Settings → Object lifecycle) or wrangler CLI for auto-expiration/transitions
- Custom domains: Attach via Dashboard (R2 → Bucket → Settings → Public access → Custom domain) for edge-cached public access without Workers

## aws4fetch — Lightweight S3 Signing for Workers

When running inside Cloudflare Workers and you need S3-compatible access (e.g., for multipart uploads, streaming, or cross-account access), use `aws4fetch` instead of the full `@aws-sdk/client-s3` which is not compatible with the Workers runtime.

```typescript
// workers/r2-s3-compat.ts
import { AwsClient } from "aws4fetch";

const r2 = new AwsClient({
  accessKeyId: R2_ACCESS_KEY_ID,     // from env or secrets
  secretAccessKey: R2_SECRET_ACCESS_KEY,
  region: "auto",
  service: "s3",
});

const R2_ENDPOINT = `https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com`;

/** Upload a file via S3-compatible PUT */
export async function putObject(
  bucket: string,
  key: string,
  body: ReadableStream | ArrayBuffer | string,
  contentType: string
): Promise<Response> {
  const url = `${R2_ENDPOINT}/${bucket}/${key}`;
  return r2.fetch(url, {
    method: "PUT",
    headers: { "Content-Type": contentType },
    body,
  });
}

/** Download a file via S3-compatible GET */
export async function getObject(bucket: string, key: string): Promise<Response> {
  const url = `${R2_ENDPOINT}/${bucket}/${key}`;
  return r2.fetch(url, { method: "GET" });
}

/** Delete a file via S3-compatible DELETE */
export async function deleteObject(bucket: string, key: string): Promise<Response> {
  const url = `${R2_ENDPOINT}/${bucket}/${key}`;
  return r2.fetch(url, { method: "DELETE" });
}

/** List objects with prefix via S3-compatible GET */
export async function listObjects(bucket: string, prefix: string): Promise<Response> {
  const url = `${R2_ENDPOINT}/${bucket}?list-type=2&prefix=${encodeURIComponent(prefix)}`;
  return r2.fetch(url, { method: "GET" });
}
```

**When to use aws4fetch vs native R2 binding:**
- **Native `env.BUCKET`** — When Worker has direct R2 binding (same account, fastest)
- **aws4fetch** — When Worker needs S3-compatible API (cross-account, custom multipart, streaming uploads, or generating presigned URLs from Workers)

Install: `npm install aws4fetch` (zero dependencies, ~4KB)

## Pitfalls

- `aws4fetch` is lighter than `@aws-sdk/client-s3` inside Workers — prefer it for Workers context
- `wrangler dev` does NOT support S3 API locally — use `--remote` flag or test against real bucket
- Missing `Content-Type` on upload → defaults to `application/octet-stream` → download issues
- R2 max single PUT: 5GB — use multipart for larger files
- Do NOT pass `ACL` params to R2 — they are silently ignored and suggest a misunderstanding of the access model

## aws4fetch Limitations

When using `aws4fetch` in Workers, be aware of these constraints:

- **No streaming** — must load full response body into memory before processing
- **No multipart upload coordination** — no built-in helper for multipart; implement manually via S3 API calls
- **No retry logic** — simpler than the full SDK; implement retries yourself if needed
- **Simpler than AWS SDK** — fewer convenience methods but sufficient for most Workers use cases
