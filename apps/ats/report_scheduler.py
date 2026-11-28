"""Scheduled WhatsApp reports for the ATS (TS-EA-14).

Replaces the six systemd timers from the old EC2 host (apps/ats/deploy/systemd). Runs as the
`ats-scheduler` Docker service, separate from the web app, so a failing report never affects
the ATS. Times are India time (IST, UTC+05:30, no daylight saving).

  python report_scheduler.py            # run forever
  python report_scheduler.py --list     # show the schedule and the next run of each job
  python report_scheduler.py --run-now daily-submission-report [--dry-run]
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))
HERE = os.path.dirname(os.path.abspath(__file__))
MON_SAT = (0, 1, 2, 3, 4, 5)

# name, weekdays (Mon=0), "HH:MM" IST, script and arguments: the same as the old systemd timers
JOBS = [
    ("team-morning-reminder", MON_SAT, "10:00", ["scripts/send_team_whatsapp_reminder.py", "morning"]),
    ("team-afternoon-reminder", MON_SAT, "14:30", ["scripts/send_team_whatsapp_reminder.py", "afternoon"]),
    ("zero-submission-check", MON_SAT, "16:00", ["scripts/no_submission_so_far_whatsapp_report.py"]),
    ("team-evening-reminder", MON_SAT, "18:00", ["scripts/send_team_whatsapp_reminder.py", "evening"]),
    ("daily-submission-report", MON_SAT, "19:00", ["scripts/daily_team_submission_whatsapp_report.py", "--format", "text"]),
    ("weekly-submission-report", (5,), "19:10", ["scripts/weekly_team_submission_whatsapp_report.py"]),
]
GRACE_MINUTES = int(os.getenv("ATS_REPORT_GRACE_MINUTES", "60"))  # still send if the Mac was asleep this long
STATE_FILE = os.getenv("ATS_REPORT_STATE_FILE", "/data/report_scheduler_state.json")
JOB_TIMEOUT = int(os.getenv("ATS_REPORT_TIMEOUT_SECONDS", "600"))


def log(message):
    print(f"{datetime.now(IST):%Y-%m-%d %H:%M:%S} IST | {message}", flush=True)


def scheduled_at(day, hhmm):
    hour, minute = (int(x) for x in hhmm.split(":"))
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=IST)


def due_jobs(now, state, jobs=JOBS, grace_minutes=GRACE_MINUTES):
    """Jobs whose time today has passed, that have not run today, and are not too late."""
    now = now.astimezone(IST)
    due = []
    for name, days, hhmm, argv in jobs:
        if now.weekday() not in days:
            continue
        at = scheduled_at(now, hhmm)
        if not (at <= now <= at + timedelta(minutes=grace_minutes)):
            continue
        if state.get(name) == now.date().isoformat():
            continue
        due.append((name, argv))
    return due


def missed_jobs(now, state, jobs=JOBS, grace_minutes=GRACE_MINUTES):
    """Jobs skipped today because the scheduler was down past the grace period (logged, not sent late)."""
    now = now.astimezone(IST)
    missed = []
    for name, days, hhmm, _argv in jobs:
        if now.weekday() in days and now > scheduled_at(now, hhmm) + timedelta(minutes=grace_minutes) \
                and state.get(name) != now.date().isoformat():
            missed.append(name)
    return missed


def next_run(now, days, hhmm):
    now = now.astimezone(IST)
    for offset in range(8):
        day = now + timedelta(days=offset)
        at = scheduled_at(day, hhmm)
        if day.weekday() in days and at > now:
            return at
    return None


def load_state():
    try:
        with open(STATE_FILE) as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE) or ".", exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as handle:
        json.dump(state, handle)
    os.replace(tmp, STATE_FILE)


def run_job(name, argv, dry_run=False):
    cmd = [sys.executable, *argv] + ([] if dry_run else ["--send"])
    env = dict(os.environ, ATS_PROCESS_ROLE="worker")  # report scripts must not start upload threads
    log(f"{name}: starting ({'dry run' if dry_run else 'send'})")
    try:
        done = subprocess.run(cmd, cwd=HERE, env=env, capture_output=True, text=True, timeout=JOB_TIMEOUT)
    except subprocess.TimeoutExpired:
        log(f"{name}: FAILED - timed out after {JOB_TIMEOUT}s")
        return False
    tail = "\n".join((done.stdout + done.stderr).strip().splitlines()[-15:])
    if done.returncode == 0:
        log(f"{name}: ok\n{tail}")
        return True
    log(f"{name}: FAILED (exit {done.returncode})\n{tail}")
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--run-now")
    parser.add_argument("--dry-run", action="store_true", help="print the message without sending it")
    args = parser.parse_args()
    if args.list:
        now = datetime.now(IST)
        for name, days, hhmm, argv in JOBS:
            print(f"{name:26} {hhmm} IST  next: {next_run(now, days, hhmm):%a %Y-%m-%d %H:%M}  -> {' '.join(argv)}")
        return 0
    if args.run_now:
        jobs = {name: argv for name, _d, _t, argv in JOBS}
        if args.run_now not in jobs:
            print(f"unknown job; choose one of: {', '.join(jobs)}")
            return 2
        return 0 if run_job(args.run_now, jobs[args.run_now], dry_run=args.dry_run) else 1

    log(f"report scheduler started: {len(JOBS)} jobs, grace {GRACE_MINUTES} min, state {STATE_FILE}")
    reported_missed = set()
    while True:
        now = datetime.now(IST)
        state = load_state()
        for name in missed_jobs(now, state):
            key = f"{name}:{now.date()}"
            if key not in reported_missed:
                log(f"{name}: MISSED today (scheduler was down past the {GRACE_MINUTES}-min grace); not sent late")
                reported_missed.add(key)
        for name, argv in due_jobs(now, state):
            run_job(name, argv)  # success or failure, it is not retried today (no duplicate messages)
            state[name] = now.date().isoformat()
            save_state(state)
        time.sleep(30)


if __name__ == "__main__":
    sys.exit(main())
