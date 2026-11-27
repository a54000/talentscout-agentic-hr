# ADR-0005: Public repository; synthetic data only in git

- **Status:** Accepted
- **Date:** 2026-11-27

## Context
GitHub CodeQL, secret scanning and unlimited Actions minutes are free only for public repositories. The repo also serves as an interview portfolio.

## Decision
The repository is public. Only synthetic, generated candidate data is committed. Real HR Guru data lives only in the local or pilot database and never in git, fixtures, logs or traces.

## Consequences
- (+) Free security tooling, visible portfolio.
- (−) Business logic is visible. No licence file is added yet, so default copyright applies (all rights reserved). The owner decides on licensing.
- Controls: gitleaks in CI, `.gitignore` for `data/real/`, a pre-commit hook, and a PR template checklist item "no real data".
