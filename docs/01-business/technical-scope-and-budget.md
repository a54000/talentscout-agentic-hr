# Technical Scope and Budget

## 1. From business scope to technical scope

| BRD scope item | Technical work packages | Epic |
|---|---|---|
| JD parsing and requirement analysis | Review and wrap existing JD parser, requirements API and UI, structured-output agent, prompt versioning, LLM router v0 | E1 |
| Resume parsing | Wrap existing resume parser in the ingestion pipeline | E2 |
| Agentic sourcing (hybrid search) | Synthetic data generator (incl. UC-001 set), chunking, masking, embeddings, Atlas indexes, RRF fusion, funnel tool, Sourcing agent | E2 |
| Intelligent search and replanning | LangGraph supervisor, bottleneck diagnosis, replanning, frozen constraints, escalation | E3 |
| Evidence-based matching | Screening and Quality agents, evidence verification | E3 |
| Human approval gates | LangGraph interrupt/resume, approval API, audit records, re-authentication | E3, E5 |
| Tools and memory | MCP server, tool scopes, MongoDB checkpointer, feedback memory | E4 |
| Safety and governance | Guardrails, PII routing, limits, threat model, DPDP pack, tamper-evident audit | E5 |
| Observability and evaluation | Langfuse, evaluation datasets, CI evaluation gate, cost dashboard | E5 |
| Agent execution dashboard | Live run view (SSE), run history, KPI aggregation, notional cost | E3, E6 |
| HR Guru ATS | Import, local Docker run, dependency patching, data recovery, Cloudflare Tunnel, backups, monitoring, hardening, read-only connector | EA |
| Interoperability and pilot | LiteLLM gateway, A2A agent (stretch), performance testing, demo deployment, pilot | E6 |
| Platform | Monorepo, Docker Compose, CI, security scans, CD, environments | E0 |

## 2. Sizing

| Epic | Stories | Story points | Sprints |
|---|---|---|---|
| EA HR Guru ATS restore and integration | 14 | 47 | 0, 1, 2 |
| E0 Inception and platform | 9 | 24 | 0, 1 |
| E1 Requirement agent | 8 | 28 | 2, 3 |
| E2 Intelligent retrieval | 7 | 29 | 3, 4 |
| E3 Multi-agent orchestration | 6 | 32 | 4, 5, 6 |
| E4 MCP and memory | 5 | 21 | 6 |
| E5 Responsible AI and LLMOps | 9 | 31 | 7, 8 |
| E6 Interop, dashboard and pilot | 7 | 27 | 8 |
| **Total** | **65** | **239** | 9 sprints × 2 weeks (to 2027-04-09) |

**Planned velocity:** 26 points per sprint. This assumes one developer at about 25 focused hours a week, assisted by Claude Code and Codex. Sprint 0 and 1 velocity will recalibrate this. Sprint 0 is over capacity by design (ATS restore was urgent) but was largely completed during inception. Sprint 1 is an ATS stabilisation sprint (re-planned 2026-11-28 at the PO's decision): TalentScout feature work starts in Sprint 2 and the plan ends 2027-04-09. TS-E5-10 (DPDP pack) is in Sprint 8; the A2A agent (TS-E6-04) is a stretch item and the first to drop if capacity is short.

## 3. Budget

### 3.1 Cash budget: **$0**

| Item | Choice | Cash cost |
|---|---|---|
| Source control, CI/CD, CodeQL, secret scanning, Dependabot, GHCR | GitHub (public repo) | $0 |
| Agile tooling | Jira Free (≤ 10 users) | $0 |
| Database and vector search | MongoDB Atlas free cluster + atlas-local Docker | $0 |
| Local LLM and embeddings | Ollama on existing MacBook M2 16 GB | $0 (owned hardware) |
| Cloud LLM | Gemini / Groq / OpenRouter free tiers (synthetic or masked data only) | $0 |
| Observability | Langfuse Cloud Hobby (50k units/month, 2 users) | $0 |
| Demo hosting (optional) | OCI Always Free ARM (2 OCPU / 12 GB) | $0 |
| Live ATS hosting | Existing Mac + Docker + Cloudflare Tunnel (free) | $0 (risk R-12) |
| AI coding assistants | Existing Claude and ChatGPT Plus subscriptions | Already paid, not project spend |
| Security tools | Trivy, gitleaks, Semgrep CE, pip-audit, npm audit | $0 |

**Cash contingency:** none. If a free tier disappears, the fallback is local-only operation (ADR-0004). Tracked as R-01.

### 3.2 Notional budget (what this would cost a client)

This is used for interview discussions and for any future commercial proposal. Rates are illustrative assumptions, not quotes.

**Effort:**

| Role | Effort (days) | Illustrative rate (₹/day) | Notional cost (₹) |
|---|---|---|---|
| Product Owner / BA | 12 | 25,000 | 3,00,000 |
| Solution Architect | 10 | 40,000 | 4,00,000 |
| Tech Lead / AI Engineer | 45 | 30,000 | 13,50,000 |
| QA / Security | 10 | 20,000 | 2,00,000 |
| **Total** | **77** | | **≈ ₹22.5 lakh** |

**Run cost at production scale** (if moved from free tiers to paid APIs). Assumptions:
- 200 requirements/month (A-02 planning figure for 25 recruiters, about 8 each).
- About 150k input and 20k output tokens per end-to-end run, including replans and evaluations.
- Example pricing: Anthropic list prices as of Nov 2026 (Sonnet 5.5 at $2 / $10 per million tokens; Haiku 5.5 at $0.10 / $0.50). Re-verify before quoting.

| Routing strategy | Cost per run | Cost per month (200 runs) |
|---|---|---|
| Everything on a mid-tier model (Sonnet 5.5) | 0.15 × $2 + 0.02 × $10 = **$0.50** | **$100** |
| Routed: 70% of tokens on Haiku 5.5, 30% on Sonnet 5.5 | ≈ **$0.17** | **≈ $34** |
| Managed DB (Atlas M10) + small VM | — | ≈ $60–80 |

The routing saving (≈ 65%) is the "token optimisation" story to tell in interviews. It is measured on the agent execution dashboard (TS-E6-03).

## 4. Out-of-scope cost drivers (deliberately excluded)

Paid job-portal APIs, WhatsApp Business API, SMS gateways, SSO providers, GPU hosting.
