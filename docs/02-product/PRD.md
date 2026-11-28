# Product Requirements Document (PRD)

| Item | Value |
|---|---|
| Product | TalentScout: Agentic AI Recruitment Command Centre (for HR Guru) |
| Version | 0.3 (scope change 2026-11-28) |
| Owner | Product Owner |
| Related | [BRD](../01-business/BRD.md), [FRD](FRD.md), [UC-002](../00-discovery/UC-002-submission-quality-audit.md), [UC-003](../00-discovery/UC-003-candidate-verification.md), [UC-004](../00-discovery/UC-004-client-pitches-and-drives.md), [UC-001](../00-discovery/UC-001-intelligent-candidate-sourcing.md), [HLD](../03-architecture/HLD.md) |

## 1. Vision

> A goal-driven team of supervised AI agents that acts as the **quality and trust layer over the HR Guru ATS**. It audits every submitted candidate against the requirement and their CV, verifies with the candidate that the submission is genuine, and turns the trusted pool into client pitches. It adapts when results fall short and escalates instead of lowering the bar.

## 2. Problem statement

Sourcers screen candidates themselves and upload them into the ATS, but nobody checks that work systematically: weak or mismatched CVs reach clients, recruiter-entered details are often wrong, and some submissions may be false (the candidate was never contacted, or was contacted for another role). The growing ATS pool is not reused for new requirements or client pitches. Quality depends on individual experience. Simple LLM matching tools rank resumes, but they don't plan, they don't adapt when the objective isn't met, and they can't be governed.

## 3. Target users

Delivery Lead / Quality reviewer (primary for UC-002 and UC-003), Recruiter / Sourcer (sees own scorecard and flags; MVP rollout to 25 recruiters), Business development (UC-004 pitches), Admin (configuration and audit).

## 4. What makes it agentic (product principles)

1. **Goal-driven.** For example: "Find 5 AWS Cloud Architects with evidence for each mandatory skill". The supervisor builds the plan.
2. **Plan → act → observe → replan.** When the objective isn't met, the agent diagnoses the bottleneck (the UC-001 notice-period funnel) and changes strategy.
3. **Bounded.** It never relaxes hiring constraints (BR-2). It escalates with options instead (BR-8). Iteration, time, token and tool-scope limits apply.
4. **Evidence over opinion.** Each skill claim cites resume evidence (BR-7).
5. **Human in control.** Approval gates; no autonomous hiring decisions; candidates are contacted only with approved verification messages (ADR-0008); no automatic action against recruiters.
6. **Observable.** 100% of steps are traced (KPI-6).

## 5. Agents (MVP)

| Agent | Responsibility | Tools (via MCP) | Side effects |
|---|---|---|---|
| Supervisor | Understand objective, plan, delegate, observe, diagnose bottleneck, replan, escalate | routes to agents | None |
| Requirement | Parse JD (reused parser), extract skills and constraints, find ambiguities, write clarification questions | `jd.parse`, `requirement.get`, `requirement.update` | None |
| Sourcing | Formulate search strategies (including serving-notice and alternative titles), hybrid search, funnel counts | `candidates.search_hybrid`, `candidates.funnel`, `memory.search_feedback` | None |
| Screening | Validate each mandatory skill against parsed resume evidence | `candidates.get_resume_chunks`, `resume.parse` | None |
| Quality | Verify evidence, detect unsupported claims, check policy and bias; detail-accuracy and duplicate checks for the audit | `evidence.verify`, `policy.check`, `submission.compare`, `candidates.find_duplicates` | None |
| Verification | Draft verification messages, send approved ones, read replies, classify them locally, compare with recruiter entries, follow up, escalate | `message.draft`, `message.send` (approval token required), `message.replies`, `submission.compare` | **Sends messages, only with an approval token** |
| Pitch | Plan pool searches for a pitch brief, rank by audit and verification status, write anonymised profiles and drive summaries | `candidates.search_hybrid`, `candidates.funnel`, `pitch.anonymise`, `pitch.export` | Export, with approval |

**How the agents combine per use case:** UC-002 audit = Supervisor → Requirement → Screening → Quality. UC-003 verification = Supervisor → Verification (with approval and reply-wait interrupts). UC-004 pitches = Supervisor → Sourcing → Screening → Pitch.

**Input source:** the HR Guru ATS. Recruiters upload sourced candidates and CVs into it, including candidates found on Naukri (Naukri has no profile API). TalentScout reads the ATS read-only (ADR-0007).

**Future phase:** marketing or job-offer outreach, Delivery agent (delivery monitoring), voice screening, writing results back to the ATS.

## 6. MVP features and priority (MoSCoW)

| ID | Feature | Priority | Sprint |
|---|---|---|---|
| F-00 | HR Guru ATS restored locally and used as the source of candidates, CVs and requirements (read-only connector) | Must | 0 (restore), 1 (stabilise), 2 (connector) |
| F-01 | Authentication and RBAC (Recruiter, Delivery Lead, Admin) | Must | 2 |
| F-02 | Requirement intake, JD parsing and analysis with clarification questions | Must | 2–3 |
| F-03 | Resume parsing and candidate store (synthetic data, embeddings, hybrid search) | Must | 3, 8 |
| F-04 | Sourcing agent with funnel analysis (used for pool reuse and pitches) | Must | 8 |
| F-05 | Multi-agent workflow: supervisor (4), replanning and escalation (8) | Must | 4, 8 |
| F-06 | Evidence-based candidate matching (Screening and Quality), used by the audit | Must | 4–5 |
| F-07 | MCP server exposing recruitment tools | Must | 6 |
| F-08 | Durable execution (checkpointing, resume) | Must | 6 |
| F-09 | Agent memory: short-term state and long-term feedback | Must | 6 |
| F-10 | Human approval workflow | Must | 5 (basic), 6 (approval token, re-auth) |
| F-11 | AI guardrails: PII masking, injection defence, tool scopes, limits | Must | 5–8 |
| F-12 | Observability (tracing) and audit trail | Must | 3 (audit events), 8 (tracing), 9 (tamper-evident) |
| F-13 | Evaluation suite and CI evaluation gate | Must | 5, 7 (audit and reply sets), 9 (gate) |
| F-14 | Agent execution dashboard: live run view, run history, KPIs, cost | Must | 5 (live view), 10 (dashboard) |
| F-15 | Model routing (local / free cloud / fallback) | Should | 2 (v0), 9 (multi-provider) |
| F-16 | A2A: independently deployed Talent Intelligence agent | Could | 10 (stretch) |
| F-20 | **Submission quality audit** (UC-002): must-have fit, detail accuracy, constraint fit, duplicates, completeness, score | Must | 4 |
| F-21 | **Recruiter quality scorecard** and lead review queue | Must | 4 |
| F-22 | **Candidate verification** (UC-003) by WhatsApp and email, approved messages, reply classification, follow-up, escalation | Must | 5 (channels), 7 |
| F-23 | Opt-out and consent handling across channels | Must | 5 |
| F-24 | **Client pitch packs and drive summaries** (UC-004), anonymised | Should | 9 |
| F-17 | Automated marketing or job-offer outreach | Won't (future) | — |
| F-18 | Delivery monitoring agent | Won't (future) | — |
| F-19 | Voice screening; ATS write-back; Naukri API (not available) | Won't (future) | — |

## 7. Key user journeys

**J0a — Audit queue (UC-002).** A lead opens the audit queue: each flagged submission shows the score, the failed checks with CV quotes, and the recruiter's entry next to the CV fact. The lead accepts or overrides each flag; the recruiter scorecard updates.

**J0b — Verify a batch (UC-003).** A lead picks the weekly sample, reviews the drafted WhatsApp and email messages, approves the batch, and later reviews outcomes: confirmed, details mismatch, wrong role, not contacted, no response.

**J0c — Build a pitch (UC-004).** Business development enters a brief and gets an anonymised pitch pack ranked by verified, clean candidates, or an escalation if the pool is short.

**J1 — Create requirement → analysis.** The recruiter enters the UC-001 requirement. The Requirement agent returns structured skills and constraints with clarification questions. The recruiter answers them.

**J2 — Run sourcing → replan → shortlist or escalation.** The recruiter starts a run. The live view shows the plan, searches, the funnel, the diagnosed bottleneck and the replans. It ends with either a shortlist with evidence for each mandatory skill, or an escalation that explains the shortfall and offers options.

**J3 — Approve.** The recruiter approves or rejects each candidate with a reason. Reasons are stored as long-term memory.

**J4 — Agent execution dashboard.** The Delivery Lead or Admin sees:
- runs and their status;
- completion rate, acceptance rate and evidence accuracy;
- latency, tokens and notional cost;
- a link from every run to its full trace.

## 8. Success metrics

| Metric | Definition | Target |
|---|---|---|
| Manual sourcing effort reduction (KPI-1) | Recruiter minutes per requirement vs baseline | 40% |
| Evidence accuracy (KPI-2) | Skill claims verified against source text | 95%+ |
| Recruiter acceptance (KPI-3) | Suggested profiles approved by the recruiter | 80%+ |
| Workflow completion (KPI-4) | Runs ending `completed` or `escalated` (with explanation) rather than `failed` | 90%+ |
| Unauthorised external actions (KPI-5) | Side-effecting tool calls without an approval record | 0 |
| Traceability (KPI-6) | Runs whose every step, tool call and decision is in the audit trail | 100% |
| Audit coverage (KPI-7) | Submissions audited within 1 h of upload | 95%+ |
| Audit precision (KPI-8) | Flags confirmed by leads | 80%+ |
| Verification response rate (KPI-9) | Candidates replying on WhatsApp or email | 40%+ |
| False-submission rate (KPI-10) | `not_contacted` + `wrong_role` among verified | Measured, then reduced |
| Pool reuse (KPI-11) | Pitch profiles from the ATS pool | Baseline first |
| Supporting: hallucination rate | Unsupported claims reaching the recruiter | ≤ 3% |
| Supporting: p95 run latency | Requirement → shortlist on the local setup | ≤ 5 min |
| Supporting: cost per requirement | Notional $ at list price (actual $0) | Tracked |

## 9. Delivery phases and releases

| Phase | Content | Sprint(s) | Gate |
|---|---|---|---|
| 1 Discovery and requirements | Business problem, BRD, FRD, PRD, success criteria, UC-001 | 0 | BRD/PRD sign-off |
| 2 Solution and architecture | HLD, LLD (Sprint 1 scope), technology selection, data flow, ADRs | 0 | Architecture sign-off |
| 3 Engineering planning | Epics, stories, acceptance criteria, estimates, sprint backlog | 0 | Backlog ready (DoR) |
| 4 Incremental development | ATS restore and stabilisation → connector → agent fundamentals → **submission audit** → LangGraph → MCP, memory → **verification** → retrieval and **pitches** → A2A | 0–10 | Sprint reviews |
| 5 AI engineering and governance | Guardrails, evaluations, observability, security, failure handling | 5–9 (and every sprint) | Governance review |
| 6 Deployment and pilot | CI/CD (from Sprint 0), ATS hosting (Sprint 0), performance testing, recruiter feedback | 10 | Pilot report |

Sprint 0 contains **no TalentScout feature code**. It sets up the repository, CI/CD and security scanning, and restores the live ATS that recruiters depend on.

## 10. Open questions

See [requirements gathering §7](../00-discovery/requirements-gathering.md#7-discovery-questions).
