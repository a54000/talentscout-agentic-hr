#!/usr/bin/env bash
# ATS smoke test: boots the app with waitress and checks health, admin login and core APIs.
# Usage: apps/ats/tests/smoke_test.sh [python-bin]
# Uses SQLite unless DATABASE_URL is set. Runs in a temporary copy so no state is left behind.
set -euo pipefail
PY="${1:-python3}"
SRC="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; JAR="$WORK/cookies"; PORT="${ATS_SMOKE_PORT:-5099}"
cp -r "$SRC/." "$WORK/app"; cd "$WORK/app"
export SECRET_KEY="smoke-test-only" ADMIN_PASSWORD="smoke-admin-pw"
if [ "${ATS_SMOKE_SERVER:-waitress}" = gunicorn ]; then
  "$(dirname "$PY")/gunicorn" --bind 127.0.0.1:"$PORT" --workers 3 --worker-class gthread --threads 4 app:app >"$WORK/ats.log" 2>&1 &
else
  "$(dirname "$PY")/waitress-serve" --host=127.0.0.1 --port="$PORT" app:app >"$WORK/ats.log" 2>&1 &
fi
PID=$!; trap 'kill $PID 2>/dev/null || true; for _ in $(seq 1 40); do kill -0 $PID 2>/dev/null || break; sleep 0.5; done; rm -rf "$WORK"' EXIT
for _ in $(seq 1 40); do curl -fsS "http://127.0.0.1:$PORT/healthz" 2>/dev/null | grep -q '"ok":true' && break; sleep 1; done
fail() { echo "FAIL: $1"; tail -40 "$WORK/ats.log"; exit 1; }
curl -fsS "http://127.0.0.1:$PORT/healthz" | grep -q '"database":"ok"' || fail "healthz"
if grep -qiE "Traceback|initialization error" "$WORK/ats.log"; then fail "startup errors in log"; fi
code=$(curl -s -o /dev/null -w '%{http_code}' -c "$JAR" -b "$JAR" -d "username=admin&password=$ADMIN_PASSWORD" "http://127.0.0.1:$PORT/login")
[ "$code" = "302" ] || fail "admin login returned $code"
for path in /app /api/candidates /api/requirements; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -b "$JAR" "http://127.0.0.1:$PORT$path")
  [ "$code" = "200" ] || fail "$path returned $code"
done
# AI screening was removed from the ATS (2026-11-28): routes return 410 and the menu is gone
code=$(curl -s -o /dev/null -w '%{http_code}' -b "$JAR" -X POST "http://127.0.0.1:$PORT/api/jd_match")
[ "$code" = "410" ] || fail "/api/jd_match returned $code, expected 410"
if curl -fsS -b "$JAR" "http://127.0.0.1:$PORT/app" | grep -q 'data-top-tab="ai-screening"'; then fail "AI Screening menu still on /app"; fi
# JD parsing for new requirements still works after the AI code was removed (TS-EA-15)
curl -fsS -b "$JAR" -H 'Content-Type: application/json' -d '{"jd_text":"Senior Java Developer. 5-8 years. Must have Java, Spring Boot, SQL. Location: Pune."}' \
  "http://127.0.0.1:$PORT/api/parse_jd" | grep -qi '"java"' || fail "/api/parse_jd did not return Java as a skill"
# Background bulk upload (TS-EA-12); ATS_SMOKE_RESUME=1 also tests resume after a crash (PostgreSQL)
"$PY" tests/bulk_upload_check.py "http://127.0.0.1:$PORT" "$ADMIN_PASSWORD" ${ATS_SMOKE_RESUME:+--resume} || fail "bulk upload check"
if [ -n "${DATABASE_URL:-}" ]; then MODE=postgres; else MODE=sqlite; fi
echo "ATS smoke test passed ($MODE, ${ATS_SMOKE_SERVER:-waitress})"
