# TalentScout: Agentic AI Recruitment Command Centre

_For HR Guru. This repository also contains the HR Guru ATS (`apps/ats`)._

A goal-driven platform of supervised AI agents for HR Guru (MVP: 25 recruiters). It checks the candidates recruiters submit, confirms with the candidates that the submissions are genuine, and turns the trusted pool into client pitches. When an objective isn't met it diagnoses why and replans; it escalates instead of lowering the bar, and every message to a candidate is approved by a lead. People stay responsible for every decision.

TalentScout is the **quality and trust layer over the HR Guru ATS**: it audits every submitted candidate ([UC-002](docs/00-discovery/UC-002-submission-quality-audit.md)), verifies submissions with the candidates by WhatsApp and email ([UC-003](docs/00-discovery/UC-003-candidate-verification.md)), and reuses the trusted pool for client pitches and drives ([UC-004](docs/00-discovery/UC-004-client-pitches-and-drives.md)). The search-and-replan reference scenario is [UC-001](docs/00-discovery/UC-001-intelligent-candidate-sourcing.md). The whole MVP runs on a **$0 cash budget**.

> **Status:** Sprint 0 (inception, walking skeleton). See the [sprint plan](docs/04-delivery/sprint-plan.md).

## Architecture

| Tier | Tech | Path |
|---|---|---|
| Web | React 19 + Vite + TypeScript | `apps/web` |
| API / BFF | Node 22 + Express 5 + MongoDB | `apps/api` |
| Agents | Python 3.12 + FastAPI + LangGraph | `services/agents` |
| **HR Guru ATS** (live system of record: candidates, CVs, requirements) | Flask + PostgreSQL | `apps/ats`, [restore runbook](docs/runbooks/ats-local-restore.md) |
| Tools | MCP server (Node/TS), from Sprint 4 | `services/mcp-server` |
| Models | Ollama (local, PII-safe) + free cloud tiers via a PII-aware router | ADR-0004 |
| Data | MongoDB Atlas (vector + text search), Redis | ADR-0003 |

Read the [HLD](docs/03-architecture/HLD.md) for diagrams and flows.

## Documents

| Discovery and business | Product | Architecture | Delivery | Quality |
|---|---|---|---|---|
| [Requirements gathering](docs/00-discovery/requirements-gathering.md), [UC-001](docs/00-discovery/UC-001-intelligent-candidate-sourcing.md)–[UC-004](docs/00-discovery/UC-004-client-pitches-and-drives.md) | [PRD](docs/02-product/PRD.md) | [HLD](docs/03-architecture/HLD.md) | [Ways of working](docs/04-delivery/ways-of-working.md) | [Test and security strategy](docs/05-quality/test-and-security-strategy.md) |
| [BRD](docs/01-business/BRD.md) | [FRD](docs/02-product/FRD.md) | [LLD](docs/03-architecture/LLD.md) | [Backlog](docs/04-delivery/backlog.md), [Task checklist](docs/04-delivery/task-checklist.md) | [Threat model](docs/03-architecture/threat-model.md) |
| [Technical scope and budget](docs/01-business/technical-scope-and-budget.md) | | [ADRs](docs/03-architecture/adr/) | [Sprint plan](docs/04-delivery/sprint-plan.md), [RAID log](docs/04-delivery/RAID-log.md) | |

**New here?** Start with [How we build TalentScout](docs/06-guides/how-we-build-talentscout.md): design, build, testing, deployment and the main issues we faced.

## Getting started (macOS, Apple Silicon)

Prerequisites: Node 22, Python 3.12, Docker Desktop (cap it at 6 GB RAM), [Ollama](https://ollama.com).

Pull the local models (they run natively so they can use the Metal GPU):

```bash
ollama pull qwen3:8b
```

```bash
ollama pull nomic-embed-text
```

Create your local env file. It is git-ignored; fill in only the free-tier keys you have:

```bash
cp .env.example .env
```

Start the whole stack (web on http://localhost:8080):

```bash
docker compose up --build
```

Or develop without Docker:

```bash
npm install && npm run lint && npm test
```

```bash
cd services/agents && python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt && .venv/bin/pytest
```

## CI/CD and security

| Workflow | When | What |
|---|---|---|
| `ci.yml` | PR, push to main | Lint, type-check, tests and build for every tier; checks the backlog docs are in sync |
| `security.yml` | PR, push, weekly | CodeQL, Semgrep, gitleaks, npm audit, pip-audit, Trivy fs/IaC |
| `cd.yml` | Merge to main | Build images → Trivy scan (blocks on critical) → SBOM → push to GHCR → optional demo deploy |

## Data rules

Only **synthetic** candidate data is ever committed. Real candidate data is processed only by local models on HR Guru hardware ([ADR-0004](docs/03-architecture/adr/0004-zero-cost-model-routing.md), [ADR-0005](docs/03-architecture/adr/0005-public-repo-synthetic-data.md)).

## Licence

No licence has been chosen yet, so default copyright applies (all rights reserved).
