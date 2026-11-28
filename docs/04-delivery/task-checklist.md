# Task Checklist

_Generated from `backlog.json` by `scripts/backlog_to_md.py`. Update a story's `status` (`todo`, `in_progress`, `blocked`, `done`) in the JSON, then re-run the script._

| Done | In progress | Blocked | To do | Deferred | Total |
|---|---|---|---|---|---|
| 14 | 1 | 0 | 71 | 1 | 87 |

## Your actions (outside the backlog)

- [x] **Refresh the Cloudflare tunnel token**: Done 2026-11-28.
- [ ] **Turn on Cloudflare Access for ats.hrgp.in** _(deferred)_: Deferred by the PO 2026-11-28 (not required at this stage). Risk R-15 accepted until ATS hardening TS-EA-07 (Sprint 1); revisit before wider rollout. Steps kept in runbook E8.
- [x] **Make a54000/hireflow private**: Done 2026-11-28 (hireflow private). Also review a54000/ATS, a54000/hrguru-ats and a54000/hireflow_app, which are still public.
- [x] **Run the ATS restore from ats.db on the Mac**: Done 2026-11-27: 9,988 candidates, 1,685 requirements restored; newest 2026-05-26.
- [x] **Create the Jira project (Scrum, key TS, name TalentScout)**: The Atlassian tools here cannot create projects; Claude imports epics, stories and sprints once it exists.
- [ ] **Decide on Gemini AI screening in the ATS (R-11)**: It sends real CVs to Gemini; options: disable, paid tier with no-training terms, or local model.
- [ ] **Review and merge the Sprint 0 and ATS pull requests**: Runs CI and all security scans on GitHub for the first time.
- [ ] **Protect main and enable secret scanning push protection**: Repo Settings → Branches and → Code security; leave CodeQL default setup off (the workflow runs it).
- [ ] **Create free accounts: MongoDB Atlas, Langfuse, Google AI Studio or Groq**: Story TS-E0-07; keys go only into the git-ignored .env.
- [ ] **Install Docker Desktop, Ollama and cloudflared on the Mac**: Docker done (ATS running). Ollama still needed for TalentScout agents (Sprint 1 spike).
- [ ] **Sign off the BRD, PRD and UC-001 (phase 1 gate)**: Approval table in the BRD.

## Sprint 0 - Inception, walking skeleton and ATS restore (2026-11-30 → 2026-12-11)

- [x] **TS-EA-01 Import ATS into the monorepo**: The ATS code in this repository, so that one pipeline builds, tests and scans everything. _(2 pts, owner: Claude, Jira TS-9)_
- [x] **TS-EA-02 Make the ATS run locally on macOS**: The ATS available again, so that I can keep uploading candidates and managing requirements. _(3 pts, owner: Claude + You, Jira TS-10)_
- [x] **TS-EA-03 Patch vulnerable ATS dependencies**: Known CVEs fixed, so that the live ATS is not exposed through old libraries. _(2 pts, owner: Claude, Jira TS-11)_
- [x] **TS-EA-04 Recover production ATS data**: The production candidates, requirements and CVs back, so that recruiters do not start from zero. _(3 pts, owner: You (script: Claude), Jira TS-12)_
- [x] **TS-EA-05 Expose the local ATS to 25 recruiters securely**: To reach the ATS from my own laptop, so that I can work as before. _(3 pts, owner: You + Claude, Jira TS-13)_
- [x] **TS-EA-06 ATS backups and restore drill**: Nightly backups and a tested restore, so that losing the host never loses data again. _(3 pts, owner: Claude + You, Jira TS-14)_
- [x] **TS-EA-09 ATS health monitoring**: To know within minutes if the ATS is down, so that recruiters are not blocked. _(2 pts, owner: Claude, Jira TS-17)_
- [x] **TS-EA-11 ATS performance quick wins: PostgreSQL indexes and multi-process serving**: The ATS to stay responsive while colleagues upload candidates, so that my work is not blocked. _(3 pts, owner: Claude + You, Jira TS-70)_
- [x] **TS-E0-01 Monorepo structure and tooling**: A monorepo with web, api and agents projects, so that all tiers build and test the same way. _(2 pts, owner: Claude, Jira TS-18)_
- [x] **TS-E0-02 CI pipeline: lint, test, build**: Every PR linted, tested and built, so that broken code never reaches main. _(3 pts, owner: Claude, Jira TS-19)_
- [x] **TS-E0-03 Security scanning pipeline**: SAST, SCA, secret and container scans on every PR, so that vulnerabilities are caught early. _(3 pts, owner: Claude, Jira TS-20)_
- [x] **TS-E0-04 CD pipeline to GHCR and demo host**: Images built, scanned and published on merge, so that every main commit is deployable. _(3 pts, owner: Claude, Jira TS-21)_
- [ ] **TS-E0-05 Docker Compose local stack** **[In progress]**: One command to start the stack, so that I can work offline on my Mac. _(2 pts, owner: Claude, Jira TS-22)_
- [ ] **TS-E0-07 Free-tier accounts and secrets handling**: Free-tier accounts set up and secrets kept out of git, so that we spend $0 and leak nothing. _(2 pts, owner: You, Jira TS-24)_
- [x] **TS-E0-09 Agile artefacts in Jira**: Epics, stories and sprints in Jira, so that delivery is tracked transparently. _(3 pts, owner: Claude, Jira TS-26)_

## Sprint 1 - ATS stabilisation (2026-12-14 → 2026-12-24)

- [x] **TS-EA-07 ATS security hardening baseline**: The most serious ATS weaknesses fixed, so that a live system with candidate PII is safe enough to run. _(5 pts, owner: Claude, Jira TS-15)_
- [ ] **TS-EA-12 Asynchronous bulk upload with progress**: My bulk upload accepted immediately and processed in the background, so that I can keep working and see progress. _(8 pts, owner: Claude, Jira TS-71)_
- [ ] **TS-EA-13 ATS performance baseline and load test**: Measured response times under realistic load, so that performance targets are verified, not assumed. _(3 pts, owner: Claude, Jira TS-72)_
- [ ] **TS-EA-14 Restore scheduled WhatsApp/email reports on the Mac**: The daily and weekly submission reports and recruiter reminders running again, so that the team keeps its routine. _(3 pts, owner: Claude + You, Jira TS-73)_
- [ ] **TS-EA-15 Delete the retired AI screening code from the ATS**: The retired AI screening and JD/CV matching code deleted from the ATS, so that dead code, the Gemini dependency and its keys are gone. _(3 pts, owner: Claude, Jira TS-95)_
- [ ] **TS-E0-06 Spike: local model selection on M2 16 GB**: To measure candidate local models, so that the PII-safe route is good enough and fast enough. _(3 pts, owner: You, Jira TS-23)_
- [ ] **TS-E0-08 Baseline measurement plan**: A baseline of recruiter effort, so that pilot results can be compared honestly. _(3 pts, owner: You, Jira TS-25)_

## Sprint 2 - Product foundation and ATS connector (2027-01-04 → 2027-01-15)

- [ ] **TS-EA-08 Read-only ATS connector**: TalentScout to see the candidates I upload to the ATS, so that agents search real, current profiles. _(5 pts, owner: Claude, Jira TS-16)_
- [ ] **TS-EA-16 Run the live ATS from the scanned GHCR images**: The Mac to run the exact images that CD built and scanned, so that what is live is what passed the security gate. _(3 pts, owner: Claude, Jira TS-96)_
- [ ] **TS-E1-01 Requirement CRUD API and UI**: To create and view requirements with constraints, so that the agents know the hiring goal. _(5 pts, owner: Claude, Jira TS-27)_
- [ ] **TS-E1-02 Authentication and RBAC**: Role-based access, so that each user sees only what they should. _(5 pts, owner: Claude, Jira TS-28)_
- [ ] **TS-E1-03 LLM router v0 with PII flag**: Every model call to go through a router that knows data sensitivity, so that PII never reaches a cloud tier. _(3 pts, owner: Claude, Jira TS-29)_
- [ ] **TS-E1-04 Requirement agent with structured output and repair loop**: The JD analysed into must-haves, constraints and ambiguities, so that sourcing starts from a clear brief. _(5 pts, owner: Claude, Jira TS-30)_
- [ ] **TS-E1-08 Review ATS JD and CV parsers and decide reuse**: The ATS parsing code reviewed, so that TalentScout reuses it through a stable wrapper instead of rebuilding it. _(2 pts, owner: Claude, Jira TS-34)_

## Sprint 3 - Single-agent completion and data (2027-01-18 → 2027-01-29)

- [ ] **TS-EA-17 One-command ATS deploy with backup, health check and rollback**: One command that backs up, deploys and checks the ATS, and rolls back on failure,, so that updates are safe and repeatable. _(5 pts, owner: Claude, Jira TS-97)_
- [ ] **TS-E1-05 Clarification questions UI**: To answer or dismiss clarification questions, so that the brief improves before sourcing. _(3 pts, owner: Claude, Jira TS-31)_
- [ ] **TS-E1-06 Audit events v0**: Every agent call recorded, so that decisions are traceable. _(2 pts, owner: Claude, Jira TS-32)_
- [ ] **TS-E1-07 Golden JD dataset and test**: 10 golden JDs with expected must-haves, so that prompt changes are measurable. _(3 pts, owner: Claude, Jira TS-33)_
- [ ] **TS-E2-01 Synthetic candidate generator incl. UC-001 scenario set**: 2,000 realistic fictional candidates, so that we can build and demo without real PII. _(5 pts, owner: Claude, Jira TS-35)_
- [ ] **TS-E2-07 Resume parsing of ATS CVs**: CVs from the ATS parsed into structured fields, so that matching uses reliable experience, notice and skills data. _(3 pts, owner: Claude, Jira TS-36)_
- [ ] **TS-E2-02 Chunking, masking and embedding pipeline**: Resumes chunked, masked and embedded locally, so that semantic search is possible safely. _(5 pts, owner: Claude, Jira TS-37)_
- [ ] **TS-E2-03 Atlas vector and text indexes**: Vector and text indexes defined as code, so that environments are reproducible. _(2 pts, owner: Claude, Jira TS-38)_

## Sprint 4 - Submission quality audit (UC-002) (2027-02-01 → 2027-02-12)

- [ ] **TS-E3-01 LangGraph supervisor graph and state**: One goal to trigger a coordinated team of agents, so that I do not orchestrate steps myself. _(5 pts, owner: Claude, Jira TS-42)_
- [ ] **TS-E3-03 Evidence-based matching per mandatory skill**: Each requirement judged with quotes from the resume, so that I can trust the score. _(5 pts, owner: Claude, Jira TS-44)_
- [ ] **TS-E7-01 Detail-accuracy check: recruiter entries vs CV**: What the recruiter typed compared with the CV, so that wrong experience, company, role, location or skills are caught before the client sees them. _(5 pts, owner: Claude, Jira TS-77)_
- [ ] **TS-E7-02 Constraint fit, completeness and quality score**: Each submission scored 0-100 with every deduction explained, so that I can prioritise reviews. _(3 pts, owner: Claude, Jira TS-78)_
- [ ] **TS-E7-03 Duplicate detection across recruiters**: The same candidate submitted by different recruiters linked, so that duplicates are not counted twice or sent twice to a client. _(3 pts, owner: Claude, Jira TS-79)_
- [ ] **TS-E7-04 Audit records and automatic audit on sync**: Every new or changed submission audited automatically, so that nothing slips through. _(3 pts, owner: Claude, Jira TS-80)_
- [ ] **TS-E7-05 Lead review queue and recruiter scorecard**: A queue of flagged submissions and a scorecard per recruiter, so that I can coach recruiters with evidence. _(5 pts, owner: Claude, Jira TS-81)_

## Sprint 5 - Audit quality and verification groundwork (2027-02-15 → 2027-02-26)

- [ ] **TS-E3-04 Quality agent evidence verification**: Unsupported claims caught before recruiters see them, so that clients get accurate submissions. _(5 pts, owner: Claude, Jira TS-45)_
- [ ] **TS-E3-05 Live run view over SSE (dashboard part 1)**: To watch the agents plan, act and replan, so that I understand what they are doing. _(3 pts, owner: Claude, Jira TS-46)_
- [ ] **TS-E3-06 Human approval gate for shortlist and escalation**: To approve or reject each shortlisted candidate with a reason, so that I remain accountable. _(6 pts, owner: Claude, Jira TS-47)_
- [ ] **TS-E5-02 PII masking and local-only routing enforcement**: PII masked and kept local, so that we comply with DPDP and provider terms. _(3 pts, owner: Claude, Jira TS-54)_
- [ ] **TS-E7-06 Golden audit dataset and precision evaluation**: Audit precision measured on labelled submissions, so that flag quality is known before leads rely on it. _(3 pts, owner: Claude, Jira TS-82)_
- [ ] **TS-E8-01 Harden the WhatsApp relay and add inbound messages**: The ATS WhatsApp relay secured and able to report replies, so that verification can use it safely. _(5 pts, owner: Claude, Jira TS-83)_
- [ ] **TS-E8-02 Opt-out and contact-consent registry**: STOP to end all messages, so that I am not contacted again. _(3 pts, owner: Claude, Jira TS-84)_

## Sprint 6 - MCP, memory, durable execution and approval controls (2027-03-01 → 2027-03-12)

- [ ] **TS-E4-01 MCP server with recruitment tools**: Recruitment capabilities exposed as MCP tools, so that any compliant agent can use them through one contract. _(5 pts, owner: Claude, Jira TS-48)_
- [ ] **TS-E4-02 Agents consume tools via MCP client**: Agents to discover tools at runtime, so that adding a tool needs no agent code change. _(3 pts, owner: Claude, Jira TS-49)_
- [ ] **TS-E4-03 Per-agent tool scopes**: Each agent limited to its tools, so that a compromised agent cannot act beyond its role. _(3 pts, owner: Claude, Jira TS-50)_
- [ ] **TS-E4-04 Durable execution with MongoDB checkpointer**: An interrupted run to continue where it stopped, so that work and quota are not wasted. _(5 pts, owner: Claude, Jira TS-51)_
- [ ] **TS-E4-05 Long-term feedback memory**: My rejection reasons remembered, so that future searches avoid the same mistakes. _(5 pts, owner: Claude, Jira TS-52)_
- [ ] **TS-E5-04 Loop, time and token limits**: Hard limits, so that runaway agents cannot burn quota or time. _(3 pts, owner: Claude, Jira TS-56)_
- [ ] **TS-E5-05 Approval-token gate on side-effecting tools**: Side-effecting tools to be impossible to run without approval, so that there are zero unauthorised actions. _(3 pts, owner: Claude, Jira TS-57)_
- [ ] **TS-E5-06 Step-up re-authentication for approvals**: Recent authentication before approvals, so that a stolen session cannot approve a shortlist or constraint relaxation. _(3 pts, owner: Claude, Jira TS-58)_

## Sprint 7 - Candidate verification (UC-003) (2027-03-15 → 2027-03-26)

- [ ] **TS-E5-10 DPDP compliance pack**: Consent, retention and erasure implemented, so that the pilot can use real data lawfully. _(3 pts, owner: Claude, Jira TS-61)_
- [ ] **TS-E8-03 Verification batches, templates and drafting**: The agent to draft verification messages for a sample I choose, so that I can review them before anything is sent. _(5 pts, owner: Claude, Jira TS-85)_
- [ ] **TS-E8-04 message.send tool with approval token, rate limits and email fallback**: Sending to be impossible without an approval token, so that no candidate is contacted without a named approver. _(5 pts, owner: Claude, Jira TS-86)_
- [ ] **TS-E8-05 Reply capture from WhatsApp and email**: Candidate replies collected automatically, so that I do not chase them by hand. _(3 pts, owner: Claude, Jira TS-87)_
- [ ] **TS-E8-06 Local reply classification and outcome comparison**: Each reply turned into an outcome compared with what the recruiter entered, so that false or wrong submissions stand out. _(5 pts, owner: Claude, Jira TS-88)_
- [ ] **TS-E8-07 Follow-up replanning, escalation and results view**: Unanswered candidates followed up once and possible false submissions escalated with evidence, so that I can decide fairly. _(5 pts, owner: Claude, Jira TS-89)_
- [ ] **TS-E8-08 Verification evaluation set**: Synthetic replies with known outcomes, so that classification accuracy is measured. _(3 pts, owner: Claude, Jira TS-90)_

## Sprint 8 - Pool retrieval, replanning and AI safety (2027-03-29 → 2027-04-09)

- [ ] **TS-E2-04 Hybrid search with RRF and filters**: Meaning-based and keyword search combined, so that I find relevant people who use different words. _(5 pts, owner: Claude, Jira TS-39)_
- [ ] **TS-E2-05 Sourcing agent with tool calling**: An agent to formulate searches from the requirement, so that I do not write boolean strings. _(5 pts, owner: Claude, Jira TS-40)_
- [ ] **TS-E2-06 Retrieval evaluation: hybrid vs keyword**: Recall@10 and nDCG@10 measured, so that the hybrid design is justified with data. _(4 pts, owner: Claude, Jira TS-41)_
- [ ] **TS-E3-02 Bottleneck diagnosis, replanning and escalation (UC-001)**: The system to recognise why the objective was not met and change strategy, without breaking my hiring constraints, and to tell me when it cannot succeed. _(8 pts, owner: Claude, Jira TS-43)_
- [ ] **TS-E5-01 Prompt-injection defence for untrusted content**: Resumes and JDs treated as data, so that embedded instructions cannot steer agents. _(5 pts, owner: Claude, Jira TS-53)_
- [ ] **TS-E5-03 Langfuse tracing and prompt versioning**: Traces and prompt versions, so that I can debug and compare agent behaviour. _(3 pts, owner: Claude, Jira TS-55)_

## Sprint 9 - Client pitches and drives (UC-004) and LLMOps (2027-04-12 → 2027-04-23)

- [ ] **TS-E5-07 Tamper-evident audit trail**: To detect altered audit events, so that the trail can be trusted. _(3 pts, owner: Claude, Jira TS-59)_
- [ ] **TS-E5-08 Evaluation gate in CI**: Evals to run on agent changes, so that quality regressions block merges. _(5 pts, owner: Claude, Jira TS-60)_
- [ ] **TS-E6-01 LiteLLM gateway with multi-provider fallback**: Routing across free providers with fallback, so that rate limits do not stop work. _(5 pts, owner: Claude, Jira TS-62)_
- [ ] **TS-E6-02 Parallel screening fan-out**: Candidates screened in parallel, so that shortlists arrive faster. _(3 pts, owner: Claude, Jira TS-63)_
- [ ] **TS-E9-01 Pitch brief and trust-ranked pool search**: To describe a pitch and get the best matches from our pool, so that we pitch candidates we can actually deliver. _(3 pts, owner: Claude, Jira TS-91)_
- [ ] **TS-E9-02 Anonymised pitch pack export**: An anonymised pitch pack, so that I can share our talent with a client without exposing candidates. _(5 pts, owner: Claude, Jira TS-92)_
- [ ] **TS-E9-03 Hiring-drive pool summary**: Counts by skill, experience band, location and notice, so that I can promise realistic numbers. _(3 pts, owner: Claude, Jira TS-93)_
- [ ] **TS-E9-04 Anonymisation leak test**: Every pitch export scanned for identifiers, so that no candidate is exposed by mistake. _(2 pts, owner: Claude, Jira TS-94)_

## Sprint 10 - Dashboard, performance and pilot (2027-04-26 → 2027-05-07)

- [ ] **TS-EA-18 Staging copy of the ATS for testing releases**: A staging ATS on the Mac with a masked copy of live data, so that releases are tried on realistic data before recruiters see them. _(3 pts, owner: Claude, Jira TS-98)_
- [ ] **TS-E6-03 Agent execution dashboard (dashboard part 2)**: Run history and KPIs in one place, so that I can see whether the agents are working and what they cost. _(5 pts, owner: Claude, Jira TS-64)_
- [ ] **TS-E6-04 A2A Talent Intelligence agent (stretch)**: An independently deployed agent reachable over A2A, so that we prove interoperability. _(5 pts, owner: Claude, Jira TS-65)_
- [ ] **TS-E6-05 Demo deployment**: A running demo on synthetic data, so that I can show the system live. _(3 pts, owner: Claude, Jira TS-66)_
- [ ] **TS-E6-07 Performance and resilience testing**: Load and failure drills, so that the pilot runs on a system with known limits. _(3 pts, owner: Claude, Jira TS-67)_
- [ ] **TS-E6-06 Recruiter pilot and results report**: A pilot report against the baseline, so that the decision to scale is evidence-based. _(3 pts, owner: You + recruiters, Jira TS-68)_

## Unscheduled (deferred) (- → -)

- [ ] **TS-EA-10 Close the post-May 2026 data gap and the missing CV/JD files** **[Deferred]**: Candidates and requirements added after 26 May 2026 recovered or re-entered, so that recruiters work from complete data. _(2 pts, owner: You, Jira TS-69)_
