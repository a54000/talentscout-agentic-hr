# Product Backlog

_Generated from `backlog.json` by `scripts/backlog_to_md.py`. Edit the JSON, not this file._

| Epic | Name | Stories | Points |
|---|---|---|---|
| E0 | Inception and platform | 9 | 24 |
| EA | HR Guru ATS restore and integration | 10 | 30 |
| E1 | Requirement agent | 8 | 28 |
| E2 | Intelligent retrieval | 7 | 29 |
| E3 | Multi-agent orchestration | 6 | 32 |
| E4 | MCP and memory | 5 | 21 |
| E5 | Responsible AI and LLMOps | 9 | 31 |
| E6 | Interoperability, delivery and pilot | 7 | 27 |
| **Total** | | **61** | **222** |

## E0: Inception and platform

Documents, repo, CI/CD, security scanning, local stack, free-tier accounts.

### TS-E0-01: Monorepo structure and tooling  (2 pts, Sprint 0, Done, Jira TS-18)

*As a developer I want a monorepo with web, api and agents projects so that all tiers build and test the same way.*

Traces to: NFR-10

Acceptance criteria:
- Given a fresh clone, when I run the documented setup, then web, api and agents install and their tests pass
- Given an unformatted file, when lint runs, then it fails with a clear message

### TS-E0-02: CI pipeline: lint, test, build  (3 pts, Sprint 0, In progress, Jira TS-19)

*As a tech lead I want every PR linted, tested and built so that broken code never reaches main.*

Traces to: NFR-7

Acceptance criteria:
- Given a PR, when CI runs, then Node and Python lint, unit tests and builds run and report status
- Given a failing test, when CI runs, then the PR check is red and merge is blocked

### TS-E0-03: Security scanning pipeline  (3 pts, Sprint 0, In progress, Jira TS-20)

*As a security owner I want SAST, SCA, secret and container scans on every PR so that vulnerabilities are caught early.*

Traces to: NFR-1, NFR-8

Acceptance criteria:
- Given a PR, when security CI runs, then CodeQL, Semgrep, gitleaks, npm audit, pip-audit and Trivy run
- Given a committed fake secret, when gitleaks runs, then the job fails
- Given a high-severity dependency vulnerability, when audit runs, then the job fails

### TS-E0-04: CD pipeline to GHCR and demo host  (3 pts, Sprint 0, In progress, Jira TS-21)

*As a tech lead I want images built, scanned and published on merge so that every main commit is deployable.*

Traces to: NFR-8

Acceptance criteria:
- Given a merge to main, when CD runs, then images for web, api and agents are pushed to GHCR tagged with the commit SHA
- Given a critical vulnerability in an image, when Trivy scans it, then the image is not pushed
- Given demo secrets are absent, when CD runs, then deploy is skipped with a notice instead of failing

### TS-E0-05: Docker Compose local stack  (2 pts, Sprint 0, In progress, Jira TS-22)

*As a developer I want one command to start the stack so that I can work offline on my Mac.*

Traces to: NFR-10

Acceptance criteria:
- Given Docker is running, when I run docker compose up, then web, api, agents, mongo and redis start and health checks pass
- Given Ollama runs natively, when the agents service starts, then it reaches Ollama via host.docker.internal

### TS-E0-06: Spike: local model selection on M2 16 GB  (3 pts, Sprint 1, To do, Jira TS-23)

*As an architect I want to measure candidate local models so that the PII-safe route is good enough and fast enough.*

Traces to: NFR-3

Acceptance criteria:
- Given 3 candidate 8B-class models, when each analyses 5 sample JDs, then quality notes, tokens/sec and RAM use are recorded
- Given the results, when the spike ends, then ADR-0004 records the chosen model

### TS-E0-07: Free-tier accounts and secrets handling  (2 pts, Sprint 0, To do, Jira TS-24)

*As a developer I want free-tier accounts set up and secrets kept out of git so that we spend $0 and leak nothing.*

Traces to: NFR-6

Acceptance criteria:
- Given the setup guide, when followed, then Atlas, Langfuse and one free LLM key are configured in a local .env that git ignores
- Given .env.example, when compared with code, then every required variable is documented

### TS-E0-08: Baseline measurement plan  (3 pts, Sprint 1, To do, Jira TS-25)

*As a product owner I want a baseline of recruiter effort so that pilot results can be compared honestly.*

Traces to: BO-1

Acceptance criteria:
- Given 3 recruiters, when they log 5 requirements each, then minutes per sourcing phase and acceptance rate are recorded
- Given the baseline, when published, then it states sample size and limitations

### TS-E0-09: Agile artefacts in Jira  (3 pts, Sprint 0, Done, Jira TS-26)

*As an engineering manager I want epics, stories and sprints in Jira so that delivery is tracked transparently.*

Traces to: n/a

Acceptance criteria:
- Given backlog.json, when imported, then every epic and story exists in Jira with points and sprint
- Given the board, when Sprint 0 starts, then its committed stories are in the sprint

## EA: HR Guru ATS restore and integration

Bring the live ATS back (local Docker + Cloudflare Tunnel), protect it (backups, security), and connect TalentScout to it read-only.

### TS-EA-01: Import ATS into the monorepo  (2 pts, Sprint 0, Done, Jira TS-9)

*As a tech lead I want the ATS code in this repository so that one pipeline builds, tests and scans everything.*

Traces to: ADR-0006

Acceptance criteria:
- Given hireflow@990f832, then it is in apps/ats without git history and without real candidate data or backup files

### TS-EA-02: Make the ATS run locally on macOS  (3 pts, Sprint 0, Done, Jira TS-10)

*As a recruiter I want the ATS available again so that I can keep uploading candidates and managing requirements.*

Traces to: FR-ATS-1

Acceptance criteria:
- Given Docker on the Mac, when docker compose up ats-db ats runs, then /healthz is ok and admin login works
- Given macOS/Linux, then the single-instance lock works (Windows-only msvcrt replaced)
- Given an empty PostgreSQL, then bootstrap_empty_postgres.sh creates the schema and refuses to touch a database that has data

### TS-EA-03: Patch vulnerable ATS dependencies  (2 pts, Sprint 0, Done, Jira TS-11)

*As a security owner I want known CVEs fixed so that the live ATS is not exposed through old libraries.*

Traces to: NFR-8

Acceptance criteria:
- Given pip-audit and Trivy, then apps/ats/requirements.txt has 0 known vulnerabilities (was 61, 7 critical)
- Given the upgrade, then SQLite and PostgreSQL smoke tests pass

### TS-EA-04: Recover production ATS data  (3 pts, Sprint 0, Done, Jira TS-12)

*As a director I want the production candidates, requirements and CVs back so that recruiters do not start from zero.*

Traces to: FR-ATS-1

Acceptance criteria:
- Given the legacy ats.db on the MacBook, when scripts/restore_from_sqlite.sh runs, then the copy is upgraded to the current schema, migrated, and counts and newest dates are printed (tested on a synthetic legacy-schema file)
- Given a pg_dump, EBS snapshot or legacy ats.db, when restored by the runbook, then candidate and requirement counts match the last known values (about 3,600 and 400)
- Given no backup exists, then the loss is recorded and the ATS starts fresh (procedure B3)
- Result 2026-11-27: restored 9,988 candidates, 1,685 requirements, 41 team members, 5 app users from ats.db (sha256 0eb4a831...). Newest records 2026-05-26; data entered on the AWS PostgreSQL after that date is not in this file (gap tracked as R-13 and TS-EA-10)

### TS-EA-05: Expose the local ATS to 25 recruiters securely  (3 pts, Sprint 0, Done, Jira TS-13)

*As a recruiter I want to reach the ATS from my own laptop so that I can work as before.*

Traces to: NFR-1

Acceptance criteria:
- Given a Cloudflare Tunnel, then https://ats.hrgp.in serves the local ATS over HTTPS with no open router ports
- Given Google login, then the OAuth redirect URI works on the new host

### TS-EA-06: ATS backups and restore drill  (3 pts, Sprint 0, Done, Jira TS-14)

*As a director I want nightly backups and a tested restore so that losing the host never loses data again.*

Traces to: NFR-4

Acceptance criteria:
- Given launchd at 21:00, then a pg_dump and an uploads archive are written and 14 copies kept, with an off-machine copy
- Given a backup, when restored into a scratch database, then counts match (drill recorded)

### TS-EA-07: ATS security hardening baseline  (5 pts, Sprint 1, To do, Jira TS-15)

*As a security owner I want the most serious ATS weaknesses fixed so that a live system with candidate PII is safe enough to run.*

Traces to: NFR-1, BR-4

Acceptance criteria:
- Given an API error, then clients receive a generic message and details go only to logs
- Given CodeQL and Semgrep findings for apps/ats, then all high and critical are fixed or risk-accepted in a tracked list
- Given AI screening, then the owner's decision on Gemini and PII (R-11) is implemented

### TS-EA-08: Read-only ATS connector  (5 pts, Sprint 2, To do, Jira TS-16)

*As a recruiter I want TalentScout to see the candidates I upload to the ATS so that agents search real, current profiles.*

Traces to: FR-ATS-2, FR-ATS-3, FR-ATS-4

Acceptance criteria:
- Given a SELECT-only DB role, when the connector syncs, then new or changed candidates appear in TalentScout within 10 minutes
- Given a candidate deleted in the ATS, then its profile, chunks and embeddings are removed at the next sync
- Given a write attempt through the connector role, then the database refuses it

### TS-EA-09: ATS health monitoring  (2 pts, Sprint 0, Done, Jira TS-17)

*As a delivery lead I want to know within minutes if the ATS is down so that recruiters are not blocked.*

Traces to: NFR-4

Acceptance criteria:
- Given the ATS stops responding, then an alert is sent within 5 minutes (existing monitor_health script or a free uptime monitor)

### TS-EA-10: Close the post-May 2026 data gap and the missing CV/JD files  (2 pts, Sprint 0, To do, Jira TS-69)

*As a director I want candidates and requirements added after 26 May 2026 recovered or re-entered so that recruiters work from complete data.*

Traces to: FR-ATS-1

Acceptance criteria:
- Given any remaining AWS artefact (EBS snapshot, RDS or pg_dump, S3 backup, recruiter Excel uploads), when found, then the missing records are imported with the runbook B1 procedure
- Given nothing remains, then recruiters re-upload active candidates and open requirements through bulk upload, and the gap is recorded
- Findings 2026-11-28: CV/JD files were only on the EC2 disk; no ATS zip backups found in Google Drive. Remaining source: AWS detached EBS volumes / snapshots / AMIs / AWS Backup in the old region; otherwise recruiters re-upload CVs for active candidates

## E1: Requirement agent

Auth, requirements, existing JD parser reuse, LLM router v0 and a bounded single agent with structured output.

### TS-E1-01: Requirement CRUD API and UI  (5 pts, Sprint 1, To do, Jira TS-27)

*As a recruiter I want to create and view requirements with constraints so that the agents know the hiring goal.*

Traces to: FR-REQ-1, FR-REQ-4

Acceptance criteria:
- Given the UC-001 values (12-18 yrs, Gurgaon, 45 LPA, notice <= 30 days, 7 mandatory skills), when I create the requirement, then all constraints are stored as mandatory
- Given valid input, when I create a requirement, then it is saved with status draft and returned
- Given a budget below 0 or a missing title, when I submit, then I get a 400 problem+json response naming the field

### TS-E1-02: Authentication and RBAC  (5 pts, Sprint 1, To do, Jira TS-28)

*As an admin I want role-based access so that each user sees only what they should.*

Traces to: FR-AUTH-1, FR-AUTH-2, FR-AUTH-3

Acceptance criteria:
- Given valid credentials, when I log in, then I receive a 15-minute access token and a refresh cookie
- Given a recruiter token, when I call an admin route, then I get 403
- Given a reused refresh token, when I refresh, then all sessions for that user are revoked

### TS-E1-03: LLM router v0 with PII flag  (3 pts, Sprint 1, To do, Jira TS-29)

*As an architect I want every model call to go through a router that knows data sensitivity so that PII never reaches a cloud tier.*

Traces to: NFR-3, NFR-4

Acceptance criteria:
- Given pii=true, when a cloud route is configured, then the router raises PolicyViolation
- Given a 429 from the free tier, when pii=false, then the router falls back to Ollama

### TS-E1-04: Requirement agent with structured output and repair loop  (5 pts, Sprint 2, To do, Jira TS-30)

*As a recruiter I want the JD analysed into must-haves, constraints and ambiguities so that sourcing starts from a clear brief.*

Traces to: FR-REQ-2

Acceptance criteria:
- Given the UC-001 JD and 9 other golden JDs, when analysed, then output validates against RequirementAnalysis and lists all 7 UC-001 mandatory skills
- Given a malformed model reply, when parsing fails, then the agent repairs at most 2 times and otherwise marks needs_human
- Given a JD containing an injection instruction, when analysed, then behaviour and schema are unchanged

### TS-E1-05: Clarification questions UI  (3 pts, Sprint 2, To do, Jira TS-31)

*As a recruiter I want to answer or dismiss clarification questions so that the brief improves before sourcing.*

Traces to: FR-REQ-3

Acceptance criteria:
- Given analysis questions, when I answer one, then the requirement version increments and the answer is stored
- Given I dismiss a question, then it is hidden and recorded as dismissed

### TS-E1-06: Audit events v0  (2 pts, Sprint 2, To do, Jira TS-32)

*As an admin I want every agent call recorded so that decisions are traceable.*

Traces to: FR-OBS-1

Acceptance criteria:
- Given an analysis run, when it completes, then model_call and observation events exist with model, tokens and latency
- Given the app database user, when it tries to update an audit event, then it is denied

### TS-E1-07: Golden JD dataset and test  (3 pts, Sprint 2, To do, Jira TS-33)

*As QA I want 10 golden JDs with expected must-haves so that prompt changes are measurable.*

Traces to: NFR-7

Acceptance criteria:
- Given the golden set, when the eval runs, then must-have recall and precision are reported
- Given recall drops more than 10 points versus baseline, then the eval exits non-zero

### TS-E1-08: Review ATS JD and CV parsers and decide reuse  (2 pts, Sprint 1, To do, Jira TS-34)

*As an architect I want the ATS parsing code reviewed so that TalentScout reuses it through a stable wrapper instead of rebuilding it.*

Traces to: FR-REQ-0, FR-CAND-0

Acceptance criteria:
- Given the parser code, when reviewed, then an ADR records reuse approach (library, service or rewrite), interfaces, quality on 10 sample documents and security findings
- Given the decision, then jd.parse and resume.parse tool contracts are defined in the LLD

## E2: Intelligent retrieval

Synthetic data (incl. UC-001), resume parsing, embeddings, hybrid search, funnel analysis and the Sourcing agent.

### TS-E2-01: Synthetic candidate generator incl. UC-001 scenario set  (5 pts, Sprint 2, To do, Jira TS-35)

*As a developer I want 2,000 realistic fictional candidates so that we can build and demo without real PII.*

Traces to: FR-CAND-4, FR-CAND-3

Acceptance criteria:
- Given a seed, when the generator runs, then the output is deterministic
- Given the UC-001 profile, when generated into a development ATS database (never the live one), then 500 resumes reproduce the funnel 500 -> 80 -> 25 -> 12 -> 2 and include serving-notice and alternative-title candidates that qualify
- Given generated data, when checked, then no protected attributes are present in searchable fields

### TS-E2-07: Resume parsing of ATS CVs  (3 pts, Sprint 2, To do, Jira TS-36)

*As a recruiter I want CVs from the ATS parsed into structured fields so that matching uses reliable experience, notice and skills data.*

Traces to: FR-CAND-0

Acceptance criteria:
- Given a CV synced from the ATS, when ingested, then the ATS parser (via resume.parse) produces structured fields and sections before chunking
- Given a resume the parser cannot handle, then it is flagged for review and not silently dropped

### TS-E2-02: Chunking, masking and embedding pipeline  (5 pts, Sprint 3, To do, Jira TS-37)

*As a developer I want resumes chunked, masked and embedded locally so that semantic search is possible safely.*

Traces to: FR-CAND-1

Acceptance criteria:
- Given a resume, when processed, then chunks by section exist with 768-dim local embeddings
- Given a chunk containing an email or phone number, when masked, then neither appears in the stored text

### TS-E2-03: Atlas vector and text indexes  (2 pts, Sprint 3, To do, Jira TS-38)

*As a developer I want vector and text indexes defined as code so that environments are reproducible.*

Traces to: FR-CAND-2

Acceptance criteria:
- Given atlas-local, when the setup script runs, then vector_index and text_index exist
- Given the script runs twice, then it is idempotent

### TS-E2-04: Hybrid search with RRF and filters  (5 pts, Sprint 3, To do, Jira TS-39)

*As a recruiter I want meaning-based and keyword search combined so that I find relevant people who use different words.*

Traces to: FR-CAND-2, NFR-5

Acceptance criteria:
- Given a query and filters, when searched, then results honour notice and CTC filters
- Given 50k profiles, when searched, then p95 latency is under 1 s locally

### TS-E2-05: Sourcing agent with tool calling  (5 pts, Sprint 3, To do, Jira TS-40)

*As a recruiter I want an agent to formulate searches from the requirement so that I do not write boolean strings.*

Traces to: FR-AGT-6, FR-CAND-5

Acceptance criteria:
- Given an analysed requirement, when the agent runs, then it issues at most 5 tool calls and returns candidates with retrieved evidence
- Given the UC-001 dataset, when the agent searches, then it reports funnel counts per stage (experience, skills, budget, notice)

### TS-E2-06: Retrieval evaluation: hybrid vs keyword  (4 pts, Sprint 3, To do, Jira TS-41)

*As an architect I want recall@10 and nDCG@10 measured so that the hybrid design is justified with data.*

Traces to: NFR-7

Acceptance criteria:
- Given 20 golden queries, when the eval runs, then hybrid and keyword scores are reported side by side
- Given results, then they are recorded in the sprint review notes

## E3: Multi-agent orchestration

LangGraph supervisor, bottleneck diagnosis, replanning with frozen constraints, escalation, evidence-based matching, approval gate.

### TS-E3-01: LangGraph supervisor graph and state  (5 pts, Sprint 3, To do, Jira TS-42)

*As a recruiter I want one goal to trigger a coordinated team of agents so that I do not orchestrate steps myself.*

Traces to: FR-AGT-1, FR-AGT-2

Acceptance criteria:
- Given a requirement, when a run starts, then a plan with steps and success criteria is stored
- Given the graph, when visualised, then nodes and conditional edges match the LLD

### TS-E3-02: Bottleneck diagnosis, replanning and escalation (UC-001)  (8 pts, Sprint 4, To do, Jira TS-43)

*As a recruiter I want the system to recognise why the objective was not met and change strategy, without breaking my hiring constraints, and to tell me when it cannot succeed.*

Traces to: FR-AGT-3, FR-AGT-4, FR-AGT-4a, FR-AGT-4b

Acceptance criteria:
- Given the UC-001 dataset, when only 2 candidates qualify, then the supervisor names notice period as the primary bottleneck
- Given the bottleneck, then it replans with at least serving-notice and alternative-title strategies
- Given any replan, then the mandatory constraints in run state equal the original requirement (budget, skills, experience, location, notice)
- Given fewer than 5 qualify after 3 replans, then the run ends escalated with the funnel, strategies tried and decision options, not failed

### TS-E3-03: Evidence-based matching per mandatory skill  (5 pts, Sprint 4, To do, Jira TS-44)

*As a recruiter I want each requirement judged with quotes from the resume so that I can trust the score.*

Traces to: FR-AGT-6

Acceptance criteria:
- Given a candidate, when screened, then each of the 7 UC-001 mandatory skills has a verdict with an evidence quote, or the verdict unknown
- Given a resume without the skill, then the verdict is not_met or unknown, never met

### TS-E3-04: Quality agent evidence verification  (5 pts, Sprint 4, To do, Jira TS-45)

*As a delivery lead I want unsupported claims caught before recruiters see them so that clients get accurate submissions.*

Traces to: FR-AGT-7

Acceptance criteria:
- Given a screening with a fabricated quote, when verified, then it is flagged unsupported and removed from facts
- Given a clean screening, then no flags are raised

### TS-E3-05: Live run view over SSE (dashboard part 1)  (3 pts, Sprint 5, To do, Jira TS-46)

*As a recruiter I want to watch the agents plan, act and replan so that I understand what they are doing.*

Traces to: FR-AGT-10, FR-DASH-3

Acceptance criteria:
- Given a running workflow, when I open the run page, then plan, tool_call, observation and replan events appear in order
- Given the connection drops, when it reconnects, then missed events are replayed

### TS-E3-06: Human approval gate for shortlist and escalation  (6 pts, Sprint 4, To do, Jira TS-47)

*As a recruiter I want to approve or reject each shortlisted candidate with a reason so that I remain accountable.*

Traces to: FR-AGT-8, FR-OUT-2

Acceptance criteria:
- Given a shortlist or an escalation, when the run reaches the gate, then status is awaiting_approval and the graph is interrupted
- Given my decisions, when submitted, then the run resumes and an approval record with user and time is stored
- Given a delivery_lead token, when submitting decisions, then 403

## E4: MCP and memory

MCP tool server, scopes, durable execution, long-term memory, live run view.

### TS-E4-01: MCP server with recruitment tools  (5 pts, Sprint 5, To do, Jira TS-48)

*As an architect I want recruitment capabilities exposed as MCP tools so that any compliant agent can use them through one contract.*

Traces to: n/a

Acceptance criteria:
- Given the MCP server, when a client lists tools, then the catalogue in the LLD is returned with JSON Schemas
- Given invalid tool arguments, then a structured error is returned and nothing is written

### TS-E4-02: Agents consume tools via MCP client  (3 pts, Sprint 5, To do, Jira TS-49)

*As a developer I want agents to discover tools at runtime so that adding a tool needs no agent code change.*

Traces to: n/a

Acceptance criteria:
- Given the agent service, when it starts, then it discovers tools from the MCP server
- Given the MCP server is down, then the run pauses with a clear error instead of crashing

### TS-E4-03: Per-agent tool scopes  (3 pts, Sprint 5, To do, Jira TS-50)

*As a security owner I want each agent limited to its tools so that a compromised agent cannot act beyond its role.*

Traces to: NFR-1

Acceptance criteria:
- Given the Sourcing agent session, when it calls shortlist.finalise, then the call is denied and a guardrail_block audit event is written

### TS-E4-04: Durable execution with MongoDB checkpointer  (5 pts, Sprint 5, To do, Jira TS-51)

*As a recruiter I want an interrupted run to continue where it stopped so that work and quota are not wasted.*

Traces to: FR-AGT-9, NFR-4

Acceptance criteria:
- Given the agent process is killed mid-run, when restarted, then the run resumes from the last checkpoint
- Given a resumed run, then no tool call with the same idempotency key is executed twice

### TS-E4-05: Long-term feedback memory  (5 pts, Sprint 5, To do, Jira TS-52)

*As a recruiter I want my rejection reasons remembered so that future searches avoid the same mistakes.*

Traces to: FR-MEM-2, FR-MEM-3

Acceptance criteria:
- Given recruiter feedback approved at the gate, when saved via memory.save_feedback with an approvalId, then it is embedded and tagged by role family
- Given a new similar requirement, when the Sourcing agent plans, then relevant feedback is retrieved and shown in the trace

## E5: Responsible AI and LLMOps

Guardrails, PII routing, limits, tracing, evaluations, audit integrity, DPDP.

### TS-E5-01: Prompt-injection defence for untrusted content  (5 pts, Sprint 6, To do, Jira TS-53)

*As a security owner I want resumes and JDs treated as data so that embedded instructions cannot steer agents.*

Traces to: NFR-1

Acceptance criteria:
- Given the injection corpus (20 cases), when evaluated, then no case changes scores or triggers tools
- Given a detected injection, then a guardrail_block event is recorded

### TS-E5-02: PII masking and local-only routing enforcement  (3 pts, Sprint 6, To do, Jira TS-54)

*As a data protection contact I want PII masked and kept local so that we comply with DPDP and provider terms.*

Traces to: NFR-2, NFR-3

Acceptance criteria:
- Given any cloud-bound prompt, when inspected in tests, then no email, phone or name from the candidate store appears
- Given pii=true, then only the local route is ever used

### TS-E5-03: Langfuse tracing and prompt versioning  (3 pts, Sprint 6, To do, Jira TS-55)

*As a tech lead I want traces and prompt versions so that I can debug and compare agent behaviour.*

Traces to: FR-OBS-2

Acceptance criteria:
- Given a run, then a Langfuse trace exists with spans per node and tool, with PII masked
- Given a prompt change, then the new version id is recorded on each call

### TS-E5-04: Loop, time and token limits  (3 pts, Sprint 6, To do, Jira TS-56)

*As an engineering manager I want hard limits so that runaway agents cannot burn quota or time.*

Traces to: FR-AGT-5

Acceptance criteria:
- Given a graph that never satisfies its goal, when run, then it stops at 12 iterations with status stopped_limit and a partial result

### TS-E5-05: Approval-token gate on side-effecting tools  (3 pts, Sprint 6, To do, Jira TS-57)

*As a director I want side-effecting tools to be impossible to run without approval so that there are zero unauthorised actions.*

Traces to: BR-5

Acceptance criteria:
- Given no approvalId, when shortlist.finalise or memory.save_feedback is called, then it is refused and audited
- Given an approval for a different run or candidate, then it is refused

### TS-E5-06: Step-up re-authentication for approvals  (3 pts, Sprint 6, To do, Jira TS-58)

*As a security owner I want recent authentication before approvals so that a stolen session cannot approve a shortlist or constraint relaxation.*

Traces to: FR-AUTH-1

Acceptance criteria:
- Given a session older than 10 minutes, when approving a shortlist or a constraint relaxation, then password re-entry is required

### TS-E5-07: Tamper-evident audit trail  (3 pts, Sprint 6, To do, Jira TS-59)

*As an auditor I want to detect altered audit events so that the trail can be trusted.*

Traces to: FR-OBS-1, KPI-6

Acceptance criteria:
- Given a run's events, when one is modified directly in the DB, then the verification endpoint reports the broken hash chain
- Given a completed run, when the completeness check runs, then every graph step has a matching audit event (traceability 100%)

### TS-E5-08: Evaluation gate in CI  (5 pts, Sprint 6, To do, Jira TS-60)

*As QA I want evals to run on agent changes so that quality regressions block merges.*

Traces to: NFR-7

Acceptance criteria:
- Given a PR touching prompts or agents, when CI runs, then golden, hallucination and fairness (name-swap) evals run on synthetic data
- Given a regression beyond threshold, then the check fails

### TS-E5-10: DPDP compliance pack  (3 pts, Sprint 7, To do, Jira TS-61)

*As a data protection contact I want consent, retention and erasure implemented so that the pilot can use real data lawfully.*

Traces to: NFR-2

Acceptance criteria:
- Given an erasure request, when executed, then the candidate, chunks, embeddings and memory references are deleted and logged
- Given retentionUntil has passed, when the job runs, then records are purged

## E6: Interoperability, delivery and pilot

LiteLLM routing, parallelism, agent execution dashboard, performance testing, deployment, pilot, A2A (stretch).

### TS-E6-01: LiteLLM gateway with multi-provider fallback  (5 pts, Sprint 7, To do, Jira TS-62)

*As an architect I want routing across free providers with fallback so that rate limits do not stop work.*

Traces to: NFR-3, NFR-4

Acceptance criteria:
- Given provider A returns 429, when called, then provider B is used, then Ollama
- Given routing policy tests, then pii=true never reaches a cloud provider

### TS-E6-02: Parallel screening fan-out  (3 pts, Sprint 7, To do, Jira TS-63)

*As a recruiter I want candidates screened in parallel so that shortlists arrive faster.*

Traces to: NFR-5

Acceptance criteria:
- Given 20 candidates, when screened, then concurrency is bounded and total time drops versus sequential, recorded in the review

### TS-E6-03: Agent execution dashboard (dashboard part 2)  (5 pts, Sprint 7, To do, Jira TS-64)

*As a delivery lead I want run history and KPIs in one place so that I can see whether the agents are working and what they cost.*

Traces to: FR-DASH-1, FR-DASH-2, FR-DASH-3

Acceptance criteria:
- Given completed runs, then the dashboard shows status, replans, duration, tokens, model routes and notional cost per run
- Given a period, then completion rate, acceptance rate, evidence accuracy, escalations and guardrail blocks are shown
- Given any run, then it links to its full timeline and trace

### TS-E6-04: A2A Talent Intelligence agent (stretch)  (5 pts, Sprint 7, To do, Jira TS-65)

*As an architect I want an independently deployed agent reachable over A2A so that we prove interoperability.*

Traces to: n/a

Acceptance criteria:
- Given the agent card, when the supervisor discovers it, then it can delegate a salary-benchmark task and receive a result
- Given the A2A agent is unavailable, then the run continues without it and logs a warning

### TS-E6-05: Demo deployment  (3 pts, Sprint 7, To do, Jira TS-66)

*As a candidate in interviews I want a running demo on synthetic data so that I can show the system live.*

Traces to: n/a

Acceptance criteria:
- Given a merge to main with demo secrets, when CD runs, then the demo host serves the latest images and health checks pass

### TS-E6-07: Performance and resilience testing  (3 pts, Sprint 7, To do, Jira TS-67)

*As a tech lead I want load and failure drills so that the pilot runs on a system with known limits.*

Traces to: NFR-5, NFR-4

Acceptance criteria:
- Given k6 load on API and search, then p95 targets in NFR-5 are met or the gap is reported
- Given the agent process is killed or a provider is down during a UC-001 run, then the run recovers and the drill result is recorded

### TS-E6-06: Recruiter pilot and results report  (3 pts, Sprint 7, To do, Jira TS-68)

*As a director I want a pilot report against the baseline so that the decision to scale is evidence-based.*

Traces to: BO-1, BO-2

Acceptance criteria:
- Given 2 weeks of pilot use, then the report compares effort, acceptance, evidence accuracy and incidents against the baseline, with limitations stated
