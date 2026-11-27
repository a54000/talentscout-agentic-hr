# RAID Log (Risks, Assumptions, Issues, Dependencies)

Owner: Engineering Manager. Reviewed at every sprint planning and retrospective.
Scale: Probability and Impact are rated 1 (low) to 5 (high). Score = P × I.

## Risks

| ID | Risk | P | I | Score | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| R-01 | A free tier is cut or removed (Oracle halved Always Free in June 2026; Gemini reduced free quotas) | 4 | 3 | 12 | Local-first design; LiteLLM multi-provider; everything runs on the Mac via Compose | Architect | Open |
| R-02 | Local 8B model quality too low for screening | 3 | 4 | 12 | Spike TS-E0-06; narrow PII tasks; masked summaries to cloud for reasoning; evaluation gate | Architect | Open |
| R-03 | 16 GB RAM contention (Docker + Mongo + LLM) | 4 | 2 | 8 | One model loaded at a time; Docker memory cap; native Ollama | Tech Lead | Open |
| R-04 | Atlas free 500 MB limit exceeded by embeddings | 3 | 2 | 6 | Pilot subset in Atlas; full set on atlas-local; 384-dim fallback | Architect | Open |
| R-05 | PII leaks to a cloud provider or trace | 2 | 5 | 10 | Router policy + masking + tests (TS-E1-03, TS-E5-02); no real data before DPDP sign-off | Security | Open |
| R-06 | Prompt injection via resumes | 3 | 4 | 12 | Untrusted-content handling, injection corpus evaluation, Quality agent | Security | Open |
| R-07 | Scope creep (too many frameworks, future-phase features pulled in) | 3 | 3 | 9 | One orchestration framework (ADR-0002); MoSCoW in the PRD; PO guards the sprint goal | PO | Open |
| R-08 | Recruiters unavailable for pilot or interviews | 3 | 3 | 9 | Book pilot slots in Sprint 0; async feedback form | PO | Open |
| R-09 | Solo-developer bus factor and fatigue | 3 | 3 | 9 | Docs-as-code, small PRs, sustainable 25 h/week, buffer in Sprint 6 | EM | Open |
| R-10 | Bias in recommendations | 2 | 5 | 10 | Protected attributes masked; name-swap fairness evaluation; human decides | PO | Open |

## Assumptions (validate by Sprint 2 planning)

| ID | Assumption | Validation |
|---|---|---|
| A-01 | ~40 recruitment professionals (confirmed); recruiter / delivery-lead split TBC | Director confirmation |
| A-02 | Planning figure: ~200 open requirements per month across multiple enterprise clients | ATS export |
| A-03 | Internal candidate DB (size TBC, planning figure 50k) plus job portals; Naukri only via authorised API | DB count, licence and API terms |
| A-04 | Existing JD and resume parsers are reusable as tools without modifying the existing platform | Code review (TS-E1-08) |
| A-05 | Business problems BP-1…BP-8 are the main pains (confirmed in brief); relative priority TBC | Recruiter interviews |
| A-06 | KPIs tracked: time to first submission, submission-to-interview, SLA breaches | Delivery Lead |
| A-07 | ~25 focused hours per week available for development | Sprint 0 actuals |

## Issues

| ID | Issue | Raised | Action | Status |
|---|---|---|---|---|
| I-01 | Jira project must be created manually (the tooling cannot create projects) | 2026-11-27 | Owner creates a Scrum project with key `TS`; then import the backlog | Open |
| I-02 | Discovery questions partly answered by the business brief (team size, problems, scope, KPIs, UC-001) | 2026-11-27 | Volumes, DB size and baselines still open (A-01…A-03, TS-E0-08) | Open |

## Dependencies

| ID | Dependency | Needed by | Status |
|---|---|---|---|
| D-01 | Decision: $0 cash budget | Sprint 0 | Closed (decided) |
| D-02 | Decision: deploy locally first, OCI optional | Sprint 0 | Closed (decided) |
| D-03 | Free accounts: MongoDB Atlas, Langfuse, Google AI Studio and/or Groq | Sprint 1 | Open |
| D-04 | Access to existing resume and JD parsers | Sprint 2 | Open |
| D-05 | DPDP sign-off for real-data pilot | Sprint 6 | Open |
| D-06 | 2–3 recruiters for pilot | Sprint 6 | Open |
