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
| Fri wk2 | Learning review | 45 min | Concept notes + interview Q&A in `docs/learning/` |

## 3. Learning loop for every story (from the project charter)
1. Understand the agentic concept.
2. Understand the business problem it solves.
3. Discuss architecture and design alternatives (record in the ADR or LLD).
4. Implement with AI-assisted coding.
5. Review the generated code (read every line; reviewer checklist below).
6. Test normal **and failure** scenarios.
7. Write interview questions and answers.

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
- [ ] Acceptance criteria demonstrated; PO accepted
- [ ] Learning note written

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
