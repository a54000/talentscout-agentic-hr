# How We Build TalentScout

A guide to how TalentScout is being built for HR Guru: how it was designed, built, tested and deployed, and the main problems we hit along the way. It is written for anyone who joins the project, reviews it, or wants to repeat the approach. Status as of **2026-11-28**: Sprint 0 is complete, and Sprint 1 (ATS stabilisation) is under way.

Contents:
1. [What we are building](#1-what-we-are-building)
2. [How we work](#2-how-we-work)
3. [Design](#3-design)
4. [Build](#4-build)
5. [Testing](#5-testing)
6. [Deployment](#6-deployment)
7. [Main issues faced and how we solved them](#7-main-issues-faced-and-how-we-solved-them)
8. [Where we are and what is next](#8-where-we-are-and-what-is-next)
9. [Lessons learned](#9-lessons-learned)

---

## 1. What we are building

**HR Guru ATS** is the live applicant tracking system that HR Guru's recruiters use every day (25 recruiters in the MVP). Sourcers find candidates, mostly on Naukri, screen them, and upload them into the ATS against a client requirement. The ATS is the **system of record**: candidates, CVs, the details recruiters enter, and requirements.

**TalentScout** is a team of supervised AI agents that acts as the **quality and trust layer over the ATS**. In priority order:

| # | Use case | What it does |
|---|---|---|
| 1 | [UC-002 Submission quality audit](../00-discovery/UC-002-submission-quality-audit.md) | Checks every submission against the requirement and the candidate's own CV: must-have skills with evidence, recruiter-entered details vs the CV, budget and notice fit, duplicates, completeness. Produces a score, a lead review queue and recruiter scorecards |
| 2 | [UC-003 Candidate verification](../00-discovery/UC-003-candidate-verification.md) | Asks the candidate on WhatsApp and email, after a lead approves the message: were you contacted for this role, are you interested, are these details right? Flags possible false submissions |
| 3 | [UC-004 Client pitches and drives](../00-discovery/UC-004-client-pitches-and-drives.md) | Reuses the audited, verified pool for anonymised client pitch packs and hiring-drive summaries |

Ground rules that shaped every decision:
- **People decide.** Agents recommend. They never reject candidates, never act against recruiters automatically, and never contact anyone without an approval.
- **Real candidate data stays on HR Guru hardware.** It is processed only by local models, never sent to free cloud AI services, and never put in git, logs or test data.
- **$0 cash budget.** Free tiers and owned hardware only (a MacBook M2, 16 GB).

## 2. How we work

**Lifecycle with gates.** The project follows six phases, and each ends with a gate ([ways of working](../04-delivery/ways-of-working.md)):

```
Discovery → Solution & architecture → Engineering planning → Incremental build → AI governance → Deployment & pilot
 (BRD/PRD)     (HLD, ADRs, threat model)  (backlog, sprints)    (2-week sprints)     (guardrails, evals)   (pilot report)
```

**One developer, several hats.** The same person acts as Product Owner, Engineering Manager, Architect, Tech Lead, Developer and QA, using AI coding assistants (Claude Code, Codex). Each hat has written responsibilities, so it's always clear which decision was made in which role.

**Scrum, with written rules:**
- **Definition of Ready:** a user story, Given/When/Then acceptance criteria including a failure case, an estimate, and the privacy impact noted.
- **Definition of Done:** merged through a PR with CI green, tests for the new logic, no new high or critical vulnerabilities, no secrets or real personal data, docs updated, and the acceptance criteria demonstrated. For changes to the live ATS, the PO also confirms it works on the live system.

**One backlog source of truth.** Stories live in [`backlog.json`](../04-delivery/backlog.json). A script (`scripts/backlog_to_md.py`) generates the backlog, the sprint plan and the [task checklist](../04-delivery/task-checklist.md), and CI fails if they drift apart. Every story also exists in Jira (project `TS`) with the same ID, points and sprint.

**Change control.** Work happens on short-lived branches (`feat/…`, `fix/…`, `docs/…`), which reach `main` only through a PR with green checks. Merges happen only with the PO's explicit OK. Commit messages carry the story ID, for example `fix(ats): TS-EA-07 …`.

## 3. Design

### 3.1 From requirements to scope
1. **Discovery:** [requirements gathering](../00-discovery/requirements-gathering.md), the AS-IS recruiter workflow, business problems and a [baseline measurement plan](../00-discovery/baseline-measurement-plan.md).
2. **[BRD](../01-business/BRD.md):** business problems, KPIs (KPI-1…11) and business rules (BR-1…12), for example "only a human can reject a candidate" and "opt-outs apply to every channel".
3. **[PRD](../02-product/PRD.md) and [FRD](../02-product/FRD.md):** the agents, features F-00…F-24, user journeys, and testable functional and non-functional requirements, such as "ATS pages p95 < 1 s" and "bulk upload accepted in < 5 s".
4. **[Technical scope and budget](../01-business/technical-scope-and-budget.md):** 84 stories, 311 points, 11 two-week sprints ending 2027-05-07, $0 cash, with notional cloud costs tracked.

### 3.2 Architecture
See the [HLD](../03-architecture/HLD.md) and [LLD](../03-architecture/LLD.md). Three tiers around the ATS:

```
Recruiters ──► HR Guru ATS (Flask + PostgreSQL)  ◄── system of record
                    │ read-only connector (SELECT-only role)
                    ▼
TalentScout:  React web ──► Express API ──► Agent service (Python, LangGraph)
                                                 │  tools only via the MCP server
                                                 ▼
                                   MongoDB (data + vector search) · Redis · Langfuse
                                   Models: local Ollama for real data; free cloud tiers only for synthetic data
```

Key decisions are recorded as ADRs (architecture decision records):

| ADR | Decision |
|---|---|
| [0001](../03-architecture/adr/0001-hybrid-mern-plus-python-agents.md) | MERN for the product; Python for the agents, which have the strongest agent ecosystem |
| [0002](../03-architecture/adr/0002-langgraph-orchestration.md) | LangGraph for orchestration: checkpoints, human-in-the-loop interrupts, replanning |
| [0003](../03-architecture/adr/0003-mongodb-atlas-vector-search.md) | MongoDB Atlas for documents and vector and text search together |
| [0004](../03-architecture/adr/0004-zero-cost-model-routing.md) | Zero-cost model routing; requests carrying personal data go only to the local model |
| [0005](../03-architecture/adr/0005-public-repo-synthetic-data.md) | Public repository (free CI and CodeQL), so synthetic data only |
| [0006](../03-architecture/adr/0006-monorepo-with-hr-guru-ats.md) | The ATS lives in the same repository, imported without its git history |
| [0007](../03-architecture/adr/0007-ats-as-system-of-record.md) | The ATS is the system of record; TalentScout reads it, never writes |
| [0008](../03-architecture/adr/0008-candidate-verification-outreach.md) | Verification messages go only through the ATS's own channels, each batch approved by a lead |

### 3.3 Security and privacy by design
- **[Threat model](../03-architecture/threat-model.md):** STRIDE plus the OWASP Top 10 for LLM applications, covering for example prompt injection inside CVs and candidate replies, spoofed replies, and identity leaks in pitch packs.
- **Data rules:** synthetic data in the repository; protected attributes are never used in screening; replies and CVs are classified locally; there's a retention and erasure path (DPDP Act 2023).
- **[RAID log](../04-delivery/RAID-log.md):** risks are tracked with owners, from "the live ATS has no backups" to "the unofficial WhatsApp library can get the number restricted".

## 4. Build

### 4.1 Repository layout (monorepo)
```
apps/web          React + Vite front end
apps/api          Express API / BFF
apps/ats          HR Guru ATS (Flask), plus its tests, scripts and the upload worker
services/agents   FastAPI + LangGraph agent service
ops/backup        nightly backup, restore drill, launchd schedule
docs/             everything in this guide, version-controlled with the code
.github/          CI, security and CD workflows, Dependabot
```

### 4.2 Sprint 0: walking skeleton (PR #1)
Before any feature work: the inception documents, a minimal web app, API and agent service, Dockerfiles, Docker Compose, and the three pipelines (CI, security, CD). Every later story is therefore built, tested and scanned from its first commit.

### 4.3 Bringing the live ATS back (PR #2, epic TS-EA)
The live ATS had been hosted on AWS EC2, and that host was torn down, so recruiters had no system. We:
1. **Imported** the latest ATS code (the `hireflow` repository) into `apps/ats`. We took **no git history** and left out a folder containing real candidate data.
2. **Made it run on macOS and Linux:** replaced a Windows-only file lock, added a Dockerfile, a PostgreSQL service and an empty-schema bootstrap.
3. **Upgraded dependencies:** 61 known vulnerabilities, 7 of them critical, went to 0.
4. **Restored the data** from the last SQLite copy into PostgreSQL with a script that refuses to touch a non-empty database: 9,988 candidates and 1,685 requirements.
5. **Published it** at `https://ats.hrgp.in` through a Cloudflare Tunnel, with no public IP or open ports.
6. **Protected it:** nightly backups to the Mac and Google Drive with a restore drill, and an uptime monitor with alerts.
7. **Sped it up:** 24 database indexes (12–26× faster lookups) and 3 web processes instead of 1.

### 4.4 Hardening the ATS (Sprint 1, PRs #13–#15)
- **Security alerts in the imported code:** 59 → 2, and the 2 left are false positives. SQL column names now come only from fixed lists, file paths can't escape the uploads folder, slow regular expressions were rewritten, and users no longer see internal error details (they get a reference number that links to the log).
- **AI screening removed from the ATS.** It sent real CVs to free cloud AI services. A switch now blocks cloud AI for candidate data, and screening will move to TalentScout's audit agent, on the local model.

### 4.5 Background bulk upload (Sprint 1, PR #17)
Bulk upload used to parse every CV inside one web request, about 1 s per CV, and blocked other recruiters while it ran. Now:
- the request saves the files and returns a **job id in well under a second**;
- a separate **`ats-worker`** process does the work, and the page shows live progress;
- each candidate row and the job's progress are saved **in one transaction**, so a crashed worker resumes where it stopped **without duplicates**;
- one bad row is reported on its own and no longer stops the rest.

## 5. Testing

| Layer | What | Where it runs |
|---|---|---|
| Unit tests | Web and API (Vitest), agents (pytest), ATS security helpers and the cloud-AI switch (22 tests) | Every PR |
| ATS smoke test | Starts the real ATS and checks health, admin login, main pages and APIs, that retired routes return 410, and a **2-row bulk upload end to end** | SQLite, PostgreSQL, PostgreSQL with gunicorn × 3 |
| Crash test | Kills a bulk-upload job after row 1, resumes it, and checks both rows are saved exactly once | PostgreSQL with the external worker, every PR |
| Security | CodeQL (security-extended), Semgrep, gitleaks, npm audit, pip-audit, Trivy (files and images) | Every PR; images also on merge |
| Live checks | After each ATS change, the PO checks the main flows on the live system: edit a candidate, upload a CV and a JD, send an email, run a bulk upload | Mac, before a story is closed |
| Load-style test | 400 dummy rows with a forced worker kill at row 203: resumed, 400 rows, no duplicates; the candidate list stayed at a median 13 ms | Run ad hoc; `tests/make_dummy_upload.py` makes the dummy data |
| Planned | Agent evaluations (golden JDs, audit precision, reply classification, prompt injection) as a CI gate; ATS load test against the NFR targets | Sprints 1–9 |

Rules: tests use **synthetic data only**; a failing check is fixed at its root cause, never skipped; and a story isn't Done until its failure case is tested.

## 6. Deployment

```
branch ──► PR ──► CI + security + image checks ──► PO approves ──► merge to main
                                                                      │
                     ┌────────────────────────────────────────────────┤
                     ▼                                                ▼
     CD: build 4 images → Trivy gate (critical = stop)     Live ATS on the Mac (manual):
         → SBOM → push to GHCR (tag = commit)                git pull
         → demo deploy (skipped: no demo host yet)           docker compose up -d --build ats ats-worker
                                                             → PO checks the main flows
```

**Live runtime:** `ats` (3 web processes), `ats-worker` (bulk uploads) and `ats-db` (PostgreSQL, no open port) run in Docker on the Mac. Recruiters reach them at `https://ats.hrgp.in` through Cloudflare Tunnel. Backups run every night at 21:00, and UptimeRobot alerts on downtime. Day-to-day steps are in the [restore runbook](../runbooks/ats-local-restore.md).

**Known gaps (planned):**
- The Mac rebuilds images from source instead of pulling the scanned images from GHCR.
- Deploying is manual and has no automatic backup or rollback step.
- There's no staging copy; the smoke test on a copy of the schema is the safety net for now.

## 7. Main issues faced and how we solved them

| # | Issue | Impact | What we did |
|---|---|---|---|
| 1 | **Live ATS host torn down.** The EC2 server was deleted | Recruiters had no ATS; data after 2026-05-26 and all CV/JD files were not recoverable | Restored from the last SQLite copy into PostgreSQL on the Mac, published it through Cloudflare Tunnel, and added nightly off-machine backups, a restore drill and uptime alerts so this can't happen silently again. The missing period is tracked as a risk |
| 2 | **The code only ran on Windows.** A Windows-only file lock broke startup on macOS and Linux | The ATS couldn't start | Replaced it with a cross-platform lock and added a smoke test on Linux in CI |
| 3 | **No PostgreSQL schema** ("relation candidates does not exist") | Migration to PostgreSQL failed | Wrote a bootstrap that builds the schema the ATS expects, refuses a non-empty database, and is tested in CI |
| 4 | **61 vulnerable dependencies (7 critical)**, including a login library signature bypass | Real security exposure on a live system with personal data | Upgraded 12 packages to 0 known vulnerabilities; Dependabot now watches them with a 7-day cooldown |
| 5 | **Candidate data in a public repository's history** (the old `hireflow` repo) | Personal data exposure | Made the repo private, imported the code without history, and listed the other old public ATS repos for review |
| 6 | **Port clashes on the Mac** (5432, 5433 already in use) | Database container wouldn't start | Removed the host port completely; restores run inside the container, which also reduces exposure |
| 7 | **Tunnel token problems**, including a token pasted into chat | Tunnel down; a leaked credential | Fixed the token format and rotated the exposed token. Rule: secrets only in git-ignored `.env` files |
| 8 | **macOS privacy blocked the scheduled backup** writing to Google Drive | Silent backup failures | Granted Full Disk Access to the shell that runs it, and the script now reports this cause clearly and sends a macOS notification on failure |
| 9 | **The ATS froze during bulk uploads.** Everything ran in one request, there were no database indexes, and there was one process | Recruiters blocked each other | Indexes (12–26× faster), 3 processes, then background uploads with a separate worker |
| 10 | **Startup race:** 3 web processes created the indexes at the same time | Some indexes missing (logs showed 7/24, 9/24…) | A database advisory lock makes one process build them and the others wait |
| 11 | **The first CD runs failed:** the web image's nginx base had 5 critical vulnerabilities | Images couldn't be published | `apk upgrade` fixed only part of it, so we switched to Alpine's patched nginx. The image scan now also runs **on PRs**, so this is caught before merge |
| 12 | **74 security alerts in the imported ATS code, 2 critical** (server-side request forgery in the Google Sheet import) | Risk on the live system | Fixed the 2 critical ones first and merged, then cut the rest from 59 to 2 false positives (see 4.4) |
| 13 | **Real CVs were going to free cloud AI**: Gemini, OpenRouter and OpenAI for screening, and HuggingFace for CV parsing (found while testing bulk upload) | Breaks the rule that personal data stays local; free tiers may use the data | One switch, off by default, blocks every path. The PO then removed AI screening from the ATS altogether |
| 14 | **Scope misunderstanding:** we first designed TalentScout to source and screen from scratch | Wrong priorities | The PO clarified that sourcers already screen before uploading. We re-planned around audit → verification → pitches, with 3 new use cases, ADR-0008 and 18 new stories (+2 sprints) |
| 15 | **Restart could duplicate candidates** in the new background upload | Duplicate rows after a crash | Progress is saved in the same transaction as each row; tested by killing the worker mid-job (CI, and 400 rows by hand) |

## 8. Where we are and what is next

**Done:**
- Sprint 0: documents, backlog and Jira, CI/CD and security scanning, and the ATS restored and live with backups and monitoring.
- From Sprint 1: ATS security hardening, AI screening removed, background bulk upload (waiting for the PO's live check).

**Next:**
- **Sprint 1:** ATS performance baseline and load test (TS-EA-13), scheduled reports (TS-EA-14), deleting the retired AI code (TS-EA-15), local model choice and the recruiter time baseline.
- **Sprints 2–10:** read-only ATS connector and the Requirement agent → **submission audit (UC-002)** → verification (UC-003) → pitches (UC-004) → dashboard, performance and pilot (ending 2027-05-07).

The live view of every task is the [task checklist](../04-delivery/task-checklist.md) and the [sprint plan](../04-delivery/sprint-plan.md).

## 9. Lessons learned

1. **Restore and protect the live system first.** Features are worthless if recruiters have no ATS or no backups.
2. **Ask "who already does this?" before designing agents.** Learning that sourcers already screen changed the product from a sourcing tool into an audit and trust layer.
3. **Make privacy rules executable.** "No real CVs to cloud AI" was in the BRD from day one, but only a code switch with tests caught every path, including one nobody knew about.
4. **Move checks earlier.** Image scans that only ran after a merge let a bad image reach `main`; now they run on every PR.
5. **Test the failure, not just the happy path.** Killing the worker mid-upload is what proved "no duplicates", not the normal runs.
6. **Small PRs, explicit approvals, one source of truth for the backlog.** They keep a fast-moving project traceable from requirement to commit to Jira.
