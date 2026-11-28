"""ATS load test: 25 recruiters working at once, with and without a bulk upload (TS-EA-13, NFR-ATS-1).

Run against a copy of the ATS, never the live one: the test creates users, synthetic
candidates and requirements (all marked with a run tag) and deletes them at the end.

  DATABASE_URL=postgresql://... ATS_BASE_URL=http://127.0.0.1:5001 \
  ATS_LOAD_USERS=25 ATS_LOAD_SECONDS=60 ATS_LOAD_SEED=10000 \
  python scripts/load_test_recruiters.py --admin-password <admin password> [--report results.md]

Phase A: every recruiter loops over the main pages and APIs for ATS_LOAD_SECONDS.
Phase B: the same load while the admin bulk-uploads ATS_LOAD_UPLOAD_ROWS dummy candidates.
Output: p50/p95 per endpoint for both phases, the slowdown during the upload, and the
upload timings, checked against NFR-ATS-1/2 (p95 < 1 s, upload accepted < 5 s, no request
more than 2x slower while an upload runs).
"""
import argparse
import concurrent.futures
import os
import random
import secrets
import shutil
import statistics
import subprocess
import sys
import tempfile
import threading
import time

import requests

ATS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ATS_DIR)
os.environ.setdefault("ATS_PROCESS_ROLE", "worker")  # do not start inline upload threads in this process

from app import USE_POSTGRES, get_db, hash_password  # noqa: E402

BASE_URL = os.getenv("ATS_BASE_URL", "http://127.0.0.1:5001").rstrip("/")
USERS = int(os.getenv("ATS_LOAD_USERS", "25"))
SECONDS = float(os.getenv("ATS_LOAD_SECONDS", "60"))
SEED = int(os.getenv("ATS_LOAD_SEED", "10000"))
UPLOAD_ROWS = int(os.getenv("ATS_LOAD_UPLOAD_ROWS", "100"))
THINK_SECONDS = float(os.getenv("ATS_LOAD_THINK_SECONDS", "0.5"))  # pause between a recruiter's clicks
PASSWORD = "LoadTestRecruiter#2026"
RUN = secrets.token_hex(3)
SKILLS = ["AWS", "Java", "Python", "React", "Terraform", "Kubernetes", "SAP", "Salesforce", "Azure", "SQL"]
CITIES = ["Gurgaon", "Noida", "Bengaluru", "Pune", "Hyderabad", "Chennai", "Mumbai"]


def pct(values, p):
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, round(p / 100 * (len(ordered) - 1))))]


# ── setup and cleanup ────────────────────────────────────────────────────────
def setup():
    conn = get_db()
    try:
        req_ids = []
        for i in range(max(1, SEED // 6)):
            req_ids.append(conn.execute(
                "INSERT INTO requirements (title, description, client_name, status, created_by) VALUES (?,?,?,?,?)",
                (f"LT{RUN} {random.choice(SKILLS)} Engineer {i}", "Synthetic load-test requirement.",
                 f"LT{RUN} Client {i % 40}", "Open", f"loadtest_{RUN}")).lastrowid)
        upload_title = f"LT{RUN} Upload Target"
        req_ids.append(conn.execute(
            "INSERT INTO requirements (title, description, client_name, status, created_by) VALUES (?,?,?,?,?)",
            (upload_title, "Synthetic load-test requirement.", f"LT{RUN} Client", "Open", f"loadtest_{RUN}")).lastrowid)
        users = []
        for i in range(USERS):
            email = f"lt-{RUN}-{i}@example.test"
            team_id = conn.execute(
                "INSERT INTO team_members (name, email, phone, role, can_bulk_upload, is_fixed) VALUES (?,?,?,?,?,1)",
                (f"LT{RUN} Recruiter {i}", email, f"98{secrets.randbelow(10**8):08d}", "Recruiter", 0)).lastrowid
            conn.execute(
                "INSERT INTO app_users (username, password, email, team_member_id, is_admin, is_bulk_admin, is_active) "
                "VALUES (?,?,?,?,0,0,1)", (f"lt_{RUN}_{i}", hash_password(PASSWORD), email, team_id))
            users.append({"username": f"lt_{RUN}_{i}", "email": email, "name": f"LT{RUN} Recruiter {i}"})
        rows = []
        for i in range(SEED):
            owner = users[i % len(users)]
            rows.append((f"lt{RUN}", owner["name"], owner["email"], f"LT{RUN} Candidate {i}",
                         f"lt-{RUN}-cand-{i}@example.test", f"97{secrets.randbelow(10**8):08d}", "Example Corp",
                         "Engineer", str(random.randint(2, 20)), ", ".join(random.sample(SKILLS, 4)), "30 days",
                         random.choice(CITIES), random.choice(req_ids[:-1])))
        conn.executemany(
            "INSERT INTO candidates (upload_batch, recruiter_name, recruiter_email, candidate_name, email_addr, phone, "
            "current_company, current_role, experience_years, key_skills, notice_period, current_location, requirement_id) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", rows) if hasattr(conn, "executemany") else [
            conn.execute("INSERT INTO candidates (upload_batch, recruiter_name, recruiter_email, candidate_name, email_addr, "
                         "phone, current_company, current_role, experience_years, key_skills, notice_period, "
                         "current_location, requirement_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", row) for row in rows]
        conn.commit()
        for user in users:  # recruiters may open only their own candidates
            user["candidate_ids"] = [r["id"] for r in conn.execute(
                "SELECT id FROM candidates WHERE recruiter_email=? ORDER BY id LIMIT 100", (user["email"],)).fetchall()]
        return users, upload_title
    finally:
        conn.close()


def cleanup():
    conn = get_db()
    try:
        ids = [r["id"] for r in conn.execute(
            "SELECT id FROM candidates WHERE email_addr LIKE ? OR email_addr LIKE ?",
            (f"lt-{RUN}-%@example.test", f"dummy.%@example.com")).fetchall()]
        for start in range(0, len(ids), 500):
            chunk = ids[start:start + 500]
            marks = ",".join("?" * len(chunk))
            conn.execute(f"DELETE FROM alerts WHERE candidate_id IN ({marks})", chunk)
            conn.execute(f"DELETE FROM candidates WHERE id IN ({marks})", chunk)
        conn.execute("DELETE FROM requirements WHERE created_by=?", (f"loadtest_{RUN}",))
        conn.execute("DELETE FROM user_login_audit WHERE username LIKE ?", (f"lt_{RUN}_%",))
        conn.execute("DELETE FROM app_users WHERE username LIKE ?", (f"lt_{RUN}_%",))
        conn.execute("DELETE FROM team_members WHERE email LIKE ?", (f"lt-{RUN}-%@example.test",))
        conn.commit()
        return len(ids)
    finally:
        conn.close()


# ── traffic ──────────────────────────────────────────────────────────────────
def endpoints():
    return [
        ("GET /app", lambda user: "/app"),
        ("GET /api/me", lambda user: "/api/me"),
        ("GET /api/candidates (page)", lambda user: "/api/candidates?page=1&page_size=15"),
        ("GET /api/candidates (search)", lambda user: f"/api/candidates?page=1&page_size=15&q={random.choice(SKILLS)}"),
        ("GET /api/candidate/<id>", lambda user: f"/api/candidate/{random.choice(user['candidate_ids'])}"),
        ("GET /api/requirements", lambda user: "/api/requirements"),
        ("GET /api/team", lambda user: "/api/team"),
        ("GET /api/stats", lambda user: "/api/stats"),
    ]


def recruiter(user, eps, stop, samples, errors):
    session = requests.Session()
    res = session.post(f"{BASE_URL}/login", data={"username": user["username"], "password": PASSWORD},
                       allow_redirects=False, timeout=30)
    if res.status_code not in (302, 303):
        errors.append(f"login {user['username']}: {res.status_code}")
        return
    while not stop.is_set():
        name, path = random.choice(eps)
        started = time.perf_counter()
        try:
            r = session.get(f"{BASE_URL}{path(user)}", timeout=60)
            elapsed = time.perf_counter() - started
            if r.status_code >= 400:
                errors.append(f"{name}: {r.status_code}")
            samples.setdefault(name, []).append(elapsed)
        except Exception as exc:
            errors.append(f"{name}: {type(exc).__name__}")
        time.sleep(random.uniform(0, THINK_SECONDS * 2))


def run_phase(users, eps, seconds, during=None):
    samples, errors, stop = {}, [], threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(users) + 1) as pool:
        futures = [pool.submit(recruiter, u, eps, stop, samples, errors) for u in users]
        extra = during() if during else None
        if extra is not None:
            extra.wait_done()
        else:
            time.sleep(seconds)
        stop.set()
        concurrent.futures.wait(futures)
    return samples, errors, extra


def default_cv_format():
    """PDF CVs are more realistic but need reportlab (pip install reportlab); otherwise use .docx."""
    try:
        import reportlab  # noqa: F401
        return "pdf"
    except ImportError:
        return "docx"


class BulkUpload:
    """Admin bulk upload of dummy candidates, run while the recruiters keep working."""

    def __init__(self, admin_password, title, min_seconds):
        self.admin_password, self.title, self.min_seconds = admin_password, title, min_seconds
        self.accept_seconds = self.total_seconds = None
        self.job = None

    def start(self):
        self.dir = tempfile.mkdtemp(prefix="lt-upload-")
        subprocess.run([sys.executable, os.path.join(ATS_DIR, "tests", "make_dummy_upload.py"), "--rows",
                        str(UPLOAD_ROWS), "--title", self.title, "--out", self.dir,
                        "--format", os.getenv("ATS_LOAD_CV_FORMAT", default_cv_format())], check=True, capture_output=True)
        self.session = requests.Session()
        self.session.post(f"{BASE_URL}/login", data={"username": "admin", "password": self.admin_password},
                          allow_redirects=False, timeout=30)
        files = [("excel_file", ("candidates.csv", open(os.path.join(self.dir, "candidates.csv"), "rb"), "text/csv")),
                 ("jd_files", (f"{self.title}.docx", open(os.path.join(self.dir, f"{self.title}.docx"), "rb")))]
        cv_dir = os.path.join(self.dir, "cvs")
        files += [("cv_files", (n, open(os.path.join(cv_dir, n), "rb"))) for n in sorted(os.listdir(cv_dir))]
        self.t0 = time.perf_counter()
        res = self.session.post(f"{BASE_URL}/api/upload", files=files, timeout=120)
        self.accept_seconds = time.perf_counter() - self.t0
        data = res.json()
        self.job_id = data.get("job_id")
        if not self.job_id:  # older ATS: the upload ran inside the request (before TS-EA-12)
            self.job = {"status": "failed" if data.get("error") else "done", "added": data.get("added"),
                        "failed": data.get("failed", 0)}
        return self

    def wait_done(self):
        while self.job_id:
            self.job = self.session.get(f"{BASE_URL}/api/upload_jobs/{self.job_id}", timeout=30).json()
            if self.job.get("status") in ("done", "failed"):
                break
            time.sleep(1)
        self.total_seconds = time.perf_counter() - self.t0
        remaining = self.min_seconds - self.total_seconds
        if remaining > 0:
            time.sleep(remaining)  # keep phase B long enough to compare with phase A
        shutil.rmtree(self.dir, ignore_errors=True)


def table(a, b):
    lines = ["| Endpoint | Requests A | p50 A | p95 A | Requests B | p50 B | p95 B | p95 B/A | NFR p95 < 1 s |",
             "|---|---|---|---|---|---|---|---|---|"]
    slow = []
    for name in sorted(set(a) | set(b)):
        va, vb = a.get(name, []), b.get(name, [])
        p95a, p95b = pct(va, 95), pct(vb, 95)
        ratio = (p95b / p95a) if p95a else 0
        ok = "yes" if max(p95a, p95b) < 1.0 else "**no**"
        slow.append((max(p95a, p95b), name))
        lines.append(f"| {name} | {len(va)} | {pct(va, 50)*1000:.0f} ms | {p95a*1000:.0f} ms | {len(vb)} | "
                     f"{pct(vb, 50)*1000:.0f} ms | {p95b*1000:.0f} ms | {ratio:.1f}x | {ok} |")
    return "\n".join(lines), sorted(slow, reverse=True)[:3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--admin-password", required=True)
    parser.add_argument("--report")
    args = parser.parse_args()
    print(f"run {RUN}: seeding {SEED} candidates, {USERS} recruiters ({'PostgreSQL' if USE_POSTGRES else 'SQLite'})", flush=True)
    t = time.perf_counter()
    users, upload_title = setup()
    print(f"seeded in {time.perf_counter() - t:.0f}s", flush=True)
    eps = endpoints()
    try:
        print(f"phase A: {USERS} recruiters for {SECONDS:.0f}s", flush=True)
        a, err_a, _ = run_phase(users, eps, SECONDS)
        print(f"phase B: same load + bulk upload of {UPLOAD_ROWS} rows", flush=True)
        b, err_b, upload = run_phase(users, eps, SECONDS,
                                     during=lambda: BulkUpload(args.admin_password, upload_title, SECONDS).start())
    finally:
        removed = cleanup()
    body, top3 = table(a, b)
    job = upload.job or {}
    all_b = [x for v in b.values() for x in v]
    all_a = [x for v in a.values() for x in v]
    ratio_all = pct(all_b, 95) / pct(all_a, 95) if all_a else 0
    report = f"""## Load test run {RUN}

- Users: {USERS} recruiters, think time 0–{THINK_SECONDS*2:.1f} s; phase length {SECONDS:.0f} s; data: {SEED} candidates, {SEED // 6 + 1} requirements
- Database: {'PostgreSQL' if USE_POSTGRES else 'SQLite'}; base URL {BASE_URL}

**Phase A** = recruiters only. **Phase B** = recruiters while a {UPLOAD_ROWS}-row bulk upload runs.

{body}

**Bulk upload:** accepted in {upload.accept_seconds:.2f} s (NFR-ATS-2: < 5 s), job `{job.get('status')}` with {job.get('added')} added, {job.get('failed')} failed; total {upload.total_seconds:.1f} s.

**All requests, p95 during upload vs without:** {ratio_all:.1f}x (NFR-ATS-1: no more than 2x).

**Slowest endpoints (worst p95):** {', '.join(f'{n} ({v*1000:.0f} ms)' for v, n in top3)}

**Errors:** phase A {len(err_a)}, phase B {len(err_b)}{(' — ' + '; '.join(sorted(set(err_a + err_b))[:5])) if (err_a or err_b) else ''}

Cleanup: {removed} test candidates removed.
"""
    print(report)
    if args.report:
        with open(args.report, "w") as f:
            f.write(report)


if __name__ == "__main__":
    main()
