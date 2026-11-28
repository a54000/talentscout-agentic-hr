"""Baseline numbers from the ATS for TS-E0-08 (read-only, aggregates only: no names, emails or phones).

  docker compose exec ats python scripts/baseline_ats_metrics.py [--days 90] [--end 2026-05-26]

By default the window is the --days before the newest candidate record (the restored data ends
2026-05-26, so "the last 90 days" from today would be empty). Prints a markdown block to paste
into docs/00-discovery/baseline-results.md.
"""
import argparse
import os
import statistics
import sys
from collections import Counter
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ATS_PROCESS_ROLE", "worker")  # do not start upload threads in this process

from app import get_db  # noqa: E402

PROGRESSED = {"shortlisted", "interview", "interview scheduled", "selected", "offered", "joined"}


def day(value):
    try:
        return datetime.fromisoformat(str(value)[:19]).date()
    except (TypeError, ValueError):
        return None


def pct(part, whole):
    return f"{(100 * part / whole):.1f}%" if whole else "n/a"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=90)
    parser.add_argument("--end", help="last day of the window (YYYY-MM-DD); default: newest candidate record")
    args = parser.parse_args()
    conn = get_db()
    try:
        newest = conn.execute("SELECT MAX(created_at) AS m FROM candidates").fetchone()["m"]
        end = date.fromisoformat(args.end) if args.end else (day(newest) or date.today())
        start = end - timedelta(days=args.days - 1)
        lo, hi = start.isoformat(), (end + timedelta(days=1)).isoformat()
        cands = [dict(r) for r in conn.execute(
            "SELECT created_at, status, is_duplicate, missing_info, cv_url, cv_filename, recruiter_email, requirement_id "
            "FROM candidates WHERE created_at >= ? AND created_at < ?", (lo, hi)).fetchall()]
        reqs = [dict(r) for r in conn.execute(
            "SELECT id, created_at FROM requirements WHERE created_at >= ? AND created_at < ?", (lo, hi)).fetchall()]
        first_sub = {}
        for r in conn.execute("SELECT requirement_id, MIN(created_at) AS first_at FROM candidates "
                              "WHERE requirement_id IS NOT NULL GROUP BY requirement_id").fetchall():
            first_sub[r["requirement_id"]] = r["first_at"]
    finally:
        conn.close()

    n = len(cands)
    weeks = max(1, args.days / 7)
    by_recruiter = Counter((c["recruiter_email"] or "").lower() for c in cands if c["recruiter_email"])
    per_recruiter_week = sorted(v / weeks for v in by_recruiter.values())
    statuses = Counter((c["status"] or "New").strip() for c in cands)
    progressed = sum(1 for c in cands if (c["status"] or "").strip().lower() in PROGRESSED)
    dup = sum(1 for c in cands if str(c["is_duplicate"] or 0) in ("1", "True", "true"))
    missing = sum(1 for c in cands if str(c["missing_info"] or "").strip())
    no_cv = sum(1 for c in cands if not (c["cv_url"] or c["cv_filename"]))
    no_req = sum(1 for c in cands if not c["requirement_id"])
    lead_days = []
    for r in reqs:
        a, b = day(r["created_at"]), day(first_sub.get(r["id"]))
        if a and b and b >= a:
            lead_days.append((b - a).days)

    print(f"""### ATS baseline: {start} to {end} ({args.days} days)

| Metric | Value |
|---|---|
| Candidates submitted | {n} ({n / weeks:.0f} per week) |
| Active recruiters | {len(by_recruiter)} |
| Submissions per recruiter per week (median, p25–p75) | {statistics.median(per_recruiter_week) if per_recruiter_week else 0:.1f} ({per_recruiter_week[len(per_recruiter_week)//4] if per_recruiter_week else 0:.1f}–{per_recruiter_week[(3*len(per_recruiter_week))//4] if per_recruiter_week else 0:.1f}) |
| Flagged as duplicate by the ATS | {dup} ({pct(dup, n)}) |
| With missing required info | {missing} ({pct(missing, n)}) |
| Without a CV file | {no_cv} ({pct(no_cv, n)}) |
| Not linked to a requirement | {no_req} ({pct(no_req, n)}) |
| Progressed past submission (shortlisted → joined) | {progressed} ({pct(progressed, n)}) |
| Requirements opened | {len(reqs)} |
| Days from requirement to first submission (median, n) | {statistics.median(lead_days) if lead_days else 'n/a'} (n={len(lead_days)}) |

Status mix: {", ".join(f"{k} {v}" for k, v in statuses.most_common(10))}

Notes: aggregates only; candidate data after 2026-05-26 was lost with the EC2 host, so windows ending later are incomplete.
""")


if __name__ == "__main__":
    main()
