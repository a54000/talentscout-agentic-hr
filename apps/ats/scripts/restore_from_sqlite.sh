#!/usr/bin/env bash
# Restore the HR Guru ATS from a legacy SQLite file (ats.db) into an EMPTY PostgreSQL database.
#
# Steps:
#   1. copy ats.db to a temp dir (the original is never modified) and record its checksum
#   2. upgrade the copy to the current ATS schema (init_db adds missing tables/columns)
#   3. migrate every table into DATABASE_URL (scripts/migrate_sqlite_to_postgres.py)
#   4. print row counts and the newest candidate/requirement dates for verification
# Refuses to run if the target already has ATS tables (protects data written after restore).
#
# Usage (from apps/ats, with the ats-db container running on host port 5433):
#   DATABASE_URL=postgresql://hrguru:<password>@127.0.0.1:5433/hrguru_ats \
#   PYTHON=.venv/bin/python scripts/restore_from_sqlite.sh /path/to/ats.db
set -euo pipefail
SRC="${1:?usage: restore_from_sqlite.sh /path/to/ats.db}"
: "${DATABASE_URL:?DATABASE_URL must point at the empty PostgreSQL database}"
PY="${PYTHON:-python3}"
cd "$(dirname "$0")/.."
[ -f "$SRC" ] || { echo "Not found: $SRC"; exit 1; }

"$PY" - <<'PYEOF'
import os, psycopg2
cur = psycopg2.connect(os.environ["DATABASE_URL"]).cursor()
cur.execute("select to_regclass('public.candidates')")
if cur.fetchone()[0] is not None:
    raise SystemExit("Refusing: target database already has ATS tables. Restore into an empty database.")
PYEOF

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cp -r . "$TMP/app"; rm -f "$TMP/app/ats.db" "$TMP/app"/*.lock
cp "$SRC" "$TMP/app/ats.db"
echo "Source checksum (sha256): $(shasum -a 256 "$SRC" 2>/dev/null || sha256sum "$SRC")"

echo "Upgrading a copy of the SQLite schema to the current ATS version..."
( cd "$TMP/app" && env -u DATABASE_URL SECRET_KEY="${SECRET_KEY:-restore-only}" "$PY" -c "import app; app.init_db()" >/dev/null )

echo "Migrating into PostgreSQL..."
"$PY" scripts/migrate_sqlite_to_postgres.py --sqlite "$TMP/app/ats.db" --database-url "$DATABASE_URL" | tail -n 3

"$PY" - <<'PYEOF'
import os, psycopg2
cur = psycopg2.connect(os.environ["DATABASE_URL"]).cursor()
print("\nRestored data:")
for table, col in [("candidates", "created_at"), ("requirements", "created_at"), ("app_users", None),
                   ("team_members", None), ("submissions", None)]:
    try:
        cur.execute(f"select count(*) from {table}")
        n = cur.fetchone()[0]
        newest = ""
        if col:
            cur.execute(f"select max({col}) from {table}")
            newest = f"  newest {col}: {cur.fetchone()[0]}"
        print(f"  {table:<14} {n:>7}{newest}")
    except Exception as exc:  # table may not exist in very old files
        cur.connection.rollback()
        print(f"  {table:<14} (not present: {type(exc).__name__})")
print("\nCompare with the last known production counts (about 3,600 candidates, 400 requirements).")
PYEOF
