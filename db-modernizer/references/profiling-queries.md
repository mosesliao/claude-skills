# Profiling Queries

Read-only queries for Phase 1. Detect the engine first, then use the matching catalog
queries. All data-quality queries below are plain ANSI SQL and work everywhere.

## Engine detection
- MySQL/MariaDB: `SELECT VERSION();`
- PostgreSQL: `SELECT version();`
- SQL Server: `SELECT @@VERSION;`
- SQLite: `SELECT sqlite_version();`

## Catalog / structure

**Tables + approximate rows**
- MySQL: `SELECT table_name, table_rows, engine, table_collation FROM information_schema.tables WHERE table_schema = DATABASE();`
- PostgreSQL: `SELECT relname, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC;`
- SQL Server: query `sys.tables` joined to `sys.dm_db_partition_stats`.
- SQLite: `SELECT name FROM sqlite_master WHERE type='table';` then `COUNT(*)` per table.

**Columns + types** (MySQL/Postgres/SQL Server all expose `information_schema.columns`):
```sql
SELECT table_name, column_name, data_type, is_nullable, character_maximum_length, column_default
FROM information_schema.columns
WHERE table_schema = <schema>
ORDER BY table_name, ordinal_position;
```

**Primary keys / foreign keys**: `information_schema.table_constraints` +
`key_column_usage` (MySQL/Postgres/SQL Server). SQLite: `PRAGMA table_info(t)` and
`PRAGMA foreign_key_list(t)`. **Absence** of rows here is itself a finding (no enforced keys).

## Data-quality (ANSI, run per suspect column)

**Null rate**
```sql
SELECT COUNT(*) total, COUNT(col) non_null, COUNT(*)-COUNT(col) nulls FROM t;
```
**Distinct-value / enum drift** (spot inconsistent categoricals)
```sql
SELECT col, COUNT(*) FROM t GROUP BY col ORDER BY COUNT(*) DESC;
```
**Duplicate entities** (adjust key columns)
```sql
SELECT keycols, COUNT(*) c FROM t GROUP BY keycols HAVING COUNT(*) > 1 ORDER BY c DESC;
```
**Orphans / broken implicit FK** (child references missing parent)
```sql
SELECT COUNT(*) FROM child c
LEFT JOIN parent p ON c.parent_id = p.id
WHERE c.parent_id IS NOT NULL AND p.id IS NULL;
```
**Format drift** — sample values to eyeball dates-as-strings, `Y/N` booleans, money as
float, CSV-in-a-cell, whitespace/encoding:
```sql
SELECT DISTINCT col FROM t LIMIT 50;
```
**Range / validity** — min/max/avg on numerics and dates to catch impossible values:
```sql
SELECT MIN(col), MAX(col), AVG(col) FROM t;
```

## Notes
- Prefer `information_schema` estimates for row counts on huge tables; use exact `COUNT(*)`
  only where precision matters.
- Never run anything that writes. If a check would need a temp table, use a CTE/subquery
  instead.
