# Ways of Working (Agile Delivery Framework)

## 1. Framework
Scrum with 2-week sprints. One developer plays several roles; each hat has explicit responsibilities, so the interview story is accurate about who did what.

| Role (hat) | Responsibilities |
|---|---|
| Product Owner | Backlog ordering, acceptance criteria, sprint goal, accepting stories at review |
| Engineering Manager / Scrum Master | Capacity, ceremonies, RAID log, impediments, metrics |
| Architect | HLD, ADRs, threat model, non-functional requirements |
| Tech Lead | LLD, code reviews, quality gates, branching, CI/CD |
| Developer | Implementation with AI-assisted coding (Claude Code, Codex) |
| QA / Security | Test strategy, evaluations, security scans triage |

## 2. Cadence (per sprint)

| Day | Ceremony | Timebox | Output |
|---|---|---|---|
| Mon wk1 | Sprint planning | 1.5 h | Sprint goal, committed stories, task breakdown |
| Daily | Stand-up (written, in Jira comment or journal) | 10 min | Yesterday / today / blockers |
| Wed wk1 | Backlog refinement (next sprint) and LLD section | 1 h | Ready stories (DoR met) |
| Fri wk2 | Sprint review / demo (with a recruiter if available) | 1 h | Demo recording, feedback |
| Fri wk2 | Retrospective | 45 min | 1–2 improvement actions |

## 3. Phases and gates

The project follows the full engineering lifecycle. Each phase ends with a gate; work does not move on until the gate is passed.

| Phase | Exit gate | Evidence |
|---|---|---|
| 1 Discovery and requirements | BRD, FRD, PRD and UC-001 approved | Signed approval table in the BRD |
| 2 Solution and architecture | HLD and ADRs approved; LLD for Sprint 1 written | ADR status "Accepted" |
| 3 Engineering planning | Sprint 1 stories meet the DoR; backlog in Jira | Jira board |
| 4 Incremental development | Sprint goal met; DoD met per story | Sprint review |
| 5 AI engineering and governance | Guardrail, evaluation and security checks green; threat model reviewed | CI reports, governance review |
| 6 Deployment and pilot | Performance targets met; pilot report against baseline | Pilot report |

Gates 1–3 close in Sprint 0. Sprint 0 has **no feature code**: only the repository, CI/CD and security scanning, so that development starts on a pipeline that already works.

## 3a. Engineering principles
1. Separate repository; the existing recruitment platform is not modified.
2. Engineering documentation is version-controlled next to the code.
3. Major architecture decisions are understood and recorded as ADRs before implementation.
4. AI-generated code is reviewed line by line before it is accepted.
5. Acceptance criteria exist before development starts (DoR).
6. Security, testing and observability are part of every sprint, not a final phase.
7. Only synthetic or properly authorised candidate data is used during development.
8. No framework is added merely to demonstrate newer technology.

## 4. Definition of Ready (DoR)
- [ ] User story in "As a… I want… so that…" form
- [ ] Acceptance criteria in Given/When/Then form, including at least one failure case
- [ ] Linked FR/NFR ids
- [ ] Estimated in story points (Fibonacci: 1, 2, 3, 5, 8; split anything over 8)
- [ ] Dependencies identified; LLD section exists if the story is technical
- [ ] Security / privacy impact noted (PII? external action?)

## 5. Definition of Done (DoD)
- [ ] Code merged to `main` via PR; CI green (lint, unit, integration, security scans)
- [ ] Unit tests for new logic; failure scenario tested
- [ ] For agent and prompt changes: evaluation suite run, no regression beyond the agreed threshold
- [ ] No new high or critical vulnerabilities (CodeQL, Semgrep, Trivy, audits)
- [ ] No secrets, no real PII in code, fixtures, logs or traces
- [ ] Docs updated (LLD, README, ADR if a decision was made)
- [ ] Acceptance criteria demonstrated (on UC-001 where applicable); PO accepted

## 6. Branching and code review
- Trunk-based: short-lived branches `feat/TS-E1-04-requirement-agent`, `fix/...`, `chore/...`.
- Conventional Commits with the Jira key: `feat(agents): TS-E1-04 add repair loop`.
- `main` is protected: PR required, status checks required, no force pushes.
- Every PR has **AI review plus human review**: Claude Code `/code-review`, Codex review as a second opinion, then a human read-through using the checklist in the PR template.

## 7. Estimation and metrics
- Story points with planning-poker-style reasoning recorded in the Jira story.
- Track: velocity, sprint goal success, escaped defects, lead time (PR open → merge), change failure rate, MTTR (the DORA metrics), plus the AI metrics in the PRD.

## 8. Environments
| Env | Where | Data | Deploy |
|---|---|---|---|
| local | Mac, Docker Compose + native Ollama | synthetic | manual |
| ci | GitHub Actions | synthetic | every PR |
| demo | OCI Always Free (optional) | synthetic | auto on `main` if secrets configured |
| pilot | Mac on HR Guru network | real (after DPDP sign-off) | manual, tagged release |
