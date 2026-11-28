"""End-to-end check of background bulk upload (TS-EA-12). Run by smoke_test.sh from the app copy.

Usage: python tests/bulk_upload_check.py <base_url> <admin_password> [--resume]

Default: uploads 2 synthetic candidates, checks the request returns a job in under 5 s,
waits for the job and checks both rows are saved.

--resume (PostgreSQL, server started with ATS_UPLOAD_WORKER=external): queues a job, runs it
in this process and kills it after the first row, then resumes it and checks that both
rows are saved exactly once.
"""
import csv
import io
import os
import secrets
import sqlite3
import sys
import time
import zipfile

import requests

BASE, PASSWORD = sys.argv[1], sys.argv[2]
RESUME = "--resume" in sys.argv
DATABASE_URL = os.getenv("DATABASE_URL", "")
TAG = secrets.token_hex(3)
TITLE = f"Smoke Cloud Architect {TAG}"


def db():
    if DATABASE_URL:
        import psycopg2
        return psycopg2.connect(DATABASE_URL)
    return sqlite3.connect("ats.db")


def sql(conn, query):
    return query if not DATABASE_URL else query.replace("?", "%s")


def insert_requirement():
    conn = db()
    cur = conn.cursor()
    cur.execute(sql(conn, "INSERT INTO requirements (title, client_name, description, status) VALUES (?,?,?,?)"),
                (TITLE, "Smoke Client", "Synthetic JD for the smoke test.", "Open"))
    conn.commit()
    conn.close()


def docx_bytes(text):
    """A minimal .docx the ATS parser can read (synthetic data only)."""
    paragraphs = "".join(f"<w:p><w:r><w:t>{line}</w:t></w:r></w:p>" for line in text.splitlines())
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                f"<w:body>{paragraphs}</w:body></w:document>")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        z.writestr("word/document.xml", document)
    return buf.getvalue()


def candidates(n):
    people = []
    for i in range(n):
        phone = f"9{secrets.randbelow(10**9):09d}"
        people.append({"name": f"Test Person{i} {TAG}", "email": f"smoke.{TAG}.{i}@example.com", "phone": phone})
    return people


def upload(session, people):
    header = ["Candidate Name", "Email", "Phone", "Current Company", "Current Role", "Experience (Years)", "Key Skills",
              "Notice Period", "Current Salary", "Expected Salary", "Current Location", "Preferred Location", "Requirement"]
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(header)
    for p in people:
        writer.writerow([p["name"], p["email"], p["phone"], "Example Corp", "Cloud Architect", "14", "AWS, Terraform",
                         "30 days", "40", "45", "Gurgaon", "Gurgaon", TITLE])
    files = [("excel_file", ("candidates.csv", out.getvalue().encode(), "text/csv"))]
    for p in people:
        cv = f"{p['name']}\nEmail: {p['email']}\nPhone: {p['phone']}\nCloud Architect with AWS and Terraform."
        files.append(("cv_files", (f"{p['name'].replace(' ', '_')}.docx", docx_bytes(cv),
                                   "application/vnd.openxmlformats-officedocument.wordprocessingml.document")))
    files.append(("jd_files", (f"{TITLE}.txt", b"Synthetic JD: AWS, Terraform.", "text/plain")))
    started = time.time()
    res = session.post(f"{BASE}/api/upload", files=files, timeout=30)
    elapsed = time.time() - started
    assert res.status_code == 202, f"upload returned {res.status_code}: {res.text[:300]}"
    assert elapsed < 5, f"upload took {elapsed:.1f}s, expected < 5s"
    return res.json()["job_id"]


def wait(session, job_id, timeout=120):
    deadline = time.time() + timeout
    while time.time() < deadline:
        job = session.get(f"{BASE}/api/upload_jobs/{job_id}", timeout=10).json()
        if job.get("status") in ("done", "failed"):
            return job
        time.sleep(1)
    raise AssertionError(f"job {job_id} did not finish in {timeout}s: {job}")


def saved_count(people):
    conn = db()
    cur = conn.cursor()
    emails = [p["email"] for p in people]
    marks = ",".join("?" for _ in emails)
    cur.execute(sql(conn, f"SELECT COUNT(*) FROM candidates WHERE email_addr IN ({marks})"), emails)
    count = cur.fetchone()[0]
    conn.close()
    return count


def main():
    session = requests.Session()
    res = session.post(f"{BASE}/login", data={"username": "admin", "password": PASSWORD}, allow_redirects=False, timeout=10)
    assert res.status_code == 302, f"login returned {res.status_code}"
    insert_requirement()
    people = candidates(2)
    job_id = upload(session, people)

    if not RESUME:
        job = wait(session, job_id)
        result = job.get("result") or {}
        assert job["status"] == "done", f"job failed: {job}"
        assert result.get("added") == 2 and job["rows_done"] == 2, f"unexpected result: {job}"
        assert saved_count(people) == 2, "candidates not saved"
        print("bulk upload check passed (background job)")
        return

    # Resume: run the job here and stop it after the first saved row, as if the worker died.
    os.environ["ATS_PROCESS_ROLE"] = "worker"
    sys.path.insert(0, os.getcwd())
    import app as ats

    real_save = ats._save_bulk_row
    calls = {"n": 0}

    def dying_save(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 2:
            raise SystemExit("simulated worker crash")
        return real_save(*args, **kwargs)

    ats._save_bulk_row = dying_save
    try:
        ats.run_upload_job(job_id)
        raise AssertionError("the simulated crash did not happen")
    except SystemExit:
        pass
    ats._save_bulk_row = real_save
    job = ats.get_upload_job(job_id)
    assert job["status"] == "running" and job["rows_done"] == 1, f"unexpected state after crash: {job}"
    assert saved_count(people) == 1

    ats.update_upload_job(job_id, updated_at="2000-01-01T00:00:00")  # make it look stale
    ats.UPLOAD_JOB_STALE_SECONDS = 1
    queued = ats.recover_upload_jobs()
    assert job_id in queued, f"job was not requeued: {queued}"
    ats.run_upload_job(job_id)
    job = ats.get_upload_job(job_id)
    assert job["status"] == "done" and job["rows_done"] == 2 and job["added"] == 2, f"resume failed: {job}"
    assert saved_count(people) == 2, f"expected 2 saved rows, got {saved_count(people)} (duplicates?)"
    print("bulk upload check passed (resume after a crash, no duplicate rows)")


if __name__ == "__main__":
    main()
