# Sprint Plan

_Generated from `backlog.json`. Two-week sprints; planned velocity 26 points (recalibrated after Sprints 0 and 1)._

| Sprint | Dates | Goal | Points | Load |
|---|---|---|---|---|
| 0 | 2026-11-30 → 2026-12-11 | Documents baselined, backlog ready, CI/CD and security scanning live, and the HR Guru ATS running locally again for recruiters with backups and alerts. | 39 | +13 over (stretch items flagged in planning) |
| 1 | 2026-12-14 → 2026-12-24 | The live ATS is secure, fast and complete: security hardening, background bulk uploads, a measured performance baseline and the scheduled reports restored; local model chosen and recruiter baseline measured. | 28 | +2 over (stretch items flagged in planning) |
| 2 | 2027-01-04 → 2027-01-15 | TalentScout has auth, requirements, the PII-aware model router and the Requirement agent, and reads candidates, CVs and requirements read-only from the ATS. | 25 | OK |
| 3 | 2027-01-18 → 2027-01-29 | The Requirement agent is evaluated on golden JDs with clarification questions and audit; resumes are parsed and the UC-001 synthetic dataset exists. | 23 | OK |
| 4 | 2027-02-01 → 2027-02-12 | Every new ATS submission is audited within 1 hour: must-have evidence, detail accuracy, constraint fit, duplicates and completeness, with a quality score, a lead review queue and recruiter scorecards. | 29 | +3 over (stretch items flagged in planning) |
| 5 | 2027-02-15 → 2027-02-26 | Audit flags are evidence-checked and approved by leads, audit precision is measured on a golden set, and the WhatsApp relay and opt-out registry are ready for verification. | 28 | +2 over (stretch items flagged in planning) |
| 6 | 2027-03-01 → 2027-03-12 | Agents use tools only through the MCP server with per-agent scopes; runs survive restarts; side-effecting tools need an approval token and step-up re-authentication. | 30 | +4 over (stretch items flagged in planning) |
| 7 | 2027-03-15 → 2027-03-26 | Leads approve verification batches; WhatsApp and email messages go out within rate limits; replies are classified locally and compared with recruiter entries; follow-ups and escalations work; DPDP pack ready for sign-off. | 29 | +3 over (stretch items flagged in planning) |
| 8 | 2027-03-29 → 2027-04-09 | Hybrid search over the ATS pool beats keyword search; the UC-001 replan and escalation works end to end; prompt-injection defence and tracing are in place. | 30 | +4 over (stretch items flagged in planning) |
| 9 | 2027-04-12 → 2027-04-23 | Anonymised pitch packs and drive summaries are built from audited, verified candidates; evaluation gate in CI; tamper-evident audit trail; LiteLLM routing. | 29 | +3 over (stretch items flagged in planning) |
| 10 | 2027-04-26 → 2027-05-07 | Agent execution dashboard with audit, verification and pitch KPIs; performance targets met; 2-week recruiter pilot report against the baseline. | 19 | OK |
| None | - → - | Deferred items; re-planned when the PO brings them back. | 2 | - |

## Sprint 0 - Inception, walking skeleton and ATS restore

**Dates:** 2026-11-30 → 2026-12-11  
**Goal:** Documents baselined, backlog ready, CI/CD and security scanning live, and the HR Guru ATS running locally again for recruiters with backups and alerts.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-EA-01 | Import ATS into the monorepo | 2 | Done |
| TS-EA-02 | Make the ATS run locally on macOS | 3 | Done |
| TS-EA-03 | Patch vulnerable ATS dependencies | 2 | Done |
| TS-EA-04 | Recover production ATS data | 3 | Done |
| TS-EA-05 | Expose the local ATS to 25 recruiters securely | 3 | Done |
| TS-EA-06 | ATS backups and restore drill | 3 | Done |
| TS-EA-09 | ATS health monitoring | 2 | Done |
| TS-EA-11 | ATS performance quick wins: PostgreSQL indexes and multi-process serving | 3 | Done |
| TS-E0-01 | Monorepo structure and tooling | 2 | Done |
| TS-E0-02 | CI pipeline: lint, test, build | 3 | Done |
| TS-E0-03 | Security scanning pipeline | 3 | Done |
| TS-E0-04 | CD pipeline to GHCR and demo host | 3 | Done |
| TS-E0-05 | Docker Compose local stack | 2 | In progress |
| TS-E0-07 | Free-tier accounts and secrets handling | 2 | To do |
| TS-E0-09 | Agile artefacts in Jira | 3 | Done |

## Sprint 1 - ATS stabilisation

**Dates:** 2026-12-14 → 2026-12-24  
**Goal:** The live ATS is secure, fast and complete: security hardening, background bulk uploads, a measured performance baseline and the scheduled reports restored; local model chosen and recruiter baseline measured.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-EA-07 | ATS security hardening baseline | 5 | Done |
| TS-EA-12 | Asynchronous bulk upload with progress | 8 | To do |
| TS-EA-13 | ATS performance baseline and load test | 3 | To do |
| TS-EA-14 | Restore scheduled WhatsApp/email reports on the Mac | 3 | To do |
| TS-EA-15 | Delete the retired AI screening code from the ATS | 3 | To do |
| TS-E0-06 | Spike: local model selection on M2 16 GB | 3 | To do |
| TS-E0-08 | Baseline measurement plan | 3 | To do |

## Sprint 2 - Product foundation and ATS connector

**Dates:** 2027-01-04 → 2027-01-15  
**Goal:** TalentScout has auth, requirements, the PII-aware model router and the Requirement agent, and reads candidates, CVs and requirements read-only from the ATS.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-EA-08 | Read-only ATS connector | 5 | To do |
| TS-E1-01 | Requirement CRUD API and UI | 5 | To do |
| TS-E1-02 | Authentication and RBAC | 5 | To do |
| TS-E1-03 | LLM router v0 with PII flag | 3 | To do |
| TS-E1-04 | Requirement agent with structured output and repair loop | 5 | To do |
| TS-E1-08 | Review ATS JD and CV parsers and decide reuse | 2 | To do |

## Sprint 3 - Single-agent completion and data

**Dates:** 2027-01-18 → 2027-01-29  
**Goal:** The Requirement agent is evaluated on golden JDs with clarification questions and audit; resumes are parsed and the UC-001 synthetic dataset exists.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E1-05 | Clarification questions UI | 3 | To do |
| TS-E1-06 | Audit events v0 | 2 | To do |
| TS-E1-07 | Golden JD dataset and test | 3 | To do |
| TS-E2-01 | Synthetic candidate generator incl. UC-001 scenario set | 5 | To do |
| TS-E2-07 | Resume parsing of ATS CVs | 3 | To do |
| TS-E2-02 | Chunking, masking and embedding pipeline | 5 | To do |
| TS-E2-03 | Atlas vector and text indexes | 2 | To do |

## Sprint 4 - Submission quality audit (UC-002)

**Dates:** 2027-02-01 → 2027-02-12  
**Goal:** Every new ATS submission is audited within 1 hour: must-have evidence, detail accuracy, constraint fit, duplicates and completeness, with a quality score, a lead review queue and recruiter scorecards.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E3-01 | LangGraph supervisor graph and state | 5 | To do |
| TS-E3-03 | Evidence-based matching per mandatory skill | 5 | To do |
| TS-E7-01 | Detail-accuracy check: recruiter entries vs CV | 5 | To do |
| TS-E7-02 | Constraint fit, completeness and quality score | 3 | To do |
| TS-E7-03 | Duplicate detection across recruiters | 3 | To do |
| TS-E7-04 | Audit records and automatic audit on sync | 3 | To do |
| TS-E7-05 | Lead review queue and recruiter scorecard | 5 | To do |

## Sprint 5 - Audit quality and verification groundwork

**Dates:** 2027-02-15 → 2027-02-26  
**Goal:** Audit flags are evidence-checked and approved by leads, audit precision is measured on a golden set, and the WhatsApp relay and opt-out registry are ready for verification.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E3-04 | Quality agent evidence verification | 5 | To do |
| TS-E3-05 | Live run view over SSE (dashboard part 1) | 3 | To do |
| TS-E3-06 | Human approval gate for shortlist and escalation | 6 | To do |
| TS-E5-02 | PII masking and local-only routing enforcement | 3 | To do |
| TS-E7-06 | Golden audit dataset and precision evaluation | 3 | To do |
| TS-E8-01 | Harden the WhatsApp relay and add inbound messages | 5 | To do |
| TS-E8-02 | Opt-out and contact-consent registry | 3 | To do |

## Sprint 6 - MCP, memory, durable execution and approval controls

**Dates:** 2027-03-01 → 2027-03-12  
**Goal:** Agents use tools only through the MCP server with per-agent scopes; runs survive restarts; side-effecting tools need an approval token and step-up re-authentication.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E4-01 | MCP server with recruitment tools | 5 | To do |
| TS-E4-02 | Agents consume tools via MCP client | 3 | To do |
| TS-E4-03 | Per-agent tool scopes | 3 | To do |
| TS-E4-04 | Durable execution with MongoDB checkpointer | 5 | To do |
| TS-E4-05 | Long-term feedback memory | 5 | To do |
| TS-E5-04 | Loop, time and token limits | 3 | To do |
| TS-E5-05 | Approval-token gate on side-effecting tools | 3 | To do |
| TS-E5-06 | Step-up re-authentication for approvals | 3 | To do |

## Sprint 7 - Candidate verification (UC-003)

**Dates:** 2027-03-15 → 2027-03-26  
**Goal:** Leads approve verification batches; WhatsApp and email messages go out within rate limits; replies are classified locally and compared with recruiter entries; follow-ups and escalations work; DPDP pack ready for sign-off.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E5-10 | DPDP compliance pack | 3 | To do |
| TS-E8-03 | Verification batches, templates and drafting | 5 | To do |
| TS-E8-04 | message.send tool with approval token, rate limits and email fallback | 5 | To do |
| TS-E8-05 | Reply capture from WhatsApp and email | 3 | To do |
| TS-E8-06 | Local reply classification and outcome comparison | 5 | To do |
| TS-E8-07 | Follow-up replanning, escalation and results view | 5 | To do |
| TS-E8-08 | Verification evaluation set | 3 | To do |

## Sprint 8 - Pool retrieval, replanning and AI safety

**Dates:** 2027-03-29 → 2027-04-09  
**Goal:** Hybrid search over the ATS pool beats keyword search; the UC-001 replan and escalation works end to end; prompt-injection defence and tracing are in place.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E2-04 | Hybrid search with RRF and filters | 5 | To do |
| TS-E2-05 | Sourcing agent with tool calling | 5 | To do |
| TS-E2-06 | Retrieval evaluation: hybrid vs keyword | 4 | To do |
| TS-E3-02 | Bottleneck diagnosis, replanning and escalation (UC-001) | 8 | To do |
| TS-E5-01 | Prompt-injection defence for untrusted content | 5 | To do |
| TS-E5-03 | Langfuse tracing and prompt versioning | 3 | To do |

## Sprint 9 - Client pitches and drives (UC-004) and LLMOps

**Dates:** 2027-04-12 → 2027-04-23  
**Goal:** Anonymised pitch packs and drive summaries are built from audited, verified candidates; evaluation gate in CI; tamper-evident audit trail; LiteLLM routing.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E5-07 | Tamper-evident audit trail | 3 | To do |
| TS-E5-08 | Evaluation gate in CI | 5 | To do |
| TS-E6-01 | LiteLLM gateway with multi-provider fallback | 5 | To do |
| TS-E6-02 | Parallel screening fan-out | 3 | To do |
| TS-E9-01 | Pitch brief and trust-ranked pool search | 3 | To do |
| TS-E9-02 | Anonymised pitch pack export | 5 | To do |
| TS-E9-03 | Hiring-drive pool summary | 3 | To do |
| TS-E9-04 | Anonymisation leak test | 2 | To do |

## Sprint 10 - Dashboard, performance and pilot

**Dates:** 2027-04-26 → 2027-05-07  
**Goal:** Agent execution dashboard with audit, verification and pitch KPIs; performance targets met; 2-week recruiter pilot report against the baseline.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-E6-03 | Agent execution dashboard (dashboard part 2) | 5 | To do |
| TS-E6-04 | A2A Talent Intelligence agent (stretch) | 5 | To do |
| TS-E6-05 | Demo deployment | 3 | To do |
| TS-E6-07 | Performance and resilience testing | 3 | To do |
| TS-E6-06 | Recruiter pilot and results report | 3 | To do |

## Unscheduled (deferred)

**Dates:** - → -  
**Goal:** Deferred items; re-planned when the PO brings them back.

| Story | Title | Points | Status |
|---|---|---|---|
| TS-EA-10 | Close the post-May 2026 data gap and the missing CV/JD files | 2 | Deferred |

Holiday break: 2026-12-25 → 2027-01-01 (no sprint).
