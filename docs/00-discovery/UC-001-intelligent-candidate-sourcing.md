# UC-001: Intelligent Candidate Sourcing

This is the reference business use case. It is carried through every sprint: each new capability must work on this scenario, and it is the first end-to-end acceptance test.

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

The synthetic dataset for UC-001 (story TS-E2-01) contains 500 resumes and is generated to reproduce this funnel on the first search:

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
| 3 | Search the candidate database | Tool calling |
| 4 | Observe that only 2 candidates qualify, so the objective is not met | Observation |
| 5 | Diagnose the bottleneck: the **notice period** (12 → 2) | Reasoning over the funnel |
| 6 | Generate an alternative strategy: serving-notice candidates and alternative job titles | Replanning |
| 7 | Re-evaluate new results against the **original, unchanged** mandatory constraints | Constraint protection |
| 8 | Verify evidence for each mandatory skill per candidate | Reflection, evidence verification |
| 9 | If ≥ 5 qualify: present the shortlist for recruiter approval. If < 5: **escalate** to the recruiter with the funnel, the strategies tried, and the options that need a human decision (for example "relax notice to 45 days?") | Human-in-the-loop |

## 4. Hard rules

- The agent **cannot** relax budget, mandatory skills, experience, location or notice period on its own. It may only *propose* a relaxation, and the recruiter decides (BR-2).
- Every claim of the form "candidate has skill X" must cite resume evidence (BR-7).
- The agent makes no hiring decision and contacts no candidate (BR-1, BR-5).

## 5. Acceptance (used by TS-E3-02 and the evaluation suite)

1. **Given** the UC-001 dataset, **when** the run executes, **then** the trace shows the funnel counts per stage and names notice period as the primary bottleneck.
2. **Given** the first search returns 2 qualifying candidates, **then** the supervisor replans with at least the serving-notice and alternative-title strategies.
3. **Given** any replan, **then** the mandatory constraints in the run state are identical to the original requirement.
4. **Given** ≥ 5 qualifying candidates, **then** the shortlist shows evidence for each of the 7 mandatory skills per candidate, or marks a skill `unknown` (never `met` without evidence).
5. **Given** < 5 qualifying candidates after the allowed replans, **then** the run ends `escalated` with an explanation and decision options, not `failed`.
6. **Given** the run, **then** 100% of steps, tool calls and decisions are present in the audit trail.
