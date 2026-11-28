# ATS Performance Baseline (TS-EA-13)

Measured 2026-11-28 against **NFR-ATS-1** (25 recruiters active: page and API p95 < 1 s; no request more than 2× slower while a bulk upload runs) and **NFR-ATS-2** (a bulk upload of up to 100 rows accepted in < 5 s).

## Result in one line

All targets are met. Worst p95 is **92 ms**, against a 1 s target. During a 100-CV upload, requests are no slower (**1.0×** p95). A bulk upload is accepted in **0.03 s**, where before TS-EA-12 it took **32 s**.

## Method

- **Script:** [`apps/ats/scripts/load_test_recruiters.py`](../../apps/ats/scripts/load_test_recruiters.py). It creates 25 recruiter logins, seeds synthetic data and deletes it all afterwards.
- **Setup:** the same as live. PostgreSQL 16, the web app on gunicorn with 3 processes × 6 threads, and the separate `ats-worker` for uploads.
- **Data:** 10,000 synthetic candidates and 1,667 requirements, close to live (9,988 and 1,685). Each recruiter owns about 400 candidates.
- **Traffic:** each of the 25 recruiters repeatedly opens one of 8 common screens or APIs at random, with 0–1 s between clicks:
  - the app page;
  - `/api/me`;
  - the candidate list;
  - candidate search;
  - one of their own candidates;
  - the requirements list;
  - the team list;
  - stats.
- **Phases (60 s each):**
  - A: recruiters only;
  - B: recruiters while the admin bulk-uploads 100 dummy candidates with 3-page PDF CVs.

## Results (after TS-EA-12)

| Endpoint | p50 A | p95 A | p50 B | p95 B | p95 B/A |
|---|---|---|---|---|---|
| `GET /app` | 5 ms | 18 ms | 5 ms | 19 ms | 1.1× |
| `GET /api/me` | 8 ms | 22 ms | 8 ms | 30 ms | 1.4× |
| `GET /api/candidates` (list) | 16 ms | 35 ms | 15 ms | 42 ms | 1.2× |
| `GET /api/candidates` (search) | 16 ms | 32 ms | 16 ms | 33 ms | 1.0× |
| `GET /api/candidate/<id>` | 11 ms | 27 ms | 11 ms | 33 ms | 1.2× |
| `GET /api/requirements` | 60 ms | 89 ms | 61 ms | 92 ms | 1.0× |
| `GET /api/team` | 8 ms | 23 ms | 8 ms | 28 ms | 1.2× |
| `GET /api/stats` | 18 ms | 33 ms | 18 ms | 39 ms | 1.2× |

About 350 requests per endpoint per phase (around 2,900 per phase), with 0 errors.

| Bulk upload (100 rows, PDF CVs) | Before TS-EA-12 (commit 5b47753) | After TS-EA-12 | Target |
|---|---|---|---|
| Upload accepted | **32.3 s**, the browser waits for everything | **0.03 s**, then a progress view | < 5 s |
| Processing time | (inside the request) | 8.1 s, in `ats-worker` | — |
| Other recruiters' p95 during the upload | 1.0× | 1.0× | ≤ 2× |
| Rows saved | 100 | 100, 0 failed | — |

The candidate and other pages already held up during uploads before TS-EA-12, because of the 3 web processes and the indexes added in Sprint 0. TS-EA-12 fixed the uploader's own 32 s wait and moved the CPU work out of the web processes.

## Top 3 slowest endpoints

1. **`GET /api/requirements`** (p95 92 ms). It returns all 1,667 requirements on every call, so it will grow with the requirement count. Suggested fix, when needed: paging or a search parameter.
2. **`GET /api/candidates`, list** (p95 42 ms).
3. **`GET /api/stats`** (p95 39 ms).

None of them is near the target, so no change is needed now.

## Limits of this measurement

- It was run in a 4-CPU Linux container, not on the M2 Mac, so the absolute numbers will differ. The relative findings (no slowdown during uploads, accepted within the target) should hold.
- The dummy PDF CVs are lighter than many real CVs; real uploads will take longer to *process*, but they no longer affect the web processes or the time to accept.
- Only reads were measured, plus one bulk upload. Recruiter edits, reports and email sends weren't part of the mix.
- **Re-run it on a copy of live data before the pilot.** That needs the staging copy (TS-EA-18). Never run the script against the live ATS: it creates test users and candidates.

## How to re-run

```bash
DATABASE_URL=postgresql://... ATS_BASE_URL=http://127.0.0.1:5001 ATS_LOAD_USERS=25 ATS_LOAD_SECONDS=60 ATS_LOAD_SEED=10000 \
python apps/ats/scripts/load_test_recruiters.py --admin-password '<admin password>' --report results.md
```
