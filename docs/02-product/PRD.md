# Product Requirements Document (PRD)

| Item | Value |
|---|---|
| Product | TalentScout: Agentic Recruitment Command Centre |
| Version | 0.1 |
| Owner | Product Owner |
| Related | [BRD](../01-business/BRD.md), [FRD](FRD.md), [HLD](../03-architecture/HLD.md) |

## 1. Vision

> A virtual recruitment team of supervised AI agents. It turns a job requirement into an evidence-backed, recruiter-approved shortlist and outreach plan, and gets better with every piece of feedback.

## 2. Problem statement

Recruiters lose hours to keyword searches and resume reading, and nothing records *why* a profile was proposed. Simple LLM matching tools rank resumes, but they don't plan, they don't adapt when results are weak, and they can't be governed.

## 3. Target users

Recruiter (primary), Delivery Lead (secondary), Admin (configuration and audit). See the personas in [requirements-gathering](../00-discovery/requirements-gathering.md).

## 4. What makes it agentic (product principles)

1. **Goal-driven.** The user states the goal: "Fill AWS Cloud Architect, ₹45 LPA, notice ≤ 30 days". The supervisor builds the plan.
2. **Plan → act → observe → replan.** If results violate constraints, for example most candidates have 60–90 day notice periods, the supervisor changes strategy (alternative titles, immediate joiners). It never relaxes mandatory constraints.
3. **Evidence over opinion.** Every claim cites the resume excerpt it is based on.
4. **Human in control.** Approval gates exist before anything leaves the system.
5. **Bounded.** Iteration limits, token budgets, tool permissions and timeouts apply.
6. **Observable.** Every step is traced and replayable.

## 5. Agents

| Agent | Responsibility | Tools (via MCP) | Can act externally? |
|---|---|---|---|
| Supervisor | Understand goal, plan, delegate, replan, stop | none directly; routes to agents | No |
| Requirement | Parse JD, extract constraints, find ambiguities, write clarification questions | `jd.parse`, `requirement.get`, `requirement.update` | No |
| Sourcing | Formulate search strategies, hybrid search, broaden optional criteria | `candidates.search_hybrid`, `candidates.get`, `memory.search_feedback` | No |
| Screening | Validate experience against the JD, with evidence | `candidates.get_resume_chunks`, `resume.parse` | No |
| Quality | Check evidence, find unsupported claims, check bias and policy | `policy.check`, `evidence.verify` | No |
| Outreach | Draft personalised messages | `templates.get`, `outreach.create_draft` | **Only after approval** (`outreach.send`, gated) |
| Delivery | Monitor ageing and bottlenecks, recommend actions | `pipeline.metrics`, `requirements.list` | No |

## 6. MVP features and priority (MoSCoW)

| ID | Feature | Priority | Sprint |
|---|---|---|---|
| F-01 | Authentication and role-based access control (Recruiter, Delivery Lead, Admin) | Must | 1 |
| F-02 | Requirement intake and JD analysis with clarification questions | Must | 1 |
| F-03 | Candidate store with synthetic dataset, embeddings, hybrid search | Must | 2 |
| F-04 | Sourcing agent with evidence retrieval | Must | 2 |
| F-05 | Multi-agent workflow (supervisor, replanning) | Must | 3 |
| F-06 | Screening report with evidence citations | Must | 3 |
| F-07 | MCP server exposing recruitment tools | Must | 4 |
| F-08 | Durable execution (checkpointing, resume after failure) | Must | 4 |
| F-09 | Long-term memory from recruiter feedback | Should | 4 |
| F-10 | Human approval gates (shortlist, outreach) | Must | 3 (basic), 5 (hardened) |
| F-11 | Guardrails: PII masking, injection defence, tool permissions, loop limits | Must | 5 |
| F-12 | Observability (Langfuse traces) and cost dashboard | Must | 5 |
| F-13 | Evaluation suite (golden dataset, Ragas or DeepEval) | Must | 5 |
| F-14 | Model routing (local / free cloud / fallback) through LiteLLM | Should | 6 |
| F-15 | Delivery agent and dashboard | Should | 6 |
| F-16 | A2A: independently deployed Talent Intelligence agent | Could | 6 |
| F-17 | Real email or WhatsApp sending | Won't (MVP) | — |

## 7. Key user journeys

**J1 — Create requirement → plan.** The recruiter pastes a JD and sets constraints. The Requirement agent returns structured requirements and clarification questions. The recruiter answers or skips them. The supervisor shows its plan.

**J2 — Run sourcing → review shortlist.** The workflow runs, and the UI shows live steps (plan, search, observation, replan). It finishes with a ranked shortlist, an evidence table for each candidate and the Quality agent's flags. The recruiter approves or rejects each candidate and gives a reason.

**J3 — Outreach.** For approved candidates, the Outreach agent drafts messages. The recruiter edits and approves. In the MVP, "send" marks the message as sent and copies it to the clipboard.

**J4 — Delivery view.** The Delivery Lead sees ageing requirements, bottleneck stages and recommended actions.

**J5 — Audit.** The Admin opens a run and sees every step, tool call, model used, tokens, cost and approval.

## 8. Success metrics

| Metric | Definition | Target |
|---|---|---|
| Agent task completion | Runs that reach a shortlist without unrecoverable error | ≥ 90% |
| Evidence accuracy | Screening claims verified against the source text (evaluation suite) | ≥ 95% |
| Recruiter acceptance | Shortlisted candidates approved | ≥ 70% |
| Unauthorised actions | External actions without an approval record | 0 |
| Hallucination rate | Claims not supported by the resume (Quality agent and evaluations) | ≤ 3% |
| Cost per requirement | Notional $ at list price (actual $0) | Tracked |
| p95 workflow latency | Requirement → shortlist on the local setup | ≤ 5 min |
| Recovery success | Interrupted runs that resume correctly | 100% in tests |

## 9. Release plan

| Release | Sprints | Outcome |
|---|---|---|
| R0 Walking skeleton | 0 | Repo, CI/CD, security scans, docs, backlog |
| R1 Single agent | 1 | Working Requirement agent |
| R2 Intelligent retrieval | 2 | Sourcing agent over hybrid search |
| R3 Multi-agent MVP | 3 | End-to-end shortlist with approval |
| R4 Stateful and tool-enabled | 4 | MCP, memory, checkpointing |
| R5 Governed | 5 | Guardrails, evaluations, observability → **pilot-ready on synthetic data** |
| R6 Enterprise-style | 6 | Routing, A2A, delivery agent, deployment → **pilot with recruiters** |

## 10. Open questions

See [requirements-gathering §4](../00-discovery/requirements-gathering.md#4-discovery-questions-and-current-answers).
