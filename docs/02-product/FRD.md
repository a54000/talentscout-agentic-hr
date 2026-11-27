# Functional Requirements Document (FRD)

Version 0.1. Requirements trace back to the [PRD](PRD.md) features (F-xx) and forward to the backlog stories (TS-Ex-yy).

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
| FR-REQ-2 | The Requirement agent returns a **validated structured output**: must-have skills, nice-to-have skills, seniority, constraints, ambiguities[], clarification questions[]. Output failing schema validation is retried at most 2 times, then marked `needs_human`. | F-02 |
| FR-REQ-3 | The recruiter can answer, edit or dismiss clarification questions. Answers update the requirement version. | F-02 |
| FR-REQ-4 | Requirement status: `draft → analysed → sourcing → shortlist_ready → outreach → closed`. | F-02, F-15 |

### FR-CAND: Candidate store and search
| ID | Requirement | Feature |
|---|---|---|
| FR-CAND-1 | Candidates hold: profile fields, parsed resume, resume chunks with embeddings, source, consent status, created/updated dates. | F-03 |
| FR-CAND-2 | Hybrid search combines vector similarity and keyword (BM25) scores with reciprocal rank fusion, and supports filters (notice, CTC, location). | F-03 |
| FR-CAND-3 | Protected attributes are never stored in searchable fields or sent to LLMs. | F-03, F-11 |
| FR-CAND-4 | A synthetic data generator produces ≥ 2,000 realistic, fictional candidate profiles for development and testing. | F-03 |

### FR-AGT: Agent workflow
| ID | Requirement | Feature |
|---|---|---|
| FR-AGT-1 | Starting a run creates a `run` with a unique id and a thread id for checkpointing. | F-05 |
| FR-AGT-2 | The supervisor produces a plan (ordered steps with the target agent and success criterion) and records it. | F-05 |
| FR-AGT-3 | After each step the supervisor evaluates the observation against the success criteria and either continues, replans, asks the human, or stops. | F-05 |
| FR-AGT-4 | Replanning may relax only **optional** criteria. Each relaxation is logged with a reason. | F-05 |
| FR-AGT-5 | Hard limits: max 12 supervisor iterations, max 5 tool calls per agent step, wall-clock timeout of 10 min per run, token budget per run (configurable). A breached limit ends the run as `stopped_limit` with a partial result. | F-11 |
| FR-AGT-6 | The Screening agent outputs, for each candidate: a score from 0 to 100, and for each requirement a verdict (`met`, `partially_met`, `not_met`, `unknown`) with evidence quotes (chunk id plus text). | F-06 |
| FR-AGT-7 | The Quality agent checks each evidence quote against the source chunk and flags `unsupported` claims. Unsupported claims cannot reach the recruiter as facts. | F-06 |
| FR-AGT-8 | The workflow pauses at the approval gate (`interrupt`) and resumes when the recruiter submits decisions. | F-10 |
| FR-AGT-9 | A run interrupted by a crash or rate limit resumes from the last checkpoint. | F-08 |
| FR-AGT-10 | The UI streams step events: plan, tool call, observation, replan, approval needed, done. | F-05 |

### FR-MEM: Memory
| ID | Requirement | Feature |
|---|---|---|
| FR-MEM-1 | Short-term memory is the workflow state for a run (LangGraph state plus checkpoints). | F-08 |
| FR-MEM-2 | Long-term memory: approved recruiter feedback ("rejected: no hands-on EKS") is stored with an embedding and tagged by role family. | F-09 |
| FR-MEM-3 | The Sourcing agent retrieves relevant feedback when planning. Retrieved memories are shown in the trace. | F-09 |

### FR-OUT: Outreach
| ID | Requirement | Feature |
|---|---|---|
| FR-OUT-1 | Generate a draft message per approved candidate, using the requirement and evidence. No protected attributes; no invented facts. | — |
| FR-OUT-2 | Only a user with the `recruiter` role can approve a draft. Approval records user, time and the final text. | F-10 |
| FR-OUT-3 | In the MVP, the `outreach.send` tool is a stub that records the event. It refuses to run without an approval id. | F-10 |

### FR-DEL: Delivery monitoring
| ID | Requirement | Feature |
|---|---|---|
| FR-DEL-1 | Compute per requirement: age, stage, days in stage, submissions, acceptance rate. | F-15 |
| FR-DEL-2 | The Delivery agent flags at-risk requirements and recommends actions. Recommendations are advisory only. | F-15 |

### FR-OBS: Audit and observability
| ID | Requirement | Feature |
|---|---|---|
| FR-OBS-1 | Each agent step, tool call, model call (model, tokens, latency, cost), and approval is stored in the `audit_events` collection, which is append-only. | F-12 |
| FR-OBS-2 | Traces are exported to Langfuse with PII masked. | F-12 |
| FR-OBS-3 | An Admin can view a run timeline and export it as JSON. | F-12 |

## 2. Non-functional requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-1 | Security | OWASP ASVS L1 controls for the web/API. OWASP Top 10 for LLM Applications controls for the agents. |
| NFR-2 | Privacy | DPDP Act 2023: consent captured, purpose limitation, retention (default 12 months, configurable), right to erasure endpoint. |
| NFR-3 | Data locality | Real PII is processed only by local models (BR-4). Cloud LLMs receive only synthetic or masked data. |
| NFR-4 | Reliability | Durable execution; idempotent tool calls (idempotency key); retries with backoff on 429/5xx. |
| NFR-5 | Performance | API p95 < 300 ms (non-AI endpoints). Search p95 < 1 s on 50k profiles. |
| NFR-6 | Cost | $0 cash. Per-run token budget. Notional cost shown per run. |
| NFR-7 | Quality | Unit coverage ≥ 70% on business logic. Evaluation suite gates merges to `main` for prompt and agent changes. |
| NFR-8 | Supply chain | Dependencies pinned via lockfiles; Dependabot; SCA (software composition analysis), SAST, secret and container scans in CI. |
| NFR-9 | Accessibility | WCAG 2.1 AA for core screens. |
| NFR-10 | Portability | Whole stack runs with `docker compose up`. Ollama runs natively on macOS for GPU (Metal) acceleration. |

## 3. Traceability

The backlog (`docs/04-delivery/backlog.md`) maps each story to FR ids. The test strategy maps test suites to FR and NFR ids.
