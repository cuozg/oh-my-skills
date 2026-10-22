# Server Actions — `'use server'` Patterns

Server actions handle mutations (create, update, delete) with built-in CSRF protection, progressive enhancement, and type safety.

## When to Use

- **Server Actions**: For mutations triggered by forms or client components within YOUR app
- **API Routes**: For external consumers, webhooks, or when you need custom HTTP semantics

## Form Action Pattern (React 19+ / Next.js 15+)

```typescript
// app/posts/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';
import { auth } from '@/auth';
import { db } from '@/lib/db';

const createPostSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200),
  content: z.string().min(10, 'Content must be at least 10 characters'),
});

export type ActionState = {
  success: boolean;
  message: string;
  errors?: Record<string, string[]>;
};

export async function createPost(
  prevState: ActionState,
  formData: FormData,
): Promise<ActionState> {
  // 1. Auth check — always first
  const session = await auth();
  if (!session?.user) {
    return { success: false, message: 'You must be signed in' };
  }

  // 2. Validate input
  const parsed = createPostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!parsed.success) {
    return {
      success: false,
      message: 'Validation failed',
      errors: parsed.error.flatten().fieldErrors,
    };
  }

  // 3. Execute mutation
  try {
    await db.post.create({
      data: { ...parsed.data, authorId: session.user.id },
    });
  } catch (error) {
    console.error('createPost failed:', error);
    return { success: false, message: 'Failed to create post. Please try again.' };
  }

  // 4. Revalidate cache
  revalidatePath('/posts');
  return { success: true, message: 'Post created!' };
}
```

## Client Component Consumption

```tsx
'use client';

import { useActionState } from 'react';
import { createPost, type ActionState } from './actions';

const initialState: ActionState = { success: false, message: '' };

export function CreatePostForm() {
  const [state, action, isPending] = useActionState(createPost, initialState);

  return (
    <form action={action}>
      <input name="title" required />
      {state.errors?.title && <p className="text-red-500">{state.errors.title[0]}</p>}

      <textarea name="content" required />
      {state.errors?.content && <p className="text-red-500">{state.errors.content[0]}</p>}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Post'}
      </button>

      {state.message && (
        <p className={state.success ? 'text-green-600' : 'text-red-600'}>
          {state.message}
        </p>
      )}
    </form>
  );
}
```

## Optimistic Updates

```tsx
'use client';

import { useOptimistic } from 'react';
import { toggleLike } from './actions';

export function LikeButton({ isLiked, count }: { isLiked: boolean; count: number }) {
  const [optimistic, setOptimistic] = useOptimistic(
    { isLiked, count },
    (current, _action: void) => ({
      isLiked: !current.isLiked,
      count: current.isLiked ? current.count - 1 : current.count + 1,
    }),
  );

  return (
    <form action={async () => {
      setOptimistic(undefined);
      await toggleLike();
    }}>
      <button type="submit">
        {optimistic.isLiked ? 'Unlike' : 'Like'} ({optimistic.count})
      </button>
    </form>
  );
}
```

## Revalidation Strategies

```typescript
// After creating/updating a resource on a specific path
revalidatePath('/posts');

// After updating cached fetch calls tagged with a label
revalidateTag('posts');

// Redirect after mutation (import from 'next/navigation')
import { redirect } from 'next/navigation';
redirect('/posts');
```

## Security Rules

- Always call `auth()` at the top of every server action — before validation
- Always validate with Zod — never trust formData directly
- Never return raw database errors — log server-side, return generic message
- Server actions get automatic CSRF protection — no extra tokens needed
- Return `ActionState` shape consistently so forms can display field-level errors
