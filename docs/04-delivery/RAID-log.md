# RAID Log (Risks, Assumptions, Issues, Dependencies)

Owner: Engineering Manager. Reviewed at every sprint planning and retrospective.
Scale: Probability and Impact are rated 1 (low) to 5 (high). Score = P × I.

## Risks

| ID | Risk | P | I | Score | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| R-01 | A free tier is cut or removed (Oracle halved Always Free in June 2026; Gemini reduced free quotas) | 4 | 3 | 12 | Local-first design; LiteLLM multi-provider; everything runs on the Mac via Compose | Architect | Open |
| R-02 | Local 8B model quality too low for screening | 3 | 4 | 12 | Spike TS-E0-06; narrow PII tasks; masked summaries to cloud for reasoning; evaluation gate | Architect | Open |
| R-03 | 16 GB RAM contention (Docker + Mongo + LLM) | 4 | 2 | 8 | One model loaded at a time; Docker memory cap; native Ollama | Tech Lead | Open |
| R-04 | Atlas free 500 MB limit exceeded by embeddings | 3 | 2 | 6 | Pilot subset in Atlas; full set on atlas-local; 384-dim fallback | Architect | Open |
| R-05 | PII leaks to a cloud provider or trace | 2 | 5 | 10 | Router policy + masking + tests (TS-E1-03, TS-E5-02); no real data before DPDP sign-off | Security | Open |
| R-06 | Prompt injection via resumes | 3 | 4 | 12 | Untrusted-content handling, injection corpus evaluation, Quality agent | Security | Open |
| R-07 | Scope creep (too many frameworks, future-phase features pulled in) | 3 | 3 | 9 | One orchestration framework (ADR-0002); MoSCoW in the PRD; PO guards the sprint goal | PO | Open |
| R-08 | Recruiters unavailable for pilot or interviews | 3 | 3 | 9 | Book pilot slots in Sprint 0; async feedback form | PO | Open |
| R-09 | Solo-developer bus factor and fatigue | 3 | 3 | 9 | Docs-as-code, small PRs, sustainable 25 h/week, buffer in Sprint 6 | EM | Open |
| R-11 | The ATS sends real CVs to Gemini for AI screening (`services/gemini_screening.py`). On a free key, inputs may be used by the provider (conflicts with BR-4) | 4 | 4 | 16 | Owner decision: disable, use a paid tier, or route to the local model (TS-EA-07) | PO | Open |
| R-12 | The ATS runs on a single Mac (sleep, reboot, travel, disk failure) after the EC2 teardown | 4 | 4 | 16 | Nightly backups and restore drill (TS-EA-06), Cloudflare Tunnel, keep-awake, health monitor; revisit hosting | Tech Lead | Open |
| R-13 | ATS data entered after 26 May 2026, and all CV/JD files, were lost with the EC2 host | 4 | 4 | 16 | ats.db restored (9,988 candidates, 1,685 requirements, newest 2026-05-26). No ATS zip backups in Google Drive. Last chance: AWS EBS volumes/snapshots/AMIs/AWS Backup; otherwise recruiters re-upload active CVs (TS-EA-10) | PO | Open |
| R-14 | The public `a54000/hireflow` repo history contains real candidate PII (`tools/case_001`) | 5 | 4 | 20 | Make the repo private now; not copied into this repo (ADR-0006) | PO | Open |
| R-15 | Legacy ATS code has security weaknesses (error text returned to clients, debug prints, send-email endpoints) | 3 | 4 | 12 | Hardening baseline TS-EA-07; dependency CVEs already patched | Security | Open |
| R-16 | ATS requests block each other: bulk upload parses every CV inside one request (~0.7–1 s per CV) and one Python process runs one CPU task at a time; PostgreSQL had no query indexes after migration | 4 | 3 | 12 | Done: 24 indexes created in PostgreSQL (12–26× faster lookups), 3 worker processes (healthz under load 129 → 24 ms). Next: background bulk upload (TS-EA-12), load-test baseline (TS-EA-13) | Tech Lead | Mitigating |
| R-10 | Bias in recommendations | 2 | 5 | 10 | Protected attributes masked; name-swap fairness evaluation; human decides | PO | Open |

## Assumptions (validate by Sprint 2 planning)

| ID | Assumption | Validation |
|---|---|---|
| A-01 | 25 recruiters in the MVP rollout (confirmed) | — |
| A-02 | Planning figure: ~200 open requirements per month across multiple enterprise clients | ATS export |
| A-03 | The ATS is the only candidate source (confirmed); about 3,600 candidates at last count; Naukri has no API | Count after data recovery (TS-EA-04) |
| A-04 | Existing JD and resume parsers are reusable as tools without modifying the existing platform | Code review (TS-E1-08) |
| A-05 | Business problems BP-1…BP-8 are the main pains (confirmed in brief); relative priority TBC | Recruiter interviews |
| A-06 | KPIs tracked: time to first submission, submission-to-interview, SLA breaches | Delivery Lead |
| A-07 | ~25 focused hours per week available for development | Sprint 0 actuals |

## Issues

| ID | Issue | Raised | Action | Status |
|---|---|---|---|---|
| I-03 | The live ATS is down (EC2 torn down) | 2026-11-27 | Restore locally (TS-EA-01…06) | In progress |
| I-01 | Jira project must be created manually (the tooling cannot create projects) | 2026-11-27 | Owner created project TS; 8 epics, 60 stories and 8 sprints imported | Closed |
| I-02 | Discovery questions partly answered by the business brief (team size, problems, scope, KPIs, UC-001) | 2026-11-27 | Volumes, DB size and baselines still open (A-01…A-03, TS-E0-08) | Open |

## Dependencies

| ID | Dependency | Needed by | Status |
|---|---|---|---|
| D-01 | Decision: $0 cash budget | Sprint 0 | Closed (decided) |
| D-02 | Decision: deploy locally first, OCI optional | Sprint 0 | Closed (decided) |
| D-03 | Free accounts: MongoDB Atlas, Langfuse, Google AI Studio and/or Groq | Sprint 1 | Open |
| D-04 | Access to existing resume and JD parsers | Sprint 2 | Open |
| D-05 | DPDP sign-off for real-data pilot | Sprint 6 | Open |
| D-06 | 2–3 recruiters for pilot | Sprint 6 | Open |
