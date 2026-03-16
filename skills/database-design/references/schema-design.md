# Schema Design — PostgreSQL Patterns

Production-quality schema design patterns for PostgreSQL. Covers naming, data types, constraints, relationships, and common patterns.

## Naming Conventions

PostgreSQL folds unquoted identifiers to lowercase. Use `snake_case` consistently.

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | singular snake_case | `user`, `order_item` |
| Columns | snake_case | `first_name`, `created_at` |
| Primary keys | `id` | `id BIGINT GENERATED ALWAYS AS IDENTITY` |
| Foreign keys | `{referenced_table}_id` | `user_id`, `organization_id` |
| Indexes | `idx_{table}_{columns}` | `idx_user_email` |
| Unique constraints | `uniq_{table}_{columns}` | `uniq_user_email` |
| Check constraints | `chk_{table}_{description}` | `chk_order_amount_positive` |
| Foreign key constraints | `fk_{table}_{referenced}` | `fk_order_user` |

## Primary Key Strategy

| Strategy | When to Use | Example |
|----------|------------|---------|
| `BIGINT GENERATED ALWAYS AS IDENTITY` | Internal IDs, high-volume tables | Fast, sequential, compact |
| `UUID v7` (sortable) | Distributed systems, public-facing IDs | `gen_random_uuid()` or app-generated UUIDv7 |
| `UUID v4` | Legacy compatibility | Random, poor index locality |

Prefer `BIGINT IDENTITY` for internal tables, UUID v7 for APIs/distributed systems. Never use `SERIAL` — it's legacy and wraps at 2.1B rows.

```sql
-- BIGINT identity (preferred for internal)
CREATE TABLE user (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  -- ...
);

-- UUID (preferred for public-facing)
CREATE TABLE api_key (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- ...
);
```

## Data Type Selection

| Use Case | Type | Why |
|----------|------|-----|
| Text | `TEXT` | No performance difference vs `VARCHAR(n)` in Postgres |
| Text with limit | `VARCHAR(100)` | Only when limit is a business rule (e.g., country codes) |
| Timestamps | `TIMESTAMPTZ` | Always with timezone — never bare `TIMESTAMP` |
| Money | `NUMERIC(12,2)` or `BIGINT` (cents) | Never `FLOAT`/`DOUBLE` — precision errors |
| Boolean | `BOOLEAN` | Not `SMALLINT` or `CHAR(1)` |
| Enums (stable) | `CREATE TYPE status AS ENUM (...)` | For values that rarely change |
| Enums (evolving) | `TEXT` + `CHECK` constraint | Easier to migrate than Postgres ENUM types |
| Structured metadata | `JSONB` | Indexable, supports containment operators |
| Arrays | `TEXT[]`, `INTEGER[]` | For simple tag-like data; avoid for relational data |

### Evolving Enums Pattern

Postgres ENUM types require `ALTER TYPE ... ADD VALUE` which can't run in a transaction. Use TEXT + CHECK for values that change:

```sql
ALTER TABLE order ADD COLUMN status TEXT NOT NULL DEFAULT 'pending'
  CONSTRAINT chk_order_status CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled'));
```

## Constraints

Apply constraints at the database level — application-level validation is insufficient for data integrity.

```sql
CREATE TABLE product (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT NOT NULL,
  price_cents BIGINT NOT NULL,
  stock_quantity INTEGER NOT NULL DEFAULT 0,
  category_id BIGINT NOT NULL REFERENCES category(id),
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at TIMESTAMPTZ,

  CONSTRAINT chk_product_price_positive CHECK (price_cents > 0),
  CONSTRAINT chk_product_stock_non_negative CHECK (stock_quantity >= 0)
);

-- Unique slug only among non-deleted products
CREATE UNIQUE INDEX uniq_product_slug ON product(slug) WHERE deleted_at IS NULL;
```

## Relationships

### One-to-Many

```sql
CREATE TABLE post (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  author_id BIGINT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT NOT NULL
);

CREATE INDEX idx_post_author ON post(author_id);
```

### Many-to-Many (Junction Table)

```sql
CREATE TABLE post_tag (
  post_id BIGINT NOT NULL REFERENCES post(id) ON DELETE CASCADE,
  tag_id BIGINT NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id)
);

CREATE INDEX idx_post_tag_tag ON post_tag(tag_id);
```

### One-to-One

```sql
CREATE TABLE user_profile (
  user_id BIGINT PRIMARY KEY REFERENCES user(id) ON DELETE CASCADE,
  bio TEXT,
  avatar_url TEXT
);
```

## Audit Columns

Every table should have `created_at` and `updated_at`:

```sql
-- Auto-update trigger for updated_at
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to each table
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON product
  FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
```

## Soft Deletes

Add a `deleted_at` column instead of physically removing rows. Critical: update unique constraints to exclude deleted rows.

```sql
ALTER TABLE user ADD COLUMN deleted_at TIMESTAMPTZ;

-- Unique email only among active users
CREATE UNIQUE INDEX uniq_user_email_active ON user(email) WHERE deleted_at IS NULL;

-- Filter deleted rows by default in application queries
-- (use Prisma middleware/extension or Drizzle wrapper)
```

## JSONB Patterns

Use JSONB for semi-structured data. Always validate with CHECK constraints or application-level validation.

```sql
-- Store flexible metadata
ALTER TABLE product ADD COLUMN attributes JSONB NOT NULL DEFAULT '{}';

-- GIN index for containment queries (@>)
CREATE INDEX idx_product_attributes ON product USING GIN (attributes);

-- Query: find products with color = 'red'
SELECT * FROM product WHERE attributes @> '{"color": "red"}';

-- Query: extract nested value
SELECT attributes->>'color' AS color FROM product;
```

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|-------------|---------|----------|
| EAV tables (key/value) | No type safety, no constraints, slow joins | Use JSONB or proper columns |
| `NULL` everywhere | Ambiguous semantics, 3-value logic bugs | Default to `NOT NULL`, use null only with intent |
| Missing foreign keys | Data corruption, orphaned rows | Always define FKs |
| `FLOAT` for money | Precision errors ($0.1 + $0.2 ≠ $0.3) | Use `NUMERIC` or integer cents |
| `SERIAL` for PKs | Wraps at 2.1B, deprecated syntax | Use `BIGINT GENERATED ALWAYS AS IDENTITY` |
| Storing timezone in app | Timezone bugs across regions | Use `TIMESTAMPTZ`, store in UTC |
