# Business Requirements Document (BRD)

| Item | Value |
|---|---|
| Product | HR Guru: Agentic AI Recruitment Command Centre (codename TalentScout) |
| Version | 0.2 |
| Sponsor | HR Guru Director |
| Author | Product Owner |
| Date | 2026-11-27 |

## 1. Business background

HR Guru provides recruitment and resource augmentation services to multiple enterprise clients, with about 40 recruitment professionals. The process relies heavily on manual work, individual recruiter experience and repetitive decisions.

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

## 3. Proposed solution

A goal-driven AI platform that plans and executes recruitment tasks independently, **within approved boundaries**. Recruiters remain responsible for hiring decisions. The first business use case is [UC-001: Intelligent Candidate Sourcing](../00-discovery/UC-001-intelligent-candidate-sourcing.md).

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
| AI guardrails | Included |
| Observability and evaluation | Included |
| Automated candidate outreach | Future phase |
| Voice-based candidate screening | Future phase |
| Naukri API integration | Subject to authorised API access |
| ATS integration | Future phase |
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
| BR-5 | Every action with an external or irreversible effect needs explicit approval from a named user. The MVP has no candidate or client contact. |
| BR-6 | Candidate data is retained only per the retention policy. Candidates can ask for erasure. |
| BR-7 | Every claim that a candidate meets a requirement must cite resume evidence. |
| BR-8 | When the objective cannot be met within the rules, the agent **escalates** to the recruiter with an explanation instead of lowering the bar. |

## 7. Engineering principles (agreed)

1. Separate repository; the existing recruitment platform is not modified.
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
