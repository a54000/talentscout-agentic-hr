# ADR-0007: The ATS is the system of record; TalentScout reads it read-only

- **Status:** Accepted
- **Date:** 2026-11-27

## Context
Recruiters (25 in the MVP) upload sourced candidates and CVs into the ATS, including candidates found on Naukri. Requirements, submissions and statuses also live in the ATS. TalentScout needs candidates, CVs and requirements as input, plus a place to record outcomes. It must never put the live ATS at risk.

## Options considered
1. **Read the ATS PostgreSQL database through a read-only role, and sync into TalentScout's own store.** No ATS code change for reads. Fast. Schema coupling is managed by a connector with contract tests.
2. **Call the ATS REST API.** It has `/api/candidates`, `/api/requirements` and more, but only session-cookie authentication and no service accounts, and large exports would load the live app.
3. **Shared database.** TalentScout writes into ATS tables. Rejected: risk to live data, no clear ownership.

## Decision
- **Reads:** Option 1. A `talentscout_reader` PostgreSQL role with `SELECT` only on the needed tables (`candidates`, `requirements`, `jd_requirements`, candidate skills and roles, submissions and statuses for feedback). The **ATS connector** in TalentScout syncs changes incrementally (`updated_at`) into TalentScout's MongoDB:
  - parsed profile fields;
  - masked resume chunks plus embeddings;
  - requirement snapshots.
  CV files are read from the ATS uploads volume, read-only.
- **Parsing:** TalentScout reuses the ATS JD and CV parsing logic (`ats_pipeline.py`, `parse_cv` / JD parsing in `app.py`, `skill_aliases.py`) through a thin, versioned wrapper, used as the `jd.parse` / `resume.parse` tools (TS-E1-08 decides the wrapping).
- **Writes back to the ATS** (for example, an approved shortlist recorded as submissions) are **out of the MVP**. When added, they go only through the ATS API with a service account, only after recruiter approval, and are audited.
- MongoDB remains TalentScout's store for derived data and agent state (ADR-0003). The ATS PostgreSQL database stays the single source of truth.

## Consequences
- (+) Zero load-bearing changes to the live ATS for the MVP. Reads cannot corrupt ATS data.
- (+) Realistic data path. The UC-001 synthetic dataset is generated **in the ATS schema**, so development and pilot use the same connector.
- (−) Schema coupling. Mitigated with connector contract tests in CI against a bootstrapped ATS schema.
- (−) Sync lag (minutes). Acceptable for sourcing.
- **PII:** ATS data is real candidate PII. All TalentScout processing of it follows ADR-0004 (local models only). Also note that the ATS itself currently sends CVs to Gemini for AI screening (`services/gemini_screening.py`). That is an existing behaviour outside TalentScout, recorded as risk R-11 for an owner decision.
