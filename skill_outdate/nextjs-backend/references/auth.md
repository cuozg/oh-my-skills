# Auth — JWT Authentication & Authorization

Production auth patterns for Next.js using Auth.js v5 or custom JWT with jose.

## Auth.js v5 Setup (Recommended Default)

```typescript
// auth.ts
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';
import Credentials from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { db } from '@/lib/db';
import { verify } from '@node-rs/argon2';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(db),
  session: { strategy: 'jwt' },
  providers: [
    GitHub,
    Credentials({
      credentials: { email: {}, password: {} },
      authorize: async (credentials) => {
        const user = await db.user.findUnique({
          where: { email: credentials.email as string },
        });
        if (!user?.passwordHash) return null;
        const valid = await verify(user.passwordHash, credentials.password as string);
        return valid ? user : null;
      },
    }),
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }
      return token;
    },
    session({ session, token }) {
      session.user.id = token.id as string;
      session.user.role = token.role as string;
      return session;
    },
  },
});
```

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth';
export const { GET, POST } = handlers;
```

## Custom JWT with jose (Edge-Compatible)

When you need full control or can't use Auth.js (custom token claims, non-standard flows):

```typescript
// lib/jwt.ts
import { SignJWT, jwtVerify, type JWTPayload } from 'jose';

const secret = new TextEncoder().encode(process.env.JWT_SECRET!);

export interface TokenPayload extends JWTPayload {
  userId: string;
  role: string;
}

export async function createToken(payload: Omit<TokenPayload, keyof JWTPayload>) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('2h')
    .sign(secret);
}

export async function verifyToken(token: string): Promise<TokenPayload | null> {
  try {
    const { payload } = await jwtVerify(token, secret);
    return payload as TokenPayload;
  } catch {
    return null;
  }
}
```

## Middleware Auth Protection

```typescript
// middleware.ts
import { auth } from '@/auth'; // Auth.js
// OR: import { verifyToken } from '@/lib/jwt'; // Custom

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isAuthRoute = req.nextUrl.pathname.startsWith('/login');
  const isProtected = req.nextUrl.pathname.startsWith('/dashboard');

  if (isAuthRoute && isLoggedIn) {
    return Response.redirect(new URL('/dashboard', req.nextUrl));
  }

  if (isProtected && !isLoggedIn) {
    return Response.redirect(new URL('/login', req.nextUrl));
  }
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

## RBAC in Server Components & Actions

```typescript
// Fine-grained check in server component
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export default async function AdminPage() {
  const session = await auth();
  if (!session?.user) redirect('/login');
  if (session.user.role !== 'admin') redirect('/unauthorized');

  return <AdminDashboard />;
}
```

```typescript
// Protected server action
'use server';
import { auth } from '@/auth';

export async function deleteUser(userId: string) {
  const session = await auth();
  if (!session?.user) throw new Error('Unauthorized');
  if (session.user.role !== 'admin') throw new Error('Forbidden');

  await db.user.delete({ where: { id: userId } });
  revalidatePath('/admin/users');
}
```

## Protected API Route Helper

```typescript
// lib/auth-helpers.ts
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

export async function withAuth(
  handler: (req: Request, session: Session) => Promise<Response>,
  requiredRole?: string,
) {
  return async (req: Request) => {
    const session = await auth();
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    if (requiredRole && session.user.role !== requiredRole) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }
    return handler(req, session);
  };
}
```

## Password Hashing

Use Argon2id (OWASP recommended) via `@node-rs/argon2` (native Node binding):

```typescript
import { hash, verify } from '@node-rs/argon2';

const passwordHash = await hash(plainPassword);
const isValid = await verify(passwordHash, plainPassword);
```

## Architecture Summary

| Layer | Responsibility | Where |
|-------|---------------|-------|
| Middleware | Coarse redirects (logged in/out) | `middleware.ts` |
| Server Components | RBAC before rendering | `auth()` in page.tsx |
| Server Actions | Auth + validation before mutation | `auth()` in actions.ts |
| API Routes | Auth for external consumers | `auth()` or `verifyToken()` |
| Client | Conditional UI (non-security) | `useSession()` |
