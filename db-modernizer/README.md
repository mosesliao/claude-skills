# db-modernizer

A Claude Skill that audits a legacy, badly-designed SQL database over a live connection and
produces a cleanup-and-migration plan landing the data in a clean, normalized schema that
follows Laravel/Eloquent conventions.

Built for the case where an old database has accumulated the usual damage: no primary or
foreign keys, tables split by a trailing counter as a hand-rolled sharding hack
(`Customer1`, `Customer2`, `Customer3`) with no sharding layer, repeating column groups,
duplicated rows, inconsistent enums, money stored as float, dates stored as strings, and
nulls where values are required.

## Workflow

The skill runs in three phases and delivers the audit **first**, before proposing any schema:

1. **Audit** — profiles the real data (not just DDL) over a read-only connection and
   produces an evidence-backed report with severity-ranked findings, a normalization
   assessment, and a data-quality scorecard.
2. **Target Schema** — proposes Laravel migration files plus a source→target mapping so
   nothing is silently dropped.
3. **Migration Plan** — an ordered, resumable plan with per-column transform rules,
   validation gates, and orphan quarantine instead of silent deletion.

## Layout

```
db-modernizer/
├── SKILL.md                          # workflow and phase definitions
├── references/
│   ├── profiling-queries.md          # engine-agnostic + per-engine catalog queries
│   ├── report-template.md            # required audit report structure
│   └── laravel-conventions.md        # Eloquent naming, types, relationships
└── scripts/
    └── profile_db.py                 # read-only DB profiler → JSON
```

## Using the profiler

```bash
pip install sqlalchemy pymysql
python scripts/profile_db.py --dsn "mysql://user:pass@host:3306/dbname"
```

Credentials are read from `--dsn` or the `DB_DSN` environment variable and are never
written into reports. The profiler runs only `SELECT` / catalog queries and never writes
to the source database.

## Safety notes

- The audit is read-only. Migrations are always run against a **copy**, never in place.
- Do not commit `db_profile.json` — it contains your real table and column names.

## Installing as a Claude Skill

Package the folder into a `.skill` file with the skill-creator packager, then upload it in
Claude under Settings → Capabilities → Skills.
