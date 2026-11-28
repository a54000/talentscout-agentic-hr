# UC-001: Intelligent Candidate Sourcing

This is the reference scenario for **search, funnel analysis and replanning**. Since the scope change of 2026-11-28 it is used through [UC-004: Client Pitches and Drives](UC-004-client-pitches-and-drives.md), where the agents search the audited ATS pool. The MVP's first priorities are [UC-002](UC-002-submission-quality-audit.md) (audit) and [UC-003](UC-003-candidate-verification.md) (verification).

> **In plain words:** the client wants 5 AWS Cloud Architects. We apply the hiring rules one by one to the CVs in the ATS, and most people drop out at the notice-period rule, leaving only 2. A normal search stops there. The agent should notice *where* people dropped out and try other legitimate ways to find more, such as people already serving notice or people with a different job title. It must not change the rules itself. If it still can't reach 5, it asks the recruiter what to do. **The numbers are illustrative.** We generate fake CVs that reproduce them so the behaviour can be tested.

## 1. Requirement

| Field | Value |
|---|---|
| Client | Investment Bank (fictional) |
| Role | AWS Cloud Architect |
| Experience | 12–18 years |
| Location | Gurgaon |
| Budget | ₹45 LPA (maximum) |
| Notice period | Maximum 30 days |
| Mandatory skills | AWS, Terraform, Kubernetes, networking, security, cloud migration, disaster recovery |

**Objective:** identify **five** suitable candidates, with supporting evidence for **each** mandatory skill, or explain why fewer than five could be found.

## 2. Scenario data (synthetic)

The synthetic dataset for UC-001 (story TS-E2-01) contains 500 resumes. It is generated **into the ATS schema** (a development copy of the ATS database, never the live one), so it flows through the same connector as real data. It reproduces this funnel on the first search:

| Stage | Candidates remaining |
|---|---|
| Available resumes | 500 |
| Relevant experience | 80 |
| Mandatory skills match | 25 |
| Budget match | 12 |
| Notice period match | **2** |

The dataset also contains **qualifying candidates that a first search misses**:
- candidates already serving notice, with a last working day ≤ 30 days away;
- candidates with alternative job titles (for example "Cloud Infrastructure Lead", "Principal DevOps Engineer", "Solutions Architect – AWS").

This lets the replanning step find more qualifying candidates, while still stopping short of five in some variants, so that escalation is tested too.

## 3. Expected agent behaviour

| Step | Behaviour | Agentic concept |
|---|---|---|
| 1 | Understand the goal: 5 candidates, 7 mandatory skills, budget, notice, experience, location | Goal understanding, structured output |
| 2 | Plan which tools and searches to use | Planning |
| 3 | Search the candidates synced from the ATS | Tool calling |
| 4 | Observe that only 2 candidates qualify, so the objective is not met | Observation |
| 5 | Diagnose the bottleneck: the **notice period** (12 → 2) | Reasoning over the funnel |
| 6 | Generate an alternative strategy: serving-notice candidates and alternative job titles | Replanning |
| 7 | Re-evaluate new results against the **original, unchanged** mandatory constraints | Constraint protection |
| 8 | Verify evidence for each mandatory skill per candidate | Reflection, evidence verification |
| 9 | If ≥ 5 qualify: present the shortlist for recruiter approval. If < 5: **escalate** to the recruiter with the funnel, the strategies tried, and the options that need a human decision (for example "relax notice to 45 days?") | Human-in-the-loop |

## 4. Hard rules

- The agent **cannot** relax budget, mandatory skills, experience, location or notice period on its own. It may only *propose* a relaxation, and the recruiter decides (BR-2).
- Every claim of the form "candidate has skill X" must cite resume evidence (BR-7).
- The agent makes no hiring decision and contacts no candidate in this flow (BR-1, BR-5); verification messages are a separate, approved flow (UC-003).

## 5. Acceptance (used by TS-E3-02 and the evaluation suite)

1. **Given** the UC-001 dataset, **when** the run executes, **then** the trace shows the funnel counts per stage and names notice period as the primary bottleneck.
2. **Given** the first search returns 2 qualifying candidates, **then** the supervisor replans with at least the serving-notice and alternative-title strategies.
3. **Given** any replan, **then** the mandatory constraints in the run state are identical to the original requirement.
4. **Given** ≥ 5 qualifying candidates, **then** the shortlist shows evidence for each of the 7 mandatory skills per candidate, or marks a skill `unknown` (never `met` without evidence).
5. **Given** < 5 qualifying candidates after the allowed replans, **then** the run ends `escalated` with an explanation and decision options, not `failed`.
6. **Given** the run, **then** 100% of steps, tool calls and decisions are present in the audit trail.
