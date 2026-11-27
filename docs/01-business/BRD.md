# Business Requirements Document (BRD)

| Item | Value |
|---|---|
| Product | TalentScout: Agentic Recruitment Command Centre |
| Version | 0.1 (Sprint 0 draft) |
| Sponsor | HR Guru Director |
| Author | Product Owner |
| Date | 2026-11-27 |

## 1. Business problem

Recruiters at HR Guru spend most of their time on low-value search and verification work. As a result:
- time to first submission is slow;
- client rejection rates are high when profiles don't actually meet mandatory constraints (notice period, budget, core skills);
- ageing requirements are spotted late.

Keyword search over the candidate database returns noisy results. There is also no record of *why* a candidate was proposed.

## 2. Business objectives

| ID | Objective | Measure | Target (pilot hypothesis, to validate) |
|---|---|---|---|
| BO-1 | Reduce manual sourcing effort | Recruiter minutes per requirement, sourcing phase | −40% |
| BO-2 | Improve submission quality | Share of shortlisted candidates the recruiter accepts | ≥ 70% |
| BO-3 | Make every recommendation explainable | Share of screening claims backed by evidence from the resume | ≥ 95% |
| BO-4 | Operate safely | Unauthorised external actions | **0** (control objective) |
| BO-5 | Run at zero cash cost | Monthly cash spend during the MVP | $0 |
| BO-6 | Detect delivery risk early | Ageing requirements flagged before SLA breach | ≥ 80% |

These are **targets for a controlled pilot, not claimed results.** The baseline is measured in Sprint 1 (story TS-E0-08).

## 3. Scope

### In scope (MVP)
1. Requirement intake with AI analysis of the JD: mandatory and optional skills, constraints, ambiguities, clarification questions.
2. Agentic sourcing over HR Guru's own candidate store using hybrid search (semantic plus keyword), with replanning when results are weak.
3. Evidence-based screening reports, where each claim links to a resume excerpt.
4. A Quality agent that checks evidence, flags unsupported claims and checks policy.
5. Human approval gates for shortlists and outreach.
6. Draft outreach messages. Sending is simulated or manual in the MVP.
7. Recruiter feedback captured into long-term memory to improve later search plans.
8. A delivery dashboard covering requirement ageing and bottlenecks, with recommended actions.
9. An audit trail of every agent decision and tool call.
10. Synthetic dataset, evaluation suite, CI/CD, security scanning.

### Out of scope (MVP)
- Replacing the existing ATS, payroll or onboarding systems.
- Scraping LinkedIn or any unlicensed source.
- Autonomous rejection of candidates, or autonomous sending of emails or WhatsApp messages.
- Fine-tuning models.
- Mobile apps, and multi-tenant SaaS billing.

## 4. Business rules

| ID | Rule |
|---|---|
| BR-1 | A candidate may be **recommended** by an agent but only **rejected** by a human. |
| BR-2 | Mandatory constraints (for example notice ≤ 30 days, budget ≤ ₹45 LPA) are never relaxed by an agent. Only optional criteria can be relaxed during replanning, and every relaxation is logged. |
| BR-3 | Protected attributes (gender, age, religion, caste, marital status, photo) are never used as screening criteria and are masked before LLM calls. |
| BR-4 | Real candidate PII is processed only by models running on HR Guru-controlled hardware. |
| BR-5 | Every external action (message send, client submission) needs an explicit approval from a named user. |
| BR-6 | Candidate data is kept only as long as the retention policy allows. Candidates can ask to be deleted. |

## 5. Assumptions, dependencies and constraints

See `docs/04-delivery/RAID-log.md`. The key constraints are a zero cash budget, a single developer working with AI coding assistants, and free-tier rate limits.

## 6. Benefits (qualitative)

- Recruiters spend their time talking to candidates and clients instead of searching.
- Clients receive fewer, better submissions with clear evidence behind them.
- The Director gets a governed, auditable way to adopt AI.
- It becomes a reusable HR asset that HR Guru can offer to other clients.

## 7. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | | | |
| Delivery Lead | | | |
| Product Owner | | | |
