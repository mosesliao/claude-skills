#!/usr/bin/env python3
"""Profile a SQL database over a live connection and emit a JSON audit profile.

Read-only: runs only SELECT / information_schema queries. Never writes.

Usage:
    python profile_db.py --dsn "mysql://user:pass@host:3306/dbname"
    python profile_db.py --dsn "postgresql://user:pass@host:5432/dbname"
    python profile_db.py --dsn "sqlite:///path/to/file.db"

Credentials come from the DSN you pass (or set DB_DSN env var); nothing is printed back.
Requires SQLAlchemy plus the matching driver (pymysql / psycopg2-binary / built-in sqlite3).
Install on demand, e.g.:  pip install sqlalchemy pymysql --break-system-packages
"""
import argparse
import json
import os
import sys

try:
    from sqlalchemy import create_engine, inspect, text
except ImportError:
    sys.exit("SQLAlchemy not installed. Run: pip install sqlalchemy <driver> --break-system-packages")


def profile(dsn: str) -> dict:
    engine = create_engine(dsn)
    insp = inspect(engine)
    out = {"dialect": engine.dialect.name, "tables": []}
    with engine.connect() as conn:
        for tbl in insp.get_table_names():
            pk = insp.get_pk_constraint(tbl).get("constrained_columns") or []
            fks = insp.get_foreign_keys(tbl)
            cols = [
                {
                    "name": c["name"],
                    "type": str(c["type"]),
                    "nullable": c["nullable"],
                    "default": str(c.get("default")),
                }
                for c in insp.get_columns(tbl)
            ]
            try:
                rows = conn.execute(text(f"SELECT COUNT(*) FROM {tbl}")).scalar()
            except Exception as e:  # noqa: BLE001
                rows = f"error: {e}"
            out["tables"].append(
                {
                    "name": tbl,
                    "row_count": rows,
                    "primary_key": pk,
                    "has_pk": bool(pk),
                    "foreign_keys": [
                        {"cols": fk["constrained_columns"], "ref": fk["referred_table"]}
                        for fk in fks
                    ],
                    "has_fks": bool(fks),
                    "columns": cols,
                }
            )
    # Detect numbered "pseudo-shard" table families (Customer1, Customer2, ...):
    # same base name differing only by a trailing integer. This is a legacy pattern
    # that must be UNIONed back into one normalized table.
    import re
    from collections import defaultdict

    families = defaultdict(list)
    for t in out["tables"]:
        m = re.match(r"^(.*?)(\d+)$", t["name"])
        if m:
            families[m.group(1).lower()].append(t["name"])
    out["numbered_table_families"] = {
        base: sorted(names) for base, names in families.items() if len(names) > 1
    }

    # Cheap heuristics the caller can turn into findings
    for t in out["tables"]:
        smells = []
        for base, names in out.get("numbered_table_families", {}).items():
            if t["name"] in names:
                smells.append(f"numbered_shard_family:{base}({len(names)} tables)")
        if not t["has_pk"]:
            smells.append("no_primary_key")
        if not t["has_fks"] and len(out["tables"]) > 1:
            smells.append("no_foreign_keys")
        for c in t["columns"]:
            ct = c["type"].upper()
            if "VARCHAR(255)" in ct.replace(" ", ""):
                smells.append(f"varchar255:{c['name']}")
            if "FLOAT" in ct or "DOUBLE" in ct:
                smells.append(f"float_maybe_money:{c['name']}")
        t["smells"] = smells
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default=os.environ.get("DB_DSN"))
    ap.add_argument("--out", default="db_profile.json")
    args = ap.parse_args()
    if not args.dsn:
        sys.exit("Provide --dsn or set DB_DSN env var.")
    profile_data = profile(args.dsn)
    with open(args.out, "w") as f:
        json.dump(profile_data, f, indent=2, default=str)
    print(f"Wrote profile for {len(profile_data['tables'])} tables -> {args.out}")


if __name__ == "__main__":
    main()
