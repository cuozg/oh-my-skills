# Signed URLs

## Presigned Upload URL (PutObject)

```typescript
// app/api/upload/presign/route.ts
import { PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { r2Client, R2_BUCKET } from "@/lib/r2";
import { z } from "zod";

const presignSchema = z.object({
  filename: z.string().min(1).max(255),
  contentType: z.string().regex(/^(image|video|application)\//),
  size: z.number().int().positive().max(50 * 1024 * 1024), // 50MB max
});

export async function POST(request: Request) {
  const session = await getSession(); // Your auth check
  if (!session) return Response.json({ error: "Unauthorized" }, { status: 401 });

  const body = await request.json();
  const parsed = presignSchema.safeParse(body);
  if (!parsed.success) {
    return Response.json({ error: parsed.error.flatten() }, { status: 400 });
  }

  const { filename, contentType, size } = parsed.data;
  const key = `uploads/${session.userId}/${Date.now()}-${filename}`;

  const command = new PutObjectCommand({
    Bucket: R2_BUCKET,
    Key: key,
    ContentType: contentType,
    ContentLength: size,
  });

  const url = await getSignedUrl(r2Client, command, {
    expiresIn: 300, // 5 minutes — short for uploads
    signableHeaders: new Set(["content-type"]), // Lock content-type
  });

  return Response.json({ url, key });
}
```

## Presigned Download URL (GetObject)

```typescript
import { GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { r2Client, R2_BUCKET } from "@/lib/r2";

export async function getDownloadUrl(key: string, filename?: string): Promise<string> {
  const command = new GetObjectCommand({
    Bucket: R2_BUCKET,
    Key: key,
    ...(filename && {
      ResponseContentDisposition: `attachment; filename="${filename}"`,
    }),
  });

  return getSignedUrl(r2Client, command, {
    expiresIn: 3600, // 1 hour — longer for downloads
  });
}
```

## HMAC Signed URLs (Workers — No SDK)

For Cloudflare Workers without S3 SDK overhead:

```typescript
// workers/sign.ts
const HMAC_SECRET = env.HMAC_SECRET; // Bound in wrangler.toml [vars] or secrets

async function generateSignedUrl(path: string, expiresIn: number): Promise<string> {
  const expiry = Math.floor(Date.now() / 1000) + expiresIn;
  const message = `${path}:${expiry}`;

  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(HMAC_SECRET),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );

  const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(message));

  const sig = btoa(String.fromCharCode(...new Uint8Array(signature)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");

  return `${path}?expires=${expiry}&sig=${sig}`;
}

async function verifySignedUrl(path: string, expires: string, sig: string): Promise<boolean> {
  if (Number(expires) < Math.floor(Date.now() / 1000)) return false;

  const message = `${path}:${expires}`;
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(HMAC_SECRET),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["verify"]
  );

  const sigBytes = Uint8Array.from(atob(sig.replace(/-/g, "+").replace(/_/g, "/")), (c) => c.charCodeAt(0));
  return crypto.subtle.verify("HMAC", key, sigBytes, new TextEncoder().encode(message));
}
```

## Multipart Upload (Presigned Per-Part)

```typescript
import {
  CreateMultipartUploadCommand,
  UploadPartCommand,
  CompleteMultipartUploadCommand,
  AbortMultipartUploadCommand,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

// 1. Initialize multipart upload (server-side)
export async function initMultipart(key: string) {
  const { UploadId } = await r2Client.send(
    new CreateMultipartUploadCommand({ Bucket: R2_BUCKET, Key: key })
  );
  return UploadId;
}

// 2. Generate presigned URL per part (server-side)
export async function getPartUrl(key: string, uploadId: string, partNumber: number) {
  const command = new UploadPartCommand({
    Bucket: R2_BUCKET,
    Key: key,
    UploadId: uploadId,
    PartNumber: partNumber,
  });
  return getSignedUrl(r2Client, command, { expiresIn: 600 });
}

// 3. Complete multipart upload (server-side)
export async function completeMultipart(
  key: string,
  uploadId: string,
  parts: { ETag: string; PartNumber: number }[]
) {
  return r2Client.send(
    new CompleteMultipartUploadCommand({
      Bucket: R2_BUCKET,
      Key: key,
      UploadId: uploadId,
      MultipartUpload: { Parts: parts },
    })
  );
}

// 4. Abort on failure (server-side)
export async function abortMultipart(key: string, uploadId: string) {
  return r2Client.send(
    new AbortMultipartUploadCommand({
      Bucket: R2_BUCKET,
      Key: key,
      UploadId: uploadId,
    })
  );
}
```

## Security Checklist

- **Short expiry** — 5 min for uploads, 1 hour for downloads
- **Content-Type lock** — Use `signableHeaders` to prevent type spoofing
- **Size validation** — Validate `Content-Length` server-side before signing
- **Auth required** — Always check session before generating URLs
- **One-time use** — For sensitive files, track used URLs and reject replays
- **CORS** — Configure R2 bucket CORS to only allow your domain
- **Post-upload validation** — After upload completes, verify file magic bytes server-side
- **`content-length-range`** — Only works with POST (PostObject) policies, NOT with presigned PUT URLs — validate size server-side instead
