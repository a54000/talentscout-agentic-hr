#!/usr/bin/env bash
# Nightly backup of the HR Guru ATS (TS-EA-06).
#   - PostgreSQL: pg_dump custom format (compressed), taken inside the ats-db container
#   - CV/JD uploads: archive of /app/uploads from the ats container
#   - SHA-256 checksums, retention of KEEP_DAYS days, optional copy to OFFSITE_DIR
# Settings (environment or ops/backup/backup.env):
#   BACKUP_DIR   local backup folder        (default: ~/HRGuruBackups/ats)
#   OFFSITE_DIR  second copy, e.g. a Google Drive / iCloud / external-disk folder (default: none)
#   KEEP_DAYS    days of backups to keep    (default: 14)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
[ -f "$HERE/backup.env" ] && . "$HERE/backup.env"
BACKUP_DIR="${BACKUP_DIR:-$HOME/HRGuruBackups/ats}"
KEEP_DAYS="${KEEP_DAYS:-14}"
OFFSITE_DIR="${OFFSITE_DIR:-}"
DC=(docker compose -f "$ROOT/docker-compose.yml")
TS="$(date +%Y%m%d-%H%M%S)"
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*"; }
fail() {
  log "BACKUP FAILED: $*"
  command -v osascript >/dev/null && osascript -e "display notification \"$*\" with title \"HR Guru ATS backup FAILED\"" || true
  exit 1
}
trap 'fail "unexpected error on line $LINENO"' ERR

mkdir -p "$BACKUP_DIR"
DB_FILE="$BACKUP_DIR/hrguru_ats-$TS.dump"
UP_FILE="$BACKUP_DIR/uploads-$TS.tgz"

log "Backing up database to $DB_FILE"
"${DC[@]}" exec -T ats-db pg_dump -U hrguru -d hrguru_ats -Fc > "$DB_FILE.partial" || fail "pg_dump failed"
[ -s "$DB_FILE.partial" ] || fail "database dump is empty"
mv "$DB_FILE.partial" "$DB_FILE"

log "Backing up uploads to $UP_FILE"
STAGE="$(mktemp -d)"
"${DC[@]}" cp ats:/app/uploads "$STAGE/uploads" >/dev/null || fail "copying uploads failed"
tar -czf "$UP_FILE" -C "$STAGE" uploads
rm -rf "$STAGE"

( cd "$BACKUP_DIR" && shasum -a 256 "$(basename "$DB_FILE")" "$(basename "$UP_FILE")" > "checksums-$TS.sha256" 2>/dev/null \
  || sha256sum "$(basename "$DB_FILE")" "$(basename "$UP_FILE")" > "checksums-$TS.sha256" )

log "Removing local backups older than $KEEP_DAYS days"
find "$BACKUP_DIR" -maxdepth 1 -type f \( -name 'hrguru_ats-*.dump' -o -name 'uploads-*.tgz' -o -name 'checksums-*.sha256' \) -mtime +"$KEEP_DAYS" -delete

if [ -n "$OFFSITE_DIR" ]; then
  [ -d "$OFFSITE_DIR" ] || fail "OFFSITE_DIR $OFFSITE_DIR is not available (disk unplugged or folder missing)"
  log "Copying to off-Mac folder $OFFSITE_DIR"
  cp "$DB_FILE" "$UP_FILE" "$BACKUP_DIR/checksums-$TS.sha256" "$OFFSITE_DIR/"
  find "$OFFSITE_DIR" -maxdepth 1 -type f \( -name 'hrguru_ats-*.dump' -o -name 'uploads-*.tgz' -o -name 'checksums-*.sha256' \) -mtime +"$KEEP_DAYS" -delete
else
  log "WARNING: OFFSITE_DIR not set - backups exist only on this Mac"
fi

log "Backup OK: db $(du -h "$DB_FILE" | cut -f1), uploads $(du -h "$UP_FILE" | cut -f1)"
