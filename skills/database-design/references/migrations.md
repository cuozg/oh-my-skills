# Migrations — Safe Schema Evolution

Strategies for evolving PostgreSQL schemas safely, including zero-downtime patterns, rollback strategies, and data migrations.

## Migration Principles

1. **Forward-only in production** — rollback migrations are useful in development but unreliable in production (data loss risk). Design migrations to be reversible by deploying a new forward migration.
2. **Idempotent scripts** — use `IF NOT EXISTS`, `IF EXISTS` guards so migrations can safely re-run.
3. **Separate schema and data migrations** — DDL changes and data backfills are different concerns with different risk profiles.
4. **Small, incremental changes** — one concern per migration. Don't combine table creation with data backfill.
5. **Lock awareness** — every DDL statement acquires some lock. Know what locks your migration needs.

## Lock-Safe DDL

PostgreSQL DDL operations acquire locks. Some are fast, some block all reads/writes.

### Safe Operations (minimal/no locking)

```sql
-- Adding a nullable column (instant, no rewrite)
ALTER TABLE order ADD COLUMN notes TEXT;

-- Adding a column with DEFAULT (PG 11+, instant, no rewrite)
ALTER TABLE order ADD COLUMN priority TEXT NOT NULL DEFAULT 'normal';

-- Creating an index concurrently
CREATE INDEX CONCURRENTLY idx_order_status ON order(status);

-- Adding a CHECK constraint as NOT VALID (no scan)
ALTER TABLE order ADD CONSTRAINT chk_order_amount
  CHECK (amount > 0) NOT VALID;

-- Validating a constraint separately (ShareUpdateExclusiveLock, no block)
ALTER TABLE order VALIDATE CONSTRAINT chk_order_amount;
```

### Dangerous Operations (avoid or use caution)

| Operation | Risk | Safe Alternative |
|-----------|------|-----------------|
| `ALTER TABLE ... ADD COLUMN NOT NULL` (no default, pre-PG11) | Full table rewrite | Add nullable → backfill → set NOT NULL |
| `ALTER TYPE ... ADD VALUE` | Can't run in transaction | Plan enum changes carefully |
| `CREATE INDEX` (non-concurrent) | Locks all writes | Always use `CONCURRENTLY` |
| `ALTER TABLE ... ALTER COLUMN TYPE` | Full table rewrite | Create new column → backfill → rename |
| `DROP COLUMN` | Brief lock, but metadata only | Safe if column is unused |

### Lock Timeout Pattern

Always set a lock timeout in production migrations to prevent the "lock queue death spiral":

```sql
-- If we can't get the lock in 5 seconds, abort rather than queue
SET lock_timeout = '5s';

ALTER TABLE order ADD COLUMN tracking_url TEXT;

RESET lock_timeout;
```

## Expand-Contract Pattern

The safest approach for breaking changes (rename column, change type, split table).

### Example: Rename a Column

```sql
-- Step 1: EXPAND — add new column
ALTER TABLE user ADD COLUMN full_name TEXT;

-- Step 2: MIGRATE — backfill (in batches for large tables)
UPDATE user SET full_name = name WHERE full_name IS NULL;
-- For large tables, batch:
-- UPDATE user SET full_name = name WHERE id BETWEEN 1 AND 10000 AND full_name IS NULL;

-- Step 3: DEPLOY — update application to write to both, read from new
-- (application code change, not a migration)

-- Step 4: CONTRACT — drop old column (after all code uses new column)
ALTER TABLE user DROP COLUMN name;
```

### Example: Change Column Type (e.g., INT → BIGINT)

```sql
-- Step 1: Add new column
ALTER TABLE order ADD COLUMN amount_v2 BIGINT;

-- Step 2: Backfill + dual-write trigger
CREATE OR REPLACE FUNCTION sync_amount() RETURNS TRIGGER AS $$
BEGIN
  NEW.amount_v2 = NEW.amount;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER sync_amount_trigger
  BEFORE INSERT OR UPDATE ON order
  FOR EACH ROW EXECUTE FUNCTION sync_amount();

-- Step 3: Backfill existing rows (batched)
UPDATE order SET amount_v2 = amount WHERE amount_v2 IS NULL;

-- Step 4: After app reads from amount_v2, drop old
ALTER TABLE order DROP COLUMN amount;
ALTER TABLE order RENAME COLUMN amount_v2 TO amount;
DROP TRIGGER sync_amount_trigger ON order;
DROP FUNCTION sync_amount();
```

## Data Migrations (Backfills)

For large tables, always backfill in batches to avoid long-running transactions and lock contention.

```sql
-- Batch backfill pattern
DO $$
DECLARE
  batch_size INT := 5000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE order
    SET status_v2 = status
    WHERE id IN (
      SELECT id FROM order
      WHERE status_v2 IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    );

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;

    COMMIT;
    PERFORM pg_sleep(0.1); -- Brief pause to reduce load
  END LOOP;
END $$;
```

## Prisma Migration Workflow

```bash
# Development: generate + apply migration
npx prisma migrate dev --name add_tracking_url

# Production: apply pending migrations (no prompts, no generation)
npx prisma migrate deploy

# Reset development database
npx prisma migrate reset

# Create a migration without applying (for custom SQL edits)
npx prisma migrate dev --create-only --name add_rls_policy
# Then edit the generated SQL file before applying
```

### Custom SQL in Prisma Migrations

For operations Prisma can't express (RLS, triggers, functions), use `--create-only`:

```bash
npx prisma migrate dev --create-only --name add_audit_trigger
# Edit the migration file to add your custom SQL
npx prisma migrate dev  # Apply it
```

## Drizzle Migration Workflow

```bash
# Generate migration SQL from schema diff
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Push schema directly (development only, no migration files)
npx drizzle-kit push

# Introspect existing database into Drizzle schema
npx drizzle-kit introspect
```

### Custom SQL in Drizzle Migrations

Drizzle generates SQL files directly — edit them before applying with `drizzle-kit migrate`.

## Rollback Strategy

| Environment | Strategy |
|-------------|----------|
| Development | `prisma migrate reset` / `drizzle-kit push` — rebuild from scratch |
| Staging | Deploy a new forward migration that reverses the change |
| Production | **Never** use down migrations. Deploy a new forward migration that undoes the change safely. |

### Why Not Down Migrations in Production

- Data loss: dropping a column loses data that can't be recovered
- State inconsistency: partial rollbacks leave the database in an unknown state
- Ordering: down migrations assume linear history which breaks with parallel development

Instead, apply the expand-contract pattern: if the new column is wrong, add another migration that drops it.

## Migration Checklist

Before applying a migration to production:

- [ ] Does the migration acquire `AccessExclusiveLock`? If so, use the safe alternative.
- [ ] For `CREATE INDEX`, is `CONCURRENTLY` used?
- [ ] For new `NOT NULL` columns, is a `DEFAULT` provided?
- [ ] For data backfills, is it batched with `LIMIT` and `COMMIT`?
- [ ] Is `lock_timeout` set to prevent queue buildup?
- [ ] Has the migration been tested on a staging database with production-like data volume?
- [ ] Is the migration idempotent (`IF NOT EXISTS` / `IF EXISTS`)?
