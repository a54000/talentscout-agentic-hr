# HR Guru: Agentic AI Recruitment Command Centre

_Codename: TalentScout_

A goal-driven platform of supervised AI agents for HR Guru's ~40 recruitment professionals. It turns a job requirement into an evidence-backed, recruiter-approved shortlist. When the objective isn't met, it diagnoses the bottleneck and replans. It escalates instead of relaxing hiring constraints, and it learns from recruiter feedback. Recruiters stay responsible for every hiring decision.

The reference scenario is [UC-001: Intelligent Candidate Sourcing](docs/00-discovery/UC-001-intelligent-candidate-sourcing.md). The whole MVP runs on a **$0 cash budget**.

> **Status:** Sprint 0 (inception, walking skeleton). See the [sprint plan](docs/04-delivery/sprint-plan.md).

## Architecture

| Tier | Tech | Path |
|---|---|---|
| Web | React 19 + Vite + TypeScript | `apps/web` |
| API / BFF | Node 22 + Express 5 + MongoDB | `apps/api` |
| Agents | Python 3.12 + FastAPI + LangGraph | `services/agents` |
| Tools | MCP server (Node/TS), from Sprint 4 | `services/mcp-server` |
| Models | Ollama (local, PII-safe) + free cloud tiers via a PII-aware router | ADR-0004 |
| Data | MongoDB Atlas (vector + text search), Redis | ADR-0003 |

Read the [HLD](docs/03-architecture/HLD.md) for diagrams and flows.

## Documents

| Discovery and business | Product | Architecture | Delivery | Quality |
|---|---|---|---|---|
| [Requirements gathering](docs/00-discovery/requirements-gathering.md), [UC-001](docs/00-discovery/UC-001-intelligent-candidate-sourcing.md) | [PRD](docs/02-product/PRD.md) | [HLD](docs/03-architecture/HLD.md) | [Ways of working](docs/04-delivery/ways-of-working.md) | [Test and security strategy](docs/05-quality/test-and-security-strategy.md) |
| [BRD](docs/01-business/BRD.md) | [FRD](docs/02-product/FRD.md) | [LLD](docs/03-architecture/LLD.md) | [Backlog](docs/04-delivery/backlog.md) | [Threat model](docs/03-architecture/threat-model.md) |
| [Technical scope and budget](docs/01-business/technical-scope-and-budget.md) | | [ADRs](docs/03-architecture/adr/) | [Sprint plan](docs/04-delivery/sprint-plan.md), [RAID log](docs/04-delivery/RAID-log.md) | |

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
