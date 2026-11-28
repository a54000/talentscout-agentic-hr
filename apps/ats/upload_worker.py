"""Bulk upload worker (TS-EA-12).

Runs queued upload jobs in its own process, so parsing CVs never slows down the
web server. Used with PostgreSQL: docker compose service `ats-worker`, with
ATS_UPLOAD_WORKER=external on the web service. With SQLite, uploads run in a
background thread of the web process instead (the default, ATS_UPLOAD_WORKER=inline).
"""
import os
import signal
import sys
import time

os.environ["ATS_PROCESS_ROLE"] = "worker"

import app as ats  # noqa: E402  (the environment must be set before the app loads)

POLL_SECONDS = float(os.getenv("ATS_UPLOAD_WORKER_POLL_SECONDS", "2"))
_stopping = False


def _stop(*_args):
    global _stopping
    _stopping = True


def main():
    if not ats.USE_POSTGRES:
        print("upload worker: needs PostgreSQL (DATABASE_URL). With SQLite, uploads run inside the web process.", flush=True)
        return 1
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    print("upload worker: started", flush=True)
    while not _stopping:
        try:
            for job_id in ats.recover_upload_jobs():
                if _stopping:
                    break
                print(f"upload worker: job {job_id} started", flush=True)
                ats.run_upload_job(job_id)
                print(f"upload worker: job {job_id} finished", flush=True)
        except Exception as exc:
            ats.report_error(exc, "Upload worker loop")
        time.sleep(POLL_SECONDS)
    print("upload worker: stopped", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
