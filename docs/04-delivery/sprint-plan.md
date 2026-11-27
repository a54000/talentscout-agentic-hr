# Sprint Plan

_Generated from `backlog.json`. Two-week sprints; planned velocity 26 points (recalibrated after Sprints 0 and 1)._

| Sprint | Dates | Goal | Points | Load |
|---|---|---|---|---|
| 0 | 2026-11-30 → 2026-12-11 | Documents baselined, backlog ready, and a walking skeleton that builds, tests, scans and ships through CI/CD. | 24 | OK |
| 1 | 2026-12-14 → 2026-12-24 | A recruiter can create a requirement and get a validated, structured JD analysis with clarification questions from a bounded single agent. | 26 | OK |
| 2 | 2027-01-04 → 2027-01-15 | The Sourcing agent finds candidates through hybrid search over synthetic profiles and beats keyword search on the golden queries. | 26 | OK |
| 3 | 2027-01-18 → 2027-01-29 | A supervised multi-agent run goes from requirement to an evidence-backed shortlist, replans when results are weak, and pauses for recruiter approval. | 29 | +3 over (stretch items flagged in planning) |
| 4 | 2027-02-01 → 2027-02-12 | Agents use recruitment tools only through a scoped MCP server, survive crashes via checkpoints, and learn from approved feedback. | 26 | OK |
| 5 | 2027-02-15 → 2027-02-26 | The platform is controlled and observable: guardrails, PII routing, limits, tracing and an evaluation gate in CI. | 28 | +2 over (stretch items flagged in planning) |
| 6 | 2027-03-01 → 2027-03-12 | Enterprise-style MVP: multi-provider routing, A2A agent, delivery dashboard, demo deployment and a recruiter pilot report. | 30 | +4 over (stretch items flagged in planning) |

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
**Goal:** A recruiter can create a requirement and get a validated, structured JD analysis with clarification questions from a bounded single agent.

| Story | Title | Points |
|---|---|---|
| TS-E1-01 | Requirement CRUD API and UI | 5 |
| TS-E1-02 | Authentication and RBAC | 5 |
| TS-E1-03 | LLM router v0 with PII flag | 3 |
| TS-E1-04 | Requirement agent with structured output and repair loop | 5 |
| TS-E1-05 | Clarification questions UI | 3 |
| TS-E1-06 | Audit events v0 | 2 |
| TS-E1-07 | Golden JD dataset and test | 3 |

## Sprint 2 - RAG and intelligent retrieval

**Dates:** 2027-01-04 → 2027-01-15  
**Goal:** The Sourcing agent finds candidates through hybrid search over synthetic profiles and beats keyword search on the golden queries.

| Story | Title | Points |
|---|---|---|
| TS-E2-01 | Synthetic candidate generator | 5 |
| TS-E2-02 | Chunking, masking and embedding pipeline | 5 |
| TS-E2-03 | Atlas vector and text indexes | 2 |
| TS-E2-04 | Hybrid search with RRF and filters | 5 |
| TS-E2-05 | Sourcing agent with tool calling | 5 |
| TS-E2-06 | Retrieval evaluation: hybrid vs keyword | 4 |

## Sprint 3 - Multi-agent orchestration

**Dates:** 2027-01-18 → 2027-01-29  
**Goal:** A supervised multi-agent run goes from requirement to an evidence-backed shortlist, replans when results are weak, and pauses for recruiter approval.

| Story | Title | Points |
|---|---|---|
| TS-E3-01 | LangGraph supervisor graph and state | 5 |
| TS-E3-02 | Replanning with constraint protection | 5 |
| TS-E3-03 | Screening agent with evidence | 5 |
| TS-E3-04 | Quality agent evidence verification | 5 |
| TS-E3-05 | Live run view over SSE | 3 |
| TS-E3-06 | Shortlist approval gate | 6 |

## Sprint 4 - MCP and agent memory

**Dates:** 2027-02-01 → 2027-02-12  
**Goal:** Agents use recruitment tools only through a scoped MCP server, survive crashes via checkpoints, and learn from approved feedback.

| Story | Title | Points |
|---|---|---|
| TS-E4-01 | MCP server with recruitment tools | 5 |
| TS-E4-02 | Agents consume tools via MCP client | 3 |
| TS-E4-03 | Per-agent tool scopes | 3 |
| TS-E4-04 | Durable execution with MongoDB checkpointer | 5 |
| TS-E4-05 | Long-term feedback memory | 5 |
| TS-E4-06 | Outreach agent drafts | 5 |

## Sprint 5 - Responsible AI and LLMOps

**Dates:** 2027-02-15 → 2027-02-26  
**Goal:** The platform is controlled and observable: guardrails, PII routing, limits, tracing and an evaluation gate in CI.

| Story | Title | Points |
|---|---|---|
| TS-E5-01 | Prompt-injection defence for untrusted content | 5 |
| TS-E5-02 | PII masking and local-only routing enforcement | 3 |
| TS-E5-03 | Langfuse tracing and prompt versioning | 3 |
| TS-E5-04 | Loop, time and token limits | 3 |
| TS-E5-05 | Approval-token gate on outreach.send | 3 |
| TS-E5-06 | Step-up re-authentication for approvals | 3 |
| TS-E5-07 | Tamper-evident audit trail | 3 |
| TS-E5-08 | Evaluation gate in CI | 5 |

## Sprint 6 - Interoperability, delivery and pilot

**Dates:** 2027-03-01 → 2027-03-12  
**Goal:** Enterprise-style MVP: multi-provider routing, A2A agent, delivery dashboard, demo deployment and a recruiter pilot report.

| Story | Title | Points |
|---|---|---|
| TS-E5-09 | Notional cost dashboard | 3 |
| TS-E5-10 | DPDP compliance pack | 3 |
| TS-E6-01 | LiteLLM gateway with multi-provider fallback | 5 |
| TS-E6-02 | Parallel screening fan-out | 3 |
| TS-E6-03 | Delivery agent and dashboard | 5 |
| TS-E6-04 | A2A Talent Intelligence agent | 5 |
| TS-E6-05 | Demo deployment | 3 |
| TS-E6-06 | Recruiter pilot and results report | 3 |

Holiday break: 2026-12-25 → 2027-01-01 (no sprint).
