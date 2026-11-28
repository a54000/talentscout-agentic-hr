"""Schedule logic of the report scheduler (TS-EA-14)."""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import report_scheduler as rs  # noqa: E402

IST = rs.IST


def names(due):
    return [name for name, _argv in due]


def test_same_times_as_the_old_systemd_timers():
    times = {name: hhmm for name, _days, hhmm, _argv in rs.JOBS}
    assert times == {"team-morning-reminder": "10:00", "team-afternoon-reminder": "14:30",
                     "zero-submission-check": "16:00", "team-evening-reminder": "18:00",
                     "daily-submission-report": "19:00", "weekly-submission-report": "19:10"}


def test_job_is_due_after_its_time_and_only_once_a_day():
    monday_1905 = datetime(2026, 11, 30, 19, 5, tzinfo=IST)
    assert "daily-submission-report" in names(rs.due_jobs(monday_1905, {}))
    assert "daily-submission-report" not in names(rs.due_jobs(monday_1905, {"daily-submission-report": "2026-11-30"}))
    assert "daily-submission-report" not in names(rs.due_jobs(datetime(2026, 11, 30, 18, 59, tzinfo=IST), {}))


def test_no_jobs_on_sunday_and_weekly_only_on_saturday():
    assert rs.due_jobs(datetime(2026, 11, 29, 19, 15, tzinfo=IST), {}) == []          # Sunday
    assert "weekly-submission-report" not in names(rs.due_jobs(datetime(2026, 11, 30, 19, 15, tzinfo=IST), {}))
    assert "weekly-submission-report" in names(rs.due_jobs(datetime(2026, 11, 28, 19, 15, tzinfo=IST), {}))


def test_too_late_is_reported_as_missed_not_sent():
    late = datetime(2026, 11, 30, 21, 0, tzinfo=IST)  # 2 h after the daily report
    assert "daily-submission-report" not in names(rs.due_jobs(late, {}))
    assert "daily-submission-report" in rs.missed_jobs(late, {})


def test_utc_clock_is_converted_to_ist():
    utc = datetime(2026, 11, 30, 13, 35).replace(tzinfo=__import__("datetime").timezone.utc)  # 19:05 IST
    assert "daily-submission-report" in names(rs.due_jobs(utc, {}))


def test_next_run_skips_sunday():
    saturday_night = datetime(2026, 11, 28, 22, 0, tzinfo=IST)
    nxt = rs.next_run(saturday_night, rs.MON_SAT, "10:00")
    assert nxt.date().isoformat() == "2026-11-30" and nxt.hour == 10
