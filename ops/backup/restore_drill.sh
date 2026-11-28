#!/usr/bin/env bash
# Restore drill (TS-EA-06): restore the newest (or given) backup into a SCRATCH database
# inside ats-db, compare row counts with the live database, then drop the scratch copy.
# The live database is only read. Usage: ops/backup/restore_drill.sh [path/to/hrguru_ats-*.dump]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
[ -f "$HERE/backup.env" ] && . "$HERE/backup.env"
BACKUP_DIR="${BACKUP_DIR:-$HOME/HRGuruBackups/ats}"
DC=(docker compose -f "$ROOT/docker-compose.yml")
DUMP="${1:-$(ls -t "$BACKUP_DIR"/hrguru_ats-*.dump 2>/dev/null | head -1)}"
[ -n "$DUMP" ] && [ -f "$DUMP" ] || { echo "No backup found in $BACKUP_DIR"; exit 1; }
SCRATCH=hrguru_drill
psql_live()    { "${DC[@]}" exec -T ats-db psql -U hrguru -d hrguru_ats -tAc "$1"; }
psql_scratch() { "${DC[@]}" exec -T ats-db psql -U hrguru -d "$SCRATCH" -tAc "$1"; }

echo "Restore drill using $(basename "$DUMP")"
"${DC[@]}" exec -T ats-db psql -U hrguru -d postgres -qc "DROP DATABASE IF EXISTS $SCRATCH" >/dev/null 2>&1
"${DC[@]}" exec -T ats-db psql -U hrguru -d postgres -qc "CREATE DATABASE $SCRATCH" >/dev/null
trap '"${DC[@]}" exec -T ats-db psql -U hrguru -d postgres -qc "DROP DATABASE IF EXISTS $SCRATCH" >/dev/null' EXIT
"${DC[@]}" exec -T ats-db pg_restore -U hrguru -d "$SCRATCH" --no-owner < "$DUMP"

status=OK
printf "%-16s %10s %10s\n" table backup live
for t in candidates requirements team_members app_users; do
  b="$(psql_scratch "select count(*) from $t")"; l="$(psql_live "select count(*) from $t")"
  printf "%-16s %10s %10s\n" "$t" "$b" "$l"
  # live may have grown since the backup; the backup must not have MORE rows or be empty
  if [ "$b" -gt "$l" ] || { [ "$t" = candidates ] && [ "$b" -eq 0 ]; }; then status=FAILED; fi
done
echo "Restore drill: $status ($(date '+%Y-%m-%d %H:%M'))"
[ "$status" = OK ]
