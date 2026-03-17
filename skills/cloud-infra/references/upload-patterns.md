# Upload Patterns

## Direct Upload Flow (Browser → R2 via Presigned URL)

```
┌──────────┐    1. Request presign    ┌──────────────┐
│  Browser  │ ──────────────────────→ │  Next.js API  │
│           │ ←────────────────────── │  (validates)   │
│           │    2. { url, key }      └──────────────┘
│           │
│           │    3. PUT file directly
│           │ ──────────────────────→ ┌──────────────┐
│           │ ←────────────────────── │  Cloudflare   │
│           │    4. 200 OK            │  R2 Bucket    │
│           │                         └──────────────┘
│           │    5. Confirm upload
│           │ ──────────────────────→ ┌──────────────┐
│           │ ←────────────────────── │  Next.js API  │
│           │    6. { file record }   │  (saves meta) │
└──────────┘                         └──────────────┘
```

## Client-Side Upload with Progress

```typescript
// hooks/useUpload.ts
"use client";

import { useState, useCallback } from "react";

interface UploadProgress {
  loaded: number;
  total: number;
  percent: number;
}

interface UseUploadReturn {
  upload: (file: File) => Promise<string>;
  progress: UploadProgress | null;
  uploading: boolean;
  error: string | null;
}

export function useUpload(): UseUploadReturn {
  const [progress, setProgress] = useState<UploadProgress | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const upload = useCallback(async (file: File): Promise<string> => {
    setUploading(true);
    setError(null);
    setProgress(null);

    try {
      // 1. Get presigned URL from server
      const presignRes = await fetch("/api/upload/presign", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          filename: file.name,
          contentType: file.type,
          size: file.size,
        }),
      });

      if (!presignRes.ok) {
        const err = await presignRes.json();
        throw new Error(err.error ?? "Failed to get upload URL");
      }

      const { url, key } = await presignRes.json();

      // 2. Upload directly to R2 with progress tracking
      await new Promise<void>((resolve, reject) => {
        const xhr = new XMLHttpRequest();

        xhr.upload.addEventListener("progress", (e) => {
          if (e.lengthComputable) {
            setProgress({
              loaded: e.loaded,
              total: e.total,
              percent: Math.round((e.loaded / e.total) * 100),
            });
          }
        });

        xhr.addEventListener("load", () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve();
          } else {
            reject(new Error(`Upload failed: ${xhr.status}`));
          }
        });

        xhr.addEventListener("error", () => reject(new Error("Network error")));
        xhr.addEventListener("abort", () => reject(new Error("Upload aborted")));

        xhr.open("PUT", url);
        xhr.setRequestHeader("Content-Type", file.type);
        xhr.send(file);
      });

      // 3. Confirm upload on server
      const confirmRes = await fetch("/api/upload/confirm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key, filename: file.name, size: file.size }),
      });

      if (!confirmRes.ok) throw new Error("Failed to confirm upload");

      const { fileId } = await confirmRes.json();
      return fileId;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Upload failed";
      setError(message);
      throw err;
    } finally {
      setUploading(false);
    }
  }, []);

  return { upload, progress, uploading, error };
}
```

## Server-Side Upload Confirmation

```typescript
// app/api/upload/confirm/route.ts
import { HeadObjectCommand } from "@aws-sdk/client-s3";
import { r2Client, R2_BUCKET } from "@/lib/r2";
import { z } from "zod";

const confirmSchema = z.object({
  key: z.string().min(1),
  filename: z.string().min(1),
  size: z.number().int().positive(),
});

export async function POST(request: Request) {
  const session = await getSession();
  if (!session) return Response.json({ error: "Unauthorized" }, { status: 401 });

  const body = await request.json();
  const parsed = confirmSchema.safeParse(body);
  if (!parsed.success) {
    return Response.json({ error: parsed.error.flatten() }, { status: 400 });
  }

  const { key, filename, size } = parsed.data;

  // Verify the file actually exists in R2
  try {
    const head = await r2Client.send(
      new HeadObjectCommand({ Bucket: R2_BUCKET, Key: key })
    );

    // Verify size matches what was declared
    if (head.ContentLength !== size) {
      return Response.json({ error: "Size mismatch" }, { status: 400 });
    }
  } catch {
    return Response.json({ error: "File not found in storage" }, { status: 404 });
  }

  // Save file record to database
  const file = await db.file.create({
    data: {
      key,
      filename,
      size,
      contentType: head.ContentType ?? "application/octet-stream",
      userId: session.userId,
    },
  });

  return Response.json({ fileId: file.id });
}
```

## File Validation (Server-Side)

```typescript
// lib/upload-validation.ts

const ALLOWED_TYPES: Record<string, { maxSize: number; extensions: string[] }> = {
  "image/jpeg": { maxSize: 10 * 1024 * 1024, extensions: [".jpg", ".jpeg"] },
  "image/png": { maxSize: 10 * 1024 * 1024, extensions: [".png"] },
  "image/webp": { maxSize: 10 * 1024 * 1024, extensions: [".webp"] },
  "application/pdf": { maxSize: 50 * 1024 * 1024, extensions: [".pdf"] },
  "video/mp4": { maxSize: 500 * 1024 * 1024, extensions: [".mp4"] },
};

export function validateUpload(
  filename: string,
  contentType: string,
  size: number
): { valid: true } | { valid: false; error: string } {
  const config = ALLOWED_TYPES[contentType];

  if (!config) {
    return { valid: false, error: `File type "${contentType}" is not allowed` };
  }

  const ext = filename.slice(filename.lastIndexOf(".")).toLowerCase();
  if (!config.extensions.includes(ext)) {
    return { valid: false, error: `Extension "${ext}" does not match content type "${contentType}"` };
  }

  if (size > config.maxSize) {
    return {
      valid: false,
      error: `File size ${(size / 1024 / 1024).toFixed(1)}MB exceeds max ${(config.maxSize / 1024 / 1024).toFixed(0)}MB`,
    };
  }

  return { valid: true };
}
```

## Multipart Upload (Large Files — Client)

```typescript
// lib/multipart-upload.ts
const PART_SIZE = 10 * 1024 * 1024; // 10MB per part

export async function multipartUpload(
  file: File,
  onProgress?: (percent: number) => void
): Promise<string> {
  // 1. Initialize
  const initRes = await fetch("/api/upload/multipart/init", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      filename: file.name,
      contentType: file.type,
      size: file.size,
    }),
  });
  const { key, uploadId } = await initRes.json();

  const totalParts = Math.ceil(file.size / PART_SIZE);
  const parts: { ETag: string; PartNumber: number }[] = [];

  try {
    // 2. Upload parts in parallel (max 3 concurrent)
    const concurrency = 3;
    for (let i = 0; i < totalParts; i += concurrency) {
      const batch = Array.from(
        { length: Math.min(concurrency, totalParts - i) },
        (_, j) => i + j + 1
      );

      const batchResults = await Promise.all(
        batch.map(async (partNumber) => {
          const start = (partNumber - 1) * PART_SIZE;
          const end = Math.min(start + PART_SIZE, file.size);
          const chunk = file.slice(start, end);

          // Get presigned URL for this part
          const urlRes = await fetch("/api/upload/multipart/part-url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key, uploadId, partNumber }),
          });
          const { url } = await urlRes.json();

          // Upload part
          const putRes = await fetch(url, { method: "PUT", body: chunk });
          const etag = putRes.headers.get("etag")!;

          onProgress?.(Math.round((partNumber / totalParts) * 100));

          return { ETag: etag, PartNumber: partNumber };
        })
      );

      parts.push(...batchResults);
    }

    // 3. Complete
    const completeRes = await fetch("/api/upload/multipart/complete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, uploadId, parts }),
    });

    const { fileId } = await completeRes.json();
    return fileId;
  } catch (error) {
    // Abort on failure
    await fetch("/api/upload/multipart/abort", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, uploadId }),
    });
    throw error;
  }
}
```

## Key Decisions

| File Size | Strategy | Why |
|-----------|----------|-----|
| < 5MB | Single presigned PUT | Simple, fast, one request |
| 5MB–100MB | Single presigned PUT + progress | Still one part, but show progress via XHR |
| > 100MB | Multipart upload | Required for reliability; parallel parts = faster |
| > 5GB | Multipart upload (mandatory) | R2 single PUT limit is 5GB |

## Abort Upload (Cancel In-Progress Uploads)

Use `AbortController` to let users cancel uploads mid-flight. Always clean up server-side multipart state on abort.

```typescript
// lib/cancellable-upload.ts
export function createCancellableUpload(file: File, onProgress?: (percent: number) => void) {
  const controller = new AbortController();

  const promise = (async () => {
    // 1. Get presigned URL
    const presignRes = await fetch("/api/upload/presign", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename: file.name,
        contentType: file.type,
        size: file.size,
      }),
      signal: controller.signal,
    });

    if (!presignRes.ok) throw new Error("Failed to get upload URL");
    const { url, key } = await presignRes.json();

    // 2. Upload with abort support
    const uploadRes = await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": file.type },
      body: file,
      signal: controller.signal,
    });

    if (!uploadRes.ok) throw new Error(`Upload failed: ${uploadRes.status}`);

    // 3. Confirm
    const confirmRes = await fetch("/api/upload/confirm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, filename: file.name, size: file.size }),
      signal: controller.signal,
    });

    if (!confirmRes.ok) throw new Error("Failed to confirm upload");
    const { fileId } = await confirmRes.json();
    return fileId;
  })();

  return {
    promise,
    cancel: () => controller.abort(),
  };
}

// Usage in React component:
// const upload = createCancellableUpload(file, setProgress);
// cancelButton.onclick = () => upload.cancel();
// const fileId = await upload.promise;
```

### Abort Multipart Uploads on Cancel

```typescript
// lib/multipart-cancel.ts
export async function abortMultipartUpload(key: string, uploadId: string): Promise<void> {
  await fetch("/api/upload/multipart/abort", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ key, uploadId }),
  });
}
```

**Important:** Always call the abort endpoint when cancelling a multipart upload. Orphaned multipart uploads still consume storage and incur costs until cleaned up via lifecycle rules.

## Retry Failed Parts (Exponential Backoff)

For multipart uploads, individual parts may fail due to network issues. Retry failed parts with exponential backoff instead of failing the entire upload.

```typescript
// lib/retry-upload.ts

interface RetryOptions {
  maxRetries: number;
  baseDelayMs: number;
  signal?: AbortSignal;
}

/**
 * Upload a single part with exponential backoff retry.
 * Delays: 1s, 2s, 4s, 8s... (baseDelayMs * 2^attempt)
 */
export async function uploadPartWithRetry(
  url: string,
  chunk: Blob,
  options: RetryOptions = { maxRetries: 3, baseDelayMs: 1000 }
): Promise<string> {
  const { maxRetries, baseDelayMs, signal } = options;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(url, {
        method: "PUT",
        body: chunk,
        signal,
      });

      if (!response.ok) {
        throw new Error(`Part upload failed: ${response.status}`);
      }

      const etag = response.headers.get("etag");
      if (!etag) throw new Error("Missing ETag in response");
      return etag;
    } catch (error) {
      // Don't retry if aborted by user
      if (signal?.aborted) throw error;

      if (attempt === maxRetries) {
        throw new Error(
          `Part upload failed after ${maxRetries + 1} attempts: ${
            error instanceof Error ? error.message : "Unknown error"
          }`
        );
      }

      // Exponential backoff: 1s, 2s, 4s, 8s...
      const delay = baseDelayMs * Math.pow(2, attempt);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw new Error("Unreachable");
}
```

### Integrating Retry into Multipart Upload

```typescript
// Updated multipart upload loop with retry
const PART_SIZE = 10 * 1024 * 1024; // 10MB (must be >= 5MB for R2 except last part)

for (let partNumber = 1; partNumber <= totalParts; partNumber++) {
  const start = (partNumber - 1) * PART_SIZE;
  const end = Math.min(start + PART_SIZE, file.size);
  const chunk = file.slice(start, end);

  // Get presigned URL for this part
  const urlRes = await fetch("/api/upload/multipart/part-url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ key, uploadId, partNumber }),
    signal: controller.signal,
  });
  const { url } = await urlRes.json();

  // Upload with retry
  const etag = await uploadPartWithRetry(url, chunk, {
    maxRetries: 3,
    baseDelayMs: 1000,
    signal: controller.signal,
  });

  parts.push({ ETag: etag, PartNumber: partNumber });
  onProgress?.(Math.round((partNumber / totalParts) * 100));
}
```

**Key rules:**
- Minimum part size for R2 multipart: **5MB** (except the last part)
- Default part size of 10MB provides a good balance of parallelism and reliability
- Always pass `AbortController.signal` to retry logic so user cancellation stops retries
- Exponential backoff prevents overwhelming the server during transient failures
- Log retry attempts for debugging: `console.warn(\`Retrying part ${partNumber}, attempt ${attempt + 1}\`)`

## Advanced Patterns

### Abort Upload

Allow user to cancel upload mid-flight and clean up incomplete multipart uploads.

```typescript
// lib/useUploadWithCancel.ts
import { useState, useRef } from "react"

export function useUploadWithCancel() {
  const [progress, setProgress] = useState(0)
  const abortControllerRef = useRef<AbortController | null>(null)
  
  const upload = async (file: File, onProgress?: (p: number) => void) => {
    const formData = new FormData()
    formData.append("file", file)
    
    abortControllerRef.current = new AbortController()
    
    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
        signal: abortControllerRef.current.signal
      })
      
      if (!response.ok) throw new Error("Upload failed")
      return await response.json()
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        console.log("Upload cancelled by user")
      }
      throw error
    }
  }
  
  const cancel = async (uploadId?: string) => {
    abortControllerRef.current?.abort()
    
    // Notify backend to clean up incomplete multipart
    if (uploadId) {
      await fetch(`/api/multipart/abort`, {
        method: "POST",
        body: JSON.stringify({ uploadId })
      })
    }
  }
  
  return { upload, cancel }
}
```

### Retry Failed Parts (Multipart)

Retry individual failed parts with exponential backoff:

```typescript
// lib/uploadMultipartWithRetry.ts
import { AbortMultipartUploadCommand, S3Client, UploadPartCommand } from "@aws-sdk/client-s3"

async function uploadPartWithRetry(
  s3: S3Client,
  bucket: string,
  key: string,
  uploadId: string,
  partNumber: number,
  body: Buffer,
  maxRetries = 3
): Promise<string> {
  let lastError: Error | null = null
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const delay = Math.min(1000 * Math.pow(2, attempt), 10000) // cap at 10s
      if (attempt > 0) await new Promise(r => setTimeout(r, delay))
      
      const result = await s3.send(
        new UploadPartCommand({
          Bucket: bucket,
          Key: key,
          UploadId: uploadId,
          PartNumber: partNumber,
          Body: body
        })
      )
      
      return result.ETag!
    } catch (error) {
      lastError = error as Error
      console.warn(`Part ${partNumber} attempt ${attempt + 1} failed: ${lastError.message}`)
      
      if (attempt === maxRetries - 1) {
        // Last attempt failed — abort entire upload
        await s3.send(
          new AbortMultipartUploadCommand({
            Bucket: bucket,
            Key: key,
            UploadId: uploadId
          })
        )
        throw new Error(`Failed to upload part ${partNumber} after ${maxRetries} retries`)
      }
    }
  }
  
  throw lastError
}
```

**Retry Strategy:**
- Exponential backoff: 1s, 2s, 4s, (capped at 10s)
- Max 3 attempts per part
- On final failure, abort entire multipart upload to prevent orphaned parts
- Specific error handling for 503 (Service Unavailable), 429 (Rate Limit), 5xx (Server Error)
