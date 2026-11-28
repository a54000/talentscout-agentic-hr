# UC-002: Submission Quality Audit

**Priority 1** (PO decision, 2026-11-28). It uses only data already in the ATS, so it needs no messaging or new consent.

> **In plain words:** sourcers screen candidates themselves and then upload them into the ATS against a requirement. Today nobody systematically checks that work. TalentScout checks every submission against its requirement and against the candidate's own CV. Does the candidate really have the must-have skills? Do the experience, salary, notice and location the recruiter typed match the CV? Is this a duplicate? It produces a quality score for each submission and a scorecard for each recruiter, and a lead reviews the flags. The audit never rejects anyone by itself.

## 1. Context

- The ATS is the **system of record** for submissions: each candidate row holds `requirement_id`, `recruiter_email` / `sourcer_id`, the details the recruiter entered (`experience_years`, `key_skills`, `current_salary`, `expected_salary`, `notice_period`, `current_location`, `current_company`, `current_role`), the CV file, `status`, and the ATS's own `is_duplicate` and `missing_info` flags.
- Sourcers have already done a first screening before upload. The audit is a **second, independent check** of that work.

## 2. Actors

| Actor | Role |
|---|---|
| Delivery Lead / Quality reviewer | Reviews flagged submissions, accepts or overrides each flag, coaches recruiters |
| Recruiter / Sourcer | Sees their own scorecard and the flags on their submissions; can reply to a flag |
| Audit agents (Supervisor, Requirement, Screening, Quality) | Run the checks; never change ATS data |

## 3. Trigger

- **Automatic:** a new or changed submission arrives through the read-only ATS connector (within 10 minutes).
- **On demand:** a lead audits a requirement, a recruiter or a date range.

## 4. Checks per submission

| # | Check | How | Result |
|---|---|---|---|
| A1 | **Must-have fit** | Requirement agent turns the JD into must-haves; Screening agent finds CV evidence for each | `met` / `partially_met` / `not_met` / `unknown` per skill, with CV quotes |
| A2 | **Detail accuracy** | Compare what the recruiter entered with what the CV says: total experience, current company and role, location, key skills | `consistent` / `mismatch` / `not_in_cv` per field |
| A3 | **Constraint fit** | Entered expected CTC vs requirement budget, notice vs max notice, location vs requirement location | `within` / `outside` / `unknown` |
| A4 | **Duplicates** | Same person submitted twice (same requirement or different recruiters): email, phone, then name + company + CV similarity | `duplicate_of` link |
| A5 | **Completeness** | Required fields and CV present (reuses the ATS `missing_info` logic) | Missing fields listed |
| A6 | **Evidence check** | Quality agent verifies every quote exists in the CV (BR-7) | Unsupported claims removed |

**Submission quality score (0–100)** = weighted A1–A5 (weights configurable; default A1 40, A2 25, A3 20, A4 10, A5 5). Every deduction is explained.

## 5. Main flow

1. The connector syncs a new submission.
2. The Supervisor plans the checks. It skips A1 if the requirement has no JD, and records why.
3. The Requirement agent returns the must-haves (cached per requirement version).
4. The Screening agent scores A1 and extracts the CV facts for A2. This runs on the **local model**, because the CV is real PII (BR-4).
5. The rule engine computes A3–A5 (deterministic, no LLM).
6. The Quality agent verifies the evidence and drops unsupported claims.
7. The result is stored as an **audit record** linked to the ATS candidate and requirement ids. Nothing is written to the ATS.
8. Flags at or below the review threshold (default score < 60, or any `mismatch`) go to the lead's review queue.
9. The lead accepts or overrides each flag with a reason. The reasons are saved as feedback memory.

## 6. Alternative and failure flows

- **CV unreadable or missing:** the submission is scored `incomplete`, the reason is shown and no LLM call is made.
- **JD missing:** A1 is skipped and the score is computed from A2–A5 with that noted.
- **Local model unavailable:** the run pauses and retries. It never falls back to a cloud model with real data.
- **Recruiter disputes a flag:** the dispute thread is attached to the audit record and the lead decides.

## 7. Outputs

- An audit record per submission: checks, evidence, score and status (`clean`, `flagged`, `reviewed_ok`, `reviewed_issue`).
- A **recruiter scorecard** (weekly and monthly): submissions, average score, mismatch rate, duplicate rate, flags confirmed by leads.
- Lead dashboard: queue, trends, worst checks.

## 8. Acceptance criteria (end to end)

- Given a synthetic submission whose entered experience is 12 years and whose CV shows 6, then A2 flags `experience: mismatch` with the CV quote.
- Given a candidate submitted by two recruiters, then A4 links both submissions and the scorecard counts it once per recruiter.
- Given a clean submission, then no flag is raised and the score is ≥ 80.
- Given any audit, then no row in the ATS database changes (connector is read-only).
- Every flag shown to a lead has a supporting quote or rule (no unexplained deductions).

## 9. Rules

BR-1 (humans decide), BR-3 (protected attributes are never used), BR-4 (local model for PII), BR-7 (evidence), BR-9 (no automatic penalties: the scorecard informs coaching and never triggers automatic action against a recruiter).
