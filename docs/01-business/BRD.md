# Business Requirements Document (BRD)

| Item | Value |
|---|---|
| Product | TalentScout: Agentic AI Recruitment Command Centre (for HR Guru) |
| Version | 0.3 (scope change 2026-11-28: quality and trust layer over the ATS) |
| Sponsor | HR Guru Director |
| Author | Product Owner |
| Date | 2026-11-28 |

## 1. Business background

HR Guru provides recruitment and resource augmentation services to multiple enterprise clients, with about 40 recruitment professionals, **25 of whom are the MVP users**. Recruiters work in the HR Guru ATS, which is the **system of record for candidates submitted against particular roles and skills**. Sourcers screen candidates themselves (mostly from Naukri) and then upload them into the ATS against a requirement. The process relies heavily on manual work and individual recruiter experience, and nobody systematically checks the quality or truthfulness of what is submitted.

Agentic AI can improve recruiter productivity, candidate quality and delivery efficiency. Details are in [requirements gathering](../00-discovery/requirements-gathering.md).

## 2. Business problems

| Problem | Business impact |
|---|---|
| Incorrect understanding of JD | Irrelevant submissions |
| Manual candidate sourcing | High recruiter effort |
| Dependency on recruiter experience | Inconsistent quality |
| Repetitive resume screening | Reduced productivity |
| Delayed client feedback | Repeated mistakes |
| Limited intelligence on talent availability | Longer closure timelines |
| Quantity-driven submissions | Lower conversion ratios |
| Manual delivery monitoring | Reactive management |
| No independent check of submitted candidates | Weak or mismatched CVs reach clients; recruiter-entered details (CTC, notice, experience) are wrong |
| Possible false submissions (candidate never contacted, or contacted for another role) | Inflated recruiter numbers, client embarrassment, wasted interviews |
| The ATS pool is not reused | Every new requirement and client pitch starts from zero on Naukri |

## 3. Proposed solution

A goal-driven AI platform that acts as a **quality and trust layer over the ATS**, planning and executing checks **within approved boundaries**. Leads and recruiters remain responsible for every decision. Use cases, in priority order (PO decision, 2026-11-28):

1. [UC-002: Submission Quality Audit](../00-discovery/UC-002-submission-quality-audit.md): check every submitted candidate against the requirement and their own CV.
2. [UC-003: Candidate Verification](../00-discovery/UC-003-candidate-verification.md): confirm with the candidate, by WhatsApp and email, that they were approached for the right role and that the details are correct.
3. [UC-004: Client Pitches and Drives](../00-discovery/UC-004-client-pitches-and-drives.md): reuse the audited and verified ATS pool for client pitches and hiring drives. It builds on [UC-001: Intelligent Candidate Sourcing](../00-discovery/UC-001-intelligent-candidate-sourcing.md), which remains the reference scenario for search and replanning.

## 4. Business success criteria (KPIs)

These are initial proposed targets. **Actual baselines are established before improvements are measured** (TS-E0-08).

| ID | KPI | Target |
|---|---|---|
| KPI-1 | Manual sourcing effort reduction | 40% |
| KPI-2 | Evidence accuracy | 95%+ |
| KPI-3 | Recruiter acceptance of suggested profiles | 80%+ |
| KPI-4 | Successful agent workflow completion | 90%+ |
| KPI-5 | Unauthorised external actions | Zero |
| KPI-6 | Agent execution traceability | 100% |
| KPI-7 | Submissions audited within 1 hour of upload | 95%+ |
| KPI-8 | Audit flags confirmed by leads (audit precision) | 80%+ |
| KPI-9 | Verification response rate (WhatsApp + email) | 40%+ |
| KPI-10 | False-submission rate (`not_contacted` + `wrong_role` among verified) | Measured; reduce quarter on quarter |
| KPI-11 | Pitch profiles drawn from the ATS pool instead of fresh sourcing | Baseline first |

KPI-1 and KPI-3 now apply mainly to pool reuse (UC-004); KPI-7–9 are the primary MVP measures.

Operational constraint (not a KPI): monthly cash spend during the MVP is $0.

## 5. MVP scope

The first release is kept small but architecturally extensible.

| Capability | MVP scope |
|---|---|
| JD parsing | Included (reuse existing component, subject to code review) |
| Resume parsing | Included (reuse existing component, subject to code review) |
| Requirement analysis agent | Included |
| Supervisor agent | Included |
| Sourcing agent | Included |
| Evidence-based candidate matching | Included |
| Intelligent search and replanning | Included |
| Agent execution dashboard | Included |
| Human approval workflow | Included |
| Agent memory | Included |
| Submission quality audit (UC-002) | **Included, priority 1** |
| Candidate verification by WhatsApp and email (UC-003) | **Included, priority 2**; messages are approved by a lead before sending |
| Client pitches and hiring drives from the ATS pool (UC-004) | **Included, priority 3** |
| Recruiter quality scorecard | Included |
| AI guardrails | Included |
| Observability and evaluation | Included |
| Automated candidate outreach (marketing, job offers) | Future phase. Only approved verification messages are in scope |
| Voice-based candidate screening | Future phase |
| HR Guru ATS | **Included:** restored to run locally; read-only source of candidates, CVs and requirements. Write-back is future |
| Naukri | No profile API is available. Recruiters source on Naukri and upload candidates and CVs into the ATS, which TalentScout reads |
| Delivery monitoring agent | Future phase |
| Autonomous hiring decisions | **Excluded** |

Also out of scope: modifying the existing recruitment platform, scraping unlicensed sources, fine-tuning models, and multi-tenant SaaS.

## 6. Business rules

| ID | Rule |
|---|---|
| BR-1 | Agents may **recommend** candidates. Only a human can **reject** a candidate or make a hiring decision. |
| BR-2 | Agents cannot relax budget, mandatory skills, experience, location or notice period. They may **propose** a relaxation, and a recruiter decides. |
| BR-3 | Protected attributes (gender, age, religion, caste, marital status, photo) are never screening criteria and are masked before LLM calls. |
| BR-4 | Real candidate PII is processed only by models on HR Guru-controlled hardware. |
| BR-5 | Every action with an external or irreversible effect needs explicit approval from a named user. In the MVP the only candidate contact is approved verification messages (UC-003, ADR-0008); there is no client contact by the system. |
| BR-6 | Candidate data is retained only per the retention policy. Candidates can ask for erasure. |
| BR-7 | Every claim that a candidate meets a requirement must cite resume evidence. |
| BR-8 | When the objective cannot be met within the rules, the agent **escalates** to the recruiter with an explanation instead of lowering the bar. |
| BR-9 | Audit scores and scorecards inform review and coaching only. No automatic action is taken against a recruiter. |
| BR-10 | A candidate can opt out of messages at any time (`STOP`). Opt-outs apply to every channel and are checked before each send. |
| BR-11 | A verification result alone never proves a false submission. A lead reviews the evidence and decides. |
| BR-12 | Pitch packs are anonymised (no name, contact details, current employer or photo). Identity is shared only after the candidate re-confirms interest. |

## 7. Engineering principles (agreed)

1. One repository for TalentScout and the ATS (ADR-0006); the live ATS is only changed to restore and secure it, never by TalentScout at runtime.
2. Version-controlled engineering documentation.
3. Major architecture decisions are understood and recorded (ADRs) before implementation.
4. AI-generated code is reviewed before it is accepted.
5. Acceptance criteria are defined before development.
6. Security, testing and observability are in every sprint.
7. Synthetic or properly authorised candidate data only during development.
8. No unnecessary frameworks merely to demonstrate newer technology.

## 8. Assumptions, dependencies and constraints

See the [RAID log](../04-delivery/RAID-log.md).

## 9. Approval (Phase 1 gate)

| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | | | |
| Delivery Lead | | | |
| Product Owner | | | |
