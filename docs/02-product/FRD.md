# Functional Requirements Document (FRD)

Version 0.3 (scope change 2026-11-28: audit, verification, pitches). Requirements trace back to the [PRD](PRD.md) features (F-xx) and forward to the backlog stories (TS-Ex-yy).

## 1. Functional requirements

### FR-AUTH: Identity and access
| ID | Requirement | Feature |
|---|---|---|
| FR-AUTH-1 | Users sign in with email and password. Passwords are hashed with bcrypt (cost ≥ 12). Sessions use short-lived JWTs (15 min) plus a rotating refresh token in an httpOnly cookie. | F-01 |
| FR-AUTH-2 | Roles: `recruiter`, `delivery_lead`, `admin`. Each API route declares the roles allowed to call it. | F-01 |
| FR-AUTH-3 | Recruiters see only the requirements assigned to them. Delivery leads see their clients. Admins see everything. | F-01 |

### FR-REQ: Requirements
| ID | Requirement | Feature |
|---|---|---|
| FR-REQ-1 | Create a requirement with: client, title, JD text, mandatory constraints (budget max, notice max, location, work mode, min experience) and optional preferences. | F-02 |
| FR-REQ-0 | JD text is parsed by the **existing HR Guru JD parser**, wrapped as the `jd.parse` tool (reuse decision in TS-E1-08). If it is unavailable, an LLM extraction fallback is used. | F-02 |
| FR-REQ-2 | The Requirement agent returns a **validated structured output**: must-have skills, nice-to-have skills, seniority, constraints, ambiguities[], clarification questions[]. Output failing schema validation is retried at most 2 times, then marked `needs_human`. | F-02 |
| FR-REQ-3 | The recruiter can answer, edit or dismiss clarification questions. Answers update the requirement version. | F-02 |
| FR-REQ-4 | Requirement status: `draft → analysed → sourcing → shortlist_ready | escalated → approved → closed`. | F-02 |

### FR-CAND: Candidate store and search
| ID | Requirement | Feature |
|---|---|---|
| FR-CAND-0 | Resumes come from the **ATS** and are parsed by the **existing ATS resume parser**, wrapped as `resume.parse`, into structured profile fields and sections before chunking. | F-03 |
| FR-CAND-1 | Candidates hold: profile fields, parsed resume, resume chunks with embeddings, source, consent status, created/updated dates. | F-03 |
| FR-CAND-2 | Hybrid search combines vector similarity and keyword (BM25) scores with reciprocal rank fusion, and supports filters (notice, CTC, location). | F-03 |
| FR-CAND-3 | Protected attributes are never stored in searchable fields or sent to LLMs. | F-03, F-11 |
| FR-CAND-4 | A synthetic data generator produces realistic, fictional profiles: a general set (≥ 2,000) and the **UC-001 scenario set** (500 resumes reproducing the 500 → 80 → 25 → 12 → 2 funnel, plus serving-notice and alternative-title candidates). | F-03 |
| FR-CAND-5 | A funnel tool returns counts per constraint stage (experience, mandatory skills, budget, notice, location) for a search. | F-04 |

### FR-AGT: Agent workflow
| ID | Requirement | Feature |
|---|---|---|
| FR-AGT-1 | Starting a run creates a `run` with a unique id and a thread id for checkpointing. | F-05 |
| FR-AGT-2 | The supervisor produces a plan (ordered steps with the target agent and success criterion) and records it. | F-05 |
| FR-AGT-3 | After each step the supervisor evaluates the observation against the objective (for example "5 qualifying candidates") and either continues, replans, escalates or stops. | F-05 |
| FR-AGT-4 | When the objective is not met, the supervisor identifies the **primary bottleneck** from the funnel and generates alternative strategies (for example serving-notice candidates, alternative job titles, adjacent skill phrasing). | F-05 |
| FR-AGT-4a | Replanning never changes mandatory constraints (budget, mandatory skills, experience, location, notice). A test asserts that the constraints in the run state equal the original requirement after every replan. Only *search strategy* and *optional* preferences may change, and each change is logged with a reason. | F-05 |
| FR-AGT-4b | If the objective is still unmet after the allowed replans (default 3), the run ends `escalated`. The escalation includes the funnel, the strategies tried, the candidates found, and decision options for the recruiter (for example "relax notice to 45 days?"). | F-05 |
| FR-AGT-5 | Hard limits: max 12 supervisor iterations, max 5 tool calls per agent step, wall-clock timeout of 10 min per run, token budget per run (configurable). A breached limit ends the run as `stopped_limit` with a partial result. | F-11 |
| FR-AGT-6 | The Screening agent outputs, for each candidate: a score from 0 to 100, and for each requirement a verdict (`met`, `partially_met`, `not_met`, `unknown`) with evidence quotes (chunk id plus text). | F-06 |
| FR-AGT-7 | The Quality agent checks each evidence quote against the source chunk and flags `unsupported` claims. Unsupported claims cannot reach the recruiter as facts. | F-06 |
| FR-AGT-8 | The workflow pauses at the approval gate (`interrupt`) for shortlists and escalations, and resumes when the recruiter submits decisions. | F-10 |
| FR-AGT-9 | A run interrupted by a crash or rate limit resumes from the last checkpoint. | F-08 |
| FR-AGT-10 | The agent execution dashboard streams step events live: plan, tool call, observation, funnel, replan, escalation, approval needed, done. | F-14 |

### FR-AUD: Submission quality audit (UC-002)
| ID | Requirement | Feature |
|---|---|---|
| FR-AUD-1 | Every new or changed ATS submission (candidate row with `requirement_id`) is audited automatically after connector sync, within 1 hour (KPI-7). Audits are idempotent per submission version. | F-20 |
| FR-AUD-2 | Detail accuracy: entered `experience_years`, `current_company`, `current_role`, `current_location` and `key_skills` are compared with facts extracted from the CV: `consistent`, `mismatch` (with CV quote) or `not_in_cv`. Extraction uses the local model only. | F-20 |
| FR-AUD-3 | Constraint fit: entered expected CTC vs requirement budget, notice vs max notice, location vs requirement location: `within`, `outside`, `unknown`. Deterministic rules, no LLM. | F-20 |
| FR-AUD-4 | Duplicates: exact match on email or phone links submissions; name + company + CV similarity above a threshold raises a possible duplicate for review. | F-20 |
| FR-AUD-5 | Completeness: required fields and the CV file are present (reuses the ATS `missing_info` rules). A missing CV gives status `incomplete` with no LLM call. | F-20 |
| FR-AUD-6 | Quality score 0–100 from weighted checks (default must-have 40, detail accuracy 25, constraint fit 20, duplicates 10, completeness 5; configurable). Every deduction names its check and evidence. | F-20 |
| FR-AUD-7 | Audit records are stored in TalentScout, linked to ATS ids. Nothing is written to the ATS. | F-20, FR-ATS-1 |
| FR-AUD-8 | Lead review queue: submissions with score < threshold (default 60) or any `mismatch`; the lead accepts or overrides each flag with a reason, which is saved as feedback memory. | F-21 |
| FR-AUD-9 | Recruiter scorecard per week and month: submissions, average score, mismatch rate, duplicate rate, confirmed flags. Recruiters see only their own. No automatic action against a recruiter (BR-9). | F-21 |
| FR-AUD-10 | Audit precision and recall per check are measured on a labelled synthetic set in CI. | F-13, F-20 |

### FR-VER: Candidate verification (UC-003)
| ID | Requirement | Feature |
|---|---|---|
| FR-VER-1 | A lead selects a verification batch; the default weekly sample is all audit-flagged submissions plus 20% of the rest per recruiter. Opted-out candidates and closed submissions older than 90 days are excluded. | F-22 |
| FR-VER-2 | Messages are drafted from a versioned template (role, client or industry, location, entered CTC, ECTC and notice) with an opt-out line. Drafts are never sent automatically. | F-22 |
| FR-VER-3 | Sending requires an approval token for the batch from a named lead with step-up re-authentication. `message.send` refuses without it and logs the attempt (KPI-5). | F-22, F-10 |
| FR-VER-4 | Channels: WhatsApp through the ATS relay and email through the ATS sender (ADR-0008). TalentScout holds no channel credentials. | F-22 |
| FR-VER-5 | Replies are captured from the relay's inbound endpoint and the reply mailbox (IMAP) and linked to the message within 10 minutes. Bounces and invalid numbers give `unreachable`. | F-22 |
| FR-VER-6 | Rate limits: default 30 messages per hour and 150 per day per channel; on WhatsApp failure the batch falls back to email and the admin is alerted. | F-22 |
| FR-VER-7 | `STOP` (or equivalent) on any channel opts the candidate out of all channels permanently, with one confirmation message. | F-23 |
| FR-VER-8 | Replies are classified by the local model into: contacted (yes / no / different role), interest (yes / no / maybe), and corrected values. Output is schema-validated; low confidence goes to the lead. | F-22 |
| FR-VER-9 | Outcome per submission: `confirmed`, `details_mismatch` (with differences), `wrong_role`, `not_contacted`, `not_interested`, `no_response`, `unreachable`, `opted_out`. | F-22 |
| FR-VER-10 | Follow-up: no WhatsApp reply in 48 h → one email; no reply after a further 72 h → `no_response`. At most 2 messages per candidate per verification. | F-22 |
| FR-VER-11 | `not_contacted` and `wrong_role` are escalated to the lead with the message, the reply and the recruiter's entry side by side; the lead records a decision and reason (BR-11). | F-22 |
| FR-VER-12 | Classification accuracy is measured on a synthetic reply set (including Hinglish, partial answers and injection attempts) in CI. | F-13, F-22 |

### FR-PIT: Client pitches and drives (UC-004)
| ID | Requirement | Feature |
|---|---|---|
| FR-PIT-1 | A pitch brief holds client or industry, role families and skills, experience bands, locations, count and optional budget band. | F-24 |
| FR-PIT-2 | The Sourcing agent searches the ATS pool (hybrid search, funnel, replanning within the brief's hard limits, escalation). Ranking prefers a recent `confirmed` verification and a clean audit. | F-24, F-04 |
| FR-PIT-3 | Anonymised profile: role, years, key skills with evidence, notice band, CTC band, location; no name, phone, email, current employer or photo (BR-12). | F-24 |
| FR-PIT-4 | Export to PDF or XLSX is an approved, logged action. | F-24 |
| FR-PIT-5 | Drive summary: available counts by skill, experience band, location and notice period. | F-24 |
| FR-PIT-6 | Every export is scanned for identifiers from the source records; any hit blocks the export. | F-24, F-11 |

### FR-MEM: Memory
| ID | Requirement | Feature |
|---|---|---|
| FR-MEM-1 | Short-term memory is the workflow state for a run (LangGraph state plus checkpoints). | F-08 |
| FR-MEM-2 | Long-term memory: approved recruiter feedback ("rejected: no hands-on EKS") is stored with an embedding and tagged by role family. | F-09 |
| FR-MEM-3 | The Sourcing agent retrieves relevant feedback when planning. Retrieved memories are shown in the trace. | F-09 |

### FR-DASH: Agent execution dashboard
| ID | Requirement | Feature |
|---|---|---|
| FR-DASH-1 | List runs with requirement, status, iterations, replans, duration, tokens, model routes and notional cost. | F-14 |
| FR-DASH-2 | Show KPIs over a period: workflow completion, recruiter acceptance, evidence accuracy, escalations, guardrail blocks. | F-14 |
| FR-DASH-3 | Every run links to its full timeline and its trace (KPI-6). | F-14 |

### Future phase (not in MVP)
Marketing or job-offer outreach (verification messages are in scope: FR-VER), the delivery monitoring agent (former FR-DEL), voice screening, and writing results back to the ATS. Naukri has no profile API, so Naukri-sourced candidates arrive through ATS uploads.

### FR-ATS: HR Guru ATS integration
| ID | Requirement | Feature |
|---|---|---|
| FR-ATS-1 | The ATS is the system of record for candidates submitted against requirements, their CVs and the recruiter-entered details. TalentScout never writes to ATS tables in the MVP; it only calls the ATS's messaging channels for approved verification messages (FR-VER-4). | F-00 |
| FR-ATS-2 | The connector reads through a `SELECT`-only PostgreSQL role and syncs changes incrementally (by `updated_at`) into TalentScout's store within 10 minutes. | F-00 |
| FR-ATS-3 | CV files are read from the ATS uploads storage, read-only. A candidate deleted in the ATS is deleted from TalentScout's index at the next sync, including chunks and embeddings. | F-00, NFR-2 |
| FR-ATS-4 | Connector contract tests run in CI against a bootstrapped ATS schema. | F-00 |

### FR-OBS: Audit and observability
| ID | Requirement | Feature |
|---|---|---|
| FR-OBS-1 | Each agent step, tool call, model call (model, tokens, latency, cost), escalation and approval is stored in the `audit_events` collection, which is append-only. A completeness check verifies that every graph step of a run has a matching event (KPI-6). | F-12 |
| FR-OBS-2 | Traces are exported to Langfuse with PII masked. | F-12 |
| FR-OBS-3 | An Admin can view a run timeline and export it as JSON. | F-12 |

## 2. Non-functional requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-1 | Security | OWASP ASVS L1 controls for the web/API. OWASP Top 10 for LLM Applications controls for the agents. |
| NFR-2 | Privacy | DPDP Act 2023: consent captured, purpose limitation, retention (default 12 months, configurable), right to erasure endpoint. |
| NFR-3 | Data locality | Real PII is processed only by local models (BR-4). Cloud LLMs receive only synthetic or masked data. |
| NFR-4 | Reliability | Durable execution; idempotent tool calls (idempotency key); retries with backoff on 429/5xx. |
| NFR-5 | Performance | API p95 < 300 ms (non-AI endpoints). Search p95 < 1 s on 50k profiles. Run p95 ≤ 5 min on the local setup. Verified by performance tests in Sprint 6. |
| NFR-6 | Cost | $0 cash. Per-run token budget. Notional cost shown per run. |
| NFR-7 | Quality | Unit coverage ≥ 70% on business logic. Evaluation suite gates merges to `main` for prompt and agent changes. |
| NFR-8 | Supply chain | Dependencies pinned via lockfiles; Dependabot; SCA (software composition analysis), SAST, secret and container scans in CI. |
| NFR-9 | Accessibility | WCAG 2.1 AA for core screens. |
| NFR-10 | Portability | Whole stack runs with `docker compose up`. Ollama runs natively on macOS for GPU (Metal) acceleration. |
| NFR-ATS-1 | ATS performance | With 25 recruiters active: page and API p95 < 1 s; no request slows others by more than 2× while a bulk upload runs. Measured with the load-test scripts (TS-EA-13) |
| NFR-ATS-2 | ATS bulk upload | Upload of up to 100 rows + CVs is accepted in < 5 s and processed in the background with visible progress (TS-EA-12); a failure in one row never loses the others |
| NFR-ATS-3 | ATS availability | Detect downtime within 10 min (uptime monitor); restore from last night's backup within 1 h (runbook F) |

## 3. Traceability

The backlog (`docs/04-delivery/backlog.md`) maps each story to FR ids. The test strategy maps test suites to FR and NFR ids.
