# ADR-0006: Single repository containing the HR Guru ATS and TalentScout

- **Status:** Accepted
- **Date:** 2026-11-27
- **Deciders:** Product Owner, Architect

## Context
- The HR Guru ATS (`a54000/hireflow`, Flask + PostgreSQL) is the live system recruiters use. Its AWS EC2 host was torn down, so it is currently unavailable and must be run locally.
- The ATS is the source of candidates and CVs for TalentScout. Naukri does not offer a profile API, so recruiters source on Naukri and upload candidates and CVs into the ATS.
- Maintaining two repositories (and the older `ATS` / `hireflow_app` copies) has already caused version drift (ATS knowledge base §18).

## Options considered
1. **Separate repositories** with a versioned integration contract. Clean ownership, but two pipelines, and drift continues.
2. **Monorepo, ATS kept as-is under `apps/ats`.** One pipeline, one place to fix, the ATS keeps its own stack (Flask, server-rendered templates).
3. **Monorepo and rewrite the ATS into MERN.** One stack, but a large, risky rewrite of a working system the business depends on.

## Decision
Option 2.
- The ATS is imported as a **snapshot** of `hireflow@990f832` into `apps/ats/`, **without git history**: the history contains real candidate data that must not be copied into a public repository.
- It keeps its Flask stack.
- TalentScout integrates with it through a defined boundary (ADR-0007), not by importing its Python modules.
- `a54000/hireflow` is frozen (archived) after the import, and all ATS changes happen here.

## Consequences
- (+) Single repository, CI/CD and security scanning for both systems. The ATS gains tests, dependency updates and image scanning it never had.
- (+) No rewrite risk. Recruiters get the system they know.
- (−) Two web stacks in one repo: MERN for TalentScout, Flask for the ATS. Accepted. The ATS UI is not rewritten in the MVP.
- (−) The ATS monolith (`app.py` ≈ 650 KB) has a security and quality backlog. Its Semgrep job is non-blocking until the baseline is triaged (TS-EA-07). Dependency CVEs are blocking from day one.
- Excluded from the import: `tools/case_001/` (real candidate data), an unreferenced personal photo, and backup copies of files.
- Action for the owner: make `a54000/hireflow` private, because its history contains candidate PII.
