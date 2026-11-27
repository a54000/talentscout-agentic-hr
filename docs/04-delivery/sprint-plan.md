# Sprint Plan

_Generated from `backlog.json`. Two-week sprints; planned velocity 26 points (recalibrated after Sprints 0 and 1)._

| Sprint | Dates | Goal | Points | Load |
|---|---|---|---|---|
| 0 | 2026-11-30 → 2026-12-11 | Documents baselined, backlog ready, and a walking skeleton that builds, tests, scans and ships through CI/CD. | 24 | OK |
| 1 | 2026-12-14 → 2026-12-24 | A recruiter can create the UC-001 requirement and get a validated, structured JD analysis (existing parser plus a bounded single agent) with clarification questions. | 28 | +2 over (stretch items flagged in planning) |
| 2 | 2027-01-04 → 2027-01-15 | Resumes are parsed and indexed; the Sourcing agent runs hybrid search with funnel counts on the UC-001 dataset and beats keyword search on golden queries. | 25 | OK |
| 3 | 2027-01-18 → 2027-01-29 | UC-001 end to end: the supervisor diagnoses the notice-period bottleneck, replans without relaxing constraints, verifies evidence per mandatory skill, and pauses for recruiter approval or escalates. | 29 | +3 over (stretch items flagged in planning) |
| 4 | 2027-02-01 → 2027-02-12 | Agents use tools only through a scoped MCP server, survive crashes via checkpoints, learn from approved feedback, and runs are visible live. | 28 | +2 over (stretch items flagged in planning) |
| 5 | 2027-02-15 → 2027-02-26 | The platform is controlled and observable: guardrails, PII routing, limits, tracing, tamper-evident audit and an evaluation gate in CI. | 28 | +2 over (stretch items flagged in planning) |
| 6 | 2027-03-01 → 2027-03-12 | Enterprise-style MVP: multi-provider routing, agent execution dashboard, performance testing, demo deployment and a recruiter pilot report (A2A as stretch). | 30 | +4 over (stretch items flagged in planning) |

## Sprint 0 - Inception and walking skeleton

**Dates:** 2026-11-30 → 2026-12-11  
**Goal:** Documents baselined, backlog ready, and a walking skeleton that builds, tests, scans and ships through CI/CD.

| Story | Title | Points |
|---|---|---|
| TS-E0-01 | Monorepo structure and tooling | 2 |
| TS-E0-02 | CI pipeline: lint, test, build | 3 |
| TS-E0-03 | Security scanning pipeline | 3 |
| TS-E0-04 | CD pipeline to GHCR and demo host | 3 |
| TS-E0-05 | Docker Compose local stack | 2 |
| TS-E0-06 | Spike: local model selection on M2 16 GB | 3 |
| TS-E0-07 | Free-tier accounts and secrets handling | 2 |
| TS-E0-08 | Baseline measurement plan | 3 |
| TS-E0-09 | Agile artefacts in Jira | 3 |

## Sprint 1 - Single-agent foundation

**Dates:** 2026-12-14 → 2026-12-24  
**Goal:** A recruiter can create the UC-001 requirement and get a validated, structured JD analysis (existing parser plus a bounded single agent) with clarification questions.

| Story | Title | Points |
|---|---|---|
| TS-E1-01 | Requirement CRUD API and UI | 5 |
| TS-E1-02 | Authentication and RBAC | 5 |
| TS-E1-03 | LLM router v0 with PII flag | 3 |
| TS-E1-04 | Requirement agent with structured output and repair loop | 5 |
| TS-E1-05 | Clarification questions UI | 3 |
| TS-E1-06 | Audit events v0 | 2 |
| TS-E1-07 | Golden JD dataset and test | 3 |
| TS-E1-08 | Review existing JD and resume parsers and decide reuse | 2 |

## Sprint 2 - RAG and intelligent retrieval

**Dates:** 2027-01-04 → 2027-01-15  
**Goal:** Resumes are parsed and indexed; the Sourcing agent runs hybrid search with funnel counts on the UC-001 dataset and beats keyword search on golden queries.

| Story | Title | Points |
|---|---|---|
| TS-E2-01 | Synthetic candidate generator incl. UC-001 scenario set | 5 |
| TS-E2-07 | Resume parsing in the ingestion pipeline | 3 |
| TS-E2-02 | Chunking, masking and embedding pipeline | 5 |
| TS-E2-03 | Atlas vector and text indexes | 2 |
| TS-E2-04 | Hybrid search with RRF and filters | 5 |
| TS-E2-05 | Sourcing agent with tool calling | 5 |

## Sprint 3 - Multi-agent orchestration

**Dates:** 2027-01-18 → 2027-01-29  
**Goal:** UC-001 end to end: the supervisor diagnoses the notice-period bottleneck, replans without relaxing constraints, verifies evidence per mandatory skill, and pauses for recruiter approval or escalates.

| Story | Title | Points |
|---|---|---|
| TS-E3-01 | LangGraph supervisor graph and state | 5 |
| TS-E3-02 | Bottleneck diagnosis, replanning and escalation (UC-001) | 8 |
| TS-E3-03 | Evidence-based matching per mandatory skill | 5 |
| TS-E3-04 | Quality agent evidence verification | 5 |
| TS-E3-06 | Human approval gate for shortlist and escalation | 6 |

## Sprint 4 - MCP and agent memory

**Dates:** 2027-02-01 → 2027-02-12  
**Goal:** Agents use tools only through a scoped MCP server, survive crashes via checkpoints, learn from approved feedback, and runs are visible live.

| Story | Title | Points |
|---|---|---|
| TS-E2-06 | Retrieval evaluation: hybrid vs keyword | 4 |
| TS-E3-05 | Live run view over SSE (dashboard part 1) | 3 |
| TS-E4-01 | MCP server with recruitment tools | 5 |
| TS-E4-02 | Agents consume tools via MCP client | 3 |
| TS-E4-03 | Per-agent tool scopes | 3 |
| TS-E4-04 | Durable execution with MongoDB checkpointer | 5 |
| TS-E4-05 | Long-term feedback memory | 5 |

## Sprint 5 - Responsible AI and LLMOps

**Dates:** 2027-02-15 → 2027-02-26  
**Goal:** The platform is controlled and observable: guardrails, PII routing, limits, tracing, tamper-evident audit and an evaluation gate in CI.

| Story | Title | Points |
|---|---|---|
| TS-E5-01 | Prompt-injection defence for untrusted content | 5 |
| TS-E5-02 | PII masking and local-only routing enforcement | 3 |
| TS-E5-03 | Langfuse tracing and prompt versioning | 3 |
| TS-E5-04 | Loop, time and token limits | 3 |
| TS-E5-05 | Approval-token gate on side-effecting tools | 3 |
| TS-E5-06 | Step-up re-authentication for approvals | 3 |
| TS-E5-07 | Tamper-evident audit trail | 3 |
| TS-E5-08 | Evaluation gate in CI | 5 |

## Sprint 6 - Interoperability, delivery and pilot

**Dates:** 2027-03-01 → 2027-03-12  
**Goal:** Enterprise-style MVP: multi-provider routing, agent execution dashboard, performance testing, demo deployment and a recruiter pilot report (A2A as stretch).

| Story | Title | Points |
|---|---|---|
| TS-E5-10 | DPDP compliance pack | 3 |
| TS-E6-01 | LiteLLM gateway with multi-provider fallback | 5 |
| TS-E6-02 | Parallel screening fan-out | 3 |
| TS-E6-03 | Agent execution dashboard (dashboard part 2) | 5 |
| TS-E6-04 | A2A Talent Intelligence agent (stretch) | 5 |
| TS-E6-05 | Demo deployment | 3 |
| TS-E6-07 | Performance and resilience testing | 3 |
| TS-E6-06 | Recruiter pilot and results report | 3 |

Holiday break: 2026-12-25 → 2027-01-01 (no sprint).
