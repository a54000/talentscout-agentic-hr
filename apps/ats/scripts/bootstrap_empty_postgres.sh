#!/usr/bin/env bash
# Create the ATS schema in an EMPTY PostgreSQL database.
# The ATS creates its schema in SQLite mode; production PostgreSQL was always populated by
# scripts/migrate_sqlite_to_postgres.py. This script does the same for a fresh install:
#   1. build an empty SQLite schema (plus the admin user if ADMIN_PASSWORD is set)
#   2. migrate it into DATABASE_URL
# Refuses to run if the target already has a candidates table (protects live data).
# Usage: DATABASE_URL=postgresql://... SECRET_KEY=... [ADMIN_PASSWORD=...] scripts/bootstrap_empty_postgres.sh
set -euo pipefail
: "${DATABASE_URL:?DATABASE_URL must point at the empty PostgreSQL database}"
: "${SECRET_KEY:?SECRET_KEY is required}"
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
"$PY" - <<'PYEOF'
import os, psycopg2
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()
cur.execute("select to_regclass('public.candidates')")
if cur.fetchone()[0] is not None:
    raise SystemExit("Refusing: target database already has ATS tables. Use a restore procedure instead.")
PYEOF
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cp -r . "$TMP/app"
( cd "$TMP/app" && rm -f ats.db && env -u DATABASE_URL "$PY" -c "import app; app.init_db()" >/dev/null )
"$PY" scripts/migrate_sqlite_to_postgres.py --sqlite "$TMP/app/ats.db" --database-url "$DATABASE_URL"
echo "Empty ATS schema created in PostgreSQL."
