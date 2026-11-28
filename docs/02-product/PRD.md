# Product Requirements Document (PRD)

| Item | Value |
|---|---|
| Product | TalentScout: Agentic AI Recruitment Command Centre (for HR Guru) |
| Version | 0.2 |
| Owner | Product Owner |
| Related | [BRD](../01-business/BRD.md), [FRD](FRD.md), [UC-001](../00-discovery/UC-001-intelligent-candidate-sourcing.md), [HLD](../03-architecture/HLD.md) |

## 1. Vision

> A goal-driven team of supervised AI agents. It turns a job requirement into an evidence-backed, recruiter-approved shortlist, adapts its strategy when results fall short, and escalates instead of lowering the bar.

## 2. Problem statement

Recruiters lose time to manual search strings, repetitive resume screening and late feedback. Quality depends on individual experience. Simple LLM matching tools rank resumes, but they don't plan, they don't adapt when the objective isn't met, and they can't be governed.

## 3. Target users

Recruiter (primary; MVP rollout to 25 recruiters), Delivery Lead (secondary), Admin (configuration and audit).

## 4. What makes it agentic (product principles)

1. **Goal-driven.** For example: "Find 5 AWS Cloud Architects with evidence for each mandatory skill". The supervisor builds the plan.
2. **Plan → act → observe → replan.** When the objective isn't met, the agent diagnoses the bottleneck (the UC-001 notice-period funnel) and changes strategy.
3. **Bounded.** It never relaxes hiring constraints (BR-2). It escalates with options instead (BR-8). Iteration, time, token and tool-scope limits apply.
4. **Evidence over opinion.** Each skill claim cites resume evidence (BR-7).
5. **Human in control.** Approval gates; no autonomous hiring decisions or candidate contact.
6. **Observable.** 100% of steps are traced (KPI-6).

## 5. Agents (MVP)

| Agent | Responsibility | Tools (via MCP) | Side effects |
|---|---|---|---|
| Supervisor | Understand objective, plan, delegate, observe, diagnose bottleneck, replan, escalate | routes to agents | None |
| Requirement | Parse JD (reused parser), extract skills and constraints, find ambiguities, write clarification questions | `jd.parse`, `requirement.get`, `requirement.update` | None |
| Sourcing | Formulate search strategies (including serving-notice and alternative titles), hybrid search, funnel counts | `candidates.search_hybrid`, `candidates.funnel`, `memory.search_feedback` | None |
| Screening | Validate each mandatory skill against parsed resume evidence | `candidates.get_resume_chunks`, `resume.parse` | None |
| Quality | Verify evidence, detect unsupported claims, check policy and bias | `evidence.verify`, `policy.check` | None |

**Input source:** the HR Guru ATS. Recruiters upload sourced candidates and CVs into it, including candidates found on Naukri (Naukri has no profile API). TalentScout reads the ATS read-only (ADR-0007).

**Future phase:** Outreach agent (automated candidate outreach), Delivery agent (delivery monitoring), voice screening, writing approved shortlists back to the ATS.

## 6. MVP features and priority (MoSCoW)

| ID | Feature | Priority | Sprint |
|---|---|---|---|
| F-00 | HR Guru ATS restored locally and used as the source of candidates, CVs and requirements (read-only connector) | Must | 0 (restore), 1 (stabilise), 2 (connector) |
| F-01 | Authentication and RBAC (Recruiter, Delivery Lead, Admin) | Must | 2 |
| F-02 | Requirement intake, JD parsing and analysis with clarification questions | Must | 2–3 |
| F-03 | Resume parsing and candidate store (synthetic data, embeddings, hybrid search) | Must | 3–4 |
| F-04 | Sourcing agent with funnel analysis | Must | 4 |
| F-05 | Multi-agent workflow: supervisor, replanning, escalation | Must | 5 |
| F-06 | Evidence-based candidate matching (Screening and Quality) | Must | 5 |
| F-07 | MCP server exposing recruitment tools | Must | 6 |
| F-08 | Durable execution (checkpointing, resume) | Must | 6 |
| F-09 | Agent memory: short-term state and long-term feedback | Must | 6 |
| F-10 | Human approval workflow | Must | 5 (basic), 7 (hardened) |
| F-11 | AI guardrails: PII masking, injection defence, tool scopes, limits | Must | 7 |
| F-12 | Observability (tracing) and audit trail | Must | 3 (audit), 7 (tracing) |
| F-13 | Evaluation suite and CI evaluation gate | Must | 7 |
| F-14 | Agent execution dashboard: live run view, run history, KPIs, cost | Must | 6 (live view), 8 (dashboard) |
| F-15 | Model routing (local / free cloud / fallback) | Should | 2 (v0), 8 (multi-provider) |
| F-16 | A2A: independently deployed Talent Intelligence agent | Could | 8 (stretch) |
| F-17 | Automated candidate outreach | Won't (future) | — |
| F-18 | Delivery monitoring agent | Won't (future) | — |
| F-19 | Voice screening; ATS write-back; Naukri API (not available) | Won't (future) | — |

## 7. Key user journeys

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
| Supporting: hallucination rate | Unsupported claims reaching the recruiter | ≤ 3% |
| Supporting: p95 run latency | Requirement → shortlist on the local setup | ≤ 5 min |
| Supporting: cost per requirement | Notional $ at list price (actual $0) | Tracked |

## 9. Delivery phases and releases

| Phase | Content | Sprint(s) | Gate |
|---|---|---|---|
| 1 Discovery and requirements | Business problem, BRD, FRD, PRD, success criteria, UC-001 | 0 | BRD/PRD sign-off |
| 2 Solution and architecture | HLD, LLD (Sprint 1 scope), technology selection, data flow, ADRs | 0 | Architecture sign-off |
| 3 Engineering planning | Epics, stories, acceptance criteria, estimates, sprint backlog | 0 | Backlog ready (DoR) |
| 4 Incremental development | ATS restore and stabilisation → connector → agent fundamentals → RAG → LangGraph → MCP, memory → A2A | 0–6, 8 | Sprint reviews |
| 5 AI engineering and governance | Guardrails, evaluations, observability, security, failure handling | 7 (and every sprint) | Governance review |
| 6 Deployment and pilot | CI/CD (from Sprint 0), ATS hosting (Sprint 0), performance testing, recruiter feedback | 8 | Pilot report |

Sprint 0 contains **no TalentScout feature code**. It sets up the repository, CI/CD and security scanning, and restores the live ATS that recruiters depend on.

## 10. Open questions

See [requirements gathering §7](../00-discovery/requirements-gathering.md#7-discovery-questions).
