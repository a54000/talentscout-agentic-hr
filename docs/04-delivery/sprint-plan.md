# Sprint Plan

_Generated from `backlog.json`. Two-week sprints; planned velocity 26 points (recalibrated after Sprints 0 and 1)._

| Sprint | Dates | Goal | Points | Load |
|---|---|---|---|---|
| 0 | 2026-11-30 → 2026-12-11 | Documents baselined, backlog ready, CI/CD and security scanning live, and the HR Guru ATS running locally again for recruiters with backups. | 38 | +12 over (stretch items flagged in planning) |
| 1 | 2026-12-14 → 2026-12-24 | The live ATS is hardened and measured (baseline); TalentScout has auth, requirements, the PII-aware model router and a parser reuse decision. | 26 | OK |
| 2 | 2027-01-04 → 2027-01-15 | The Requirement agent analyses the UC-001 JD into validated structured output, and candidates, CVs and requirements sync read-only from the ATS. | 26 | OK |
| 3 | 2027-01-18 → 2027-01-29 | Hybrid search with funnel counts over ATS-sourced candidates beats keyword search on golden queries; the supervisor graph exists. | 26 | OK |
| 4 | 2027-02-01 → 2027-02-12 | UC-001 end to end: bottleneck diagnosis, replanning with frozen constraints, evidence per mandatory skill, approval or escalation. | 24 | OK |
| 5 | 2027-02-15 → 2027-02-26 | Agents use tools only through a scoped MCP server, survive crashes via checkpoints, learn from approved feedback, and runs are visible live. | 24 | OK |
| 6 | 2027-03-01 → 2027-03-12 | Guardrails, PII routing, limits, tracing, tamper-evident audit and an evaluation gate in CI. | 28 | +2 over (stretch items flagged in planning) |
| 7 | 2027-03-15 → 2027-03-26 | Multi-provider routing, agent execution dashboard, performance testing, DPDP pack, and a recruiter pilot report (A2A as stretch). | 30 | +4 over (stretch items flagged in planning) |

## Sprint 0 - Inception, walking skeleton and ATS restore

**Dates:** 2026-11-30 → 2026-12-11  
**Goal:** Documents baselined, backlog ready, CI/CD and security scanning live, and the HR Guru ATS running locally again for recruiters with backups.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-EA-01 | Import ATS into the monorepo | 2 | Done |
| TS-EA-02 | Make the ATS run locally on macOS | 3 | Done |
| TS-EA-03 | Patch vulnerable ATS dependencies | 2 | Done |
| TS-EA-04 | Recover production ATS data | 3 | Done |
| TS-EA-05 | Expose the local ATS to 25 recruiters securely | 3 | Done |
| TS-EA-06 | ATS backups and restore drill | 3 | Done |
| TS-EA-09 | ATS health monitoring | 2 | To do |
| TS-EA-10 | Close the post-May 2026 data gap | 2 | To do |
| TS-E0-01 | Monorepo structure and tooling | 2 | Done |
| TS-E0-02 | CI pipeline: lint, test, build | 3 | In progress |
| TS-E0-03 | Security scanning pipeline | 3 | In progress |
| TS-E0-04 | CD pipeline to GHCR and demo host | 3 | In progress |
| TS-E0-05 | Docker Compose local stack | 2 | In progress |
| TS-E0-07 | Free-tier accounts and secrets handling | 2 | To do |
| TS-E0-09 | Agile artefacts in Jira | 3 | Done |

## Sprint 1 - ATS hardening and product foundation

**Dates:** 2026-12-14 → 2026-12-24  
**Goal:** The live ATS is hardened and measured (baseline); TalentScout has auth, requirements, the PII-aware model router and a parser reuse decision.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-EA-07 | ATS security hardening baseline | 5 | To do |
| TS-E0-06 | Spike: local model selection on M2 16 GB | 3 | To do |
| TS-E0-08 | Baseline measurement plan | 3 | To do |
| TS-E1-01 | Requirement CRUD API and UI | 5 | To do |
| TS-E1-02 | Authentication and RBAC | 5 | To do |
| TS-E1-03 | LLM router v0 with PII flag | 3 | To do |
| TS-E1-08 | Review ATS JD and CV parsers and decide reuse | 2 | To do |

## Sprint 2 - Single-agent foundation and ATS connector

**Dates:** 2027-01-04 → 2027-01-15  
**Goal:** The Requirement agent analyses the UC-001 JD into validated structured output, and candidates, CVs and requirements sync read-only from the ATS.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-EA-08 | Read-only ATS connector | 5 | To do |
| TS-E1-04 | Requirement agent with structured output and repair loop | 5 | To do |
| TS-E1-05 | Clarification questions UI | 3 | To do |
| TS-E1-06 | Audit events v0 | 2 | To do |
| TS-E1-07 | Golden JD dataset and test | 3 | To do |
| TS-E2-01 | Synthetic candidate generator incl. UC-001 scenario set | 5 | To do |
| TS-E2-07 | Resume parsing of ATS CVs | 3 | To do |

## Sprint 3 - RAG and intelligent retrieval

**Dates:** 2027-01-18 → 2027-01-29  
**Goal:** Hybrid search with funnel counts over ATS-sourced candidates beats keyword search on golden queries; the supervisor graph exists.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E2-02 | Chunking, masking and embedding pipeline | 5 | To do |
| TS-E2-03 | Atlas vector and text indexes | 2 | To do |
| TS-E2-04 | Hybrid search with RRF and filters | 5 | To do |
| TS-E2-05 | Sourcing agent with tool calling | 5 | To do |
| TS-E2-06 | Retrieval evaluation: hybrid vs keyword | 4 | To do |
| TS-E3-01 | LangGraph supervisor graph and state | 5 | To do |

## Sprint 4 - Multi-agent orchestration (UC-001 end to end)

**Dates:** 2027-02-01 → 2027-02-12  
**Goal:** UC-001 end to end: bottleneck diagnosis, replanning with frozen constraints, evidence per mandatory skill, approval or escalation.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E3-02 | Bottleneck diagnosis, replanning and escalation (UC-001) | 8 | To do |
| TS-E3-03 | Evidence-based matching per mandatory skill | 5 | To do |
| TS-E3-04 | Quality agent evidence verification | 5 | To do |
| TS-E3-06 | Human approval gate for shortlist and escalation | 6 | To do |

## Sprint 5 - MCP, memory and durable execution

**Dates:** 2027-02-15 → 2027-02-26  
**Goal:** Agents use tools only through a scoped MCP server, survive crashes via checkpoints, learn from approved feedback, and runs are visible live.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E3-05 | Live run view over SSE (dashboard part 1) | 3 | To do |
| TS-E4-01 | MCP server with recruitment tools | 5 | To do |
| TS-E4-02 | Agents consume tools via MCP client | 3 | To do |
| TS-E4-03 | Per-agent tool scopes | 3 | To do |
| TS-E4-04 | Durable execution with MongoDB checkpointer | 5 | To do |
| TS-E4-05 | Long-term feedback memory | 5 | To do |

## Sprint 6 - Responsible AI and LLMOps

**Dates:** 2027-03-01 → 2027-03-12  
**Goal:** Guardrails, PII routing, limits, tracing, tamper-evident audit and an evaluation gate in CI.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E5-01 | Prompt-injection defence for untrusted content | 5 | To do |
| TS-E5-02 | PII masking and local-only routing enforcement | 3 | To do |
| TS-E5-03 | Langfuse tracing and prompt versioning | 3 | To do |
| TS-E5-04 | Loop, time and token limits | 3 | To do |
| TS-E5-05 | Approval-token gate on side-effecting tools | 3 | To do |
| TS-E5-06 | Step-up re-authentication for approvals | 3 | To do |
| TS-E5-07 | Tamper-evident audit trail | 3 | To do |
| TS-E5-08 | Evaluation gate in CI | 5 | To do |

## Sprint 7 - Routing, dashboard, performance and pilot

**Dates:** 2027-03-15 → 2027-03-26  
**Goal:** Multi-provider routing, agent execution dashboard, performance testing, DPDP pack, and a recruiter pilot report (A2A as stretch).

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E5-10 | DPDP compliance pack | 3 | To do |
| TS-E6-01 | LiteLLM gateway with multi-provider fallback | 5 | To do |
| TS-E6-02 | Parallel screening fan-out | 3 | To do |
| TS-E6-03 | Agent execution dashboard (dashboard part 2) | 5 | To do |
| TS-E6-04 | A2A Talent Intelligence agent (stretch) | 5 | To do |
| TS-E6-05 | Demo deployment | 3 | To do |
| TS-E6-07 | Performance and resilience testing | 3 | To do |
| TS-E6-06 | Recruiter pilot and results report | 3 | To do |

Holiday break: 2026-12-25 → 2027-01-01 (no sprint).
