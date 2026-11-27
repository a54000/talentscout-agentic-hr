# Technical Scope and Budget

## 1. From business scope to technical scope

| BRD scope item | Technical work packages | Epic |
|---|---|---|
| Requirement intake and JD analysis | Requirements API and UI, structured-output agent, prompt versioning, LLM router v0 | E1 |
| Agentic sourcing (hybrid search) | Synthetic data generator, chunking, masking, embeddings, Atlas indexes, RRF fusion, Sourcing agent | E2 |
| Evidence-based screening and quality | LangGraph supervisor, Screening and Quality agents, evidence verification | E3 |
| Human approval gates | LangGraph interrupt/resume, approval API, audit records, re-authentication | E3, E5 |
| Tools and memory | MCP server, tool scopes, MongoDB checkpointer, feedback memory | E4 |
| Safety and governance | Guardrails, PII routing, limits, threat model, DPDP pack, tamper-evident audit | E5 |
| Observability and evaluation | Langfuse, evaluation datasets, CI evaluation gate, cost dashboard | E5 |
| Delivery monitoring | Metrics aggregation, Delivery agent, dashboard | E6 |
| Interoperability | LiteLLM gateway, A2A agent | E6 |
| Platform | Monorepo, Docker Compose, CI, security scans, CD, environments | E0 |

## 2. Sizing

| Epic | Stories | Story points | Sprint |
|---|---|---|---|
| E0 Inception and platform | 9 | 24 | 0 |
| E1 Requirement agent | 7 | 26 | 1 |
| E2 Intelligent retrieval | 6 | 26 | 2 |
| E3 Multi-agent orchestration | 6 | 29 | 3 |
| E4 MCP and memory | 6 | 26 | 4 |
| E5 Responsible AI and LLMOps | 10 | 34 | 5 (overflow → 6) |
| E6 Interop, delivery and pilot | 6 | 24 | 6 |
| **Total** | **50** | **189** | 7 sprints × 2 weeks |

**Planned velocity:** 26 points per sprint. This assumes one developer at about 25 focused hours a week, assisted by Claude Code and Codex. Sprint 0 and 1 velocity will recalibrate this. E5 is deliberately heavy: two stories (TS-E5-09 and TS-E5-10) are planned as overflow into Sprint 6.

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
- 60 requirements/month (A-02).
- About 150k input and 20k output tokens per end-to-end run, including replans and evaluations.
- Example pricing: Anthropic list prices as of Nov 2026 (Sonnet 5.5 at $2 / $10 per million tokens; Haiku 5.5 at $0.10 / $0.50). Re-verify before quoting.

| Routing strategy | Cost per run | Cost per month (60 runs) |
|---|---|---|
| Everything on a mid-tier model (Sonnet 5.5) | 0.15 × $2 + 0.02 × $10 = **$0.50** | **$30** |
| Routed: 70% of tokens on Haiku 5.5, 30% on Sonnet 5.5 | ≈ **$0.17** | **≈ $10** |
| Managed DB (Atlas M10) + small VM | — | ≈ $60–80 |

The routing saving (≈ 65%) is the "token optimisation" story to tell in interviews. It is measured with the notional cost tracker (TS-E5-09).

## 4. Out-of-scope cost drivers (deliberately excluded)

Paid job-portal APIs, WhatsApp Business API, SMS gateways, SSO providers, GPU hosting.
