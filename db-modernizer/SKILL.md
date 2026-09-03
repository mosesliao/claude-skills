---
name: db-modernizer
description: >-
  Audit a legacy, poorly-designed SQL database over a live connection, then produce a
  cleanup-and-migration plan that lands the data in a clean, normalized schema following
  Laravel/Eloquent conventions so a new app can be built on trustworthy data. Use this
  skill whenever the user wants to clean up, refactor, re-architect, normalize, or
  "port"/"migrate" an old or messy database; mentions bad data quality, inconsistent
  schemas, or getting data ready for business insights; or references moving a legacy DB
  onto Laravel or a "12-factor" backend. Trigger even if they only say "my database is a
  mess" or "help me redesign this schema" without naming every step — this skill owns the
  full audit → target-schema → migration-plan workflow. Works with any SQL engine
  (MySQL/MariaDB, PostgreSQL, SQL Server, SQLite, etc.).
---

# DB Modernizer

Turn a legacy, badly-maintained SQL database into a clean Laravel-ready schema. The skill
runs in three phases against a **live database connection**: **Audit → Target Schema →
Migration Plan**. Always deliver the audit first and get sign-off before proposing the new
schema, because the redesign is only as good as the problems you correctly identified.

## Before you start

Confirm two things with the user:

1. **Connection details.** How do you reach the database (host/port/db/user, or a DSN, or
   an existing framework `.env`)? Never hardcode or echo credentials into reports or files
   — read them from the environment or a config the user points you at. If no live access
   is possible, offer to work from a schema dump instead, but this skill assumes a live
   connection so you can profile real data, not just DDL.
2. **Read-only is the default.** You will only run non-destructive `SELECT` /
   `INFORMATION_SCHEMA` / `SHOW` / `EXPLAIN` queries during the audit. State this explicitly.
   You never `ALTER`, `DROP`, `UPDATE`, or `DELETE` against the source. The migration plan is
   delivered as scripts the user runs themselves against a copy.

Detect the engine early (`SELECT version()` / `@@version`, or the driver in the DSN) and
adapt catalog queries accordingly — see `references/profiling-queries.md`.

## Phase 1 — Audit (deliver first)

Goal: an evidence-backed picture of what's wrong. Profile the *actual data*, not just the
schema. Use `scripts/profile_db.py` to gather metrics, or run the queries in
`references/profiling-queries.md` manually if the environment lacks Python drivers.

Cover at minimum:

- **Inventory** — tables, row counts, approximate size, engine/collation per table.
- **Structural smells** — missing primary keys, no foreign keys (relationships implied by
  naming only), `VARCHAR(255)`-everything, columns storing CSV/JSON blobs that should be
  rows, boolean-as-`Y/N`/`0/1/'true'` inconsistency, dates stored as strings, money as float.
- **Numbered "pseudo-shard" tables** — families of tables that differ only by a trailing
  number (`Customer1`, `Customer2`, `Customer3`) used as a hand-rolled sharding/partitioning
  hack with no real sharding layer. Treat these as ONE logical entity: they must be UNIONed
  back into a single normalized table in Phase 2, deduplicated across shards (the same row
  often exists in several), with a note on how to detect and merge cross-shard duplicates.
  The profiler reports these under `numbered_table_families`.
- **Normalization violations** — repeating groups (`phone1`, `phone2`, `phone3`),
  derived/duplicated columns, partial and transitive dependencies (candidate 2NF/3NF fixes).
- **Data-quality issues** — nulls where values are required, orphaned rows (broken implicit
  FKs), duplicate entities, inconsistent enumerations (`"NY"` vs `"New York"` vs `"new york"`),
  out-of-range values, encoding/whitespace problems, format drift in dates/emails/phones.
- **Integrity & keys** — natural vs surrogate keys, uniqueness that isn't enforced, columns
  that are effectively FKs but lack constraints.

Write the audit using the exact structure in `references/report-template.md`. Every claim
must cite evidence: a count, a sample query, or specific example values. Rank issues by
severity (Critical / High / Medium / Low) and by migration risk.

## Phase 2 — Target Schema (after audit sign-off)

Propose the clean schema as **Laravel migration files** (`database/migrations/*.php` using
the `Schema::create` builder) plus a short rationale. Follow Eloquent conventions so the
user can scaffold models directly — the details (plural snake_case tables, `id` big-increment
PKs, `foreignId()->constrained()`, `timestamps()`, pivot naming, enum handling) live in
`references/laravel-conventions.md`. Read that file before writing any migration.

Design principles: normalize to 3NF by default (call out any deliberate denormalization for
reporting and why), enforce every relationship with real foreign keys, pick correct types
(decimals for money, native booleans, proper date/time, lookup tables or DB enums for
categoricals), and add the indexes the query patterns imply. Map every source table/column
to its destination in a mapping table so nothing is silently dropped.

## Phase 3 — Migration Plan

Deliver an ordered, resumable plan to move data from old → new **on a copy**, never in place:

- **Ordering** by FK dependency (parents before children).
- **Transform rules** per column — the cleaning logic for each issue found in Phase 1
  (dedupe strategy, enum canonicalization map, type coercions, default backfills, how
  orphans are handled: repair, quarantine table, or drop-with-log).
- **Validation gates** — row-count reconciliation, referential-integrity checks, and
  spot-check queries that must pass before cutover.
- **Rollback / safety** — everything staged, idempotent where possible, run inside
  transactions per table batch.

Prefer expressing transforms as SQL `INSERT ... SELECT` into the new schema, or as a Laravel
seeder/console-command if the user prefers to stay in-framework. State which and why.

## Output structure

Produce three artifacts, in order, as separate files the user can review and download:

1. `audit-report.md`
2. `migrations/` (Laravel migration PHP files) + `schema-mapping.md`
3. `migration-plan.md` (+ any transform SQL/seeders)

Don't skip ahead to Phase 2/3 until the user has seen and accepted the audit.

## Reference files

- `references/profiling-queries.md` — engine-agnostic + engine-specific catalog and
  data-quality queries. Read when starting Phase 1.
- `references/report-template.md` — required structure for `audit-report.md`.
- `references/laravel-conventions.md` — Eloquent naming/type/relationship rules. Read
  before writing migrations in Phase 2.
- `scripts/profile_db.py` — connects and emits a JSON profile of the DB. Run it to gather
  Phase 1 metrics instead of hand-running every query.
