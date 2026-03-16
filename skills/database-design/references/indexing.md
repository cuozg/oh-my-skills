# Indexing — PostgreSQL Index Strategies

When and how to create indexes for PostgreSQL. Covers index types, composite indexes, partial indexes, and common mistakes.

## Index Type Selection

| Type | Use Case | Example |
|------|----------|---------|
| **B-Tree** (default) | Equality (`=`), range (`<`, `>`, `BETWEEN`), sorting | `CREATE INDEX idx_user_email ON user(email)` |
| **GIN** | JSONB containment (`@>`), full-text search (`@@`), arrays | `CREATE INDEX idx_product_attrs ON product USING GIN (attributes)` |
| **GiST** | Geometry, range types, nearest-neighbor | `CREATE INDEX idx_location ON place USING GIST (coordinates)` |
| **BRIN** | Very large tables with natural ordering (time-series) | `CREATE INDEX idx_log_ts ON log USING BRIN (created_at)` |
| **Hash** | Equality-only (rare — B-tree usually better) | `CREATE INDEX idx_session_token ON session USING HASH (token)` |

## When to Index

**Index these columns:**
- Foreign keys (Postgres does NOT auto-index FK columns — always add manually)
- Columns in `WHERE` clauses of frequent queries
- Columns in `ORDER BY` of paginated queries
- Columns in `JOIN` conditions
- Unique constraints (auto-creates an index)

**Do NOT index these:**
- Small tables (< 1000 rows) — sequential scan is faster
- Low-cardinality columns (e.g., `boolean is_active`) — unless combined with a partial index
- Frequently updated columns — index maintenance overhead outweighs read benefit
- Columns only used in `SELECT` (not `WHERE`/`ORDER BY`/`JOIN`)

## Composite Indexes

Column order matters. The **leftmost prefix rule** determines which queries can use the index.

```sql
-- This index supports queries filtering on:
-- (tenant_id), (tenant_id, status), (tenant_id, status, created_at)
-- But NOT (status) alone or (status, created_at) alone
CREATE INDEX idx_order_tenant_status_date
  ON order(tenant_id, status, created_at);
```

**Column order guidelines:**
1. Put equality columns first (`tenant_id = ?`)
2. Put range/sort columns last (`created_at > ?`)
3. High-cardinality columns before low-cardinality

## Partial Indexes

Index only a subset of rows. Reduces index size and speeds up writes.

```sql
-- Only index active users (most queries filter by active)
CREATE INDEX idx_user_email_active
  ON user(email) WHERE deleted_at IS NULL;

-- Only index pending orders (status check is frequent)
CREATE INDEX idx_order_pending
  ON order(created_at) WHERE status = 'pending';

-- Unique constraint on active records only (soft delete safe)
CREATE UNIQUE INDEX uniq_user_email
  ON user(email) WHERE deleted_at IS NULL;
```

## Expression Indexes

Index the result of a function for case-insensitive or computed lookups.

```sql
-- Case-insensitive email lookup
CREATE INDEX idx_user_email_lower ON user(lower(email));
-- Query MUST use lower(): SELECT * FROM user WHERE lower(email) = 'foo@bar.com';

-- Year extraction for time-based partitioning queries
CREATE INDEX idx_order_year ON order(EXTRACT(YEAR FROM created_at));
```

## Covering Indexes (INCLUDE)

Add extra columns to an index so Postgres can serve the query from the index alone (Index-Only Scan) without touching the table heap.

```sql
-- Index covers both the lookup and the selected columns
CREATE INDEX idx_order_status_covering
  ON order(status, created_at)
  INCLUDE (total_amount, customer_id);

-- This query uses Index-Only Scan — no heap access:
SELECT total_amount, customer_id
FROM order
WHERE status = 'shipped'
ORDER BY created_at DESC
LIMIT 20;
```

## Full-Text Search Indexes

```sql
-- Add a generated tsvector column for efficient FTS
ALTER TABLE post ADD COLUMN search_vector TSVECTOR
  GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(content, '')), 'B')
  ) STORED;

CREATE INDEX idx_post_search ON post USING GIN (search_vector);

-- Query
SELECT * FROM post
WHERE search_vector @@ plainto_tsquery('english', 'database design')
ORDER BY ts_rank(search_vector, plainto_tsquery('english', 'database design')) DESC;
```

## JSONB Indexes

```sql
-- GIN index for containment queries
CREATE INDEX idx_product_metadata ON product USING GIN (metadata);
-- Supports: WHERE metadata @> '{"color": "red"}'

-- Expression index for specific JSON paths
CREATE INDEX idx_product_category ON product((metadata->>'category'));
-- Supports: WHERE metadata->>'category' = 'electronics'

-- GIN with jsonb_path_ops (smaller, faster for @> only)
CREATE INDEX idx_product_metadata_pathops
  ON product USING GIN (metadata jsonb_path_ops);
```

## Concurrent Index Creation

In production, always create indexes concurrently to avoid locking the table:

```sql
-- Non-blocking (can take longer, but doesn't lock writes)
CREATE INDEX CONCURRENTLY idx_order_customer ON order(customer_id);

-- If it fails partway, clean up the invalid index:
-- DROP INDEX CONCURRENTLY idx_order_customer;
-- Then retry.
```

**Caveats:**
- Cannot run inside a transaction
- Takes longer than non-concurrent
- May fail and leave an INVALID index — check with `\d tablename` and retry if needed

## Index Maintenance

```sql
-- Check index usage (unused indexes waste space and slow writes)
SELECT
  schemaname, tablename, indexname,
  idx_scan AS times_used,
  pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Check bloat and consider REINDEX for fragmented indexes
REINDEX INDEX CONCURRENTLY idx_order_customer;
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Missing FK indexes | Slow joins, slow cascading deletes | Always index FK columns |
| Over-indexing | Slower writes, more disk, no read benefit | Remove unused indexes (check `pg_stat_user_indexes`) |
| Wrong composite order | Index not used for your query pattern | Equality columns first, range columns last |
| Non-concurrent in prod | Table locked during index build | Always use `CONCURRENTLY` |
| Indexing low-cardinality | B-tree on boolean — useless | Use partial index instead |
